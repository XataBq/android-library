# Task 011 — Minimal Competency-to-Topic Mapping Model

Status: DONE

## Objective

Introduce the first repository-native Competency-to-Topic Mapping model.

The mapping model connects stable canonical competencies with authored educational topics without changing the identity, ownership, or semantics of either model.

This task defines only the mapping architecture.

Do not introduce production mappings or authored educational topics.

## Architectural motivation

The repository already contains:

- accepted canonical competency architecture;
- canonical competency packages;
- educational topic model;
- learning-sequence model.

However, there is currently no repository-native answer to the question:

> Which authored educational topics intentionally teach a given canonical competency?

The mapping model fills this gap.

It is a separate domain model.

It is not:

- part of canonical competencies;
- part of topic metadata;
- part of learning sequences.

## Required reading

Read before implementation:

1. AGENTS.md
2. README.md
3. docs/PROJECT_STATE.md
4. docs/ROADMAP.md
5. docs/architecture/CANONICAL_COMPETENCY_MODEL.md
6. docs/CONTENT_MODEL.md
7. docs/LEARNING_SEQUENCE_MODEL.md
8. docs/COMPETENCY_NORMALIZATION_WORKFLOW.md
9. Task 001
10. Task 006
11. Task 009
12. Task 010

The accepted canonical competency model is authoritative.

## Core decision

Introduce a separate mapping package.

Conceptually:

Canonical Competency
        ↕
Competency-to-Topic Mapping
        ↕
Educational Topic

The mapping owns the relationship.

Neither competencies nor topics own the relationship.

## Relationship cardinality

The model must support many-to-many relationships.

One competency may reference many topics.

One topic may reference many competencies.

## Meaning of a mapping

A mapping means:

> This topic intentionally teaches knowledge or skills required to demonstrate the referenced canonical competency.

A mapping does NOT imply:

- learner mastery;
- assessment completion;
- prerequisite relationships;
- learning-sequence ordering;
- full competency coverage beyond the declared mapping;
- publication approval.

## Scope

Implement:

- mapping JSON Schema;
- repository semantic validation;
- fixtures;
- validator tests;
- author documentation;
- architecture documentation;
- project synchronization.

Do NOT implement:

- production mapping packages;
- authored educational topics;
- competency relations;
- assessment mapping;
- learner progress;
- generated catalogs;
- web/backend/Android behaviour.

## Repository layout

Preferred structure:

schemas/
    competency-topic-mapping.schema.json

competency-topic-mappings/
    README.md

fixtures/
    competency-topic-mappings/
        valid/
        invalid/

docs/
    COMPETENCY_TOPIC_MAPPING_MODEL.md
    COMPETENCY_TOPIC_MAPPING_AUTHORING.md

tasks/
    011-minimal-competency-topic-mapping-model.md

Use existing repository conventions if names differ.

## Schema

The first schema version should support:

schema_version: 1

mapping_id: android-app-architecture-topics
mapping_version: 1

language: en
status: review

competency_set:
    id: android-app-architecture
    version: 2

mappings:
  - competency_id: explain-repository-responsibilities

    topics:
      - topic_id: repository-responsibilities
        content_version: 1
        coverage: primary

## Required top-level fields

Require:

- schema_version
- mapping_id
- mapping_version
- language
- status
- competency_set
- mappings

Optional:

- description
- editorial_notes

No speculative extension fields.

## Coverage model

Version 1 supports exactly two values:

coverage:
- primary
- partial

Definitions:

primary

The topic is intentionally designed to teach the competency as one of its primary educational goals.

partial

The topic intentionally teaches only part of the competency.

No percentages.

No weights.

No scores.

No confidence values.

## Field constraints

Require:

schema_version == 1

positive mapping_version

non-empty mapping_id

valid language

existing editorial status vocabulary

positive competency_set.version

non-empty mappings

## Mapping constraints

Each mapping requires:

- competency_id
- topics

Each topic reference requires:

- topic_id
- content_version
- coverage

Optional:

- rationale

No ordering field.

## Semantic validation

Validator must detect:

1. competency set does not exist

2. competency set version mismatch

3. competency does not exist

4. referenced topic does not exist

5. topic content_version mismatch

6. duplicate competency entries

7. duplicate topic references inside one competency

8. duplicate competency/topic pairs

9. duplicate mapping package ID/version

10. malformed YAML root

Diagnostics must remain deterministic.

## Fixtures

Add valid fixtures covering:

- minimal mapping package
- multiple competencies
- multiple topic references
- primary coverage
- partial coverage

Invalid fixtures:

- missing required field
- unsupported schema version
- duplicate competency
- duplicate topic
- unknown competency set
- wrong competency-set version
- unknown competency
- unknown topic
- wrong topic version
- invalid coverage value
- unexpected property

## Tests

Add tests for:

- schema acceptance
- schema rejection
- every semantic validation rule
- deterministic diagnostics
- repository validation remaining successful

Do not weaken existing validation.

## Documentation

Create:

docs/COMPETENCY_TOPIC_MAPPING_MODEL.md

Cover:

- purpose
- ownership
- many-to-many relationships
- coverage semantics
- versioning
- validation
- deliberate non-goals

Create:

docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md

Cover:

- selecting competency set
- selecting topic version
- when to use primary
- when to use partial
- versioning
- validation command

Documentation must explicitly state:

- mapping is independent from learning sequences;
- mapping is independent from competency identity;
- mapping does not define prerequisites;
- mapping does not imply learner mastery.

## No production mapping

Do NOT create:

competency-topic-mappings/android-app-architecture/

There are currently no production educational topics.

Use fixtures only.

Production mappings will be introduced in a future task.

## Project synchronization

Update:

README.md

docs/PROJECT_STATE.md

docs/ROADMAP.md

The project state should describe the mapping model as implemented infrastructure while clearly stating that no production mapping packages exist yet.

## Validation

Run:

python -B scripts/validate_competencies.py

python -B scripts/validate_content.py

python -B -m unittest discover

git diff --check

Record commands and results.

## Implementation report

Create a Task 011 implementation report using repository conventions.

Include:

- files added
- schema decisions
- validation rules
- fixtures
- tests
- deferred work
- commands executed
- deviations

## Acceptance criteria

Task 011 is complete only when:

- mapping schema exists;
- semantic validator resolves competency and topic references;
- duplicate mappings are rejected;
- fixtures cover required cases;
- tests pass;
- documentation is synchronized;
- no production mapping package is created;
- no competency relations are introduced;
- no authored educational topics are introduced.

## Expected result

After Task 011 the repository supports a validated, versioned Competency-to-Topic Mapping model while keeping:

- canonical competencies;
- educational topics;
- learning sequences;
- learner progress

as independent architectural concepts.
