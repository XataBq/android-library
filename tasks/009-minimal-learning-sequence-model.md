# Task 009 — Minimal Learning Sequence Model

Status: DONE

## Objective

Implement the first repository-native learning-sequence model and one reviewed Android app architecture learning sequence.

The model must describe an authored pedagogical order through canonical competencies without introducing canonical competency relations, semantic prerequisites, adaptive routing, or learner-progress behavior.

## Architectural basis

Read before implementation:

1. `README.md`
2. `docs/PROJECT_STATE.md`
3. `docs/ROADMAP.md`
4. `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`
5. `docs/COMPETENCY_NORMALIZATION_WORKFLOW.md`
6. `research/architecture-studies/001-canonical-competency-relations.md`
7. `research/architecture-studies/002-learning-sequence-model.md`
8. `AGENTS.md`

The architecture study is authoritative for Task 009.

## Core decision

A learning sequence is a separate pedagogical model.

It references canonical competencies but does not modify their identity or define semantic relations between them.

A sequence contains ordered stages. Each stage contains one or more canonical competency references.

Stage order means:

> competencies in an earlier stage are recommended to be learned before competencies in a later stage within this authored sequence.

It does not mean:

- semantic prerequisite;
- mandatory dependency;
- canonical competency relation;
- inability to assess a later competency independently;
- universal ordering across all learning paths.

## Scope

Implement:

- one JSON Schema for learning-sequence YAML;
- repository-local semantic validation;
- valid and invalid fixtures;
- validator unit tests;
- one real reviewed sequence package;
- author documentation;
- project-state and roadmap synchronization.

Do not implement:

- canonical competency relations;
- graph edges between competencies;
- `requires`, `supports`, `recommended-before`, or similar relation records;
- branching conditions;
- weights or difficulty scores;
- learner progress;
- adaptive sequencing;
- topic mapping;
- generated catalogs;
- backend, web, or Android client behavior.

## Proposed repository layout

Use existing repository conventions where possible. Prefer:

```text
schemas/
  learning-sequence.schema.json

learning-sequences/
  android-app-architecture-foundations/
    sequence.yaml
    README.md

fixtures/
  learning-sequences/
    valid/
    invalid/

docs/
  LEARNING_SEQUENCE_MODEL.md
  LEARNING_SEQUENCE_AUTHORING.md

research/
  architecture-studies/
    002-learning-sequence-model.md

tasks/
  009-minimal-learning-sequence-model.md
```

If the repository already has a more specific naming or fixture convention, follow it consistently and document any deviation.

## Learning-sequence schema

The first schema version must support this conceptual shape:

```yaml
schema_version: 1
sequence_id: android-app-architecture-foundations
sequence_version: 1
title: Android app architecture foundations
description: >
  A foundational learning path through the canonical Android app architecture
  competency set.
language: en
status: review

competency_set:
  id: android-app-architecture
  version: 2

stages:
  - id: platform-constraints
    title: Platform constraints
    rationale: >
      Establish the Android lifecycle and process constraints that motivate later
      architecture decisions.
    competencies:
      - explain-android-component-lifecycle-constraints
```

### Required top-level fields

Require:

- `schema_version`
- `sequence_id`
- `sequence_version`
- `title`
- `language`
- `status`
- `competency_set`
- `stages`

### Allowed top-level fields

Allow only the documented fields. Suggested optional fields:

- `description`
- `editorial_notes`

Do not add speculative extensibility fields.

### Field constraints

At minimum:

- `schema_version` must currently equal `1`;
- `sequence_id` must follow the repository's stable ID convention;
- `sequence_version` must be a positive integer;
- `title` must be non-empty;
- `language` must follow the repository's existing language convention;
- `status` must reuse the repository's existing editorial-status vocabulary where appropriate;
- `competency_set.id` must be non-empty;
- `competency_set.version` must be a positive integer;
- `stages` must contain at least one stage.

### Stage constraints

Each stage must require:

- `id`
- `title`
- `competencies`

Allow optional:

- `rationale`
- `editorial_notes`

Require:

- non-empty stage ID;
- non-empty title;
- at least one competency reference;
- no duplicate competency ID inside a stage.

Do not introduce ordering fields inside a stage.

## Semantic validation

Extend the existing competency validator or add a narrowly scoped repository-local learning-sequence validator, following current project conventions.

The validator must detect:

1. referenced canonical competency set does not exist;
2. referenced canonical competency set version does not match;
3. referenced competency ID does not exist in the selected set/version;
4. duplicate stage IDs inside one sequence;
5. duplicate competency references within one stage;
6. duplicate competency references across different stages of the same sequence;
7. empty stages;
8. malformed sequence packages according to schema;
9. duplicate `sequence_id` plus `sequence_version` packages, if repository layout permits multiple packages.

Diagnostics must be deterministic and follow the repository's existing diagnostic style.

Do not infer or validate semantic prerequisites.

## First real sequence

Create:

```text
learning-sequences/android-app-architecture-foundations/
```

Use:

```yaml
sequence_id: android-app-architecture-foundations
sequence_version: 1
competency_set:
  id: android-app-architecture
  version: 2
status: review
language: en
```

Before writing the final YAML, read the canonical competency package and use exact existing competency IDs. Do not reconstruct IDs from titles.

The sequence must contain these stages and intended competencies.

### Stage 1 — Platform constraints

- Explain Android component lifecycle constraints.

### Stage 2 — Foundational boundaries

- Apply separation of concerns.
- Design independent Android app components.
- Isolate Android framework dependencies.

### Stage 3 — State and data principles

- Explain single source of truth.
- Explain unidirectional data flow.
- Persist relevant data models.

### Stage 4 — UI architecture

- Explain UI-layer responsibilities.
- Design ViewModel UI state.
- Select UI state holders by scope.
- Handle lifecycle work in Compose UI.

### Stage 5 — Data architecture

- Explain repository responsibilities.
- Design a data layer around repositories.
- Use coroutines and flows across layers.

### Stage 6 — Dependency management

- Explain dependency injection.
- Scope dependencies when needed.

### Stage 7 — Application composition

- Design single-activity navigation.
- Evaluate an optional domain layer.
- Evaluate layer-specific models.

Add concise rationale text for every stage.

## Sequence package README

The package README must explain:

- intended audience;
- learning goal;
- competency-set version used;
- why stages are ordered this way;
- that order is recommended rather than mandatory;
- that competencies inside one stage are not semantically ordered;
- that the package remains in `review`.

Do not duplicate the entire authoring guide.

## Fixtures

Add valid fixtures covering at least:

- minimal valid sequence;
- valid multi-stage sequence;
- optional description and rationale fields.

Add invalid fixtures covering at least:

- missing required top-level field;
- unsupported schema version;
- empty stages;
- empty stage competencies;
- duplicate stage IDs;
- duplicate competency within one stage;
- duplicate competency across stages;
- unknown competency-set ID;
- wrong competency-set version;
- unknown competency ID;
- unexpected property if schemas use closed objects.

Use fixture naming consistent with existing repository conventions.

## Tests

Add unit tests for:

- schema acceptance and rejection;
- every semantic validation rule;
- deterministic diagnostic order;
- successful validation of the real sequence package;
- repository-wide validation remaining successful.

Do not weaken existing tests or validation rules.

## Documentation

Create `docs/LEARNING_SEQUENCE_MODEL.md` covering:

- purpose of the model;
- separation from canonical competency identity;
- stage semantics;
- versioning;
- validation rules;
- deliberate non-goals.

Create `docs/LEARNING_SEQUENCE_AUTHORING.md` covering:

- how to choose a competency set/version;
- how to group competencies into stages;
- how to write stage rationales;
- how to decide when a separate sequence is preferable to branching;
- how to version a changed sequence;
- validation command.

Documentation must explicitly state:

- stage order is pedagogical;
- canonical relations remain deferred;
- alternative routes are separate sequence packages in version 1;
- topics are not sequence nodes yet.

## Architecture study placement

Add the approved study at:

```text
research/architecture-studies/002-learning-sequence-model.md
```

Keep the relation research at:

```text
research/architecture-studies/001-canonical-competency-relations.md
```

The second study should reference the first study's conclusion that canonical relations are deferred.

## Project synchronization

Update all relevant project documents, including at least:

- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`

The updated state must say:

- canonical competency relations were researched and deferred;
- the minimal learning-sequence model is now implemented;
- the first Android app architecture sequence exists in `review`;
- topic mapping and authored educational content remain future work.

Do not claim that the learning sequence is approved or published.

## Validation commands

Run all existing validation and test commands plus the new learning-sequence checks.

At minimum, preserve successful execution of the repository's current competency and content validation suites.

Document the exact commands and results in the implementation report.

## Implementation report

Add a Task 009 implementation report using the repository's established convention.

The report must include:

- files added and modified;
- schema decisions;
- semantic validation rules;
- fixture and test coverage;
- exact canonical competency set/version referenced;
- exact sequence stage summary;
- commands executed and results;
- deviations from this task;
- deferred work.

## Acceptance criteria

Task 009 is complete only when:

- the learning-sequence schema exists and rejects malformed data;
- semantic validation resolves the referenced canonical set/version and all competency IDs;
- duplicate stages and duplicate competency references are rejected;
- valid and invalid fixtures cover the required cases;
- tests cover all new rules and pass;
- the real Android architecture sequence uses exact canonical IDs;
- the sequence contains all seven approved stages;
- documentation clearly separates pedagogical order from canonical relations;
- the architecture study is stored under `research/architecture-studies/`;
- project-state documentation is synchronized;
- all repository validation and tests pass;
- no canonical relation model or prerequisite graph was introduced.

## Expected result

After Task 009, the repository should support one minimal, validated, versioned learning path through canonical competencies while preserving the independence of:

- canonical competency identity;
- pedagogical ordering;
- future educational topic content;
- future learner progress.
