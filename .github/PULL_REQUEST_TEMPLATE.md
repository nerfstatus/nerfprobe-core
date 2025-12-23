## Description

<!-- Brief summary of what this PR adds/changes -->

**Related Issue:** #
**Research Paper:** <!-- e.g., [2407.15847] LLMmap -->

---

## Type of Change

- [ ] **New Probe** — Adds a new detection probe
- [ ] **New Scorer** — Adds reusable scoring logic
- [ ] **Enhancement** — Improves existing probe/scorer
- [ ] **Bug Fix** — Fixes incorrect behavior
- [ ] **Documentation** — Updates docs only
- [ ] **CI/Tooling** — Build, test, or dev workflow changes

---

## Research Citation Checklist

> All probes must be grounded in academic research.

- [ ] Paper reference included in module docstring
- [ ] ArXiv/ACL link added to README probe table (if new probe)
- [ ] `research_ref` field populated in `ProbeResult.metadata`
- [ ] Detection methodology matches paper's approach

**Paper Citation Example:**
```python
"""
FingerprintProbe - Framework/model fingerprinting via error templates.

Ref: [2407.15847] LLMmap
"""
```

---

## Architecture Alignment Checklist

### For New Probes

- [ ] **Config class** added to `src/nerfprobe_core/probes/config.py`
  - Extends `BaseProbeConfig`
  - Includes research reference in docstring
  - Defines `max_tokens_per_run` budget

- [ ] **Probe class** placed in correct tier directory:
  - `probes/core/` — Essential, <100 tokens
  - `probes/advanced/` — Complex, multiple API calls
  - `probes/optional/` — Requires logprobs or heavy deps

- [ ] **Registration** in `probes/__init__.py`:
  - Added to tier list (`CORE_PROBES`, `ADVANCED_PROBES`, or `OPTIONAL_PROBES`)
  - Added to `PROBE_REGISTRY` dict
  - Added to `__all__` exports

- [ ] **ProbeProtocol** implemented correctly:
  ```python
  @property
  def config(self) -> MyProbeConfig: ...

  @property
  def estimated_cost(self) -> CostEstimate: ...

  async def run(self, target: ModelTarget, generator: LLMGateway) -> ProbeResult: ...
  ```

- [ ] **ProbeResult** populated with all fields:
  - `probe_name`, `probe_type`, `target`
  - `score` (0.0–1.0), `passed` (bool)
  - `latency_ms`, `input_tokens`, `output_tokens`
  - `error_reason` (if failed)
  - `metadata` with `research_ref`

### For New Scorers

- [ ] **Scorer class** added to `src/nerfprobe_core/scorers/`
- [ ] **ScorerProtocol** implemented:
  ```python
  def score(self, response: Any) -> float: ...
  def metrics(self, response: Any) -> dict[str, Any]: ...
  ```
- [ ] Scorer is **pure logic** (no LLM calls, no side effects)
- [ ] Exported in `scorers/__init__.py`

---

## Code Quality Checklist

> All checks must pass before merge. Pre-commit hooks enforce these automatically.

- [ ] **Linting**: `uv run ruff check .` passes
- [ ] **Formatting**: `uv run ruff format .` applied
- [ ] **Type Checking**: `uv run mypy src` passes with no errors
- [ ] **Tests**: `uv run pytest` passes

### Pre-commit Setup
```bash
pip install pre-commit
pre-commit install
# Now hooks run automatically on commit
```

---

## Test Coverage Checklist

- [ ] **Unit tests** added in `tests/unit/test_<name>_probe.py`
- [ ] Tests cover:
  - [ ] Scoring logic with mock responses
  - [ ] Edge cases (empty response, malformed input)
  - [ ] Failure modes (API errors, budget exceeded)
  - [ ] Token usage tracking
- [ ] All tests pass: `uv run pytest tests/unit/test_<name>_probe.py -v`

**Example Test Structure:**
```python
import pytest
from nerfprobe_core.probes import NewProbe, NewProbeConfig

def test_probe_scoring_logic():
    config = NewProbeConfig(...)
    probe = NewProbe(config)
    # Test scorer directly with mock response
    ...

@pytest.mark.asyncio
async def test_probe_run():
    # Test full probe execution with mock gateway
    ...
```

---

## Documentation Checklist

- [ ] **README.md** updated if adding new probe:
  - Added to correct tier table
  - Paper link included
  - Detection target documented

- [ ] **CONTRIBUTING.md** still accurate (no breaking changes to workflow)

- [ ] **Docstrings** complete:
  - Module-level docstring with paper reference
  - Class docstring explaining purpose
  - Method docstrings for public API

---

## Token Usage & Performance

**Estimated cost per execution:**
- Input tokens: <!-- e.g., 100 -->
- Output tokens: <!-- e.g., 200 -->
- Total: <!-- e.g., 300 -->

**Number of API calls:** <!-- e.g., 1, 3 for multi-check probes -->

**Performance considerations:**
<!-- Any caching, batching, or optimization notes? -->

---

## Screenshots/Examples (if applicable)

<!-- Show example output, CLI results, or test runs -->

```
$ nerfprobe run gpt-4o --probes new_probe
┌─────────────┬────────┬───────┬──────────┐
│ Probe       │ Score  │ Pass? │ Latency  │
├─────────────┼────────┼───────┼──────────┤
│ new_probe   │ 0.85   │ ✓     │ 234ms    │
└─────────────┴────────┴───────┴──────────┘
```

---

## Reviewer Notes

<!-- Any context for reviewers? Tricky decisions? Alternative approaches considered? -->
