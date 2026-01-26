# Contributing to LoFi Gate

**Physics over Law.**

We do not have a 50-page rulebook. We have a **Gate**.
If you want to contribute, your code must pass the Gate.

## 1. The Physics (Rules)

### Red-Green-Refactor

This repository (and the Judge skill) enforces **Strict TDD**.

- **Red**: Write a test that fails.
- **Green**: Write code to pass the test.
- **Refactor**: Clean it up.

> 🚨 **Breaking the Physics**: If you submit a PR with new source code but NO new tests, the underlying `strict_tdd` check will fail.

## 2. Development Setup

This is a Python package. Treat it like one.

1.  **Clone & Install**

    ```bash
    git clone https://github.com/LoFi-Monk/lofi-gate.git
    cd lofi-gate
    pip install -e .
    ```

2.  **Dogfooding (Init)**
    We use LoFi Gate to verify LoFi Gate. Initialize the physics in the repo root:

    ```bash
    lofi-gate init
    ```

3.  **Run Verification**
    ```bash
    lofi-gate verify
    ```
    _This runs our tests, lint, and security checks._

## 3. Pull Requests

- **Humans**: Open a PR. If the CI (GitHub Actions) passes, we will review it.
- **Agents**: Ensure you have run `lofi-gate verify` locally before pushing. If the Ledger shows **FAIL**, do not push.

## 4. Documentation

- **Philosophy**: See [docs/Philosophy.md](docs/Philosophy.md).
- **Wiki**: See [docs/](docs/) for deep dives.
