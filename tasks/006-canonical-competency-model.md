# Task 006 — Canonical competency model

Status: DONE

## Goal

Introduce and implement the repository's canonical competency model.

Task 006 must convert the approved architecture in:

```text
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

into:

- versioned JSON Schemas;
- cross-reference validation;
- positive and negative fixtures;
- one pilot canonical competency package;
- documentation updates.

This task validates the model on real evidence from the source package imported in Task 005.

## Architectural authority

The implementation must follow:

```text
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

The task must not independently redesign the domain model.

If the existing repository structure conflicts with the architecture document, stop and report the conflict rather than silently changing the model.

## Preconditions

The repository already contains:

```text
competencies/sources/android-developers-app-architecture/
    source.yaml
    items.yaml
```

Task 005 is complete.

The working tree must be clean before implementation begins.

## Required additions

### 1. Architecture document

Add:

```text
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

Use the approved architecture document exactly, except for repository-relative formatting corrections that do not change meaning.

### 2. Schemas

Add schemas for:

```text
competency-set.yaml
competencies.yaml
```

Recommended names:

```text
schemas/canonical-competency-set.schema.json
schemas/canonical-competencies.schema.json
```

Schema names may follow established repository conventions, but the conceptual model must remain unchanged.

The schemas must support only the initial fields defined by the architecture document.

Do not add:

- prerequisites;
- relations;
- topics;
- tags;
- levels;
- difficulty;
- priority;
- mastery;
- progress;
- assessments;
- learning paths.

### 3. Pilot package

Create:

```text
competencies/normalized/android-app-architecture/
    competency-set.yaml
    competencies.yaml
```

The package must:

- use `status: review`;
- use `schema_version: 1`;
- use package version `1`;
- contain 8–12 canonical competencies;
- reference only real source items from Task 005;
- preserve the source package unchanged;
- demonstrate both simple and non-trivial normalization decisions.

The pilot should cover the architecture core where supported by imported evidence, such as:

- Android framework component constraints;
- separation of concerns;
- persistent data models;
- UI layer responsibility;
- data layer responsibility;
- repository responsibility;
- single source of truth;
- unidirectional data flow;
- optional domain layer;
- dependency injection.

This is a thematic target, not permission to invent unsupported competencies. Only create competencies directly supported by imported source items.

### 4. Evidence field

Canonical competencies must use:

```yaml
evidence:
  - source_id: ...
    source_version: ...
    item_ids:
      - ...
```

Do not use `source_refs` as the canonical field name.

### 5. Normalization notes

Add `normalization_notes` when required by the architecture document.

At minimum, the pilot must include examples of:

- several source items merged into one competency;
- one source item supporting more than one competency, if the imported evidence genuinely supports such a split;
- canonical wording generalized away from source-specific wording.

Do not force these patterns when evidence does not support them. Report any pattern that could not be demonstrated safely.

### 6. Validator

Extend the competency validator or add an appropriately scoped validator.

It must validate:

1. Schema conformance.
2. Package metadata/list ID agreement.
3. Package version agreement.
4. Canonical competency ID uniqueness across all canonical packages.
5. At least one evidence entry per competency.
6. Referenced source package existence.
7. Referenced source version equality.
8. Referenced source-item existence.
9. Non-empty evidence item lists.
10. Duplicate item IDs within one evidence entry.
11. Exact duplicate evidence entries.
12. No unsupported future-model fields.
13. Existing source packages remain independently valid.

The validator must not attempt to infer semantic equivalence automatically.

### 7. Fixtures and tests

Create positive fixtures for:

- one valid canonical competency package;
- multiple evidence entries;
- several items in one evidence entry;
- one source item reused by more than one competency.

Create negative fixtures or tests for:

- missing evidence;
- unknown source package;
- wrong source version;
- unknown item ID;
- duplicate competency ID;
- duplicate item ID in one evidence entry;
- duplicate evidence entry;
- package ID mismatch;
- package version mismatch;
- unsupported future field;
- empty title;
- empty outcome.

Use existing repository fixture and test conventions.

### 8. Documentation

Update documentation minimally to explain:

- source items are imported evidence;
- canonical competencies live under `competencies/normalized/`;
- normalization is governed by the architecture document;
- the first canonical package is a review-stage pilot;
- future relations and learning models are not yet implemented.

Likely files:

```text
README.md
docs/PROJECT_STATE.md
docs/ROADMAP.md
```

Follow actual repository layout.

## Canonical competency quality rules

Every pilot competency must:

1. Express one demonstrable capability.
2. Use an action-oriented title.
3. Use an observable outcome.
4. Be meaningful outside the source publication.
5. Remain within the scope of its evidence.
6. Avoid unsupported labels such as MVVM unless imported evidence explicitly supports them.
7. Avoid combining independent capabilities.
8. Avoid duplicating another pilot competency.
9. Use stable source-independent IDs.
10. Include normalization notes for non-trivial mappings.

## Required review report

Create:

```text
competencies/reports/android-app-architecture-normalization-review.md
```

The report must include:

- pilot package path;
- competency count;
- source package and version used;
- source-item coverage count;
- source items intentionally not covered;
- competencies with merged evidence;
- any source item reused by multiple competencies;
- canonical wording decisions;
- possible duplicates considered and rejected;
- unsupported candidate competencies intentionally not created;
- known limitations;
- validation commands and results;
- confirmation that Task 005 source files were not modified.

## Validation commands

Run the repository's applicable commands, including at least:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

If command names differ, use the repository's actual equivalents and explain the difference.

## Acceptance criteria

Task 006 is accepted only if:

- the architecture document exists;
- both canonical schemas exist;
- a pilot package with 8–12 competencies exists;
- every competency has valid evidence;
- all evidence resolves to Task 005 source items;
- canonical IDs are unique;
- referential validation is implemented;
- required negative cases are tested;
- non-trivial mappings contain normalization notes;
- source packages are unchanged;
- no future-model fields are introduced;
- the pilot package remains `review`;
- all validations pass;
- the review report is complete;
- no commit is created before reviewer approval.

## Out of scope

Do not:

- normalize all 35 source items;
- import additional publications;
- modify Task 005 source content;
- build prerequisite relations;
- build topic mappings;
- build learning paths;
- add levels or difficulty;
- add questions or practice;
- add user progress;
- implement automatic semantic deduplication;
- commit or push.

## Delivery

Return an implementation report containing:

1. Files added and modified.
2. Pilot competency count.
3. Evidence coverage.
4. Key normalization decisions.
5. Validator behavior.
6. Tests and fixtures.
7. Validation output.
8. Final `git status --short`.
9. Confirmation that no commit was created.

Then stage the intended changes and export the full review diff outside the repository:

```bash
git add .
git diff --cached > ..\task-006-review.diff
```
