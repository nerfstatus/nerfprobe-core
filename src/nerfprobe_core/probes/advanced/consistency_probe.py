from typing import Any
import time

from nerfprobe_core.core.entities import ModelTarget, ProbeResult, ProbeType
from nerfprobe_core.core.scorer import ProbeProtocol, CostEstimate
from nerfprobe_core.core.gateway import LLMGateway
from nerfprobe_core.probes.config import ConsistencyProbeConfig
from nerfprobe_core.scorers.consistency_scorer import ConsistencyScorer

class ConsistencyProbe(ProbeProtocol):
    """
    Detects self-contradiction or lack of fact permanence using ConsistencyScorer.
    Formerly ContradictionProbe.
    """
    
    def __init__(self, config: ConsistencyProbeConfig):
        self._config = config
        self._scorer = ConsistencyScorer(
            consistency_type=config.consistency_type,
            expect_match=config.expect_match
        )

    @property
    def config(self) -> ConsistencyProbeConfig:
        return self._config

    @property
    def estimated_cost(self) -> CostEstimate:
        return CostEstimate(input_tokens=100, output_tokens=100) # 2 turns

    async def run(self, target: ModelTarget, generator: LLMGateway) -> ProbeResult:
        # Enforce Token Budget
        if self.config.max_tokens_per_run > 0 and self.estimated_cost.total_tokens > self.config.max_tokens_per_run:
             return ProbeResult(
                probe_name=self.config.name,
                probe_type=ProbeType.HALLUCINATION,
                target=target,
                passed=False,
                score=0.0,
                latency_ms=0.0,
                raw_response="SKIPPED: Exceeds token budget",
                metadata={"error": "Token budget exceeded"}
            )
        start = time.perf_counter()
        
        try:
            # Turn 1
            resp1 = await generator.generate(target, self.config.prompt1)
            
            # Turn 2
            resp2 = await generator.generate(target, self.config.prompt2)
            
            latency_ms = (time.perf_counter() - start) * 1000
        except Exception as e:
            err_msg = str(e)
            reason = "Error"
            if "429" in err_msg:
                reason = "Rate Limit"
            elif "401" in err_msg:
                reason = "Auth Error"
            elif "500" in err_msg or "503" in err_msg:
                reason = "Server Error"

            return ProbeResult(
                probe_name=self.config.name,
                probe_type=ProbeType.HALLUCINATION,
                target=target,
                passed=False,
                score=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                raw_response=f"ERROR: {str(e)}",
                error_reason=reason,
                metadata={"error": str(e)}
            )

        responses = [resp1, resp2]
        score = self._scorer.score(responses)
        metrics = self._scorer.metrics(responses)
        passed = score == 1.0
        

        # Calculate usage
        u1 = getattr(resp1, "usage", {})
        u2 = getattr(resp2, "usage", {})
        input_tokens = u1.get("prompt_tokens", 0) + u2.get("prompt_tokens", 0)
        output_tokens = u1.get("completion_tokens", 0) + u2.get("completion_tokens", 0)
        
        failure_reason = None
        if not passed:
             sim = metrics.get('similarity', 0.0)
             if self.config.expect_match:
                 failure_reason = f"Mismatch (Sim: {sim:.2f})"
             else:
                 failure_reason = f"Should mismatch (Sim: {sim:.2f})"

        return ProbeResult(
            probe_name=self.config.name,
            probe_type=ProbeType.HALLUCINATION,
            target=target,
            passed=passed,
            score=score,
            latency_ms=latency_ms,
            raw_response=f"A1: {resp1} | A2: {resp2}",
        
            # Calculate usage
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            error_reason=failure_reason,
            
            metric_scores={
                "similarity": metrics["similarity"]
            },
            metadata={
                "research_ref": "[2504.04823]",
                "config": self.config.model_dump(),
                "answer1": metrics["answer1"],
                "answer2": metrics["answer2"]
            }
        )
