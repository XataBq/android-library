# Architecture

## Current architectural stage

The active product phase is **Phase 3 — Learning Content MVP**. Phase 2 —
Canonical Knowledge Foundation is completed. The repository foundation,
educational topic contracts, competency foundations, learning-sequence
infrastructure, competency-to-topic mapping infrastructure, and first fourteen
production educational topics are implemented. The first learning sequence
version 1 has machine status `approved` and conceptual state `accepted`; source
packages, the canonical competency package, and topics remain in `review`. No
production mapping package exists.

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
        └──────────────→ Competency-to-topic mappings
                               ↓
                      Future authored educational topics
```

This is an editorial and architectural flow, not an automatic generation
pipeline. Source items preserve the meaning, context, and provenance of an
external publication. Evidence links connect versioned source items to
repository-owned canonical competencies, which express stable demonstrable
capabilities independently of any one publication.

Learning sequences are separate pedagogical data that reference a fixed
canonical competency-set version. Their stage order is recommended only within
the authored sequence and creates no canonical relation. Canonical competency
relations remain deferred. Competency-to-topic mapping packages are a separate
implemented domain that owns versioned many-to-many relationships between
canonical competencies and topics; no production mapping packages exist yet.
Educational topics are separately authored learning material; fourteen production
topic packages currently exist in `review`, and they are not generated
automatically from competencies.
Learner progress is personal state and remains outside competency, sequence,
mapping, and topic data.

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
├── competency-topic-mappings/  Versioned relationships from competencies to topics
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

The implemented competency-to-topic mapping area currently contains its model
documentation and implementation reports. Future production packages will use
`competency-topic-mappings/<mapping-id>/mapping.yaml`. No such package exists
until production educational topics justify it.

Potential `web/`, `android/`, `backend/`, `shared/`, `tools/`, and `.github/`
areas remain future work. A future directory's presence would not authorize its
implementation.

## Dependency direction

- Source packages preserve publication data and do not depend on canonical
  competencies.
- Canonical competencies may reference versioned source evidence.
- Learning sequences reference one exact canonical competency set and version;
  their order does not create canonical competency relations.
- Competency-to-topic mapping packages reference one exact canonical
  competency-set version and exact topic content versions. The relationship is
  not stored in either referenced domain and is independent from sequences.
- Educational topics remain separately authored content and do not depend on a
  mapping package for their identity or prerequisite semantics.
- Competency data does not depend on clients or learner state.
- Educational content does not depend on web, Android, backend, or database
  models.
- Clients and tooling may depend on stable educational contracts.
- Learner state must refer to stable domain identifiers, not filesystem paths.

## Separate future graphs

Any future canonical competency relation graph would describe relationships
between capabilities. Learning-sequence stage order is contextual pedagogical
guidance. The existing topic prerequisite graph describes dependencies between
authored learning materials. Competency-to-topic mappings describe content
coverage and create none of those relations. These are separate data models and
must not be merged.

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
`review`. Learning sequence version 1 has machine status `approved`, conceptual
state `accepted`, and is not published. Architecture acceptance does not
approve editorial packages. Canonical relations and competency-to-topic
production mappings remain deferred; only the separate mapping infrastructure
is implemented.

## Architecture and package status

Architecture status answers whether a model or decision is the repository's
approved design. Package editorial status answers whether one exact package
version has passed content review. Architecture `ACCEPTED`, task `DONE`, and
publication of a derived artifact do not accept an editorial package.

The repository-wide lifecycle, machine-supported status vocabulary, promotion
criteria, and human approval authority are defined in
[`docs/EDITORIAL_PACKAGE_LIFECYCLE.md`](EDITORIAL_PACKAGE_LIFECYCLE.md).

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
