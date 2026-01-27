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
gh api repos/:owner/:repo/rulesets \
  -f name="Strict TDD Gate" \
  -f target="branch" \
  -f enforcement="active" \
  -F conditions[ref_name][include][]="refs/heads/main" \
  -F rules[0][type]="required_status_checks" \
  -F rules[0][parameters][required_status_checks][][context]="gate" \
  -F rules[0][parameters][strict_required_status_checks_policy]=true
```

### Option B: Manual Setup

1. Go to **Settings > Rules > Rulesets**.
2. Click **New branch ruleset**.
3. Name: `Strict TDD Gate`.
4. Target: `Includes default branch`.
5. Check **Require status checks to pass**.
6. Add `gate`.
7. Click **Create**.
