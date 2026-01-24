# AiVerify 🤖✅

![AiVerify Hero](hero.png)

**The Context-Preserving Test Runner for AI Agents**

> "Strong verification loops guide the agent toward the desired result... abstracting away much of the noise that would otherwise consume the agent’s precious context window." — _Spotify Engineering_

AiVerify is a high-performance verification proxy designed for the era of agentic software development. It acts as an intelligent "Inner Loop" verifier, ensuring your AI pair (Claude, GPT, Antigravity) receives the pure **Signal** it needs to ship, without the toxic **Noise** of verbose terminal logs.

## The Problem: Context Starvation

Traditional test suites (Jest, Pytest, Go Test) are built for humans with high visual bandwidth. They dump thousands of lines of "Success" logs.
For an AI Agent, this is code-crushing bloat:

- **Hallucinations**: Verbose logs push original source code out of the context window.
- **Cost**: You pay for every line of "Noise" being sent to the LLM.
- **Speed**: Sequential test runs create unacceptably long feedback loops for agents.

## The Solution: Spotify-Inspired Verification Loops

Inspired by Spotify's research into [Predictable Agentic Results through Strong Feedback Loops](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3), AiVerify provides:

1. **Silent Success**: If your tests/lint pass, AiVerify returns a concise "✅ Verified" signal.
2. **Smart Truncation**: If failure occurs, it captures and displays only the most relevant error lines (the last ~100 lines), preserving precious context space.
3. **Parallel Execution**: Automatically runs independent checks (Lint, Audit, and Tests) in parallel to speed up the agent's feedback loop.
4. **Strict TDD Gate**: Optional enforcement that ensures every new code file has a corresponding test file before allowing a "Pass" status.

## Visual Proof: Signal vs. Noise

### ❌ The Old Way (Toxic Noise)

When your agent runs tests, it gets back a wall of text that pushes your code out of context.

```text
$ npm test
> project@1.0.0 test
> jest

 PASS  test/auth.test.js (1.2s)
 PASS  test/utils.test.js (0.8s)
 PASS  test/api.test.js (2.1s)
 ... [500 lines of passing details] ...
-----------------------|---------|----------|---------|---------|-------------------
File                   | % Stmts | % Branch | % Locs  | % Lines | Uncovered Line #s
-----------------------|---------|----------|---------|---------|-------------------
All files              |     100 |      100 |     100 |     100 |
-----------------------|---------|----------|---------|---------|-------------------
Test Suites: 15 passed, 15 total
Tests:       84 passed, 84 total
Snapshots:   0 total
Time:        4.5s
```

### ✅ The AiVerify Way (Pure Signal)

AiVerify strips the noise. Your agent stays focused on the logic.

```text
$ python aiverify.py --parallel
🚀 Running 4 checks in PARALLEL...
----------------------------------------
✅ TDD Check Passed! (0.10s)
✅ Security Scan Passed! (1.20s)
✅ Lint Check Passed! (0.85s)
✅ Test Suite Passed! (2.10s)
----------------------------------------
✨ All systems go!
```

## Quick Start

### Installation

Move `aiverify.py` into your `scripts/` directory or project root.

### Usage

```bash
python aiverify.py --parallel
```

### Flags

- `--parallel`: Run independent checks (Lint, Security, Test) concurrently.
- `--serial`: Run checks one by one (default, handles fail-fast cases).

## Integration with Node.js

Add it to your `package.json`:

```json
"scripts": {
  "verify": "python aiverify.py --parallel"
}
```

---

## Detailed Setup & Trust Gates

AiVerify is designed to be your project's **Local Trust Gate**. It ensures that your AI agent never commits or pushes code that hasn't been strictly verified.

### 1. The Node.js "Professional" setup

For Node projects, don't just run it manually. Make it the default gate using **Husky**:

1. **Install Husky**: `npm install husky --save-dev && npx husky init`
2. **Add the Hook**: Update your `.husky/pre-push` or `.husky/pre-commit` file:
   ```bash
   # .husky/pre-push
   npm run verify
   ```
   Now, the AI agent _cannot_ push code unless the "Pure Signal" is achieved.

### 2. Implementation for Python

If you are working in a Python environment, `aiverify.py` will autodetect `pytest` or `requirements.txt`.

```bash
# Set up a alias or script
python aiverify.py --parallel
```

### 3. Implementation for Rust (Blazing Fast)

AiVerify loves Rust. It wraps `cargo test` and `cargo check` to provide near-instant feedback.
Ensure your `aiverify.py` is in the root, and run:

```bash
python aiverify.py --parallel
```

_Note: In our tests, local verification with AiVerify took <30 seconds, compared to 5+ minutes for equivalent cloud CI runs._

### 4. A Note on CI (GitHub Actions)

**Keep AiVerify local.**
While you _could_ run AiVerify in GitHub Actions, it is optimized for **Human-AI Pair Speed**. In CI, you usually want the verbose logs for post-mortem debugging. Keep AiVerify in your local dev loop to maintain the "Fast Internal Feedback Loop" described in the Spotify research.

---

_Built to help humans and AI agents work together in harmony._
