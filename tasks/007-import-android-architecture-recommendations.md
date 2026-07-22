# Task 007 — Import Android architecture recommendations as a second source

Status: DONE
Phase: Phase 2 — Competency import
Type: Provenance-preserving source import

## Goal

Import the Android Developers publication **Recommendations for Android architecture** as the repository's second real competency source package.

This task records what the publication says. It must not normalize the imported items, modify canonical competencies, add evidence to the canonical registry, define relations, or create a learning sequence.

The resulting package will become the input for a separate cross-source normalization task.

## Selected source

Canonical publication URL:

```text
https://developer.android.com/topic/architecture/recommendations?hl=en
```

Expected publication title:

```text
Recommendations for Android architecture
```

Expected publisher:

```text
Android Developers
```

Proposed source package ID:

```text
android-developers-architecture-recommendations
```

The live publication is authoritative. Verify its title, visible update date, scope, hierarchy, wording, recommendation priorities, and canonical URL during implementation.

Do not use this task's descriptive text as a substitute for inspecting the live source.

## Why this source

This publication is suitable as a second source because it:

- is a separately maintained Android architecture publication;
- contains explicit recommendation strength;
- overlaps with the existing app-architecture source in areas such as layers, repositories, unidirectional data flow, domain layers, dependency injection, and lifecycle handling;
- introduces additional implementation-oriented capabilities;
- can test cross-source identity and evidence aggregation in the next task.

This task does not perform that cross-source comparison.

## Architectural authority

Read and follow:

```text
AGENTS.md
docs/PROJECT_VISION.md
docs/PROJECT_PRINCIPLES.md
docs/ARCHITECTURE.md
docs/PROJECT_STATE.md
docs/ROADMAP.md
docs/COMPETENCY_SOURCE_MODEL.md
docs/COMPETENCY_IMPORT_WORKFLOW.md
docs/COMPETENCY_NORMALIZATION_WORKFLOW.md
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

For this task, the primary operational authorities are:

```text
docs/COMPETENCY_SOURCE_MODEL.md
docs/COMPETENCY_IMPORT_WORKFLOW.md
```

## Preconditions

The repository already contains:

```text
competencies/sources/android-developers-app-architecture/
competencies/normalized/android-app-architecture/
```

The existing source and canonical packages must remain unchanged.

Task 006.2 should already be committed before this task is implemented.

---

# Required work

## 1. Inspect repository state

Before editing:

```bash
git status --short
git log --oneline --decorate -12
```

Confirm:

- the worktree is clean or contains only explicitly expected task setup;
- Task 006.2 is committed;
- the source model and import workflow are current;
- the proposed source ID is not already used.

Read the complete existing source package:

```text
competencies/sources/android-developers-app-architecture/source.yaml
competencies/sources/android-developers-app-architecture/items.yaml
competencies/reports/android-developers-app-architecture-review.md
```

Use it as a structural precedent, not as content to copy.

## 2. Inspect the complete live publication

Inspect:

```text
https://developer.android.com/topic/architecture/recommendations?hl=en
```

Record the actual UTC retrieval date.

Inspect the entire in-scope publication, including:

- introduction and recommendation-strength definitions;
- layered architecture;
- UI layer;
- ViewModel;
- lifecycle;
- dependency handling;
- testing;
- models;
- naming conventions;
- any other first-party section currently present on the canonical page;
- visible update label;
- source hierarchy;
- notes and exceptions that qualify recommendation strength.

Do not import linked publications as though they were part of this source.

Links may be recorded in review notes as out-of-scope references, but linked pages require separate source packages.

## 3. Define the source boundary

The package represents exactly the canonical English page:

```text
https://developer.android.com/topic/architecture/recommendations?hl=en
```

It does not include:

- the general Guide to app architecture page;
- the Views-specific recommendations page;
- linked UI-layer, data-layer, domain-layer, coroutine, testing, Compose, Navigation, Hilt, or lifecycle publications;
- code samples as separate competencies;
- material inferred from linked pages;
- general Android knowledge not stated on the page.

If the canonical page includes embedded prose necessary to interpret a recommendation, retain that meaning in the relevant item or context.

## 4. Create the source package

Create:

```text
competencies/sources/android-developers-architecture-recommendations/
├── source.yaml
└── items.yaml
```

Do not create `raw/` artifacts unless storage is clearly permitted, necessary, declared, and approved by the existing source model.

The expected default is no raw artifacts.

### 4.1 `source.yaml`

Use the current source schema.

Expected values include:

```yaml
schema_version: 1
id: android-developers-architecture-recommendations
title: Recommendations for Android architecture
source_type: other
language: en
source_version: 1
status: review
repository_usage: citation-only
```

Use the exact values supported by the current schema and source-model conventions.

For provenance:

- use the canonical English URL;
- record publisher;
- record the actual retrieval date;
- record the visible publication update label when present;
- use a concise citation;
- state the package boundary;
- note that linked publications are out of scope.

Do not claim that schema validity establishes copyright or licensing permission.

### 4.2 `items.yaml`

Create faithful source items for the meaningful recommendations on the complete page.

Each item must include:

```yaml
id:
statement:
locator:
```

Use optional fields only when they add real source fidelity:

```yaml
context:
declared_level:
transcription_notes:
```

## 5. Preserve recommendation strength

The publication distinguishes recommendation priorities.

Preserve the exact source-declared priority in:

```yaml
declared_level:
```

Use the source's own English wording consistently, for example:

```text
Strongly recommended
Recommended
Optional
```

Do not translate these into learner difficulty, seniority, obligation, or platform policy.

Do not omit recommendation strength when the source explicitly attaches it to an item.

The page-level statement that recommendations are not strict requirements must be preserved in package provenance, review documentation, or relevant extraction notes so individual items are not misread as absolute rules.

## 6. Extraction granularity

Use one source item per independently meaningful recommendation.

Do not mechanically create source items from:

- section headings alone;
- introductory prose with no distinct recommendation;
- code samples that merely illustrate a recommendation;
- every bullet when bullets are inseparable qualifications of one recommendation;
- every sentence within a table cell.

A recommendation and its essential conditions or qualifying bullets should normally remain one item.

Split one recommendation only when the publication clearly contains multiple independently reviewable claims.

Do not merge different recommendation rows merely because they share a section.

## 7. Item IDs

Use stable semantic lowercase kebab-case IDs.

IDs must:

- describe the source-level recommendation;
- remain understandable without array position;
- avoid retrieval dates;
- avoid canonical competency identity assumptions;
- avoid implementation-specific wording unless it is essential to the source recommendation.

Examples of acceptable style:

```text
use-clearly-defined-data-layer
expose-data-through-repositories
follow-unidirectional-data-flow
keep-viewmodels-lifecycle-independent
use-lifecycle-aware-ui-state-collection
use-dependency-injection
prefer-fakes-to-mocks
```

These are examples of ID style, not a mandatory extraction list. Derive the final IDs from the live publication.

## 8. Statements and faithful transcription

Statements must be concise faithful transcriptions or owner-authored summaries permitted by `citation-only`.

Preserve:

- recommendation action;
- conditions;
- exceptions;
- recommendation strength through `declared_level`;
- source-specific technologies when they are central to the recommendation;
- distinctions such as Hilt versus manual dependency injection;
- distinctions between screen-level ViewModels and reusable UI state holders;
- conditional guidance for small or complex applications.

Do not:

- convert recommendations into universal requirements;
- normalize source wording into canonical competency outcomes;
- broaden Compose-specific guidance into generic UI guidance;
- infer Clean Architecture, MVVM, MVI, or other labels not explicitly stated;
- combine statements using knowledge from linked pages;
- add explanations from general Android knowledge.

## 9. Locators

Use durable heading-based locators.

Each item should be traceable to:

- the relevant publication section;
- the recommendation row or visible recommendation label;
- a human-readable detail when several items share the same heading.

Prefer locators based on visible structure rather than:

- DOM selectors;
- generated anchors;
- row numbers;
- paragraph indexes;
- copied HTML identifiers.

## 10. Review report

Create:

```text
competencies/reports/android-developers-architecture-recommendations-review.md
```

Required sections:

```text
# Android Developers architecture recommendations import review

## Package summary
## Source boundary
## Extraction approach
## Recommendation priority handling
## Section coverage
## Item inventory
## Linked material intentionally excluded
## Potential overlap for future normalization
## Ambiguities and transcription decisions
## Public-repository safety
## Validation results
## Human review checklist
```

### 10.1 Package summary

Record:

- source ID;
- source version;
- package status;
- retrieval date;
- visible update label;
- total item count.

### 10.2 Section coverage

List every in-scope publication section and the imported item IDs derived from it.

If a section produces no item, explain why.

### 10.3 Item inventory

Provide a compact table:

```text
Item ID | Section | Declared level | Extraction note
```

### 10.4 Potential overlap

Identify, without performing normalization, likely areas of overlap with the existing source and canonical pilot.

Examples may include:

- layered architecture;
- repositories;
- UI responsibilities;
- UDF;
- optional domain layer;
- dependency injection;
- lifecycle-safe ownership.

This section is analysis for the next task only.

Do not:

- attach evidence;
- declare semantic equivalence as final;
- modify canonical wording;
- create new canonical competencies.

Classify observations only as candidates requiring Task 008 review.

### 10.5 Human review checklist

Include checks for:

- exact source boundary;
- complete section coverage;
- recommendation priority accuracy;
- faithful conditions and exceptions;
- locator traceability;
- item granularity;
- no linked-page leakage;
- no canonicalization leakage;
- public repository safety.

## 11. Validation and validator changes

Run the existing validator without changing it first:

```bash
python -B scripts/validate_competencies.py
```

The new package should be accepted by existing source schemas and semantic validation.

Do not modify schemas, validator code, or tests merely to accommodate bad package data.

A validator change is allowed only if the new valid package exposes a concrete defect in already-approved behavior.

If that occurs:

1. stop;
2. report the defect clearly;
3. avoid silently expanding Task 007;
4. wait for architectural approval before changing validator behavior.

## 12. Documentation synchronization

Update only factual state documents that must acknowledge the second source import.

Expected minimal updates:

```text
README.md
docs/PROJECT_STATE.md
```

Update them only after the package is complete.

State accurately that:

- two source packages now exist in `review`;
- only the first source has a canonical normalization pilot;
- cross-source normalization has not yet been performed;
- Task 008 is the next milestone.

Do not mark:

- source packages as `approved`;
- canonical package as `approved`;
- canonical model as `ACCEPTED`;
- Phase 2 as complete.

Update this task status from `READY` to `REVIEW` after successful implementation.

---

# Explicit non-goals

Do not:

- change the existing source package;
- change the existing canonical package;
- add evidence to canonical competencies;
- create canonical competencies;
- normalize source items;
- define duplicate resolutions;
- change canonical competency wording;
- define prerequisite or related-competency edges;
- define learning order;
- map competencies to topics;
- generate educational topics;
- add learner difficulty;
- add assessment;
- add progress state;
- scrape or store complete page HTML;
- import linked publications;
- add CI;
- create a commit;
- push changes.

---

# Required validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Verify existing domain data is unchanged:

```bash
git diff -- competencies/sources/android-developers-app-architecture/
git diff -- competencies/normalized/
git diff -- schemas/ scripts/ tests/ content/ templates/
```

Verify the new package contains only intended files:

```bash
find competencies/sources/android-developers-architecture-recommendations -maxdepth 3 -type f
```

Use the Windows equivalent if required by the environment.

## Acceptance criteria

Task 007 is accepted only if:

- the complete live canonical publication was inspected;
- source scope is exactly one independently maintained English page;
- every meaningful in-scope recommendation was considered;
- recommendation priorities are preserved as source-declared levels;
- conditions and exceptions are retained;
- code examples are not extracted as standalone competencies;
- linked pages do not leak into the package;
- source items are source-level and not canonicalized;
- IDs are stable and semantic;
- locators are durable and manually traceable;
- the review report accounts for every in-scope section;
- potential overlap is documented only as future-review candidates;
- existing source and canonical packages are unchanged;
- current schemas and validators accept the package;
- all validation commands pass;
- package status remains `review`;
- canonical model remains `PROPOSED`;
- no commit is created.

## Delivery report

Return:

1. Files created and changed.
2. Live source title, canonical URL, retrieval date, and visible update label.
3. Final source boundary.
4. Total imported item count.
5. Item count by section and recommendation priority.
6. Important extraction and granularity decisions.
7. Linked material excluded.
8. Candidate overlap areas for Task 008.
9. Validation results.
10. Existing package immutability confirmation.
11. Final `git status --short`.
12. Confirmation that no commit was created.

Then stage the intended changes and export:

```bash
git add README.md docs/PROJECT_STATE.md competencies/sources/android-developers-architecture-recommendations competencies/reports/android-developers-architecture-recommendations-review.md tasks/007-import-android-architecture-recommendations.md
git diff --cached > ..\task-007-review.diff
```

Do not create a commit.
