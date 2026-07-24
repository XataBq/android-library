# Project Roadmap

This roadmap describes product development, not the educational competency
roadmap. Phase deliverables are planning boundaries, not approved implementation
tasks. No dates are assigned.

## Phase 0 — Project Foundation

**Status: Completed.**

Purpose: establish project rules, ownership, architectural boundaries, AI
collaboration rules, workflow, ADR usage, and task format.

## Phase 1 — Structured Content Foundation

**Status: Completed.**

Purpose: define stable machine-readable educational-topic contracts and
validation infrastructure.

Implemented:

- topic metadata and test schemas;
- the canonical topic package structure;
- templates and fixtures;
- repository-local schema and semantic content validation;
- prerequisite cycle detection;
- validator unit tests.

## Phase 2 — Canonical Knowledge Foundation

**Status: Completed.**

Purpose: create a provenance-preserving and source-independent knowledge
foundation.

Implemented:

- a competency source model;
- two Android Developers source packages in `review`;
- the canonical competency model, accepted as repository architecture;
- the version 2 Android app architecture competency set in `review`;
- evidence references and a normalization workflow;
- canonical relation research, with production relations deferred;
- a minimal learning-sequence model;
- the first learning sequence version 1 editorially accepted with machine
  status `approved`, but not published, under a documented dependency
  exception;
- competency-to-topic mapping infrastructure, with no production mapping
  packages;
- repository-wide exact-version package lifecycle and promotion criteria.

Architecture acceptance does not approve source, canonical competency, or
learning-sequence packages.

Phase 2 closed after the first learning sequence received an `APPROVE`
disposition. Both source packages and the canonical competency package remain
in `review`; canonical competency relations remain deferred unless a real use
case requires them.

## Phase 3 — Learning Content MVP

**Status: Current.**

Purpose: make the repository useful as a standalone learning product before
building a client.

The implemented baseline is the four-topic Android app architecture foundation
from Tasks 012.1–012.3 and Task 016. All four topics remain in `review`:

- Architecture Foundations (`android-app-architecture-foundations`);
- UI Layer and UDF (`android-ui-layer-and-unidirectional-data-flow`);
- Data Layer, Repositories and Synchronization
  (`android-data-layer-repositories-and-synchronization`);
- Domain Layer and Use Cases (`android-domain-layer-and-use-cases`).

Target deliverables:

- 10–15 reviewed production topics;
- one coherent reviewed learning path;
- production competency-to-topic mappings;
- a generated topic catalog;
- usable Markdown navigation;
- internal link validation;
- source and reference audit;
- freshness metadata;
- a CI workflow;
- editorial release rules.

Future content planning candidates, without approved task numbers:

- ViewModel and UI State;
- Android Lifecycle and State Restoration;
- Kotlin Coroutines Foundations;
- Structured Concurrency;
- Networking Architecture;
- Dependency Injection;
- Navigation;
- Testing;
- Android Security Foundations.

## Phase 4 — Content Automation and Compiler

**Status: Planned.**

Purpose: transform repository-authored Markdown and YAML into stable,
machine-readable publication artifacts.

Planned deliverables:

- generated catalog;
- content compiler;
- normalized JSON bundle;
- versioned content releases;
- content and asset manifests;
- checksums;
- search index;
- prerequisite graph export;
- competency coverage export;
- CI build artifacts;
- publication validation.

Conceptual flow:

```text
Markdown / YAML
        ↓
Validation
        ↓
Content compiler
        ↓
Versioned bundle
        ↓
Web / Android / Telegram / AI
```

Clients should consume stable publication contracts rather than repository file
paths.

## Phase 5 — Distribution MVP

**Status: Planned.**

Purpose: validate real demand and content usefulness through lightweight
distribution channels.

Planned web capabilities:

- topic catalog and topic pages;
- prerequisite navigation;
- theory and cheat-sheet rendering;
- tests and search;
- anonymous or local progress;
- analytics and feedback.

Planned Telegram experiments:

- generated drafts and short topic series;
- quizzes and a question of the day;
- links to web content;
- publication analytics.

Candidate validation metrics include topic views, completion, test attempts,
return rate, topic-to-topic navigation, and Telegram-to-web conversion. These
metrics are not yet collected and do not imply product validation.

## Phase 6 — User Platform and Synchronized Progress

**Status: Planned.**

Purpose: introduce persistent personal learning state.

Planned deliverables:

- authentication and a user database;
- topic progress, attempts, and answers;
- competency mastery and weak areas;
- review queue, bookmarks, and notes;
- synchronization;
- product-event analytics.

Data ownership:

```text
Git = source of truth for canonical content
Database = source of truth for user state
```

This roadmap does not define a database schema.

## Phase 7 — AI Learning Services

**Status: Planned.**

Purpose: support guided explanations, assessment, interview practice, and
personalization.

Planned deliverables:

- retrieval over exact content versions and bounded AI context;
- guided explanations and free-text answer evaluation;
- rubric-based assessment and interview simulation;
- weak-area recommendations and additional question generation;
- safety and cost constraints;
- evaluation datasets and answer-quality monitoring.

NotebookLM export packages, audio summaries, slides, and generated
visualizations are optional future integration or export outputs. No such
integration currently exists. AI-generated output is derived presentation
content and must not automatically modify or become canonical knowledge.

## Phase 8 — Android Client

**Status: Planned.**

Purpose: provide an offline-first mobile learning client.

Planned deliverables:

- Compose UI and Room storage;
- content-bundle and progress synchronization;
- topic reader, tests, and review queue;
- notifications, offline assets, and structured visualizations.

The client should consume stable publication contracts.

## Phase 9 — Monetization Experiments

**Status: Planned; experiments may begin earlier.**

Purpose: test willingness to pay before building large commercial
infrastructure.

Candidate experiments:

- paid interview-preparation pack;
- AI interview subscription;
- premium learning paths;
- paid intensive;
- corporate onboarding pilot;
- content licensing.

Possible experiment outcomes include pricing and conversion measurements,
willingness-to-pay feedback, basic unit-economics assumptions, and selection of
a repeatable paid product. Revenue, customers, conversion, willingness to pay,
and market validation have not been established.

## Phase 10 — B2B Platform and Custom Backend

**Status: Deferred until justified.**

Purpose: add organization-specific capabilities only when validated product
requirements require them.

Possible future capabilities:

- private knowledge spaces and source packages;
- corporate competency models, role matrices, and team analytics;
- white-label clients and advanced permissions;
- private AI services, an integration API, and SLA requirements;
- a Kotlin/Ktor backend, PostgreSQL, OpenAPI, Docker, integration tests, and
  observability.

A custom backend is not a goal by itself.

## Current phase

**Phase 3 — Learning Content MVP**

Phase 2 is completed. Its closure did not approve source packages, the
canonical competency package, topics, mappings, or canonical relations.
