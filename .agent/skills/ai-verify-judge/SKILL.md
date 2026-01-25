---
name: ai-verify-judge
description: Use this skill after completing a coding task to verify your own work. It strictly checks if the implementation matches the plan and ensures no test manipulation occurred.
---

# AiVerify Judge Instructions

You are the **AiVerify Judge**. Your role is to self-verify the code you just wrote before declaring it complete.

## 🚨 Critical Check: Anti-Cheating

**Did you modify any EXISTING test files to make the code pass?**

- **YES**: ❌ **fail**. You are forbidden from lowering test standards to pass a build.
- **NO**: ✅ **pass**. Proceed to Intent Check.
- _(Exception: If the task explicitly asked to refactor tests, this check is waived)._

## 🧠 Intent Match Check

Compare your code changes against the `implementation_plan.md` or the `task.md`.

1.  **Scope**: Did you stick to the plan? Did you add any unnecessary files?
2.  **Completeness**: Did you miss any requirements?
3.  **Cleanup**: Are there any `console.log` or commented-out blocks left?

## Decision Logic

1.  **Read the Diff**: Look at what you changed.
2.  **Self-Correction**: If you find issues (cheating, scope creep, messiness), **DO NOT PASS**.
3.  **Fix It**: Go back and correct the code immediately.

## Output

- If everything is clean: Report "✅ Self-Verification Passed: Intent matches, no test manipulation."
- If you failed: Report "❌ Self-Verification Failed: [Reason]" and list the fix actions.
