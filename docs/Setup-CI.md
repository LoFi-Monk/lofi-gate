# CI Setup Guide

## 1. Add the Workflow

Create `.github/workflows/gate.yml` in your repository:

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

## 2. Enforce the Rules (Branch Protection)

You must configure GitHub to block merges if `gate.yml` fails.

### Option A: GitHub CLI (Fast)

Run this command in your terminal:

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

1. Go to **Settings > Rules > Rulesets**.
2. Click **Add Classic branch protection rule**.
3. Branch Name Pattern: `main` or `master`.
4. Require a pull request before merging: `Yes`
5. Require approvals: `No`
6. Require status checks to pass before merging: `Yes`
7. Require branches to be up to date before merging: `Yes`
8. Status checks to require: `gate`
9. Do not allow bypassing this rule: `Yes`
10. Click **Create**.
