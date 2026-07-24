# Android ViewModel and UI State

This topic assumes the existing architecture, UDF, repository, and optional
Domain-layer boundaries. It focuses on the Android-specific state holder that
coordinates one UI scenario: `ViewModel`.

## Learning outcomes

You will learn to choose ViewModel scope, distinguish its lifetime from process
persistence, design coherent state, select Flow contracts, own concurrency,
restore small inputs, keep lifecycle and navigation in UI, and test observable
state transitions.

## 1. ViewModel is a scoped UI state holder

A ViewModel exposes state to a UI and coordinates the UI scenario behind that
state. It receives UI actions, calls repository or use-case contracts, and
turns results into presentation-ready state. Its scope is chosen for a screen,
destination, navigation graph, Activity, or explicitly scoped complex UI.

“Survives rotation” describes one lifetime benefit, not the responsibility.
A class that survives configuration change but owns unrelated features,
navigation controllers, data sources, or global events is still badly scoped.

ViewModel is not a Repository, global singleton, event bus, process-death
database, or owner of Android UI objects.

## 2. ViewModelStoreOwner defines identity and scope

A ViewModel instance belongs to a `ViewModelStoreOwner`. The owner determines
which callers receive the same instance and when that instance is cleared.
Common owners include an Activity, Fragment, navigation destination, navigation
graph, or an explicitly chosen Compose scope.

Choose the narrowest owner that matches the UI scenario:

- destination/screen scope for one screen;
- navigation-graph scope for a workflow deliberately shared by its
  destinations;
- Activity scope only for state genuinely shared across that Activity;
- plain, hoistable state holders for reusable UI components.

Accidentally requesting from a broader owner turns screen state into shared
state. Requesting from different owners creates distinct instances even when
the ViewModel class is the same.

## 3. Configuration change is not destruction of the scenario

During a configuration change, the old Activity or Fragment instance is
destroyed and recreated, but the ViewModelStore is retained and associated with
the new owner instance. The ViewModel keeps its in-memory state and ongoing
`viewModelScope` work.

The UI must still re-collect state and render from the current value. The
ViewModel must not retain the old Activity, Fragment, View, binding, Context, or
Compose node; those objects belong to the destroyed UI instance.

## 4. Permanent owner removal and process death

When an owner is permanently removed—such as a navigation destination popped
from the back stack—its ViewModel is cleared and `viewModelScope` is cancelled.
`onCleared()` is a cleanup signal, not a general persistence callback.

System-initiated process death is different. The process, ViewModel, in-memory
state, and coroutine work disappear. A later recreation constructs a new
ViewModel. Authoritative application data must be reloaded from repositories or
persistent storage. Small recovery inputs may come from saved state.

Force stop, removal from recents, or other task-stack removal can also remove
saved state. Design restoration as recovery, not immortality.

## 5. Design UI state as a contract

UI state answers what the UI can render now. It should expose immutable values
and represent combinations the screen actually supports.

```kotlin
data class ProfileUiState(
    val loading: Boolean = true,
    val refreshing: Boolean = false,
    val profile: ProfileUi? = null,
    val message: String? = null,
)

class ProfileViewModel(
    private val observeProfile: ObserveProfile,
    private val refreshProfile: RefreshProfile,
) : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()
}
```

Private mutability gives the ViewModel one write boundary. Public immutable
state lets the UI observe without bypassing action and transition rules.

## 6. One state object or multiple flows

Use one state object when values form one coherent screen snapshot or must
change atomically. It prevents the UI from observing combinations that never
represented a real transition.

Multiple flows can be appropriate for genuinely independent data with
different lifetimes or consumers. The official guidance permits separate
properties for unrelated data. Avoid splitting one invariant merely to reduce
the size of a data class.

Ask whether values must be read together. `items`, `query`, and
`selectedFilter` may need one coherent model; an independent snackbar effect
does not become state merely to fit that object.

## 7. StateFlow, SharedFlow, Channel, and cold Flow

These types communicate different contracts:

- `StateFlow` is hot state with a current value; a new collector immediately
  receives the latest value.
- `SharedFlow` is a configurable hot broadcast. Replay and buffering determine
  what late or slow collectors observe.
- `Channel` transfers elements to receivers; with multiple receivers, an
  element is normally consumed by one receiver rather than broadcast as state.
- a cold `Flow` starts its upstream work independently for each collector
  unless it is shared.

No type is the universal “event solution.” First decide whether the information
is durable state, a broadcast effect, a queue-like handoff, or a repeatable
query. Then define behavior for no collector, recreation, multiple collectors,
buffering, and failure.

## 8. State versus transient events

If an outcome must still be visible after recreation, represent it as state.
For example, “order submitted with ID 42” can become `Completed(orderId)`, and
the UI can navigate or render based on that state with an explicit
acknowledgement policy.

```kotlin
sealed interface CheckoutStatus {
    data object Editing : CheckoutStatus
    data object Submitting : CheckoutStatus
    data class Completed(val orderId: String) : CheckoutStatus
    data class Rejected(val reasons: List<String>) : CheckoutStatus
}
```

A transient effect may be appropriate when replay would be incorrect, such as
requesting focus or showing a short-lived animation. An event mechanism then
needs an explicit loss, replay, and multi-collector contract:

```kotlin
private val _effects = MutableSharedFlow<CheckoutEffect>(
    extraBufferCapacity = 1,
)
val effects: SharedFlow<CheckoutEffect> = _effects.asSharedFlow()
```

Do not use an event stream to hide durable state transitions. Do not assume an
emission is delivered when no collector exists.

## 9. Actions define the write API

Expose intent-oriented actions rather than public mutable flows:

```kotlin
sealed interface SearchAction {
    data class QueryChanged(val value: String) : SearchAction
    data object Retry : SearchAction
    data object Refresh : SearchAction
}

fun onAction(action: SearchAction) {
    when (action) {
        is SearchAction.QueryChanged -> updateQuery(action.value)
        SearchAction.Retry -> load()
        SearchAction.Refresh -> refresh()
    }
}
```

One dispatcher is optional; named methods are also valid. The important point
is that callers request transitions and the ViewModel preserves invariants.
Navigation execution remains in UI, even if state indicates that navigation is
now appropriate.

## 10. Atomic state updates

Read-then-assign can lose concurrent changes:

```kotlin
// Risky when another coroutine can update uiState between read and write.
_uiState.value = _uiState.value.copy(refreshing = true)
```

Use `MutableStateFlow.update` for an atomic transformation:

```kotlin
_uiState.update { current ->
    current.copy(refreshing = true, message = null)
}
```

Atomic update protects the read-modify-write operation. It does not by itself
decide which concurrent request wins. Request identity, cancellation, or
serialization must define that policy.

## 11. Loading, refresh, retry, and partial failure

One Boolean rarely describes every operation. Initial loading may have no
content; refresh may preserve content; a form submission may run independently.
Represent states the UI can act on.

An initial failure can replace the whole screen. A refresh failure may keep
usable content and expose a retryable message. A field error may coexist with
other valid fields. The ViewModel maps repository or use-case outcomes into
these UI decisions; it should not duplicate the Data layer's source policy.

Retry is an action with defined scope: retry initial load, refresh, or submit.
“Retry everything” can duplicate work or erase useful state.

## 12. viewModelScope and structured concurrency

`viewModelScope` is cancelled when the ViewModel is cleared. Launch UI-scenario
work there and call suspending repository or use-case contracts. Do not use
`GlobalScope` or create hidden unmanaged scopes.

For latest-wins search, cancel the previous job or use Flow operators whose
semantics express replacement:

```kotlin
private val query = MutableStateFlow("")

val uiState: StateFlow<SearchUiState> =
    query
        .debounce(300)
        .flatMapLatest(searchRepository::search)
        .map(SearchUiState::Content)
        .catch { emit(SearchUiState.Error) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = SearchUiState.Loading,
        )
```

Cancellation is part of the contract. A repository operation that must survive
screen removal needs a different durable owner; keeping the ViewModel alive is
not the solution.

## 13. Duplicate collectors duplicate cold work

Each collection of a cold Flow starts its upstream again:

```kotlin
// Anti-pattern: two collectors may start the same expensive upstream twice.
val items = repository.observeItems()
val count = repository.observeItems().map(List<Item>::size)
```

Share once when both values derive from the same stream:

```kotlin
private val items: StateFlow<List<Item>> =
    repository.observeItems().stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = emptyList(),
    )

val uiState: StateFlow<ItemsUiState> =
    items.map { ItemsUiState(items = it, count = it.size) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = ItemsUiState(),
        )
```

Also inspect repository behavior: some upstreams are already hot or internally
shared. Do not add sharing blindly.

## 14. stateIn and SharingStarted

`stateIn` converts a Flow into a hot `StateFlow` in a supplied scope, stores the
latest value, and shares one upstream instance among collectors. The initial
value must be a truthful renderable state.

For example, profile identity and unread-message count can form one coherent
dashboard snapshot: the screen renders them together and should not maintain
independent copies that can drift. Each repository still owns and updates its
own data. The ViewModel combines their contracts and produces presentation
state:

```kotlin
sealed interface DashboardUiState {
    data object Loading : DashboardUiState
    data class Content(
        val displayName: String,
        val unreadMessages: Int,
    ) : DashboardUiState
}

class DashboardViewModel(
    profileRepository: ProfileRepository,
    messageRepository: MessageRepository,
) : ViewModel() {
    val uiState: StateFlow<DashboardUiState> =
        combine(
            profileRepository.observeProfile(),
            messageRepository.observeUnreadCount(),
        ) { profile, unreadCount ->
            DashboardUiState.Content(
                displayName = profile.displayName,
                unreadMessages = unreadCount,
            )
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = DashboardUiState.Loading,
        )
}
```

`Loading` is truthful until both repositories have supplied values; a fabricated
empty profile or zero count would falsely claim that real data had loaded.
Do not apply `combine` mechanically to unrelated UI concerns. A snackbar effect,
independent editor draft, or navigation request may need a different contract
and lifetime even when it appears on the same screen.

`SharingStarted` controls when upstream collection runs:

- `Eagerly`: start immediately;
- `Lazily`: start with the first subscriber and keep running;
- `WhileSubscribed`: run according to subscriber presence, with configurable
  stop and replay-expiration behavior.

`WhileSubscribed(5_000)` can bridge short collector gaps such as configuration
changes. Five seconds is a policy choice, not a law. Consider upstream cost,
freshness, expected gaps, and whether stopping is safe.

Handle upstream exceptions before `stateIn` when they must become UI state;
otherwise the sharing coroutine's scope handles them and collectors do not
receive a value describing the failure.

## 15. Lifecycle-aware collection belongs to UI

ViewModel exposes state; UI decides when it is active enough to collect.
Compose can use `collectAsStateWithLifecycle`. View-based UIs can collect inside
`repeatOnLifecycle`.

```kotlin
@Composable
fun ProfileRoute(viewModel: ProfileViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ProfileScreen(state = state, onAction = viewModel::onAction)
}
```

The ViewModel must not receive a LifecycleOwner or call Fragment lifecycle
methods. Lifecycle-aware collection may stop a `WhileSubscribed` upstream;
the ViewModel's current state remains available when collection resumes.

## 16. SavedStateHandle restores small recovery inputs

ViewModel memory survives configuration change, not process death.
`SavedStateHandle` participates in saved-state restoration for small,
serializable values needed to reconstruct the screen: route IDs, query text,
filter choices, or an in-progress selection.

```kotlin
class ResultsViewModel(
    savedStateHandle: SavedStateHandle,
    private val search: SearchRepository,
) : ViewModel() {
    private val query = savedStateHandle.getStateFlow("query", "")

    val uiState: StateFlow<ResultsUiState> =
        query
            .flatMapLatest(search::results)
            .map(ResultsUiState::Content)
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = ResultsUiState.Loading,
            )

    fun setQuery(value: String) {
        savedStateHandle["query"] = value
    }
}
```

Do not store bitmaps, large lists, database snapshots, repository caches, or
authoritative application records in saved state. Persist application data in
the Data layer. Restore the small input, then reload the current data.

## 17. Dependencies, navigation, and errors

Inject repositories and focused use cases; do not own Retrofit services, DAOs,
Context, Application, Activity, Fragment, View, NavController, or Compose
runtime state in the ViewModel.

The ViewModel may expose a state or effect that tells UI an outcome occurred.
The UI performs navigation using its current controller and lifecycle. This
keeps destinations and platform objects out of the state holder.

Repositories and use cases expose application-level contracts. The ViewModel
turns expected failures into screen decisions and presentation keys or models.
It should not display transport exception messages directly or swallow errors
that the UI must represent.

## 18. Shared ViewModels are scoped collaboration, not an event bus

A graph- or Activity-scoped ViewModel can coordinate state intentionally shared
by several destinations. The shared owner must match the workflow lifetime,
and the state must have one coherent responsibility.

Do not use an Activity-scoped ViewModel as a global bucket for unrelated
screens or as an application event bus. Broad scope increases retention,
coupling, accidental observers, and unclear reset behavior. For reusable UI,
prefer state hoisting and a plain state holder.

## 19. Test observable behavior with coroutine control

Test initial state, successful transitions, failure, retry, cancellation,
latest-wins behavior, sharing, and restored inputs. Use fake repositories or
use cases and coroutine test control.

```kotlin
@Test
fun `new query cancels previous search and publishes latest result`() = runTest {
    val repository = FakeSearchRepository()
    val savedState = SavedStateHandle(mapOf("query" to "old"))
    val viewModel = ResultsViewModel(savedState, repository)
    val collected = mutableListOf<ResultsUiState>()
    val job = backgroundScope.launch {
        viewModel.uiState.toList(collected)
    }

    viewModel.setQuery("new")
    repository.emit("new", listOf(Result("latest")))
    advanceUntilIdle()

    assertEquals("new", savedState["query"])
    assertTrue(collected.last().shows("latest"))
    assertTrue(repository.wasCancelled("old"))
    job.cancel()
}
```

Keep a collector active when testing `WhileSubscribed`; otherwise the upstream
may correctly remain stopped. Test state values and outcomes, not private
implementation calls.

## 20. Anti-pattern review and decision summary

Watch for:

- ViewModel justified only as a “rotation survivor”;
- Activity-scoped global state for unrelated features;
- Activity, Fragment, View, Context, NavController, or Compose objects retained;
- public `MutableStateFlow`;
- Repository, DAO, or Retrofit responsibilities inside ViewModel;
- unrelated feature logic in one class;
- one loading flag for concurrent operations;
- read-then-assign lost updates;
- duplicate cold collectors;
- events used for durable outcomes;
- SharedFlow or Channel chosen without loss/replay semantics;
- large authoritative data in `SavedStateHandle`;
- hidden scopes or work expected to survive owner removal.

Choose the owner first. Define coherent immutable state, explicit actions, and
atomic transitions. Share upstream work deliberately. Let UI own lifecycle and
navigation, Data own authoritative records, and optional Domain own reusable
application operations. Treat saved state as a small recovery recipe, then
rebuild the screen from current data.
