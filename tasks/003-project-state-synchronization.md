# Task 003 — Synchronize project state and roadmap

- Status: READY
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Synchronize the repository documentation with the actual completed project state and provide one concise document that allows a human or AI contributor to restore the current project context quickly.

## Context

The repository has completed:

- Task 000 — repository foundation;
- Task 001 — educational content model;
- Task 002 — repository content validator.

However, `docs/ROADMAP.md` still declares the current phase as:

```text
Phase 0 — Foundation
```

This no longer reflects the repository state.

The repository now has:

- documented project principles and architecture boundaries;
- a canonical educational topic package;
- YAML metadata schemas;
- JSON Schema validation;
- repository-wide semantic validation;
- tests for the validator.

The next active product phase is:

```text
Phase 2 — Competency import
```

A concise project-state document is needed so that contributors can restore context without relying on chat history.

This task is documentation-only. It must not introduce new product architecture, schemas, scripts, dependencies, competency data, or educational content.

## Required reading

Before making changes, read:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_VISION.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/CONTENT_STRATEGY.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_VALIDATION.md`
- `docs/ROADMAP.md`
- `docs/AI_COLLABORATION.md`
- `docs/decisions/0001-content-and-progress-storage.md`
- `docs/decisions/0002-yaml-content-model-and-json-schema.md`
- `docs/decisions/0003-repository-content-validator.md`
- `tasks/000-foundation.md`
- `tasks/001-content-model.md`
- `tasks/002-content-validator.md`

## Scope

### 1. Create `docs/PROJECT_STATE.md`

Create a concise, factual project-state document.

It must contain the following sections.

#### Project phase

State that:

```text
Current phase: Phase 2 — Competency import
```

Explain briefly that Phase 0 and Phase 1 deliverables are complete enough for the project to proceed.

Do not claim that the entire product or content repository is complete.

#### Completed capabilities

Summarize the capabilities currently present in the repository:

- documented project vision and principles;
- architecture boundaries;
- Git-based educational content source of truth;
- separation of shared content and learner progress;
- canonical topic package structure;
- `topic.yaml` and `test.yaml` schemas;
- topic templates;
- valid and invalid schema fixtures;
- repository-local content validator;
- schema and semantic validation;
- dependency-cycle detection;
- validator unit tests.

Keep this at capability level.

Do not copy large implementation descriptions from completed tasks.

#### Completed tasks

List:

- Task 000 — DONE;
- Task 001 — DONE;
- Task 002 — DONE.

Each task should have a one-sentence outcome summary.

#### Current focus

State that the current focus is to:

- define how source competencies are represented;
- import the first competency source;
- normalize duplicate and overlapping requirements;
- build an approved prerequisite graph;
- define the first learning sequence.

#### Next planned tasks

List the immediate planned sequence:

```text
Task 004 — Define competency source model
Task 005 — Import first competency source
Task 006 — Normalize competencies
Task 007 — Build prerequisite graph
Task 008 — Approve first learning sequence
Task 009 — Generate content catalog
Task 010+ — Create first reviewed educational topics
```

Make clear that task numbers after Task 003 describe the current plan and may be refined through normal architecture review.

#### Known non-goals and deferred work

State that the repository currently does not yet provide:

- real published educational topic content;
- competency import data;
- generated catalog;
- web application;
- Android application;
- backend;
- user accounts;
- synchronized progress;
- AI tutor;
- CI workflow.

This section must distinguish clearly between completed infrastructure and future product features.

#### Context restoration

Include a short recommended reading order for a new contributor or a new AI session:

1. `README.md`
2. `docs/PROJECT_STATE.md`
3. `docs/ROADMAP.md`
4. relevant task file
5. relevant architecture and content documents

State that Git is the source of truth, not prior chat history.

### 2. Update `docs/ROADMAP.md`

Make focused changes only.

Required changes:

1. Change the `Current phase` section from:

```text
Phase 0 — Foundation
```

to:

```text
Phase 2 — Competency import
```

2. Mark Phase 0 as completed in a concise and unambiguous way.

3. Mark Phase 1 as completed in a concise and unambiguous way.

4. Do not mark Phase 2 as completed.

5. Do not redesign or substantially rewrite the roadmap phases.

The roadmap must remain a product-development roadmap rather than a task tracker.

### 3. Update `README.md`

Add `docs/PROJECT_STATE.md` to the `Start here` reading sequence.

The preferred reading order should make the current state visible near the beginning, after the high-level project vision and principles.

Keep the existing content-validation guidance intact.

### 4. Update Task 003 status

The task file begins with:

```text
Status: READY
```

Codex may change it to:

```text
Status: IN_PROGRESS
```

while implementing.

It must not be changed to `DONE` before human and ChatGPT review.

## Acceptance criteria

- [ ] `docs/PROJECT_STATE.md` exists.
- [ ] The document accurately reflects Tasks 000–002.
- [ ] The current phase is stated as `Phase 2 — Competency import`.
- [ ] Completed capabilities are described without claiming unfinished product features.
- [ ] Immediate next tasks are documented.
- [ ] Deferred work is explicitly separated from completed work.
- [ ] The document includes a context-restoration reading order.
- [ ] `docs/ROADMAP.md` marks Phase 0 as completed.
- [ ] `docs/ROADMAP.md` marks Phase 1 as completed.
- [ ] `docs/ROADMAP.md` identifies Phase 2 as current.
- [ ] Phase 2 is not marked completed.
- [ ] Existing later roadmap phases are not materially redesigned.
- [ ] `README.md` links to `docs/PROJECT_STATE.md`.
- [ ] No application code, schema, validator logic, dependency, fixture, or competency data is added.
- [ ] All referenced repository paths exist.
- [ ] The final report lists every changed file and all validation results.

## Forbidden changes

- adding competency schemas or competency files;
- importing a competency matrix;
- modifying the topic or test schemas;
- modifying validator behavior;
- adding or changing Python dependencies;
- adding CI;
- generating application projects;
- creating web, Android, backend, or database code;
- introducing a new ADR;
- renumbering completed tasks;
- rewriting the project vision or principles;
- declaring unfinished phases complete;
- changing Task 003 to `DONE` before review;
- broad wording changes unrelated to project-state synchronization.

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B -m unittest discover
git diff --check
git status --short
```

Also verify manually:

- every path referenced by `docs/PROJECT_STATE.md` exists;
- README links to `docs/PROJECT_STATE.md`;
- the roadmap current phase is Phase 2;
- Phase 0 and Phase 1 are marked completed;
- Phase 2 remains incomplete.

## Deliverables

1. `tasks/003-project-state-synchronization.md`
2. `docs/PROJECT_STATE.md`
3. focused update to `docs/ROADMAP.md`
4. focused update to `README.md`
5. Codex final report containing:
   - implementation summary;
   - changed files;
   - validation commands and results;
   - assumptions;
   - unresolved issues;
   - explicit confirmation that no product code, schema, validator behavior, dependencies, competency data, or CI configuration were added.
