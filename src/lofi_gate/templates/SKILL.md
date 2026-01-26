---
name: lofi-gate
description: A "Physics-based" verification gate that ensures code quality and TDD compliance.
---

# LoFi Gate: The Dojo Rules

> "Physics over Law. If the build breaks, you stop."

## 1. The Constitution

As an Agent in this workspace, you are bound by these physical laws:

1.  **Red-Green-Refactor**: You MUST write tests _before_ implementation.
2.  **No Broken Windows**: You typically cannot proceed if the `judge` returns a FAILURE exit code.
3.  **Trust the Physics**: If the `judge` says it failed, it failed. Do not argue. Fix the code.

## 2. Tools

### `judge`

Runs the verification suite (Tests, Lint, Security, TDD Check).

**Usage**:
Run this python script at the root of the workspace.

```bash
python .agent/skills/lofi-gate/judge.py
```

**Interpretation**:

- **Exit Code 0**: SUCCESS. You may proceed.
- **Exit Code 1**: FAILURE. Read the output. The error log is truncated to show the "Head" and "Tail" of the error.

## 3. Logs

A history of all verification runs is stored in `verification_history.md` in the project root.

- Use this to see if you are making progress or regressing.
- Check the "Total Token Savings" to see how efficient you are being.
