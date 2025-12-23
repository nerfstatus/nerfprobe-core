"""
ChainOfThoughtProbe - CoT reliability and error accumulation detection.

Ref: [2504.04823]
"""

import time

from nerfprobe_core.core import (
    CostEstimate,
    LLMGateway,
    ModelTarget,
    ProbeResult,
    ProbeType,
)
from nerfprobe_core.probes.config import ChainOfThoughtProbeConfig
from nerfprobe_core.scorers.cot import ChainOfThoughtScorer


class ChainOfThoughtProbe:
    """
    Detects degradation in reasoning chains (circularity, shallowness).
    Analyzes step structure and repetition patterns.
    """

    def __init__(self, config: ChainOfThoughtProbeConfig):
        self._config = config
        self._scorer = ChainOfThoughtScorer(
            min_steps=config.min_steps,
            detect_circular=config.detect_circular,
        )

    @property
    def config(self) -> ChainOfThoughtProbeConfig:
        return self._config

    @property
    def estimated_cost(self) -> CostEstimate:
        return CostEstimate(input_tokens=100, output_tokens=400)

    async def run(self, target: ModelTarget, generator: LLMGateway) -> ProbeResult:
        if self.config.max_tokens_per_run > 0 and self.estimated_cost.total_tokens > self.config.max_tokens_per_run:
            return ProbeResult(
                probe_name=self.config.name,
                probe_type=ProbeType.REASONING,
                target=target,
                passed=False,
                score=0.0,
                latency_ms=0.0,
                raw_response="SKIPPED: Exceeds token budget",
                metadata={"error": "Token budget exceeded"},
            )

        start = time.perf_counter()
        response_text = ""

        try:
            response_text = await generator.generate(target, self.config.prompt)
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
                probe_type=ProbeType.REASONING,
                target=target,
                passed=False,
                score=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                raw_response=f"ERROR: {e!s}",
                error_reason=reason,
                metadata={"error": str(e)},
            )

        score = self._scorer.score(response_text)
        metrics = self._scorer.metrics(response_text)
        passed = score == 1.0

        # Extract usage
        usage = getattr(response_text, "usage", {})
        input_tokens = usage.get("prompt_tokens")
        output_tokens = usage.get("completion_tokens")

        failure_reason = None
        if not passed:
            if metrics["is_circular"]:
                failure_reason = "Circular reasoning detected"
            elif metrics["step_count"] < self.config.min_steps:
                failure_reason = f"Too few steps ({metrics['step_count']} < {self.config.min_steps})"
            else:
                failure_reason = "CoT Reasoning Failed"

        return ProbeResult(
            probe_name=self.config.name,
            probe_type=ProbeType.REASONING,
            target=target,
            passed=passed,
            score=score,
            latency_ms=latency_ms,
            raw_response=str(response_text),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            error_reason=failure_reason,
            metric_scores={
                "step_count": float(metrics["step_count"]),
                "is_circular": 1.0 if metrics["is_circular"] else 0.0,
            },
            metadata={
                "research_ref": "[2504.04823]",
                "config": self.config.model_dump(),
                "steps_extracted": metrics.get("steps_extracted", []),
            },
        )
