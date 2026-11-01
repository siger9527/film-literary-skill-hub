# L1 Source Triage Policy

## Purpose
L1 is a low-cost metadata and repository-structure triage. It decides what deserves human/source-level review next; it does not certify quality.

## Signals
- Source text retrieval succeeded.
- Skill frontmatter contains name and description.
- Repository README exists.
- Repository is archived or active.
- Repository push recency.
- License evidence state is visible.

## Score semantics
`metadata_completeness_score` measures record completeness and maintenance signals only. It is not a skill quality, correctness, safety, or production-readiness score. Stars and forks are recorded as context only and do not improve the score.

## Dispositions
- `BLOCKED`: pinned Skill text could not be read.
- `MANUAL_REVIEW_REQUIRED`: archived source or no license found.
- `L1_CANDIDATE`: metadata completeness score >= 80 with no blocking condition.
- `OBSERVE`: insufficient metadata or maintenance signals.

## Boundaries
L1 does not read all source files, trace tool execution, install dependencies, execute source code, or test runtime behavior. L2 is required to inspect implementation mechanisms and tests. L3 is reserved for critical infrastructure and high-risk paths. A candidate must never be described as approved or production-ready based on L1 alone.
