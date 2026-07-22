# Android Library

A competency-driven learning platform and knowledge base for Android and software engineering.

## Current status

The project is in **Phase 2 — Competency import**. Two Android Developers source
packages and the version 2 canonical Android app architecture set remain in
`review`. Canonical competency relations were researched and deferred. A
minimal learning-sequence model and the first Android app architecture sequence
are implemented; the sequence also remains in `review`. The canonical
competency model is now the repository's `ACCEPTED` architecture. This
architecture status does not approve any package.

The repository will gradually contain:

- structured educational content;
- competency and dependency-based roadmaps;
- theory, cheat sheets, tests, practice, and interview materials;
- content validation tools;
- a web client;
- an Android client;
- user progress tracking;
- spaced repetition;
- AI-assisted learning workflows.

## Source of truth

- Educational content and project documentation live in Git.
- User-specific progress will eventually live in a database.
- Architecture decisions are recorded in `docs/decisions/`.

## Start here

1. Read `docs/PROJECT_VISION.md`.
2. Read `docs/PROJECT_PRINCIPLES.md`.
3. Read `docs/PROJECT_STATE.md` for the current phase, completed capabilities, and next work.
4. Read `docs/ARCHITECTURE.md`.
5. Read `docs/DEVELOPMENT_WORKFLOW.md`.
6. Read `docs/COMPETENCY_SOURCE_MODEL.md` before recording competency sources.
7. Read the [competency import workflow](docs/COMPETENCY_IMPORT_WORKFLOW.md) before importing a source publication.
8. Read the [canonical competency model](docs/architecture/CANONICAL_COMPETENCY_MODEL.md) before normalizing source evidence.
9. Read the [competency normalization workflow](docs/COMPETENCY_NORMALIZATION_WORKFLOW.md) before adding evidence or canonical competencies.
10. Read the [learning-sequence model](docs/LEARNING_SEQUENCE_MODEL.md) and [authoring guide](docs/LEARNING_SEQUENCE_AUTHORING.md) before changing a sequence.
11. Run `python -B scripts/validate_competencies.py` after changing source, canonical competency, or learning-sequence packages.
12. Read `docs/CONTENT_MODEL.md` before authoring educational content.
13. Run `python -B scripts/validate_content.py` after adding or changing topic content.
14. Read `docs/CONTENT_VALIDATION.md` for content-validator rules and diagnostics.
15. Read `AGENTS.md` before using an AI coding agent.
