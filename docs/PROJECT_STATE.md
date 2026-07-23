# Project State

## Project phase

**Current phase: Phase 2 — Competency import**

Phase 0 and Phase 1 deliverables are complete enough for the project to proceed to competency import. This does not mean that the product or educational content repository is complete.

## Completed capabilities

The repository currently provides:

- documented project vision, principles, and architecture boundaries;
- Git as the source of truth for shared educational content;
- separation between shared content and learner progress;
- a canonical educational topic package structure;
- JSON Schemas for `topic.yaml` and `test.yaml`;
- reusable topic templates;
- valid and intentionally invalid schema fixtures;
- a repository-local content validator;
- separate schema and repository-wide semantic validation;
- prerequisite dependency-cycle detection;
- unit tests for validator behavior;
- a provenance-preserving competency source model and templates;
- competency source schemas, fixtures, and repository-local validation;
- two real competency source packages, each with review documentation;
- an accepted canonical competency architecture, canonical schemas,
  evidence-reference validation, and a version 2 Android app architecture set
  normalized across both sources in review;
- a minimal ordered-stage learning-sequence schema, semantic reference
  validation, fixtures, tests, and authoring documentation;
- the first Android app architecture foundations sequence in `review`;
- a separate version 1 competency-to-topic mapping schema, cross-domain
  reference validation, fixtures, tests, and authoring documentation.
- the first production educational topic package,
  `android-app-architecture-foundations`, in `review` as the editorial baseline
  for later topics.
- the second production educational topic package,
  `android-ui-layer-and-unidirectional-data-flow`, in `review`, with the
  foundations topic as its prerequisite.
- the third production educational topic package,
  `android-data-layer-repositories-and-synchronization`, in `review`, with the
  foundations and UI-layer topics as prerequisites.

## Completed tasks

- **Task 000 — DONE:** Established the repository structure, project rules, architecture boundaries, and initial decision record.
- **Task 001 — DONE:** Defined the YAML and Markdown educational content model, schemas, templates, fixtures, and author documentation.
- **Task 002 — DONE:** Added the repository-local validator, semantic checks, deterministic diagnostics, tests, and validation documentation.
- **Task 003 — completed:** Synchronized the documented project state and moved the roadmap to Phase 2.
- **Task 004 — DONE:** Defined the provenance-preserving competency source model, schemas, fixtures, validator support, templates, and workflow documentation.
- **Task 005 — DONE:** Imported the first external source package and recorded its extraction review.
- **Task 006 — DONE:** Implemented the proposed canonical competency model, evidence validation, fixtures, tests, and a small canonical pilot. Task 006.1 completed its editorial and technical review.
- **Task 006.2 — DONE:** Synchronized the repository architecture and normalization workflow documentation.
- **Task 007 — DONE:** Imported the second Android Developers architecture source package and recorded its review.
- **Task 008 — DONE:** Normalized the second source across the canonical registry and advanced the canonical set to version 2.
- **Task 009 — DONE:** Implemented the minimal ordered-stage learning-sequence model and the first review-stage Android architecture sequence.
- **Task 010 — DONE:** Reviewed and accepted the canonical competency model as repository architecture without changing package editorial states.

- **Task 011 — DONE:** Implemented the separate competency-to-topic mapping model without creating a production mapping.
- **Task 012.1 — DONE:** Added the first production topic as the architecture foundations baseline.
- **Task 012.2 — DONE:** Added the second production topic for the Android UI layer and Unidirectional Data Flow.
- **Task 012.3 — DONE:** Added the third production topic for the Android Data layer, repositories, and synchronization.

## Current focus

Two Android Developers source packages are implemented with `review` status:
`android-developers-app-architecture` and
`android-developers-architecture-recommendations`. Cross-source normalization
has been performed against both packages. The resulting canonical Android app
architecture package is version 2 and remains in `review`.

The cross-source review recommendation has been accepted: the canonical
competency model is now `ACCEPTED` repository architecture. This does not
change the editorial state of either source package or the canonical package;
all remain in `review`. Canonical competency relations were researched and
deferred. The minimal learning-sequence model is implemented, and
the `android-app-architecture-foundations` learning sequence version 1 also
remains in `review`.
Competency-to-topic mapping infrastructure is implemented as a separate domain,
but there are no production mapping packages. The first production educational
topic, `android-app-architecture-foundations` version 1, now exists in `review`.
It remains the architectural and editorial foundation for the second production
topic, `android-ui-layer-and-unidirectional-data-flow` version 1, which also
exists in `review`. The third production topic,
`android-data-layer-repositories-and-synchronization` version 1, deepens Data
ownership, repository boundaries, and synchronization and also remains in
`review`. Tasks 012.1–012.3 form the current Android app architecture
foundation. Production competency-to-topic mappings remain deferred.

## Next planned tasks

The immediate planned sequence is:

1. Review the first learning sequence as an editorial package without treating
   its stage order as canonical competency relations.
2. Review the first production educational topic as an editorial package.
3. Author further production Android topics after Task 012.3.
4. Author production competency-to-topic mappings against exact reviewed topic
   and canonical package versions without treating topics as sequence nodes.
5. Generate the first content catalog when real content justifies it.

Exact task numbers for the later mapping and catalog work have not yet been
approved.

## Known non-goals and deferred work

The completed foundation and content tooling do not yet provide:

- real published educational topic content;
- approved competency source packages;
- approved canonical competency packages;
- approved or published learning-sequence packages;
- canonical competency relations;
- production competency-to-topic mapping packages;
- a generated content catalog;
- a web application;
- an Android application;
- a backend;
- user accounts;
- synchronized learner progress;
- an AI tutor;
- a CI workflow.

These are future product or content capabilities, not part of the completed infrastructure.

## Context restoration

For a new contributor or AI session, use this reading order:

1. `README.md`
2. `docs/PROJECT_STATE.md`
3. `docs/ROADMAP.md`
4. the relevant task file under `tasks/`
5. the relevant architecture and content documents under `docs/`

Git and the files in this repository are the source of truth. Prior chat history is not.
