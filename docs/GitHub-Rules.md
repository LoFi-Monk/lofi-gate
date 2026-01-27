# GitHub Repository Rules

**The Gate must be unbreakable.**

To fully enforce "Physics over Law," you must configure your GitHub Repository to **reject** any code that does not pass LoFi Gate.

## 1. Branch Protection Rules

You must configure GitHub to block merges if CI fails.

### Option A: GitHub CLI (Fast)

Run this command in your terminal to instantly protect `main`:

```bash
gh api -X PUT repos/:owner/:repo/branches/main/protection \
  -F required_status_checks[strict]=true \
  -F required_status_checks[contexts][]=gate \
  -F enforce_admins=true \
  -F required_pull_request_reviews[dismiss_stale_reviews]=false \
  -F required_pull_request_reviews[require_code_owner_reviews]=false \
  -F required_pull_request_reviews[required_approving_review_count]=0 \
  -F restrictions=null
```

### Option B: Manual Setup

1. Go to **Settings > Branches > Branch protection rules**.
2. Click **Add Classic branch protection rule**.
3. **Branch Name Pattern**: `main` or `master`.
4. **Require a pull request before merging**: `Yes`
5. **Require approvals**: `No`
6. **Require status checks to pass before merging**: `Yes`
7. **Require branches to be up to date before merging**: `Yes`
8. **Status checks to require**: `gate`
9. **Do not allow bypassing this rule**: `Yes`
10. Click **Create**.

## 2. CI Configuration

Ensure your CI workflow (GitHub Actions) runs the gate and fails on error.

**Recommended Workflow (`.github/workflows/gate.yml`):**

```yaml
name: LoFi Gate

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install LoFi Gate
        run: pip install lofi-gate

      - name: Run Verification
        run: lofi-gate verify
```

## 3. The Result

When an Agent (or Human) opens a PR:

1.  GitHub Actions runs `lofi-gate verify`.
2.  If it fails (Red), the **Merge** button is disabled.
3.  The Agent _must_ fix the code to turn it Green.

**There is no negotiation. Only passing tests.**
