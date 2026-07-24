# Kotlin Structured Concurrency and Supervision

This topic builds on Kotlin Coroutines Foundations. It assumes you already
understand scopes, Jobs, builders, suspension, dispatchers, cancellation, and
basic exception behavior. Here the focus is lifetime-tree and failure policy.

## Learning outcomes

You will learn to predict Job propagation, select fail-fast or supervised
execution, observe every failure, constrain timeout and cleanup, assign
long-lived Android work to a real owner, and test the resulting contracts.

## 1. From coroutine syntax to lifetime design

Knowing `launch` and `async` does not answer who owns work, when a function is
complete, what happens when one child fails, or whether navigation cancels an
operation. Structured concurrency makes those answers visible in a bounded
scope.

The key question is not “which builder is shorter?” but “what result and
failure contract does the enclosing owner promise?”

## 2. Structured-concurrency invariants

Structured concurrency maintains these invariants:

```text
Every coroutine has an explicit owner.
Child work belongs to a bounded lifetime.
A parent does not complete before its children.
Parent cancellation propagates downward.
Regular child failure propagates upward and cancels siblings.
The enclosing suspend contract exposes completion or failure to its caller.
```

Supervision deliberately changes one failure edge. It does not remove
ownership, parent waiting, downward cancellation, or the need to handle errors.

## 3. Read the Job tree

Builders attach new Jobs to the current scope by default:

```kotlin
suspend fun update(repository: Repository) = coroutineScope { // scope Job
    launch {                                      // child A
        repository.updateProfile()
        launch { repository.updateAvatarIndex() } // grandchild A1
    }
    async { repository.updateMessages() }         // child B
}
```

The scope owns A and B; A owns A1. A detached `Job()` or new hidden scope would
break this tree. Draw the tree before reasoning about propagation.

## 4. Parent completion waits for children

Reaching the last statement of a parent block is not the same as completion:

```kotlin
suspend fun warmCaches(cache: Cache) = coroutineScope {
    launch {
        cache.warmProfile()
    }
    println("children launched")
}
// Returns only after warmProfile completes, fails, or is cancelled.
```

That guarantee makes the suspend contract meaningful: after normal return, its
owned children are finished. Hidden fire-and-forget work destroys this
reasoning.

## 5. Cancellation propagates downward

Canceling a parent requests cancellation of all descendants:

```kotlin
suspend fun cancelTree() = coroutineScope {
    val childrenReady = CompletableDeferred<Unit>()
    val parent = launch {
        launch { awaitCancellation() }
        launch { awaitCancellation() }
        childrenReady.complete(Unit)
    }

    childrenReady.await()
    parent.cancelAndJoin()
}
```

Children must still cooperate with cancellation. Downward propagation gives
them the same lifetime decision; it cannot forcibly stop arbitrary blocking or
non-cooperative code.

## 6. Regular child failure propagates upward

In a regular hierarchy, a child that fails with a non-
`CancellationException` cancels its parent. The parent then cancels its other
children and completes exceptionally.

Cancellation is different: a child ending with `CancellationException` does
not normally fail its parent. Do not translate cancellation into another
exception merely to report it as an application error.

## 7. Siblings cancel in fail-fast trees

One regular child failure invalidates the scope and cancels siblings:

```kotlin
suspend fun demonstrateSiblingCancellation() = coroutineScope {
    val siblingStarted = CompletableDeferred<Unit>()
    launch {
        siblingStarted.complete(Unit)
        try {
            awaitCancellation()
        } finally {
            println("sibling cancelled")
        }
    }
    launch {
        siblingStarted.await()
        error("required child failed")
    }
}
```

This is desirable when the aggregate is meaningful only if every required
child succeeds. It is not a defect to “fix” with blanket supervision.

## 8. `coroutineScope` is a fail-fast suspend boundary

`coroutineScope` creates a lexical child scope, inherits caller cancellation,
waits for children, returns its block result, and fails when required child
work fails. The caller can use ordinary suspend control flow around the whole
operation.

The lexical boundary matters: the caller is suspended until the subtree has a
final outcome. No application-long owner is introduced.

## 9. Fail-fast aggregation

Use sibling `async` for independent values that are jointly required:

```kotlin
suspend fun loadSecureProfile(
    profiles: ProfileRepository,
    permissions: PermissionRepository,
): SecureProfile = coroutineScope {
    val profile = async { profiles.load() }
    val grants = async { permissions.load() }
    SecureProfile(profile.await(), grants.await())
}
```

Failure of either child cancels the scope and the other child. This avoids
publishing a profile whose required permission snapshot is missing.

## 10. `supervisorScope` isolates direct child failures

Use supervision when children are genuinely independent and partial results
are part of the product contract:

```kotlin
private suspend fun <T> resultPreservingCancellation(
    block: suspend () -> T,
): Result<T> =
    try {
        Result.success(block())
    } catch (cancelled: CancellationException) {
        throw cancelled
    } catch (failure: Exception) {
        Result.failure(failure)
    }

suspend fun loadWidgets(
    news: NewsRepository,
    weather: WeatherRepository,
): Dashboard = supervisorScope {
    val newsResult = async { resultPreservingCancellation { news.load() } }
    val weatherResult = async { resultPreservingCancellation { weather.load() } }

    Dashboard(
        news = newsResult.await().toWidgetState(),
        weather = weatherResult.await().toWidgetState(),
    )
}
```

One child failure does not automatically cancel its sibling. Both Deferred
values are awaited, and each outcome becomes explicit state. Cancellation must
still reach the owner: the helper converts ordinary child failures into
explicit results but immediately rethrows `CancellationException`.

If the `supervisorScope` block itself throws or its caller is cancelled, its
children are cancelled. The scope still waits for children before completing.

## 11. `SupervisorJob` is for a long-lived supervising owner

`SupervisorJob` commonly defines a scope whose independent direct children can
fail without cancelling each other:

```kotlin
class ApplicationWorkOwner(
    dispatcher: CoroutineDispatcher,
) : Closeable {
    private val job = SupervisorJob()
    val scope = CoroutineScope(job + dispatcher + CoroutineName("app-work"))

    override fun close() {
        job.cancel()
    }
}
```

The application constructs, owns, injects, and closes this scope.
`supervisorScope` is a bounded suspend function; `SupervisorJob` is a Job
policy useful in an explicitly managed longer-lived scope.

Do not add `SupervisorJob()` to an arbitrary `launch` context. Replacing the
inherited Job can sever parent-child structure rather than create safe lexical
supervision.

## 12. Supervision never means error suppression

A supervised failed child still failed. A `launch` failure needs local handling
or an appropriate uncaught-exception policy. An `async` failure must be
observed through `await` or another explicit outcome contract.

Ignoring it can leave a UI section loading forever, lose diagnostics, or report
false overall success. Supervision answers “should siblings be cancelled?” It
does not answer “how is this failure represented, logged, retried, or surfaced?”

## 13. Choose fail-fast or best-effort deliberately

| Policy | Use when | Example |
|---|---|---|
| fail-fast | every value is required for a valid result | profile plus permissions |
| fail-fast | operation is one atomic preparation | transaction inputs |
| best-effort | sections are independently useful | dashboard widgets |
| best-effort | optional data may be absent | recommendations |
| best-effort | unrelated maintenance may proceed | independent cache refreshes |

Do not select supervision because it “prevents crashes.” Select it because the
domain or presentation model defines a valid partial outcome.

## 14. Model partial success explicitly

There is no universal result wrapper. Define a model that reflects the
consumer's decisions:

```kotlin
sealed interface SectionState<out T> {
    data class Content<T>(val value: T) : SectionState<T>
    data class Unavailable(val reason: FailureKind) : SectionState<Nothing>
}

data class DashboardState(
    val profile: SectionState<Profile>,
    val recommendations: SectionState<List<Recommendation>>,
)
```

The model should identify which section failed, whether existing content
remains, and who owns retry. Do not turn cancellation into `Unavailable`.

## 15. Deferred values have owners

Every `Deferred<T>` represents a result and possible failure:

```kotlin
suspend fun refreshIndependent(
    tasks: List<suspend () -> RefreshResult>,
): List<RefreshResult> = supervisorScope {
    tasks.map { task ->
        async { task() }
    }.awaitAll()
}
```

Retain and await all Deferred values inside their bounded owner. In a supervised
scope, `async` does not become self-handling; failure is rethrown by `await`.
If best-effort is required, translate each failure deliberately while
preserving cancellation.

## 16. Cancellation is not ordinary failure

Cancellation says the owner no longer needs the result. A failure says an
attempted useful operation could not complete. Catch `CancellationException`
only to add context or cleanup, then rethrow it.

Supervision does not block downward cancellation. Canceling the caller of
`supervisorScope` still cancels every child. This preserves ownership even when
child failures are isolated from siblings.

## 17. Timeout is bounded cancellation policy

`withTimeout` cancels its lexical block and throws
`TimeoutCancellationException`; `withTimeoutOrNull` returns `null` on its own
timeout:

```kotlin
suspend fun loadPreview(repository: Repository): Preview? =
    withTimeoutOrNull(2_000) {
        repository.loadPreview()
    }
```

Children launched inside the block are cancelled with it. Timeout is a product
policy, not a substitute for all lower-level network timeouts. Detached scopes
inside the block can escape this lifetime and are therefore a defect.

Timeout can race with completion. Do not acquire a resource in the timed block
and expose it without a cleanup design.

## 18. Cleanup belongs in `finally`

Non-suspending cleanup works naturally during cancellation:

```kotlin
suspend fun consume(channel: ReceiveChannel<Event>) {
    try {
        for (event in channel) process(event)
    } finally {
        channel.cancel()
    }
}
```

For a small mandatory suspending cleanup, narrow the cancellation override:

```kotlin
suspend fun useSession(session: Session) {
    try {
        session.run()
    } finally {
        withContext(NonCancellable) {
            session.closeAndFlush()
        }
    }
}
```

Keep the `NonCancellable` block minimal and bounded. It delays completion and
cannot respond normally to owner cancellation. Never wrap business work,
retries, or a whole child in it, and do not use it as a builder Job.

## 19. External and application scopes need explicit owners

Some in-process work may outlive a screen but remain disposable when the
process ends. Inject a named application-owned scope rather than creating a
Repository scope:

```kotlin
class BookmarkRepository(
    private val externalScope: CoroutineScope,
    private val store: BookmarkStore,
) {
    suspend fun bookmark(id: String) {
        externalScope.launch {
            store.write(id)
        }.join()
    }
}
```

Here the caller waits for the application-owned child, while navigation does
not cancel it. The API must state why that lifetime is required. If the caller
does not join, another observable completion contract is needed.

An application scope is still in-memory. For reliable work that must be
rescheduled after process exit or device restart, use an appropriate persistent
scheduler such as WorkManager. WorkManager is not required for ordinary
in-process suspend work.

## 20. Android architecture scenarios

A ViewModel screen load can use fail-fast aggregation when every value is
required:

```kotlin
class CheckoutViewModel(
    private val loadCheckout: LoadCheckout,
) : ViewModel() {
    fun load() {
        viewModelScope.launch {
            uiState.value = CheckoutUiState.Content(loadCheckout())
        }
    }
}
```

The use case owns the bounded child aggregation; ViewModel owns the screen
request. Navigation away clears the owner and cancels the tree.

Independent dashboard sections may use supervised partial results. A
Repository refresh normally exposes completion to its caller. A cache update
that must outlive the screen uses an injected application owner. Upload or sync
that must survive process loss crosses into WorkManager or another justified
durable mechanism.

## 21. Test propagation and supervision deterministically

Use `runTest`, shared test scheduling, and deterministic signals rather than
sleep-based races:

```kotlin
@Test
fun `regular child failure cancels sibling`() = runTest {
    val siblingCancelled = CompletableDeferred<Unit>()

    assertFailsWith<IllegalStateException> {
        coroutineScope {
            launch {
                try {
                    awaitCancellation()
                } finally {
                    siblingCancelled.complete(Unit)
                }
            }
            launch {
                yield()
                error("boom")
            }
        }
    }

    siblingCancelled.await()
}
```

Supervision should preserve the independent sibling while observing failure:

```kotlin
@Test
fun `supervised sibling completes after peer failure`() = runTest {
    val completed = CompletableDeferred<String>()

    val failed = supervisorScope {
        val first = async<String> { error("boom") }
        val second = async { completed.complete("ok") }
        second.await()
        try {
            first.await()
            null
        } catch (cancelled: CancellationException) {
            throw cancelled
        } catch (failure: IllegalStateException) {
            failure
        }
    }

    assertIs<IllegalStateException>(failed)
    assertEquals("ok", completed.await())
}
```

Also test parent waiting, caller cancellation, virtual-time timeout, `finally`,
partial-result mapping, and that the test scope has no unintended unfinished
children.

## 22. Anti-patterns and decision checklist

Watch for:

- `GlobalScope` or hidden `CoroutineScope(...)`;
- arbitrary `SupervisorJob` added to a child builder;
- Repository fire-and-forget work with no owner or result;
- unobserved Deferred values;
- blanket `supervisorScope` around required results;
- supervised failures ignored rather than represented;
- swallowed failure or `CancellationException`;
- broad `NonCancellable` business work;
- child work escaping timeout into another scope;
- application scope used for screen-only work;
- screen scope used for work claimed to be durable;
- `CoroutineExceptionHandler` treated as domain error handling.

Decision checklist:

```text
Who owns the subtree?
When may the owner complete?
Are all child results required?
Should one failure cancel siblings?
How is every failure observed?
Can partial success be represented honestly?
Does timeout cancel every owned child?
Is cleanup non-suspending or narrowly NonCancellable?
May work outlive the screen, process, or device restart?
Which deterministic test proves the propagation rule?
```

Use a regular scope for one fail-fast result. Use supervision only for
independent children with explicit outcome handling. Choose an external scope
or durable scheduler from the real lifetime requirement, never as an escape
from structured ownership.
