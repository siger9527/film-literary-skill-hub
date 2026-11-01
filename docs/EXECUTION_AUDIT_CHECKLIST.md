# Execution Audit Checklist

This checklist is mandatory before submission, task completion, handoff, and resumption after interruption.

## A. Baseline and scope
- [ ] Current branch and base commit confirmed.
- [ ] Current locked requirements and relevant decision records read.
- [ ] Change scope matches the authorized task.
- [ ] No silent architecture or V0.1 baseline change.

## B. Completeness
- [ ] All intended files exist.
- [ ] No accidental deletions, partial writes, placeholders, or truncated content.
- [ ] Cross-file references and paths resolve.
- [ ] Documentation and machine-readable configuration agree.
- [ ] Generated files are reproducible or explicitly marked as generated.

## C. Correctness
- [ ] Syntax / format checks pass.
- [ ] Schemas validate both valid and invalid fixtures.
- [ ] Unit tests pass.
- [ ] Regression and negative-path tests pass.
- [ ] Failure handling, API limits, network errors, and partial results are handled.
- [ ] Security, permissions, untrusted input, and license boundaries reviewed.

## D. Evidence
- [ ] Exact commit SHA recorded.
- [ ] Exact commands and exit codes recorded.
- [ ] Test output or CI run URL recorded.
- [ ] Static analysis is not described as runtime testing.
- [ ] Unverified assumptions and limitations are listed.

## E. Release / handoff
- [ ] Changelog / state / risks / failure ledger updated where relevant.
- [ ] PR template completed.
- [ ] No merge or release if required checks are missing or failing.
- [ ] Next action and blocking decision are explicit.

**Gate outcome:** `PASS`, `BLOCKED`, or `REWORK_REQUIRED`. There is no implicit pass.
