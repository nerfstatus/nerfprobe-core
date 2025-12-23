"""NerfProbe Core - Shared probe and scorer implementations."""

from nerfprobe_core.core.entities import (
    LogprobResult,
    LogprobToken,
    ModelTarget,
    ProbeResult,
    ProbeType,
    ProviderType,
    StrWithUsage,
)
from nerfprobe_core.core.gateway import LLMGateway
from nerfprobe_core.core.scorer import CostEstimate, ProbeProtocol, ScorerProtocol
from nerfprobe_core.models import ModelInfo, get_model_info, list_models
from nerfprobe_core.models.research import RESEARCH_PROMPT, get_research_prompt

__all__ = [
    "MetricResult",
    "ModelTarget",
    "ProbeResult",
    "ProbeType",
    "ProviderType",
    "LogprobToken",
    "LogprobResult",
    "StrWithUsage",
    # Protocols
    "LLMGateway",
    "ScorerProtocol",
    "ProbeProtocol",
    "CostEstimate",
    # Models
    "ModelInfo",
    "get_model_info",
    "list_models",
    "RESEARCH_PROMPT",
    "get_research_prompt",
]

__version__ = "0.1.0"
