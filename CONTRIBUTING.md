# Contributing to AiVerify

**Welcome to the Dojo.**

We accept contributions from both Humans and Artificial Intelligence. However, the standards are strict. We prioritize **Signal over Noise**.

## 🧠 The Philosophy

1.  **Strict Verification**: No code enters `main` without passing `aiverify.py`.
2.  **Test Integrity**: Modifying tests to pass a bugfix is considered "Cheating" and is grounds for immediate rejection.
3.  **Determinism**: If it works on your machine, it must work on CI.

## 🤖 For AI Agents

If you are an agent (Claude, Cursor, etc.) attempting to contribute:

1.  **Read the Instructions**: Acknowledge the `README.md` as the functional spec.
2.  **Judge Yourself**: Use the `ai-verify-judge` skill to ensure you didn't hallucinate or cheat.
3.  **Do Not Chat**: Submit PRs that are complete and self-verified.

## 👤 For Humans

1.  **Setup**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Submit PR**: Ensure your PR description clearly states the _Intent_ of the change.
    - _Note: GitHub Actions will enforce the Verification Gate._

## 🧪 Testing

We use `pytest`. You can run it manually, or let CI verify it for you.

```bash
# Manual run
pytest
```
