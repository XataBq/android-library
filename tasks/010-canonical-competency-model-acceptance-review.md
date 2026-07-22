# Task 010 — Canonical Competency Model Acceptance Review

Status: DONE

## Objective

Complete the final architecture and consistency review required to decide whether the repository's canonical competency model can move from `PROPOSED` to `ACCEPTED`.

This task concerns the **architecture status of the model**, not the editorial publication status of any competency source package, canonical competency set, or learning sequence.

The task must either:

1. accept the canonical competency model and synchronize the repository documentation; or
2. keep the model `PROPOSED` and record concrete, evidence-based blockers.

Do not change the model to `ACCEPTED` merely because the implementation exists or current tests pass.

## Why this is Task 010

The repository already has an educational Topic Model from Task 001:

- `schemas/topic.schema.json`;
- `schemas/test.schema.json`;
- `docs/CONTENT_MODEL.md`;
- `templates/topic/`;
- `scripts/validate_content.py`.

Therefore Task 010 must not create a second Topic Model.

The immediate unresolved Phase 2 milestone is the architecture-status decision for the canonical competency model.

## Required reading

Read before making changes:

1. `AGENTS.md`
2. `README.md`
3. `docs/PROJECT_STATE.md`
4. `docs/ROADMAP.md`
5. `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`
6. `docs/COMPETENCY_NORMALIZATION_WORKFLOW.md`
7. `competencies/normalized/android-app-architecture/competency-set.yaml`
8. `competencies/normalized/android-app-architecture/competencies.yaml`
9. Task 006 implementation and review artifacts
10. Task 006.1 review artifacts
11. Task 006.2 documentation-sync artifacts
12. Task 008 implementation and cross-source review artifacts
13. `research/architecture-studies/001-canonical-competency-relations.md`
14. `research/architecture-studies/002-learning-sequence-model.md`
15. `docs/LEARNING_SEQUENCE_MODEL.md`
16. `learning-sequences/android-app-architecture-foundations/sequence.yaml`
17. `tasks/009-minimal-learning-sequence-model.md`

Use the actual repository filenames where the implementation and review reports differ from these conceptual names.

## Decision being made

Determine whether this document:

```text
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

can change from:

```text
Status: PROPOSED
```

to:

```text
Status: ACCEPTED
```

Acceptance means:

> The model is the repository's approved architecture for representing stable, source-independent, evidence-backed competencies.

Acceptance does not mean:

- every existing competency is permanently correct;
- the current canonical set is published;
- source packages are approved;
- the learning sequence is approved;
- competency relations are implemented;
- competency-to-topic mappings exist;
- no future schema version will ever be needed.

## Review questions

The implementation report must answer every question below with:

- `PASS`;
- `BLOCKER`;
- or `NOT APPLICABLE`;

and cite concrete repository files or tests.

### 1. Domain separation

Confirm that the repository consistently separates:

- source publications;
- source items;
- evidence references;
- canonical competencies;
- educational topics;
- learning sequences;
- learner progress.

Check for contradictory terminology or ownership assumptions.

### 2. Canonical identity

Confirm that canonical competency identity is:

- stable;
- source-independent;
- not derived from filesystem location;
- not owned by a source package;
- distinct from topic IDs and sequence stage IDs.

### 3. Demonstrability and granularity

Confirm that the model provides sufficiently explicit rules for:

- demonstrable capability;
- one coherent primary idea;
- merge decisions;
- split decisions;
- duplicate and near-duplicate handling;
- canonical wording.

Determine whether these rules are usable by future reviewers without relying on hidden chat context.

### 4. Evidence model

Confirm that:

- every canonical competency requires evidence;
- evidence references exact source package versions;
- referenced source items must exist;
- one source item may support multiple competencies;
- one competency may accumulate evidence from multiple sources;
- imported source packages remain immutable during normalization.

### 5. Versioning and lifecycle

Confirm that the model clearly distinguishes:

- model-document version;
- competency-set version;
- source-package version;
- editorial status;
- semantic changes versus formatting-only changes.

Record any ambiguity that could make future migrations unsafe.

### 6. Validation coverage

Confirm that schemas and repository validation enforce the machine-checkable invariants promised by the model.

At minimum inspect coverage for:

- package shape;
- stable ID patterns;
- package/path consistency;
- duplicate competency IDs;
- evidence source existence;
- evidence source-version matching;
- evidence item existence;
- duplicate evidence references where prohibited;
- deterministic diagnostics;
- malformed YAML root values;
- repository-wide successful validation.

Do not demand that automation enforce editorial judgments such as semantic equivalence.

### 7. Cross-source normalization evidence

Use the two imported Android Developers source packages and canonical set version 2 to determine whether the model has survived a real cross-source normalization exercise.

Confirm that the review evidence demonstrates:

- evidence added to existing competencies where meanings matched;
- new competencies created only for distinct capabilities;
- source-specific wording did not become canonical identity;
- merge/split decisions were documented;
- the canonical set remained coherent after the second import.

### 8. Downstream compatibility

Confirm that Task 009's learning-sequence model can reference canonical competencies without changing their identity or introducing hidden prerequisite semantics.

Confirm that accepting the canonical competency model does not require accepting:

- canonical competency relations;
- the current sequence ordering;
- future topic mappings.

### 9. Known limitations

Confirm that deferred capabilities are explicitly documented and are not accidentally presented as completed:

- canonical competency relations;
- competency-to-topic mappings;
- assessment mappings;
- learner mastery;
- generated catalogs;
- adaptive routing.

A limitation is not automatically a blocker if it is outside the accepted model's scope.

### 10. Documentation consistency

Check at least:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`;
- `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`;
- `docs/COMPETENCY_NORMALIZATION_WORKFLOW.md`;
- learning-sequence documentation.

There must be no contradictory statements about the model's status or implemented capabilities after Task 010.

## Acceptance rule

Change the canonical model status to `ACCEPTED` only when:

1. all architecture-critical review questions pass;
2. no unresolved contradiction changes the meaning of canonical competency identity, evidence, or versioning;
3. current implementation materially matches the documented model;
4. all repository validators and tests pass;
5. the implementation report records the acceptance rationale.

Minor wording issues, missing future features, and deliberately deferred relations are not blockers when they do not invalidate the current model.

If a blocker exists:

- keep `Status: PROPOSED`;
- do not redesign the model opportunistically;
- record the blocker precisely;
- make only minimal documentation corrections that are uncontroversial;
- mark Task 010 as blocked rather than done.

## Allowed changes when accepted

If the decision is `ACCEPT`:

1. Change:

   ```text
   docs/architecture/CANONICAL_COMPETENCY_MODEL.md
   ```

   from `Status: PROPOSED` to `Status: ACCEPTED`.

2. Increment the model-document version only if the repository convention requires it for this status transition. Do not increment canonical competency-set version merely because the architecture document is accepted.

3. Update repository documentation to state clearly:

   - canonical competency architecture is accepted;
   - `android-app-architecture` version 2 remains in `review` unless separately approved;
   - source packages remain in their existing editorial states;
   - learning sequence version 1 remains in `review`;
   - relations and topic mappings remain deferred.

4. Update Task 010 status to `DONE`.

5. Add an implementation/decision report using existing repository conventions.

## Files that must not change merely because of model acceptance

Do not change without a separately justified editorial decision:

- source package status;
- canonical competency-set status;
- individual competency wording;
- canonical competency IDs;
- evidence references;
- canonical competency-set version;
- learning-sequence status;
- learning-sequence ordering;
- topic schemas;
- topic prerequisite semantics.

Do not add a competency relation model.

## Required decision report

Add a Task 010 report using the repository's existing report convention.

Suggested path:

```text
competencies/reports/task-010-canonical-model-acceptance-review.md
```

Use a different existing canonical location if repository conventions require it.

The report must include:

1. final decision: `ACCEPT` or `BLOCKED`;
2. reviewed repository revision;
3. review scope;
4. a matrix covering all ten review questions;
5. concrete evidence paths;
6. validation and test coverage reviewed;
7. cross-source normalization findings;
8. downstream learning-sequence compatibility findings;
9. known limitations and why they are or are not blockers;
10. files changed;
11. exact commands executed and results;
12. deviations from this task;
13. human-owner decision note.

## Human-owner boundary

Codex performs the technical and editorial consistency review, but the repository owner controls final architecture acceptance.

Therefore:

- Codex may recommend `ACCEPT`;
- Codex may prepare the status change when all criteria pass;
- the report must explicitly state that the human owner approves the final status transition through review and commit;
- Codex must not claim independent product authority.

If the repository convention requires the human decision before editing `Status`, Codex must produce the review report first and leave the status unchanged. Follow `AGENTS.md`.

## Tests and validation

Run at minimum:

```bash
python -B scripts/validate_competencies.py
python -B scripts/validate_content.py
python -B -m unittest discover
git diff --check
```

Also run any repository-prescribed command found in `AGENTS.md`, README, or validation documentation.

Record exact command output summaries in the decision report.

## Project synchronization

If accepted, update at least:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`;
- `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`;
- Task 010;
- the Task 010 decision report.

The roadmap should no longer list canonical model acceptance as an unresolved Phase 2 milestone.

Do not automatically mark Phase 2 complete. The first learning-sequence review may remain a separate milestone.

## Out of scope

Task 010 must not implement:

- a new Topic Model;
- competency-to-topic mapping;
- authored educational topics;
- competency relations;
- new learning sequences;
- assessment mapping;
- learner progress;
- catalog generation;
- web, backend, or Android application behavior;
- broad refactoring unrelated to acceptance.

## Acceptance criteria

Task 010 is complete only when:

- all required documents and implementation artifacts were reviewed;
- every review question has a documented result;
- the final decision is supported by repository evidence;
- model status is changed only if all critical criteria pass;
- model status is clearly distinguished from package editorial statuses;
- documentation contains no contradictory current-state claims;
- no canonical IDs, evidence links, package versions, or sequence semantics were silently changed;
- all validators and tests pass;
- the decision report is complete;
- the human-owner boundary is recorded.

## Expected result

After Task 010, the repository has an explicit, auditable answer to:

> Is the canonical competency model accepted as repository architecture?

The result must be either:

- an accepted architecture with synchronized documentation; or
- a still-proposed architecture with precise blockers and a bounded follow-up.
