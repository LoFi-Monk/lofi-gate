# AI Instructions: Integrating AiVerify

If you are an AI Agent (Claude, ChatGPT, etc.) being asked to set up this repo, follow these exact steps.

### 1. Installation

Copy the `aiverify.py` script into the project.

```bash
# If using curl/wget is allowed
curl -o scripts/aiverify.py https://raw.githubusercontent.com/your-org/aiverify/main/aiverify.py

# OR if local file is provided, verify it exists at:
# ./scripts/aiverify.py
```

### 2. Configuration (package.json)

You MUST configure the `package.json` with these exact scripts to ensure compatibility.

```json
"scripts": {
  "verify": "python scripts/aiverify.py --parallel",
  "test": "npm run verify",
  "test:agent": "jest --onlyChanged"
}
```

- `verify`: The main gate. Runs lint, security, and tests in parallel.
- `test`: Redirects standard `npm test` to the verifier.
- `test:agent`: **CRITICAL**. Use this when you are debugging or iterating. It only tests changed files.

### 3. Usage Rules

- **Always** run `npm run verify` before telling the user you are done.
- **Never** use `--no-verify` or attempt to bypass hooks.
- If `npm run verify` fails, read the error log. Do **not** edit the test file to make it pass unless the test itself is incorrect. Fix the implementation code.
