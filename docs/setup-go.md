# Setup LoFi Gate for Go 🐹

## 1. Prerequisites

Ensure strict TDD compliance in your Go project.

```bash
# Verify you have Go installed
go version
```

## 2. Install the Script

Run this in your project root:

```bash
curl -o lofi_gate.py https://raw.githubusercontent.com/LoFi-Monk/lofi-gate/main/lofi_gate.py
```

## 3. Git Hook Setup

Go doesn't have a standardized `package.json` equivalent for scripts, so we rely heavily on Git Hooks (Husky or manual).

### Manual Method

Create `.git/hooks/pre-push` (or `pre-commit`):

```bash
#!/bin/sh
python3 lofi_gate.py --parallel
```

Make it executable:
`chmod +x .git/hooks/pre-push`

## 4. Usage

The script automatically detects `go.mod` and runs:

- **Lint**: `go vet ./...`
- **Tests**: `go test ./...`
- **TDD Check**: Scans for new `*.go` files without `*_test.go`.
