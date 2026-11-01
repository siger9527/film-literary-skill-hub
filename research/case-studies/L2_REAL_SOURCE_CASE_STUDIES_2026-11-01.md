# L2 Real-Source Case Studies

Review date: 2026-11-01

This document records source-grounded case studies against immutable upstream commits. It is a research artifact, not an approval or runtime-test certificate.

## Case A — OpenMontage

- Repository: https://github.com/calesthio/OpenMontage
- Reviewed commit: `195eab24478dc9363326aec437aefc3701635ddf`
- License evidence: repository `LICENSE` at the reviewed commit identifies GNU AGPL version 3.
- Review scope: `lib/checkpoint.py`, `lib/pipeline_loader.py`, `tests/lib/test_checkpoint_prerequisites.py`, pipeline manifest/schema references.

### Mechanisms observed

1. Pipeline manifests are loaded from `pipeline_defs/<name>.yaml`, parsed with `yaml.safe_load`, and validated against a JSON Schema before use (`lib/pipeline_loader.py`, lines 39–67).
2. Stage approval defaults are read from the manifest by `get_stage_human_approval_default` (`lib/pipeline_loader.py`, around line 173).
3. Checkpoint writes call `_stage_requires_approval`; a manifest gate or stricter caller flag requires `human_approved=True` before a gated stage can be marked completed (`lib/checkpoint.py`, lines 251–285 and 470–493).
4. Stage advancement checks predecessor checkpoints, their validity, project/pipeline/stage identity, completion state, and required approvals (`lib/checkpoint.py`, lines 290–350).
5. Tests cover missing predecessors, unapproved predecessors, malformed predecessor checkpoints, and non-blocking in-progress heartbeats (`tests/lib/test_checkpoint_prerequisites.py`).

### Important limitation / risk

The approval-policy loader catches non-`FileNotFoundError` exceptions, logs a warning, and returns `None`; the caller then falls back to `human_approval_required`. This means malformed YAML, schema-validation failure, or other manifest-loading errors can degrade enforcement if the caller does not independently require approval. This is a static control-flow finding from the pinned source, not a dynamically reproduced bypass.

### Transferable design lesson

For this Skill Hub and its downstream production governance, policy/configuration needed to decide whether an operation is authorized should fail closed when it cannot be loaded or validated. A fallback may be appropriate for non-security presentation defaults, but not for approval policy. The decision record should identify the policy version and preserve the failure state.

### Evidence classification

- Source fact: manifest parsing, schema validation, gate lookup, checkpoint gating and predecessor validation.
- Test evidence: the listed test cases exist in the pinned source; this review did not execute them.
- Static inference: gate degradation on non-missing manifest load errors.
- Runtime status: not tested by this review.

## Case B — FFmpeg Skill

- Repository: https://github.com/kajisho5/ffmpeg-skill
- Reviewed commit: `1ce2c186bf1dba96132d87274eee46df4f537e0e`
- License evidence: repository `LICENSE` at the reviewed commit identifies MIT License.
- Review scope: `SKILL.md`, `scripts/_common/runner.py`, `scripts/batch.py`, `scripts/verify.py`, selected orchestration and delivery tests.

### Mechanisms observed

1. The Skill explicitly separates deterministic media execution from creative decisions. It directs agents to probe real media properties, plan with dry-run, execute, check, verify, and inspect visual output. It explicitly states that technical execution does not decide which cut is right or whether a deliverable is approvable (`SKILL.md`).
2. Shared process execution centralizes timeouts, child-process tracking, output locking, cleanup and structured error reporting (`scripts/_common/runner.py`).
3. The output lock uses exclusive file creation. If lock creation fails due to an OS error, the tool warns and continues without a lock, so concurrent writers may still collide (`scripts/_common/runner.py`, around lines 865–930).
4. The outer sibling-script timeout kills the direct child process. Linux child-process parent-death handling is implemented for FFmpeg subprocesses, while the source comments explicitly note no equivalent mechanism for Windows and macOS (`scripts/_common/runner.py`, around lines 1400–1540).
5. Batch processing uses a thread lock for in-process cache updates and writes a sibling temporary file followed by `os.replace`; this protects against torn cache writes within the process, but is not by itself a cross-process transaction (`scripts/batch.py`, around lines 360–510).
6. `verify.py` probes media, plans multiple real processing steps, records pass/fail/skipped results, and returns a verification failure if any required step fails (`scripts/verify.py`).

### Transferable design lesson

Separate creative approval from deterministic execution. A media tool can prove properties such as dimensions, duration, codec, frame rate, loudness, output identity and decode success; it cannot decide narrative quality, emotional impact, visual taste or whether a shot serves the director's intent. Production Skills should pass a structured, versioned execution specification to media tools and then interpret the evidence against creative acceptance criteria.

### Evidence classification

- Source fact: workflow instructions, subprocess/lock/cache mechanisms and verification report construction.
- Test evidence: relevant test files and test cases exist in the pinned source; this review did not execute them.
- Static inference: lockless continuation creates a concurrent-write risk; cross-process cache coordination is not guaranteed by a thread lock.
- Runtime status: not tested by this review.

## Cross-case synthesis for the Skill Hub

| Concern | OpenMontage pattern | FFmpeg Skill pattern | Skill Hub application |
|---|---|---|---|
| Governance | Manifest-defined gates and predecessor validation | Execution preconditions and structured failures | Keep policy decisions separate from catalog metadata; fail closed on policy uncertainty |
| Evidence | Checkpoint artifacts and approval state | Probe, command, verification and output identity | Every review claim must link to pinned source evidence |
| Responsibility | Human approval is explicit | Creative judgement remains with caller/human | L1/L2 are triage/research only; no automatic quality endorsement |
| Failure handling | Missing predecessor blocks advancement | Timeout, lock, output and verification errors are explicit | Record BLOCKED and error evidence; do not silently publish partial results |
| Tool boundary | Orchestration governs stage lifecycle | FFmpeg performs deterministic media operations | Distinguish professional judgement, orchestration and tool execution |

## Research status

- OpenMontage: source-mechanism case study recorded; no runtime validation performed.
- FFmpeg Skill: source-mechanism case study recorded; no runtime validation performed.
- Neither source is automatically copied into the curated library.
- These case studies do not modify the locked five-stage, 21-node V0.1 production framework.
