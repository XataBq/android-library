# Task 019 — Kotlin Coroutines Foundations implementation report

## Final result

**PASS**

Task 019 adds the seventh production educational topic in `review`. It presents
a coroutine as an owned cancellable computation rather than a lightweight
thread and builds an execution model around scope, context, Job, dispatcher,
thread, suspension, and continuation.

## Files

Created the six canonical files under
`content/kotlin/coroutines/kotlin-coroutines-foundations/` and this
implementation report. Updated `README.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, two stale topic-count phrases in `docs/ARCHITECTURE.md`, and
Task 019 status.

No existing topic, source package, competency, learning sequence, mapping,
schema, validator, fixture, or test file changed.

## Source and evidence audit

Both imported Android Developers source packages were inspected. The primary
repository evidence comes from
`android-developers-architecture-recommendations` items
`communicate-between-layers-with-coroutines-flows` and
`use-flows-and-suspend-functions-in-viewmodels`. Lifecycle-aware UI collection
and Compose coroutine work reinforce Android ownership. The first source
package reinforces component lifetime and separation boundaries without
inventing coroutine runtime detail.

Current official Kotlin documentation was inspected for coroutine basics,
context and dispatchers, cancellation, and exception behavior. Current
official Android documentation was inspected for coroutine best practices,
lifecycle-aware scopes, ViewModel ownership, and coroutine testing. All eight
metadata references are official Kotlin or Android Developers pages and use
the actual inspection date `2026-07-24`.

The content makes no unstable scheduler, pool-size, compiler-transformation,
thread-affinity, or performance guarantee.

## Canonical competency coverage

Primary:

- `use-coroutines-and-flows-across-layers`.

Strongly reinforced:

- `handle-compose-lifecycle-work`;
- `design-viewmodel-ui-state`;
- `explain-android-component-lifecycle-constraints`.

Contextually reinforced:

- `apply-separation-of-concerns`;
- `explain-ui-layer-responsibilities`;
- `design-data-layer-around-repositories`;
- `evaluate-optional-domain-layer`.

No competency or production competency-to-topic mapping was created or
modified.

## Execution-model audit

The topic explicitly distinguishes:

- coroutine as a cancellable computation;
- CoroutineScope as lifetime owner;
- CoroutineContext as a collection of execution elements;
- Job as lifecycle and parent-child hierarchy;
- Dispatcher as scheduling policy;
- Thread as the actual JVM/OS execution resource;
- continuation as the state needed to resume suspended computation.

It states that `suspend` neither creates a coroutine, selects background
execution, nor converts blocking work. Main, Default, IO, and Unconfined are
explained by responsibility without treating a dispatcher as one thread or
relying on pool sizes.

`launch`, `async`, `Deferred`, and `withContext` are separated by result,
overlap, and lifetime needs. Sequential, concurrent, and potentially parallel
execution are distinct, and immediate `async().await()` is shown as a
counterexample.

## Cancellation and exception audit

Cancellation is presented as cooperative Job control flow. Cancellable
suspensions observe cancellation; CPU loops use periodic `ensureActive` or
`yield`; parent cancellation reaches children; cleanup belongs in `finally`.

The cancellation-safe catch example rethrows `CancellationException` before
translating an expected `IOException`. The topic explains basic launch/async
failure behavior and why `CoroutineExceptionHandler` is not a universal
catch-all. Advanced supervision and partial-failure strategy remain deferred.

## Android scope and layer-boundary audit

`viewModelScope`, `lifecycleScope`, `repeatOnLifecycle`, and Compose-owned
scopes are selected according to their actual owners. Longer-lived work
requires an explicit application or persistent-work owner rather than
`GlobalScope`.

ViewModel starts UI-scenario work; Domain exposes focused suspend or Flow
contracts; Data owns blocking/suspending source integration and dispatcher
selection near blocking or CPU-intensive implementations. Suspend contracts
are main-safe without requiring every pure class to own a dispatcher.
Repositories do not hide caller-owned fire-and-forget work.

## Prerequisite and duplication audit

The prerequisites are:

- `android-app-architecture-foundations`;
- `android-viewmodel-and-ui-state`;
- `android-lifecycle-and-state-restoration`.

Content validation confirms that all prerequisites exist and the graph is
acyclic. The new topic assumes existing architecture, UiState, ViewModel,
lifecycle, Data, and Domain ownership. It deepens coroutine execution,
suspension, dispatching, cancellation, basic failure behavior, and testing
without repeating full existing-topic explanations.

All six existing topic packages and their statuses are unchanged.

## Theory coverage

The 22 numbered theory sections cover:

1. motivation;
2. coroutine versus thread;
3. suspend functions;
4. continuation and resumption;
5. CoroutineScope;
6. CoroutineContext;
7. Job hierarchy;
8. dispatchers;
9. thread switching;
10. `launch`;
11. `async` and Deferred;
12. `withContext`;
13. sequential, concurrent, and parallel execution;
14. blocking versus suspending;
15. cooperative cancellation;
16. cancellation-safe catches;
17. parent-child cancellation;
18. basic exceptions;
19. Android scopes;
20. layer boundaries;
21. virtual-time testing;
22. anti-patterns and decision checklist.

## Kotlin example audit

Theory contains exactly 14 Kotlin code blocks:

1. basic sequential suspending function;
2. parent scope and child Jobs;
3. thread logging around suspension;
4. `launch` returning Job;
5. concurrent sibling `async`/`await`;
6. immediate-await counterexample;
7. `withContext` for blocking file integration;
8. sequential dependency example;
9. `delay` versus `Thread.sleep`;
10. cancellable CPU loop;
11. cancellation-safe exception handling;
12. parent-child cancellation;
13. ViewModel-owned coroutine;
14. `runTest` with virtual time.

Examples avoid `GlobalScope`, undocumented runtime internals, fixed thread
guarantees, and advanced supervision implementation.

## Exact item counts

- Package files: exactly 6.
- Numbered theory sections: exactly 22.
- Kotlin code blocks in theory: exactly 14.
- Practice exercises: exactly 4.
- Interview questions: exactly 22.
- Test questions: exactly 10.
- Official references: exactly 8.

## Metadata and taxonomy audit

- ID/path: `kotlin-coroutines-foundations`.
- Track/section: `kotlin` / `coroutines`.
- Difficulty/status: `foundation` / `review`.
- Estimated time/content version: 180 minutes / 1.
- Prerequisites: three existing review-stage topics.

The current schema explicitly permits `kotlin` as a track and accepts
`coroutines` as a kebab-case section, so no taxonomy adaptation or schema
change was required.

## Validation

```text
python -B scripts/validate_content.py
PASS — 7 topic packages, 2 templates, 4 schema fixtures

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

Advanced structured concurrency, supervision and partial-failure policy, deep
Flow mechanics, durable application work ownership, human editorial acceptance
or publication, production mappings, remaining MVP topics, catalog generation,
CI, clients, database-backed learner state, and AI tutor services remain
deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/kotlin/coroutines/kotlin-coroutines-foundations/cheat-sheet.md
 A content/kotlin/coroutines/kotlin-coroutines-foundations/interview.md
 A content/kotlin/coroutines/kotlin-coroutines-foundations/practice.md
 A content/kotlin/coroutines/kotlin-coroutines-foundations/test.yaml
 A content/kotlin/coroutines/kotlin-coroutines-foundations/theory.md
 A content/kotlin/coroutines/kotlin-coroutines-foundations/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-019-kotlin-coroutines-foundations-implementation.md
 A tasks/019-add-kotlin-coroutines-foundations-topic.md
?? 019-codex-prompt.md
?? 019-review.diff
```

## Recommended commit message

```text
feat(content): add Kotlin coroutines foundations topic
```
