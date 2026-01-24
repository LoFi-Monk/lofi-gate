# AiVerify 🤖✅

![AiVerify Hero](hero.png)

**The Context-Preserving Test Runner for AI Agents**

> "Strong verification loops guide the agent toward the desired result... abstracting away much of the noise that would otherwise consume the agent’s precious context window." — _Spotify Engineering_

AiVerify is a high-performance verification proxy designed for the era of agentic software development. It acts as an intelligent "Inner Loop" verifier, ensuring your AI pair (Claude, GPT, Antigravity) receives the pure **Signal** it needs to ship, without the toxic **Noise** of verbose terminal logs.

## 🧠 The Philosophy

Standard Coding Agents fail in two main ways:

1.  **Context Bloat**: Agents often read _every_ test file just to understand how to run them. This wastes tokens and distracts the model with irrelevant code.
2.  **Cheating**: When faced with a failure, Agents often modify the test itself to force a pass, rather than fixing the bug.

**The Solution**: AiVerify standardizes the entry point to enforce a strict, project-owned verification workflow that the agent cannot circumvent.

## 🚀 Core Features

### 1. Eliminating Context Bloat (The "Speed Lane")

Agents run `npm run test:agent` (if configured) to execute tools like `jest --onlyChanged`.

- **Result**: The Agent verifies code in seconds, scanning only relevant files.

### 2. Smart Truncation

The script buffers output to prevent token overflow and context exhaustion.

- **Success**: Prints `✅ Verified` (hides 1000s of lines of logs).
- **Failure**: Prints only the last 100 lines of the error.

### 3. Parallel Execution & Auto-Retry

- **Parallelism**: Automatically runs Lint, Security, and Tests concurrently for instant feedback.
- **Flake Protection**: Automatically retries a failed test command once before reporting it to the agent, reducing friction from flaky tests.

## 🛡️ Advanced Gates ("The Iron Man Suite")

AiVerify blindly enforces these project rules if conditions are met:

- **Gate 1: Security Scan**: If `package.json` exists, it runs `npm audit --audit-level=high`. Blocks on Critical/High vulnerabilities.
- **Gate 2: Strict TDD Enforcer**: Checks `git status` for new implementation files. Fails with "STRICT TDD VIOLATION" if code is created without a corresponding test file.
- **Gate 3: Coverage Check**: If a `coverage` script exists, it ensures thresholds are met before allowing a passage.

## Visual Proof: Signal vs. Noise

### ❌ The Old Way (Toxic Noise)

```text
$ npm test
> project@1.0.0 test
> jest

 PASS  test/auth.test.js (1.2s)
 PASS  test/utils.test.js (0.8s)
 PASS  test/api.test.js (2.1s)
 ... [500 lines of passing details] ...
Test Suites: 15 passed, 15 total
Tests:       84 passed, 84 total
Time:        4.5s
```

### ✅ The AiVerify Way (Pure Signal)

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

## ⚙️ Configuration

AiVerify respects your standard tool configurations.

**To set a Coverage Threshold (Jest example):**

```json
"jest": {
  "coverageThreshold": { "global": { "lines": 90 } }
}
```

**Standard Node Integration:**
Add to `package.json`:

```json
"scripts": {
  "test": "npm run verify",
  "verify": "python scripts/aiverify.py --parallel",
  "test:agent": "jest --onlyChanged",
  "lint": "eslint .",
  "coverage": "jest --coverage"
}
```

---

## Detailed Setup & Trust Gates

### 1. The Node.js "Professional" setup

For Node projects, make it the default gate using **Husky**:

1. **Install**: `npm install husky --save-dev && npx husky init`
2. **Add Hook**: Update `.husky/pre-push`:
   ```bash
   npm run verify
   ```

### 2. Cross-Language Support

- **Python**: Autodetects `pytest` or `requirements.txt`.
- **Rust (Blazing Fast)**: Wraps `cargo test` and `cargo check`. (Local speed <30s vs Cloud CI 5m).

### 3. A Note on CI (GitHub Actions)

**Keep AiVerify local.** It is optimized for **Human-AI Pair Speed**. In CI, use standard verbose logs for post-mortem debugging.

---

_Built to help humans and AI agents work together in harmony._
