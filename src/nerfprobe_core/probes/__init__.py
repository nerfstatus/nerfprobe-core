"""Probes module - organized by tier."""

from nerfprobe_core.probes.config import (
    # Base
    BaseProbeConfig,
    # Core tier
    MathProbeConfig,
    StyleProbeConfig,
    TimingProbeConfig,
    CodeProbeConfig,
    # Advanced tier
    FingerprintProbeConfig,
    ContextProbeConfig,
    RoutingProbeConfig,
    RepetitionProbeConfig,
    ConstraintProbeConfig,
    LogicPuzzleProbeConfig,
    ChainOfThoughtProbeConfig,
    # Optional tier
    CalibrationProbeConfig,
    ZeroPrintProbeConfig,
    MultilingualProbeConfig,
    # Utility
    ComparisonProbeConfig,
    FactProbeConfig,
)

# Core tier probes
from nerfprobe_core.probes.core import (
    MathProbe,
    StyleProbe,
    TimingProbe,
    CodeProbe,
)

# Advanced tier probes
from nerfprobe_core.probes.advanced import (
    FingerprintProbe,
    ContextProbe,
    RoutingProbe,
    RepetitionProbe,
    ConstraintProbe,
    LogicProbe,
    ChainOfThoughtProbe,
)

# Optional tier probes
from nerfprobe_core.probes.optional import (
    CalibrationProbe,
    ZeroPrintProbe,
    MultilingualProbe,
)

# Tier definitions for CLI --tier flag
CORE_PROBES = ["math", "style", "timing", "code"]
ADVANCED_PROBES = [
    "fingerprint",
    "context",
    "routing",
    "repetition",
    "constraint",
    "logic",
    "cot",
]
OPTIONAL_PROBES = ["calibration", "zeroprint", "multilingual"]

ALL_PROBES = CORE_PROBES + ADVANCED_PROBES + OPTIONAL_PROBES

# Probe class registry
PROBE_REGISTRY = {
    # Core
    "math": MathProbe,
    "style": StyleProbe,
    "timing": TimingProbe,
    "code": CodeProbe,
    # Advanced
    "fingerprint": FingerprintProbe,
    "context": ContextProbe,
    "routing": RoutingProbe,
    "repetition": RepetitionProbe,
    "constraint": ConstraintProbe,
    "logic": LogicProbe,
    "cot": ChainOfThoughtProbe,
    # Optional
    "calibration": CalibrationProbe,
    "zeroprint": ZeroPrintProbe,
    "multilingual": MultilingualProbe,
}

__all__ = [
    # Configs
    "BaseProbeConfig",
    "MathProbeConfig",
    "StyleProbeConfig",
    "TimingProbeConfig",
    "CodeProbeConfig",
    "FingerprintProbeConfig",
    "ContextProbeConfig",
    "RoutingProbeConfig",
    "RepetitionProbeConfig",
    "ConstraintProbeConfig",
    "LogicPuzzleProbeConfig",
    "ChainOfThoughtProbeConfig",
    "CalibrationProbeConfig",
    "ZeroPrintProbeConfig",
    "MultilingualProbeConfig",
    "ComparisonProbeConfig",
    "FactProbeConfig",
    # Probe classes
    "MathProbe",
    "StyleProbe",
    "TimingProbe",
    "CodeProbe",
    "FingerprintProbe",
    "ContextProbe",
    "RoutingProbe",
    "RepetitionProbe",
    "ConstraintProbe",
    "LogicProbe",
    "ChainOfThoughtProbe",
    "CalibrationProbe",
    "ZeroPrintProbe",
    "MultilingualProbe",
    # Tier lists
    "CORE_PROBES",
    "ADVANCED_PROBES",
    "OPTIONAL_PROBES",
    "ALL_PROBES",
    "PROBE_REGISTRY",
]
