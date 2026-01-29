# PR & Release Checklist

To ensure high-quality contributions and prevent recurring errors, every pull request must satisfy the following:

## 1. Local Verification

- [ ] Run all automated tests (e.g., `python -m unittest discover tests`).
- [ ] Run reproduction scripts if applicable (e.g., `reproduce_bloat.py`).
- [ ] Verify manual functionality (e.g., `lofi-gate verify`).

## 2. Versioning & Metadata

- [ ] Bump version in `pyproject.toml` (Semantic Versioning).
- [ ] Bump version in `src/lofi_gate/__init__.py`.
- [ ] Ensure `lofi-gate --version` reflects the local source version.

## 3. Documentation & History

- [ ] Update artifact documentation (`walkthrough.md`, `implementation_plan.md`).
- [ ] Update user documentation in `docs/` if features changed.
- [ ] Clean up `verification_history.md` or confirm it behaves as expected.

## 4. Git & PR Cleanliness

- [ ] Work in a dedicated feature branch.
- [ ] Ensure no temporary files (e.g., `reproduce_bloat.py`) are committed unless intended.
- [ ] Provide clear PR title and description with `Closes #XX` if applicable.
