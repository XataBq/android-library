# Task 018 — Android Lifecycle and State Restoration implementation report

## Final result

**PASS**

Task 018 adds the sixth production Android app architecture topic in `review`.
It teaches lifecycle and restoration as connected but separate concerns and
assigns state according to ownership, scope, size, durability, and
reconstructability.

## Files

Created the six canonical files under
`content/android/app-architecture/android-lifecycle-and-state-restoration/`
and this implementation report. Updated `README.md`,
`docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, two stale topic-count phrases in
`docs/ARCHITECTURE.md`, and Task 018 status.

No existing topic, source package, competency, learning sequence, mapping,
schema, validator, fixture, or test file changed.

## Source and evidence audit

Both imported Android Developers source packages were inspected.
`android-developers-app-architecture` supplies evidence for process
termination, keeping state out of Activities, persistent data models, and
configuration-change UI state. `android-developers-architecture-recommendations`
supplies lifecycle-aware UI collection, Compose lifecycle work, state-holder
scope, ViewModel state production, and framework-independent ViewModels.

Current official Android documentation was inspected for Activity and process
lifecycle, Fragment and Fragment View lifecycle, saved UI state, Saved State
Registry, `SavedStateHandle`, Compose saveable state, Fragment Result API,
Navigation back-stack results, Parcelables, Bundles, and Binder transaction
limits. All nine metadata references are official Android Developers pages and
use the actual inspection date `2026-07-24`; no access date was fabricated.

The content does not claim that `onDestroy` is guaranteed, that ViewModel
survives process death, that saved state is durable persistence, or that a
simple recreation test fully simulates an OS process kill.

## Canonical competency coverage

Primary:

- `explain-android-component-lifecycle-constraints`;
- `handle-compose-lifecycle-work`.

Strongly reinforced:

- `design-viewmodel-ui-state`;
- `select-ui-state-holders-by-scope`;
- `explain-persistent-data-models`;
- `isolate-android-framework-dependencies`.

Contextually reinforced:

- `explain-ui-layer-responsibilities`;
- `explain-unidirectional-data-flow`;
- `design-data-layer-around-repositories`.

No competency or production competency-to-topic mapping was created or
modified.

## Lifecycle-scenario audit

Theory explicitly distinguishes:

- configuration change, which recreates UI while a correctly scoped ViewModel
  can be retained for the same logical owner;
- a destination remaining on the back stack, where its View can be destroyed
  while its entry and scoped state remain;
- navigation removal, which destroys the entry and clears its scoped
  ViewModels;
- explicit `finish()`, which permanently ends the Activity owner;
- background process termination, which removes all in-memory objects without
  guaranteeing `onDestroy`;
- later process recreation, which creates new objects and may restore eligible
  small state.

Activity, Fragment, and Fragment View lifecycles have separate ownership
explanations. Binding, observers, and collectors are tied to
`viewLifecycleOwner`, with a broken/corrected binding example and a
`repeatOnLifecycle` collection example.

## State-placement audit

The topic uses the following responsibility model:

- View or `remember` for ephemeral rendering state;
- View saved state or `rememberSaveable` for small recreatable UI details;
- ViewModel for in-memory screen presentation state;
- `SavedStateHandle` for small process-recreatable inputs used by ViewModel
  logic;
- Repository or persistent storage for authoritative and durable application
  data.

The placement matrix covers scroll position, expanded state, route ID, filter,
unfinished form text, loaded profile, auth token, bitmap, repository cache,
and derived UiState. The process-recreation examples construct a new
ViewModel, restore compact inputs, reload current repository data, and rebuild
truthful presentation state.

## Bundle, Parcel, and Binder audit

The topic distinguishes Bundle as a typed key-value container, Parcel as an
Android marshaling representation, and Binder as the IPC transaction
mechanism. It explains that the Binder transaction buffer is limited and
shared by transactions in progress, so nested Bundles, arguments, View state,
navigation state, and saveable state can contribute to one aggregate failure.

Parcelable and Serializable are presented as encodings, not persistence
strategies or exceptions to size limits. Large objects, bitmaps, documents,
lists, and cached responses are redirected to Repository, database, file, or
cache ownership; only compact IDs, URIs, paths, and reconstruction inputs cross
Bundle-backed boundaries.

## Prerequisite and duplication audit

All five existing Android architecture topics are prerequisites. Content
validation confirms that every prerequisite exists and the graph is acyclic.

The new topic assumes prior UiState, StateFlow, ViewModel, UDF, Repository, and
optional Domain-layer knowledge. It does not repeat their full design
guidance. It deepens only component and View lifetimes, saved-state mechanics,
process reconstruction, back-stack ownership, result delivery, Bundle
transport, and restoration testing.

All five existing topic packages and their statuses are unchanged.

## Theory coverage

The 22 numbered theory sections cover:

1. lifecycle versus restoration;
2. Activity lifecycle;
3. Fragment lifecycle;
4. Fragment View lifecycle and `viewLifecycleOwner`;
5. lifecycle-aware Flow collection;
6. scenario comparison;
7. configuration change;
8. navigation removal and explicit finish;
9. process termination and recreation;
10. `onSaveInstanceState`;
11. Saved State Registry;
12. `SavedStateHandle`;
13. View hierarchy and custom View state;
14. Compose `remember`, `rememberSaveable`, and `Saver`;
15. ViewModel reconstruction;
16. navigation back-stack ownership;
17. Fragment Result API and alternatives;
18. Bundle, Parcel, and Binder;
19. transaction limits;
20. Parcelable versus Serializable;
21. state placement;
22. testing and anti-patterns.

## Kotlin example audit

Theory contains exactly 11 Kotlin code blocks:

1. broken Fragment binding and Fragment-lifecycle observation;
2. corrected binding lifetime and `viewLifecycleOwner`;
3. Flow collection with `viewLifecycleOwner` and `repeatOnLifecycle`;
4. `SavedStateHandle` with route ID and small filter;
5. custom View `BaseSavedState` skeleton;
6. `remember` versus `rememberSaveable`;
7. custom Compose `Saver`;
8. new-ViewModel reconstruction from saved input plus Repository data;
9. Fragment Result API;
10. Navigation previous-entry saved-state result and one-time consumption;
11. reconstruction test with a new `SavedStateHandle` and Repository reload.

The examples avoid repositories, Views, Context, and NavController in saved
state; large Bundle payloads; and undocumented internal APIs.

## Exact item counts

- Package files: exactly 6.
- Numbered theory sections: exactly 22.
- Kotlin code blocks in theory: exactly 11.
- Practice exercises: exactly 4.
- Interview questions: exactly 22.
- Test questions: exactly 10.
- Official references: exactly 9.

## Metadata and reference audit

- ID/path: `android-lifecycle-and-state-restoration`.
- Difficulty/status: `foundation` / `review`.
- Estimated time/content version: 180 minutes / 1.
- Prerequisites: all five existing Android architecture topics.
- References: 9 current official Android Developers pages.

The package contains exactly the six canonical files. No extra package file,
production mapping, catalog entry, or publication artifact was created.

## Validation

```text
python -B scripts/validate_content.py
PASS — 6 topic packages, 2 templates, 4 schema fixtures

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

Human editorial acceptance or publication, production mappings, additional
topics toward the 10–15-topic MVP, catalog generation, link automation, CI,
web and Android clients, database-backed learner state, and AI tutor services
remain deferred.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/app-architecture/android-lifecycle-and-state-restoration/cheat-sheet.md
 A content/android/app-architecture/android-lifecycle-and-state-restoration/interview.md
 A content/android/app-architecture/android-lifecycle-and-state-restoration/practice.md
 A content/android/app-architecture/android-lifecycle-and-state-restoration/test.yaml
 A content/android/app-architecture/android-lifecycle-and-state-restoration/theory.md
 A content/android/app-architecture/android-lifecycle-and-state-restoration/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-018-android-lifecycle-and-state-restoration-implementation.md
 A tasks/018-add-lifecycle-and-state-restoration-topic.md
?? 018-codex-prompt.md
?? 018-review.diff
```

## Recommended commit message

```text
feat(content): add Android lifecycle and state restoration topic
```
