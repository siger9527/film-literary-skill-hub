# L2 Source Mechanism Review Policy

## Purpose
L2 inspects the pinned repository tree and bounded text files to understand implementation structure, dependencies, tests, execution mechanisms, permission/approval signals, and potential risk areas.

## Evidence rules
Every review is pinned to repository, commit, and Skill path. File evidence records the path, file kind, read status, and byte count or reason for failure. Static pattern findings record source path, signal code, occurrence count, and line numbers. Findings are review leads, not proof of vulnerability or runtime behavior.

## Safety boundary
The reviewer reads public text files only. It never clones a repository, installs dependencies, or executes upstream code. Files above 200 KB or unreadable files are recorded as review errors; an incomplete repository scan is BLOCKED. Recursive Git tree truncation also blocks review.

## Dispositions
- `L2_STATIC_REVIEW_COMPLETE`: selected bounded text files were read and statically inspected; this is not runtime validation.
- `BLOCKED`: repository tree or required text could not be fully reviewed.

## Explicit limitations
- A detected pattern is not proof of exploitability.
- No detected pattern is not proof of safety.
- A test file's presence does not mean its tests pass.
- L2 does not certify creative quality or production readiness.
- L3/runtime testing is reserved for critical infrastructure or high-risk mechanisms and must be performed in an isolated, authorized environment.
