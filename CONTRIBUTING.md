# Contributing to NerfProbe

Thank you for your interest in contributing to **NerfProbe**! We are building the industry standard for specific, scientific LLM degradation detection.

## Development Setup

This project uses `uv` for dependency management and `hatchling` for building.

### Prerequisites

- Python 3.11 or higher
- `uv` (Universal Python Packager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/skew202/nerfprobe-core.git
   cd nerfprobe-core
   ```

2. Install dependencies:
   ```bash
   uv sync --all-extras --dev
   ```

## Running Tests

We use `pytest` for unit and integration testing.

```bash
uv run pytest
```

To run a specific test file:
```bash
uv run pytest tests/unit/test_core_probes.py
```

## Code Quality

We enforce strict code quality standards using `ruff` and `mypy`. CI will fail if these checks do not pass.

### Linting & Formatting

```bash
# Check for linting errors
uv run ruff check .

# Fix auto-fixable errors
uv run ruff check --fix .

# format code
uv run ruff format .
```

### Type Checking

```bash
uv run mypy src
```

## Creating a New Probe

1. **Research**: Identify a specific, cited paper or phenomenon you want to detect.
2. **Design**:
   - Create a `Config` class in `src/nerfprobe_core/probes/config.py`.
   - Create a `Probe` class in `src/nerfprobe_core/probes/<tier>/<name>_probe.py`.
   - (Optional) Create a reusable `Scorer` in `src/nerfprobe_core/scorers/`.
3. **Register**: Add your probe to `src/nerfprobe_core/probes/__init__.py`.
4. **Test**: Add unit tests in `tests/`.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue a PR with a clear description of the research grounding (links to Arxiv papers are highly encouraged).

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.
