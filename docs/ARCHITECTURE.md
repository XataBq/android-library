# Architecture

## Current architectural stage

The repository is currently in the **Foundation** phase.

No production application architecture is considered final yet.

## System boundaries

The project has two primary data categories.

### Educational content

Examples:

- topic metadata;
- theory;
- cheat sheets;
- tests;
- practice;
- interview questions;
- references;
- roadmap dependencies.

Planned storage:

- Markdown;
- YAML or JSON;
- Git repository.

### Personal learning state

Examples:

- progress;
- attempts;
- scores;
- mastery;
- weak areas;
- review dates;
- personal notes.

Planned storage evolution:

1. local browser storage for the earliest web MVP;
2. persistent database when synchronization is introduced;
3. local Android database plus synchronization for offline-first support.

## Target high-level architecture

```text
                 Git repository
              educational content
                       |
          +------------+------------+
          |                         |
    content tooling              CI validation
          |                         |
          +------------+------------+
                       |
                    Web client
                       |
             Progress API / BaaS
                       |
                  PostgreSQL
                       |
                 Android client
```

## Repository areas

```text
android-library/
├── docs/          Project and architecture documentation
├── content/       Educational content
├── schemas/       Machine-readable content schemas
├── templates/     Templates for new topics and tasks
├── scripts/       Content validation and generation tools
├── tasks/         Approved implementation tasks
├── web/           Future web application
├── android/       Future Android application
├── backend/       Future custom backend, only when justified
├── shared/        Future shared contracts or generated artifacts
├── tools/         Developer tooling that does not belong in scripts
└── .github/       CI, issue templates, and repository automation
```

Empty future directories may contain `.gitkeep`. Their presence does not authorize implementation.

## Dependency direction

Educational content must not depend on:

- web code;
- Android code;
- backend code;
- database models.

Clients and tooling may depend on content contracts.

Personal progress models must refer to stable topic identifiers rather than filesystem paths.

## Initial topic package

A topic is expected to evolve toward:

```text
content/<track>/<section>/<topic>/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

The exact schemas will be approved in a dedicated task.

## Architecture decision records

Important decisions are recorded in:

```text
docs/decisions/
```

ADR naming format:

```text
NNNN-short-decision-title.md
```

Example:

```text
0001-markdown-content-postgresql-progress.md
```
