# LoFi Gate

**Signal-first verification for AI coding agents.**

## Why? The Shepherd of Cats

AI Agents are like cats: smart, autonomous, but easily distracted. You cannot "command" a cat; you have to structure its environment so the only logical thing to do is what you want.

A Shepherd doesn't:

- Ask sheep nicely to stay together.
- Write documentation about staying together.
- Hope they follow the process.

A Shepherd:

- **Uses a fence** (Environment Design).
- **Uses a dog** (Enforcement Mechanism).
- **Makes it easier to stay together than to wander off.**

### The Reality

A single Jest failure can produce **15,000 tokens of noise** — that's **85% of Claude's context window** burned on a single test run.

Feeding this to an LLM ensures it misses the root cause and burns through your API budget. "Context Overflow" causes agents to hallucinate fixes or get stuck in failure loops.

### The Solution

LoFi Gate is a **signal-first** verification proxy. It wraps your existing tools (npm, cargo, pytest), truncates the noise, and delivers a concise, token-optimized failure report that Agents can actually understand.

> [!TIP]
> **Full Documentation**: [LoFi Gate Wiki](https://github.com/LoFi-Monk/lofi-gate/wiki)

## The Old Way

![The Old Way](docs/images/testing-old-way.gif)

## The New Way

![The New Way](docs/images/testing-lofi-way.gif)

## Quick Install

Get to a "working experience" in 30 seconds:

```bash
pip install lofi-gate
lofi-gate init
lofi-gate verify  # Test it immediately
```

_This creates `.agent/skills/lofi-gate/` with your local config._

## Usage

Run the gate to verify your changes. This will run your tests, lint, and security checks, and output a clean, token-optimized report.

```bash
lofi-gate verify
```

---

## Wire It Up

LoFi Gate is designed to be the "Hardware Interface" between your AI Agent and your project.

### 1. Choose Your Stack

Detailed setup guides for specific environments:

- [**Node.js**](docs/Setup-Node.md) (`package.json`)
- [**Python**](docs/Setup-Python.md) (`pyproject.toml`)
- [**Rust**](docs/Setup-Rust.md) (`Cargo.toml`)
- [**Go**](docs/Setup-Go.md) (`go.mod`)

### 2. Configure Your Agent

If you are using a "Skill-based" agent (Claude, Qwen, etc), point it to the scaffolded skill file:

- [**Skill: The Judge**](docs/Skill-Judge.md) (Rules)
- [**Configuration**](docs/Configuration.md) (`lofi.toml`)

### 3. Enforce The Rules

Don't let broken code merge.

- [**GitHub Repo Rules**](docs/GitHub-Rules.md) (Branch Protection)

### 4. Read The Docs

- [**Philosophy**](docs/Philosophy.md): Why "Physics over Law"?
- [**Compatibility**](docs/compatibility.md): Using LoFi Gate with Local Models.

* [**Logging & The Ledger**](docs/Ledger.md): Understanding the `verification_history.md` format and Token Savings.

---

## The Ledger

Every time LoFi Gate runs, it calculates **Token Savings**.
Check `verification_history.md` to see exactly how much context (and money) you are saving per run.

> 📊 **Total Token Size:** 14502 | 💰 **Total Token Savings:** 12400
