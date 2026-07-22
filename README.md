# Android Library

A competency-driven learning platform and knowledge base for Android and software engineering.

## Current status

The project is in **Phase 2 — Competency import**. The first real competency
source package, `android-developers-app-architecture`, is implemented with
`review` status and awaits human review; normalization has not started.

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
8. Run `python -B scripts/validate_competencies.py` after adding or changing competency sources.
9. Read `docs/CONTENT_MODEL.md` before authoring educational content.
10. Run `python scripts/validate_content.py` after adding or changing topic content.
11. Read `docs/CONTENT_VALIDATION.md` for content-validator rules and diagnostics.
12. Read `AGENTS.md` before using an AI coding agent.
