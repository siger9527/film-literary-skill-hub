# Professional Knowledge Entry: Deterministic Media Execution and Verification

**Entry ID:** `PKB-MEDIA-001`  
**Domain:** Media execution / technical verification  
**V0.1 mapping:** Nodes 13–19, especially 14, 15 and 19; evidence support for node 20  
**Evidence level:** L2 source inspection  
**Runtime status:** NOT_TESTED  
**Upstream:** [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill)  
**Pinned commit:** `1ce2c186bf1dba96132d87274eee46df4f537e0e`  
**License evidence:** repository `LICENSE` identifies MIT; this entry is an independently authored summary.

## Professional principle

Creative intent and media execution are separate responsibilities. The professional node defines what the shot or sequence must achieve; deterministic tools execute bounded operations and report what actually happened. Technical verification can establish measurable media properties, but cannot certify narrative or artistic quality.

## Mechanisms observed in source

1. The Skill workflow emphasizes probing actual media, planning, executing, checking and verifying, while keeping creative choices with the responsible editor/director.  
   Evidence: `SKILL.md`, workflow and responsibility-boundary sections.
2. Shared execution code implements process timeouts, child-process tracking and structured timeout reporting.  
   Evidence: `scripts/_common/runner.py`, around lines 1400–1545.
3. Output locking attempts exclusive lock-file creation to prevent concurrent writers targeting the same output. If lock creation fails with an OS error, it warns and continues without a lock.  
   Evidence: `scripts/_common/runner.py`, around lines 865–930.
4. Linux child processes receive parent-death handling; the source documents that macOS and Windows do not have the same mechanism.  
   Evidence: `scripts/_common/runner.py`, around lines 1460–1535.
5. Batch processing writes cache updates through a sibling temporary file followed by `os.replace`, and uses a thread lock for in-process cache mutation. This does not establish cross-process transactional coordination.  
   Evidence: `scripts/batch.py`, around lines 360–510.
6. The verification command probes media, conditionally plans real operations, records passed/failed/skipped steps, and returns failure when required steps fail.  
   Evidence: `scripts/verify.py`, around lines 140–275.

## Transferable production design

For our system, every execution request should be compiled from a versioned professional specification and contain:
- source media references and content identity;
- target shot/sequence IDs;
- operation and exact parameters;
- expected output path and format;
- timeout, cancellation and recovery policy;
- required technical checks;
- creative acceptance criteria supplied by the responsible node;
- execution receipt and output identity.

The tool result must be separate from the professional acceptance decision.

## Technical evidence vs creative acceptance

**Technical verification can measure**
- file existence and readability;
- codec, container, dimensions and frame rate;
- duration and timebase;
- audio channel layout and sample rate;
- loudness and peak measurements;
- decode/encode success;
- output identity/hash;
- required streams and delivery profile.

**Technical verification cannot independently determine**
- whether the cut preserves dramatic intent;
- whether a reaction shot is emotionally correct;
- whether camera movement communicates the intended perspective;
- whether a color grade supports the scene;
- whether music and silence are dramatically appropriate;
- whether the finished work is coherent and compelling.

Node 20 must independently assess the complete work against creative, continuity, rights, and technical criteria.

## Critical limitations found

- A failed output-lock creation can allow execution to continue without mutual exclusion; this is a concurrency/integrity risk.
- Outer-process timeout handling kills the direct child process; OS-specific descendant cleanup differs.
- A thread lock protects in-process cache mutation, not arbitrary cross-process writers.

These are source-based risk observations. They were not dynamically reproduced in this review.

## Inputs and outputs

**Inputs**
- Approved, version-pinned edit/processing specification.
- Media references and probe metadata.
- Tool/encoder versions and environment.
- Technical acceptance profile.
- Creative acceptance criteria.

**Outputs**
- Execution receipt with command/parameters/tool version.
- Output media reference and content identity.
- Probe and verification report.
- Warnings, failures, skipped checks and recovery state.
- Separate professional acceptance record.

## Acceptance criteria

An execution adapter is acceptable only when tests prove:
- invalid media and invalid parameters fail explicitly;
- output collisions are detected before overwrite;
- cancellation and timeout stop or account for all child processes;
- partial outputs cannot be mistaken for completed deliverables;
- output identity is recorded and rechecked;
- required technical checks are not silently skipped;
- cache hits are invalidated when source or output identity changes;
- verification failure prevents delivery acceptance;
- technical pass does not automatically imply creative acceptance.

## Boundary

This knowledge entry supports deterministic execution and technical QC. It does not replace the professional authority of nodes 03–09, 15–18 or the independent release authority of node 20.
