# Task 021 — Add Kotlin Flow and Reactive Streams Topic

Status: DONE

## Objective

Add the ninth production educational topic in the Junior Core:

```text
kotlin-flow-and-reactive-streams
```

The topic must explain Kotlin Flow as a cold asynchronous stream abstraction and teach Android developers how to design, transform, combine, share, collect, and test reactive data pipelines without losing ownership, lifecycle, cancellation, or backpressure semantics.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds directly on:

```text
kotlin-coroutines-foundations
kotlin-structured-concurrency-and-supervision
```

The topic must deepen reactive stream design rather than repeat coroutine basics.

---

## Core teaching position

The central model is:

```text
Flow
= asynchronous sequence of values
+ coroutine cancellation
+ explicit collection
+ operator pipeline
```

Key distinctions:

```text
cold Flow
→ upstream starts per collector

StateFlow
→ hot state holder with current value

SharedFlow
→ hot broadcast stream with configurable replay/buffer

Channel
→ point-to-point or fan-out communication primitive

suspend function
→ one asynchronous result

Flow
→ zero, one, or many asynchronous values over time
```

The topic must not reduce Flow to “RxJava but newer” or “a list that loads later.”

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
- all content-authoring documentation;
- the canonical Android architecture competency package;
- both imported Android source packages;
- all current production topics;
- Task 019 and Task 020.

At minimum inspect evidence related to:

```text
use-coroutines-and-flows-across-layers
design-viewmodel-ui-state
explain-unidirectional-data-flow
design-data-layer-around-repositories
handle-compose-lifecycle-work
```

Use official Kotlin Flow documentation and official Android guidance for Flow, StateFlow, SharedFlow, lifecycle-aware collection, and testing.

Do not invent runtime guarantees or undocumented operator behavior.

Do not fabricate access dates.

---

## Canonical competency scope

Primary:

```text
use-coroutines-and-flows-across-layers
```

Strongly reinforced:

```text
design-viewmodel-ui-state
explain-unidirectional-data-flow
design-data-layer-around-repositories
handle-compose-lifecycle-work
```

Contextually reinforced:

```text
explain-ui-layer-responsibilities
explain-persistent-data-models
apply-separation-of-concerns
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/kotlin/flow/kotlin-flow-and-reactive-streams/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: flow` is invalid, use the valid repository convention and document the adaptation.

---

## Topic metadata

Preferred metadata:

```yaml
id: kotlin-flow-and-reactive-streams
title: Kotlin Flow and Reactive Streams
track: kotlin
section: flow
difficulty: foundation
status: review
estimated_minutes: 210
content_version: 1
prerequisites:
  - kotlin-coroutines-foundations
  - kotlin-structured-concurrency-and-supervision
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain what Flow represents and when it is appropriate.
2. Distinguish cold and hot streams.
3. Explain when upstream starts and stops.
4. Use `flow {}` and `emit`.
5. Explain sequential operator execution.
6. Distinguish intermediate and terminal operators.
7. Use `map`, `filter`, `transform`, and `onEach`.
8. Use `catch`, `retry`, and `retryWhen` deliberately.
9. Explain why `catch` does not catch downstream collector failures.
10. Distinguish `flowOn` from `withContext`.
11. Explain context preservation.
12. Use `buffer`, `conflate`, and `collectLatest`.
13. Distinguish backpressure strategies.
14. Use `combine`, `zip`, `merge`, and `flatMapLatest`.
15. Explain cancellation of obsolete work.
16. Distinguish Flow from StateFlow, SharedFlow, and Channel.
17. Use `stateIn` and `shareIn`.
18. Choose `SharingStarted` intentionally.
19. Collect Flow with Android lifecycle ownership.
20. Test cold and hot streams deterministically.
21. Recognize reactive-stream anti-patterns.
22. Design Flow boundaries across UI, Domain, and Data layers.

---

## Theory requirements

`theory.md` must contain approximately 20–24 substantial sections.

Required coverage:

### 1. One value versus a stream

Compare:

```text
suspend fun load(): User
Flow<User>
```

Explain when a stream is justified.

### 2. Cold Flow

Explain:

- upstream starts per collector;
- each collector gets an independent execution;
- repeated collection can repeat work;
- coldness is about subscription behavior, not temperature metaphors alone.

### 3. Building a Flow

Cover:

- `flow {}`;
- `emit`;
- cancellation;
- sequential emission;
- exception behavior.

### 4. Collection

Cover:

- `collect`;
- terminal nature;
- collection suspends;
- no work happens without collection for cold Flow.

### 5. Intermediate versus terminal operators

Explain pipeline construction and execution.

### 6. Mapping and filtering

Cover:

- `map`;
- `filter`;
- `transform`;
- `onEach`.

### 7. Context preservation

Explain:

- Flow preserves context;
- upstream should not emit from arbitrary foreign contexts inside `flow`;
- execution policy belongs at the correct boundary.

### 8. `flowOn`

Explain:

- affects upstream operators;
- does not move downstream collector;
- differs from wrapping collection in `withContext`;
- may introduce a concurrency boundary.

### 9. Error handling

Cover:

- `catch`;
- upstream-only interception;
- rethrowing cancellation;
- domain errors versus stream failures;
- `onCompletion`.

### 10. Retry

Cover:

- `retry`;
- `retryWhen`;
- bounded retry;
- backoff concept;
- retry ownership;
- avoiding hidden infinite retries.

### 11. Backpressure and throughput

Explain producer/consumer speed mismatch.

### 12. `buffer`

Explain overlap and buffering.

### 13. `conflate`

Explain dropping intermediate values while preserving latest.

### 14. `collectLatest`

Explain cancelling previous collector work when a new value arrives.

### 15. Combining streams

Compare:

- `combine`;
- `zip`;
- `merge`.

Use concrete scenarios.

### 16. Latest-wins switching

Explain:

- `flatMapLatest`;
- cancellation of obsolete child streams;
- search query and route-selection scenarios;
- not using it when all work must complete.

### 17. Hot streams overview

Distinguish:

```text
StateFlow
SharedFlow
Channel
```

### 18. StateFlow

Cover:

- always has current value;
- conflated state semantics;
- equality-based suppression where relevant;
- not for one-off events by default;
- UI state usage.

### 19. SharedFlow

Cover:

- replay;
- extra buffer capacity;
- overflow policy at a high level;
- broadcast behavior;
- event and shared-update use cases;
- subscriber timing.

### 20. Channel

Explain:

- send/receive;
- rendezvous or buffered behavior;
- point-to-point/fan-out semantics;
- conversion to Flow where appropriate;
- why Channel and SharedFlow are not interchangeable.

### 21. `stateIn` and `shareIn`

Cover:

- scope ownership;
- initial value for `stateIn`;
- replay;
- `SharingStarted`;
- `Eagerly`;
- `Lazily`;
- `WhileSubscribed`;
- avoiding dogmatic timeout values.

### 22. Android lifecycle collection

Cover:

- `repeatOnLifecycle`;
- `collectAsStateWithLifecycle`;
- Fragment view lifecycle;
- multiple Flow collection;
- cancellation and restart;
- why plain `launch { collect }` can be insufficient.

### 23. Layer boundaries

Explain:

- Data layer exposes source streams;
- Repository combines and normalizes data;
- Domain may expose focused Flow contracts;
- ViewModel converts streams to UiState;
- UI collects lifecycle-aware;
- avoid exposing mutable flows.

### 24. Testing and anti-patterns

Testing must cover:

- cold Flow collection;
- StateFlow;
- SharedFlow;
- virtual time;
- finite versus infinite streams;
- collecting in a background test coroutine;
- cancellation.

Anti-patterns must include:

- collecting the same cold network Flow multiple times;
- hidden expensive upstream work;
- `catch` that swallows cancellation;
- using SharedFlow as global event bus;
- using StateFlow for transient events without policy;
- `flowOn` applied blindly;
- `combine` for unrelated state;
- unbounded replay;
- unobserved hot stream;
- mutable flow exposed publicly;
- collection outside lifecycle ownership;
- retry forever;
- using `collectLatest` when every item must complete;
- wrapping every source in `shareIn` without an owner.

---

## Kotlin example requirements

Include at least:

1. basic `flow { emit(...) }`;
2. cold Flow collected twice;
3. `map`/`filter`;
4. `flowOn`;
5. `catch` preserving cancellation;
6. bounded `retryWhen`;
7. `buffer`;
8. `conflate`;
9. `collectLatest`;
10. `combine`;
11. `zip`;
12. `flatMapLatest`;
13. StateFlow;
14. SharedFlow;
15. Channel;
16. `stateIn`;
17. `shareIn`;
18. lifecycle-aware Android collection;
19. Flow test;
20. StateFlow or SharedFlow test.

Examples must be conceptually compilable.

Avoid outdated or experimental APIs unless clearly marked and source-supported.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- Flow mental model;
- cold vs hot;
- operator categories;
- `flowOn`;
- error handling;
- retry;
- buffer/conflate/collectLatest;
- combine/zip/merge;
- `flatMapLatest`;
- StateFlow vs SharedFlow vs Channel;
- `stateIn` vs `shareIn`;
- lifecycle collection;
- architecture placement;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Cold Flow duplication

Diagnose a screen that collects one cold repository Flow multiple times and triggers repeated network/database work.

Require:

- identify duplicated upstream execution;
- choose whether to keep cold, cache, `stateIn`, or `shareIn`;
- define owner scope;
- test expected subscription behavior.

### Exercise 2 — Search pipeline

Design a search Flow with:

- query stream;
- debounce where source-supported;
- distinct values;
- `flatMapLatest`;
- loading/error/result state;
- cancellation of stale searches.

Do not provide a full final solution.

### Exercise 3 — Combine application state

Combine user, settings, and connectivity streams into coherent UI state.

Require:

- justify `combine` versus `zip`;
- define initial state;
- handle one failing source;
- prevent unrelated event streams from entering state.

### Exercise 4 — Hot stream review

Review incorrect use of StateFlow, SharedFlow, Channel, replay, and lifecycle collection.

Require corrected choices and tests.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

---

## Interview requirements

`interview.md` must contain approximately 20–24 substantial questions.

Cover:

- Flow versus suspend;
- cold versus hot;
- collection;
- operators;
- context preservation;
- `flowOn`;
- `catch`;
- retry;
- buffer;
- conflate;
- collectLatest;
- combine;
- zip;
- merge;
- flatMapLatest;
- StateFlow;
- SharedFlow;
- Channel;
- stateIn;
- shareIn;
- SharingStarted;
- lifecycle collection;
- layer boundaries;
- testing.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where appropriate.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. Flow versus suspend;
2. cold collection behavior;
3. `flowOn`;
4. `catch` boundary;
5. buffer/conflate/collectLatest;
6. combine versus zip;
7. flatMapLatest;
8. StateFlow/SharedFlow/Channel;
9. stateIn/shareIn ownership;
10. Android lifecycle collection architecture.

Distractors must be plausible.

Explanations must teach the stream semantics.

---

## References

Use official Kotlin and Android references.

At minimum inspect:

- Kotlin Flow overview;
- context and `flowOn`;
- exception handling;
- flattening operators;
- StateFlow and SharedFlow;
- Android StateFlow/SharedFlow guidance;
- lifecycle-aware collection;
- Compose lifecycle collection;
- coroutine testing.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 9 of 17.

The implementation report must record:

```text
Junior Core status after Task 021:
9 of 17 mandatory topics implemented as production packages in review.
8 mandatory topics remain.
```

Do not define the Junior/Middle boundary yet.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 021 only after successful validation;
- record nine production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that eight mandatory topics remain:
  - Navigation;
  - Networking;
  - Dependency Injection and Scoping;
  - Testing;
  - Security;
  - Room;
  - WorkManager;
  - Compose;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if a hardcoded topic count or list becomes stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. canonical competency coverage;
5. cold/hot semantics audit;
6. operator and backpressure audit;
7. StateFlow/SharedFlow/Channel audit;
8. lifecycle and ownership audit;
9. layer-boundary audit;
10. Junior Core progress audit;
11. exact counts;
12. validation;
13. UTF-8/mojibake audit;
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

- exactly six package files;
- exactly four exercises;
- exactly ten tests;
- interview count in range;
- schema-valid taxonomy;
- prerequisites exist;
- no prerequisite cycle;
- no existing topic-package changes;
- no source, competency, sequence, mapping, schema, validator, or test-infrastructure changes;
- UTF-8;
- no mojibake;
- no local absolute paths.

---

## Acceptance criteria

- Six-file package exists.
- Status is `review`.
- Content version is `1`.
- Task 019 and 020 are prerequisites.
- Flow versus suspend is clear.
- Cold and hot semantics are accurate.
- Collection behavior is explicit.
- `flowOn` and context preservation are correct.
- Error handling preserves cancellation.
- Retry is bounded and policy-driven.
- Backpressure strategies are distinguished.
- `combine`, `zip`, `merge`, and `flatMapLatest` are distinguished.
- StateFlow, SharedFlow, and Channel are distinguished.
- `stateIn` and `shareIn` ownership is clear.
- Lifecycle collection is correct.
- Layer boundaries are preserved.
- Tests cover cold and hot streams.
- Practice contains exactly 4 exercises.
- Test contains exactly 10 questions.
- Junior Core progress is updated to 9/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. cold/hot and operator audit;
5. StateFlow/SharedFlow/Channel audit;
6. Android lifecycle and ownership audit;
7. Junior Core progress update;
8. exact counts;
9. validation results;
10. UTF-8 audit;
11. deferred work;
12. literal `git status --short`;
13. recommended commit message.

Do not commit.
