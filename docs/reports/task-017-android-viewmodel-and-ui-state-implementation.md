# Task 017 — Android ViewModel and UI State implementation report

## Final result

**PASS**

Task 017 adds the fifth production Android app architecture topic in `review`.
It presents ViewModel as a scoped screen-level state holder and UI-scenario
coordinator, not merely a rotation survivor or global container.

## Files

Created the six canonical files under
`content/android/app-architecture/android-viewmodel-and-ui-state/` and this
implementation report. Updated `README.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, two stale topic-count phrases in `docs/ARCHITECTURE.md`, and
Task 017 status.

## Source and evidence audit

Imported `android-developers-architecture-recommendations` evidence supports:

- conditional use of ViewModel to expose UI state and coordinate UI logic;
- screen-level or explicitly scoped complex-UI ViewModels;
- plain state holders for reusable UI;
- StateFlow plus `stateIn`/`WhileSubscribed` construction choices;
- lifecycle-aware UI collection;
- Flow and suspending calls across ViewModel boundaries;
- framework-independent ViewModels.

Current official Android and Kotlin documentation was inspected for
ViewModelStoreOwner lifetime, configuration change, process death,
SavedStateHandle, stateIn, SharingStarted, and lifecycle-aware collection.
Existing repository URLs and access dates were reused; newly inspected official
ViewModel, SavedStateHandle, and Kotlin stateIn pages use the actual review date
`2026-07-24`.

## Canonical coverage

Primary:

- `design-viewmodel-ui-state`;
- `select-ui-state-holders-by-scope`;
- `handle-compose-lifecycle-work`.

Reinforced without redefining:

- `explain-ui-layer-responsibilities`;
- `explain-unidirectional-data-flow`;
- `explain-android-component-lifecycle-constraints`;
- `use-coroutines-and-flows-across-layers`;
- `isolate-android-framework-dependencies`;
- `explain-persistent-data-models`.

No competency or production mapping was created or modified.

## Prerequisite and duplication audit

All four existing Android architecture topics are prerequisites. The validated
graph is acyclic. The new topic assumes UDF, Repository, and optional Domain
fundamentals and deepens only ViewModel-specific scope, state construction,
Flow sharing, lifecycle collection, recovery, navigation boundaries, and
testing.

## Theory and Kotlin audit

- Package files: exactly 6.
- Numbered theory sections: exactly 20.
- Kotlin code blocks in theory: exactly 13.
- Practice exercises: exactly 4.
- Interview questions: exactly 20.
- Test questions: exactly 10.

Examples cover private mutable/public immutable StateFlow, atomic `update`,
latest-wins state converted with `stateIn`, explicit actions, state-based
outcomes and a SharedFlow alternative, SavedStateHandle recovery, duplicate
collector correction, lifecycle-aware Compose collection, and a coroutine-aware
fake-based test. A dedicated `combine(...).stateIn(...)` example builds one
coherent dashboard snapshot from independent profile and message repository
Flows while preserving repository data ownership, ViewModel presentation-state
ownership, a truthful loading `initialValue`, and the warning not to combine
unrelated UI concerns mechanically.

The topic excludes `GlobalScope`, retained Activity/Fragment/View/NavController
objects, public mutable state, direct Retrofit/DAO ownership, arbitrary Context,
mandatory Hilt, universal wrappers, and ViewModel-as-event-bus design.

## Metadata and references

- ID/path: `android-viewmodel-and-ui-state`.
- Difficulty/status: `foundation` / `review`.
- Estimated time/content version: 180 minutes / 1.
- Prerequisites: all four existing Android architecture topics.
- References: 8 official Android Developers or Kotlin documentation pages.

## Validation

```text
python -B scripts/validate_content.py
PASS — 5 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

All new and modified Markdown/YAML files decode as strict UTF-8 without BOM and
contain none of the checked mojibake sequences. No absolute local path exists
in the new topic package.

## Deferred work

Editorial acceptance or publication, production mappings, deeper lifecycle and
state-restoration material, coroutine foundations, catalog generation, CI,
clients, database, and AI services remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/app-architecture/android-viewmodel-and-ui-state/cheat-sheet.md
 A content/android/app-architecture/android-viewmodel-and-ui-state/interview.md
 A content/android/app-architecture/android-viewmodel-and-ui-state/practice.md
 A content/android/app-architecture/android-viewmodel-and-ui-state/test.yaml
 A content/android/app-architecture/android-viewmodel-and-ui-state/theory.md
 A content/android/app-architecture/android-viewmodel-and-ui-state/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-017-android-viewmodel-and-ui-state-implementation.md
 A tasks/017-add-viewmodel-and-ui-state-topic.md
?? 017-codex-prompt.md
?? 017-review.diff
```

## Recommended commit message

```text
feat(content): add Android ViewModel and UI state topic
```
