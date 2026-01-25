# Contributing to AiVerify

**Welcome to the Dojo.**

We accept contributions from both Humans and Artificial Intelligence. However, the standards are strict. We prioritize **Signal over Noise**.

## 🧠 The Philosophy

1.  **Strict Verification**: No code enters `main` without passing `aiverify.py`.
2.  **Test Integrity**: Modifying tests to pass a bugfix is considered "Cheating" and is grounds for immediate rejection.
3.  **Determinism**: If it works on your machine, it must work on CI.

## 🤖 For AI Agents

If you are an agent (Claude, Cursor, etc.) attempting to contribute:

1.  **Read the Instructions**: `instructions-for-ai.md` is your source of truth.
2.  **Verify Locally**: Run `python aiverify.py` before EVERY commit.
3.  **Judge Yourself**: Use the `ai-verify-judge` skill to ensure you didn't hallucinate or cheat.
4.  **Do Not Chat**: Submit PRs that are complete and self-verified.

## 👤 For Humans

1.  **Setup**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Verification**:
    ```bash
    python aiverify.py
    ```
3.  **Submit PR**: Ensure your PR description clearly states the _Intent_ of the change.

## 🧪 Testing

We use `pytest`. The verification script will automatically detect and run it.

```bash
# Manual run
pytest
```
