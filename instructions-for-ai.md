# Instructions for AI Agents (LoFi Gate)

**If you are an AI (Claude, GitHub Copilot, Cursor, Windsurf), READ THIS.**

You are working in a **LoFi Gate** enabled repository.
This environment works differently than standard environments.

## ⚡ The Rules of Physics Here

1.  **Verification is Law**: You cannot bypass the verification gate.
2.  **Tests are Sacred**: You are forbidden from modifying existing tests to make them pass (unless the requirement changed).
3.  **No Fluff**: Do not explain what you are doing. Just do it.

## 🛠️ Your Toolbelt

### 1. The Verification Script (`lofi_gate.py`)

This is your single source of truth.

- **Command**: `python lofi_gate.py --parallel`
- **What it does**: Runs TDD check, Security audit, Linting, and Tests.
- **When to run it**: Before _every_ commit.

### 2. The Speed Lane (`npm run test:agent`)

LoFi Gate is optimized for you. It automatically uses `jest --onlyChanged` logic (if available).

- **Do NOT run**: `npm test` (It might be too slow/noisy).
- **DO run**: `python lofi_gate.py`. It handles the optimization.

## 🛑 How to Handle Failure

If `lofi_gate.py` fails:

1.  **Read the truncated output** (It shows you exactly what failed).
2.  **Fix the code**.
3.  **Re-run**: `python lofi_gate.py`.

## ⚖️ The Judge Skill (`lofi-gate-judge`)

If available in `.agent/skills/lofi-gate-judge`, you MUST run it after your tests pass but BEFORE you declare the task done.

It verifies:

1.  Did you modify tests? (Anti-Cheat)
2.  Did you fulfill the prompt? (Intent)
