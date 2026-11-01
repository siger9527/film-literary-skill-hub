# Professional Knowledge Entry: Visual Bible, Asset Identity and Cross-Shot Continuity

**Entry ID:** `PKB-VISUAL-001`  
**Domain:** Visual development / production design interfaces / asset continuity  
**V0.1 mapping:** Nodes 04, 09 and 10; supports nodes 03, 05, 06, 07 and 12  
**Evidence level:** L2 static source inspection  
**Runtime status:** NOT_TESTED

## 1. Purpose

The visual bible is the controlled reference for the project's visual identity and repeatable world facts. It must preserve approved creative intent while allowing deliberate changes in costume, injury, weather, time, lighting and scene state. It is not a prompt dump and not a substitute for the director's visual thesis or production designer's decisions.

## 2. Separate identity, variant and current state

For recurring characters, locations and props, distinguish:
- **Identity:** canonical facts that define which character/location/prop this is.
- **Variant:** an approved form such as costume, age/time period, injury, weather, damage, day/night or alternate set dressing.
- **Current state:** facts at this point in the story, such as wet clothing, a held key, an open door, a broken cup or a visible wound.
- **Continuity lock:** only the visible facts that must remain stable across a defined set of shots.

Do not freeze changing story states into permanent identity descriptions. Do not create a new character identity every time the same person changes clothes.

## 3. Reference assets have distinct evidence states

Use explicit identifiers to distinguish:
- planned image prompt/specification;
- reference image expected to be supplied externally;
- actual image file that exists and has been inspected.

A planned prompt or a declared reference is not proof that a reference image exists. Each actual reference must have a recorded purpose: identity, costume, location geography, prop, composition, lighting or style. A single image should not be assumed to control every visual dimension.

## 4. Shot continuity is state-based

Each shot should record relevant start/end facts:
- character position, facing and eyeline;
- costume and body condition;
- hand occupancy and prop ownership/state;
- location geography and entrance/exit state;
- screen direction and action axis;
- camera position and visible spatial relationships;
- lighting source/direction/contrast;
- weather, time and atmosphere;
- what must match the next shot.

The next shot inherits the actual previous end state unless the script explicitly marks an ellipsis, time jump, off-screen action, replay or deliberate discontinuity. A new camera angle changes what is visible, not the underlying world state.

## 5. Visual development and production design interface

The director and visual development function should define:
- visual thesis and tone;
- palette and material/texture direction;
- shape language and silhouette;
- environmental motifs;
- location hierarchy and recurring spatial anchors;
- visual contrast between characters, groups and environments;
- what changes over the story and what remains invariant.

Node 04 owns the designed physical world: locations, sets, architecture, materials, props and spatial logic. Node 09 owns cross-project visual coherence and development of the visual language. The two collaborate but are not interchangeable. The inspected sources provide useful continuity and visual-bible mechanisms, but do not yet provide enough evidence for a complete professional production-design methodology.

## 6. Validation and handoff

Before downstream production:
- resolve every asset ID used by the shot plan;
- distinguish existing, planned and missing references;
- verify that shot/keyframe text only claims visible facts supported by its references;
- ensure continuity locks appear only on the shots where they apply;
- record intentional state changes and their source scene/shot;
- keep approved look decisions separate from model-specific prompt syntax;
- have generated outputs visually inspected; metadata or reference declarations alone do not prove visual match.

## 7. Failure modes

| Failure | Response |
|---|---|
| Character face stays stable but wardrobe/prop/condition drifts | Check variant and current-state tracking, not only turnaround sheet |
| Location left/right flips across reverse angles | Use spatial anchors and camera-specific view descriptions |
| A planned reference is treated as an existing image | Require actual file identity and inspection before marking it available |
| Prompt says "same as previous" without a resolvable reference | Bind explicit stable IDs and source files |
| Every visual detail is locked, preventing story changes | Lock only invariants; version intentional variants and state changes |
| Visual bible dictates story or performance | Return creative authority to writer/director; bible records approved decisions |
| All locations look stylistically identical | Review production design differentiation and visual hierarchy |

## 8. Limits

The source set supports identity/variant/state separation, continuity locks, reference provenance, visual thesis and style consistency. It does not fully establish the complete responsibilities, drawing/document standards, art department breakdown, set-construction methods, materials specification or professional visual-development approval process for node 04 and node 09. Those require further specialist research.

## Source provenance

- `cajias/agentic-video-skills` — commit `204cefd08bbb87fd4681f1f2b0dccbc444a978c1`; MIT; inspected continuity-bible and cinematic-director material.
- `wuwangzhang1216/DirectorSKILL` — commit `c65ae0d14457053efb1e354c7e7f7e120d97fad1`; MIT; inspected shot-plan, production workflow and visual-direction references.
- `0xhughs/director-skills` — commit `35ca0a2b4cd55b0668aa9ea0f40273324b774bb4`; MIT; inspected character/location/prop bible and identity-anchor references.
- `zenstory-ai/drama-skills` — commit `66b7b3e9e913fcefe81849941c0761facd5b1d5e`; MIT; inspected character consistency, storyboard and documented blocking-probe material.
- `smixs/visual-skills` — commit `92be33a5a73325fb3d8e0c73b22744b114e2a90e`; CC BY 4.0; supplementary visual-language source; attribution obligations apply to any future adaptation or redistribution.

All evidence is static source inspection. No upstream code, Skill or evaluation suite was executed by this Hub review.
