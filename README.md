# AiVerify 🤖✅

**The Context-Preserving Test Runner for AI**

AiVerify is a transparent verification proxy designed specifically for developers working with AI coding agents (like Claude, GPT, or Antigravity). It solves the problem of "Context Bloat" by intelligently filtering and status-reporting your project's verification suite.

## The Problem: Context Starvation

Traditional test runners (like Jest, Pytest, or npm test) often dump thousands of lines of verbose logs into the terminal. For a human, this is noise. For an AI Agent, this is **toxic context bloat**.

Every line of "Success" log pushes your source code out of the AI's short-term memory (context window), making the agent more forgetful and prone to hallucinations.

## The Solution: Signal, Not Noise

AiVerify acts as a smart filter around your existing tools:

1. **Silent Success**: If your tests/lint pass, AiVerify returns a concise "✅ Verified" signal.
2. **Smart Truncation**: If failure occurs, it captures and displays only the most relevant error lines (the last ~100 lines), preserving precious context space.
3. **Parallel Execution**: Automatically runs independent checks (Lint, Audit, and Tests) in parallel to speed up the agent's feedback loop.
4. **Strict TDD Gate**: Optional enforcement that ensures every new code file has a corresponding test file before allowing a "Pass" status.

## Quick Start

### Installation

Move `verify.py` into your `scripts/` directory or project root.

### Usage

```bash
python verify.py --parallel
```

### Flags

- `--parallel`: Run independent checks (Lint, Security, Test) concurrently.
- `--serial`: Run checks one by one (default, handles fail-fast cases).

## Integration with Node.js

Add it to your `package.json`:

```json
"scripts": {
  "verify": "python verify.py --parallel"
}
```

---

_Built to help humans and AI agents work together in harmony._
