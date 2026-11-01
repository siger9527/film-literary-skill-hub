# L2 Source Review: Screenwriting and Novel Adaptation Skills

Review date: 2026-11-01

This review advances the literary-development portion of the Skill Hub. It distinguishes repository claims, inspected source mechanisms, professional interpretation and runtime evidence. No upstream code was executed.

## 1. jtydhr88/screenwriting-skills

- Repository: https://github.com/jtydhr88/screenwriting-skills
- Pinned commit: `51115f18d160aa8b2ac5813e4432b6f0b425358f`
- Repository license: MIT (`LICENSE` at pinned commit).
- Repository's README claims 26 Agent Skills and a knowledge base distilled from 47 craft books and 23 published-script/play volumes. These are upstream author claims, not independently audited counts.
- Inspected files: `README.md`; `plugins/screenwriting/skills/sw-workflow/SKILL.md`; `sw-workflow/reference.md`; `sw-story-structure/SKILL.md`; `sw-scene-craft/SKILL.md`; `sw-premise-theme/SKILL.md`; `sw-character-conflict/SKILL.md`; `LICENSE`.

### Strong mechanisms

1. **Workflow sequencing and persistent state:** the workflow Skill routes projects through premise, structure, character, scene list, draft, revision and submission; defines deliverables and advisory exit checks; maintains a Story Bible for resumption; and explicitly permits stage rollback when later writing reveals upstream defects.
2. **Medium-specific routes:** feature/stage play, series, short form and Chinese opera are not forced through one universal sequence. The source uses separate route tables and explains when specialist Skills enter.
3. **Story design as competing lenses:** structure frameworks are compared and assigned different functions instead of being presented as one universally correct formula.
4. **Scene-level professional reasoning:** scene work is tied to value change, conflict, objectives/tactics, beats, subtext, location, props, suspense and entry/exit points.
5. **Character/opponent design:** character differentiation, objective/obstacle/stakes, opposing forces, motive and conflict escalation are treated as causal systems.
6. **Session continuity:** decisions are stored as conclusions; changes are logged; large artifacts remain separate from the compact project bible.

### Limitations and risks

- A large combined Skill library can overwhelm an agent if the orchestrator does not load only the relevant specialist knowledge.
- Several beat-sheet/page-position recommendations are model-specific heuristics. They should be selected by medium, genre, runtime and intended audience, not treated as universal law.
- The repository says it derives material from many books and published scripts. MIT licensing of repository files does not independently settle the copyright status of every underlying source quotation, example or adaptation. The Hub will not copy upstream passages or reference corpora; only independently written summaries of inspected mechanisms will be retained.
- The workflow's exit checks are advisory craft checks, not objective proof that a screenplay is good.
- The source's tests and comparison claims were inspected only where present; no runtime or controlled quality experiment was executed by this review.

### Disposition

**L2_SOURCE_REVIEWED (static source inspection only).** High-value reference for nodes 01–02, especially premise/theme, structure, character conflict, scene craft and project continuity. Do not import as a monolithic replacement for the locked V0.1 nodes.

## 2. egguy886/write-screenplay-skill

- Repository: https://github.com/egguy886/write-screenplay-skill
- Pinned commit: `fd2404312b2d4fa1e0b0381529de9d9cf21da547`
- Repository license: MIT (`LICENSE` at pinned commit).
- Inspected files: `README.zh-CN.md`; `SKILL.md`; `references/novel-to-script-engine.md`; `references/long-novel-adaptation.md`; `references/character-and-dialogue.md`; `references/production-bible.md`; `scripts/outline_check.py`; `scripts/bible_check.py`; adaptation templates and example JSON files.

### Strong mechanisms

1. **Novel-to-screenplay conversion:** separates prose interiority and authorial explanation from visible action, audible dialogue and information carried by props, behavior and conflict.
2. **Long-form adaptation is planned before drafting:** chapter indexing and beat cards precede compression decisions, episode budgeting, episode outlines and script drafting.
3. **Source fidelity is checked against the actual manuscript:** chapter cards are treated as provisional; chapter openings, middles and endings must be checked against the full text before adaptation decisions are finalized.
4. **Compression decisions are explicit:** preserve, merge, combine characters/locations, montage, move events and cut material each require reasons; the adaptation ledger can record canon conflicts and deletions.
5. **Production Bible bridges writing and production:** character dramatic/language/visual/voice attributes, costume variants, props, locations and voice assets receive stable IDs and are cross-checked against scripts.
6. **Executable outline checks:** the inspected `outline_check.py` checks episode numbering, chapter coverage or documented cuts, opening payoffs, required fields, hook type/strength and episode-count limits, then emits a readable outline.
7. **Human approval remains at critical creative gates:** the README and workflow require user approval of adaptation parameters and episode outlines before expensive downstream production.

### Limitations and risks

- The repository is explicitly optimized for vertical micro-drama and adaptation into bounded episode counts. Its defaults (for example, 60-episode caps, 2-minute pacing, hook rotation and short scene budgets) are not universal rules for feature films, literary drama, animation or slower serial storytelling.
- Its opening-hook and cliffhanger prescriptions can create repetitive escalation if used as mandatory formulas.
- Some checks are structural proxies: a hook type or field being present does not establish emotional impact, originality, dramatic necessity or faithful adaptation.
- The source's strong production-asset model is useful for AI production, but asset IDs and visual constraints must remain subordinate to story and directing intent.
- Static inspection of scripts does not establish that the tools run correctly; no runtime execution was performed here.

### Disposition

**L2_SOURCE_REVIEWED (static source inspection only).** High-value specialist reference for node 02 adaptation, serialization, production-bible handoff and continuity. Apply its workflow selectively by target format.

## 3. DenisHumen/cinema-skills

- Repository: https://github.com/DenisHumen/cinema-skills
- Pinned commit: `0ea4971cc5022c616e14b8eb572fb818433d1219`
- Repository license: MIT (repository `LICENSE`).
- Inspected tree and README, discipline directory READMEs, templates and `scripts/validate_skills.py`.
- The pinned tree describes ten discipline folders with planned-skill checklists, templates, bibliography and a validator. The inspected discipline files are README/checklist placeholders rather than a complete body of operational SKILL.md implementations.

### Disposition

**REVIEWED_L1; not promoted to L2.** Useful as a taxonomy/template/validator reference and a candidate to monitor as it develops. Current evidence does not support treating it as a mature set of ten executable professional Skills.

## 4. Cross-source conclusion

The strongest complementary pattern is:

- jtydhr88: deep craft knowledge and a staged writing workflow;
- egguy886: novel-adaptation controls, chapter-level traceability, serialized outline checks and production-asset continuity;
- cinema-skills: discipline taxonomy and reusable packaging conventions, currently at an early skeleton stage.

These sources do not replace one another and should not be merged by concatenating their Skills. Their reusable mechanisms are being translated into separate knowledge entries with explicit applicability and limits.

## Evidence boundary

- All three repository commits are pinned.
- File paths and blob-level evidence were read from those commits.
- License files were inspected at those commits.
- No third-party code was executed.
- No upstream runtime tests were run.
- No upstream source text or reference corpora are copied into the Hub.
