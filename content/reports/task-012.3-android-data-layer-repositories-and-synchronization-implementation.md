# Task 012.3 — Android Data Layer, Repositories, and Synchronization implementation report

## Final result

**PASS**

Task 012.3 adds the third production topic package in `review`, with the
Task 012.1 foundations topic and Task 012.2 UI-layer topic as prerequisites.
No production mapping, competency, learning-sequence, schema, or validator
change was made.

## Files

Created the six canonical files under
`content/android/app-architecture/android-data-layer-repositories-and-synchronization/`
and this report. Updated `README.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and the Task 012.3 status.

## Metadata

- ID: `android-data-layer-repositories-and-synchronization`
- difficulty/status: `foundation` / `review`
- estimated time/version: 150 minutes / 1
- prerequisites: `android-app-architecture-foundations` and
  `android-ui-layer-and-unidirectional-data-flow`

## Educational design decisions

- The theory follows the required 21-section sequence and treats repository,
  source, and synchronization diagrams as conceptual responsibility flows.
- Repositories expose application operations and own source selection,
  freshness, synchronization, and application-level error policy. Data sources
  communicate with one concrete system.
- SSOT is defined per data set and may be remote, durable local storage, or
  repository-owned memory. A cache is not automatically authoritative.
- Network-first, cache-first, and local-first reads are compared through
  latency, freshness, fallback, offline behavior, invalidation, and
  synchronization cost.
- Remote-first, optimistic, and offline-queued writes include partial failure,
  retry classification, idempotency, rollback, pending state, and conflict
  semantics.
- Transport, persistence, application, and UI models are separated only when
  different contracts justify their mapping cost.
- Practice contains five complete architecture exercises. The test contains
  exactly twelve questions, all five supported types, scenarios, two code
  analyses, and valid constructed-answer rubrics.
- Primary sources are four canonical official Android Developers pages checked
  on 2026-07-23.

## Validation

```text
python -B scripts/validate_content.py
PASS — 3 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

Encoding audit: all new and modified Markdown/YAML files decode as strict
UTF-8, contain no BOM, and contain no known mojibake or Unicode replacement
characters. The six topic files are present and the test contains exactly
twelve questions. A separate repository-wide audit scanned 136 Markdown/YAML
files and found nine pre-existing mojibake occurrences in
`competency-topic-mappings/reports/task-011-minimal-competency-topic-mapping-model-implementation.md`.
That protected, out-of-scope Task 011 report was not modified.

## Deferred work

Editorial approval/publication, further production topics, production
competency-to-topic mappings, API-specific persistence or networking topics,
and Android client/runtime synchronization remain deferred.

## Git status

The literal final `git status --short` output is recorded here after
intent-to-add and review-diff generation:

```text
 M README.md
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/cheat-sheet.md
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/interview.md
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/practice.md
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/test.yaml
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/theory.md
 A content/android/app-architecture/android-data-layer-repositories-and-synchronization/topic.yaml
 A content/reports/task-012.3-android-data-layer-repositories-and-synchronization-implementation.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A tasks/012.3-android-data-layer-repositories-and-synchronization.md
?? 012.3-review.diff
```

Intent-to-add is used only to make new files visible in the normal repository
diff. No file content is staged, and no commit was created.

## Recommended commit message

```text
feat(content): add Android data layer topic
```
