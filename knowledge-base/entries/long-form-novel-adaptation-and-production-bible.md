# Professional Knowledge Entry: Long-Form Novel Adaptation and Production-Bible Handoff

**Entry ID:** `PKB-ADAPT-001`  
**Domain:** Novel adaptation / serialized screenplay development / production continuity  
**V0.1 mapping:** Node 01 Creative Development; Node 02 Screenwriting; handoff support to Nodes 03, 09, 10 and 14  
**Evidence level:** L2 static source inspection  
**Runtime status:** NOT_TESTED  
**Upstream:** [egguy886/write-screenplay-skill](https://github.com/egguy886/write-screenplay-skill)  
**Pinned commit:** `fd2404312b2d4fa1e0b0381529de9d9cf21da547`  
**License evidence:** repository `LICENSE` identifies MIT. This is an independently authored summary; no upstream code or long passages are copied.

## Professional principle

Adaptation is a sequence of explicit editorial decisions, not chapter-to-episode transcription. The source novel remains the authority for what actually happens; summaries and outlines are navigation aids. Adaptation decisions must preserve causal, emotional and thematic functions while changing medium, runtime and production form.

## Source-grounded workflow

1. **Set adaptation parameters:** target medium/platform, episode count, runtime, content boundaries, voice-over policy and protected story elements.
2. **Index the source:** create chapter cards containing summary, dramatic function, filmable beats, emotional intensity, hook strength, information changes and key props.
3. **Verify against the manuscript:** compare chapter cards with actual chapter text, including openings, middle and endings. Record contradictions between source text and prior outlines.
4. **Make compression decisions:** retain, merge scenes, combine characters, consolidate locations, montage, move events or cut material. Each decision needs a reason.
5. **Budget episodes/arcs:** allocate runtime and episode capacity according to dramatic function rather than equal chapter division.
6. **Write episode outlines:** identify source chapters, episode goal, turn, scenes, opening payoff, information state and ending hook.
7. **Require review before drafting at scale:** the source workflow explicitly places user review at adaptation-parameter and episode-outline gates.
8. **Draft in batches and maintain continuity:** compare each episode against the production bible and continuity ledger.

## Translation from prose to screen action

The source distinguishes literary interiority and authorial explanation from observable action, audible dialogue and information that can be carried by behavior, props, images or sound.

This is a medium-conversion principle, not a ban on all subjective cinematic techniques. Voice-over, memory, subjective sound and visual metaphor may be valid when deliberately chosen and supported by the directing concept.

## Production Bible as a controlled handoff

The source's production-bible design separates dramatic, language, visual and voice attributes for characters; tracks costume variants, props, locations and voice assets; and uses stable identifiers so scripts can be checked against the asset inventory.

**Application**
- Character identity and dramatic canon remain separate from generated visual variants.
- Costume changes are tracked as variants linked to the canonical character.
- Props and locations have stable identities and state/continuity records.
- Script references use IDs that can flow into storyboard, asset production, voice and editing.
- A bible check can find missing assets or inconsistent names, but cannot decide whether the design is artistically correct.

## Inputs and outputs

**Inputs**
- full source manuscript and canonical version;
- prior outline/notes (non-authoritative until checked);
- adaptation brief and protected creative intent;
- target runtime, platform, episode format and production constraints.

**Outputs**
- chapter index and verified beat cards;
- compression decision ledger;
- arc/episode budget;
- episode outline and approval record;
- screenplay batch;
- production bible and stable asset references;
- continuity and source-coverage report.

## Acceptance criteria

- Every source chapter is accounted for as adapted, merged, moved, montaged or cut with a reason.
- Chapter cards have been checked against actual source text.
- Every major adaptation change records the source function being preserved or intentionally changed.
- Episode count and runtime are feasible, not merely numerically within a cap.
- Each episode has a clear dramatic goal, turn and justified ending.
- Character, prop, location and costume references resolve to canonical records.
- User approval is recorded before irreversible adaptation decisions or large-scale script drafting.
- Technical lint success is not treated as proof of dramatic quality or faithful adaptation.

## Critical applicability limits

The upstream Skill is optimized for vertical micro-drama and short serialized formats. Its fixed defaults—episode caps, short runtime, hook rotations, limited scene counts and platform-specific pacing—must not be imposed on feature films, literary animation, long-form series or slower dramatic works without justification.

The Hub should extract its traceability, source-verification, compression-ledger, approval-gate and production-bible mechanisms while treating its platform pacing rules as optional profiles.

## Failure modes

| Failure | Required response |
|---|---|
| One chapter mechanically becomes one episode | Reassess dramatic function and runtime capacity |
| Beat cards rely on an old outline | Recheck the full manuscript and update the canon discrepancy ledger |
| Compression removes a later payoff's causal setup | Restore or replace the setup; document the decision |
| Characters/locations are merged only to reduce asset count | Verify dramatic identity and relationship functions first |
| Every episode uses the same hook formula | Review audience promise, emotional variation and long-range rhythm |
| Asset bible is treated as creative authority | Route design decisions to directing/visual departments |
| Lint passes but episode is dramatically weak | Conduct independent story and screenplay review |

## Boundary

This knowledge entry supports node 01/02 and downstream handoff. It does not replace the director's interpretation, production design, cinematography, editing or independent QC.
