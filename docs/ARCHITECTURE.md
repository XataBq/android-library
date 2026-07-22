# Architecture

## Current architectural stage

The repository is currently in **Phase 2 — Competency import**. The repository
foundation, educational topic contracts, source competency model, and first
canonical competency model are implemented. Current work focuses on
provenance-preserving source import and editorial canonicalization.

No production client architecture is considered final yet.

## System boundaries

The project has two primary data categories.

### Educational content

Examples:

- imported competency source packages and source items;
- canonical competencies and their evidence links;
- topic metadata;
- theory;
- cheat sheets;
- tests;
- practice;
- interview questions;
- references;
- roadmap dependencies.

Storage:

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

## Competency-to-content flow

The current and future educational domains follow this conceptual flow:

```text
External publication
        ↓
Source package
        ↓
Source items
        ↓
Evidence links
        ↓
Canonical competencies
        ↓
Future relations and learning sequence
        ↓
Educational topics
```

This is an editorial and architectural flow, not an automatic generation
pipeline. Source items preserve the meaning, context, and provenance of an
external publication. Evidence links connect versioned source items to
repository-owned canonical competencies, which express stable demonstrable
capabilities independently of any one publication.

Competency relations and learning sequences are future domain data.
Educational topics are separately authored learning material; they are not
generated automatically from competencies. Learner progress is personal state
and remains outside both competency and topic data.

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
├── competencies/  Imported evidence, canonical competencies, and review reports
├── content/       Authored educational topic packages
├── docs/          Project, workflow, and architecture documentation
├── schemas/       Machine-readable content and competency schemas
├── templates/     Templates for topics, source packages, and tasks
├── scripts/       Repository-local validation tools
└── tasks/         Approved implementation tasks
```

The implemented competency area is organized as:

```text
competencies/
├── sources/       Immutable, versioned representations of external publications
├── normalized/    Repository-owned canonical competency sets and evidence links
└── reports/       Import and normalization review records
```

Potential `web/`, `android/`, `backend/`, `shared/`, `tools/`, and `.github/`
areas remain future work. A future directory's presence would not authorize its
implementation.

## Dependency direction

- Source packages preserve publication data and do not depend on canonical
  competencies.
- Canonical competencies may reference versioned source evidence.
- Educational topics may later map to canonical competencies, but this
  architecture does not yet define that mapping.
- Competency data does not depend on clients or learner state.
- Educational content does not depend on web, Android, backend, or database
  models.
- Clients and tooling may depend on stable educational contracts.
- Learner state must refer to stable domain identifiers, not filesystem paths.

## Separate future graphs

The future competency prerequisite or relation graph describes relationships
between canonical capabilities. The existing topic prerequisite graph describes
authored learning-material dependencies between educational topics. They may
inform one another, but they are separate data models and must not be merged.

## Educational topic package

The current topic contract uses:

```text
content/<track>/<section>/<topic>/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

The topic and test schemas are implemented under `schemas/`. Topic packages and
their prerequisite graph remain separate from canonical competency data.

## Canonical model status

`docs/architecture/CANONICAL_COMPETENCY_MODEL.md` remains `PROPOSED`. The first
canonical competency set exercises the model with one source, but a second
independent source and cross-source normalization are still required before an
acceptance decision.

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
