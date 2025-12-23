---
name: New Probe/Scorer Proposal
about: Propose a new scientific probe or scorer based on research
title: '[PROBE] '
labels: enhancement, research
---

## Research Grounding

> All probes must be grounded in specific academic research. Please provide the paper reference.

**Paper Citation:**
<!-- Example: [2407.15847] LLMmap: Fingerprinting LLMs -->

**ArXiv/ACL Link:**
<!-- Example: https://arxiv.org/abs/2407.15847 -->

**Key Finding from Paper:**
<!-- What specific phenomenon does this paper document? -->

---

## Detection Target

**What degradation does this probe detect?**
<!-- e.g., "Detects quantization-induced arithmetic errors via multi-digit addition tests" -->

**Observable Signal:**
<!-- What measurable output difference indicates this degradation? -->

**Detection Confidence:**
<!-- How reliably can this be detected? Are there false positive concerns? -->

---

## Proposed Implementation

### Tier Classification

- [ ] **Core** — Essential, low-cost (<100 tokens), foundational signal
- [ ] **Advanced** — Complex detection, multiple API calls, structural integrity
- [ ] **Optional** — Requires logprobs, heavy dependencies, or experimental

**Justification for tier choice:**

### Methodology

**How will the paper's technique be adapted?**
<!-- Describe the specific prompts, scoring logic, and thresholds -->

**Number of API calls required:**

**Estimated token cost:**
<!-- Input tokens + output tokens per execution -->

---

## API Design Sketch

### Config Class
```python
class NewProbeConfig(BaseProbeConfig):
    """
    Brief description.
    Ref: [PAPER_ID] Paper Title
    """
    name: str = "new_probe"
    # Add probe-specific parameters
```

### Expected ProbeResult.metadata
```python
{
    "research_ref": "[PAPER_ID]",
    # What additional metadata will this probe produce?
}
```

---

## Architecture Reference

> New contributors: Please review this architecture before implementing.

```
nerfprobe-core/src/nerfprobe_core/
├── core/
│   ├── entities.py    # ProbeResult, ModelTarget, ProbeType enum
│   ├── gateway.py     # LLMGateway protocol (async generate())
│   └── scorer.py      # ProbeProtocol, ScorerProtocol, CostEstimate
├── probes/
│   ├── config.py      # All *ProbeConfig classes (add yours here)
│   ├── core/          # Essential tier: math, style, timing, code, fact
│   ├── advanced/      # Structural: fingerprint, context, routing, etc.
│   └── optional/      # Experimental: calibration, zeroprint, multilingual
├── scorers/           # Reusable pure-logic scoring components
└── models/            # Model metadata and research utilities
```

### Key Protocols

**ProbeProtocol** (what your probe must implement):
```python
@property
def config(self) -> BaseProbeConfig: ...

@property
def estimated_cost(self) -> CostEstimate: ...

async def run(self, target: ModelTarget, generator: LLMGateway) -> ProbeResult: ...
```

**ScorerProtocol** (optional, for reusable scoring logic):
```python
def score(self, response: Any) -> float: ...      # 0.0–1.0 normalized
def metrics(self, response: Any) -> dict: ...     # Detailed breakdown
```

---

## Research Paper Categories

Reference papers from our documentation:

| Category | Key Papers | Detection Focus |
|----------|------------|-----------------|
| **Quantization** | [2403.06408], [2411.17525], [2504.04823] | PPL paradox, vocabulary collapse, reasoning degradation |
| **Fingerprinting** | [2407.15847] LLMmap, [2502.20589] | Error templates, timing rhythms |
| **Routing Detection** | [2406.18665] RouteLLM | Difficulty gap analysis |
| **Context Degradation** | [2512.12008] | KV cache compression, middle-depth failure |
| **Instruction Following** | [2409.11055] | Constraint adherence, format compliance |

---

## Checklist

- [ ] I have identified a specific academic paper
- [ ] The detection target is clearly defined
- [ ] This does not duplicate an existing probe
- [ ] I have considered the appropriate tier
- [ ] I am willing to implement this (or seeking a collaborator)
