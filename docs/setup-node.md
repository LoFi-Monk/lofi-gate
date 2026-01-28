# Setup: Node.js

## 1. Install LoFi Gate

Install the package using Python's package manager:

```bash
pip install lofi-gate
```

## 2. Initialize Physics

Scaffold the configuration into your workspace:

```bash
lofi-gate init
```

_This creates `.agent/skills/lofi-gate/`._

## 3. Configure `package.json`

Add the following scripts to your `package.json`:

```json
{
  "scripts": {
    "lofi-gate": "lofi-gate verify --parallel",
    "test": "npm run lofi-gate",
    "test:agent": "jest --onlyChanged",
    "lint": "eslint ."
  }
}
```

_Note: `test:agent` is the "Speed Lane". Configure your test runner (Jest/Vitest) to run only changed files._

## 4. Install Husky (Optional but Recommended)

Prevent messy commits by running the gate on push.

```bash
npm install husky --save-dev
npx husky init
echo "npm test" > .husky/pre-push
```

## 5. Verify

Run the gate manually:

```bash
npm run lofi-gate
```

## 6. Troubleshooting

### `npm audit` Failures

If you are using Next.js 16 with Storybook 8 (or other conflicting peer dependencies), `npm audit` might fail even if there are no critical vulnerabilities, due to `ERESOLVE` errors.

To fix this unrelated blocking error, update `.agent/skills/lofi-gate/lofi.toml`:

```toml
[gate]
security_fail_on_error = false
```

This will run the audit and show warnings, but won't block your verification.
