# Setup: Rust

## 1. Install Requirements

Ensure you have Python 3.8+ installed (for the gate script) and Cargo.

## 2. Copy the Script

Copy `lofi_gate.py` to your project root.

## 3. Usage

Since Cargo doesn't have a built-in "scripts" section like npm (without plugins/aliases), you typically run the script directly or use a `Makefile` / `Justfile`.

**Makefile Example:**

```makefile
verify:
	python lofi_gate.py --parallel
```

## 4. Automatic Detection

LoFi Gate automatically detects `Cargo.toml`.

- It runs `cargo check` (Security/Lint equivalent)
- It runs `cargo test`

## 5. Verify

Run the gate manually:

```bash
python lofi_gate.py --parallel
```
