# GitHub Repository Rules

**The Gate must be unbreakable.**

To fully enforce "Physics over Law," you must configure your GitHub Repository to **reject** any code that does not pass LoFi Gate.

## 1. Branch Protection Rules

Go to **Settings** > **Rules** > **Rulesets** (or **Branches** in older repos) and create a rule for `main`:

### Critical Settings

- [x] **Require status checks to pass before merging**
  - Search for your CI job (e.g., `verify`, `test`, or `ci/circleci`).
  - _Why_: This ensures `lofi-gate verify` actually ran and returned `Exit Code 0`.
- [x] **Require branches to be up to date before merging**
  - _Why_: Prevents logical conflicts that might break the build after merge.
- [x] **Do not allow bypassing the above settings**
  - _Why_: Even Admins should not break the build.

## 2. CI Configuration

Ensure your CI workflow (GitHub Actions) runs the gate and fails on error.

**Example (`.github/workflows/verify.yml`):**

```yaml
name: Verify
on: [push, pull_request]

jobs:
  lofi-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install
        run: pip install lofi-gate
      - name: Verify
        run: lofi-gate verify
```

## 3. The Result

When an Agent (or Human) opens a PR:

1.  GitHub Actions runs `lofi-gate verify`.
2.  If it fails (Red), the **Merge** button is disabled.
3.  The Agent _must_ fix the code to turn it Green.

**There is no negotiation. Only passing tests.**
