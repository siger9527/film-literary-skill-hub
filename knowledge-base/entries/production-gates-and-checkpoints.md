# Professional Knowledge Entry: Production Gates and Checkpoints

**Entry ID:** `PKB-GOV-001`  
**Domain:** Production governance / workflow orchestration  
**V0.1 mapping:** Node 00; cross-stage G1–G5 governance  
**Evidence level:** L2 source inspection  
**Runtime status:** NOT_TESTED  
**Upstream:** [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)  
**Pinned commit:** `195eab24478dc9363326aec437aefc3701635ddf`  
**License evidence:** repository `LICENSE` identifies AGPL-3.0; this entry is an independently authored summary and does not copy upstream implementation.

## Professional principle

A production stage is not complete merely because an agent produced an artifact or wrote a completion status. Advancement requires validated prerequisites, correct project/stage identity, and any required approval evidence.

## Mechanism observed in source

1. Pipeline manifests are loaded from YAML and validated against a JSON Schema before being used as pipeline definitions.  
   Evidence: `lib/pipeline_loader.py`, lines 39–67.
2. Stage-level human approval defaults are read from the same manifest field used by gate enforcement.  
   Evidence: `lib/pipeline_loader.py`, lines 170–185.
3. Checkpoint advancement checks predecessor records for existence, valid structure, matching project/pipeline/stage identity, completed status, and required approval.  
   Evidence: `lib/checkpoint.py`, lines 290–350.
4. A gated stage cannot be written as completed without explicit human approval evidence.  
   Evidence: `lib/checkpoint.py`, lines 470–493.
5. The source includes tests for missing/incomplete/unapproved predecessors and malformed predecessor checkpoints.  
   Evidence: `tests/lib/test_checkpoint_prerequisites.py`. Test files were inspected; tests were not executed as part of this review.

## Critical limitation found

The approval-policy lookup catches general manifest-loading exceptions, logs a warning, and returns `None`, allowing the caller's `human_approval_required` flag to become the fallback. If the manifest is malformed or cannot be validated and the caller does not independently require approval, the manifest's gate may not be enforced.

This is a static control-flow risk, not a dynamically reproduced bypass.

## Application to our production system

Adopt the principle, not the upstream pipeline structure:

- Keep the locked 21-node V0.1 structure unchanged.
- Separate artifact completion, handoff acceptance, stage-gate approval and release authorization.
- Validate predecessor deliverables by immutable object/version references, not only by filenames or a status string.
- Record the policy version and the exact evidence used for each approval.
- Treat an unreadable, malformed or unvalidated authorization policy as `BLOCKED`.
- Allow a stricter caller requirement, but never let a caller weaken a mandatory project policy.
- Require explicit, authorized waiver records; a warning is not a waiver.

## Inputs and outputs

**Inputs**
- Project and pipeline identity.
- Current stage and predecessor stage records.
- Immutable references to predecessor artifacts and acceptance records.
- Applicable gate policy and approval authority.

**Outputs**
- Gate evaluation record: `PASS`, `CONDITIONAL_PASS`, `BLOCKED`, `REWORK_REQUIRED` or authorized `WAIVED`.
- Missing/invalid prerequisite list.
- Approval evidence and policy version.
- Actionable return path to the responsible upstream node.

## Acceptance criteria

A gate implementation is acceptable only when tests prove:
- missing predecessor blocks advancement;
- wrong project/pipeline/stage identity blocks advancement;
- invalid or incomplete predecessor record blocks advancement;
- missing required approval blocks advancement;
- policy parse/schema/permission failure blocks advancement;
- waiver without authority/evidence is rejected;
- a valid completed and approved predecessor allows advancement;
- recovery/resume does not silently bypass prior gate decisions.

## Failure modes and response

| Failure | Required response |
|---|---|
| Missing predecessor | BLOCKED; identify responsible stage |
| Invalid predecessor record | BLOCKED; preserve evidence and request repair |
| Required approval absent | BLOCKED; return to approval owner |
| Gate policy cannot be loaded or validated | BLOCKED; do not use permissive fallback |
| Upstream artifact superseded | Re-resolve pinned dependency and re-evaluate affected gate |
| Waiver requested | Require authorized DecisionRecord and fixed evidence references |

## Boundary

This mechanism belongs to project governance. It does not decide whether the story, directing, visual design, performance, editing or sound is artistically successful. Those judgments remain with the responsible professional nodes and independent QC.
