# Task 005 — Import the Android Developers Guide to app architecture

- Status: DONE
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Create the repository's first real competency source package from the official Android Developers publication **Guide to app architecture**.

The result must be a high-quality reference implementation of the source-import workflow established by Task 004. It must demonstrate how to:

- identify one logically coherent external publication;
- record precise provenance;
- preserve the publication's information hierarchy;
- extract source-level competency statements without normalizing them;
- use stable identifiers and useful locators;
- respect public-repository and licensing constraints;
- validate the package with the existing competency validator;
- document extraction decisions sufficiently for later review and updates.

The source package created by this task is:

```text
android-developers-app-architecture
```

The canonical source URL is:

```text
https://developer.android.com/topic/architecture
```

This task imports **only that publication**. It must not import the surrounding Android Developers architecture category, linked sub-guides, recommendation tables, samples, videos, or other pages.

## Context

Task 004 established the source competency model:

```text
source material
    ↓ extraction
source competency items
    ↓ later normalization
canonical competencies
    ↓ later graph design
prerequisites and learning sequences
    ↓ later content work
educational topic packages
```

Task 005 is the first production use of that model.

The source publication currently presents architecture guidance covering areas such as:

- app composition and Android component lifecycle constraints;
- multiple form factors and configuration changes;
- resource constraints and variable launch conditions;
- separation of concerns;
- adaptive layouts;
- driving UI from data models;
- single source of truth;
- unidirectional data flow;
- recommended UI, data, and optional domain layers;
- state holders;
- repositories and data sources;
- modular boundaries;
- testability;
- concurrency responsibility;
- offline-capable data persistence;
- benefits of architecture.

The implementer must inspect the live official page during implementation. This task intentionally does not freeze the publication's full text.

## Source granularity decision

One source package represents one logically coherent publication or independently versioned documentation section.

Do not create a giant package named:

```text
android-developers
```

Do not merge the following into this package:

```text
https://developer.android.com/topic/architecture/recommendations
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/topic/architecture/data-layer
https://developer.android.com/topic/architecture/domain-layer
```

Those are separate publications and may become separate source packages in later tasks.

The package created here represents only:

```text
Guide to app architecture
https://developer.android.com/topic/architecture
```

## Required reading

Before making changes, read:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/PROJECT_VISION.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/CONTENT_STRATEGY.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_VALIDATION.md`
- `docs/COMPETENCY_SOURCE_MODEL.md`
- `docs/ROADMAP.md`
- `docs/AI_COLLABORATION.md`
- `docs/decisions/0004-source-competencies-before-normalization.md`
- `schemas/competency-source.schema.json`
- `schemas/competency-items.schema.json`
- `templates/competency-source/source.yaml`
- `templates/competency-source/items.yaml`
- `scripts/validate_competencies.py`
- `tests/competency_validator/test_validate_competencies.py`
- `tasks/004-competency-source-model.md`

Inspect the live official source page before extracting items.

## Approved architectural constraints

### 1. Source items are not normalized competencies

Each item records one meaningful statement from the source publication.

Do not add:

- canonical competency IDs;
- prerequisite IDs;
- related competency IDs;
- topic IDs;
- educational difficulty;
- learning order;
- mastery criteria;
- learner progress;
- deduplication decisions;
- merge decisions;
- personal assessment;
- inferred role or grade expectations.

Do not rewrite the source into a final learning curriculum.

### 2. Import one publication only

The source boundary is the HTML publication at:

```text
https://developer.android.com/topic/architecture
```

Links from the page are supporting navigation, not part of this import.

Do not extract content from linked pages merely to make an item more complete.

### 3. Repository usage and licensing

Use:

```yaml
repository_usage: citation-only
```

Do not create a `raw/` directory.

Do not store:

- an HTML snapshot;
- a PDF export;
- screenshots;
- diagrams;
- images;
- copied code samples;
- downloaded assets;
- a full-text transcription of the publication.

The source metadata must identify Google / Android Developers and the official URL.

The implementation may contain short attributed source-derived statements where allowed by the project's source model, but it must avoid reproducing substantial contiguous portions of the publication.

Legal permission remains a human-review responsibility. Do not change the repository's general licensing policy in this task.

### 4. Faithful extraction, not broad summarization

An item must preserve one actionable architectural principle, responsibility, constraint, or stated benefit from the publication.

A good item is:

- traceable to one source location;
- understandable without copying a full paragraph;
- narrow enough to review;
- faithful to the source's intended meaning;
- still visibly source-level rather than a normalized platform competency.

Do not combine unrelated statements solely to reduce item count.

Do not split one atomic statement into artificial fragments solely to increase item count.

When source wording cannot be retained safely or cleanly, use a concise faithful transcription and record the transformation in `transcription_notes`.

Do not use `transcription_notes` to add interpretation, teaching commentary, or normalization decisions.

### 5. Preserve the source hierarchy

Use `context` to preserve the publication's heading hierarchy.

Recommended form:

```yaml
context:
  - Common architectural principles
  - Separation of concerns
```

or:

```yaml
context:
  - Recommended app architecture
  - Data layer
```

Rules:

- use exact or faithfully transcribed heading labels;
- order labels from broadest to most specific;
- do not invent a normalized taxonomy;
- do not include the publication title in every context array;
- do not include duplicate labels;
- use an empty context only when the source genuinely provides no useful hierarchy.

### 6. Locators must remain useful when the page changes

Prefer:

```yaml
locator:
  type: heading
  value: Separation of concerns
```

Use `details` when multiple items share one heading or when a precise sub-location is useful:

```yaml
locator:
  type: heading
  value: General best practices
  details: Don't store data in app components.
```

Rules:

- locator values must identify visible source structure;
- do not use fragile paragraph numbers;
- do not use DOM selectors or generated element IDs;
- do not use line numbers from downloaded HTML;
- do not use only a URL as an item locator;
- repeated headings must be disambiguated using `details` or context;
- every item must be manually traceable on the live page.

### 7. Stable item identifiers

Item IDs must:

- use lowercase kebab-case;
- describe the source statement;
- remain stable across formatting changes;
- not encode array order;
- not encode the retrieval date;
- not encode a platform-normalized competency;
- be unique within the source package.

Examples of acceptable identifier style:

```text
separate-concerns
keep-state-out-of-app-components
drive-ui-from-data-models
assign-single-source-of-truth
use-ui-and-data-layers
add-domain-layer-when-needed
centralize-data-changes-in-repositories
limit-data-source-responsibility
reduce-android-framework-dependencies
define-module-responsibility-boundaries
expose-minimal-module-api
make-types-main-safe
persist-relevant-fresh-data
```

These examples are guidance, not a mandatory final inventory. IDs must match the actual extracted statements.

### 8. Source version

Use:

```yaml
source_version: 1
```

in both package files.

The source's own page update date belongs in provenance, not in `source_version`.

If the page exposes a visible “Last updated” date during implementation, preserve it as:

```yaml
provenance:
  version_label: "Last updated YYYY-MM-DD UTC"
```

Do not put a future or guessed date into metadata.

Set `retrieved_on` to the actual UTC calendar date on which Codex inspects the source.

### 9. Extraction status

Use:

```yaml
status: review
```

The first real package requires human review before it may become `approved`.

Do not mark the package `approved` in this task.

### 10. No schema expansion by default

The existing schemas are expected to be sufficient.

Do not change either competency schema unless implementation reveals a concrete blocker that prevents faithful representation of this source.

A preference, convenience improvement, or desire for extra metadata is not a blocker.

If a genuine blocker exists:

1. stop before changing the schema;
2. report the blocker;
3. explain the smallest possible schema change;
4. leave Task 005 incomplete for architecture review.

Do not silently expand the model.

## Scope

### 1. Create the source package

Create:

```text
competencies/sources/android-developers-app-architecture/
├── source.yaml
└── items.yaml
```

Do not create `raw/`.

Remove `competencies/sources/.gitkeep` if the directory is no longer empty and the file has no remaining purpose.

### 2. Create `source.yaml`

The file must validate against:

```text
schemas/competency-source.schema.json
```

Use the following intended shape:

```yaml
id: android-developers-app-architecture
title: Guide to app architecture
source_type: other
language: en
source_version: 1
status: review
repository_usage: citation-only

provenance:
  citation: Android Developers, Guide to app architecture
  publisher: Google
  url: https://developer.android.com/topic/architecture
  retrieved_on: YYYY-MM-DD
  version_label: Last updated YYYY-MM-DD UTC
  notes: >
    This package represents only the Guide to app architecture publication,
    not the complete Android Developers app architecture documentation set.

scope:
  roles:
    - Android developer
  declared_levels: []
  platforms:
    - Android
  technologies:
    - Android
```

This example defines intent, not byte-for-byte required formatting.

Requirements:

- use only schema-supported fields;
- use the actual retrieval date;
- use the page's visible update label when available;
- keep notes factual;
- do not add artifacts;
- do not invent declared levels;
- do not claim the package covers linked sub-guides.

`source_type: other` is acceptable because the publication is guidance documentation rather than a formal curriculum, standard, roadmap, assessment framework, or competency matrix.

Do not change the enum merely to add `documentation`.

### 3. Create `items.yaml`

The file must validate against:

```text
schemas/competency-items.schema.json
```

Root:

```yaml
source_id: android-developers-app-architecture
source_version: 1
items:
```

#### Expected coverage

Extract a coherent reference set from the entire publication.

The extraction should normally contain approximately **20–35 items**.

This is a quality range, not a target to game:

- fewer than 20 requires an explanation that the publication changed or contains fewer distinct source statements;
- more than 35 requires justification that items are not over-split;
- do not add filler to reach a number;
- do not omit major sections merely to stay under a number.

At minimum, inspect and represent applicable statements from:

```text
App composition
Common architectural principles
Recommended app architecture
General best practices
Benefits of architecture
```

Where the live page contains meaningful subsections, preserve them through locators and context.

#### Coverage expectations

The extraction should represent, where present on the live page:

- lifecycle and process constraints affecting architecture;
- component independence and state-storage constraints;
- separation of concerns;
- configuration changes and adaptive design;
- data-model-driven UI;
- persistent models;
- single source of truth;
- unidirectional data flow;
- minimum UI and data layers;
- conditions for an optional domain layer;
- modern architecture techniques;
- UI element and state-holder responsibilities;
- repository responsibilities;
- data-source responsibility boundaries;
- app-component and Android-framework dependency boundaries;
- module responsibility boundaries;
- minimal public APIs;
- reuse of platform/recommended libraries;
- preservation of UI state;
- reusable and composable UI;
- isolated testability;
- concurrency ownership and main safety;
- offline-oriented persistence;
- major stated engineering benefits.

Only include concepts actually present in the live publication.

#### Item example

```yaml
- id: separate-concerns
  statement: >
    Structure the app into units with clearly defined responsibilities and
    boundaries rather than concentrating unrelated work in UI entry points.
  locator:
    type: heading
    value: Separation of concerns
  context:
    - Common architectural principles
    - Separation of concerns
  transcription_notes: >
    Faithful concise transcription of the source guidance; terminology was
    shortened without assigning a normalized competency.
```

The example is illustrative. Codex must inspect the live publication and independently verify every item.

#### Statement rules

Each statement must:

- be written in English because the source language is English;
- express one source-derived requirement, responsibility, constraint, technique, or benefit;
- remain source-specific;
- avoid unsupported strength words such as `must` when the source presents guidance rather than a strict requirement;
- preserve conditional language such as optionality;
- preserve distinctions between UI, data, domain, repository, data-source, module, and app-component responsibilities;
- not introduce Clean Architecture terminology absent from the source;
- not introduce project-specific technologies or opinions;
- not cite linked pages as evidence.

#### `declared_level`

Do not add `declared_level` unless the live source explicitly assigns a level to that statement.

The expected result is that items omit this field.

#### `transcription_notes`

Use this field only where useful.

It should explain extraction mechanics such as:

- one long paragraph was condensed;
- one bullet was converted into an imperative statement;
- two adjacent clauses were kept together because they form one atomic source rule;
- source-specific wording was shortened while preserving meaning.

Do not mechanically add the same note to every item.

### 4. Add import documentation

Create:

```text
docs/COMPETENCY_IMPORT_WORKFLOW.md
```

The document must explain the reusable workflow demonstrated by this package.

Required sections:

1. **Purpose**
   - importing source material before normalization.

2. **Source boundary**
   - one coherent publication or independently maintained documentation section per package;
   - linked pages are not automatically included.

3. **Pre-import checks**
   - public accessibility;
   - provenance;
   - repository usage;
   - confidentiality and personal-data review;
   - licensing remains a human responsibility.

4. **Extraction workflow**
   - inspect source;
   - identify hierarchy;
   - identify atomic statements;
   - assign stable IDs;
   - add locators;
   - record transcription caveats;
   - validate;
   - request review.

5. **Good extraction**
   - faithful;
   - traceable;
   - source-level;
   - neither over-split nor over-merged.

6. **Bad extraction**
   - normalization during import;
   - copying an entire publication;
   - combining linked publications;
   - inventing difficulty;
   - adding prerequisites;
   - using fragile locators;
   - turning recommendations into absolute requirements.

7. **Versioning and updates**
   - retrieval date;
   - source version;
   - page update labels;
   - when to increment source version;
   - preserving stable item IDs;
   - never silently reusing removed IDs.

8. **Review checklist**
   - schema validity;
   - semantic validity;
   - provenance;
   - source boundary;
   - coverage;
   - wording fidelity;
   - locator traceability;
   - no normalization leakage;
   - public-repository safety.

Use the Android Developers package as the concrete example, but keep the document reusable for future imports.

### 5. Add an extraction review record

Create:

```text
competencies/reports/android-developers-app-architecture-import-review.md
```

This is a human-facing import report, not a normalized competency report.

Required content:

- source package ID;
- source title and URL;
- retrieval date;
- visible source update label, if present;
- package status;
- item count;
- sections inspected;
- sections intentionally excluded;
- linked pages intentionally excluded;
- extraction approach;
- notable transcription decisions;
- known ambiguities;
- licensing/repository-usage declaration;
- confirmation that no source artifact was stored;
- confirmation that no normalization or prerequisite design was performed.

The report must not duplicate every item from `items.yaml`.

### 6. Update repository documentation

Update `README.md` minimally:

- mention the first real competency source package;
- link to `docs/COMPETENCY_IMPORT_WORKFLOW.md`;
- include the competency validation command if not already present;
- do not turn the README into a detailed architecture document.

Update `docs/PROJECT_STATE.md`:

- keep the current phase as:

```text
Phase 2 — Competency import
```

- record that the first source package is implemented and awaiting review;
- state that normalization has not started;
- do not claim Phase 2 is complete;
- do not mark Task 005 complete inside project state before review.

Update `docs/ROADMAP.md` only if its wording incorrectly assumes that all Android Developers documentation is one source package. Make no unrelated roadmap changes.

### 7. Task status

Create or update:

```text
tasks/005-import-android-app-architecture.md
```

with this task specification.

Keep:

```text
Status: READY
```

during implementation.

Codex must not mark the task `DONE`.

The reviewer changes the status only after approval.

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
git status --short
```

Also perform the following review checks:

1. Parse both new YAML files directly.
2. Validate them directly against the Draft 2020-12 schemas.
3. Confirm that the package contains no `raw/` directory.
4. Confirm that all item IDs are unique.
5. Confirm that all item locators point to visible source headings or clearly identifiable statements.
6. Confirm that `source.yaml` and `items.yaml` use the same source ID and source version.
7. Confirm that no item contains normalized competency IDs, prerequisite IDs, topic IDs, difficulty, mastery, or progress fields.
8. Confirm that no linked publication was imported.
9. Confirm that the package is reported by `validate_competencies.py`.
10. Confirm there are no Python cache files.

## Acceptance criteria

Task 005 is acceptable when:

- `competencies/sources/android-developers-app-architecture/` exists;
- it contains exactly `source.yaml` and `items.yaml`;
- no source artifact or `raw/` directory is committed;
- both YAML files validate against their schemas;
- repository semantic validation passes;
- source ID and version match across both files;
- provenance identifies the official Android Developers publication;
- retrieval date is accurate;
- the visible source update label is preserved when available;
- repository usage is `citation-only`;
- package status is `review`;
- the import covers all major sections of the publication without importing linked pages;
- items are source-level, traceable, faithful, and reasonably atomic;
- context follows the publication hierarchy;
- locators are durable and reviewable;
- item IDs are stable and semantic;
- no normalization decisions are present;
- no prerequisite or learning graph is present;
- the reusable import workflow is documented;
- the import review report is present;
- README and project state are synchronized;
- all validators and tests pass;
- Task 005 remains `READY`;
- no commit is created.

## Explicitly out of scope

Do not add:

- another Android Developers source package;
- content from architecture recommendations;
- content from UI layer, data layer, or domain layer sub-guides;
- normalized competencies;
- duplicate detection;
- cross-source mapping;
- prerequisite relationships;
- learning sequences;
- educational topics;
- Android application code;
- backend code;
- database schemas;
- learner profiles or progress;
- CI configuration;
- new third-party dependencies;
- web scraping infrastructure;
- automatic internet fetching inside repository validators;
- cached source HTML;
- screenshots or diagrams;
- schema changes without an approved blocker;
- commits.

## Implementation report

After implementation, report:

1. exact files added, modified, and removed;
2. the source page retrieval date;
3. the visible source update label used;
4. total extracted item count;
5. source sections represented;
6. intentionally excluded material;
7. any transcription decisions or ambiguities;
8. whether schemas changed;
9. validation command results;
10. `git status --short`;
11. confirmation that Task 005 remains `READY`;
12. confirmation that no commit was created.

Do not claim approval. Approval belongs to the reviewer.
