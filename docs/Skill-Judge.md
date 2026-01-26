# Skill: The Judge

The **Judge** is the active enforcement mechanism of LoFi Gate. It is the "Guard at the Door" of the Dojo.

## How it Works

When you run `lofi-gate init`, it installs a lightweight skill into your agent's brain (workspace):

```text
.agent/skills/lofi-gate/
├── judge.py        # The Enforcement Script
├── SKILL.md        # The Constitution (Instructions for AI)
└── lofi.toml       # The Configuration
```

### 1. `judge.py`

This script is a thin wrapper around the `lofi-gate` python package. It runs the verification suite (Tests, Lint, Security).

- **Success**: Returns `Exit Code 0`. The Agent is allowed to proceed.
- **Failure**: Returns `Exit Code 1`. The Agent is blocked.

### 2. `SKILL.md` (The Constitution)

This file tells the Agent **how to behave**. It establishes the "Physics" of the workspace:

- **Red-Green-Refactor**: Tests must be written first.
- **Trust the Physics**: If the build fails, the code is wrong.

### 3. `lofi.toml` (Configuration)

You can likely leave this alone, but it allows you to toggle specific gates.

```toml
[project]
# Custom test command (optional)
test_cmd = "npm run test:special"

[gate]
strict_tdd = true      # Block usage if new files lack tests
security_check = true  # Run npm audit / cargo audit
```

## The "Strict TDD" Gate

The Judge includes a **Strict TDD** check.
If you add a new source file (e.g., `user_service.py`) but do _not_ add a corresponding test file (e.g., `test_user_service.py` or existing test update), the Judge will **reject** the commit.

> "No code without law."
