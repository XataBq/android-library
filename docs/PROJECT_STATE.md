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
- competency source schemas, fixtures, and repository-local validation.

## Completed tasks

- **Task 000 — DONE:** Established the repository structure, project rules, architecture boundaries, and initial decision record.
- **Task 001 — DONE:** Defined the YAML and Markdown educational content model, schemas, templates, fixtures, and author documentation.
- **Task 002 — DONE:** Added the repository-local validator, semantic checks, deterministic diagnostics, tests, and validation documentation.

## Current focus

The next operational step is importing the first approved competency source. The broader Phase 2 focus remains to:

- import the first competency source;
- normalize duplicate and overlapping requirements;
- build an approved prerequisite graph;
- define the first learning sequence.

## Next planned tasks

The immediate planned sequence is:

1. Task 004 — Define competency source model
2. Task 005 — Import first competency source
3. Task 006 — Normalize competencies
4. Task 007 — Build prerequisite graph
5. Task 008 — Approve first learning sequence
6. Task 009 — Generate content catalog
7. Task 010+ — Create first reviewed educational topics

Task numbers after Task 003 describe the current plan and may be refined through the normal architecture-review process.

## Known non-goals and deferred work

The completed foundation and content tooling do not yet provide:

- real published educational topic content;
- competency import data;
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
