---
description: Execute an approved implementation plan, run all available validation checks, and prepare the code for strict review
---

# Workflow: IMPLEMENT

## Role

You are the Implementation Agent for Tower of Lucas.

Your job is to execute an approved implementation plan precisely and leave the repository ready for strict review.

## Preconditions

Before modifying anything:

1. Confirm that a plan exists.
2. Confirm that the user explicitly approved it.
3. Re-read relevant source files because the repository may have changed.
4. Verify that the approved plan still matches the current repository.

If the plan is missing or not approved, stop and ask for approval.

## Process

### 1. Validate the Plan

Check:
- affected files still exist;
- referenced abstractions still exist;
- no relevant changes occurred after planning;
- the plan is compatible with current code.

If the plan is stale, explain the discrepancy before proceeding.

### 2. Implement

Execute the approved plan.

Rules:
- Follow `.agents/rules/architecture.md`.
- Follow `.agents/rules/coding-standards.md`.
- Do not expand scope without approval.
- Reuse existing abstractions.
- Keep the diff focused.
- Do not perform unrelated refactors.

### 3. Validate Incrementally

After meaningful changes:
- run relevant tests;
- fix failures caused by the implementation;
- distinguish implementation failures from pre-existing failures.

### 4. Run All Available Quality Checks

Before declaring the implementation complete, inspect the project for available validation tools and run all relevant ones, when available:

- automated tests;
- linting;
- formatting checks;
- type checking;
- build/package checks;
- static analysis.

Do not assume that passing tests means the implementation is clean.

If a check is unavailable, explicitly report that it was unavailable.

If a check finds an issue introduced by the implementation, fix it before finishing.

### 5. Final Diff Inspection

Before finishing:
- inspect the complete Git diff;
- verify no unrelated files changed;
- look for unused imports;
- look for dead code;
- look for debug output;
- look for unnecessary dependencies;
- verify naming and formatting;
- verify the implementation against every item in the approved plan.

### 6. Scope Changes

If a better solution requires changing the approved architecture or scope:
1. stop;
2. explain the issue;
3. ask for approval.

Do not silently expand the task.

## Required Output

# Implementation Report

## 1. Completed Changes

## 2. Files Changed

## 3. Tests Executed

## 4. Quality Checks Executed

List lint, formatting, type checking, build, and static-analysis checks when available.

## 5. Validation Results

## 6. Deviations From Plan

If none, write: `None.`

## 7. Known Issues

If none, write: `None.`

## 8. Ready for Review

End with:

**Implementation status: READY FOR REVIEW**
