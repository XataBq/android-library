# Task 020 — Kotlin Structured Concurrency and Supervision implementation report

## Final result

**PASS**

Task 020 adds the eighth production topic in `review`, focused on owned Job
trees, propagation, fail-fast and supervised execution, timeout, cleanup, and
long-lived Android work.

## Files

Created the six canonical files under
`content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/` and
this report. Updated `README.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`,
two stale counts in `docs/ARCHITECTURE.md`, and the canonical Task 020 file at
`tasks/020-add-kotlin-structured-concurrency-and-supervision-topic.md`.

No existing topic, source, competency, sequence, mapping, schema, validator,
fixture, or test infrastructure file changed.

## Source and evidence audit

Both imported Android source packages, the canonical Android architecture
package, all production topics, and Task 019 were inspected. Repository
evidence primarily supports `use-coroutines-and-flows-across-layers`, with
ViewModel, lifecycle, separation, Domain, and Data boundaries reinforced.

Current official Kotlin material was checked for structured concurrency, Job
hierarchy, cancellation, exception propagation, `coroutineScope`,
`supervisorScope`, `SupervisorJob`, timeout, and `NonCancellable`. Official
Android guidance was checked for external scopes, coroutine tests, and the
WorkManager durable-scheduling boundary. All 8 references use the actual
inspection date `2026-07-24`.

## Canonical coverage

Primary: `use-coroutines-and-flows-across-layers`.

Reinforced: `design-viewmodel-ui-state`,
`handle-compose-lifecycle-work`,
`explain-android-component-lifecycle-constraints`,
`apply-separation-of-concerns`,
`evaluate-optional-domain-layer`, and
`design-data-layer-around-repositories`.

No competency or production mapping changed.

## Job-tree and propagation audit

The content demonstrates explicit Job trees, parent waiting, downward
cancellation, upward non-cancellation failure, and regular-scope sibling
cancellation. `coroutineScope` is presented as a bounded fail-fast suspend
contract. Cancellation remains cooperative and distinct from failure.

## Supervision audit

`supervisorScope` isolates direct child failures within a bounded call;
`SupervisorJob` defines failure policy for an explicitly owned long-lived
scope. Neither suppresses errors. Every Deferred is retained and awaited or
translated into explicit partial state while preserving cancellation.
The best-effort helper and the supervised-failure test explicitly rethrow
`CancellationException`; no ordinary `runCatching` remains around suspending
work.

Fail-fast is selected for required aggregates; best-effort is selected only
for independently useful outcomes.

## Timeout and cleanup audit

`withTimeout` and `withTimeoutOrNull` cancel their lexical child subtree.
Detached work escaping timeout is rejected. Cleanup uses `finally`;
`NonCancellable` is limited to small mandatory suspending cleanup and is not
used as a child Job or business-work region.

## Android ownership audit

Screen work belongs to ViewModel/lifecycle ownership. Disposable work that
must outlive a screen can use an injected application-owned scope with an
explicit completion contract. Reliable work that must be rescheduled beyond
process exit or device restart crosses into WorkManager. Repositories do not
create ad hoc scopes.

## Junior-Core documentation audit

Structured Concurrency and Supervision is recorded as
**Junior Core — advanced foundation**. The Junior Core target is exactly 17
mandatory topics. Eight currently exist as complete production packages in
`review`; nine remain: Kotlin Flow and Reactive Streams, Android Navigation
Architecture, Android Networking Architecture, Dependency Injection and
Scoping, Android Testing Foundations, Android Security Foundations, Local
Persistence with Room, Background Work and WorkManager, and Compose
Foundations. The final Junior/Middle boundary is deferred until the full Junior
Core is implemented and reviewed. No grading schema or universal
industry-level claim was introduced.

## Content and duplication audit

Task 019 is the sole prerequisite and the validated graph is acyclic. Coroutine
foundations are referenced briefly rather than repeated. Existing production
topic packages and statuses are unchanged.

## Exact counts and metadata

- Package files: 6.
- Theory sections: 22.
- Kotlin examples: 16.
- Practice exercises: 4.
- Interview questions: 22.
- Test questions: 10.
- Official references: 8.
- Taxonomy: `kotlin` / `coroutines`.
- Status/version/time: `review` / 1 / 180 minutes.

The preferred `intermediate` difficulty is not schema-valid. It was adapted to
the nearest supported value, `middle`, while the separate editorial
classification remains Junior Core — advanced foundation.

## Validation

```text
python -B scripts/validate_content.py
PASS — 8 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

## UTF-8 and mojibake audit

All 12 new or modified Markdown/YAML source files decode as strict UTF-8
without BOM. They contain none of the checked mojibake sequences, and the new
topic contains no absolute local path.

## Deferred work

The nine remaining mandatory Junior Core topics, final Junior/Middle boundary
review, editorial acceptance/publication, mappings, catalog, CI, clients,
learner database, and AI tutor remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/cheat-sheet.md
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/interview.md
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/practice.md
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/test.yaml
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/theory.md
 A content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-020-kotlin-structured-concurrency-and-supervision-implementation.md
 A tasks/020-add-kotlin-structured-concurrency-and-supervision-topic.md
?? 020-codex-prompt.md
?? 020-review.diff
```

## Recommended commit message

```text
feat(content): add Kotlin structured concurrency topic
```
