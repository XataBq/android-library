# Task 009 — Minimal Learning Sequence Model implementation report

## Summary

Task 009 adds a repository-native version 1 learning-sequence contract and one
reviewed Android app architecture path. The sequence is a separate pedagogical
model: its ordered stages reference canonical competencies without creating
canonical relations or prerequisites.

## Files

Added:

- `schemas/learning-sequence.schema.json`;
- two valid and eleven invalid fixtures under
  `schemas/fixtures/learning-sequences/`;
- `tests/learning_sequence_validator/__init__.py`;
- `tests/learning_sequence_validator/test_validate_learning_sequences.py`;
- `learning-sequences/android-app-architecture-foundations/sequence.yaml`;
- `learning-sequences/android-app-architecture-foundations/README.md`;
- this implementation report;
- `docs/LEARNING_SEQUENCE_MODEL.md`;
- `docs/LEARNING_SEQUENCE_AUTHORING.md`;
- `research/architecture-studies/001-canonical-competency-relations.md`;
- `research/architecture-studies/002-learning-sequence-model.md`.

Modified:

- `scripts/validate_competencies.py`;
- `README.md`;
- `docs/ARCHITECTURE.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Removed:

- the obsolete unnumbered learning-sequence architecture-study duplicate; its
  authoritative numbered replacement is
  `research/architecture-studies/002-learning-sequence-model.md`.

No existing competency package, source package, content package, schema, or
test was removed.

Pre-existing untracked inputs included with Task 009:

- `tasks/009-minimal-learning-sequence-model.md`;
- `research/architecture-studies/001-canonical-competency-relations-phase-2a-semantic-profiling.md`;
- `research/architecture-studies/001-canonical-competency-relations-phase-2b-iteration-1.md`.

The task specification was retained unchanged. The two phase-study inputs had
only trailing whitespace removed so the staged review diff passes whitespace
validation; their research content was not changed.

## Schema decisions

The schema uses JSON Schema Draft 2020-12 and `schema_version: 1`. Top-level,
competency-set-reference, and stage objects are closed with
`additionalProperties: false`.

Required top-level fields are `schema_version`, `sequence_id`,
`sequence_version`, `title`, `language`, `status`, `competency_set`, and
`stages`. Only `description` and `editorial_notes` are optional. A stage
requires `id`, `title`, and `competencies`; only `rationale` and
`editorial_notes` are optional.

IDs use the repository kebab-case convention. Text must be non-empty, language
uses the existing language-tag pattern, status reuses the existing editorial
vocabulary, and both versions are positive integers. Stages and competency
lists have `minItems: 1`; a stage's competency list also has `uniqueItems: true`.

The schema contains no relation, graph, branching, weight, difficulty,
progress, adaptive-routing, or topic-mapping fields.

## Semantic validation

The existing competency validator now discovers immediate sequence packages
under `learning-sequences/` and checks:

- package directory equals `sequence_id`;
- each `sequence_id` plus `sequence_version` pair is unique;
- the referenced canonical competency set exists;
- the referenced set version exactly matches repository metadata;
- every referenced competency ID exists in that set;
- stage IDs are unique;
- a competency is not repeated within one stage;
- a competency is not repeated across stages;
- stages and competency lists are not empty;
- required package files parse and satisfy the schema.

Diagnostics use the existing immutable diagnostic record and sorted,
deduplicated rendering, so output remains deterministic. Validation does not
infer prerequisites or evaluate pedagogical quality.

## Fixtures and tests

Valid fixtures cover a minimal sequence and a multi-stage sequence using all
optional text fields. Invalid fixtures cover a missing required field,
unsupported schema version, empty stages, an empty competency list, duplicate
stage IDs, duplicate competencies within and across stages, an unknown set,
wrong set version, unknown competency ID, and an unexpected property.

Twenty-two focused unit tests cover schema meta-validation, both valid fixtures,
all schema and semantic rejection rules, package ID consistency, duplicate
sequence identity/version, missing and malformed package files, list and scalar
YAML roots, deterministic diagnostics, and successful repository-wide
validation of the real package.

## Canonical reference and stages

The sequence references canonical competency set `android-app-architecture`
version `2`. Its 19 references exactly cover the current 19 IDs once each:

1. `platform-constraints`
   - `explain-android-component-lifecycle-constraints`
2. `foundational-boundaries`
   - `apply-separation-of-concerns`
   - `design-independent-app-components`
   - `isolate-android-framework-dependencies`
3. `state-and-data-principles`
   - `establish-single-source-of-truth`
   - `explain-unidirectional-data-flow`
   - `explain-persistent-data-models`
4. `ui-architecture`
   - `explain-ui-layer-responsibilities`
   - `design-viewmodel-ui-state`
   - `select-ui-state-holders-by-scope`
   - `handle-compose-lifecycle-work`
5. `data-architecture`
   - `explain-repository-responsibilities`
   - `design-data-layer-around-repositories`
   - `use-coroutines-and-flows-across-layers`
6. `dependency-management`
   - `explain-dependency-injection`
   - `scope-dependencies-when-needed`
7. `application-composition`
   - `design-single-activity-navigation`
   - `evaluate-optional-domain-layer`
   - `evaluate-layer-specific-models`

## Validation results

Baseline before implementation:

- `python -B scripts/validate_content.py` — passed, 0 topic packages, 2
  templates, 4 fixtures;
- `python -B scripts/validate_competencies.py` — passed, 2 source packages, 1
  canonical package, 2 templates, 13 fixtures;
- `python -B -m unittest discover` — 64 tests passed;
- `git diff --check` — passed.

Implemented checks:

- `python -B -m unittest tests.learning_sequence_validator.test_validate_learning_sequences`
  — 22 tests passed;
- `python -B scripts/validate_content.py` — passed, 0 topic packages, 2
  templates, 4 fixtures;
- `python -B scripts/validate_competencies.py` — passed, 2 source packages, 1
  canonical package, 1 learning-sequence package, 2 templates, 26 fixtures;
- `python -B -m unittest discover` — 86 tests passed;
- `git diff --check` — passed; Git emitted only its Windows LF-to-CRLF working
  copy warning for `scripts/validate_competencies.py`;
- direct YAML parsing, Draft 2020-12 schema meta-validation and instance
  validation, exact set/version matching, and exact 19-ID coverage — passed;
- the three local Markdown targets added to or changed in documentation — all
  exist.

One initial auxiliary Python one-liner for the direct coverage check had a
PowerShell quoting `SyntaxError`. The same check was rerun with simplified
quoting and passed; repository code and data were not involved in the failure.

## Deviations and input-path reconciliation

The requested exact research paths were absent at baseline. The supplied
materials instead used two phase-specific Study 001 filenames and an unnumbered
learning-sequence study. They were read completely. Exact Study 001 and Study
002 decision files were added at the paths required by Task 009 without
changing the approved ordered-stage architecture, and the obsolete unnumbered
duplicate was removed.

The implementation report is stored in `learning-sequences/reports/`, following
the existing domain-local `reports/` convention. Package discovery deliberately
excludes that documentation directory.

No domain-model deviation from Task 009 was introduced. The task-file status
was not changed because Task 009 does not authorize an implementer status
transition and repository policy leaves status control to the human owner.

## Deferred work

Canonical competency relations, prerequisites, general graphs, branches,
weights, difficulty, learner progress, adaptive routing, assessments, topic
mappings, authored topics, and publication remain deferred. The sequence and
canonical package remain in `review`; the canonical model remains `PROPOSED`.
