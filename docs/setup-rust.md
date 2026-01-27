# Setup: Rust

## 1. Install LoFi Gate

Install the package (requires Python 3.8+):

```bash
pip install lofi-gate
```

## 2. Initialize Physics

Scaffold the configuration into your workspace:

```bash
lofi-gate init
```

_This creates `.agent/skills/lofi-gate/`._

## 3. Configure `Cargo.toml` (Optional)

Rust doesn't have a standardized "scripts" section like Node, but you can use `cargo-make` or just run the CLI directly.

**Using cargo-make (Makefile.toml):**

```toml
[tasks.verify]
command = "lofi-gate"
args = ["verify", "--parallel"]
```

## 4. Verify

Run the gate manually:

```bash
lofi-gate verify
```
