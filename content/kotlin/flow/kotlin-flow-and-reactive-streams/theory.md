# Kotlin Flow and Reactive Streams

This topic builds on coroutine foundations and structured concurrency. It
focuses on stream semantics: when work starts, who owns collection and sharing,
which values may be skipped, how failures cross an operator pipeline, and how
Android lifecycle changes affect subscribers.

## Learning outcomes

You will learn to distinguish one-shot suspend results from streams, reason
about cold and hot execution, select operators by their cancellation and
throughput semantics, expose immutable state, and test finite and infinite
flows without leaking collectors.

## 1. One asynchronous value versus a stream

A suspend function represents one eventual completion. `Flow<T>` represents
zero, one, or many values over time:

```kotlin
interface UserRepository {
    suspend fun loadUser(id: String): User
    fun observeUser(id: String): Flow<User>
}
```

Use the suspend contract for a one-shot action or snapshot. Use Flow when
changes after the first value are part of the contract. A Flow is not justified
merely because implementation work is asynchronous.

## 2. A cold Flow starts once per collector

Most flows built with `flow`, `flowOf`, or operators are cold. Their upstream
code starts independently for each collector:

```kotlin
var starts = 0
val cold = flow {
    starts += 1
    emit("run-$starts")
}

val first = cold.first()  // run-1
val second = cold.first() // run-2
```

Repeated collection can repeat database queries, callback registration, or
network work. Coldness describes subscription behavior; it does not imply a
particular thread or inexpensive execution.

## 3. Build a Flow with `flow` and `emit`

The `flow` builder runs when collected and emits sequentially:

```kotlin
fun observeCountdown(): Flow<Int> = flow {
    for (value in 3 downTo 1) {
        delay(100)
        emit(value)
    }
}
```

Suspending calls and `emit` cooperate with cancellation. An unhandled upstream
exception completes collection exceptionally. The builder must preserve Flow
context rules; use purpose-built builders such as `callbackFlow` when multiple
callbacks or concurrent senders must feed one stream.

## 4. Collection is terminal and suspending

Intermediate operators describe a pipeline. A terminal operator starts a cold
pipeline and suspends until its own completion rule is satisfied:

```kotlin
suspend fun consume(repository: ArticleRepository) {
    repository.observeArticles().collect { articles ->
        renderCount(articles.size)
    }
}

suspend fun firstArticle(repository: ArticleRepository): Article =
    repository.observeArticles().first()
```

`collect` normally waits for upstream completion. `first` cancels collection
after one value. `toList` is appropriate only when the stream is known to be
finite; using it on a never-ending hot stream would wait forever.

## 5. Intermediate and terminal operators

Intermediate operators return another cold Flow and do not run it by
themselves. Terminal operators consume it:

```kotlin
val visibleTitles: Flow<String> =
    repository.observeArticles()        // source
        .map { articles -> articles.filter(Article::visible) }
        .map { articles -> articles.map(Article::title) }
        .transform { titles -> titles.forEach { emit(it) } }

val count: Int = visibleTitles.count() // terminal operator
```

By default, upstream, intermediate operators, and the collector execute
sequentially in one coroutine. Operators such as `buffer` and sharing operators
introduce deliberate concurrency boundaries.

## 6. Map, filter, transform, and onEach

Choose an operator that communicates intent:

```kotlin
val auditReadyNames: Flow<String> =
    users
        .filter(User::active)
        .map(User::displayName)
        .transform { name ->
            emit(name.trim())
            if (name.isBlank()) emit("Anonymous")
        }
        .onEach { name -> audit.recordSeenName(name) }
```

`map` makes one output per input, `filter` retains matching inputs,
`transform` may emit any number of outputs, and `onEach` performs a suspending
side effect while passing the original value downstream. Keep side effects
owned and observable; `onEach` does not make fire-and-forget work safe.

## 7. Flow preserves its collection context

A regular Flow encapsulates its upstream context and must not emit from an
arbitrary foreign context inside `flow`:

```kotlin
fun observeDocuments(source: DocumentSource): Flow<List<Document>> =
    flow {
        emit(source.readDocuments())
    }
```

The collector chooses its context, while the upstream implementation can apply
`flowOn` at the boundary that owns blocking or CPU-intensive work. Do not wrap
`emit` in an unrelated `withContext`. If concurrent producers are genuinely
required, choose `channelFlow` and define their ownership explicitly.

## 8. `flowOn` changes only its upstream

`flowOn` moves the operators before it to the supplied context; downstream
operators and the collector retain the collector's context:

```kotlin
val summaries: Flow<Summary> =
    repository.observeRawRecords()
        .map(parser::parse)
        .flowOn(Dispatchers.Default)
        .map(presenter::toSummary)

withContext(Dispatchers.Main) {
    summaries.collect(view::render)
}
```

This differs from wrapping collection in `withContext`, which changes the
context of the entire collection call. `flowOn` may create a coroutine and
buffer boundary, so place it deliberately and avoid stacking dispatchers
without a responsible upstream operation.

## 9. Handle upstream failures without swallowing cancellation

`catch` sees exceptions from operators placed before it, not failures thrown by
later operators or the collector. Use it to translate expected upstream
failures, and preserve owner cancellation explicitly:

```kotlin
val state: Flow<FeedState> =
    repository.observeFeed()
        .map<Feed, FeedState>(FeedState::Content)
        .catch { failure ->
            when (failure) {
                is CancellationException -> throw failure
                is IOException -> emit(FeedState.Offline)
                else -> throw failure
            }
        }
        .onCompletion { cause ->
            metrics.collectionFinished(cancelledOrFailed = cause != null)
        }
```

Flow's `catch` operator is cancellation-transparent, but the explicit branch
keeps translation policy obvious and safe if the block is later refactored.
`onCompletion` observes normal completion, failure, or cancellation; it is not
a blanket recovery operator. Domain failures represented as values should not
be confused with broken stream execution.

## 10. Retry is bounded policy

Retry re-collects upstream. Bound it by failure type and attempt count:

```kotlin
val updates: Flow<Update> =
    remote.observeUpdates()
        .retryWhen { failure, attempt ->
            val retryable = failure is IOException && attempt < 2
            if (retryable) delay(250L * (attempt + 1))
            retryable
        }
```

This allows at most two retries after the initial attempt. Backoff values,
connectivity policy, and user-triggered retry belong to the responsible layer.
Never hide an infinite retry loop in a repository contract, and never retry
programming errors merely because they are `Throwable`.

## 11. Throughput requires an explicit loss policy

When a producer is faster than its consumer, decide what must happen:

| Strategy | Effect | Appropriate when |
|---|---|---|
| sequential | producer waits for consumer | every value and order matter |
| `buffer` | producer and consumer overlap | every value matters, bounded lag is acceptable |
| `conflate` | intermediate pending values may be skipped | only the latest state matters |
| `collectLatest` | previous collector block is cancelled | old processing becomes obsolete |

These are semantic choices, not automatic performance switches. Skipping a
state snapshot may be valid; skipping a payment command is not.

## 12. `buffer` overlaps upstream and downstream

Without a buffer, emission waits for downstream processing. A buffer allows
bounded overlap while retaining values:

```kotlin
suspend fun indexAll(files: Flow<FileRecord>) {
    files
        .map(reader::read)
        .buffer(capacity = 16)
        .collect(index::store)
}
```

The producer may run ahead until capacity is reached, then suspends. Buffering
changes scheduling and memory use but does not make work durable or detach it
from the collecting scope.

## 13. `conflate` keeps the latest pending state

Conflation is appropriate when intermediate states lose value after a newer
state exists:

```kotlin
suspend fun renderTelemetry(states: Flow<TelemetryState>) {
    states
        .conflate()
        .collect(chart::render)
}
```

A slow renderer may skip intermediate telemetry snapshots but receives the
latest available value. Do not conflate commands, audit records, or any stream
where every element must be processed.

## 14. `collectLatest` cancels obsolete collector work

`collectLatest` cancels the previous collector block when a new value arrives:

```kotlin
suspend fun renderPreviews(requests: Flow<PreviewRequest>) {
    requests.collectLatest { request ->
        val bitmap = previewRenderer.render(request)
        previewView.show(bitmap)
    }
}
```

Cancellation must be safe for `render`. Use this for latest-wins presentation
work. Use ordinary `collect` when every element must reach completion.

## 15. Combine, zip, and merge answer different questions

`combine` emits a new coherent result whenever either source changes, after
both have emitted at least once:

```kotlin
val checkout: Flow<CheckoutState> =
    combine(cartRepository.observeCart(), accountRepository.observeAccount()) {
        cart, account ->
        CheckoutState(cart = cart, canPurchase = account.enabled)
    }
```

`zip` pairs values one-to-one. `merge` interleaves same-typed values without
pairing:

```kotlin
val numberedPairs: Flow<Pair<Int, String>> =
    numbers.zip(labels, ::Pair)

val allAlerts: Flow<Alert> =
    merge(systemAlerts, accountAlerts)
```

Use `combine` for values that jointly form one snapshot, `zip` for positional
pairs, and `merge` for independent occurrences. Do not combine unrelated UI
concerns merely because they share a screen.

## 16. `flatMapLatest` replaces obsolete child streams

When a selector changes, `flatMapLatest` cancels collection of the previous
inner Flow and switches to the newest. In the current kotlinx.coroutines API
documentation, `debounce` is marked `@FlowPreview` and `flatMapLatest` is
marked `@ExperimentalCoroutinesApi`, so this example opts in explicitly:

```kotlin
@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)
fun searchResults(
    queries: Flow<String>,
    repository: SearchRepository,
): Flow<List<SearchResult>> =
    queries
        .debounce(300)
        .map(String::trim)
        .distinctUntilChanged()
        .flatMapLatest { query ->
            if (query.isEmpty()) flowOf(emptyList())
            else repository.search(query)
        }
```

This expresses latest-wins search or route selection. It is wrong when every
submitted operation must complete. Cancellation of the old inner Flow must
propagate through its repository work. API markers can change between
kotlinx.coroutines releases: verify the declarations and required opt-ins
against the version installed in the project, and keep each opt-in as narrow as
practical.

## 17. Hot streams exist independently of a collector

The core hot primitives have different contracts:

| Type | Core meaning | New subscriber behavior | Consumer relationship |
|---|---|---|---|
| `StateFlow<T>` | current state | immediately receives current value | broadcast |
| `SharedFlow<T>` | configured shared emissions | receives replay cache, then new values | broadcast |
| `Channel<T>` | send/receive communication | no automatic state replay | receivers compete |

Hot does not mean global. Every mutable producer and sharing coroutine still
needs an owner and a bounded lifetime.

## 18. StateFlow represents current state

`StateFlow` always has a current value and uses equality-based conflation:

```kotlin
class DownloadStateHolder {
    private val _state = MutableStateFlow<DownloadState>(DownloadState.Idle)
    val state: StateFlow<DownloadState> = _state.asStateFlow()

    fun update(progress: Int) {
        _state.value = DownloadState.Running(progress)
    }
}
```

Expose the read-only type. Model a truthful initial value. A slow collector may
observe the latest state rather than every rapid intermediate assignment.
StateFlow is therefore not a default one-off event queue.

## 19. SharedFlow broadcasts configured emissions

`SharedFlow` can replay recent values and buffer for slow subscribers:

```kotlin
class RefreshSignals {
    private val _signals = MutableSharedFlow<RefreshSignal>(
        replay = 0,
        extraBufferCapacity = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST,
    )
    val signals: SharedFlow<RefreshSignal> = _signals.asSharedFlow()

    fun request(source: RefreshSource): Boolean =
        _signals.tryEmit(RefreshSignal(source))
}
```

Every active subscriber sees broadcast emissions. Replay controls what a late
subscriber receives; it is not unlimited history. With no replay, subscriber
timing can mean an occurrence is missed. Use an explicit state model when the
outcome must survive collector absence.

## 20. Channel coordinates senders and receivers

A Channel models communication where receivers consume elements:

```kotlin
suspend fun processCommands(
    commands: ReceiveChannel<Command>,
    handler: CommandHandler,
) {
    for (command in commands) {
        handler.handle(command)
    }
}
```

An unbuffered Channel is rendezvous: send and receive meet. A buffered Channel
allows limited producer lead. Multiple receivers compete, so one element is
normally handled by one receiver rather than broadcast to all. Convert with
`receiveAsFlow` or `consumeAsFlow` only after choosing the required
single-consumer or fan-out semantics.

## 21. `stateIn`, `shareIn`, and `SharingStarted` require an owner

`stateIn` shares the latest state in a supplied scope. Its initial value must be
truthful before upstream produces:

```kotlin
class ProfileViewModel(
    repository: ProfileRepository,
) : ViewModel() {
    val uiState: StateFlow<ProfileUiState> =
        repository.observeProfile()
            .map<Profile, ProfileUiState>(ProfileUiState::Content)
            .catch { failure ->
                if (failure is CancellationException) throw failure
                emit(ProfileUiState.Error)
            }
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(),
                initialValue = ProfileUiState.Loading,
            )
}
```

`shareIn` shares emissions and configures replay:

```kotlin
val sharedMessages: SharedFlow<Message> =
    backendMessages
        .shareIn(
            scope = applicationScope,
            started = SharingStarted.Lazily,
            replay = 1,
        )
```

`Eagerly` starts immediately and keeps running, `Lazily` starts at the first
subscriber and then keeps running, and `WhileSubscribed` starts and stops
according to subscriber presence. Stop timeouts and replay expiration are
product policies, not magic constants. The scope must live exactly as long as
the shared resource should live.

## 22. Android UI collection follows UI lifecycle

For a Fragment, collect against the View lifecycle and launch independent
collectors in parallel:

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        launch { viewModel.uiState.collect(::render) }
        launch { viewModel.effects.collect(::handleEffect) }
    }
}
```

The block is cancelled below `STARTED` and restarted when active again. Compose
uses lifecycle-aware state collection:

```kotlin
@Composable
fun ProfileRoute(viewModel: ProfileViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ProfileScreen(state = state, onAction = viewModel::onAction)
}
```

A plain UI `launch { flow.collect(...) }` can keep processing while a View UI
is stopped. ViewModel exposes the contract; the UI owns its lifecycle threshold.

## 23. Keep Flow boundaries aligned with architecture

Each layer owns a different decision:

```kotlin
interface UserRepository {
    fun observeUser(id: UserId): Flow<User>
}

class ObserveProfile(
    private val users: UserRepository,
) {
    operator fun invoke(id: UserId): Flow<Profile> =
        users.observeUser(id).map(User::toProfile)
}

@OptIn(ExperimentalCoroutinesApi::class)
class ProfileViewModel(
    observeProfile: ObserveProfile,
    savedStateHandle: SavedStateHandle,
) : ViewModel() {
    private val id = savedStateHandle.getStateFlow("user-id", UserId.None)

    val uiState: StateFlow<ProfileUiState> =
        id.flatMapLatest(observeProfile::invoke)
            .map<Profile, ProfileUiState>(ProfileUiState::Content)
            .stateIn(
                viewModelScope,
                SharingStarted.WhileSubscribed(),
                ProfileUiState.Loading,
            )
}
```

Data owns source access and normalization. A Domain use case may expose a
focused stream when reusable application logic justifies it. ViewModel produces
presentation state. UI collects lifecycle-aware. Never expose a mutable Flow
type or force lifecycle APIs into Repository or Domain code.

## 24. Test stream contracts and review anti-patterns

Use finite terminal operators when possible:

```kotlin
@Test
fun `cold flow transforms every value`() = runTest {
    val actual = flowOf(1, 2, 3)
        .map { it * 2 }
        .toList()

    assertEquals(listOf(2, 4, 6), actual)
}
```

For a hot stream, start its sharing collector and assert current state without
waiting for infinite completion:

```kotlin
@Test
fun `stateIn exposes latest value`() = runTest {
    val source = MutableSharedFlow<Int>()
    val state = source.stateIn(
        scope = backgroundScope,
        started = SharingStarted.Eagerly,
        initialValue = 0,
    )
    runCurrent()

    source.emit(7)
    runCurrent()

    assertEquals(7, state.value)
}
```

SharedFlow tests can start an infinite collector in `backgroundScope` and
cancel it explicitly:

```kotlin
@Test
fun `shared flow collector stops on cancellation`() = runTest {
    val source = MutableSharedFlow<Int>()
    val actual = mutableListOf<Int>()
    val collector = backgroundScope.launch {
        source.collect { actual += it }
    }
    runCurrent()

    source.emit(4)
    runCurrent()
    collector.cancelAndJoin()

    assertEquals(listOf(4), actual)
}
```

Use the test scheduler for delays and retry timing. Bound infinite collection
with `first`, `take`, cancellation, or a background test scope.

Review these smells:

- collecting one cold network Flow multiple times without intending repeated
  upstream work;
- hiding expensive work in an innocent-looking stream;
- swallowing failure or `CancellationException`;
- using SharedFlow as a global event bus;
- using StateFlow for transient events without a delivery policy;
- applying `flowOn`, sharing, or buffers blindly;
- combining unrelated state;
- unbounded replay or retry;
- leaving a hot producer unobserved and ownerless;
- exposing `MutableStateFlow` or `MutableSharedFlow`;
- collecting outside UI lifecycle ownership;
- using `collectLatest` when every item must finish.

Start with semantics: one value or stream, cold or hot, every value or latest,
broadcast or competing receivers, and who owns the lifetime. Then choose the
operator or primitive that states that contract directly.
