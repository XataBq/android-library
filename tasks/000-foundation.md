# Task 000 — Establish repository foundation

- Status: DONE
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Establish the documented foundation of the `android-library` repository without implementing product features.

## Context

The repository is intended to become a competency-driven learning platform and knowledge base for Android and software engineering.

The project is currently in Phase 0 — Foundation.

## Required reading

Before making changes, read:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_VISION.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/AI_COLLABORATION.md`
- `docs/CONTENT_STRATEGY.md`
- `docs/ROADMAP.md`
- `docs/decisions/0001-content-and-progress-storage.md`

## Scope

1. Ensure the repository contains these top-level directories:

   - `docs/`
   - `docs/decisions/`
   - `content/`
   - `schemas/`
   - `templates/`
   - `scripts/`
   - `tasks/`
   - `web/`
   - `android/`
   - `backend/`
   - `shared/`
   - `tools/`
   - `.github/`

2. Preserve all foundation documents supplied with this task.

3. Add `.gitkeep` only to empty directories that Git would otherwise ignore.

4. Add a root `.gitignore` containing only broadly justified entries for:

   - operating-system files;
   - IDE-local files;
   - environment files and secrets;
   - Node build/dependency output;
   - Gradle/Android build output;
   - Python cache and virtual environments.

5. Do not create application source code.

6. Do not initialize Next.js, Android, Ktor, Supabase, a database, or CI workflows.

7. Inspect existing repository contents and avoid overwriting useful user-created files without reporting the conflict.

## Acceptance criteria

- [ ] All required directories exist.
- [ ] Foundation documents are present and internally consistent.
- [ ] Empty required directories are tracked using `.gitkeep` where necessary.
- [ ] `.gitignore` exists and does not ignore educational content or project documentation.
- [ ] No frameworks or product source code are added.
- [ ] No secrets or machine-specific configuration are committed.
- [ ] Markdown links and referenced paths in foundation documents are valid.
- [ ] `git status` contains only expected foundation changes.
- [ ] The final report lists every changed file and any assumptions.

## Forbidden changes

- choosing a final web, backend, or Android architecture;
- adding dependencies;
- adding generated application projects;
- adding educational topic content;
- importing competency matrices;
- redesigning the repository structure;
- broad wording rewrites that change approved meaning.

## Validation

Run appropriate local checks, including:

```bash
git status --short
git diff --check
```

If a Markdown link checker is already available, run it. Do not add a dependency solely for this task.

## Deliverables

1. Repository foundation files.
2. Required empty directories.
3. Root `.gitignore`.
4. Codex final report containing:
   - implementation summary;
   - changed files;
   - checks run and results;
   - unresolved issues;
   - explicit confirmation that no product code or dependencies were added.
