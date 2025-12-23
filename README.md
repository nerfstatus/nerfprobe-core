# NerfProbe Core

**Scientifically-grounded LLM degradation detection.**

`nerfprobe-core` provides the essential detection logic, scorers, and probe definitions used by the [NerfProbe CLI](https://pypi.org/project/nerfprobe/) and [NerfStatus](https://nerfstatus.com). It is designed for developers who need rigorous, research-backed instruments to measure model quality, consistency, and alignment.

## Installation

```bash
pip install nerfprobe-core
```

## Features

- **17 Research-Backed Probes**: Detection instruments grounded in specific academic papers on model collapse and quantization artifacts.
- **3-Tier Architecture**: Organized into Core (Essential), Advanced (Structural), and Optional (Experimental) tiers.
- **Universal Scoring**: Reusable scorers (JSON schema validation, TTR, Fact verification) independent of the probe execution.
- **Type-Safe**: Fully typed with Python 3.11+, leveraging Pydantic for configuration and results.

## Probes

### Core Tier (Essential Signals)
| Probe | Detection Target | Paper |
|-------|------------------|-------|
| **MathProbe** | Arithmetic reasoning degradation | [2504.04823](https://arxiv.org/abs/2504.04823) |
| **StyleProbe** | Vocabulary collapse (Type-Token Ratio) | [2403.06408](https://arxiv.org/abs/2403.06408) |
| **TimingProbe** | Latency fingerprinting & TTFT degradation | [2502.20589](https://arxiv.org/abs/2502.20589) |
| **CodeProbe** | Syntax collapse in generated code | [2512.08213](https://arxiv.org/abs/2512.08213) |
| **FactProbe** | Factual recall and hallucination checks | N/A |

### Advanced Tier (Structural Integrity)
| Probe | Detection Target | Paper |
|-------|------------------|-------|
| **JsonProbe** | JSON schema adherence & structure | [2402.16775](https://arxiv.org/abs/2402.16775) |
| **ConsistencyProbe**| Fact permanence & self-contradiction | [2504.04823](https://arxiv.org/abs/2504.04823) |
| **FingerprintProbe**| Underlying framework/model identity detection | [2407.15847](https://arxiv.org/abs/2407.15847) |
| **ContextProbe** | Key-Value cache compression artifacts | [2512.12008](https://arxiv.org/abs/2512.12008) |
| **RoutingProbe** | MoE routing path detection | [2406.18665](https://arxiv.org/abs/2406.18665) |
| **RepetitionProbe** | Loop detection & phrase repetition | [2403.06408](https://arxiv.org/abs/2403.06408) |
| **ConstraintProbe** | Negative constraint adherence | [2409.11055](https://arxiv.org/abs/2409.11055) |
| **LogicProbe** | Reasoning step validity | [2504.04823](https://arxiv.org/abs/2504.04823) |
| **ChainOfThoughtProbe** | CoT step integrity | [2504.04823](https://arxiv.org/abs/2504.04823) |

### Optional Tier (Experimental)
| Probe | Detection Target | Paper |
|-------|------------------|-------|
| **CalibrationProbe**| Confidence score calibration | [2511.07585](https://arxiv.org/abs/2511.07585) |
| **ZeroPrintProbe** | Mode collapse via entropy measurement | [2407.01235](https://arxiv.org/abs/2407.01235) |
| **MultilingualProbe**| Cross-language performance asymmetry | [EMNLP.935](https://aclanthology.org/2023.findings-emnlp.935/) |

## Usage

### Basic Probe Execution

```python
import asyncio
from nerfprobe_core import ModelTarget
from nerfprobe_core.probes import MathProbe
from nerfprobe_core.probes.config import MathProbeConfig

# 1. Configure the probe
config = MathProbeConfig(
    prompt="Calculate 15 * 12 + 8.",
    expected_answer="188",
)

# 2. Define the target
target = ModelTarget(provider_id="openai", model_name="gpt-4o")

# 3. Instantiate and run (requires an LLM Gateway)
probe = MathProbe(config)
# result = await probe.run(target, gateway)

# print(result.summary())
# > math_probe: PASS (1.00) in 234ms
```

### Using Scorers Directly

You can use the scoring logic without the full probe infrastructure:

```python
from nerfprobe_core.scorers import JsonScorer

scorer = JsonScorer(strict=True)
valid_json = '{"name": "NerfProbe"}'
invalid_json = '```json{"name": "NerfProbe"}```'

score, metadata = scorer.score(valid_json)
print(f"Score: {score}") # 1.0

score, metadata = scorer.score(invalid_json)
print(f"Score: {score}") # 0.0 (Strict mode rejects markdown blocks)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up the development environment, run tests, and submit PRs.

## License

Apache-2.0
