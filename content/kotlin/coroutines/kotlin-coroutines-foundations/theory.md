# Kotlin Coroutines Foundations

This topic assumes the existing UI, Data, Domain, ViewModel, and lifecycle
ownership boundaries. It deepens the execution and cancellation mechanics
behind their suspend and Flow contracts. Advanced supervision and structured
concurrency design remain separate topics.

## Learning outcomes

You will learn to model a coroutine as an owned cancellable computation,
distinguish suspension from thread blocking, choose builders and dispatchers by
responsibility, preserve cancellation, and test behavior with virtual time.

## 1. Why coroutines exist

Applications often wait for network, database, timers, or user-driven work
while the UI must stay responsive. Callbacks can represent that waiting, but
nested callbacks make ordering, errors, and cancellation harder to see.
Coroutines let asynchronous code retain a sequential-looking control flow.

A coroutine does not make an operation concurrent or parallel merely by
existing. A plain sequence of suspend calls is still sequential. Concurrency
appears only when work is deliberately started so executions can overlap.

## 2. Coroutine, thread, and task are different

A coroutine is a cancellable computation that can suspend and resume. A thread
is an OS/JVM execution resource on which instructions actually run. “Task” is
an informal problem description, not a precise coroutine type.

When a coroutine is running on the JVM, a thread executes it. When it suspends,
it can release that thread for other work. Later, a dispatcher schedules its
resumption on an eligible thread. Many coroutines can share threads, but that
does not justify the misleading identity “coroutine = lightweight thread.”

Resource cost and performance depend on workload, dispatcher, runtime, and
platform. Avoid universal thread-count or speed claims.

## 3. A suspend function may suspend

The `suspend` modifier allows a function to call other suspend functions and
pause before returning. It does not start a coroutine, select a dispatcher, or
move execution off Main.

```kotlin
suspend fun loadGreeting(api: GreetingApi): String {
    val user = api.currentUser()       // May suspend.
    val greeting = api.greeting(user)  // Runs after currentUser returns.
    return greeting
}
```

These calls are sequential. If either implementation performs blocking work on
the caller's thread, the `suspend` keyword does not transform that work into
non-blocking behavior.

## 4. Continuation and resumption

Conceptually, suspension follows this path:

```text
run
→ reach a suspension point
→ retain enough continuation state to proceed later
→ release the current thread
→ awaited event completes
→ dispatcher schedules the continuation
→ resume from the suspension point
```

A suspend call is a possible suspension point; it need not actually suspend
when its result is already available. The continuation represents “what
happens next,” not a dedicated thread parked beside the coroutine. Compiler
and runtime implementation details beyond this public model are not required
for correct application design.

## 5. CoroutineScope owns lifetime

`CoroutineScope` supplies a `coroutineContext` and defines the lifetime into
which builders launch work. It is an ownership boundary, not a convenient bag
of functions.

Canceling the scope's Job cancels its active children. An ad hoc or global
scope detaches work from the screen, request, or application component that
needs it. Before calling `launch`, identify who should cancel the work and how
long it remains useful.

Use framework scopes or an explicitly managed application scope where their
lifetimes match. Do not manufacture a new scope inside each function to escape
the caller's cancellation.

## 6. CoroutineContext describes execution elements

`CoroutineContext` is a collection of keyed elements. Common elements include:

- `Job`, which represents lifecycle and hierarchy;
- `CoroutineDispatcher`, which schedules runnable work;
- `CoroutineName`, which can improve diagnostics;
- `CoroutineExceptionHandler`, which handles limited uncaught-root cases.

Builders inherit their scope's context and can add or replace elements. A
context is not the coroutine's business result and a dispatcher is not its
lifetime owner. The Job and dispatcher answer different questions.

## 7. Job creates a parent-child hierarchy

A builder normally creates a child Job of the current scope. A parent waits
for its children before completing. Canceling a parent cancels its children.
An unhandled child failure normally cancels its parent and sibling subtree;
advanced supervision changes that policy and is deferred.

```kotlin
suspend fun refreshAll(repository: Repository) = coroutineScope {
    val cache = launch { repository.refreshCache() }
    launch { repository.refreshProfile() }

    cache.join()
    // coroutineScope still waits for every child before returning.
}
```

`Job` reports states such as active, completing, completed, or cancelled.
`Deferred<T>` is also a Job and adds an eventual result. Parent-child structure
keeps completion and cancellation visible to the owner.

## 8. Dispatchers select execution policy

The standard choices have distinct purposes:

| Dispatcher | Typical use |
|---|---|
| `Dispatchers.Main` | UI-confined work and Android presentation state |
| `Dispatchers.Default` | CPU-intensive computation |
| `Dispatchers.IO` | integration with blocking I/O |
| `Dispatchers.Unconfined` | specialized low-level cases; not a normal app default |

A dispatcher can use multiple threads, and a thread can execute many coroutine
segments over time. Pool sizes and scheduler internals are not stable
application guarantees. Select by the work's contract, not by assumed thread
names.

Main must remain responsive. IO does not make a blocking API cancellable; it
keeps that blocking call away from Main. Default does not make an algorithm
parallel unless several computations actually overlap.

## 9. Coroutine identity is independent of thread identity

Logging can demonstrate that code before and after suspension has one
coroutine control flow without promising the same physical thread:

```kotlin
suspend fun logAroundDelay() = withContext(Dispatchers.Default) {
    println("before: ${Thread.currentThread().name}")
    delay(100)
    println("after: ${Thread.currentThread().name}")
}
```

The names may match or differ. Both results are valid. Dispatcher confinement
defines eligible execution, not a guarantee that one coroutine owns one
thread. Code that relies on thread-local state needs explicit context
propagation or confinement.

## 10. `launch` starts owned work and returns Job

Use `launch` when the scope owns an operation and the caller needs lifecycle or
completion control rather than a direct value:

```kotlin
fun CoroutineScope.refresh(repository: Repository): Job =
    launch {
        repository.refresh()
    }
```

`launch` returns immediately with a `Job`; `join()` can wait for completion.
Starting a launch does not prove parallel execution—it only permits overlap
according to suspension and scheduling. An unhandled `launch` exception follows
the Job hierarchy rather than waiting for a result consumer.

## 11. `async` represents a concurrent result

`async` returns `Deferred<T>`. Use it when independent result-producing
operations should overlap and their results are both needed:

```kotlin
suspend fun loadDashboard(
    accounts: AccountRepository,
    messages: MessageRepository,
): Dashboard = coroutineScope {
    val account = async { accounts.loadCurrent() }
    val unread = async { messages.loadUnreadCount() }
    Dashboard(account.await(), unread.await())
}
```

`await()` suspends until the result is available and rethrows failure. The
Deferred still participates in the parent hierarchy; it is not a detached
future.

This counterexample adds ceremony but no useful concurrency:

```kotlin
suspend fun loadAccount(repository: AccountRepository): Account =
    coroutineScope {
        async { repository.loadCurrent() }.await()
    }
```

Call the suspend function directly. A Deferred that is never awaited or
otherwise deliberately observed is a smell: its result and failure contract
are unclear.

## 12. `withContext` changes context sequentially

`withContext` runs a block in a derived context, suspends the caller, and
returns the block's result. It does not detach the block from the caller's Job.

```kotlin
class FileDocumentSource(
    private val ioDispatcher: CoroutineDispatcher,
) {
    suspend fun read(path: Path): String =
        withContext(ioDispatcher) {
            Files.readString(path) // Blocking integration kept off Main.
        }
}
```

From the caller's perspective this remains one sequential operation. Put the
dispatcher switch near the blocking or CPU-intensive implementation so callers
receive a main-safe suspend contract without knowing file or JDBC details.

## 13. Sequential, concurrent, and parallel are distinct

Sequential work preserves dependency order:

```kotlin
val token = authenticate()
val profile = loadProfile(token)
```

Independent operations can be concurrent with sibling `async` children.
Concurrency means their lifetimes overlap. Parallelism means instructions
actually execute simultaneously on different resources and depends on the
dispatcher, available threads/cores, and workload.

Do not parallelize dependent work or use `async` as a performance decoration.
Define error and cancellation behavior for the whole aggregation.

## 14. Blocking and suspending consume resources differently

`Thread.sleep(1_000)` blocks its thread. `delay(1_000)` suspends the coroutine
and frees the thread for other work. A blocking file, JDBC, or socket API
continues to block even when called from a suspend function.

```kotlin
suspend fun waitWithoutBlockingThread() {
    delay(1_000)
}

fun blockCurrentThread() {
    Thread.sleep(1_000)
}
```

Prefer a genuine suspending client when available. Otherwise isolate blocking
integration on an appropriate dispatcher. Never use `runBlocking` in Android
UI code; it bridges by blocking the current thread.

## 15. Cancellation is cooperative

Canceling a Job requests cancellation. Cancellable suspending functions check
the request and throw `CancellationException`. CPU loops without suspension
must check explicitly:

```kotlin
suspend fun checksum(bytes: ByteArray): Long =
    withContext(Dispatchers.Default) {
        var result = 0L
        bytes.forEachIndexed { index, byte ->
            if (index % 1_024 == 0) ensureActive()
            result = result * 31 + byte
        }
        result
    }
```

`ensureActive()` throws when the current Job is cancelled. `yield()` can both
offer other work an execution opportunity and check cancellation. Choose a
check frequency that balances responsiveness and overhead.

## 16. Preserve CancellationException

Cancellation is control flow, not an ordinary domain failure. A broad catch
must rethrow it:

```kotlin
suspend fun loadResult(repository: Repository): LoadResult =
    try {
        LoadResult.Success(repository.load())
    } catch (cancelled: CancellationException) {
        throw cancelled
    } catch (failure: IOException) {
        LoadResult.Unavailable(failure)
    }
```

`catch (Exception)` and `catch (Throwable)` can accidentally swallow
`CancellationException`, allowing obsolete work and UI updates to continue.
Put resource cleanup in `finally`; use `NonCancellable` only for a small
cleanup suspension that genuinely must finish, not to continue business work.

## 17. Parent cancellation reaches children

Cancellation propagation makes lifetime ownership observable:

```kotlin
suspend fun demonstrateParentCancellation() = coroutineScope {
    val parent = launch {
        launch {
            try {
                awaitCancellation()
            } finally {
                println("child cleaned up")
            }
        }
    }

    parent.cancelAndJoin()
}
```

The child belongs to the parent and is cancelled with it. Creating another Job
or scope inside the child would break that relationship. Cleanup still runs,
but cancelled code should not publish normal success afterward.

## 18. Exception behavior depends on builder and hierarchy

An unhandled exception from a child normally cancels its parent hierarchy.
`launch` has no result channel in which to store failure. `async` exposes
failure through `await`, while its Job still participates in hierarchy.
Therefore, try/catch placement matters: catching around `launch { ... }` after
the builder returns does not catch a later child failure.

`CoroutineExceptionHandler` observes limited uncaught exceptions for root-like
coroutines; it is not a universal try/catch and does not replace domain error
modeling. Expected network or validation failures should be translated at the
appropriate Data/Domain/UI boundary. Advanced `supervisorScope`,
`SupervisorJob`, and partial-failure policies are deferred.

## 19. Android scopes express UI ownership

`viewModelScope` owns UI-scenario work and is cancelled when the ViewModel is
cleared. `lifecycleScope` is cancelled when its Lifecycle is destroyed.
`repeatOnLifecycle` starts and cancels a child block as visibility state
changes. Compose effects and remembered scopes follow their composition owner.

```kotlin
class ProfileViewModel(
    private val refreshProfile: RefreshProfile,
) : ViewModel() {
    fun refresh() {
        viewModelScope.launch {
            refreshProfile()
        }
    }
}
```

No scope fits every task. A UI-triggered operation that must outlive its
ViewModel needs a deliberate longer-lived application or persistent-work
owner; hiding it in `GlobalScope` does not create durability.

## 20. Layer boundaries keep execution decisions local

The UI or ViewModel owns when a UI scenario starts. Domain exposes focused
suspend or Flow contracts. Data owns source coordination and isolates blocking
or suspending implementation details.

Official Android guidance calls suspend functions main-safe: callers should be
able to invoke them from Main while the class doing long blocking or CPU work
moves that work appropriately. This does not require injecting a dispatcher
into every pure class. Inject execution policy where production code genuinely
selects it and tests need control.

Repositories should not secretly fire-and-forget caller-owned actions. A
suspend function should normally complete when its promised work completes or
fail/cancel visibly. Durable background work needs an explicit owner and
contract beyond this foundation topic.

## 21. Test with controlled coroutine time

`runTest` creates a test scope and scheduler. Test dispatchers use virtual time,
so delays can advance without real wall-clock waiting:

```kotlin
@Test
fun `refresh publishes result after delay`() = runTest {
    val repository = FakeRepository(delayMillis = 5_000)
    val result = async { repository.refresh() }

    assertFalse(result.isCompleted)
    advanceTimeBy(5_000)
    runCurrent()

    assertEquals("updated", result.await())
}
```

All test dispatchers involved should share the test scheduler. Use
`runCurrent`, `advanceTimeBy`, or `advanceUntilIdle` deliberately. Inject a
dispatcher or scope only where code owns scheduling; assert results, ordering,
cancellation, and collaboration rather than thread names or private calls.

## 22. Anti-pattern review and decision checklist

Watch for:

- `GlobalScope` or ad hoc scopes without a lifetime owner;
- “one coroutine equals one lightweight thread”;
- assuming `suspend` means background execution;
- `async` immediately followed by `await`;
- forgotten Deferred results;
- blocking Main with sleep, file, JDBC, socket, or `runBlocking`;
- hardcoded Main/IO scattered through every layer;
- wrapping every pure function in `withContext`;
- swallowing `CancellationException`;
- CPU loops without cancellation checks;
- fire-and-forget repository work;
- unnecessary `CoroutineExceptionHandler`;
- hidden retry loops that ignore cancellation;
- lifecycle work launched from the wrong owner.

Use this decision sequence:

```text
Who owns this work and cancels it?
Does the caller need a result?
Must independent operations overlap?
Can the implementation suspend, block, or consume CPU?
Which dispatcher is justified closest to that implementation?
How do cancellation and failure propagate?
How will virtual-time tests observe the contract?
```

Choose `launch` for owned resultless work, direct suspend calls for sequential
results, `async` for deliberate concurrent results, and `withContext` for a
sequential context change. Keep Job hierarchy intact and treat cancellation as
part of the public behavior.
