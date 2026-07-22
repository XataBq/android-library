# Android Library

A competency-driven learning platform and knowledge base for Android and software engineering.

## Current status

The project is in **Phase 2 — Competency import**. The first real competency
source package, `android-developers-app-architecture`, is implemented with
`review` status. One canonical Android app architecture competency set is also
implemented as a `review`-stage pilot. The source is only partially normalized;
the next validation milestone is importing a second independent source and
normalizing it against the existing canonical registry.

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
10. Run `python -B scripts/validate_competencies.py` after changing source or canonical competency packages.
11. Read `docs/CONTENT_MODEL.md` before authoring educational content.
12. Run `python -B scripts/validate_content.py` after adding or changing topic content.
13. Read `docs/CONTENT_VALIDATION.md` for content-validator rules and diagnostics.
14. Read `AGENTS.md` before using an AI coding agent.
