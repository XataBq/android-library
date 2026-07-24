# Project State

## Project phase

**Current phase: Phase 3 — Learning Content MVP**

Phase 2 — Canonical Knowledge Foundation is completed. Repository-wide package
promotion criteria are defined, and the first learning sequence version 1 has
passed editorial review. Phase 3 remains the active product phase. Phase 2
closure does not approve any other review-stage package.

## Completed capabilities

The repository currently provides:

- documented project vision, principles, architecture boundaries, and a stable
  human + ChatGPT + Codex workflow;
- Git as the source of truth for shared educational content, separated from
  future learner state;
- a canonical educational topic package structure;
- JSON Schemas for `topic.yaml` and `test.yaml`;
- reusable topic templates and schema fixtures;
- repository-local schema and semantic content validation;
- prerequisite dependency-cycle detection and validator unit tests;
- a provenance-preserving competency source model, schemas, templates,
  fixtures, workflow, and validation;
- two Android Developers source packages in `review`;
- an accepted canonical competency architecture, evidence-reference
  validation, and a version 2 Android app architecture competency set in
  `review`;
- a minimal learning-sequence model, validation, fixtures, tests, and authoring
  documentation;
- the first Android app architecture learning sequence version 1 with machine
  status `approved`, conceptual state `accepted`, and no publication;
- separate version 1 competency-to-topic mapping infrastructure, with no
  production mapping packages;
- a repository-wide editorial package lifecycle with exact-version promotion
  criteria for all five package domains;
- eleven production educational topics in `review`, forming the growing
  Learning Content MVP foundation:
  - Architecture Foundations
    (`android-app-architecture-foundations`);
  - UI Layer and UDF
    (`android-ui-layer-and-unidirectional-data-flow`);
  - Data Layer, Repositories and Synchronization
    (`android-data-layer-repositories-and-synchronization`);
  - Domain Layer and Use Cases
    (`android-domain-layer-and-use-cases`);
  - ViewModel and UI State
    (`android-viewmodel-and-ui-state`);
  - Lifecycle and State Restoration
    (`android-lifecycle-and-state-restoration`);
  - Kotlin Coroutines Foundations
    (`kotlin-coroutines-foundations`);
  - Kotlin Structured Concurrency and Supervision
    (`kotlin-structured-concurrency-and-supervision`);
  - Kotlin Flow and Reactive Streams
    (`kotlin-flow-and-reactive-streams`);
  - Android Navigation Architecture
    (`android-navigation-architecture`);
  - Android Networking Architecture
    (`android-networking-architecture`).

## Completed tasks

- **Task 000 — DONE:** Established the repository structure, project rules,
  architecture boundaries, and initial decision record.
- **Task 001 — DONE:** Defined the YAML and Markdown educational content model,
  schemas, templates, fixtures, and author documentation.
- **Task 002 — DONE:** Added the repository-local validator, semantic checks,
  deterministic diagnostics, tests, and validation documentation.
- **Task 003 — completed:** Synchronized the documented project state and moved
  the roadmap to Phase 2.
- **Task 004 — DONE:** Defined the provenance-preserving competency source
  model, schemas, fixtures, validator support, templates, and workflow
  documentation.
- **Task 005 — DONE:** Imported the first external source package and recorded
  its extraction review.
- **Task 006 — DONE:** Implemented the proposed canonical competency model,
  evidence validation, fixtures, tests, and a small canonical pilot. Task 006.1
  completed its editorial and technical review.
- **Task 006.2 — DONE:** Synchronized the repository architecture and
  normalization workflow documentation.
- **Task 007 — DONE:** Imported the second Android Developers architecture
  source package and recorded its review.
- **Task 008 — DONE:** Normalized the second source across the canonical
  registry and advanced the canonical set to version 2.
- **Task 009 — DONE:** Implemented the minimal ordered-stage learning-sequence
  model and the first review-stage Android architecture sequence.
- **Task 010 — DONE:** Reviewed and accepted the canonical competency model as
  repository architecture without changing package editorial states.
- **Task 011 — DONE:** Implemented the separate competency-to-topic mapping
  model without creating a production mapping.
- **Task 012.1 — DONE:** Added the first production topic as the architecture
  foundations baseline.
- **Task 012.2 — DONE:** Added the second production topic for the Android UI
  layer and Unidirectional Data Flow.
- **Task 012.3 — DONE:** Added the third production topic for the Android Data
  layer, repositories, and synchronization.
- **Task 013 — DONE:** Reframed the project roadmap around learning content,
  automation, distribution, product validation, and deferred expansion.
- **Task 014 — DONE:** Defined the repository-wide editorial package lifecycle
  and exact-version promotion criteria without promoting any package.
- **Task 015 — DONE:** Editorially reviewed and accepted the first learning
  sequence version 1, applied machine status `approved`, and formally closed
  Phase 2 without promoting its canonical dependency.
- **Task 016 — DONE:** Added the fourth production Android architecture topic
  covering the optional Domain layer and focused use cases.
- **Task 017 — DONE:** Added the fifth production Android architecture topic
  covering ViewModel scope, UI state, lifecycle, restoration, and testing.
- **Task 018 — DONE:** Added the sixth production Android architecture topic
  covering component lifecycles, saved state, process recreation, navigation
  ownership, and Binder transport limits.
- **Task 019 — DONE:** Added the seventh production topic covering Kotlin
  coroutine execution, suspension, dispatchers, cancellation, Android scope
  ownership, layer boundaries, and virtual-time testing.
- **Task 020 — DONE:** Added the eighth production topic covering Job-tree
  propagation, fail-fast and supervised execution, partial success, timeout,
  cleanup, and long-lived Android work ownership.
- **Task 021 — DONE:** Added the ninth production topic covering cold and hot
  Flow semantics, operators, sharing, lifecycle-aware collection, architecture
  boundaries, and deterministic stream testing.
- **Task 022 — DONE:** Added the tenth production topic covering navigation
  ownership, back-stack state, routes, scopes, results, external entry points,
  restoration, and architecture-focused testing.
- **Task 023 — DONE:** Added the eleventh production topic covering HTTP
  semantics, Data-layer network boundaries, resilient calls, authentication,
  TLS, caching, pagination, file transfer, and layered testing.

## Current focus

Phase 3 focuses on producing and reviewing a coherent Learning Content MVP that
is useful directly from the repository. Tasks 012.1–012.3 and Tasks 016–023
provide the growing eleven-topic foundation; all eleven topic packages remain in
`review`.

Structured Concurrency and Supervision is recorded editorially as
**Junior Core — advanced foundation**. The Junior Core target is exactly 17
mandatory topics. Eleven currently exist as complete production packages in
`review`; six remain:

12. Dependency Injection and Scoping
13. Android Testing Foundations
14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

The final Junior/Middle boundary is deferred until the full Junior Core is
implemented and reviewed; this is a curriculum decision, not a universal
industry grading claim.

The canonical competency model is `ACCEPTED` repository architecture, while
both source packages and the version 2 canonical competency package remain in
`review`. The first learning sequence version 1 is `approved`/conceptually
`accepted` under a documented exact-version dependency exception and is not
published. Canonical competency relations are deferred. Competency-to-topic
mapping infrastructure is implemented, but no production mapping package
exists.

Phase 2 is formally closed. This closure does not promote source packages, the
canonical competency package, topics, or mappings.

## Next planned work

The next work is planned, not yet approved as numbered implementation tasks:

1. Review and expand the eleven existing production packages toward the exact
   17-topic mandatory Junior Core target.
2. Create production competency-to-topic mappings against exact reviewed
   package versions.
3. Extend usable Markdown navigation and prepare the first generated catalog
   when real content justifies it.
4. Add link and source/reference audits, freshness metadata, editorial release
   rules, and CI validation.
5. Proceed toward a stable content compiler and versioned publication bundle.

The six remaining mandatory topics are Dependency Injection and Scoping,
Android Testing Foundations, Android Security Foundations, Local Persistence
with Room, Background Work and WorkManager, and Compose Foundations. These
topics have no assigned task numbers.

## Known non-goals and deferred work

The repository does not yet provide:

- accepted or published source, canonical competency, or educational-topic
  packages;
- a published learning-sequence package;
- canonical competency relations;
- production competency-to-topic mapping packages;
- a generated catalog, content compiler, or versioned publication bundle;
- a web client or Telegram integration;
- a user database, accounts, or synchronized progress;
- AI learning services, an AI tutor, or NotebookLM integration;
- an Android client;
- a CI workflow;
- validated monetization, revenue, customers, or market demand;
- a custom backend or B2B platform.

NotebookLM exports, audio summaries, slides, and generated visualizations are
optional future derived outputs, not canonical knowledge. Monetization items
are unvalidated experiments. Custom backend and B2B capabilities remain
deferred until justified by product requirements.

## Context restoration

For a new contributor or AI session, use this reading order:

1. `README.md`
2. `docs/PROJECT_STATE.md`
3. `docs/ROADMAP.md`
4. the relevant task file under `tasks/`
5. the relevant architecture and content documents under `docs/`

Git and the files in this repository are the source of truth. Prior chat history
is not.
