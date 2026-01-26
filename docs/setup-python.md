# Setup: Python

## 1. Install Requirements

Ensure you have Python 3.8+ installed.

## 2. Copy the Script

Copy `lofi_gate.py` to your project root or `scripts/` folder.

## 3. Configure `pyproject.toml` (if using Poetry/PDM)

You can use `taskipy` or similar tools to map the command.

```toml
[tool.taskipy.tasks]
lofi-gate = "python lofi_gate.py --parallel"
test = "task lofi-gate"
```

## 4. Configure `test:agent`

LoFi Gate looks for a specific pattern to run optimized tests.

If using `pytest`, you can use `pytest-testmon` or similar packages to run only affected tests, or simply default to standard pytest if optimization isn't set up yet.

## 5. Verify

Run the gate manually:

```bash
python lofi_gate.py --parallel
```
