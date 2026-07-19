# Task 001 — Define the educational content model

- Status: DONE
- Owner: Human
- Implementer: Codex
- Reviewer: Human + ChatGPT

## Goal

Define the first stable, machine-readable content model for educational topics and tests.

The task must establish:

- the canonical topic package structure;
- a schema for `topic.yaml`;
- a schema for `test.yaml`;
- reusable templates;
- one small validation fixture;
- documentation describing how content authors should use the model.

This task must not add real educational material or application code.

---

## Context

The repository stores shared educational content in Git.

Personal learning progress is stored separately and must not appear in topic metadata or test files.

A mature topic package is expected to use this structure:

```text
content/<track>/<section>/<topic>/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

The content model must remain independent from:

- the web client;
- the Android client;
- backend implementation;
- database entities;
- filesystem-specific UI assumptions.

Stable identifiers must be used so that future progress records can reference topics and questions without depending on file paths.

---

## Required reading

Before making changes, read:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_VISION.md`
- `docs/PROJECT_PRINCIPLES.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTENT_STRATEGY.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/AI_COLLABORATION.md`
- `docs/ROADMAP.md`
- `docs/decisions/0001-content-and-progress-storage.md`
- `templates/TASK_TEMPLATE.md`

---

## Approved design constraints

### 1. Source formats

Use:

- YAML for author-facing topic and test metadata;
- JSON Schema Draft 2020-12 for validation;
- Markdown for human-readable educational content.

Do not introduce a database schema in this task.

### 2. Stable identifiers

Topic IDs must:

- be globally unique;
- use lowercase kebab-case;
- remain stable after creation;
- not depend on the directory path;
- describe the concept rather than a UI screen.

Examples:

```text
java-object-equality
java-hashmap
kotlin-coroutine-context
android-activity-lifecycle
```

Question IDs must:

- be unique within the topic;
- use lowercase kebab-case;
- remain stable after publication.

Examples:

```text
hash-collision-definition
equals-hashcode-contract
predict-map-output
```

### 3. Shared content versus personal state

Do not include personal progress fields such as:

- completion status;
- score;
- attempt count;
- mastery;
- next review date;
- bookmarks;
- personal notes.

Shared content may contain only author-defined educational metadata.

### 4. Versioning

Each topic must have an integer `content_version`.

Rules:

- the initial value is `1`;
- increment it when published educational meaning changes;
- formatting-only edits do not require an increment;
- IDs must not be reused after removal.

Do not add semantic-version strings unless clearly required by an existing repository rule.

### 5. Extensibility

The schema should support future clients without attempting to model every possible feature now.

Prefer:

- explicit enums;
- required core fields;
- optional extension fields only when justified;
- `additionalProperties: false` for controlled objects.

Avoid speculative fields that have no current use.

---

## Scope

### 1. Create `schemas/topic.schema.json`

The schema must validate `topic.yaml`.

Required topic fields:

```yaml
id:
title:
track:
section:
difficulty:
status:
estimated_minutes:
content_version:
prerequisites:
learning_outcomes:
tags:
references:
```

Required semantics:

#### `id`

- string;
- lowercase kebab-case;
- globally unique by repository policy.

#### `title`

- non-empty human-readable string.

#### `track`

Use a controlled enum for the initial platform tracks:

```text
computer-science
java
kotlin
jvm
algorithms
concurrency
coroutines
networking
databases
architecture
testing
security
android
system-design
tools
```

Do not add `backend` as a separate initial track unless repository documentation already requires it. Backend concepts can initially belong to existing tracks such as `networking`, `databases`, `architecture`, or `system-design`.

#### `section`

- lowercase kebab-case;
- groups related topics inside a track;
- examples: `collections`, `object-model`, `lifecycle`, `structured-concurrency`.

#### `difficulty`

Enum:

```text
foundation
junior
middle
advanced
```

Difficulty is not personal mastery.

#### `status`

Enum:

```text
draft
review
published
deprecated
```

This is content publication status, not learner progress.

#### `estimated_minutes`

- positive integer;
- expected active study time;
- minimum `5`.

#### `content_version`

- positive integer;
- minimum `1`.

#### `prerequisites`

- array of stable topic IDs;
- unique values;
- may be empty;
- must not contain the topic's own ID.

The JSON Schema may validate shape but does not need to validate repository-wide existence or cycles.

#### `learning_outcomes`

- non-empty array;
- unique, non-empty strings;
- each item describes an observable learner outcome.

#### `tags`

- array of lowercase kebab-case strings;
- unique values;
- may be empty.

#### `references`

Array of reference objects.

Each reference object must contain:

```yaml
title:
url:
type:
```

Allowed `type` values:

```text
official-docs
specification
book
article
paper
video
course
repository
```

Optional reference fields:

```yaml
author:
accessed_on:
notes:
```

`accessed_on`, when present, must use `YYYY-MM-DD`.

### 2. Optional topic fields

The topic schema may support these optional fields:

```yaml
summary:
android_connections:
jvm_connections:
related_topics:
```

Rules:

- `summary` is a concise non-empty string;
- connection fields are arrays of non-empty strings;
- `related_topics` is an array of stable topic IDs;
- arrays must use unique values.

Do not add more optional fields without explaining why in the final report.

### 3. Create `schemas/test.schema.json`

The schema must validate `test.yaml`.

Required root fields:

```yaml
topic_id:
content_version:
passing_score_percent:
questions:
```

Rules:

- `topic_id` uses the same stable topic-ID pattern;
- `content_version` is a positive integer;
- `passing_score_percent` is an integer from `1` to `100`;
- `questions` is a non-empty array.

### 4. Supported question types

Support exactly these initial types:

```text
single-choice
multiple-choice
true-false
free-text
code-analysis
```

Every question must contain:

```yaml
id:
type:
prompt:
difficulty:
points:
explanation:
```

Common rules:

- `id` uses lowercase kebab-case;
- `prompt` is non-empty;
- `difficulty` uses:
  - `foundation`
  - `junior`
  - `middle`
  - `advanced`
- `points` is a positive integer;
- `explanation` is a non-empty explanation shown after evaluation.

#### `single-choice`

Must contain:

```yaml
options:
correct_option_id:
```

Each option:

```yaml
id:
text:
```

Rules:

- at least two options;
- option IDs unique within the question;
- exactly one referenced correct option.

#### `multiple-choice`

Must contain:

```yaml
options:
correct_option_ids:
```

Rules:

- at least two options;
- at least one correct option;
- unique correct IDs;
- every referenced correct ID must exist.

Cross-field reference validation may require a later repository validator if JSON Schema cannot express it cleanly. Document any such limitation.

#### `true-false`

Must contain:

```yaml
correct_answer:
```

where `correct_answer` is boolean.

#### `free-text`

Must contain:

```yaml
rubric:
```

`rubric` must be a non-empty array of rubric items.

Each rubric item:

```yaml
criterion:
points:
```

Optional:

```yaml
sample_answer:
```

#### `code-analysis`

Must contain:

```yaml
language:
code:
rubric:
```

Allowed initial languages:

```text
java
kotlin
xml
gradle-kotlin
bash
sql
```

Optional:

```yaml
sample_answer:
```

Do not support executable code tests in this task.

### 5. Create topic templates

Create:

```text
templates/topic/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

Requirements:

- templates must be syntactically valid;
- templates must demonstrate the intended structure;
- placeholder IDs must still satisfy schema patterns;
- templates must not pretend to be a real published lesson;
- use `status: draft`;
- content should be minimal and clearly marked for replacement.

### 6. Create validation fixtures

Create:

```text
schemas/fixtures/valid/topic.yaml
schemas/fixtures/valid/test.yaml
schemas/fixtures/invalid/topic-invalid-id.yaml
schemas/fixtures/invalid/test-missing-answer.yaml
```

The valid fixtures must pass their corresponding schemas.

The invalid fixtures must intentionally fail for the reason stated in the filename or a nearby comment/documentation.

Do not place fixtures under `content/`.

### 7. Create content model documentation

Create:

```text
docs/CONTENT_MODEL.md
```

It must explain:

- the canonical topic package;
- field meanings;
- stable-ID rules;
- content publication status versus learner progress;
- versioning rules;
- question types;
- references;
- what JSON Schema validates;
- what requires future repository-wide validation;
- a concise author workflow for adding a new topic.

### 8. Record the architecture decision

Create:

```text
docs/decisions/0002-yaml-content-model-and-json-schema.md
```

The ADR must record:

- why YAML is used for authoring;
- why JSON Schema is used for validation;
- why stable IDs are independent from file paths;
- why learner progress is excluded;
- consequences and known limitations.

### 9. Update existing documentation

Make only necessary focused updates:

- add `docs/CONTENT_MODEL.md` to the README start-here section;
- update Phase 1 in `docs/ROADMAP.md` only if required to reflect completed deliverables;
- do not mark Phase 1 complete;
- do not change Task 001 status to `DONE` until implementation and review are complete.

---

## Schema quality requirements

All JSON Schema files must:

- use JSON Schema Draft 2020-12;
- include `$schema`;
- include a stable local `$id`;
- include `title`;
- include `description`;
- define reusable structures under `$defs`;
- use `required` explicitly;
- use `additionalProperties: false` for controlled objects;
- avoid duplicated definitions where `$ref` is appropriate;
- remain readable and reasonably documented.

Use local schema IDs such as:

```text
https://android-library.local/schemas/topic.schema.json
https://android-library.local/schemas/test.schema.json
```

These are identifiers, not expected public URLs.

---

## Validation implementation

Use the smallest justified validation mechanism.

Preferred order:

1. use an already available JSON Schema validator;
2. use Python with the `jsonschema` and `PyYAML` packages only if those packages are already available;
3. otherwise create a small dependency-free structural validation script only if feasible;
4. if proper schema validation cannot run without adding dependencies, do not add dependencies silently.

A dependency proposal must be reported before being introduced.

If no validator is available, still:

- validate JSON syntax;
- validate YAML syntax using available tooling;
- document which schema checks could not be executed.

Do not initialize a package manager solely for this task.

---

## Acceptance criteria

- [ ] `schemas/topic.schema.json` exists and follows Draft 2020-12.
- [ ] `schemas/test.schema.json` exists and follows Draft 2020-12.
- [ ] Required topic fields are represented.
- [ ] Personal learner-progress fields are excluded.
- [ ] All five approved question types are represented.
- [ ] Question-type-specific structures are explicit.
- [ ] Stable topic and question ID patterns are documented and validated.
- [ ] Topic templates exist and are syntactically valid.
- [ ] Valid and invalid fixtures exist.
- [ ] `docs/CONTENT_MODEL.md` clearly documents the model.
- [ ] ADR 0002 exists.
- [ ] README references the content-model documentation.
- [ ] Existing architecture principles remain unchanged.
- [ ] No application code, backend code, database schema, CI workflow, or real educational lesson is added.
- [ ] JSON files parse successfully.
- [ ] YAML files parse successfully using available tooling.
- [ ] Valid fixtures pass schema validation when a validator is available.
- [ ] Invalid fixtures fail schema validation when a validator is available.
- [ ] `git diff --check` passes.
- [ ] The final report lists limitations that require a future repository-wide validator.

---

## Repository-wide checks intentionally deferred

This task does not need to implement validation for:

- globally unique topic IDs;
- globally unique question IDs outside their topic;
- prerequisite existence;
- prerequisite cycles;
- self-dependency across files;
- related-topic existence;
- duplicate content paths;
- references to removed IDs;
- consistency between `topic.yaml` and `test.yaml` versions;
- aggregate scoring rules;
- Markdown heading structure;
- internal Markdown links.

These belong to a later content-validator task.

---

## Forbidden changes

Do not:

- initialize Next.js, Android, Ktor, Supabase, or any database;
- add production application source code;
- add CI workflows;
- add real learning topics;
- import competency matrices;
- add learner progress fields;
- store answers or user attempts;
- create a custom YAML dialect;
- use filesystem paths as topic IDs;
- create more question types;
- add executable code runners;
- silently add dependencies;
- broadly rewrite existing foundation documents;
- redesign the repository structure.

---

## Validation

Run all applicable commands available in the repository.

At minimum:

```bash
git status --short
git diff --check
```

Validate JSON syntax, for example with an available tool or standard library.

Validate YAML syntax and schemas using existing tooling when available.

If Python dependencies are already installed, an acceptable ad hoc validation approach is:

```bash
python -c "import json; json.load(open('schemas/topic.schema.json', encoding='utf-8')); json.load(open('schemas/test.schema.json', encoding='utf-8')); print('JSON schemas parsed')"
```

Do not assume `python` is available under that exact command name on every system. Use the available interpreter.

---

## Deliverables

1. `schemas/topic.schema.json`
2. `schemas/test.schema.json`
3. topic package templates under `templates/topic/`
4. valid and invalid fixtures under `schemas/fixtures/`
5. `docs/CONTENT_MODEL.md`
6. `docs/decisions/0002-yaml-content-model-and-json-schema.md`
7. focused README and roadmap updates where required
8. Codex final report containing:
   - implementation summary;
   - complete changed-file list;
   - schema design decisions;
   - checks run and their results;
   - validation limitations;
   - assumptions;
   - unresolved issues;
   - explicit confirmation that no product code, database, CI workflow, or real lesson was added.
