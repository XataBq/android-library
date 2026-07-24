# Kotlin Coroutines Foundations — Practice

## Exercise 1 — Trace the execution model

### Goal

Explain coroutine ownership, ordering, suspension, and cancellation without
guessing from thread names.

### Scenario

Analyze several snippets containing a direct suspend call, two launches, two
async operations, `delay`, `Thread.sleep`, `withContext`, and parent
cancellation. Some operations depend on earlier results; others are
independent.

### Constraints

- Identify the scope and parent Job for every builder.
- Mark calls as sequential, concurrent, and only potentially parallel.
- Identify which operation blocks a thread.
- State where resumption may occur without promising a thread.
- Trace cancellation to every active child.

### Expected deliverable

An execution timeline, ownership tree, blocking/suspending table, and written
explanation for each ordering claim.

### Evaluation criteria

- Coroutine identity is not equated with thread identity.
- Direct suspend calls remain sequential.
- Concurrency is attributed only to explicitly overlapping work.
- Blocking and suspension are distinguished.
- Cancellation follows the actual Job hierarchy.

### Optional hints

Draw Job relationships first, then mark when each operation starts, suspends,
resumes, and completes.

## Exercise 2 — Repair a broken Repository

### Goal

Create a main-safe suspend contract with visible ownership and cancellation.

### Scenario

A Repository starts an unmanaged scope, performs blocking file work on Main,
wraps a single call in `async().await()`, catches `Exception` and returns an
empty value, and launches a hidden fire-and-forget cache write.

### Constraints

- The caller must own the operation lifetime.
- Blocking integration must be isolated close to its implementation.
- `CancellationException` must not become a fallback result.
- Remove unnecessary Deferred and hidden work.
- State what completion of the suspend contract guarantees.

### Expected deliverable

A defect/consequence table, corrected public contract, implementation sketch,
and cancellation/exception explanation.

### Evaluation criteria

- Main is not blocked.
- No unmanaged scope remains.
- Cancellation propagates to the caller.
- Expected I/O failure and cancellation are distinct.
- The function's return corresponds to completed promised work.

### Optional hints

Ask whether the cache write is required for success; its answer belongs in the
contract rather than in an invisible launch.

## Exercise 3 — Design concurrent aggregation

### Goal

Combine two independent results without losing structure or failure semantics.

### Scenario

A use case needs an account summary and unread count. They are independent in
one mode, but in another mode the account ID is required before messages can be
queried.

### Constraints

- Use the caller's structured lifetime.
- Concurrent mode must make both child results observable.
- Define cancellation and basic child-failure behavior.
- Keep dependent mode sequential.
- Do not introduce supervision policy beyond the stated requirements.

### Expected deliverable

Two execution plans, API sketch, Job tree, timing diagram, and test cases for
success, failure, and cancellation.

### Evaluation criteria

- Only independent work overlaps.
- No Deferred is forgotten.
- Parent cancellation stops children.
- Error behavior is explicit.
- Tests do not depend on real threads or elapsed wall time.

### Optional hints

Start both Deferred values before awaiting either one, but do not use async
when the second input cannot exist yet.

## Exercise 4 — Test coroutine behavior

### Goal

Verify delay, ordering, concurrency, and cancellation deterministically.

### Scenario

A component delays before publishing a value, starts one concurrent
aggregation, cancels stale work when its owner closes, and must publish values
in a defined order.

### Constraints

- Use `runTest` and one shared scheduler.
- Use controlled test dispatchers only where production code owns dispatching.
- Cover `runCurrent`, `advanceTimeBy`, or `advanceUntilIdle` intentionally.
- Include a cancellation assertion and a concurrency overlap assertion.
- Do not call `Thread.sleep` or inspect production thread names.

### Expected deliverable

A test matrix, fake collaborators, scheduler plan, and representative tests
without a complete production implementation.

### Evaluation criteria

- Tests use virtual rather than wall-clock time.
- Queued work is advanced explicitly.
- Ordering and overlap are observable through fakes.
- Cancellation prevents obsolete completion.
- All participating test dispatchers share one scheduler.

### Optional hints

Record start/completion events in the fake and assert the event order before
and after advancing virtual time.
