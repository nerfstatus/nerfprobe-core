"""
LogicProbe - GSM8k-style reasoning drift detection.

Ref: [2504.04823] Q-Hurts-Reasoning
"""

import time

from nerfprobe_core.core import (
    CostEstimate,
    LLMGateway,
    ModelTarget,
    ProbeResult,
    ProbeType,
)
from nerfprobe_core.probes.config import LogicPuzzleProbeConfig
from nerfprobe_core.scorers.logic import LogicScorer


class LogicProbe:
    """
    Detects reasoning drift (correct answer, wrong path).
    Checks both final answer and intermediate reasoning steps.
    """

    def __init__(self, config: LogicPuzzleProbeConfig):
        self._config = config
        self._scorer = LogicScorer(
            expected_answer=config.expected_answer,
            required_reasoning=config.required_reasoning,
        )

    @property
    def config(self) -> LogicPuzzleProbeConfig:
        return self._config

    @property
    def estimated_cost(self) -> CostEstimate:
        return CostEstimate(input_tokens=150, output_tokens=300)

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
            if not metrics.get("has_answer"):
                failure_reason = "No final answer found"
            elif metrics.get("missing_steps"):
                failure_reason = f"Missing steps: {len(metrics['missing_steps'])}"
            else:
                failure_reason = "Reasoning incorrect"

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
                "reasoning_completeness": metrics["reasoning_completeness"],
            },
            metadata={
                "research_ref": "[2504.04823]",
                "config": self.config.model_dump(),
                "missing_steps": metrics.get("missing_steps", []),
                "has_answer": metrics.get("has_answer", False),
            },
        )
