# Task 004 — Define the competency source model

- Status: DONE
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Define the first stable, machine-readable model for recording source competency materials before they are normalized into the platform's approved competency registry and learning graph.

The task must establish:

- the repository structure for competency sources;
- a schema for source metadata;
- a schema for extracted source items;
- stable source and item identifiers;
- provenance and public-repository safety rules;
- templates and validation fixtures;
- repository-local validation;
- author documentation;
- an architecture decision record.

This task must not import a real competency matrix, create normalized competencies, define prerequisite relationships, or create educational topics.

## Context

The repository already defines and validates mature educational topic packages under `content/`.

The project is now in **Phase 2 — Competency import**. The next stage begins with external or owner-provided materials such as:

- competency matrices;
- role expectations;
- curricula;
- assessment frameworks;
- job descriptions;
- public roadmaps;
- structured personal study requirements.

These materials are not yet the platform's canonical competencies.

A source may contain:

- duplicate statements;
- overlapping requirements;
- inconsistent terminology;
- mixed abstraction levels;
- source-specific grade names;
- ambiguous wording;
- requirements that later map to multiple topics;
- multiple statements that later map to one normalized competency.

Therefore, the repository must preserve source meaning and provenance before interpretation.

The model created by this task represents **what a source says**, not the platform's final judgment about:

- canonical competency identity;
- competency equivalence;
- prerequisite relationships;
- topic mapping;
- learning order;
- learner mastery.

The following separation is mandatory:

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
- `docs/ROADMAP.md`
- `docs/AI_COLLABORATION.md`
- `docs/decisions/0001-content-and-progress-storage.md`
- `docs/decisions/0002-yaml-content-model-and-json-schema.md`
- `docs/decisions/0003-repository-content-validator.md`
- `tasks/001-content-model.md`
- `tasks/002-content-validator.md`
- `tasks/003-project-state-synchronization.md`
- `templates/TASK_TEMPLATE.md`

## Approved design constraints

### 1. Source records are not canonical competencies

A source item records a requirement or statement from one source.

It must not contain fields that claim normalized platform meaning, including:

- canonical competency IDs;
- prerequisite IDs;
- related competency IDs;
- topic IDs;
- learning sequence positions;
- mastery criteria;
- personal progress;
- duplicate-resolution decisions;
- merge decisions.

Those belong to later tasks.

### 2. Preserve provenance

Every source package must identify where the material came from.

Every extracted item must identify where it appeared inside that source.

A future reviewer must be able to answer:

- Which source contained this statement?
- Which source version was used?
- Where in the source did it appear?
- Was the statement transcribed faithfully?
- Is the material safe to store in this public repository?

### 3. Preserve source wording

The required `statement` field represents the source statement itself.

It should be:

- verbatim when legally and practically appropriate; or
- a faithful transcription when formatting conversion is necessary.

Do not normalize terminology, merge multiple requirements, or rewrite the statement into a platform competency.

Any unavoidable transcription issue must be recorded separately in `transcription_notes`.

### 4. Stable identifiers

Source IDs must:

- be globally unique within the repository;
- use lowercase kebab-case;
- remain stable after creation;
- describe the source rather than its filesystem location.

Examples:

```text
android-developer-competency-matrix-2026
google-associate-android-developer-guide
personal-android-gap-analysis-2026
```

Source item IDs must:

- be unique within one source;
- use lowercase kebab-case;
- remain stable after review;
- not encode array indexes that may change;
- not be reused after removal.

Examples:

```text
activity-lifecycle
explicit-and-implicit-intents
structured-concurrency-basics
```

The stable cross-source reference form is:

```text
<source-id>:<item-id>
```

Example:

```text
android-developer-competency-matrix-2026:activity-lifecycle
```

This reference form is documented for future normalization work but is not yet used to create normalized competencies.

### 5. Source versioning

Every source package must have an integer `source_version`.

Rules:

- initial value is `1`;
- increment when the represented source material changes;
- increment when extracted item meaning changes because the source was updated;
- formatting-only repository edits do not require an increment;
- `source.yaml` and `items.yaml` must contain the same source version.

Source versioning is independent from educational `content_version`.

### 6. Public-repository safety

The repository is public.

Do not commit:

- confidential employer competency matrices;
- proprietary internal documents without permission;
- personal data;
- secrets;
- access-controlled source exports;
- copyrighted full-text material when repository storage is not permitted.

Each source metadata file must declare a `repository_usage` value:

```text
public
owned
permission-granted
citation-only
```

Meaning:

- `public` — publicly accessible material that may be represented in the repository under applicable terms;
- `owned` — material created and owned by the repository owner;
- `permission-granted` — storage or transcription permission has been obtained;
- `citation-only` — only metadata, locators, short permitted excerpts, or owner-authored summaries may be committed; the original source artifact must not be stored.

The schema validates the declared value, but legal permission remains a human responsibility.

### 7. Source-specific terminology is preserved

A source may use grade or role labels such as:

```text
intern
junior
junior+
middle
level-1
associate
```

The model must preserve such labels without forcing them into the educational topic difficulty enum.

Therefore, source-declared levels are non-empty strings rather than the controlled topic difficulty values.

### 8. YAML and JSON Schema

Use:

- YAML for source metadata and extracted source items;
- JSON Schema Draft 2020-12 for structural validation;
- Markdown for human-facing documentation.

Reuse schema definitions where doing so improves consistency without coupling competency schemas to client or database models.

## Scope

### 1. Create the competency source directory structure

Create:

```text
competencies/
├── sources/
├── normalized/
└── reports/
```

Use `.gitkeep` only where an otherwise empty directory must be tracked.

For Task 004:

- `competencies/sources/` is the future location of real source packages;
- `competencies/normalized/` is reserved for later normalized competency work;
- `competencies/reports/` is reserved for later duplicate, conflict, and graph reports.

Do not add real competency data.

A future real source package will use:

```text
competencies/sources/<source-id>/
├── source.yaml
├── items.yaml
└── raw/
```

The `raw/` directory is optional.

Do not create `raw/` in templates or fixtures unless it contains an intentional small text fixture. Do not add binary source documents in this task.

### 2. Create `schemas/competency-source.schema.json`

The schema must validate `source.yaml`.

Use JSON Schema Draft 2020-12.

Required root fields:

```yaml
id:
title:
source_type:
language:
source_version:
status:
repository_usage:
provenance:
```

Set `additionalProperties: false` for controlled objects.

#### `id`

- non-empty string;
- lowercase kebab-case;
- globally unique by repository policy.

#### `title`

- non-empty human-readable string.

#### `source_type`

Controlled enum:

```text
competency-matrix
curriculum
assessment-framework
role-expectations
job-description
roadmap
personal-analysis
standard
other
```

#### `language`

- non-empty BCP 47-style language tag;
- support values such as `en`, `ru`, `zh-CN`;
- use a practical schema pattern rather than attempting exhaustive language-tag validation.

#### `source_version`

- positive integer;
- minimum `1`.

#### `status`

Controlled enum:

```text
draft
review
approved
deprecated
```

This is the status of the repository's source extraction, not the publication status of educational content.

#### `repository_usage`

Controlled enum:

```text
public
owned
permission-granted
citation-only
```

#### `provenance`

Required object containing:

```yaml
citation:
```

Optional fields:

```yaml
publisher:
url:
published_on:
retrieved_on:
version_label:
notes:
```

Rules:

- `citation` is a concise, non-empty human-readable identification of the source;
- `url`, when present, must be an absolute `http` or `https` URI;
- date fields, when present, use `YYYY-MM-DD`;
- `version_label` preserves a source's own version name and is independent from `source_version`;
- `additionalProperties: false`.

#### Optional `scope`

The schema may support:

```yaml
scope:
  roles:
  declared_levels:
  platforms:
  technologies:
```

Each field:

- is an array of unique, non-empty strings;
- preserves source terminology;
- may be empty only if there is a clear reason documented in the schema description.

`scope` must not create normalized taxonomy.

#### Optional `artifacts`

The schema may support an array of objects describing source artifacts that are legally safe to store.

Each artifact object contains:

```yaml
path:
media_type:
sha256:
```

Optional:

```yaml
description:
```

Rules:

- `path` is repository-relative and must point inside the same source package's `raw/` directory;
- `media_type` is a non-empty MIME type string;
- `sha256` is exactly 64 lowercase hexadecimal characters;
- paths must be unique within the array;
- `additionalProperties: false`.

Repository-wide path existence and package-boundary checks belong to semantic validation.

When `repository_usage` is `citation-only`, committed artifacts must be rejected by semantic validation.

### 3. Create `schemas/competency-items.schema.json`

The schema must validate `items.yaml`.

Required root fields:

```yaml
source_id:
source_version:
items:
```

Rules:

- `source_id` uses the same source-ID pattern;
- `source_version` is a positive integer;
- `items` is a non-empty array;
- root object uses `additionalProperties: false`.

Every item must contain:

```yaml
id:
statement:
locator:
```

Optional item fields:

```yaml
context:
declared_level:
transcription_notes:
```

#### Item `id`

- lowercase kebab-case;
- unique within `items`;
- stable after review.

JSON Schema should reject duplicate item IDs if expressible cleanly. Otherwise, repository validation must enforce uniqueness.

#### `statement`

- non-empty string;
- represents the original requirement or a faithful transcription;
- must not contain normalized competency decisions.

#### `locator`

Required object containing:

```yaml
type:
value:
```

Allowed `type` values:

```text
page
section
heading
row
cell
item
timestamp
other
```

Rules:

- `value` is a non-empty human-readable location such as `Junior sheet, row 17`;
- optional `details` may provide additional non-empty locator information;
- `additionalProperties: false`.

#### `context`

Optional array of unique, non-empty strings preserving source hierarchy.

Example:

```yaml
context:
  - Android platform
  - Application components
  - Activity
```

#### `declared_level`

- optional non-empty string;
- preserves the level written by the source;
- must not be validated against topic difficulty enums.

#### `transcription_notes`

- optional non-empty string;
- records formatting loss, ambiguity, OCR uncertainty, translation handling, or other extraction caveats;
- must not contain normalization decisions.

### 4. Create templates

Create:

```text
templates/competency-source/
├── source.yaml
└── items.yaml
```

Requirements:

- templates must be syntactically valid;
- templates must pass their schemas;
- placeholder identifiers must satisfy ID patterns;
- templates use `status: draft`;
- templates use `repository_usage: owned`;
- templates contain no real competency source material;
- template comments or placeholder text must make replacement requirements obvious;
- the template demonstrates at least two source items with distinct locator types;
- do not add normalized competency IDs, prerequisites, or topic mappings.

### 5. Create schema fixtures

Create:

```text
schemas/fixtures/competencies/valid/source.yaml
schemas/fixtures/competencies/valid/items.yaml
schemas/fixtures/competencies/invalid/source-invalid-usage.yaml
schemas/fixtures/competencies/invalid/items-duplicate-id.yaml
schemas/fixtures/competencies/invalid/items-missing-locator.yaml
```

Requirements:

- valid fixtures pass their corresponding schemas and semantic checks;
- every invalid fixture fails for the reason indicated by its filename;
- fixtures contain invented, minimal source material;
- fixtures do not appear under `competencies/sources/`;
- invalid duplicate IDs must be detected either by JSON Schema or semantic validation.

Do not modify the meaning of existing topic/test fixtures.

### 6. Add repository-local competency validation

Create:

```text
scripts/validate_competencies.py
```

Use Python 3.12.

Allowed dependencies:

- Python standard library;
- existing repository dependencies already used for YAML and JSON Schema validation.

Do not add a new dependency.

The validator must:

1. discover source packages under:

   ```text
   competencies/sources/<source-id>/
   ```

2. ignore `.gitkeep` and unrelated reserved empty directories;

3. require both:

   ```text
   source.yaml
   items.yaml
   ```

4. load YAML safely;

5. validate files against the competency schemas;

6. perform repository-wide semantic validation;

7. validate competency templates and fixtures;

8. emit deterministic diagnostics;

9. support CLI execution from the repository root.

Required semantic rules:

- package directory name equals `source.yaml:id`;
- `items.yaml:source_id` equals `source.yaml:id`;
- source versions match;
- source IDs are globally unique;
- item IDs are unique within a source;
- every declared artifact path:
  - is repository-relative;
  - stays inside the current package's `raw/` directory;
  - exists;
  - is a regular file;
  - has the declared SHA-256 digest;
- `repository_usage: citation-only` rejects committed artifacts;
- no undeclared regular files exist inside `raw/`;
- template files validate;
- valid fixtures pass;
- each invalid fixture fails for its intended reason.

The validator must not:

- normalize statements;
- infer duplicates across sources;
- generate canonical competencies;
- create prerequisite links;
- map source items to topic IDs;
- modify repository files.

#### CLI and exit codes

Use:

```bash
python -B scripts/validate_competencies.py
```

Exit codes:

- `0` — all competency sources, templates, and fixtures are valid;
- `1` — validation failure;
- `2` — configuration or internal error.

Successful output must include deterministic counts for:

- discovered source packages;
- competency templates;
- competency schema fixtures.

Diagnostics must identify:

- file path;
- relevant field or item when possible;
- concise reason.

Do not print Python tracebacks for expected validation failures.

### 7. Add tests

Add unittest coverage for the new validator.

Tests must cover at least:

- valid source package;
- missing `source.yaml`;
- missing `items.yaml`;
- source/package ID mismatch;
- source ID mismatch between files;
- source version mismatch;
- duplicate item IDs;
- missing item locator;
- invalid repository usage;
- artifact path escaping the package;
- missing artifact;
- SHA-256 mismatch;
- undeclared file under `raw/`;
- artifacts forbidden for `citation-only`;
- deterministic diagnostics;
- exit code `0`;
- exit code `1`;
- exit code `2` for invalid validator configuration.

Use temporary directories and invented test material.

Do not require network access.

### 8. Create `docs/COMPETENCY_SOURCE_MODEL.md`

Document:

- why source items are separate from canonical competencies;
- the source package structure;
- field meanings;
- stable ID rules;
- cross-source reference syntax;
- source versioning;
- provenance requirements;
- source wording and transcription rules;
- public-repository safety;
- source-declared levels versus platform difficulty;
- optional raw artifacts and checksum behavior;
- what JSON Schema validates;
- what semantic validation validates;
- what remains deferred to normalization;
- author workflow for adding a future source.

Include a concise workflow:

1. verify that the source is safe to represent publicly;
2. create a package from the template;
3. record provenance;
4. extract items without normalization;
5. add precise locators;
6. add allowed raw artifacts only when appropriate;
7. run competency validation;
8. submit for review;
9. do not mark the source `approved` until human review.

### 9. Record the architecture decision

Create:

```text
docs/decisions/0004-source-competencies-before-normalization.md
```

The ADR must record:

- why source items and canonical competencies are separate;
- why source wording and provenance are preserved;
- why identifiers are stable;
- why source-declared levels are not normalized yet;
- why raw artifacts are optional;
- why public-repository usage must be explicit;
- why canonical competency relationships are deferred;
- consequences and known limitations.

Use the repository's existing ADR style.

### 10. Update existing documentation

Make focused updates only.

#### `README.md`

Add:

- `docs/COMPETENCY_SOURCE_MODEL.md` to the `Start here` sequence;
- the competency validation command:

  ```bash
  python -B scripts/validate_competencies.py
  ```

Keep existing content validation guidance intact.

#### `docs/PROJECT_STATE.md`

Update completed capabilities only after implementation is complete enough to justify them.

Add the competency source model and validator as current capabilities.

Keep the current phase as:

```text
Phase 2 — Competency import
```

Do not mark Task 004 as completed until review.

Update current focus only where necessary to state that the next operational step is importing the first approved source.

#### `docs/ROADMAP.md`

Do not mark Phase 2 complete.

Make only a focused wording update if needed to reflect that the source model and validation infrastructure now exist.

Do not turn the roadmap into a task tracker.

#### `docs/CONTENT_VALIDATION.md`

Do not merge competency validation into content validation.

A focused cross-reference to `docs/COMPETENCY_SOURCE_MODEL.md` is allowed only if it improves discoverability.

### 11. Task status

Task 004 begins as:

```text
Status: READY
```

Codex may change it to:

```text
Status: IN_PROGRESS
```

during implementation.

It must not be changed to `DONE` before human and ChatGPT review.

## Acceptance criteria

- [ ] `competencies/sources/`, `competencies/normalized/`, and `competencies/reports/` exist.
- [ ] Empty reserved directories are tracked without adding real competency data.
- [ ] `schemas/competency-source.schema.json` exists and uses JSON Schema Draft 2020-12.
- [ ] `schemas/competency-items.schema.json` exists and uses JSON Schema Draft 2020-12.
- [ ] Required source metadata fields are validated.
- [ ] Required source item fields are validated.
- [ ] Controlled enums are documented and enforced.
- [ ] Source-declared levels remain source strings rather than topic difficulty enums.
- [ ] Stable source IDs and source-local item IDs are documented.
- [ ] Cross-source reference syntax is documented.
- [ ] Source version consistency is enforced.
- [ ] Provenance is required.
- [ ] Public-repository usage is explicitly declared.
- [ ] Citation-only sources cannot contain committed raw artifacts.
- [ ] Optional artifacts are constrained to the package's `raw/` directory.
- [ ] Artifact existence and SHA-256 values are checked.
- [ ] Undeclared files under `raw/` are rejected.
- [ ] Competency source templates exist and validate.
- [ ] Valid and invalid fixtures exist.
- [ ] Every invalid fixture fails for its intended reason.
- [ ] `scripts/validate_competencies.py` exists.
- [ ] Competency source packages are discovered and validated deterministically.
- [ ] Expected validation failures do not print tracebacks.
- [ ] Validator exit codes `0`, `1`, and `2` are tested.
- [ ] Unit tests cover the required semantic rules.
- [ ] `docs/COMPETENCY_SOURCE_MODEL.md` exists and explains the complete author workflow.
- [ ] ADR 0004 records the approved architecture decision.
- [ ] README links to the new documentation and command.
- [ ] Existing content schemas, topic templates, content fixtures, and content semantics remain unchanged.
- [ ] No real competency source is imported.
- [ ] No normalized competency registry is created.
- [ ] No prerequisite graph or learning sequence is created.
- [ ] No application, backend, database, CI, or learner-progress code is added.
- [ ] The final report lists all changed files, commands, results, assumptions, and unresolved issues.

## Forbidden changes

- importing a real competency matrix or job description;
- storing confidential, proprietary, personal, or access-controlled source material;
- creating canonical or normalized competency records;
- creating duplicate-resolution or conflict reports;
- adding prerequisite or related-competency relationships;
- mapping source items to educational topic IDs;
- creating learning sequences;
- creating educational topic packages;
- changing `topic.yaml` or `test.yaml` schemas;
- changing existing topic/test content semantics;
- merging competency files into `content/`;
- storing learner progress or personal mastery;
- adding a database schema;
- adding web, Android, backend, or shared application code;
- adding CI;
- adding dependencies;
- using network access in validation or tests;
- introducing executable code evaluation;
- broad rewrites of foundation documentation;
- marking Phase 2 complete;
- changing Task 004 to `DONE` before review.

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
git status --short
```

Also verify manually:

- all paths referenced by the new documentation exist;
- no real source material was added;
- no confidential or proprietary material was added;
- no normalized competency files exist;
- no prerequisite graph exists;
- no topic mapping exists;
- Phase 2 remains current and incomplete;
- Task 004 is not marked `DONE`;
- existing content validation still passes unchanged.

## Deliverables

1. `tasks/004-competency-source-model.md`
2. competency source directory structure
3. `schemas/competency-source.schema.json`
4. `schemas/competency-items.schema.json`
5. competency source templates
6. competency schema fixtures
7. `scripts/validate_competencies.py`
8. validator unit tests
9. `docs/COMPETENCY_SOURCE_MODEL.md`
10. `docs/decisions/0004-source-competencies-before-normalization.md`
11. focused updates to existing documentation
12. Codex final report containing:
    - implementation summary;
    - changed files;
    - validation commands and results;
    - assumptions;
    - unresolved issues;
    - explicit confirmation that no real competency source, normalized competency, graph, topic mapping, product code, database, CI configuration, dependency, confidential material, or learner-progress logic was added.
