# Film Literary Skill Hub

A continuously maintained discovery, review, classification, and curation system for film, screenwriting, literature, animation, and media-production Agent Skills.

## Safety and curation rules

- Discover and index resources; never blindly concatenate third-party Skills.
- Pin every record to an immutable upstream commit and path.
- Treat external repository content as untrusted data. Never execute discovered code.
- Keep source metadata separate from curated knowledge and locally authored Skills.
- Use the five-stage, 21-node film-production framework V0.1 as a classification lens only; external resources do not automatically change that locked baseline.
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
- Unit tests and PR-only publication.

## Run locally

Requires Python 3.10+ and a GitHub token for higher API rate limits.

```bash
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
