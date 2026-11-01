# Curated Professional Knowledge Base

This directory contains locally authored, evidence-backed professional knowledge derived from reviewed sources. It is not a mirror of upstream Skill files.

## Entry contract

Every entry must state:
- the professional capability and applicable V0.1 node(s);
- the actual mechanism or principle;
- when it should and should not be used;
- inputs, outputs and acceptance evidence;
- known failure modes and recovery;
- immutable upstream repository, commit, file paths and line ranges;
- review level and whether runtime behavior was tested;
- license/provenance constraints.

## Initial entries

- `entries/production-gates-and-checkpoints.md` — stage gating, predecessor validation and approval-policy failure handling (OpenMontage).
- `entries/deterministic-media-execution-and-verification.md` — deterministic media execution, process/output safety and technical verification (FFmpeg Skill).

## Evidence policy

A source citation is not proof of runtime behavior. Static review, upstream test-file inspection, executed tests, and runtime/integration validation are separate evidence levels. Do not promote an entry to production-ready merely because it is documented here.

## Framework boundary

The V0.1 five-stage, 21-node production framework remains locked. Knowledge entries map capabilities to that framework; they do not redefine node ownership or stage structure.
