# Task 025 — Add Android Testing Foundations Topic

Status: DONE

## Objective

Add the thirteenth production educational topic in the Junior Core:

```text
android-testing-foundations
```

The topic must explain Android testing as a layered confidence strategy rather than a collection of test libraries.

The learner must understand:

- what to test;
- where to test it;
- unit, integration, component, and UI test boundaries;
- test doubles;
- deterministic coroutine and Flow testing;
- ViewModel testing;
- repository testing;
- Room/network boundary testing at a conceptual level;
- Compose and View-system UI testing;
- lifecycle-sensitive testing;
- navigation testing;
- flaky-test prevention;
- testability as an architectural property.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds on:

- Architecture Foundations;
- UI Layer and UDF;
- Data Layer and Repositories;
- Domain Layer and Use Cases;
- ViewModel and UI State;
- Lifecycle and State Restoration;
- Coroutines;
- Structured Concurrency;
- Flow;
- Navigation;
- Networking;
- Dependency Injection and Scoping.

---

## Core teaching position

Testing is not “writing checks after implementation.”

The core model is:

```text
architecture defines boundaries
→ boundaries define test seams
→ each test owns a specific risk
→ the smallest reliable test is preferred
→ higher-level tests verify integration and user-observable behavior
```

The topic must preserve these distinctions:

```text
unit test
≠ integration test
≠ UI test
≠ instrumentation test
≠ end-to-end test
```

The test pyramid is guidance, not a rigid quota.

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
- canonical Android architecture competencies;
- imported Android Developers source packages;
- all production topics;
- Tasks 016–024.

Use current official or primary documentation for:

- Android local and instrumented tests;
- JUnit;
- Kotlin coroutine testing;
- Flow testing;
- ViewModel testing;
- Compose testing;
- Espresso/View testing;
- Navigation testing;
- Room testing where referenced;
- dependency replacement with Hilt where referenced;
- WorkManager testing only as a boundary preview, not full coverage.

Do not fabricate library behavior.

Do not fabricate access dates.

Clearly distinguish stable testing principles from framework-specific APIs.

---

## Canonical competency scope

Primary:

```text
apply-separation-of-concerns
design-viewmodel-ui-state
use-coroutines-and-flows-across-layers
```

Strongly reinforced:

```text
design-data-layer-around-repositories
evaluate-optional-domain-layer
handle-compose-lifecycle-work
select-ui-state-holders-by-scope
```

Contextually reinforced:

```text
explain-ui-layer-responsibilities
explain-unidirectional-data-flow
isolate-android-framework-dependencies
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/testing/android-testing-foundations/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: testing` is invalid, adapt using repository conventions and document the choice.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-testing-foundations
title: Android Testing Foundations
track: android
section: testing
difficulty: foundation
status: review
estimated_minutes: 240
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-ui-layer-and-unidirectional-data-flow
  - android-data-layer-repositories-and-synchronization
  - android-domain-layer-and-use-cases
  - android-viewmodel-and-ui-state
  - android-lifecycle-and-state-restoration
  - kotlin-coroutines-foundations
  - kotlin-structured-concurrency-and-supervision
  - kotlin-flow-and-reactive-streams
  - android-navigation-architecture
  - android-networking-architecture
  - android-dependency-injection-and-scoping
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain why tests exist and what risk they reduce.
2. Distinguish unit, integration, component, UI, instrumentation, and end-to-end tests.
3. Choose the smallest reliable test boundary.
4. Explain test pyramid and test portfolio trade-offs.
5. Distinguish state verification, interaction verification, and observable behavior.
6. Use fakes, stubs, spies, mocks, and dummies deliberately.
7. Prefer fakes over excessive mocking where stateful behavior matters.
8. Design code for testability without test-only production abstractions.
9. Test pure domain logic.
10. Test ViewModel state transitions.
11. Test coroutine cancellation and virtual time.
12. Test cold Flow and hot Flow deterministically.
13. Test repositories with fake data sources.
14. Test serialization/mapping failures.
15. Test navigation outcomes.
16. Test lifecycle-aware UI behavior.
17. Test Compose semantics.
18. Explain Espresso synchronization at a high level.
19. Prevent flaky tests.
20. Isolate global state and dependency graphs.
21. Explain snapshot/golden testing trade-offs at a high level.
22. Build a balanced project test strategy.

---

## Theory requirements

`theory.md` must contain approximately 22–26 substantial sections.

Required coverage:

### 1. What a test protects

Explain:

- regression risk;
- design assumptions;
- contracts;
- refactoring confidence;
- user-observable behavior.

### 2. Test boundaries

Define:

- unit;
- integration;
- component;
- UI;
- instrumentation;
- end-to-end.

Explain that naming conventions vary, so the boundary must be described explicitly.

### 3. Test portfolio

Explain:

- many fast focused tests;
- fewer integration tests;
- few expensive end-to-end tests;
- cost, speed, realism, diagnostics.

### 4. Smallest reliable test

Explain why the smallest test that catches the target failure is usually preferred.

### 5. Arrange–Act–Assert

Teach structure without dogmatism.

### 6. State, interaction, and observable behavior

Compare:

- returned value/state;
- collaborator call;
- public outcome.

Warn against overspecifying implementation details.

### 7. Test doubles

Define:

- dummy;
- stub;
- fake;
- spy;
- mock.

Explain that terminology can vary across frameworks.

### 8. Fakes versus mocks

Explain:

- behavior-rich fake;
- call verification;
- brittle overspecification;
- deterministic control.

### 9. Testability and architecture

Explain:

- constructor injection;
- explicit dispatchers/clocks;
- pure mapping;
- repository interfaces;
- lifecycle owners;
- avoiding static/global access.

### 10. Pure logic tests

Cover:

- use cases;
- validators;
- reducers;
- mappers;
- state machines.

### 11. ViewModel tests

Cover:

- initial state;
- actions;
- state transitions;
- effects;
- loading/error/success;
- cancellation;
- SavedStateHandle inputs;
- avoiding Android framework dependency.

### 12. Coroutine tests

Cover:

- `runTest`;
- test scheduler;
- virtual time;
- `advanceUntilIdle`;
- `advanceTimeBy`;
- injected dispatchers;
- child coroutine completion;
- leaked jobs.

### 13. Main dispatcher replacement

Explain `Dispatchers.Main` replacement or injection strategy without prescribing one universal rule.

### 14. Flow tests

Cover:

- finite cold Flow;
- infinite Flow;
- background collection;
- StateFlow;
- SharedFlow;
- replay;
- cancellation;
- avoiding hanging tests.

### 15. Repository tests

Explain:

- fake remote/local sources;
- source-of-truth behavior;
- cache policy;
- refresh;
- error mapping;
- synchronization.

### 16. Networking tests

Cover:

- fake service;
- mock web server;
- contract shape;
- malformed payload;
- status errors;
- timeout;
- retry;
- cancellation.

Do not duplicate Task 023 in full.

### 17. Database tests

Cover at a high level:

- in-memory database;
- DAO queries;
- transactions;
- migration testing;
- threading;
- cleanup.

Do not preempt the full Room topic.

### 18. Navigation tests

Cover:

- destination assertions;
- fake navigator;
- NavHostController;
- back-stack behavior;
- deep links;
- result delivery.

### 19. UI tests

Explain:

- user-observable behavior;
- semantics;
- synchronization;
- stable selectors;
- avoiding implementation-only assertions.

### 20. Compose testing

Cover:

- semantics tree;
- node queries;
- actions;
- assertions;
- merged/unmerged tree at a high level;
- test tags as a deliberate fallback;
- state restoration where relevant.

### 21. View-system and Espresso testing

Cover:

- matcher/action/assertion model;
- synchronization;
- IdlingResource concept;
- FragmentScenario/ActivityScenario at a high level.

### 22. Lifecycle-sensitive tests

Explain:

- recreation;
- STARTED/STOPPED transitions;
- collection restart;
- Fragment view destruction;
- process-death boundaries versus ordinary recreation.

### 23. Flaky tests

At minimum:

- real time;
- sleeps;
- network;
- shared mutable state;
- order dependence;
- animation;
- race conditions;
- unstable selectors;
- unclosed resources;
- test pollution;
- asynchronous work without ownership.

### 24. Snapshot and golden tests

Explain benefits and risks:

- visual regression;
- broad diffs;
- maintenance;
- environment dependence;
- accessibility/behavior not fully covered.

### 25. Test naming and diagnostics

Explain readable names, one failure reason, useful assertion messages, and localizing failures.

### 26. Anti-patterns and decision guide

At minimum:

- only UI tests;
- only mocked unit tests;
- testing private methods;
- verifying every call;
- `Thread.sleep`;
- real backend in routine tests;
- singleton mutation;
- test-order dependence;
- production code branching on test mode;
- ignoring cancellation;
- asserting implementation details;
- giant end-to-end fixture;
- nondeterministic clocks/randomness;
- no cleanup;
- confusing instrumentation with integration.

End with:

```text
What risk is covered?
What is the smallest reliable boundary?
What dependencies must be controlled?
What time/lifecycle state is involved?
What should be observed?
Why could this test become flaky?
```

---

## Kotlin example requirements

Include at least:

1. pure use-case unit test;
2. fake repository;
3. ViewModel state test;
4. SavedStateHandle ViewModel test;
5. `runTest`;
6. virtual time;
7. dispatcher injection;
8. cancellation test;
9. cold Flow test;
10. StateFlow test;
11. SharedFlow test;
12. repository refresh test;
13. mapper failure test;
14. mock-server networking test;
15. in-memory DAO test;
16. fake navigator test;
17. NavHostController test;
18. Compose semantics test;
19. Espresso-style test;
20. lifecycle recreation test;
21. flaky sleep anti-pattern and correction;
22. Hilt test replacement sketch.

Examples must be conceptually compilable and version-aware.

Preserve cancellation semantics.

Do not use real delays where virtual time is appropriate.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- test-boundary matrix;
- smallest-reliable-test rule;
- test-double glossary;
- Arrange–Act–Assert;
- state versus interaction verification;
- coroutine testing;
- Flow testing;
- ViewModel testing;
- repository/network/database testing;
- navigation testing;
- Compose/Espresso testing;
- lifecycle testing;
- flakiness checklist;
- test-isolation checklist;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — ViewModel test plan

Given a ViewModel with loading, retry, cancellation, and navigation effect:

Require:

- state-transition tests;
- effect-delivery policy;
- virtual time;
- fake repository;
- cancellation test;
- recreation considerations.

### Exercise 2 — Repository integration boundary

Design tests for repository coordination between remote and local data sources.

Require:

- cache hit;
- refresh;
- stale data;
- mapping failure;
- remote error;
- cancellation;
- deterministic fake sources.

### Exercise 3 — Flaky UI test repair

Given a UI test using sleeps, text-position selectors, and shared state:

Require:

- synchronization strategy;
- stable semantics/selectors;
- graph reset;
- test isolation;
- failure diagnostics.

### Exercise 4 — Balanced test portfolio

Create a test strategy for a checkout feature.

Require:

- unit tests;
- repository/integration tests;
- navigation tests;
- UI tests;
- one end-to-end path;
- explicit risks and costs.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

Do not provide complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 22–26 substantial questions.

Cover:

- purpose of testing;
- test boundaries;
- test pyramid/portfolio;
- smallest reliable test;
- test doubles;
- fakes versus mocks;
- testability;
- pure logic;
- ViewModel tests;
- coroutine testing;
- virtual time;
- Main dispatcher;
- Flow tests;
- repository tests;
- network tests;
- database tests;
- navigation tests;
- Compose tests;
- Espresso;
- lifecycle;
- flaky tests;
- snapshot tests;
- isolation;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where useful.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. choosing test boundary;
2. fake versus mock;
3. ViewModel state test;
4. coroutine virtual time;
5. Flow testing;
6. repository integration;
7. navigation testing;
8. Compose/Espresso semantics;
9. flaky-test diagnosis;
10. balanced test portfolio.

Distractors must be plausible.

Explanations must teach testing strategy, not framework trivia.

---

## References

Use current primary sources.

At minimum inspect:

- Android testing overview;
- local versus instrumented tests;
- coroutine test documentation;
- Flow testing guidance;
- ViewModel testing guidance;
- Compose testing;
- Espresso;
- Navigation testing;
- Room testing where referenced;
- Hilt testing where referenced.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 13 of 17.

The implementation report must record:

```text
Junior Core status after Task 025:
13 of 17 mandatory topics implemented as production packages in review.
4 mandatory topics remain.
```

Remaining mandatory topics:

14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

Do not define the Junior/Middle boundary yet.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 025 after successful validation;
- record thirteen production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that four topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. test-boundary audit;
5. doubles and architecture audit;
6. coroutine/Flow determinism audit;
7. ViewModel/repository audit;
8. UI/navigation/lifecycle audit;
9. flakiness and isolation audit;
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
- no changes to existing topic packages;
- no source, competency, sequence, mapping, schema, validator, or test-infrastructure changes;
- UTF-8;
- no mojibake;
- no local absolute paths.

---

## Acceptance criteria

- Six-file package exists.
- Status is `review`.
- Content version is `1`.
- Testing is presented as a layered confidence strategy.
- Test boundaries are distinguished.
- Smallest reliable test is central.
- Test doubles are used deliberately.
- Coroutine and Flow tests are deterministic.
- ViewModel and repository tests are clear.
- UI/navigation/lifecycle testing is covered.
- Flaky-test prevention is practical.
- Test isolation is explicit.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 13/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. test-boundary audit;
5. doubles/testability audit;
6. coroutine/Flow audit;
7. ViewModel/repository audit;
8. UI/navigation/lifecycle audit;
9. flakiness/isolation audit;
10. Junior Core progress;
11. exact counts;
12. validation results;
13. UTF-8 audit;
14. deferred work;
15. literal `git status --short`;
16. recommended commit message.

Do not commit.
