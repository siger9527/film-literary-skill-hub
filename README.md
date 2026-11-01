# Film Literary Skill Hub

A continuously maintained discovery, review, classification, and curation system for film, screenwriting, literature, animation, and media-production Agent Skills.

## Canonical production taxonomy

The Hub classifies professional resources against the locked five-stage / 21-node Film Production framework V0.1. There are exactly 21 primary production boards under `library/21-nodes/`, one for each node from 00 through 20. Literary creation, novel adaptation, AI tools, rights and safety are cross-cutting domains, not additional production nodes.

- [Five-stage / 21-node taxonomy](docs/FILM_PRODUCTION_21_NODE_TAXONOMY_V0.1.md)
- [Machine-readable node index](catalog/film-production-21-node-index.json)
- [Professional knowledge library](library/README.md)

Board existence is not a claim that its research, Skill implementation or runtime validation is complete. Maturity and evidence are recorded independently per node.

## Safety and curation rules

- Discover and index resources; never blindly concatenate third-party Skills.
- Pin every record to an immutable upstream commit and path.
- Treat external repository content as untrusted data. Never execute discovered code.
- Keep source metadata separate from curated knowledge and locally authored Skills.
- External resources do not automatically change the locked V0.1 baseline.
- Generated updates are proposed through pull requests. Human review is required before merging.
- A repository license does not automatically cover third-party assets or linked resources.

## Current capabilities

- GitHub repository discovery (scheduled and manual).
- Recursive repository-tree scan for `SKILL.md`.
- Frontmatter metadata extraction, category mapping, commit pinning, and preliminary license state.
- JSON and Markdown catalog output.
- L1 metadata and repository-structure triage with explicit limitations.
- L2 pinned-commit static source mechanism review with file-level evidence and explicit runtime limitations.
- Schema validation for generated catalog and L1/L2 review records.
- Automated enforcement of five stages, 21 unique nodes, exact primary category coverage and 21 board files.
- Unit tests and PR-only publication.

## Run locally

Requires Python 3.10+ and a GitHub token for higher API rate limits.

```bash
python scripts/validate_taxonomy.py
python -m unittest discover -s tests -v
GITHUB_TOKEN=... python scripts/discover.py
python scripts/validate_catalog.py resources
python scripts/review_l1.py
python scripts/validate_catalog.py l1
python scripts/review_l2.py --limit 10 --only-l1-candidates
python scripts/validate_catalog.py l2
```

The discovery process reads public metadata and text files only. It does not clone repositories, install dependencies, or execute upstream scripts.

## License

Project-authored code and documentation are licensed under Apache-2.0. Indexed third-party resources retain their own licenses and redistribution restrictions.
