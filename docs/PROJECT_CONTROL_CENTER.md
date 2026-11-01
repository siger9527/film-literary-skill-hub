# Project Control Center

## Purpose

Provide one intake and review surface for problems, improvement proposals, new ideas, risks, decisions, and verification evidence discovered during project execution.

## Interactive entry point

Use the GitHub Issue Form: **Project Control Center**. It collects:
- record type;
- summary and context;
- priority and impact scope;
- affected 21-node IDs / files / workflows;
- evidence;
- recommended action and alternatives;
- locked-baseline consideration;
- objective acceptance criteria.

The Issue Form is the single intake surface. GitHub Issues remain the durable record; implementation changes are made through pull requests. The form does not grant approval to change locked requirements.

## Record lifecycle

`CAPTURED -> TRIAGED -> ACCEPTED | DEFERRED | REJECTED -> IN_PROGRESS -> REVIEW_REQUIRED -> VERIFIED -> CLOSED`

A decision request may remain `AWAITING_USER_DECISION`. A defect may be marked `BLOCKED` if required evidence or access is unavailable.

## Mandatory pre-submit / pre-resume gate

Before any PR is opened, any task is marked complete, or work resumes after interruption, the operator must:
1. Re-read the current project state, locked requirements, relevant decisions, and the exact branch/commit being continued.
2. Inspect the complete diff and every changed file; verify that no files are missing, stale, truncated, or contradictory.
3. Validate syntax and schemas for all changed machine-readable files.
4. Run relevant unit, regression, and negative-path tests.
5. Verify generated outputs against their schemas and verify source pins / license evidence.
6. Distinguish static inspection, automated tests, and real runtime/integration evidence.
7. Record exact commands, commit SHA, results, failures, and untested areas.
8. Update project state, decision/risk/failure/evidence records as applicable.
9. If any mandatory check fails or cannot be run, stop the gate. Mark `BLOCKED` or `REVIEW_REQUIRED`; do not claim verified completion.

The review is not a self-attestation checkbox alone: CI must run deterministic checks, and the PR description must contain inspectable evidence. High-impact or locked-baseline changes require explicit human approval.

## Work-resumption protocol

On every resume:
- identify the last verified commit and any uncommitted / newly committed changes;
- compare current repository state with the last execution receipt;
- inspect the most recent work before adding new changes;
- resolve regressions first;
- only then continue the next planned task.

## Evidence vocabulary

- `SOURCE_INSPECTED`: source read at a pinned commit.
- `STATIC_CHECKED`: deterministic static validation completed.
- `TESTED`: named tests executed and passed.
- `RUNTIME_TESTED`: actual runtime execution with a receipt.
- `INTEGRATION_TESTED`: connected components exercised end-to-end.
- `NOT_TESTED`: no execution evidence.
- `BLOCKED`: could not proceed because a required condition was unavailable.

Never promote one evidence level to another by inference.
