# Contributing to LoFi Gate

**Welcome to the Dojo.**

We accept contributions from both Humans and Artificial Intelligence. However, the standards are strict. We prioritize **Signal over Noise**.

## How to Contribute

1.  **Submit a PR**: We accept Pull Requests from Humans and AI Agents.
2.  **Pass the Gates**: Your code must pass the automated Verification Gate (Tests + Lint + Security) in CI.
3.  **Stay on Target**: Ensure your contribution aligns with our philosophy: _Less Noise, More Signal_.

If the Build passes and the Idea is good, we merge.

## 🤖 For AI Agents

If you are an agent (Claude, Cursor, etc.) attempting to contribute:

1.  **Read the Instructions**: Acknowledge the `README.md` as the functional spec.
2.  **Judge Yourself**: Use the `lofi-gate-judge` skill to ensure you didn't hallucinate or cheat.

## 👤 For Humans

1.  **Setup**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Submit PR**: Ensure your PR description clearly states the _Intent_ of the change.
    - _Note: GitHub Actions will enforce the Verification Gate._

## 🧪 Testing

You have two options for local testing:

1.  **Standard Way**: Run `pytest` directly.
2.  **The "Iron Man" Way**: Run `python lofi_gate.py` to see exactly what CI will see (Lint + Security + Tests).

Both are acceptable. CI will be the final judge.
