# Task 025 — Android Testing Foundations implementation report

## Implementation summary

**PASS**

Task 025 adds the thirteenth production educational topic in `review`. It
teaches Android testing as a risk-based confidence strategy: architecture
defines seams, each test owns a specific risk, the smallest reliable boundary
is preferred, and higher-level tests protect real integration or
user-observable behavior.

## Changed files

Created the six canonical files under
`content/android/testing/android-testing-foundations/` and this report. Updated
`README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and Task 025 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test-infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the version 2 canonical
Android app architecture competency set, all twelve preceding production
topics, and Tasks 016–024 were inspected.

Primary canonical coverage:

- `apply-separation-of-concerns`;
- `design-viewmodel-ui-state`;
- `use-coroutines-and-flows-across-layers`.

Strongly reinforced:

- `design-data-layer-around-repositories`;
- `evaluate-optional-domain-layer`;
- `handle-compose-lifecycle-work`;
- `select-ui-state-holders-by-scope`.

UI-layer responsibilities, UDF, and Android-framework isolation are
contextually reinforced. No competency or production competency-to-topic
mapping changed.

Current official Android Developers, JUnit 4, Kotlin coroutine testing, and
primary OkHttp documentation was inspected for test strategy and doubles,
local versus instrumented environments, coroutine and Flow testing, Compose
semantics, Espresso synchronization, Navigation tests, Room tests, Hilt
replacement, and mock-server behavior. All 17 metadata references are official
or primary documentation and use the actual inspection date `2026-07-24`. Stable testing
principles are distinguished from version-sensitive framework APIs.

## Test-boundary audit

Unit, integration, component, UI, instrumentation, and end-to-end concepts are
distinguished. Scope is independent from execution environment: local is not a
synonym for unit, and instrumented is not a synonym for integration or
end-to-end.

The topic treats the test pyramid as portfolio guidance rather than a quota.
Every boundary decision starts from the failure risk and chooses the least
expensive boundary that still contains the real behavior. Pure mapping remains
local; HTTP, Room, Navigation, lifecycle, and UI semantics receive real
boundary evidence only where required.

## Doubles and architecture audit

Dummy, stub, fake, spy, and mock roles are defined while acknowledging
framework terminology differences. Stateful fakes are preferred for coherent
repository, cache, Flow, and navigation behavior. Interaction verification is
reserved for interactions that form the public contract.

Testability follows explicit constructors, repository and platform seams, pure
transformations, controlled clocks/randomness/dispatchers, and owned
asynchronous work. The topic rejects interface ceremony, static lookup,
production test-mode branches, process-global fakes, private-method tests, and
verification of every implementation call.

## Coroutine and Flow determinism audit

`runTest`, `TestScope`, a single shared `TestCoroutineScheduler`,
`StandardTestDispatcher`, deliberate `UnconfinedTestDispatcher`,
`runCurrent`, `advanceTimeBy`, and `advanceUntilIdle` are explained with their
scheduling roles. Virtual time is not claimed to accelerate blocking I/O.

Main replacement and dispatcher injection are separate seams. Every example
owns, awaits, cancels, or places indefinite work in `backgroundScope`.
Cancellation tests use `cancelAndJoin` and `finally`; no broad catch or ordinary
`runCatching` swallows `CancellationException`.

Cold finite Flow uses bounded terminal operations. StateFlow tests account for
conflation, and `stateIn(WhileSubscribed)` starts a collector before upstream
emission. SharedFlow tests define subscriber timing and bound infinite
collection. Optional Turbine use is not required or treated as changing Flow
semantics.

## ViewModel and repository audit

ViewModel tests cover initial state, public actions, state transitions,
controlled Main execution, cancellation, and `SavedStateHandle` inputs without
starting an Activity. Constructing a `SavedStateHandle` is explicitly not
presented as proof of operating-system process recreation.

Repository tests use deterministic remote/local fakes and controlled clocks for
cache, freshness, refresh, mapping, persistence, error, source-of-truth, and
cancellation policy. Pure mapping, mock-server HTTP, and real Room/SQLite tests
own separate adapter risks. Routine tests do not call a production backend.

## UI, navigation, and lifecycle audit

Navigation intent is tested through callbacks or a recording navigator.
Graph, route, result, deep-link, and back-stack behavior uses the current test
navigation controller only when actual navigation mechanics are the risk.

Compose tests use user-facing semantics, with merged/unmerged trees and test
tags described deliberately. Espresso uses matcher/action/assertion and
synchronizes known main-queue work plus registered idling resources. Unknown
background work requires a deterministic fake or explicit synchronization
boundary, never a real sleep.

Activity recreation, lifecycle state changes, Fragment View recreation,
navigation removal, task loss, and process death remain separate. The report
and topic do not claim that `ActivityScenario.recreate()` tests process death.

## Flakiness and isolation audit

The topic audits wall-clock time, real network, shared state, order dependence,
animation, races, unstable selectors, random/locale inputs, unclosed resources,
and asynchronous work without ownership. Theory shows the mandated sleep
anti-pattern only as a commented line; assessment shows it solely as broken
code to diagnose. No repository test executes a real sleep.

Every test should own a fresh graph, mutable fake, database, server, scenario,
clock/seed, and collector. Main, rules, idling resources, databases, servers,
and scenarios are reset or closed. Hilt replacement does not imply that
mutable fake state is automatically reset.

Snapshot/golden tests are limited to visual-regression evidence and are not
presented as proof of accessibility, interaction, navigation, or business
correctness.

## Junior Core progress audit

Junior Core status after Task 025:
13 of 17 mandatory topics implemented as production packages in review.
4 mandatory topics remain.

The remaining mandatory topics are:

14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grading schema, production mapping, or catalog
output was introduced.

## Exact counts

- Package files: 6.
- Numbered theory sections: 26.
- Meaningful Kotlin code blocks/categories in theory: 29.
- Practice exercises: 4.
- Interview questions: 26.
- Test questions: 10.
- Official/primary references: 17.
- Taxonomy: `android` / `testing`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 240 minutes.
- Prerequisites: 12.
- Production topic packages after Task 025: 13.
- Mandatory Junior Core topics remaining: 4.

The preferred taxonomy, metadata, and prerequisites are schema-valid. The
prerequisite graph remains acyclic.

## Validation

```text
python -B scripts/validate_content.py
PASS — 13 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

## UTF-8 and mojibake audit

All 12 new or modified repository Markdown/YAML source files decode as strict
UTF-8 without BOM. They contain none of the checked mojibake sequences. The new
topic and review diff contain no absolute local path.

## Deferred work

The four remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, and AI tutor remain deferred. The
dedicated Room, WorkManager, and Compose topics retain their full content scope.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/testing/android-testing-foundations/cheat-sheet.md
 A content/android/testing/android-testing-foundations/interview.md
 A content/android/testing/android-testing-foundations/practice.md
 A content/android/testing/android-testing-foundations/test.yaml
 A content/android/testing/android-testing-foundations/theory.md
 A content/android/testing/android-testing-foundations/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-025-android-testing-foundations-implementation.md
 A tasks/025-add-android-testing-foundations-topic.md
?? 025-codex-prompt.md
?? 025-review.diff
```

## Recommended commit message

```text
feat(content): add Android testing foundations topic
```
