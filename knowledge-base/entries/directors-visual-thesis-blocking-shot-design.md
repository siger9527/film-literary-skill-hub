# Professional Knowledge Entry: Director's Visual Thesis, Blocking and Shot Design

**Entry ID:** `PKB-DIRECT-001`  
**Domain:** Directing / previsualization / scene blocking / shot design  
**V0.1 mapping:** Nodes 03, 05, 06 and 08; supporting interfaces to 04, 07 and 09  
**Evidence level:** L2 static source inspection  
**Runtime status:** NOT_TESTED

## 1. Professional responsibility

The director defines what the audience should understand and feel, and why a scene must be staged and photographed in a particular way. The storyboard and shot plan translate that intent into visible, executable decisions. They do not invent arbitrary coverage or merely turn every screenplay sentence into a separate picture.

## 2. Start with dramatic direction, not camera vocabulary

Before designing shots, record:
- literal event and dramatic question;
- external and internal conflict;
- subtext and information asymmetry;
- emotional movement from opening state through pressure and turn to ending state;
- concrete visual thesis governing the scene;
- what changes for the character and audience.

A visual thesis must be expressible as a concrete visual rule, not just a theme word. Example form: "the character is increasingly boxed by the doorway as the other person gains control of the room."

## 3. Blocking before camera

For each character, establish:
- start position and facing;
- immediate objective and who/what they move toward or away from;
- path, pace, duration and interaction with props;
- relationship to barriers, entrances, exits and other bodies;
- eyeline target;
- end position and final body/prop state.

Blocking communicates power and subtext through distance, height, who moves or holds, who controls the exit, who invades space, who turns away and who is visually boxed by architecture. Quantified distances can help when the relationship depends on a measurable change, but numerical values are planning aids rather than universal acting rules.

**Two-layer spatial notation**
1. Scene-level plan: stable anchors, set geometry, action axis, character relationships and position changes.
2. Shot-level translation: camera location, foreground/background, screen-left/right, facing toward/away from camera, occlusion and visible spatial relationships.

A character being "across the table" is not always enough for an image/video model to construct depth. Translate the scene plan into the actual camera view for each shot.

## 4. Shot design after staging

Build shots from beats and audience information needs. A shot specification should include:
- stable shot ID and source scene/beat;
- dramatic function (establish, reveal, power, pressure, detail, reaction, impact, aftermath, exit);
- frame content and subject hierarchy;
- shot size, horizontal angle, camera height and axis side;
- lens/focal-length intention where relevant;
- one motivated camera move or locked camera;
- blocking start → action → end;
- motivated light direction and continuity;
- sound/dialogue timing;
- duration estimate and basis;
- continuity anchors and adjacent-shot dependencies;
- generation/production risk and intended cut point.

Do not force every scene into the same coverage pattern or a fixed number of shots. A locked wide can be more expressive than six inserts if the staging carries the conflict.

## 5. Lighting as a motivated design

Record physical sources and their relationship to the subject and camera:
- source and motivation (window, lamp, neon, practical, sun);
- direction relative to the camera for the shot;
- height, apparent size/quality and shadow behavior;
- key, fill, rim/kicker and background separation roles;
- lit/shadow-side relationship or a plainly described contrast;
- color temperature/palette and practical environment;
- what must remain consistent across adjacent shots and what changes for dramatic reasons.

"Moody lighting" is not an executable specification. Describe what produces the light, where it comes from, what it illuminates, what remains in shadow and why.

## 6. From keyframe to motion

When identity, wardrobe, composition or geography matters:
1. approve a named/versioned keyframe;
2. check identity, costume, prop state, composition, camera view and lighting;
3. only then compile the motion request;
4. describe one dominant action chain, camera behavior, environmental motion and explicit endpoint;
5. compare generated clip with approved keyframe and shot specification.

A labelled feasibility probe may be exempt from delivery approval if it is explicitly disposable and cannot silently become a final asset. Faceless plates or inserts may use other routes when identity is not at stake, but continuity still applies.

## 7. Quality checks

- Every shot has a dramatic function and traceable source.
- Staging is understandable before lens choice.
- Camera position reveals rather than obscures the intended geometry.
- Screen direction and eyelines are coherent across cuts.
- The start state, action and end state can be independently checked.
- The selected lens/move has a stated purpose.
- Lighting sources and directions are physically and dramatically motivated.
- A keyframe is reviewed before costly generation where required.
- Technical prompt completeness does not substitute for directorial approval.

## 8. Failure diagnosis

| Symptom | Likely root | Repair owner |
|---|---|---|
| Random coverage or beautiful but purposeless shots | No beat/function or visual thesis | Node 03 / 05 |
| Camera cannot clarify who dominates | Blocking geometry unresolved | Node 08, then 06 |
| Characters appear on wrong sides after reverse shots | Scene anchors and axis not established | Node 08 / 06 / 05 |
| Model fails to place subjects across depth | Scene relationship not translated to camera-relative view | Node 05 / 08 |
| Face/costume is correct in still but drifts in motion | Keyframe/identity anchors or motion complexity | Node 10 / 11 / 12 |
| Light changes unpredictably between cuts | Source/direction/invariant not specified | Node 07 / 09 |
| Shot requires many simultaneous actions | Shot complexity exceeds execution capability | Node 05 / 11 / 12 |

## 9. Limits

This entry synthesizes source-grounded methods, not a universal directing formula. Model-specific shot durations, prompt recipes and risk scores must be versioned adapters, not fixed directing laws. Real performance, optics and lighting decisions require professional review and, where possible, production evidence.

## Source provenance

- `cajias/agentic-video-skills` — commit `204cefd08bbb87fd4681f1f2b0dccbc444a978c1`; MIT; inspected cinematic-director Skill and its cinematic-language, continuity-bible and tool-adapter references.
- `wuwangzhang1216/DirectorSKILL` — commit `c65ae0d14457053efb1e354c7e7f7e120d97fad1`; MIT; inspected blocking/staging, lighting/color, production workflow, shot-plan template and evaluation instructions.
- `0xhughs/director-skills` — commit `35ca0a2b4cd55b0668aa9ea0f40273324b774bb4`; MIT; inspected shotlist/visual-breakdown and identity-anchor mechanisms.
- `smixs/visual-skills` — commit `92be33a5a73325fb3d8e0c73b22744b114e2a90e`; CC BY 4.0; used only as a cited source for dramaturgy/keyframe concepts. Attribution obligations apply to any future adaptation or redistribution.
- `zenstory-ai/drama-skills` — commit `66b7b3e9e913fcefe81849941c0761facd5b1d5e`; MIT; inspected storyboard, continuity, evaluation and documented blocking-probe material.

All evidence is static source inspection. No upstream code, skill or evaluation suite was executed by this Hub review; the narrow Seedance probe is reported by its upstream project and was not independently reproduced.
