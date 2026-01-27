# How to Contribute

## 1. The Rules (Physics)

This repo is protected by **LoFi Gate**.

- You must write tests.
- You cannot commit if `lofi-gate verify` fails.

## 2. Setup

1. Fork & Clone.
2. `pip install -e .`
3. Hack away.

## 3. Releasing (For Maintainers)

To publish a new version to PyPI:

1.  **Bump Version**: Update `version = "x.y.z"` in `pyproject.toml`.
2.  **Commit**: `git commit -m "chore: bump version to x.y.z"`
3.  **Release**:
    - Go to GitHub -> [Releases](https://github.com/LoFi-Monk/lofi-gate/releases).
    - Draft a new release.
    - Tag it `vx.y.z`.
    - Click **Publish**.
4.  **Watch**: The `Publish to PyPI` Action will verify, build, and upload automatically.
