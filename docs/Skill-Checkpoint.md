# Skill: The Checkpoint

The **Checkpoint** is the active enforcement mechanism of LoFi Gate. It guarantees your code meets the quality standards before you commit.

## How it Works

When you run `lofi-gate init`, it installs a mandatory skill into your agent's brain (workspace):

```text
.agent/skills/lofi-gate-checkpoint/
├── SKILL.md             # The Rules (Instructions for AI)
└── scripts/logger.py    # The Ledger Writer
```

### 1. The Command (`lofi-gate verify`)

You don't run a script manually. You run the CLI:

```bash
lofi-gate verify
```

- **Success**: Returns `Exit Code 0`. The Agent is allowed to proceed.
- **Failure**: Returns `Exit Code 1`. The Agent is blocked.

### 2. `SKILL.md` (The Rules)

This file tells the Agent **how to behave**. It establishes the "Rules" of the workspace:

- **Red-Green-Refactor**: Tests must be written first.
- **Trust the Build**: If the build fails, the code is wrong.
- **Mandatory Checkpoint**: The Agent must verify "Anti-Cheat" questions before committing.

## The "Strict TDD" Gate

The Checkpoint includes a **Strict TDD** check.
If you add a new source file (e.g., `user_service.py`) but do _not_ add a corresponding test file (e.g., `test_user_service.py` or existing test update), the Checkpoint will **reject** the commit.
