# Instructions for AI Agents: Installing LoFi Gate

**Goal**: You are tasked with installing **LoFi Gate** into the user's repository.

## 1. Install the Script

Download the latest `lofi_gate.py` to the project root.

```bash
# If curl is available (Linux/Mac)
curl -o lofi_gate.py https://raw.githubusercontent.com/LoFi-Monk/lofi-gate/main/lofi_gate.py

# If Windows (PowerShell)
Invoke-WebRequest -Uri https://raw.githubusercontent.com/LoFi-Monk/lofi-gate/main/lofi_gate.py -OutFile lofi_gate.py
```

## 2. Configure the Environment

You must configure the project to use the gate.
**Read the guide for the specific tech stack you are working in:**

### 🟢 Node.js

[👉 Read docs/setup-node.md](docs/setup-node.md)
_Configures `package.json`, "Speed Lane" `test:agent`, and Husky._

### 🐍 Python

[👉 Read docs/setup-python.md](docs/setup-python.md)
_Configures `pyproject.toml` and Pre-commit hooks._

### 🦀 Rust

[👉 Read docs/setup-rust.md](docs/setup-rust.md)
_Configures `Cargo.toml` and Git hooks._

### 🐹 Go

[👉 Read docs/setup-go.md](docs/setup-go.md)
_Auto-runs `go test` and `go vet`._

## 3. Verify

Run the gate manually to prove it works:

```bash
python lofi_gate.py
```
