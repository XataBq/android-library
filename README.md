# Android Library

A competency-driven learning platform and knowledge base for Android and
software engineering.

## Current status

The active product phase is **Phase 3 — Learning Content MVP**. Phase 2 —
Canonical Knowledge Foundation is near completion; it still requires editorial
review of the first learning sequence, explicit package-promotion criteria, and
formal phase closure.

The canonical competency model is the repository's `ACCEPTED` architecture.
Architecture acceptance does not approve editorial packages: the two Android
Developers source packages, version 2 canonical Android app architecture
competency set, and first learning sequence all remain in `review`.

Tasks 012.1–012.3 form the current three-topic Android app architecture
foundation:

- Architecture Foundations;
- UI Layer and UDF;
- Data Layer, Repositories and Synchronization.

All three production educational topics remain in `review`. Competency-to-topic
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
6. Read `docs/DEVELOPMENT_WORKFLOW.md`.
7. Read `docs/COMPETENCY_SOURCE_MODEL.md` before recording competency sources.
8. Read the [competency import workflow](docs/COMPETENCY_IMPORT_WORKFLOW.md)
   before importing a source publication.
9. Read the [canonical competency model](docs/architecture/CANONICAL_COMPETENCY_MODEL.md)
   before normalizing source evidence.
10. Read the [competency normalization workflow](docs/COMPETENCY_NORMALIZATION_WORKFLOW.md)
    before adding evidence or canonical competencies.
11. Read the [learning-sequence model](docs/LEARNING_SEQUENCE_MODEL.md) and
    [authoring guide](docs/LEARNING_SEQUENCE_AUTHORING.md) before changing a
    sequence.
12. Read the [competency-to-topic mapping model](docs/COMPETENCY_TOPIC_MAPPING_MODEL.md)
    and [authoring guide](docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md) before
    creating a future mapping package.
13. Run `python -B scripts/validate_competencies.py` after changing source,
    canonical competency, learning-sequence, or competency-to-topic mapping
    packages.
14. Read `docs/CONTENT_MODEL.md` before authoring educational content.
15. Run `python -B scripts/validate_content.py` after adding or changing topic
    content.
16. Read `docs/CONTENT_VALIDATION.md` for content-validator rules and
    diagnostics.
17. Read `AGENTS.md` before using an AI coding agent.
