# Task 020 — Add Kotlin Structured Concurrency and Supervision Topic

Status: DONE

## Objective

Add the eighth production educational topic:

```text
kotlin-structured-concurrency-and-supervision
```

The topic must explain how coroutine work is organized into explicit lifetime trees, how failure and cancellation propagate, and how to choose between fail-fast and supervised execution.

This task belongs to:

```text
Phase 3 — Learning Content MVP
```

The new package must remain in `review`.

It builds directly on:

```text
kotlin-coroutines-foundations
```

Task 019 established coroutine, scope, context, Job, dispatcher, suspension, cancellation, and basic exception semantics. Task 020 must deepen ownership and failure design rather than repeat those foundations.

---

## Core teaching position

Structured concurrency means:

```text
Every coroutine has an explicit owner.
Child work belongs to a bounded lifetime.
The parent does not complete before its children.
Cancellation and failures follow a deliberate hierarchy.
Callers can reason about completion from the enclosing suspend contract.
```

The central distinction is:

```text
coroutineScope / Job
→ fail-fast sibling cancellation

supervisorScope / SupervisorJob
→ child failures can be isolated when the parent handles results deliberately
```

Supervision is not a way to ignore errors. It changes propagation policy; the application must still observe, represent, log, retry, or otherwise handle failures.

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
- Task 019 and its implementation report.

Use official Kotlin coroutine documentation and official Android coroutine guidance.

At minimum inspect official material related to:

- structured concurrency;
- coroutine scope and Job hierarchy;
- cancellation;
- exception propagation;
- supervision;
- `coroutineScope`;
- `supervisorScope`;
- `SupervisorJob`;
- timeout;
- Android external scopes and long-lived work;
- coroutine testing.

Do not invent runtime guarantees or undocumented internal behavior.

Do not fabricate access dates.

---

## Canonical competency scope

Primary:

```text
use-coroutines-and-flows-across-layers
```

Reinforced where supported:

```text
design-viewmodel-ui-state
handle-compose-lifecycle-work
explain-android-component-lifecycle-constraints
apply-separation-of-concerns
evaluate-optional-domain-layer
design-data-layer-around-repositories
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/kotlin/coroutines/kotlin-structured-concurrency-and-supervision/
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

Preferred metadata:

```yaml
id: kotlin-structured-concurrency-and-supervision
title: Kotlin Structured Concurrency and Supervision
track: kotlin
section: coroutines
difficulty: intermediate
status: review
estimated_minutes: 180
content_version: 1
prerequisites:
  - kotlin-coroutines-foundations
```

Inspect the actual schema before using `intermediate`.

If the current schema supports another equivalent difficulty value, use the valid value and document the adaptation.

Do not change the schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain structured concurrency through ownership, bounded lifetime, and completion.
2. Read a Job tree and predict parent/child completion.
3. Explain upward failure and downward cancellation.
4. Distinguish cancellation from failure.
5. Use `coroutineScope` for fail-fast concurrent work.
6. Use `supervisorScope` for deliberately isolated child failure.
7. Distinguish `Job` from `SupervisorJob`.
8. Explain the difference between `supervisorScope` and adding `SupervisorJob` to an arbitrary context.
9. Predict sibling behavior after a child failure.
10. Design fail-fast and best-effort aggregation.
11. Observe all `Deferred` failures.
12. Avoid detached and orphaned coroutines.
13. Apply timeout without leaking child work.
14. Perform cancellation-safe cleanup.
15. Use `NonCancellable` only for small mandatory suspending cleanup.
16. Design external scopes for work that must outlive a screen.
17. Define ownership for application-scoped work.
18. Represent partial success explicitly.
19. Test failure propagation, cancellation, timeout, and supervision.
20. Recognize structured-concurrency anti-patterns.

---

## Theory requirements

`theory.md` must contain approximately 18–22 substantial sections.

Required coverage:

### 1. From coroutine syntax to lifetime design

Explain why knowing `launch` and `async` is not enough.

### 2. Structured concurrency invariants

Explain ownership, bounded lifetime, parent waiting, and observable completion.

### 3. Job tree

Explain parent and child Jobs and how builders attach to the current scope.

### 4. Parent completion

Explain why a parent waits for children even if the parent block has reached its last statement.

### 5. Downward cancellation

Explain parent cancellation propagating to children.

### 6. Upward failure

Explain how a non-cancellation child failure affects its parent in a regular Job hierarchy.

### 7. Sibling cancellation

Explain why fail-fast hierarchies cancel siblings after one child fails.

### 8. `coroutineScope`

Explain:

- suspend boundary;
- child ownership;
- parent waiting;
- fail-fast behavior;
- result return;
- cancellation propagation.

### 9. Fail-fast aggregation

Show two independent `async` operations where either failure invalidates the whole result.

### 10. `supervisorScope`

Explain child-failure isolation and why each failed child still requires observation and handling.

### 11. `SupervisorJob`

Explain its role for long-lived scopes with independent children.

Clearly distinguish it from `supervisorScope`.

### 12. Supervision is not error suppression

Cover lost exceptions, ignored Deferred values, incomplete UI state, and missing observability.

### 13. Fail-fast versus best-effort

Provide a decision table.

Fail-fast examples:

- required profile plus permissions;
- transaction preparation;
- dependent aggregate.

Best-effort examples:

- independent dashboard widgets;
- optional recommendations;
- background refresh of unrelated caches.

### 14. Partial success modeling

Discuss explicit result models without prescribing one universal wrapper.

### 15. `launch` and `async` inside hierarchies

Explain:

- result ownership;
- awaiting all Deferred values;
- forgotten Deferred;
- exceptions;
- why `async` does not become safe merely because it is supervised.

### 16. Cancellation versus failure

Explain `CancellationException`, cooperative cancellation, and why cancellation normally should not be converted into business failure.

### 17. Timeout

Cover:

- `withTimeout`;
- `withTimeoutOrNull`;
- child cancellation;
- cleanup;
- timeout as policy;
- avoiding detached work that survives timeout.

### 18. Cleanup

Explain:

- `try/finally`;
- non-suspending cleanup;
- suspending cleanup;
- narrowly scoped `withContext(NonCancellable)`;
- why broad NonCancellable regions are dangerous.

### 19. External and application scopes

Explain work that must outlive ViewModel or UI:

- explicit owner;
- application or process lifetime;
- injected external scope;
- caller deciding whether to `join`;
- persistence and scheduling alternatives;
- WorkManager for durable deferrable work where appropriate.

Do not teach arbitrary repository-created scopes.

### 20. Android architecture scenarios

Cover:

- ViewModel fail-fast screen load;
- independent dashboard sections;
- repository refresh;
- user-triggered operation;
- app-scoped cache update;
- navigation away and cancellation.

### 21. Testing propagation and supervision

Use `runTest` to verify:

- sibling cancellation;
- supervised sibling survival;
- parent completion;
- timeout;
- cleanup;
- partial results;
- no leaked jobs.

### 22. Anti-patterns and decision checklist

At minimum:

- `GlobalScope`;
- hidden `CoroutineScope(...)`;
- arbitrary `SupervisorJob`;
- fire-and-forget repository work;
- unobserved Deferred;
- blanket `supervisorScope`;
- swallowing failure;
- swallowing cancellation;
- broad `NonCancellable`;
- child work escaping timeout;
- application scope used for screen work;
- screen scope used for durable work;
- `CoroutineExceptionHandler` treated as business error handling.

End with a concise decision checklist.

---

## Kotlin example requirements

Include at least:

1. a visible Job tree;
2. parent waiting for children;
3. downward cancellation;
4. regular-scope sibling failure;
5. fail-fast `coroutineScope` aggregation;
6. supervised independent children;
7. `SupervisorJob` external-scope example;
8. explicit partial-success model;
9. `withTimeout`;
10. cleanup in `finally`;
11. narrow `NonCancellable` cleanup;
12. `runTest` verifying sibling cancellation;
13. `runTest` verifying supervised survival.

Examples must be conceptually compilable.

Do not rely on timing sleeps to prove ordering when deterministic synchronization is possible.

---

## Cheat-sheet requirements

`cheat-sheet.md` must include:

- structured-concurrency invariants;
- Job-tree rules;
- cancellation/failure propagation table;
- `coroutineScope` versus `supervisorScope`;
- `Job` versus `SupervisorJob`;
- fail-fast versus best-effort guide;
- partial-success checklist;
- Deferred ownership rules;
- timeout rules;
- cleanup and NonCancellable rules;
- Android scope ownership guide;
- testing checklist;
- common smells;
- interview summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Predict the Job tree

Given nested builders, predict:

- parent-child relationships;
- completion;
- failure propagation;
- sibling cancellation;
- final observable result.

### Exercise 2 — Fail-fast feature load

Design concurrent loading where all required values must succeed.

Require:

- `coroutineScope`;
- cancellation semantics;
- error boundary;
- test for sibling cancellation.

### Exercise 3 — Best-effort dashboard

Design independent widgets where one failure must not cancel others.

Require:

- supervision;
- explicit partial result;
- observed failures;
- retry ownership;
- tests.

### Exercise 4 — Long-lived work review

Review flawed code using repository-owned ad hoc scopes, broad `SupervisorJob`, fire-and-forget work, and `NonCancellable`.

Require a corrected ownership model and a decision between screen scope, application scope, persistence, or WorkManager.

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

`interview.md` must contain approximately 18–22 substantial questions.

Cover:

- definition of structured concurrency;
- Job tree;
- parent waiting;
- downward cancellation;
- upward failure;
- sibling cancellation;
- `coroutineScope`;
- `supervisorScope`;
- `Job`;
- `SupervisorJob`;
- fail-fast;
- best-effort;
- partial success;
- Deferred failure;
- timeout;
- cleanup;
- `NonCancellable`;
- external scope;
- durable work;
- ViewModel ownership;
- testing;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-up questions where appropriate.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. structured-concurrency ownership;
2. parent completion;
3. downward cancellation;
4. sibling failure in regular scope;
5. `coroutineScope`;
6. `supervisorScope`;
7. `SupervisorJob`;
8. fail-fast versus best-effort;
9. timeout and cleanup;
10. Android scope-ownership scenario.

Distractors must be plausible.

Explanations must teach the propagation rule.

---

## References

Use official Kotlin and Android references.

At minimum inspect:

- coroutine basics and structured concurrency;
- cancellation;
- exception handling;
- supervision;
- Android coroutine best practices;
- external scope guidance;
- WorkManager guidance where durable work is discussed;
- coroutine test guidance.

Follow repository reference conventions.

Do not fabricate access dates.

---

## Relationship to grade levels

Do not define the Junior/Middle boundary in this task.

Structured concurrency is part of the complete Junior Core because a working
Android developer must understand coroutine ownership, cancellation, sibling
failure, and supervision well enough to avoid leaked or silently broken work.

The implementation report may record:

```text
Recommended level: Junior Core — advanced foundation
```

This classification is editorial documentation only unless the current schema
already supports a compatible machine-readable level.

Do not change schemas to add grade-level metadata.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 020 after successful validation;
- record eight production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- record the exact 17-topic mandatory Junior Core target;
- do not create mappings or catalog output;
- do not promote existing topics.

Add a concise roadmap note that the Junior Core is still incomplete.

Do not define a final Junior/Middle boundary yet.

The Junior Core contains exactly 17 mandatory topics. Eight currently exist as
complete production packages in `review`; nine remain:

9. Kotlin Flow and Reactive Streams
10. Android Navigation Architecture
11. Android Networking Architecture
12. Dependency Injection and Scoping
13. Android Testing Foundations
14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

The boundary may be finalized only after the full Junior Core is implemented
and reviewed.

This is an editorial curriculum decision, not a universal industry grading claim.

---

## Implementation report

Create the repository-standard report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. canonical coverage;
5. Job-tree and propagation audit;
6. supervision audit;
7. timeout and cleanup audit;
8. Android ownership audit;
9. Junior-Core completeness documentation audit;
10. content and duplication audit;
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
- schema-valid taxonomy and difficulty;
- prerequisite exists;
- no cycle;
- no modifications to existing topic packages;
- no source, competency, sequence, mapping, schema, validator, or test infrastructure changes;
- UTF-8;
- no mojibake;
- no local absolute paths.

---

## Acceptance criteria

- Six-file package exists.
- Status is `review`.
- Content version is `1`.
- Task 019 is the prerequisite.
- Structured-concurrency invariants are clear.
- Job-tree behavior is accurate.
- Failure and cancellation are distinguished.
- `coroutineScope` and `supervisorScope` are distinguished.
- `Job` and `SupervisorJob` are distinguished.
- Supervision does not hide failures.
- Fail-fast and best-effort policies are explicit.
- Partial success is modeled deliberately.
- Deferred failures are observed.
- Timeout does not leak detached work.
- Cleanup guidance is accurate.
- `NonCancellable` is narrowly constrained.
- External scope ownership is explicit.
- Durable work alternatives are discussed.
- Testing covers propagation.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Roadmap records the exact 17-topic Junior Core target, eight existing topics,
  nine remaining topics, and the deferred Junior/Middle boundary.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. propagation and supervision audit;
5. Android ownership audit;
6. Junior-Core roadmap update;
7. exact counts;
8. validation results;
9. UTF-8 audit;
10. deferred work;
11. literal `git status --short`;
12. recommended commit message.

Do not commit.
