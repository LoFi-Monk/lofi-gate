# Compatibility & Local Models

> **The LoFi Philosophy**: "Physics over Law."
> We believe the environment should force compliance, not the prompt.

However, we acknowledge that smaller, quantized models (e.g., Llama 3 8B, Mistral, older local models) may panic when encountering a strict verification failure without context.

If you are using a "Smart" Model (Claude 3.5, GPT-4), you do **NOT** need this.
If you are using a "LoFi" Model, you might.

## The "break Glass" Primer

If your local agent is struggling to understand the workflow, you may include this minimal instruction in its system prompt or custom instructions:

```text
[LOFI GATE PROTOCOL]
You are working in a verified environment.
1. Rule: You MUST run verification before every commit.
2. Command: `python lofi_gate.py --parallel`
3. Failure: If verification fails, read the error summary, fix the code, and RETRY.
4. Prohibition: Do NOT edit test files to force a pass.
```

## Supported Stacks

LoFi Gate is designed to be a Universal Adapter.

- **Node.js**: First-class support via `package.json`.
- **Python**: Native support via `pyproject.toml` or direct execution.
- **Rust**: Native support via `cargo` wrapping.
- **Go**: Supported via `go test` wrapping (auto-detected).
