# Evidence-Based Film Node Mapping — L2 Case Studies

Basis: pinned source case studies in `L2_REAL_SOURCE_CASE_STUDIES_2026-11-01.md`.
The mapping below means "potential reference relevance", not adoption or production approval.

| Source capability / mechanism | Candidate V0.1 node(s) | Why relevant | Adoption boundary |
|---|---|---|---|
| Manifest-defined stage order, required tools and stage-level approval | 00 Project Management | Supports project workflow configuration, resource readiness and stage governance | Do not import OpenMontage's stage taxonomy as a replacement for the 21-node V0.1 model |
| Checkpoint validation and predecessor checks | 00; cross-stage governance | Demonstrates machine-checkable stage state, prerequisite validation and resumability | Need project-specific UPDP object identity, immutable versions and formal handoff/acceptance records |
| Human approval gate | 00; G1–G5 governance | Makes explicit that completion and approval are distinct states | Approval policy must fail closed when its manifest cannot be loaded or validated |
| Probe media before planning | 14 Media Management; 15 Editing; 19 Final Delivery | Decisions can use actual media metadata rather than filename or assumptions | Probe facts do not determine creative value |
| Deterministic cut/join/reframe/caption/export tools | 13 Animation & VFX; 15 Editing; 16 Color; 17 Sound; 18 Titles; 19 Delivery | Provides reproducible execution for bounded media transformations | Each operation needs a node-specific input contract, parameters and evidence |
| Output locks, staging, timeout and cleanup | 10–13; 15–19 | Useful execution reliability patterns for long-running media tasks | Lock failure must not silently continue when output integrity is at risk; OS-specific process cleanup needs explicit treatment |
| Structured verification and output identity | 19 Final Delivery; 20 Independent QC | Technical evidence can be tied to the exact output file rather than merely its path | Node 20 must remain independent and also assess creative, continuity, rights and delivery requirements |
| Visual inspection sheet | 06 Cinematography; 09 Visual Development; 13; 20 | Gives a reviewable visual artifact after image-changing operations | Automated contact sheets do not substitute for human/agent visual judgement |

## Priority extraction into Skill Hub

1. Add a shared evidence record shape: repository, immutable commit, file path, line range, claim type, evidence excerpt/reference, confidence, and runtime-verification status.
2. Add explicit separation between professional decision, execution instruction, tool result and acceptance decision.
3. Add fail-closed policy for authorization and review gates.
4. Add output identity and media-probe evidence to future media-execution adapters.
5. Keep creative acceptance criteria separate from technical verification criteria.

## Non-adoption decisions

- Do not adopt a nine-stage OpenMontage pipeline in place of the locked 21-node framework.
- Do not treat FFmpeg Skill as a director, editor or QC authority; its own documentation explicitly limits it to deterministic execution and measurement.
- Do not copy upstream Skill bodies, scripts or assets into this repository merely because their repository license exists. Any adaptation requires scoped license and third-party-content review.
- Do not mark either project `RUNTIME_TESTED` based on this static review.
