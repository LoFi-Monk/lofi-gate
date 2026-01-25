---
name: lofi-gate-judge
description: A self-reflexive verification skill that ensures agent compliance with LoFi Gate rules (Anti-Cheat, Intent Check).
---

# LoFi Gate Judge Skill

You have completed coding and tests are passing. Now you must judge your own work before declaring victory.

## Step 1: Gather Evidence

Run this command to see exactly what you changed:

```bash
git diff --staged
```

If nothing is staged, run:

```bash
git diff HEAD
```

Save the output. This is your **evidence**.

## Step 2: Recall Your Mission

Find the original instructions. Check these locations in order:

1. The user's original request (in conversation history)
2. `implementation_plan.md` (if you created one)
3. `task.md` (if it exists)

This is your **mission**.

## Step 3: The Anti-Cheat Check

Look at your evidence (the diff). Answer these questions:

**Q1: Did you modify any EXISTING test files?**

- Look for changes to files matching: `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go`
- If YES → Did the mission explicitly ask you to modify tests?
  - NO → **VERDICT: FAIL** - "Modified existing tests without authorization"
  - YES → Continue

**Q2: Did you disable, skip, or weaken any tests?**

- Look for: `.skip`, `.only`, `@pytest.mark.skip`, `expect(true).toBe(true)`, commented-out assertions
- If YES → **VERDICT: FAIL** - "Weakened test integrity"

**Q3: Did you delete test files or test cases?**

- If YES and not authorized → **VERDICT: FAIL** - "Deleted tests without authorization"

## Step 4: The Scope Check

Compare your evidence against your mission:

**Q4: Did you stay within scope?**

- Did you only change what was asked?
- Did you add files or features that weren't requested?
- If you went outside scope → **VERDICT: FAIL** - "Scope creep detected"

**Q5: Did you complete the mission?**

- Review each requirement in the mission
- Is each one addressed in your changes?
- If incomplete → **VERDICT: FAIL** - "Mission incomplete"

## Step 5: Deliver Judgment

If all checks pass:

```
✅ JUDGMENT: APPROVED
All changes align with the mission. No test manipulation detected.
```

If any check fails:

```
❌ JUDGMENT: REJECTED
Reason: [specific failure reason]
Required action: [what to fix]
```

## Step 6: Act on Judgment

- **If APPROVED**: You may proceed to commit/push.
- **If REJECTED**: You MUST fix the issues before proceeding. Do not ignore this judgment.
