# Setup: Python

## 1. Install LoFi Gate

Install the package:

```bash
pip install lofi-gate
```

## 2. Initialize Physics

Scaffold the configuration into your workspace:

```bash
lofi-gate init
```

_This creates `.agent/skills/lofi-gate/`._

## 3. Configure Workflow

You can run `lofi-gate verify` directly, or wrap it in a `Makefile` or `pyproject.toml` script (if using `pdm` or `poetry`).

**Example Makefile:**

```makefile
test:
    lofi-gate verify --parallel
```

## 4. Verify

Run the gate manually:

```bash
lofi-gate verify
```
