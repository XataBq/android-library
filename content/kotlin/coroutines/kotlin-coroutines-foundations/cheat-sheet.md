# Kotlin Coroutines Foundations — Cheat sheet

## Core model

```text
Coroutine  = cancellable computation
Scope      = lifetime owner
Context    = Job, Dispatcher, name, and other execution elements
Job        = lifecycle and parent-child hierarchy
Dispatcher = scheduling policy for runnable work
Thread     = actual JVM/OS execution resource
```

A running coroutine executes on a thread. A suspended coroutine does not need
to block that thread and may resume on another eligible thread.

## What `suspend` means

- the function may suspend before returning;
- it may call other suspend functions;
- it does not create a coroutine;
- it does not select IO or background execution;
- it does not convert blocking APIs into non-blocking APIs;
- calls remain sequential unless concurrency is explicitly introduced.

## Scope, context, and Job

- Launch only in a scope whose owner and cancellation point are known.
- Builders inherit context and create child Jobs by default.
- Parent cancellation reaches children.
- Parent completion waits for children.
- An unhandled child failure normally affects its hierarchy.
- Advanced supervision policies belong to a later topic.

## Dispatcher guide

| Dispatcher | Use |
|---|---|
| Main | UI-confined work |
| Default | CPU-intensive computation |
| IO | blocking I/O integration |
| Unconfined | specialized cases, not normal application work |

Dispatchers are not single threads. Do not depend on pool sizes or thread
names. Put dispatcher selection near the blocking or CPU-heavy implementation.

## `launch`, `async`, and `withContext`

| API | Returns | Use |
|---|---|---|
| `launch` | `Job` | owned work without a direct value |
| `async` | `Deferred<T>` | deliberate concurrent result |
| `withContext` | block result | sequential context change |

- Direct suspend call: sequential result.
- Two sibling `async` calls before awaiting: concurrent results.
- `async { work() }.await()`: normally unnecessary.
- Forgotten Deferred: unclear result and failure contract.

## Sequential, concurrent, parallel

- Sequential: B starts after A returns.
- Concurrent: lifetimes overlap.
- Parallel: instructions execute simultaneously on separate resources.

Concurrency permits but does not guarantee parallelism. Preserve sequential
order when B depends on A.

## Blocking versus suspending

- `Thread.sleep`: blocks the current thread.
- `delay`: suspends the coroutine.
- Blocking file/JDBC/socket code remains blocking inside `suspend`.
- Prefer suspending clients or isolate blocking integration on IO.
- Never use `runBlocking` on Android Main.

## Cancellation checklist

- Cancellation is cooperative.
- Cancellable suspensions check the Job.
- CPU loops use `ensureActive`, `isActive`, or `yield`.
- Rethrow `CancellationException`.
- Cleanup resources in `finally`.
- Do not publish normal success after cancellation.
- Do not detach children into unmanaged scopes.

## Exception basics

- `launch` has no returned result channel for failure.
- `async` exposes failure through `await` and remains part of the hierarchy.
- Catch around the suspending operation, not merely around a builder call.
- `CoroutineExceptionHandler` is not universal catch-all logic.
- Expected domain/data failures remain separate from cancellation.

## Android scope guide

- `viewModelScope`: UI-scenario work; cancelled when ViewModel is cleared.
- `lifecycleScope`: work bounded by Lifecycle destruction.
- `repeatOnLifecycle`: restartable child work for active lifecycle states.
- Compose effect/remembered scope: composition-owned UI work.
- Longer-lived work: explicit application or persistent-work owner.

Scope length must match usefulness; the longest scope is not the safest.

## Layer boundary guide

- UI/ViewModel decides when UI-scenario work starts.
- Domain exposes focused suspend or Flow contracts.
- Data hides blocking/suspending source details.
- Suspend contracts should be safe to call from Main.
- The implementation doing blocking or CPU work selects appropriate execution.
- Repository must not hide caller-owned fire-and-forget work.

## Testing checklist

- use `runTest`;
- share one `TestCoroutineScheduler`;
- use test dispatchers for code that owns dispatching;
- advance with `runCurrent`, `advanceTimeBy`, or `advanceUntilIdle`;
- avoid real sleeps and wall-clock waits;
- assert results, ordering, cancellation, and child behavior;
- do not assert production thread names.

## Common smells

- `GlobalScope`;
- new scope inside every method;
- suspend assumed to mean background;
- immediate `async`/`await`;
- blocking Main;
- hardcoded dispatchers everywhere;
- swallowed cancellation;
- forgotten Deferred;
- endless CPU loop without checks;
- hidden retry or fire-and-forget repository work;
- handler added instead of defining error ownership.

## Interview-ready summary

A coroutine is an owned cancellable computation, not a thread. A scope and Job
define lifetime, a context carries execution elements, and a dispatcher
schedules runnable segments on threads. Suspension releases a thread; it does
not imply background execution. Choose builders by result and concurrency,
preserve cancellation, isolate blocking work, and test with controlled time.
