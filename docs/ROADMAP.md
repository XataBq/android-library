# Project Roadmap

This roadmap describes product development, not the educational competency roadmap.

## Phase 0 — Foundation

**Status: Completed.**

Goal: establish project rules and repository structure.

Deliverables:

- project vision;
- principles;
- architecture boundaries;
- AI collaboration rules;
- development workflow;
- initial ADR;
- task format.

## Phase 1 — Content model

**Status: Completed.**

Goal: define a stable machine-readable representation of topics.

Deliverables:

- topic metadata schema;
- test schema;
- topic templates;
- sample topic package;
- validation rules.

## Phase 2 — Competency import

**Status: Current; not completed.**

Goal: import coherent, provenance-preserving source publications, normalize
their evidence into canonical competencies, and establish the reviewed basis
for a future learning graph.

Implemented foundations:

- source package and source-item model;
- two external source packages in `review`;
- accepted canonical competency model and registry validation;
- one version 2 canonical set normalized across both sources in `review`;
- a cross-source model review and completed architecture acceptance decision;
- canonical competency relation research, with production relations deferred;
- a minimal ordered-stage learning-sequence model;
- one Android app architecture foundations sequence in `review`;
- separate competency-to-topic mapping schema, validation, fixtures, and
  authoring documentation, with no production mapping packages;
- the first production educational topic package,
  `android-app-architecture-foundations`, in `review` as an editorial baseline;
- the second production educational topic package,
  `android-ui-layer-and-unidirectional-data-flow`, in `review`, continuing the
  foundations topic with focused UI-layer and UDF coverage.
- the third production educational topic package,
  `android-data-layer-repositories-and-synchronization`, in `review`, completing
  the current three-topic architecture foundation with Data-layer coverage.

Remaining Phase 2 milestones:

- review the first learning sequence without treating its stage order as
  canonical competency relations.

## Phase 3 — Content repository MVP

Goal: make the repository useful for real learning without an application.

Tasks 012.1–012.3 form the current Android app architecture foundation:
architecture fundamentals, UI-layer and UDF reasoning, and Data-layer
repository and synchronization reasoning. Further production topics and
production mappings remain deferred.

Deliverables:

- first 10–15 reviewed topics;
- production mappings from canonical competencies to authored topics using the
  implemented mapping contract;
- catalog generation;
- content validation;
- internal link checking;
- usable Markdown navigation.

## Phase 4 — Web MVP

Goal: provide a read-only and locally stateful learning interface.

Deliverables:

- topic catalog;
- roadmap visualization;
- topic page;
- Markdown rendering;
- tests;
- local progress;
- search.

## Phase 5 — Synchronized progress

Goal: provide accounts and persistent progress.

Deliverables:

- authentication;
- database;
- attempt history;
- mastery model;
- review queue;
- synchronization.

## Phase 6 — AI tutor

Goal: support open-answer assessment and guided explanations.

Deliverables:

- rubric-based answer evaluation;
- interview mode;
- additional question generation;
- weak-area explanations;
- usage and safety constraints.

## Phase 7 — Android client

Goal: provide an offline-first mobile client.

Deliverables:

- Compose UI;
- Room cache;
- synchronization;
- topic reading;
- tests and review queue;
- notifications;
- offline access.

## Phase 8 — Custom backend

Goal: introduce a Kotlin backend only when product requirements justify replacing or extending the initial backend solution.

Possible deliverables:

- Ktor service;
- PostgreSQL;
- OpenAPI;
- authentication integration;
- Docker;
- integration tests;
- observability.

## Current phase

**Phase 2 — Competency import**
