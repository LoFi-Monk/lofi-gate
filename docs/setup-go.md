# Setup: Go

## 1. Install LoFi Gate

Install the package (requires Python 3.8+):

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

Go developers typically use a `Makefile`.

**Makefile:**

```makefile
verify:
    lofi-gate verify --parallel
```

## 4. Verify

Run the gate manually:

```bash
lofi-gate verify
```
