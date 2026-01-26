# Configuration (`lofi.toml`)

LoFi Gate is designed to work out-of-the-box (Zero Config), but you can customize the "Physics" of your workspace using the `lofi.toml` file found in `.agent/skills/lofi-gate/`.

## Structure

The configuration is divided into two sections: **Project** (Environment) and **Gate** (Rules).

```toml
[project]
test_command = ""  # Override auto-detection

[gate]
strict_tdd = true     # Block code without tests
lint_check = true     # Run linter
security_check = true # Run audit
```

## `[project]` Settings

### `test_command`

- **Default**: `""` (Auto-Detect)
- **Description**: The command used to verify logic correctness.
- **Auto-Detection**: If left empty, LoFi Gate looks for:
  1.  `npm run test:agent` (The Speed Lane)
  2.  `npm test`
  3.  `python -m pytest`
  4.  `cargo test`
  5.  `go test ./...`
- **Usage**: Set this if you use a custom runner (e.g., `make test` or `./scripts/verify.sh`).

## `[gate]` Settings

These are the "Physics" toggles.

### `strict_tdd`

- **Default**: `true`
- **Description**: Enforces Red-Green-Refactor.
- **Behavior**:
  - **Enabled**: Fails if you add a new source file (e.g., `api.py`) without adding a corresponding test file (e.g., `test_api.py`) or updating existing tests.
  - **Disabled**: Allows "Cowboy Coding" (code without tests). Useful for pure prototyping phases.

### `lint_check`

- **Default**: `true`
- **Description**: Enforces Code Style/Quality.
- **Behavior**: Runs `npm run lint`, `cargo check`, or `go vet`. If the linter reports errors, the Gate closes.

### `security_check`

- **Default**: `true`
- **Description**: Enforces Supply Chain Security.
- **Behavior**: Runs `npm audit` (High/Critical only) or `cargo audit`. Failure blocks the build.
