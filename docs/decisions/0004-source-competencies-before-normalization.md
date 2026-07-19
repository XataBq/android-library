# ADR 0004: Preserve source competencies before normalization

- Status: Accepted
- Date: 2026-07-19

## Context

Competency matrices, curricula, role expectations, standards, and personal analyses use different terminology, levels, structure, and granularity. Their statements may duplicate, overlap, conflict, or later map many-to-many with canonical competencies and educational topics. Interpreting them during extraction would lose provenance and obscure what each source actually said.

The repository is public, so source representation must also make storage permissions and artifact handling explicit.

## Decision

Store source metadata and faithful source items separately from future canonical competencies. Preserve each statement's source wording, source-local context and level, precise locator, and any transcription caveat.

Use globally stable source IDs and stable source-local item IDs. Use `<source-id>:<item-id>` as the future unambiguous cross-source reference form without treating it as a canonical competency ID.

Require provenance, source version consistency, and an explicit public-repository usage declaration. Raw artifacts are optional because many sources can be cited or transcribed safely without storing the original file, while other permitted sources benefit from checksummed archival material. Citation-only sources cannot store raw artifacts.

Defer competency equivalence, duplicate resolution, canonical identity, relationships, topic mapping, prerequisites, and learning order to later reviewed tasks.

## Consequences

### Positive

- reviewers can trace extracted statements to a source version and location;
- source meaning and terminology remain distinguishable from platform decisions;
- stable IDs support later normalization without mutable array positions;
- checksummed artifacts can detect accidental file changes;
- explicit usage declarations make public-repository review requirements visible;
- normalization can compare multiple preserved sources without rewriting evidence.

### Negative

- source and normalized representations will require separate files and validation;
- duplicate and inconsistent statements remain intentionally unresolved at this stage;
- source-declared levels cannot yet drive platform difficulty or learning order;
- legal permission remains a human judgment beyond schema validation;
- checksum metadata must be updated deliberately when an allowed artifact changes.

## Alternatives considered

### Normalize during extraction

Rejected because it would mix evidence with interpretation, hide source disagreement, and make later review harder.

### Reuse educational topic metadata

Rejected because source statements are neither teaching units nor assessments and must not acquire topic difficulty, prerequisites, or publication semantics.

### Require every original artifact

Rejected because storage may be unnecessary, prohibited, proprietary, access-controlled, or excessive for a public repository.

### Force source levels into a shared enum

Rejected because mapping labels such as `junior+`, `associate`, or `level-1` is a normalization decision.

## Known limitations

The source model does not resolve duplicates, define canonical competencies, create relationships or learning sequences, map items to topics, verify remote availability, or determine legal permission. Those decisions require later human-reviewed work.
