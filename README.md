# LoFi Gate

**Signal-first verification for AI coding agents.**

## The Problem

AI Agents struggle to debug massive terminal output. Feeding an Agent 10,000 lines of CI logs ensures it misses the root cause and burns through your API budget.

### The Reality

A failed test run can easily produce 5,000-10,000 tokens of noise - stack traces, error messages, and framework output that obscures the actual problem.

Feeding this to an LLM ensures it misses the root cause and burns through your API budget. "Context Overflow" causes agents to hallucinate fixes or get stuck in failure loops.

### The Solution

LoFi Gate is a **signal-first** verification proxy. It wraps your existing tools (npm, cargo, pytest), truncates the noise, and delivers a concise, token-optimized failure report that Agents can actually understand.

> [!TIP]
> **Full Documentation**: [LoFi Gate Wiki](https://github.com/LoFi-Monk/lofi-gate/wiki)

## The Old Way

![The Old Way](assets/images/testing-old-way.gif)

## The New Way

![The New Way](assets/images/testing-lofi-way.gif)

In extreme cases (complex failures, verbose frameworks), we've measured single test failures producing 15,000+ tokens.

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

## The Judge (Anti-Cheat)

When an Agent submits code, LoFi Gate performs a **Physical Interrogation**:

> **Q1: Did you modify any EXISTING test files?**
> _If YES → FAILS immediately._
>
> **Q2: Did you disable, skip, or weaken any tests?**
> _If YES → FAILS immediately (Nice try, `expect(true).toBe(true)`)._
>
> **Q3: Did you delete test files?**
> _If YES → FAILS immediately._

**The Gate only opens when the interrogation passes.**

---

## Wire It Up

LoFi Gate is designed to be the "Hardware Interface" between your AI Agent and your project.

### 1. Choose Your Stack

Detailed setup guides for specific environments:

- [**Node.js**](https://github.com/LoFi-Monk/lofi-gate/wiki/Setup-Node) (`package.json`)
- [**Python**](https://github.com/LoFi-Monk/lofi-gate/wiki/Setup-Python) (`pyproject.toml`)
- [**Rust**](https://github.com/LoFi-Monk/lofi-gate/wiki/Setup-Rust) (`Cargo.toml`)
- [**Go**](https://github.com/LoFi-Monk/lofi-gate/wiki/Setup-Go) (`go.mod`)

### 2. Configure Your Agent

If you are using a "Skill-based" agent (Claude, Qwen, etc), point it to the scaffolded skill file:

- [**Skill: The Judge**](https://github.com/LoFi-Monk/lofi-gate/wiki/Skill-Judge) (Rules)
- [**Configuration**](https://github.com/LoFi-Monk/lofi-gate/wiki/Configuration) (`lofi.toml`)

### 3. Enforce The Rules

Don't let broken code merge.

- [**GitHub Repo Rules**](https://github.com/LoFi-Monk/lofi-gate/wiki/GitHub-Rules) (Branch Protection)

### 4. Read The Docs

- [**Philosophy**](https://github.com/LoFi-Monk/lofi-gate/wiki/Philosophy): Why "Physics over Law"?
- [**Compatibility**](https://github.com/LoFi-Monk/lofi-gate/wiki/compatibility): Using LoFi Gate with Local Models.

* [**Logging & The Ledger**](https://github.com/LoFi-Monk/lofi-gate/wiki/Ledger): Understanding the `verification_history.md` format and Token Savings.

---

## The Ledger

Every time LoFi Gate runs, it calculates **Token Savings**.
Check `verification_history.md` to see exactly how much context (and money) you are saving per run.

> 📊 **Total Token Size:** 14502 | 💰 **Total Token Savings:** 12400
