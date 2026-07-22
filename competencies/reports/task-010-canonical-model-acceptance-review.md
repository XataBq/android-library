# Task 010 — Canonical Competency Model Acceptance Review

## Final decision

**ACCEPT**

The canonical competency model is mature enough to become the repository's
accepted architecture for stable, source-independent, evidence-backed
competencies. The implementation matches the documented model, the model has
survived a complete second-source normalization exercise, and downstream
learning-sequence references use canonical IDs without changing their identity
or creating hidden prerequisite semantics.

Acceptance applies to the architecture model only. Both source packages,
`android-app-architecture` version 2, and
`android-app-architecture-foundations` version 1 remain in `review`.

## Reviewed repository revision

- Base revision: `a12f1aa` (`feat(learning-sequences): add minimal validated learning sequence model`)
- Current branch: `main`
- Review input: repository contents at that revision plus the Task 010 task file

## Review scope

The review covered the canonical architecture document, normalization workflow,
both canonical schemas, validator and unit tests, both source packages, the
complete 19-competency version 2 registry, Task 006/006.1/006.2 and Task 008
review artifacts, deferred-relation research, and the Task 009 sequence model
and real sequence.

It did not re-review publication extraction for approval, edit competency
wording or evidence, approve any editorial package, design relations, or define
topic mappings.

## Review matrix

| # | Review question | Result | Repository evidence and finding |
|---:|---|---|---|
| 1 | Domain separation | `PASS` | `docs/ARCHITECTURE.md`, `docs/COMPETENCY_SOURCE_MODEL.md`, `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`, `docs/CONTENT_MODEL.md`, and `docs/LEARNING_SEQUENCE_MODEL.md` separately define publications, source items, evidence, canonical competencies, topics, sequences, and learner state. No ownership contradiction was found. |
| 2 | Canonical identity | `PASS` | Canonical model sections 3, 6, 8, and 11.4 define source-independent stable identity. `schemas/canonical-competencies.schema.json` uses stable IDs, while content and sequence schemas use their own topic, sequence, and stage IDs. Paths organize packages but do not own competency identity. |
| 3 | Demonstrability and granularity | `PASS` | Canonical model sections 4, 5, 7, 9, 12, and 14 define demonstrability, coherent primary capability, merge/split rules, canonical wording, duplicate review, and required notes. `android-app-architecture-normalization-review.md` demonstrates that reviewers can apply the rules without chat context. |
| 4 | Evidence model | `PASS` | `schemas/canonical-competencies.schema.json` requires non-empty evidence with `source_id`, `source_version`, and non-empty `item_ids`. `scripts/validate_competencies.py` resolves exact source versions and items. Tests cover multiple sources/items, reuse, missing sources/items, wrong versions, and duplicate evidence. The normalization workflow requires source immutability. |
| 5 | Versioning and lifecycle | `PASS` | Canonical model section 11.5 now distinguishes model-document version, schema version, competency-set version, source version, and editorial status, including semantic versus formatting-only changes. `docs/COMPETENCY_SOURCE_MODEL.md` and `docs/LEARNING_SEQUENCE_MODEL.md` define their independent version rules. No migration-blocking ambiguity remains. |
| 6 | Validation coverage | `PASS` | Both canonical schemas are closed Draft 2020-12 schemas. `scripts/validate_competencies.py` enforces path/package consistency, global canonical-ID uniqueness, exact evidence resolution, order-insensitive duplicate evidence, deterministic diagnostics, and repository-wide coexistence. `tests/competency_validator/` and `tests/learning_sequence_validator/` cover malformed YAML, non-mapping roots, missing files, Boolean versions, schema failures, semantic failures, and deterministic output. |
| 7 | Cross-source normalization evidence | `PASS` | `android-app-architecture-cross-source-normalization-review.md` accounts for all 29 second-source items: 3 attach-existing, 3 attach-existing-and-reword, 13 create-new item dispositions supporting 8 competencies, and 10 deferrals. All 11 original IDs remained stable; source-specific strength and technology details remained evidence/report concerns. The resulting 19 competencies were reviewed for duplicates and coherence. |
| 8 | Downstream compatibility | `PASS` | `docs/LEARNING_SEQUENCE_MODEL.md`, Architecture Study 002, and `learning-sequences/android-app-architecture-foundations/sequence.yaml` reference `android-app-architecture` version 2 by exact canonical IDs. Stage order is explicitly pedagogical and does not create canonical relations. Model acceptance does not approve the sequence, relations, or future mappings. |
| 9 | Known limitations | `PASS` | Canonical model sections 15–16, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, relation Study 001, and learning-sequence documentation keep relations, topic mappings, assessment mappings, mastery, catalogs, and adaptive routing deferred. These are separate future models, not missing invariants of canonical identity and evidence. |
| 10 | Documentation consistency | `PASS` | `README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, the canonical model, normalization workflow, and learning-sequence documentation consistently distinguish accepted architecture status from `review` package statuses. No document claims relations, topic mappings, or learner state are implemented. |

## Validation and test coverage reviewed

The schema and validator review confirmed:

- canonical set and competency-list shape;
- closed objects and stable kebab-case ID patterns;
- directory/set ID and set-version consistency;
- repository-wide canonical competency ID uniqueness;
- required evidence and non-empty item lists;
- source existence and exact source-version matching;
- source-item existence;
- duplicate item and order-insensitive duplicate evidence rejection;
- deterministic diagnostics;
- controlled diagnostics for malformed YAML and non-mapping roots;
- successful coexistence of source, canonical, and learning-sequence validation.

A direct data review found two source packages, 19 unique canonical competency
IDs, 40 resolved source-item references, matching canonical metadata/list
version 2, and 19 unique sequence references resolving to the complete current
canonical set.

## Cross-source normalization findings

The second source fit the existing architecture without schema changes,
validator changes, unsupported fields, or structural workarounds. Equivalent
capabilities accumulated evidence under stable IDs. Partial overlaps were
classified before disposition. Eight distinct capabilities were added, ten
under-supported or source-specific items were deferred, and all recommendation-
strength differences and tensions remained visible in the report.

The canonical package advanced from version 1 to version 2 while retaining all
11 existing IDs. This demonstrates stable identity, evidence aggregation,
controlled membership growth, explicit deferral, and human semantic duplicate
review.

## Downstream learning-sequence compatibility

The first sequence pins `android-app-architecture` version 2 and references all
19 current competency IDs exactly once. The learning-sequence schema and
validator resolve those references but do not add relations to canonical data.
Accepting the canonical architecture therefore does not accept the sequence's
editorial ordering and does not require a relation or topic-mapping model.

## Known limitations

The following remain deliberately deferred and are not blockers:

- canonical competency relations;
- competency-to-topic mappings;
- assessment and practice mappings;
- learner mastery and progress;
- generated catalogs;
- adaptive routing;
- aliases, deprecations, and automated semantic duplicate detection.

The active canonical package represents one current version and relies on Git
history for earlier revisions. Exact-version consumers must migrate when the
active version changes. This behavior is now explicit in the architecture
document and is sufficient for the current repository-local workflow.

## Files changed

- `docs/architecture/CANONICAL_COMPETENCY_MODEL.md`;
- `README.md`;
- `docs/ARCHITECTURE.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`;
- `competencies/reports/android-app-architecture-cross-source-normalization-review.md`;
- `tasks/010-canonical-competency-model-acceptance-review.md`;
- `competencies/reports/task-010-canonical-model-acceptance-review.md`.

No source package, canonical package, schema, validator, test, content package,
or learning-sequence package changed.

## Commands and results

```text
python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
2 templates, 26 schema fixtures

python -B scripts/validate_content.py
PASS — 0 topic packages, 2 templates, 4 schema fixtures

python -B -m unittest discover
PASS — 86 tests

git diff --check
PASS

repository-local Markdown target check
PASS — all Markdown link targets resolve

git diff -- competencies/normalized competencies/sources schemas scripts tests content templates learning-sequences
PASS — no changes
```

Direct Draft 2020-12 and reference-resolution review also passed: 19 unique
competencies, 40 resolved item references, canonical/sequence version 2, and 19
unique sequence references. Baseline and final Git object hashes also confirmed
that both source packages, both canonical package files, and the real sequence
were byte-for-byte unchanged.

## Deviations

No task deviation was required. The model-document version remains `1` because
the status transition approves the existing architecture contract and the
repository has no convention requiring a version increment for status-only
acceptance. Package versions and editorial statuses were intentionally left
unchanged.

## Human-owner decision note

This report records Codex's technical and editorial recommendation to
**ACCEPT** and prepares `Status: ACCEPTED` under Task 010. The repository owner
retains final architecture authority and approves the transition by reviewing
and committing these changes. No package is approved by this decision.
