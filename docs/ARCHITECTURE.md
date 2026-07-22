# Architecture

## Current architectural stage

The repository is currently in **Phase 2 — Competency import**. The repository
foundation, educational topic contracts, source competency model, and first
canonical competency model are implemented. Current work focuses on
provenance-preserving source import, editorial canonicalization, and reviewed
pedagogical sequences through canonical competencies.

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
        ├──────────────→ Authored learning sequences
        ├──────────────→ Future canonical relations (deferred)
        └──────────────→ Future educational-topic mappings
                               ↓
                      Authored educational topics
```

This is an editorial and architectural flow, not an automatic generation
pipeline. Source items preserve the meaning, context, and provenance of an
external publication. Evidence links connect versioned source items to
repository-owned canonical competencies, which express stable demonstrable
capabilities independently of any one publication.

Learning sequences are separate pedagogical data that reference a fixed
canonical competency-set version. Their stage order is recommended only within
the authored sequence and creates no canonical relation. Canonical competency
relations remain deferred.
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
├── learning-sequences/  Authored pedagogical paths through canonical competencies
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

The implemented learning-sequence area is organized as:

```text
learning-sequences/
├── <sequence-id>/  Versioned sequence YAML and package README
└── reports/        Sequence implementation and review records
```

Potential `web/`, `android/`, `backend/`, `shared/`, `tools/`, and `.github/`
areas remain future work. A future directory's presence would not authorize its
implementation.

## Dependency direction

- Source packages preserve publication data and do not depend on canonical
  competencies.
- Canonical competencies may reference versioned source evidence.
- Learning sequences reference one exact canonical competency set and version;
  their order does not create canonical competency relations.
- Educational topics may later map to canonical competencies, but this
  architecture does not yet define that mapping.
- Competency data does not depend on clients or learner state.
- Educational content does not depend on web, Android, backend, or database
  models.
- Clients and tooling may depend on stable educational contracts.
- Learner state must refer to stable domain identifiers, not filesystem paths.

## Separate future graphs

Any future canonical competency relation graph would describe relationships
between capabilities. Learning-sequence stage order is contextual pedagogical
guidance. The existing topic prerequisite graph describes dependencies between
authored learning materials. These are separate data models and must not be
merged.

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

`docs/architecture/CANONICAL_COMPETENCY_MODEL.md` is `ACCEPTED` as the
repository architecture for stable, source-independent, evidence-backed
competencies. Both source packages and the canonical competency set remain in
`review`, as does learning sequence version 1. Architecture acceptance does not
approve those editorial packages. Canonical relations and competency-to-topic
mappings remain deferred.

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
