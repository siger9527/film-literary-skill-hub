# L2 Source Review: Directing, Blocking, Storyboard and Visual Pre-Production

Review date: 2026-11-01

Scope: V0.1 nodes 03–09. This is a focused static source review of directing/previsualization and AI-assisted visual planning resources. It does not claim that all seven nodes are fully researched or validated.

## Sources and immutable pins

### A. cajias/agentic-video-skills — cinematic-director module
- Commit: `204cefd08bbb87fd4681f1f2b0dccbc444a978c1`
- Skill license: MIT; inspected `plugins/cinematic-director/skills/cinematic-director/LICENSE`.
- Inspected: `SKILL.md`, `references/cinematic-language.md`, `references/continuity-bible.md`, `references/ai-video-tool-adapters.md`.
- Focus: dramatic breakdown, beat mapping, director's book, blocking, shot rationale, continuity, prompt/tool adaptation.
- The skill's own default shot durations and model recommendations are production heuristics, not universal film grammar.

### B. wuwangzhang1216/DirectorSKILL
- Commit: `c65ae0d14457053efb1e354c7e7f7e120d97fad1`
- License: MIT; inspected root `LICENSE`.
- Inspected: `SKILL.md`, `references/blocking-and-staging.md`, `references/lighting-and-color.md`, `references/production-workflow.md`, `assets/shot-plan-template.md`, `evals/run.md`.
- Focus: quantified blocking/proxemics, camera geometry, motivated lighting, shot-plan completeness, risk budgeting, approved-keyframe gate, eval methodology.
- The evaluation guide explicitly says evals are behavior contracts requiring generated responses and independent grading; its percentages and scoring thresholds belong to that project's suite, not ours.

### C. 0xhughs/director-skills
- Commit: `35ca0a2b4cd55b0668aa9ea0f40273324b774bb4`
- License: MIT; inspected root `LICENSE`.
- Inspected: root `SKILL.md`, `skills/shotlist-and-visual-breakdown/SKILL.md`, `skills/character-location-prop-bible/references/identity_anchors.md`.
- Focus: modular routing, shot purpose, asset breakdown, continuity bible and identity anchors, separating creative intent from cinematic execution and model adaptation.

### D. smixs/visual-skills
- Commit: `92be33a5a73325fb3d8e0c73b22744b114e2a90e`
- License: CC BY 4.0; inspected root `LICENSE`.
- Inspected: `video/SKILL.md`, `video/references/dramaturgy.md`, `video/references/camera-lighting-vocabulary.md`, `video/references/animatic-keyframes.md`.
- Focus: shot-level dramatic function, blocking as desire, staging/subtext, keyframe design, montage and camera/lighting vocabulary.
- Any redistribution of adapted material requires attribution and compliance with CC BY 4.0. This Hub stores only independently written summaries and citations, not copied text.

### E. zenstory-ai/drama-skills
- Commit: `66b7b3e9e913fcefe81849941c0761facd5b1d5e`
- License: MIT; inspected root `LICENSE`.
- Inspected: `README.md`, `docs/character-consistency-across-shots.md`, `docs/short-drama-storyboard-script-template.md`, `evaluations/README.md`, and implemented note `.agents/notes/implemented/feature/2026-10-20-scene-blocking-and-camera-terms.md`.
- Focus: explicit approval before paid generation, document-level continuity locks, shot-to-source traceability, scene blocking anchors, camera-relative translation, production regression and holdout evaluation.
- The cited blocking note reports a small controlled Seedance 2.0 probe: three arms with three runs each, where the camera-relative foreground/background formulation achieved the tested across-table relationship 3/3 versus 0/3 for the two other formulations. This is a narrow, model-specific result, not a universal guarantee. The repository's evaluation README describes a broader test design; its claims were inspected, not independently rerun here.

## Cross-source professional findings

1. **Director's intent must precede shot selection.** Extract dramatic question, conflict, subtext, emotional movement and a concrete visual thesis before choosing coverage. A shot should have a readable story function; shot variety is not a substitute for direction.
2. **Blocking precedes camera.** Establish bodies, props, entrances/exits, distance, height, barriers, power and action geometry. Camera placement then reveals that geometry. A lens cannot repair unclear staging.
3. **Maintain two coordinate layers.** Scene-level blocking uses stable spatial anchors, character relationships and the action axis; each shot translates these into camera-relative foreground/background, screen direction, facing and visibility. This avoids treating frame-left as an invariant of the physical location.
4. **Shot design must carry executable states.** Every shot needs purpose, source scene/beat, start state, one legible action chain, end state, composition, camera, light, duration, sound and continuity dependencies. Stable shot IDs permit revision without losing traceability.
5. **Lighting is a motivated system.** Record source, direction relative to camera, quality, key/fill/rim roles, ratio or explicit shadow behavior, practical motivation and what must remain constant across cuts. Mood adjectives alone are not a lighting plan.
6. **Freeze and approve the still before expensive motion generation when identity/composition matters.** The keyframe establishes identity, costume, space, composition and light; video prompt then specifies motion, camera behavior and endpoint. This is a workflow control, not a claim that every shot must use image-to-video.
7. **Continuity is a set of changing facts, not one permanent reference image.** Separate canonical identity from costume/condition/time variants; track prop ownership/state, location geography, screen direction, eyeline, light and start/end states. A reference asset is not proof that the generated output matches it.
8. **Separate creative intent, cinematic execution and model adaptation.** Preserve the director's intent in a model-neutral shot specification; compile target-tool prompts in a separate adapter layer.
9. **Evaluate behavior, not document verbosity.** A Markdown eval definition is not an executed evaluation. Controlled comparisons require isolated sessions, fixed inputs, blind/independent grading and explicit replicate accounting.

## V0.1 node applicability and evidence gaps

| Node | Relevant evidence | Current confidence / gap |
|---|---|---|
| 03 Directing | Dramatic breakdown, visual thesis, director's book, shot rationale, performance and staging | Strong source coverage; no independent production test |
| 04 Production Design | Location/prop anchors, set geometry, visual bible and motivated practicals | Partial only; specialist art-direction research still required |
| 05 Storyboard | Beat-to-shot decomposition, keyframe cards, start/action/end, shot function | Strong source coverage; no complete animatic pipeline test |
| 06 Cinematography | Frame size/angle/lens/movement, axis, screen direction, camera geometry | Strong source coverage; no optical practice validation on real footage |
| 07 Lighting | Motivated sources, direction, key/fill/rim, ratio, palette and continuity | Partial-to-strong; no calibrated lighting/grade test |
| 08 Blocking & Staging | Proxemics, power geometry, anchors, entrances/exits, camera-relative translation | Strong conceptual coverage; narrow model probe only |
| 09 Visual Development | Director's visual thesis, style bible, identity anchors, palette and look continuity | Partial; visual development/art direction needs separate deeper review |

## Disposition

- `cajias/agentic-video-skills`: L2 static source review.
- `wuwangzhang1216/DirectorSKILL`: L2 static source review; eval protocol inspected, not run.
- `0xhughs/director-skills`: L2 static source review.
- `smixs/visual-skills`: L2 static source review; CC BY 4.0 attribution obligations retained.
- `zenstory-ai/drama-skills`: L2 static source review; its narrow model-behavior probe is source-reported, not independently reproduced.

No upstream code or Skills were executed by this Hub review. No actual production footage, lighting setup or full animatic was tested. This review does not authorize replacing or restructuring V0.1 nodes.
