# Setup: Node.js

## 1. Install Requirements

Ensure you have Python 3.8+ installed (for the gate script).

## 2. Copy the Script

Copy `lofi_gate.py` to your `scripts/` folder:

```bash
mkdir -p scripts
cp lofi_gate.py scripts/
```

## 3. Configure `package.json`

Add the following scripts to your `package.json`:

```json
{
  "scripts": {
    "lofi-gate": "python scripts/lofi_gate.py --parallel",
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
