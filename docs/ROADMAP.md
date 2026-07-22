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
- one Android app architecture foundations sequence in `review`.

Remaining Phase 2 milestones:

- review the first learning sequence without treating its stage order as
  canonical competency relations.

## Phase 3 — Content repository MVP

Goal: make the repository useful for real learning without an application.

Deliverables:

- first 10–15 reviewed topics;
- mappings from canonical competencies to authored topics;
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
