# Task 019 — Add Kotlin Coroutines Foundations Topic

Status: DONE

## Objective

Add the seventh production educational topic in the Android app architecture track:

```text
kotlin-coroutines-foundations
```

The topic must explain the execution model of Kotlin coroutines for Android developers without reducing coroutines to:

> “lightweight threads.”

The learner must understand:

- coroutine versus thread;
- suspending functions;
- coroutine builders;
- CoroutineScope;
- CoroutineContext;
- Job hierarchy;
- dispatchers;
- continuation and resumption;
- thread switching;
- cancellation;
- exception propagation;
- `launch` versus `async`;
- `withContext`;
- lifecycle-owned scopes;
- blocking versus suspending;
- testing basics.

This task belongs to:

```text
Phase 3 — Learning Content MVP
```

It extends the current architecture foundation after lifecycle and state restoration.

The new package must remain in `review`.

Task 019 is a foundation topic.

Advanced structured-concurrency design, supervision strategy, parallel decomposition, and deep Flow mechanics remain separate future topics.

---

## Core teaching position

The central model is:

```text
Coroutine = a cancellable computation
CoroutineScope = owner of coroutine lifetime
CoroutineContext = execution metadata and elements
Job = lifecycle and parent-child relationship
Dispatcher = decides where runnable coroutine work may execute
Thread = actual OS/JVM execution resource
Continuation = suspended computation state that can later resume
```

A coroutine:

- is not a thread;
- can suspend without blocking its current thread;
- may resume on the same or a different thread depending on context;
- must belong to a deliberate scope;
- participates in a Job hierarchy;
- should cooperate with cancellation;
- does not make blocking APIs non-blocking automatically.

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
- all current production topics, especially:
  - UI Layer and UDF;
  - Data Layer;
  - Domain Layer and Use Cases;
  - ViewModel and UI State;
  - Lifecycle and State Restoration.

At minimum inspect evidence related to:

```text
use-coroutines-and-flows-across-layers
handle-compose-lifecycle-work
design-viewmodel-ui-state
explain-android-component-lifecycle-constraints
```

Use official Kotlin coroutine documentation and official Android coroutine guidance for technical details not represented in repository source packages.

Do not invent scheduler, compiler, or runtime internals.

Do not fabricate access dates.

---

## Canonical competency scope

Primary:

```text
use-coroutines-and-flows-across-layers
```

Strongly reinforced:

```text
handle-compose-lifecycle-work
design-viewmodel-ui-state
explain-android-component-lifecycle-constraints
```

Contextually reinforced:

```text
apply-separation-of-concerns
explain-ui-layer-responsibilities
design-data-layer-around-repositories
evaluate-optional-domain-layer
```

Do not modify competency files.

Do not create a production competency-to-topic mapping in this task.

---

## Package location

Create exactly:

```text
content/kotlin/coroutines/kotlin-coroutines-foundations/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use the actual repository track/section conventions. If a Kotlin track or `coroutines` section does not yet exist, use schema-valid metadata without changing schemas.

---

## Topic metadata

Preferred metadata:

```yaml
id: kotlin-coroutines-foundations
title: Kotlin Coroutines Foundations
track: kotlin
section: coroutines
difficulty: foundation
status: review
estimated_minutes: 180
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-viewmodel-and-ui-state
  - android-lifecycle-and-state-restoration
```

Adapt only where required by the current schema or actual repository taxonomy.

Do not invent unsupported taxonomy values.

If the schema restricts track or section values, inspect existing conventions and document the chosen adaptation in the implementation report.

---

## Required learning outcomes

The final topic must cover outcomes equivalent to:

1. Explain the difference between a coroutine, a thread, and a task.
2. Explain what suspension means and why it does not block a thread.
3. Describe how a suspended coroutine can later resume.
4. Explain the roles of CoroutineScope, CoroutineContext, Job, and Dispatcher.
5. Explain why coroutine lifetime must have an owner.
6. Use `launch`, `async`, and `withContext` according to result and lifetime needs.
7. Distinguish sequential and concurrent coroutine execution.
8. Explain how dispatchers select execution resources.
9. Explain why a coroutine may start on one thread and resume on another.
10. Distinguish blocking calls from suspending calls.
11. Explain cooperative cancellation.
12. Use cancellable suspending APIs and avoid swallowing cancellation.
13. Explain basic parent-child Job behavior.
14. Explain basic exception behavior in `launch` and `async`.
15. Use lifecycle-owned Android scopes appropriately.
16. Recognize GlobalScope and unmanaged-scope risks.
17. Avoid hardcoded dispatcher ownership in inappropriate layers.
18. Design suspend boundaries across UI, Domain, and Data layers.
19. Test coroutine code with controlled virtual time.
20. Recognize foundational coroutine anti-patterns.

Final wording must remain source-supported and schema-compliant.

---

## Theory requirements

`theory.md` must be a coherent guide with approximately 18–22 substantial sections.

### 1. Why coroutines exist

Explain:

- asynchronous work;
- waiting on I/O;
- responsive UI;
- callback complexity;
- sequential-looking asynchronous code.

Do not claim coroutines make work inherently parallel.

### 2. Coroutine versus thread

Explain:

- thread as an execution resource;
- coroutine as a computation that may suspend;
- many coroutines can use a smaller pool of threads;
- a running coroutine still executes on a thread;
- suspension releases the thread for other work.

Avoid unqualified performance slogans.

### 3. Suspending functions

Explain:

- `suspend` marks a function that may suspend;
- it does not automatically run in background;
- it does not automatically create a coroutine;
- a suspend function can call other suspend functions;
- suspension points cooperate with continuation-based resumption.

### 4. Continuation and resumption

Explain conceptually:

```text
run
→ reach suspension point
→ store continuation state
→ release thread
→ awaited work completes
→ resume continuation
```

Avoid unstable compiler internals.

### 5. CoroutineScope

Explain:

- scope owns lifetime;
- `coroutineContext`;
- cancellation of a scope;
- scope is not merely a utility object;
- unmanaged scopes detach work from lifecycle.

### 6. CoroutineContext

Explain it as a collection of context elements.

At minimum:

- Job;
- Dispatcher;
- CoroutineName where useful;
- exception handler at a high level.

Do not make context composition unnecessarily abstract.

### 7. Job and hierarchy

Explain:

- parent-child relationships;
- completion;
- cancellation;
- children normally belong to parent lifetime;
- parent waits for children;
- child failure behavior at a basic level.

Reserve advanced supervision for a later structured-concurrency topic.

### 8. Dispatchers

Explain:

- `Dispatchers.Main`;
- `Dispatchers.Default`;
- `Dispatchers.IO`;
- `Dispatchers.Unconfined` as a specialized tool, not a normal application default.

Clarify:

- Main for UI-confined work;
- Default for CPU-intensive work;
- IO for blocking I/O integration;
- dispatcher is not equivalent to one thread;
- implementation details and pool sizes are not stable API guarantees.

### 9. Thread switching

Explain why:

- coroutine identity is independent from thread identity;
- dispatcher/context determines where resumable work is scheduled;
- suspension and resumption may involve different threads;
- thread-local assumptions require care.

Include a concise logging example.

### 10. Builders: `launch`

Explain:

- returns Job;
- use when the caller needs lifecycle/control but no direct result value;
- exceptions are not deferred like `async`;
- launching does not imply parallelism unless execution overlaps.

### 11. Builders: `async`

Explain:

- returns Deferred;
- result is obtained with `await`;
- `async` should represent concurrent result-producing work;
- using `async` and immediately awaiting it adds no useful concurrency;
- forgotten Deferred is a smell.

Do not turn `async` into a universal replacement for suspend functions.

### 12. `withContext`

Explain:

- changes context for a block;
- returns the block result;
- remains sequential from the caller's perspective;
- useful for dispatcher confinement or integrating blocking work;
- not a new detached lifecycle.

### 13. Sequential versus concurrent execution

Show:

```kotlin
val a = loadA()
val b = loadB()
```

versus:

```kotlin
coroutineScope {
    val a = async { loadA() }
    val b = async { loadB() }
    combine(a.await(), b.await())
}
```

Explain:

- concurrency is deliberate;
- parallel execution depends on dispatcher/resources;
- dependency ordering must remain sequential.

### 14. Blocking versus suspending

Explain:

- `Thread.sleep` blocks;
- `delay` suspends;
- blocking JDBC/file/socket APIs can still block inside a coroutine;
- `suspend` does not transform blocking work;
- use an appropriate dispatcher or suspending client.

### 15. Cancellation

Explain:

- cancellation is cooperative;
- suspending functions usually check cancellation;
- CPU loops need explicit checks or yielding;
- cancellation propagates through Job hierarchy;
- cleanup belongs in `finally`;
- cancellation is not an ordinary business failure.

### 16. Cancellation mistakes

Cover:

- swallowing `CancellationException`;
- broad `catch (Throwable)` or `catch (Exception)` without rethrowing cancellation;
- blocking calls that ignore cancellation;
- detached child work;
- infinite loops without checks;
- continuing state updates after cancellation.

### 17. Exceptions

Explain basic behavior:

- `launch` failure is delivered through Job hierarchy;
- `async` stores failure until `await`, while still participating in hierarchy;
- try/catch location matters;
- CoroutineExceptionHandler is not a universal catch-all;
- domain/data error modeling remains separate from coroutine failure semantics.

Keep advanced supervision for Task 020.

### 18. Android-owned scopes

Explain:

- `viewModelScope`;
- `lifecycleScope`;
- `repeatOnLifecycle`;
- Compose effects/scopes at a high level;
- ownership determines cancellation;
- Repository application-long work needs an explicit longer-lived owner.

Do not imply one Android scope fits all work.

### 19. Layer boundaries

Explain:

- ViewModel launches UI-scenario work;
- Domain exposes focused suspend or Flow contracts;
- Data layer owns blocking/suspending implementation details;
- callers should not need to know Retrofit/Room internals;
- main-safety should be discussed as a contract where source-supported;
- dispatcher selection should live near the blocking or CPU-bound implementation.

### 20. Testing foundations

Explain:

- `runTest`;
- virtual time;
- test dispatcher/scheduler;
- avoiding real delays;
- injecting dispatcher or execution policy only where needed;
- testing results, cancellation, and ordering.

Do not make a specific third-party library mandatory.

### 21. Common anti-patterns

At minimum:

- `GlobalScope`;
- creating ad hoc scopes without ownership;
- `async` followed by immediate `await`;
- blocking Main;
- hardcoding Main/IO throughout every layer;
- swallowing cancellation;
- wrapping every function in `withContext`;
- fire-and-forget work inside repositories;
- assuming one coroutine equals one thread;
- assuming suspend means background;
- unnecessary `CoroutineExceptionHandler`;
- hidden retry loops;
- forgotten Deferred;
- lifecycle work started from the wrong owner.

### 22. Decision checklist

End with a compact process:

```text
Who owns this work?
Does it return a result?
Must operations overlap?
Can it suspend?
Can it block?
Which dispatcher is justified?
How is cancellation observed?
How is it tested?
```

---

## Kotlin example requirements

Include at least:

1. a basic suspending function;
2. `launch` returning Job;
3. `async`/`await` concurrent result example;
4. `async` immediately awaited as a counterexample;
5. `withContext` for blocking integration;
6. thread logging before and after suspension;
7. cooperative cancellation in a CPU loop;
8. cancellation-safe exception handling;
9. Android ViewModel scope example;
10. `runTest` with virtual time;
11. parent-child cancellation example.

Examples must be conceptually compilable.

Avoid:

- `GlobalScope` except in an explicitly marked anti-pattern;
- undocumented dispatcher internals;
- fake thread guarantees;
- advanced supervision implementation that belongs to Task 020.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and contain:

- coroutine vs thread;
- suspend meaning;
- scope/context/job/dispatcher summary;
- dispatcher selection guide;
- `launch` vs `async` vs `withContext`;
- sequential vs concurrent;
- blocking vs suspending;
- cancellation checklist;
- exception basics;
- Android scope guide;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Execution model

Given several coroutine snippets, determine:

- which coroutine owns the work;
- whether calls are sequential or concurrent;
- whether a thread is blocked;
- where resumption may occur;
- what happens on cancellation.

Require explanations, not only outputs.

### Exercise 2 — Fix a broken repository

Provide code containing:

- blocking work on Main;
- hardcoded unmanaged scope;
- swallowed cancellation;
- unnecessary `async`;
- hidden fire-and-forget behavior.

Require a corrected suspend contract and ownership analysis.

### Exercise 3 — Concurrent aggregation

Design a use case that loads two independent values concurrently.

Require:

- structured owner;
- error behavior;
- cancellation;
- sequential fallback where one value depends on another;
- tests.

Do not provide the final solution.

### Exercise 4 — Coroutine tests

Write tests for:

- delay-based behavior;
- cancellation;
- ordering;
- one concurrent operation;
- no real wall-clock wait.

Use `runTest` and controlled scheduling.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints separated from the solution path.

---

## Interview requirements

`interview.md` must contain approximately 18–22 substantial questions.

Cover:

- coroutine vs thread;
- `suspend`;
- continuation;
- CoroutineScope;
- CoroutineContext;
- Job hierarchy;
- dispatcher selection;
- IO vs Default;
- Unconfined;
- `launch`;
- `async`;
- `Deferred`;
- `withContext`;
- sequential vs concurrent;
- blocking vs suspending;
- cancellation;
- `CancellationException`;
- exception propagation;
- Android scopes;
- layer boundaries;
- testing;
- common anti-patterns.

For each question include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where appropriate.

Do not reward API-name memorization without ownership reasoning.

---

## Test requirements

`test.yaml` must contain exactly 10 questions.

Required coverage:

1. coroutine vs thread;
2. suspend meaning;
3. scope ownership;
4. dispatcher selection;
5. `launch` vs `async`;
6. sequential vs concurrent;
7. blocking vs suspending;
8. cooperative cancellation;
9. exception/cancellation scenario;
10. Android architecture placement scenario.

Questions must test reasoning.

Distractors must be plausible.

Explanations must teach why the selected answer is correct.

---

## References

Use official Kotlin and Android references.

At minimum inspect:

- Kotlin coroutine basics;
- coroutine context and dispatchers;
- cancellation and timeouts;
- exception handling;
- Android coroutines best practices;
- lifecycle-aware coroutine guidance;
- ViewModel coroutine guidance;
- coroutine testing guidance.

Use current official URLs.

Do not fabricate access dates.

Follow repository reference metadata conventions.

---

## Android connections

Metadata should include Android-specific connections equivalent to:

- Android UI work must not block the Main thread.
- ViewModel and lifecycle scopes bind coroutine work to UI ownership.
- Data implementations choose appropriate execution for blocking or CPU-intensive work.
- Suspend and Flow contracts cross architectural layers without exposing thread management to UI.
- Cancellation follows the lifecycle owner when work is correctly scoped.

Final wording must remain source-supported.

---

## Relationship to existing topics

Do not repeat full explanations from:

- ViewModel and UI State;
- Lifecycle and State Restoration;
- Domain Layer and Use Cases;
- Data Layer.

Assume learners already understand those ownership boundaries.

This topic must deepen coroutine execution and cancellation mechanics.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 019 as completed only after validation;
- record the seventh production topic in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- state that seven production topics form the growing MVP;
- do not claim the 10–15-topic target is complete;
- do not create production mappings;
- do not create a catalog;
- do not promote existing topics;
- do not claim CI, web, Android client, database, AI tutor, or publication exists.

Update `docs/ARCHITECTURE.md` only if a hardcoded topic count or list becomes stale.

---

## Implementation report

Create the repository-standard implementation report.

Include:

1. implementation summary;
2. files created and changed;
3. source and evidence audit;
4. canonical competency coverage;
5. execution-model audit;
6. cancellation and exception audit;
7. Android scope and layer-boundary audit;
8. prerequisite and duplication audit;
9. theory coverage;
10. Kotlin example audit;
11. exact exercise count;
12. exact interview-question count;
13. exact test-question count;
14. metadata and taxonomy audit;
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

- exactly six files in the new package;
- exactly four exercises;
- exactly ten tests;
- interview count in range;
- topic ID and directory match;
- taxonomy values are schema-valid;
- prerequisites exist;
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
- Coroutine and thread are distinguished.
- Suspension and continuation are explained.
- Scope, context, Job, and Dispatcher are distinguished.
- Dispatchers are explained without unstable pool-size guarantees.
- `launch`, `async`, and `withContext` are used by responsibility.
- Sequential and concurrent work are distinguished.
- Blocking and suspending are distinguished.
- Cooperative cancellation is explained.
- CancellationException is not swallowed.
- Basic exception behavior is accurate.
- Android scopes are ownership-based.
- Layer boundaries are preserved.
- Testing uses controlled coroutine time.
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
5. execution, cancellation, and exception audit;
6. Android scope and layer-boundary audit;
7. content and duplication audit;
8. exact section and item counts;
9. validation results;
10. UTF-8 audit;
11. deferred work;
12. literal `git status --short`;
13. recommended commit message.

Do not commit.
