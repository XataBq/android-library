# Task 017 — Add Android ViewModel and UI State Topic

Status: DONE

## Objective

Add the fifth production educational topic in the Android app architecture track:

```text
android-viewmodel-and-ui-state
```

The topic must explain ViewModel as a screen-level state holder and UI-scenario coordinator, including:

- ownership and scope;
- UI state design;
- state versus events;
- StateFlow and other Flow-based contracts;
- lifecycle-aware collection;
- configuration changes;
- process death;
- SavedStateHandle;
- coroutine ownership;
- navigation and error presentation boundaries;
- shared state;
- ViewModel testing.

The topic must not reduce ViewModel to the slogan:

> “It survives screen rotation.”

Instead, it must provide a complete responsibility and lifecycle model.

This task belongs to:

```text
Phase 3 — Learning Content MVP
```

It extends the current architecture content foundation after:

1. `android-app-architecture-foundations`
2. `android-ui-layer-and-unidirectional-data-flow`
3. `android-data-layer-repositories-and-synchronization`
4. `android-domain-layer-and-use-cases`

The new package must remain in `review`.

---

## Core teaching position

The central model is:

```text
Repositories / Use cases
        ↓
ViewModel
        ↓
UiState
        ↓
UI renders state

UI actions
        ↓
ViewModel
        ↓
state transition / application operation
```

A ViewModel is normally:

- owned by a ViewModelStoreOwner;
- scoped to a UI destination or deliberately shared scope;
- responsible for screen-level state and UI scenario coordination;
- independent from concrete Android View objects and UI lifecycle observation;
- recreated after process death;
- cleared when its owner is permanently removed.

A ViewModel is not automatically:

- a Repository;
- a global singleton;
- an application-wide event bus;
- an owner of Activity, Fragment, View, NavController, or Compose runtime objects;
- a guarantee of process-death survival;
- a container for unrelated feature logic;
- a replacement for persistent state.

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
- all existing production topic packages;
- relevant repository review and normalization records.

At minimum, inspect evidence relevant to:

- `explain-android-component-lifecycle-constraints`;
- `explain-ui-layer-responsibilities`;
- `design-viewmodel-ui-state`;
- `select-ui-state-holders-by-scope`;
- `handle-compose-lifecycle-work`;
- `explain-unidirectional-data-flow`;
- `use-coroutines-and-flows-across-layers`;
- `isolate-android-framework-dependencies`;
- `explain-persistent-data-models`.

The repository files are the primary source of truth.

Use outside official Android documentation only to clarify concepts not fully represented in the imported source packages. Clearly preserve the distinction between repository-supported claims and broader reference material.

Do not silently fill source gaps.

---

## Canonical competency scope

Primary competencies:

```text
design-viewmodel-ui-state
select-ui-state-holders-by-scope
handle-compose-lifecycle-work
```

Strongly reinforced:

```text
explain-ui-layer-responsibilities
explain-unidirectional-data-flow
explain-android-component-lifecycle-constraints
use-coroutines-and-flows-across-layers
isolate-android-framework-dependencies
```

Contextually reinforced:

```text
explain-persistent-data-models
apply-separation-of-concerns
evaluate-optional-domain-layer
```

Do not create new canonical competencies.

Do not modify competency files.

Do not create a production competency-to-topic mapping in this task.

---

## Package location

Create exactly:

```text
content/android/app-architecture/android-viewmodel-and-ui-state/
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
id: android-viewmodel-and-ui-state
title: Android ViewModel and UI State
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
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The final topic must cover outcomes equivalent to:

1. Explain why Android screens need state holders outside individual UI instances.
2. Explain how ViewModelStoreOwner scope determines ViewModel lifetime.
3. Distinguish configuration change, permanent owner removal, and process death.
4. Design a coherent immutable UiState contract.
5. Decide when one state object or several independent flows are appropriate.
6. Distinguish StateFlow, SharedFlow, Channel, and cold Flow by responsibility.
7. Decide whether a UI outcome should be represented as durable state or a transient event.
8. Model UI actions through explicit methods or an action contract.
9. Update state atomically and avoid inconsistent or stale state transitions.
10. Model initial loading, refreshing, content, empty state, partial failure, and terminal failure.
11. Use viewModelScope and structured concurrency without duplicate collectors or hidden work.
12. Convert cold upstream flows into state with appropriate sharing behavior.
13. Keep lifecycle-aware collection in the UI layer.
14. Use SavedStateHandle only for small recoverable state and route arguments.
15. Explain how screen restoration works after process death.
16. Keep ViewModel dependencies independent from Activity, Fragment, View, NavController, and mutable UI objects.
17. Model navigation and user-visible errors without leaking framework responsibilities.
18. Evaluate shared ViewModel scope versus repository-owned shared data.
19. Test observable ViewModel behavior with coroutine-aware fakes.
20. Recognize common ViewModel and UI-state anti-patterns.

Final wording must fit the schema and actual source support.

---

## Theory requirements

`theory.md` must be a coherent guide with approximately 18–22 substantial sections.

It must not become a disconnected API catalog.

### 1. The real purpose of ViewModel

Explain:

- Android UI instances can be recreated;
- the screen needs a stable state owner outside a particular Activity, Fragment, or composable instance;
- ViewModel retains in-memory state across configuration changes;
- ViewModel does not survive process death;
- ViewModel does not replace persistent storage or SavedStateHandle.

### 2. ViewModel ownership and lifetime

Explain:

- `ViewModelStore`;
- `ViewModelStoreOwner`;
- Activity scope;
- Fragment scope;
- shared Activity scope;
- navigation graph or destination scope;
- Compose `viewModel()` ownership;
- how incorrect scope causes premature state loss or excessive lifetime.

Avoid undocumented internal implementation claims unless cited and necessary.

### 3. Lifecycle scenarios

Compare clearly:

```text
configuration change
navigation away / owner removed
process death
application process lifetime
```

For each, explain what happens to:

- UI instance;
- ViewModel;
- in-memory state;
- SavedStateHandle;
- repository/persistent data.

### 4. What UI state is

Explain and distinguish:

- screen state;
- input state;
- derived presentation state;
- transient rendering state;
- domain data;
- persistent application data;
- navigation outcomes;
- one-time commands.

Use one realistic immutable state model.

### 5. Designing coherent UiState

Explain:

- immutable data classes or sealed states;
- consistent snapshots;
- impossible state combinations;
- derived properties;
- atomic updates;
- when sealed variants are clearer than booleans;
- when a single `isLoading` is insufficient.

Cover states equivalent to:

```text
initial loading
content
empty
refreshing over content
recoverable error
terminal error
partial content with warning
```

Do not require one universal state representation.

### 6. One UiState versus several flows

Provide criteria.

One state object is often useful when:

- properties form one screen snapshot;
- atomic consistency matters;
- the UI renders the whole screen from one contract.

Separate flows may be valid when:

- concerns are genuinely independent;
- data has different lifetimes or observation patterns;
- merging creates an artificial giant state.

Explain trade-offs involving:

- `combine`;
- derived state;
- invalid combinations;
- update coordination;
- state explosion.

### 7. StateFlow, SharedFlow, Channel, and cold Flow

Explain their responsibilities without oversimplifying.

#### StateFlow

Use for current observable state with a latest value.

#### SharedFlow

Use for multicast emissions when an event model is truly appropriate.

#### Channel

Explain queue-like producer/consumer behavior and why it is not an automatic UI-event default.

#### Cold Flow

Explain deferred upstream execution and collection-driven work.

Do not claim one primitive is universally correct.

### 8. State versus events

This must be a central section.

Discuss scenarios such as:

- Snackbar;
- navigation;
- payment completion;
- authentication required;
- validation error;
- retry prompt;
- dialog request.

Explain risks of transient event streams:

- missed emissions;
- multiple collectors;
- configuration change;
- duplicate handling;
- replay ambiguity;
- process recreation.

Explain when representing the outcome as state is more robust.

Also explain when an event stream remains justified.

Do not state that all events must become state.

### 9. UI actions and intent contracts

Compare:

```kotlin
fun retry()
fun save()
fun updateName(value: String)
```

with:

```kotlin
sealed interface ProfileAction
fun onAction(action: ProfileAction)
```

Explain:

- both are valid;
- action contracts help UDF/MVI-like screens;
- separate methods may be simpler;
- the public contract should remain cohesive and explicit.

### 10. Atomic state updates

Show:

```kotlin
_state.update { current ->
    current.copy(isLoading = true)
}
```

Explain:

- immutable state;
- stale reads;
- lost updates;
- concurrent actions;
- `update` versus read-then-assign;
- serializing or cancelling conflicting work when necessary.

Do not promise thread safety beyond what the selected primitive actually guarantees.

### 11. Loading, refresh, retry, and repeated work

Explain:

- initial load;
- user refresh;
- retry;
- idempotency;
- repeated collectors;
- duplicate requests;
- latest-wins behavior;
- preserving content during refresh;
- operation-specific loading flags.

Discuss when work belongs in `init` and when it should be triggered explicitly.

### 12. viewModelScope and structured concurrency

Explain:

- ownership of child coroutines;
- cancellation at `onCleared`;
- sibling failure behavior where relevant;
- exceptions;
- parallel work;
- latest-wins;
- storing Job references only when useful;
- avoiding GlobalScope and hidden unmanaged scopes.

Include an example of accidentally starting the same long-lived collector more than once and how to prevent it.

### 13. stateIn and sharing behavior

Include an example conceptually equivalent to:

```kotlin
val uiState = combine(
    repository.observeUser(),
    repository.observeSettings(),
) { user, settings ->
    ProfileUiState(user, settings)
}.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5_000),
    initialValue = ProfileUiState.Loading,
)
```

Explain:

- cold-to-hot conversion;
- initial state;
- `Eagerly`;
- `Lazily`;
- `WhileSubscribed`;
- subscriber disappearance;
- upstream restart;
- why a timeout may be used;
- why a specific timeout is not a universal rule.

### 14. Lifecycle-aware UI collection

Explain:

- ViewModel should not know whether Activity or Fragment is STARTED;
- ViewModel should not know whether a composable is currently in composition;
- UI owns lifecycle-aware collection;
- Compose may use `collectAsStateWithLifecycle`;
- View-based UI may use `repeatOnLifecycle`.

Do not imply collection APIs are interchangeable in every context.

### 15. SavedStateHandle

Explain:

- why it exists;
- route arguments;
- small recoverable user input;
- IDs and filters;
- process recreation;
- restoration limitations.

Do not store:

- large graphs;
- bitmaps;
- repositories;
- complex service objects;
- complete durable datasets;
- anything that should be loaded from the Data layer.

Connect:

```text
ViewModel
SavedStateHandle
saved instance state
Saved State Registry
```

without inventing undocumented internals.

### 16. Process death restoration

Show the lifecycle:

```text
Activity + ViewModel exist
→ process is killed
→ all in-memory objects disappear
→ new process starts
→ Activity is recreated
→ a new ViewModel is created
→ small saved state is restored
→ repositories reload authoritative data
```

Explain what is and is not restored.

### 17. Dependency boundaries

Reasonable ViewModel dependencies may include:

- repositories;
- use cases;
- saved-state contract;
- analytics abstraction;
- dispatcher abstraction only where justified.

Problematic dependencies include:

- Activity;
- Fragment;
- View;
- NavController;
- mutable Compose state owned by the UI;
- arbitrary Context;
- Service Locator calls inside the ViewModel.

Explain how presentation models or abstractions can avoid framework leakage.

### 18. Navigation

Explain:

- ViewModel may expose a navigation outcome;
- UI performs actual framework navigation;
- ViewModel should not own NavController;
- duplicate navigation;
- navigation after configuration change;
- state versus event trade-offs;
- deep-link or route arguments;
- result handling after returning.

Do not prescribe one universal navigation architecture.

### 19. Error presentation

Distinguish:

- transport errors;
- data errors;
- domain errors;
- validation errors;
- UI presentation decisions.

Cover:

- inline field errors;
- screen-level errors;
- content with warning;
- retryable errors;
- Snackbar/banner/dialog decisions;
- stable error contracts instead of leaking Retrofit or storage exceptions into UI.

### 20. Shared state across screens

Explain:

- Activity-scoped ViewModel;
- navigation-graph-scoped ViewModel;
- repository-owned shared data;
- when shared ViewModel is appropriate;
- when shared state belongs in Data layer;
- why a shared ViewModel must not become a global event bus.

### 21. Testing ViewModel contracts

Include:

- fake repositories or use cases;
- coroutine test scheduler;
- initial state;
- action-to-state assertions;
- loading-success;
- loading-error;
- cancellation;
- latest-wins;
- repeated collector protection;
- SavedStateHandle restoration;
- Flow testing;
- testing observable behavior instead of private methods.

Turbine may be mentioned only as an optional tool, not a repository requirement.

### 22. Common anti-patterns and decision summary

At minimum cover:

- God ViewModel;
- application-wide ViewModel;
- mutable state exposed publicly;
- unrelated StateFlows;
- ViewModel acting as Repository;
- transport models in UI;
- Context or View references;
- direct NavController ownership;
- GlobalScope;
- duplicated long-lived collectors;
- hidden side effects;
- one `isLoading` for unrelated operations;
- transient events that are lost or duplicated;
- large SavedStateHandle payloads;
- duplicated business logic across ViewModels.

Finish with a practical decision checklist.

---

## Kotlin example requirements

Examples must be conceptually compilable, focused, and idiomatic.

Include at least:

1. immutable UiState and private mutable/public immutable StateFlow;
2. atomic `update`;
3. a combined Flow converted using `stateIn`;
4. explicit action handling;
5. a state-based outcome and an event-based alternative with trade-offs;
6. SavedStateHandle for a route ID or small user input;
7. duplicate collector anti-pattern and correction;
8. one ViewModel unit-test example using fakes and coroutine testing.

Avoid:

- `GlobalScope`;
- Activity or Fragment references;
- NavController in ViewModel;
- direct Retrofit/DAO ownership;
- mutable state exposed publicly;
- universal wrappers;
- unnecessarily large framework examples;
- requiring Hilt.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and contain:

- ViewModel responsibility summary;
- lifetime table;
- owner/scope selection guide;
- configuration change versus process death;
- UiState design checklist;
- one state object versus several flows;
- StateFlow/SharedFlow/Channel/cold Flow comparison;
- state-versus-event decision guide;
- viewModelScope rules;
- stateIn and SharingStarted summary;
- lifecycle-aware collection rules;
- SavedStateHandle checklist;
- dependency boundaries;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Design a complete UiState

Design state for a screen with:

- initial loading;
- content;
- empty result;
- refresh;
- partial warning;
- recoverable error;
- terminal error;
- user input.

Require justification for one state object, sealed variants, and derived fields.

### Exercise 2 — Repair a broken ViewModel

Provide a deliberately flawed ViewModel with:

- mutable state exposed publicly;
- multiple unrelated flows;
- duplicate collectors;
- read-then-assign updates;
- lost or duplicated events;
- one loading flag for several operations;
- a framework dependency.

Require diagnosis and a corrected design.

### Exercise 3 — Saved state and process death

Given a screen with route arguments, filter input, loaded data, bitmap, and repository state, decide:

- what belongs in SavedStateHandle;
- what belongs in Repository/persistent storage;
- what is recomputed;
- what cannot be restored automatically.

Require a restoration flow.

### Exercise 4 — ViewModel contract tests

Design tests for:

- initial state;
- success;
- error;
- cancellation;
- latest-wins;
- repeated collector protection;
- restored SavedStateHandle input.

Use fakes and coroutine test control.

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

- purpose of ViewModel;
- ViewModelStoreOwner;
- Activity/Fragment/navigation/Compose scope;
- configuration change;
- process death;
- `onCleared`;
- UiState design;
- one state object versus multiple flows;
- StateFlow;
- SharedFlow;
- Channel;
- state versus events;
- atomic updates;
- repeated collectors;
- viewModelScope;
- stateIn;
- SharingStarted;
- lifecycle-aware collection;
- SavedStateHandle;
- navigation boundary;
- error presentation;
- shared state;
- testing.

For each question include:

- what a strong answer should cover;
- weak or misleading answers;
- follow-up questions where appropriate.

Do not reward slogan-only answers.

---

## Test requirements

`test.yaml` must contain exactly 10 questions.

Required coverage:

1. ViewModel lifetime and configuration change;
2. process death;
3. owner/scope selection;
4. coherent UiState design;
5. StateFlow versus transient event mechanism;
6. atomic state update;
7. `stateIn` and sharing behavior;
8. lifecycle-aware collection;
9. SavedStateHandle placement;
10. architecture scenario involving ViewModel, use case, Repository, and navigation responsibility.

Questions must test reasoning.

Distractors must be plausible.

Explanations must teach the architectural reason.

---

## References

Use official Android sources and repository-supported evidence.

At minimum inspect current official guidance for:

- ViewModel;
- UI layer;
- state holders;
- StateFlow and Flow collection;
- lifecycle-aware collection;
- SavedStateHandle;
- saving UI state;
- app architecture recommendations.

Use the actual current URLs already represented in repository source packages or existing topic references where possible.

If new official references are necessary, verify them before use.

Do not fabricate access dates.

Follow repository metadata conventions.

---

## Android connections

Metadata should include Android-specific connections equivalent to:

- ViewModelStoreOwner scope controls how long screen state survives.
- ViewModel preserves in-memory screen state through configuration changes but not process death.
- SavedStateHandle restores small recoverable state while repositories reload authoritative data.
- Compose and View-based UIs collect state according to their own lifecycle.
- ViewModel coordinates UI scenarios without owning Activity, Fragment, View, or NavController.

Final wording must remain source-supported.

---

## Relationship to existing topics

Do not duplicate full explanations from:

- architecture foundations;
- UI layer and UDF;
- Data layer;
- Domain layer and use cases.

Assume learners already understand:

- basic layer boundaries;
- state flowing toward UI;
- UI actions flowing toward state owners;
- Repository ownership;
- optional Domain layer.

Use those topics as prerequisites and deepen ViewModel-specific design.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 017 as completed only after validation;
- record the fifth production topic in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- state that five production topics form the growing Android architecture foundation;
- do not claim the 10–15-topic target is complete;
- do not create production mappings;
- do not create a catalog;
- do not promote existing topics;
- do not claim CI, web, Android client, database, AI tutor, or publication exists.

Update `docs/ARCHITECTURE.md` only if an explicit topic count or list would otherwise become stale.

---

## Implementation report

Create the repository-standard implementation report under the current report convention.

Include:

1. implementation summary;
2. files created and changed;
3. source and evidence audit;
4. canonical competency coverage;
5. prerequisite and duplication audit;
6. theory coverage;
7. Kotlin example audit;
8. exact exercise count;
9. exact interview-question count;
10. exact test-question count;
11. metadata and reference audit;
12. validation results;
13. UTF-8 and mojibake audit;
14. deferred work;
15. literal `git status --short`;
16. recommended commit message.

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
- interview count is within the requested range;
- topic ID and directory match;
- all prerequisite IDs exist;
- no prerequisite cycle;
- references are valid;
- new files are UTF-8;
- no mojibake;
- no absolute local paths;
- no source, competency, sequence, mapping, schema, validator, test, or existing-topic data changed;
- no package status outside the new topic changed;
- only allowed documentation and report files changed.

---

## Acceptance criteria

- The six-file topic package exists.
- Metadata conforms to schema.
- Status is `review`.
- Content version is `1`.
- Four existing architecture topics are prerequisites.
- ViewModel is presented as a scoped screen state holder, not a global container.
- Configuration change and process death are clearly distinguished.
- ViewModelStoreOwner and scope are explained.
- UiState design is responsibility-first.
- StateFlow, SharedFlow, Channel, and cold Flow are distinguished without dogma.
- State-versus-event trade-offs are explicit.
- Atomic updates and duplicate collector risks are covered.
- stateIn and SharingStarted are explained.
- Lifecycle-aware collection remains UI-owned.
- SavedStateHandle use is constrained to small recoverable state.
- Navigation and Android framework objects do not leak into ViewModel ownership.
- Shared ViewModel is not presented as an event bus.
- ViewModel testing is substantial.
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
5. content and duplication audit;
6. exact counts for theory sections, Kotlin examples, exercises, interview questions, and tests;
7. validation results;
8. UTF-8 audit;
9. deferred work;
10. literal `git status --short`;
11. recommended commit message.

Do not commit.
