# Android Library

A competency-driven learning platform and knowledge base for Android and
software engineering.

## Current status

The active product phase is **Phase 3 — Learning Content MVP**. Phase 2 —
Canonical Knowledge Foundation is completed. Repository-wide package promotion
criteria are defined, and the first learning sequence version 1 has been
editorially accepted.

The canonical competency model is the repository's `ACCEPTED` architecture.
Architecture acceptance does not approve editorial packages: the two Android
Developers source packages, version 2 canonical Android app architecture
competency set remain in `review`. The first learning sequence has machine
status `approved`, is conceptually `accepted`, and is not published.

Tasks 012.1–012.3 and Tasks 016–020 form the current eight-topic Learning
Content MVP foundation:

- Architecture Foundations;
- UI Layer and UDF;
- Data Layer, Repositories and Synchronization;
- Domain Layer and Use Cases;
- ViewModel and UI State;
- Lifecycle and State Restoration;
- Kotlin Coroutines Foundations;
- Kotlin Structured Concurrency and Supervision.

All eight production educational topics remain in `review`. Competency-to-topic
mapping infrastructure exists, but no production mapping packages exist.
There is also no generated catalog, web client, user database, synchronized
progress, AI tutor, Android client, or CI workflow yet.

The repository will gradually contain:

- structured educational content;
- competency and dependency-based roadmaps;
- theory, cheat sheets, tests, practice, and interview materials;
- content validation and compilation tools;
- web and Android clients;
- user progress tracking and spaced repetition;
- AI-assisted learning workflows.

## Source of truth

- Git is the source of truth for canonical educational content and project
  documentation.
- A future database will be the source of truth for user-specific state.
- Architecture decisions are recorded in `docs/decisions/`.

## Start here

1. Read `docs/PROJECT_VISION.md`.
2. Read `docs/PROJECT_PRINCIPLES.md`.
3. Read `docs/PROJECT_STATE.md` for the current phase, completed capabilities,
   and next work.
4. Read `docs/ROADMAP.md`.
5. Read `docs/ARCHITECTURE.md`.
6. Read the [editorial package lifecycle](docs/EDITORIAL_PACKAGE_LIFECYCLE.md)
   before reviewing or promoting a versioned package.
7. Read `docs/DEVELOPMENT_WORKFLOW.md`.
8. Read `docs/COMPETENCY_SOURCE_MODEL.md` before recording competency sources.
9. Read the [competency import workflow](docs/COMPETENCY_IMPORT_WORKFLOW.md)
   before importing a source publication.
10. Read the [canonical competency model](docs/architecture/CANONICAL_COMPETENCY_MODEL.md)
   before normalizing source evidence.
11. Read the [competency normalization workflow](docs/COMPETENCY_NORMALIZATION_WORKFLOW.md)
    before adding evidence or canonical competencies.
12. Read the [learning-sequence model](docs/LEARNING_SEQUENCE_MODEL.md) and
    [authoring guide](docs/LEARNING_SEQUENCE_AUTHORING.md) before changing a
    sequence.
13. Read the [competency-to-topic mapping model](docs/COMPETENCY_TOPIC_MAPPING_MODEL.md)
    and [authoring guide](docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md) before
    creating a future mapping package.
14. Run `python -B scripts/validate_competencies.py` after changing source,
    canonical competency, learning-sequence, or competency-to-topic mapping
    packages.
15. Read `docs/CONTENT_MODEL.md` before authoring educational content.
16. Run `python -B scripts/validate_content.py` after adding or changing topic
    content.
17. Read `docs/CONTENT_VALIDATION.md` for content-validator rules and
    diagnostics.
18. Read `AGENTS.md` before using an AI coding agent.
