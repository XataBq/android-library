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
- canonical competency schemas, evidence-reference validation, and a small
  Android app architecture pilot in review.

## Completed tasks

- **Task 000 — DONE:** Established the repository structure, project rules, architecture boundaries, and initial decision record.
- **Task 001 — DONE:** Defined the YAML and Markdown educational content model, schemas, templates, fixtures, and author documentation.
- **Task 002 — DONE:** Added the repository-local validator, semantic checks, deterministic diagnostics, tests, and validation documentation.
- **Task 003 — completed:** Synchronized the documented project state and moved the roadmap to Phase 2.
- **Task 004 — DONE:** Defined the provenance-preserving competency source model, schemas, fixtures, validator support, templates, and workflow documentation.
- **Task 005 — DONE:** Imported the first external source package and recorded its extraction review.
- **Task 006 — DONE:** Implemented the proposed canonical competency model, evidence validation, fixtures, tests, and a small canonical pilot. Task 006.1 completed its editorial and technical review.

## Current focus

Two Android Developers source packages are implemented with `review` status:
`android-developers-app-architecture` and
`android-developers-architecture-recommendations`. Only the first source has a
small canonical Android app architecture pilot, also in `review`. The canonical
model remains `PROPOSED`, and cross-source normalization has not been performed.
Phase 2 remains incomplete.

Task 008 is the next validation milestone: normalize the second source against
the complete existing canonical registry. This will test cross-source evidence
reuse, duplicate review, and canonical wording before an architecture-status
decision.

## Next planned tasks

The immediate planned sequence is:

1. Perform Task 008 cross-source normalization against the existing canonical registry.
2. Decide whether the canonical model can move from `PROPOSED` to `ACCEPTED`.
3. Define competency relations and prerequisites.
4. Define the first learning sequence.
5. Map canonical competencies to authored educational topics.
6. Generate the first content catalog.
7. Create reviewed educational topics.

Exact task numbers for this work have not yet been approved.

## Known non-goals and deferred work

The completed foundation and content tooling do not yet provide:

- real published educational topic content;
- approved competency source packages;
- approved canonical competency packages;
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
