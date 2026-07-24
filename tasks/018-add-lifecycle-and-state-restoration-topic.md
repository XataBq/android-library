# Task 018 — Add Android Lifecycle and State Restoration Topic

Status: DONE

## Objective

Add the sixth production educational topic in the Android app architecture track:

```text
android-lifecycle-and-state-restoration
```

The topic must explain how Android UI components are created, destroyed, recreated, and restored, and how state responsibilities are divided among:

- Activity and Fragment lifecycle;
- Fragment view lifecycle;
- View state;
- Compose state;
- `savedInstanceState`;
- Saved State Registry;
- `SavedStateHandle`;
- ViewModel;
- Repository and persistent storage;
- navigation back stack;
- Binder/Bundle transport boundaries.

The topic must distinguish:

```text
configuration change
navigation removal
explicit finish
background process termination
process recreation
```

The learner must understand that these are different events with different consequences.

This task belongs to:

```text
Phase 3 — Learning Content MVP
```

It extends the current architecture sequence after:

1. `android-app-architecture-foundations`
2. `android-ui-layer-and-unidirectional-data-flow`
3. `android-data-layer-repositories-and-synchronization`
4. `android-domain-layer-and-use-cases`
5. `android-viewmodel-and-ui-state`

The new package must remain in `review`.

---

## Core teaching position

The central responsibility model is:

```text
Ephemeral rendering state
→ View / remember

Recreatable UI state
→ saved instance state / SavedStateRegistry / rememberSaveable

Screen in-memory state
→ ViewModel

Small process-recreatable screen inputs
→ SavedStateHandle

Authoritative or durable application data
→ Repository / persistent storage
```

The topic must make clear:

- ViewModel survives configuration changes, not process death;
- saved-state APIs restore small serializable state, not arbitrary object graphs;
- Repository or persistent storage remains authoritative for durable data;
- Fragment and Fragment view have distinct lifecycles;
- UI lifecycle collection belongs to the UI layer;
- Bundle size is constrained by Binder transaction behavior;
- no saved-state mechanism should become a substitute for correct data ownership.

---

## Source-of-truth requirements

Before authoring, inspect:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_VALIDATION.md`
- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`
- all relevant content-authoring documentation;
- the canonical Android app architecture competency package;
- both imported Android Developers source packages;
- all current production topic packages;
- relevant review and normalization records;
- the implementation and final form of Task 017.

At minimum inspect evidence relevant to:

- `explain-android-component-lifecycle-constraints`;
- `design-viewmodel-ui-state`;
- `select-ui-state-holders-by-scope`;
- `handle-compose-lifecycle-work`;
- `explain-persistent-data-models`;
- `isolate-android-framework-dependencies`.

Use official Android documentation for lifecycle, saved state, Fragment, Compose state restoration, navigation saved state, `SavedStateHandle`, and Binder limits where repository evidence is insufficient.

Do not silently invent details about internal framework behavior.

Do not fabricate access dates.

---

## Canonical competency scope

Primary:

```text
explain-android-component-lifecycle-constraints
handle-compose-lifecycle-work
```

Strongly reinforced:

```text
design-viewmodel-ui-state
select-ui-state-holders-by-scope
explain-persistent-data-models
isolate-android-framework-dependencies
```

Contextually reinforced:

```text
explain-ui-layer-responsibilities
explain-unidirectional-data-flow
design-data-layer-around-repositories
```

Do not modify competency files.

Do not create a production competency-to-topic mapping in this task.

---

## Package location

Create exactly:

```text
content/android/app-architecture/android-lifecycle-and-state-restoration/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

---

## Topic metadata

Use:

```yaml
id: android-lifecycle-and-state-restoration
title: Android Lifecycle and State Restoration
track: android
section: app-architecture
difficulty: foundation
status: review
estimated_minutes: 180
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-ui-layer-and-unidirectional-data-flow
  - android-data-layer-repositories-and-synchronization
  - android-domain-layer-and-use-cases
  - android-viewmodel-and-ui-state
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The final topic must cover outcomes equivalent to:

1. Distinguish Activity lifecycle, Fragment lifecycle, and Fragment view lifecycle.
2. Explain why lifecycle is not a simple linear callback sequence.
3. Distinguish configuration change, navigation removal, explicit finish, and process death.
4. Explain what survives each lifecycle scenario.
5. Use `viewLifecycleOwner` correctly for Fragment UI observers and collectors.
6. Explain the purpose and limits of `onSaveInstanceState`.
7. Explain the role of Saved State Registry.
8. Use `SavedStateHandle` for small recoverable state and route inputs.
9. Distinguish ViewModel retention from process-state restoration.
10. Explain how View state is automatically saved and restored.
11. Explain `remember`, `rememberSaveable`, `Saver`, and Compose saveable state.
12. Decide which state belongs in View/Compose, ViewModel, SavedStateHandle, or Repository.
13. Explain navigation back-stack ownership and scoped ViewModels.
14. Compare Fragment Result API, shared ViewModel, and navigation saved-state result patterns.
15. Explain Bundle, Parcel, and Binder responsibilities at a practical level.
16. Explain why Binder transaction limits can produce `TransactionTooLargeException`.
17. Distinguish `Parcelable` and `Serializable` without treating either as persistent storage.
18. Design a restoration flow after process recreation.
19. Test recreation and restoration behavior realistically.
20. Recognize lifecycle and saved-state anti-patterns.

Final wording must remain schema-compliant and source-supported.

---

## Theory requirements

`theory.md` must be a coherent guide with approximately 18–22 substantial sections.

### 1. Why lifecycle and restoration are separate problems

Explain:

- lifecycle controls when objects exist and are active;
- restoration controls what state can be reconstructed;
- ownership determines where state belongs;
- no single API solves all state problems.

### 2. Activity lifecycle

Cover:

- `onCreate`;
- `onStart`;
- `onResume`;
- `onPause`;
- `onStop`;
- `onDestroy`.

Explain:

- callbacks are state transitions, not business guarantees;
- lifecycle can move backward and forward;
- `onDestroy` is not guaranteed before process death;
- expensive or durable persistence must not depend on a final callback.

### 3. Fragment lifecycle

Explain:

- Fragment instance lifecycle;
- attachment and detachment;
- creation and destruction;
- relationship to FragmentManager;
- why Fragment may exist while its View does not.

### 4. Fragment view lifecycle

This must be a major section.

Explain:

- `onCreateView`;
- `onViewCreated`;
- `onDestroyView`;
- `viewLifecycleOwner`;
- binding lifetime;
- observers and collectors tied to view lifecycle;
- why using Fragment lifecycle for View-bound work can leak or update a destroyed View.

Include a broken example and correction.

### 5. Lifecycle scenarios compared

Provide a matrix for:

```text
configuration change
navigation removal
explicit finish
background process kill
process recreation
```

For each, compare:

- Activity/Fragment instance;
- Fragment View;
- ViewModel;
- in-memory state;
- saved state;
- persistent data.

### 6. Configuration change

Explain:

- old UI instance is destroyed;
- a new instance is created;
- ViewModel can be retained by the same logical owner;
- View/Compose state may be restored;
- resources/configuration can change;
- UI must re-render from current state.

### 7. Navigation removal and permanent owner destruction

Explain:

- leaving a destination can destroy its owner;
- scoped ViewModel is then cleared;
- back-stack behavior depends on whether the entry remains;
- navigation away is not the same as configuration change.

### 8. Process death

Explain:

```text
process memory disappears
→ ViewModels disappear
→ Activities and Fragments disappear
→ a new process may later recreate UI
→ small saved state is restored
→ authoritative data is reloaded
```

State clearly that ViewModel does not survive process death.

### 9. `onSaveInstanceState`

Explain:

- purpose;
- timing constraints;
- why it is not a guaranteed final persistence callback;
- what types fit;
- what should not be stored;
- why large data is dangerous;
- relationship to framework restoration.

Do not promise callback timing guarantees not supported by documentation.

### 10. Saved State Registry

Explain:

- providers register state;
- restored state is consumed later;
- Activity, Fragment, Navigation, and ViewModel integrations build on saved-state infrastructure;
- use the public model, not undocumented internals.

### 11. SavedStateHandle

Explain:

- route arguments;
- IDs;
- filters;
- small user input;
- process recreation;
- integration with ViewModel;
- what not to store;
- why Repository remains authoritative.

Include a conceptually compilable example.

### 12. View state restoration

Explain:

- automatic View hierarchy state;
- stable View IDs;
- built-in widgets;
- custom View state;
- `BaseSavedState`;
- why arbitrary business data should not be placed in View state.

### 13. Compose state restoration

Explain:

- recomposition;
- `remember`;
- configuration recreation;
- `rememberSaveable`;
- `Saver`;
- saveable state limits;
- `SaveableStateRegistry`;
- navigation destination state;
- why saveable state is not durable persistence.

Include one realistic Compose example.

### 14. ViewModel and restoration

Connect:

```text
ViewModel
SavedStateHandle
saved instance state
Saved State Registry
Repository
```

Explain:

- ViewModel retains in-memory screen state across configuration change;
- new ViewModel is created after process recreation;
- SavedStateHandle reconstructs small inputs;
- Repository reloads authoritative data;
- UiState is rebuilt.

### 15. Navigation back stack and state ownership

Explain:

- back-stack entry as owner;
- destination-scoped ViewModel;
- graph-scoped ViewModel;
- state retained while an entry remains;
- result delivery;
- recreation of navigation state;
- avoiding global shared state for destination-local concerns.

### 16. Fragment Result API and alternatives

Compare:

- Fragment Result API;
- shared ViewModel;
- navigation saved-state result;
- direct callback/interfaces where appropriate.

Explain:

- lifecycle-aware delivery;
- one-off results versus shared durable state;
- ownership and scope.

Do not prescribe one universal mechanism.

### 17. Bundle, Parcel, and Binder

Explain practically:

- Bundle is a typed key-value container;
- Parcel is an Android marshaling format;
- Binder transports data across process boundaries;
- Binder transaction limits apply to the transaction buffer;
- several values together can exceed the limit;
- `TransactionTooLargeException` is not only about one large extra.

Avoid unsupported implementation-detail claims.

### 18. Parcelable versus Serializable

Explain:

- both serialize object state;
- Parcelable is Android-oriented and explicit;
- Serializable is Java serialization;
- performance and tooling considerations;
- neither is a persistence strategy;
- neither makes arbitrary large state safe.

### 19. State placement matrix

Include a practical table for examples such as:

- scroll position;
- expanded section;
- current route ID;
- filter input;
- unfinished form text;
- loaded profile;
- auth token;
- bitmap;
- repository cache;
- derived UiState.

Require reasoning based on ownership, size, durability, and reconstructability.

### 20. Testing recreation and restoration

Cover:

- Activity recreation;
- Fragment view recreation;
- `ActivityScenario.recreate()`;
- SavedStateHandle reconstruction;
- Compose state restoration tests;
- process-death-like tests;
- why recreation tests do not fully equal a real OS process kill;
- validating observable restoration behavior.

### 21. Common anti-patterns

At minimum cover:

- expecting ViewModel to survive process death;
- observing Fragment UI with Fragment lifecycle instead of view lifecycle;
- using binding after `onDestroyView`;
- persisting large objects in Bundle;
- storing repositories or services in SavedStateHandle;
- relying on `onDestroy`;
- duplicate collectors after recreation;
- storing Context/View/NavController;
- duplicating the same source of truth across ViewModel, Bundle, and Repository;
- using `remember` when restoration is required;
- using `rememberSaveable` for large or authoritative data;
- passing full objects through navigation instead of IDs.

### 22. Restoration decision checklist

End with a compact decision process based on:

- ownership;
- size;
- durability;
- reconstructability;
- scope;
- process survival requirement.

---

## Kotlin example requirements

Include at least:

1. Fragment binding lifecycle anti-pattern and correction;
2. lifecycle-aware Flow collection using `viewLifecycleOwner`;
3. `SavedStateHandle` with a route ID or small filter value;
4. ViewModel restoration flow after process recreation;
5. `remember` versus `rememberSaveable`;
6. custom `Saver` example;
7. custom View saved state example or concise skeleton;
8. Fragment Result API example;
9. navigation saved-state result example where supported;
10. a test or reconstruction example for state restoration.

Avoid:

- large production frameworks;
- fake undocumented internals;
- storing repositories or View objects in saved state;
- huge Bundle payloads;
- claiming real process-death coverage from a simple recreation test.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and contain:

- lifecycle callback summary;
- Activity vs Fragment vs Fragment view lifecycle;
- configuration change vs process death;
- ViewModel vs SavedStateHandle vs Repository;
- saved-state placement guide;
- View and Compose restoration rules;
- Fragment Result API comparison;
- Bundle/Parcel/Binder summary;
- Parcelable vs Serializable;
- `TransactionTooLargeException` checklist;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — State placement

Given a realistic screen with:

- route ID;
- loaded entity;
- scroll position;
- filter text;
- bitmap;
- unsent form input;
- auth state;
- derived UiState;

assign each item to:

- View/Compose state;
- ViewModel;
- SavedStateHandle;
- Repository/persistent storage.

Require justification.

### Exercise 2 — Broken Fragment lifecycle

Provide a Fragment with:

- binding retained after `onDestroyView`;
- collector launched against Fragment lifecycle;
- repeated collection;
- UI updates after View destruction.

Require diagnosis and corrected code.

### Exercise 3 — Process recreation design

Design restoration for a form-driven screen after process death.

Require:

- what is saved;
- what is reloaded;
- how a new ViewModel reconstructs state;
- how errors are handled;
- what is deliberately not restored.

### Exercise 4 — TransactionTooLargeException review

Provide a scenario with:

- large Parcelable;
- image bytes;
- nested Bundle;
- navigation arguments;
- saved state.

Require:

- identify likely causes;
- redesign transport;
- move large data to Repository/cache/file storage;
- preserve exact IDs and minimal restoration state.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints separated from the solution path.

Do not include complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 18–22 substantial questions.

Cover:

- Activity lifecycle;
- Fragment lifecycle;
- Fragment view lifecycle;
- `viewLifecycleOwner`;
- configuration change;
- process death;
- `onSaveInstanceState`;
- Saved State Registry;
- `SavedStateHandle`;
- View state;
- `remember`;
- `rememberSaveable`;
- `Saver`;
- ViewModel restoration;
- navigation back stack;
- Fragment Result API;
- Bundle;
- Parcel;
- Binder;
- transaction limits;
- Parcelable;
- Serializable;
- testing restoration.

For each question include:

- what a strong answer should cover;
- common weak or incorrect answers;
- follow-ups where appropriate.

Do not reward memorized lifecycle callback sequences without ownership reasoning.

---

## Test requirements

`test.yaml` must contain exactly 10 questions.

Required coverage:

1. Fragment lifecycle vs Fragment view lifecycle;
2. configuration change;
3. process death;
4. ViewModel vs SavedStateHandle;
5. `onSaveInstanceState`;
6. Compose `remember` vs `rememberSaveable`;
7. state placement;
8. Fragment Result API/shared ViewModel/navigation result;
9. Binder transaction limit;
10. end-to-end restoration architecture scenario.

Questions must test reasoning.

Distractors must be plausible.

Explanations must teach the architectural reason.

---

## References

Use official Android references and repository-supported evidence.

At minimum inspect official guidance for:

- Activity lifecycle;
- Fragment lifecycle;
- saving UI state;
- Saved State module;
- ViewModel saved state;
- Compose state and state restoration;
- navigation state;
- Fragment Result API;
- Parcelables and Bundles;
- Binder transaction limits.

Use current official URLs.

Do not fabricate access dates.

Follow repository metadata conventions.

---

## Android connections

Metadata should include Android-specific connections equivalent to:

- Activity, Fragment, and Fragment View lifecycles have different ownership boundaries.
- ViewModel retains in-memory screen state through configuration change but not process death.
- SavedStateHandle and saved-state APIs restore small reconstructable state.
- Repository and persistent storage own authoritative or durable data.
- Compose and View-based state use different restoration APIs but share the same ownership principles.
- Binder transaction size constrains Bundle-based state transport.

Final wording must remain source-supported.

---

## Relationship to existing topics

Do not duplicate full explanations from:

- ViewModel and UI State;
- UI Layer and UDF;
- Data Layer;
- Domain Layer.

Assume learners already understand:

- ViewModel as a screen state holder;
- StateFlow and UiState;
- Repository ownership;
- lifecycle-aware collection at a basic level.

This topic must deepen lifecycle and restoration mechanics.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 018 as completed only after validation;
- record the sixth production topic in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- state that six production topics now form the growing Android architecture foundation;
- do not claim the 10–15-topic target is complete;
- do not create production mappings;
- do not create a catalog;
- do not promote existing topics;
- do not claim CI, web, Android client, database, AI tutor, or publication exists.

Update `docs/ARCHITECTURE.md` only if an explicit topic count or list would otherwise become stale.

---

## Implementation report

Create the repository-standard implementation report.

Include:

1. implementation summary;
2. files created and changed;
3. source and evidence audit;
4. canonical competency coverage;
5. lifecycle-scenario audit;
6. state-placement audit;
7. Bundle/Parcel/Binder audit;
8. prerequisite and duplication audit;
9. theory coverage;
10. Kotlin example audit;
11. exact exercise count;
12. exact interview-question count;
13. exact test-question count;
14. metadata and reference audit;
15. validation results;
16. UTF-8 and mojibake audit;
17. deferred work;
18. literal `git status --short`;
19. recommended commit message.

---

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Also verify:

- exactly six files exist in the new package;
- exactly four exercises;
- exactly ten test questions;
- interview count is within range;
- topic ID and directory match;
- all prerequisites exist;
- no prerequisite cycle;
- references are valid;
- UTF-8;
- no mojibake;
- no absolute local paths;
- no source, competency, sequence, mapping, schema, validator, test, or existing-topic data changed;
- no package status outside the new topic changed;
- only allowed documentation and report files changed.

---

## Acceptance criteria

- The six-file package exists.
- Metadata conforms to schema.
- Status is `review`.
- Content version is `1`.
- Five existing architecture topics are prerequisites.
- Activity, Fragment, and Fragment View lifecycles are distinguished.
- Configuration change, navigation removal, finish, and process death are distinguished.
- ViewModel retention and process restoration are not conflated.
- `onSaveInstanceState`, Saved State Registry, and SavedStateHandle are explained.
- View and Compose restoration are covered.
- `remember` and `rememberSaveable` are distinguished.
- State placement is responsibility-based.
- Navigation back-stack ownership is covered.
- Fragment Result API is compared with alternatives.
- Bundle, Parcel, Binder, Parcelable, and Serializable are explained accurately.
- Binder transaction limits and `TransactionTooLargeException` are covered.
- Testing limitations are explicit.
- Theory includes realistic Kotlin examples.
- Cheat sheet is independently useful.
- Practice contains exactly 4 exercises.
- Interview material is substantial.
- Test contains exactly 10 reasoning-focused questions.
- Existing topics are not substantially duplicated.
- Project documentation is synchronized.
- All validations pass.
- Task becomes `DONE` only after validation succeeds.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source and evidence audit;
4. canonical coverage;
5. lifecycle and restoration audit;
6. Bundle/Parcel/Binder audit;
7. content and duplication audit;
8. exact section and item counts;
9. validation results;
10. UTF-8 audit;
11. deferred work;
12. literal `git status --short`;
13. recommended commit message.

Do not commit.
