# Contributing to LoFi Gate

Thank you for your interest in contributing! Whether you are a human or an AI agent, we welcome your PRs.

## How to Contribute

1.  **Fork** the repository and clone it locally.
2.  **Create a Branch** for your feature or fix.
    ```bash
    git checkout -b feat/my-feature
    ```
3.  **Make your changes**.
    - Please include tests for new functionality.
4.  **Submit a Pull Request**.
    - Push your branch to your fork.
    - Open a PR against the `main` branch.
    - Our CI (GitHub Actions) will run the verification suite automatically.

## AI Agent Instructions

If you are an AI agent contributing to this repo:

- Follow the standard Git workflow above.
- Write clear, conventional commit messages (e.g., `feat: add logging`).
- Do not overwrite existing tests unless the requirements have changed.

## Development Setup

To run the verification gate locally, please follow the setup guide for your environment:

- [**Node.js Setup**](docs/setup-node.md)
- [**Python Setup**](docs/setup-python.md)
- [**Rust Setup**](docs/setup-rust.md)

Once set up, you can verify your changes by running:
`python lofi_gate.py`
