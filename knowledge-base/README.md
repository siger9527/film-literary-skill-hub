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

- `entries/production-design-and-visual-development-workflow.md` — production design (node 04) and visual development (node 09), their role boundaries, design-to-execution workflows, deliverables, acceptance and failure routing. Industry-role research synthesis; runtime not tested.

- `entries/asset-visual-execution-video-generation-animation-vfx.md` — nodes 10–13: asset identity/version/publishing, visual execution compilation, video generation lifecycle and VFX repair; AYON Core, ComfyUI, Wan2.1 and Natron pinned-source review. L2 static review; runtime not tested.

## Evidence policy

A source citation is not proof of runtime behavior. Static review, upstream test-file inspection, executed tests, and runtime/integration validation are separate evidence levels. Do not promote an entry to production-ready merely because it is documented here.

## Framework boundary

The V0.1 five-stage, 21-node production framework remains locked. Knowledge entries map capabilities to that framework; they do not redefine node ownership or stage structure.
