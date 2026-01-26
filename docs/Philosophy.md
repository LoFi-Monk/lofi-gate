# Philosophy: The Way of LoFi

> "Physics over Law. If the build breaks, you stop."

## Core Values

### 1. Signal over Noise

Modern CI logs are trash. Feeding 10,000 lines of `npm test` output to an LLM is a guaranteed way to induce hallucinations (and bankruptcy).

#### Comparison

The Old Way:
![The Old Way](images/testing-old-way.gif)

The New Way:
![The New Way](images/testing-lofi-way.gif)

**LoFi Gate** acts as a compression algorithm for verification. It extracts the **Signal** (Did it fail? Why? What is the error?) and discards the **Noise** (Success logs, download bars, warnings).

### 2. Physics over Law

Traditional "Rules" (files like `.rules.md`) are soft. An Agent can ignore them.
**Physics** (Code) cannot be ignored. If `lofi-gate verify` returns `Exit Code 1`, the Agent fails. It cannot proceed. This creates a feedback loop that forces the Agent to correct itself, rather than apologizing and continuing.

### 3. Verification is Currency

In the age of generative code, "It looks correct" is dangerous.
"It runs and passes tests" is the only currency that matters.

## The Metaphor: The Gate

We are the **Gate**.
The Agent is the martial artist entering the Dojo.
The Gate does not care who you are.
The Gate only cares: **Do you know the password?** (Passing Tests).
