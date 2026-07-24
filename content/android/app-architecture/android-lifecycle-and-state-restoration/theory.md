# Android Lifecycle and State Restoration

This topic assumes that you already understand UI state, StateFlow,
ViewModel scope, repositories, and basic lifecycle-aware collection. It focuses
on what Android creates, destroys, retains, saves, and reconstructs.

## Learning outcomes

You will learn to distinguish component lifetimes from restoration, bind work
to the correct owner, save only a small reconstruction recipe, reload
authoritative data, respect Bundle transport limits, and test observable
restoration without overstating what a recreation test proves.

## 1. Lifecycle and restoration are separate problems

Lifecycle describes when an object exists and when it is active. Restoration
describes which state a later object can reconstruct. Ownership decides which
mechanism should hold that state.

No API solves every lifetime:

```text
Ephemeral rendering state               → View / remember
Small recreatable UI state              → saved state / rememberSaveable
Screen in-memory presentation state     → ViewModel
Small process-recreatable screen input  → SavedStateHandle
Authoritative or durable data           → Repository / persistent storage
```

A ViewModel can outlive one Activity instance without surviving the process.
A Bundle can cross recreation without becoming a database. A repository can
own durable data without owning scroll position. Good restoration composes
these mechanisms instead of asking one of them to hold everything.

## 2. Activity lifecycle is a state machine

The principal callbacks are `onCreate`, `onStart`, `onResume`, `onPause`,
`onStop`, and `onDestroy`. They report transitions: created, visible,
interactive, partially inactive, not visible, and destroyed. An Activity can
move forward and backward as dialogs, multi-window, navigation, and background
changes occur; the callbacks are not a once-through business workflow.

Use lifecycle signals to acquire and release UI-bound resources at matching
states. Do not treat them as proof that a purchase was persisted, a network
write completed, or a final save ran. In particular, the system can terminate
the process without calling `onDestroy`. Durable work and data must have owners
and persistence policies that do not depend on a last callback.

## 3. Fragment lifecycle is not its View lifecycle

A Fragment instance is managed by a `FragmentManager`. It can be attached,
created, started, resumed, stopped, destroyed, and detached. Its maximum state
also depends on its manager, parent, and transaction policy.

The Fragment may remain on a back stack while its View is destroyed. The
Fragment therefore has one `Lifecycle`, while a non-null View returned from
`onCreateView` has another. Code that assumes “Fragment exists, therefore its
View exists” crosses ownership boundaries.

Fragment instance state, arguments, a Fragment-scoped ViewModel, and
View-bound objects can consequently have different lifetimes. Choose the owner
that matches the object being observed or mutated.

## 4. Fragment View lifecycle and `viewLifecycleOwner`

`onCreateView` creates the View, `onViewCreated` is the normal setup point, and
`onDestroyView` ends that View instance's lifetime. A later View can be created
for the same Fragment. Binding, adapters that retain Views, UI observers, and
collectors must not outlive the View.

This anti-pattern retains a destroyed binding and observes with the longer
Fragment lifecycle:

```kotlin
class BrokenDetailsFragment : Fragment(R.layout.details) {
    private lateinit var binding: DetailsBinding

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding = DetailsBinding.bind(view)
        viewModel.title.observe(this) { title ->
            binding.title.text = title
        }
    }
}
```

A nullable binding cleared at `onDestroyView` and a View lifecycle owner align
both references and delivery with the current View:

```kotlin
class DetailsFragment : Fragment(R.layout.details) {
    private var _binding: DetailsBinding? = null
    private val binding get() = requireNotNull(_binding)

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        _binding = DetailsBinding.bind(view)
        viewModel.title.observe(viewLifecycleOwner) { title ->
            binding.title.text = title
        }
    }

    override fun onDestroyView() {
        _binding = null
        super.onDestroyView()
    }
}
```

`viewLifecycleOwner` exists only for a created Fragment View. Use it from
View-lifecycle callbacks, not before a View exists.

## 5. Collect Flow for the current Fragment View

Collection that renders a Fragment View belongs to the View lifecycle. A
lifecycle-aware block starts collection while the View is active and cancels
it when the View falls below the selected state:

```kotlin
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    _binding = DetailsBinding.bind(view)

    viewLifecycleOwner.lifecycleScope.launch {
        viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.uiState.collect { state ->
                binding.render(state)
            }
        }
    }
}
```

Launching a new collector from every `onStart`, or using the Fragment's
`lifecycleScope` for View updates, can duplicate work or deliver into a
destroyed View. `repeatOnLifecycle` handles repeated start/stop transitions,
but it does not change repository or ViewModel ownership.

## 6. Lifecycle scenarios are not interchangeable

| Scenario | UI instances | Scoped ViewModel | In-memory state | Saved state | Durable data |
|---|---|---|---|---|---|
| Configuration change | old instances destroyed; new ones created | normally retained for the same logical owner | ViewModel memory retained; View memory lost | eligible UI state restored | unchanged in Repository/storage |
| Destination kept on back stack | View may be destroyed; entry remains | retained with its owner | retained while process lives | entry may retain saved state | unchanged |
| Destination removed / popped | destination owner is destroyed | cleared | owner memory lost | no longer retained for that removed entry | unchanged |
| Explicit Activity `finish()` | Activity is permanently destroyed | cleared with owner | lost | restoration of that finished instance is not expected | unchanged |
| Background process termination | every process object disappears | disappears without surviving | lost | previously captured eligible state may remain with task | persistent data remains |
| Later process recreation | new process and UI objects | new instance | rebuilt | small saved values supplied when available | reloaded from current source of truth |

This is a responsibility matrix, not a promise that every app/task action
preserves saved state. Force stop, task removal, user dismissal, and device or
OEM behavior can remove the restoration opportunity.

## 7. Configuration change recreates UI with a new configuration

For a default configuration change, Android destroys the old UI instance and
creates a new one with updated resources and configuration. A ViewModel
obtained from the same retained store can remain, but old Views, binding,
Activity references, and configuration-dependent values cannot.

The new UI reattaches observers and renders current presentation state. View
hierarchy or Compose saveable state may restore UI details. Code must not fight
recreation merely to preserve data; data and state owners should make
recreation routine.

## 8. Navigation removal and explicit finish destroy an owner

A navigation destination has a back-stack entry that can own a lifecycle,
saved-state registry, and ViewModel store. While that entry remains, its state
holder can remain even if its visible View does not. When the entry is popped,
its lifecycle is destroyed and its ViewModels are cleared.

Graph-scoped ViewModels live while their graph entry remains. Activity-scoped
ViewModels live longer and should not be selected merely to prevent clearing.
Explicit `finish()` similarly states that the Activity instance is done; it is
not a configuration-change retention case.

Whether “navigate away” destroys an owner therefore depends on the operation:
covering or stacking a destination differs from popping it.

## 9. Process termination and process recreation

When the system terminates a background process, its Activities, Fragments,
Views, ViewModels, coroutines, singletons, and caches all disappear. No
`onDestroy` guarantee makes those objects persistent.

If the task is later restored, Android starts a new process and reconstructs
eligible navigation and UI state. A new ViewModel receives small restored
inputs; repositories reload authoritative data; the ViewModel produces new
presentation state; the UI renders it.

```text
restored route ID and filter
        ↓
new ViewModel
        ↓
Repository observes current entity
        ↓
new presentation UiState
        ↓
new UI instance renders
```

“Process death” is the loss event. “Process recreation” is a possible later
recovery event. The latter is not guaranteed after finish, force stop, task
removal, or every user-initiated dismissal.

## 10. `onSaveInstanceState` is a snapshot hook, not durable persistence

The saved instance state mechanism records small transient UI information that
helps reconstruct a system-destroyed instance. Framework Views contribute
hierarchy state, and an Activity or Fragment can add suitable values to a
`Bundle`.

Do not use `onSaveInstanceState` as a guaranteed final callback. It is not
called in every destruction scenario, and writes made after the relevant state
has already been saved may not enter the captured snapshot. Do not perform
slow database or network persistence there.

Save identifiers, small selections, scroll coordinates, or user input when
restoring them is useful. Do not save bitmaps, repositories, services, whole
response graphs, or duplicate database contents.

## 11. Saved State Registry composes providers

`SavedStateRegistryOwner` exposes a registry where a component can register a
provider under a key and later consume the restored `Bundle` for that key. The
registry asks providers for state during the host's saving phase. Activity,
Fragment, Navigation, and ViewModel saved-state integrations build on this
public infrastructure.

Providers still share saved-instance-state constraints. Registration does not
turn the state into durable storage, guarantee a future recreation, or remove
Bundle size limits. Prefer a higher-level integration such as
`SavedStateHandle` or `rememberSaveable` when it directly matches the owner;
use registry APIs for lifecycle-aware components that genuinely contribute
their own small state.

## 12. `SavedStateHandle` stores a reconstruction recipe

A ViewModel can use `SavedStateHandle` for a route ID, filter, small selection,
or unfinished input needed by presentation logic:

```kotlin
class ProductViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val repository: ProductRepository,
) : ViewModel() {
    private val productId: String = checkNotNull(savedStateHandle["productId"])
    private val filter = savedStateHandle.getStateFlow("filter", "all")

    val uiState: StateFlow<ProductUiState> =
        filter.flatMapLatest { selected ->
            repository.observeProduct(productId, selected)
        }.map(ProductUiState::Content)
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = ProductUiState.Loading,
            )

    fun setFilter(value: String) {
        savedStateHandle["filter"] = value
    }
}
```

The handle owns neither `ProductRepository` nor loaded products. The
repository remains the data owner. `Loading` is truthful while a newly created
ViewModel reloads current data from the restored inputs.

Like other saved-state APIs, a correctly owner-bound handle participates in
process recreation. A handle constructed directly in a unit test is only an
in-memory test object unless the test explicitly reconstructs it from captured
values.

## 13. View hierarchy state and custom Views

Views with stable IDs can participate in automatic hierarchy saving. Built-in
widgets commonly restore small UI details such as text or selection. This
works only when the hierarchy and IDs allow Android to match the new View with
saved state.

A custom View that owns a small UI property can extend `BaseSavedState`:

```kotlin
class ExpandableCard @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
) : View(context, attrs) {
    var expanded: Boolean = false

    override fun onSaveInstanceState(): Parcelable =
        SavedState(super.onSaveInstanceState(), expanded)

    override fun onRestoreInstanceState(state: Parcelable?) {
        if (state !is SavedState) {
            super.onRestoreInstanceState(state)
            return
        }
        super.onRestoreInstanceState(state.superState)
        expanded = state.expanded
    }

    private class SavedState : BaseSavedState {
        val expanded: Boolean

        constructor(superState: Parcelable?, expanded: Boolean) : super(superState) {
            this.expanded = expanded
        }

        private constructor(source: Parcel) : super(source) {
            expanded = source.readInt() != 0
        }

        override fun writeToParcel(out: Parcel, flags: Int) {
            super.writeToParcel(out, flags)
            out.writeInt(if (expanded) 1 else 0)
        }

        companion object CREATOR : Parcelable.Creator<SavedState> {
            override fun createFromParcel(source: Parcel) = SavedState(source)
            override fun newArray(size: Int) = arrayOfNulls<SavedState>(size)
        }
    }
}
```

The View owns `expanded`; it does not save a product, bitmap, repository cache,
or auth token. If another owner needs the property, hoist it instead of
creating competing writable copies.

## 14. Compose `remember`, `rememberSaveable`, and `Saver`

`remember` retains a value across recompositions while that remembered slot
remains in the Composition. It does not by itself survive Activity recreation.
`rememberSaveable` uses saveable-state infrastructure to restore supported
small UI values across eligible Activity or process recreation:

```kotlin
@Composable
fun Filters() {
    var animationTick by remember { mutableIntStateOf(0) }
    var query by rememberSaveable { mutableStateOf("") }

    FilterPanel(
        query = query,
        onQueryChange = { query = it },
        animationTick = animationTick,
        onAnimationTick = { animationTick++ },
    )
}
```

Here query input is useful after recreation; an animation tick is ephemeral.
Neither value is authoritative application data.

For a small custom type, save only the minimal supported representation:

```kotlin
data class FilterDraft(val categoryId: String, val showArchived: Boolean)

val FilterDraftSaver = listSaver<FilterDraft, Any>(
    save = { listOf(it.categoryId, it.showArchived) },
    restore = {
        FilterDraft(
            categoryId = it[0] as String,
            showArchived = it[1] as Boolean,
        )
    },
)

@Composable
fun rememberFilterDraft(): MutableState<FilterDraft> =
    rememberSaveable(stateSaver = FilterDraftSaver) {
        mutableStateOf(FilterDraft(categoryId = "all", showArchived = false))
    }
```

A `Saver` is a conversion contract, not permission to serialize a large graph.
Compose saveable state shares Bundle constraints and is not durable storage.

## 15. ViewModel restoration rebuilds presentation state

After configuration change, a retained ViewModel can continue exposing its
current in-memory UiState. After process recreation, Android creates a new
ViewModel. `SavedStateHandle` supplies small inputs when saved state is
available; the data layer supplies current authoritative records.

```kotlin
class EditorViewModel(
    savedStateHandle: SavedStateHandle,
    repository: DocumentRepository,
) : ViewModel() {
    private val documentId: String = checkNotNull(savedStateHandle["documentId"])
    private val draftTitle = savedStateHandle.getStateFlow("draftTitle", "")

    val uiState: StateFlow<EditorUiState> =
        combine(repository.observe(documentId), draftTitle) { document, title ->
            EditorUiState.Ready(document = document, draftTitle = title)
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = EditorUiState.Restoring,
        )

    fun changeTitle(value: String) {
        savedStateHandle["draftTitle"] = value
    }
}
```

`Restoring` truthfully represents the interval before authoritative data
arrives. The ViewModel produces presentation state; it does not claim that the
old instance survived.

## 16. Navigation back-stack entries own state

A `NavBackStackEntry` provides a lifecycle, ViewModel store, and saved-state
registry for a destination. A graph entry can similarly own state shared by a
workflow. While an entry remains on the stack, its destination-scoped state can
remain; popping the entry destroys that ownership boundary and clears its
ViewModels.

Choose destination scope for destination-local state and graph scope for a
coherent multi-destination workflow. Avoid an Activity-wide shared ViewModel
for unrelated destination concerns. Navigation restoration can reconstruct
eligible entries and small state, but repositories must still reload durable
data.

## 17. Fragment Result API and alternatives

The Fragment Result API fits a one-time Bundle-compatible result. The listener
is lifecycle-aware and receives the pending result when its owner is at least
`STARTED`:

```kotlin
class ListFragment : Fragment(R.layout.list) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setFragmentResultListener("filter-request") { _, result ->
            viewModel.setFilter(result.getString("filter").orEmpty())
        }
    }
}

class FilterFragment : Fragment(R.layout.filter) {
    fun submit(filter: String) {
        setFragmentResult("filter-request", bundleOf("filter" to filter))
    }
}
```

Use a shared, correctly scoped ViewModel for ongoing shared UI state with a
custom contract. Use a direct callback when parent-child ownership and lifetime
are explicit. No one mechanism is universal: distinguish one-off result
delivery from a shared source of truth.

Navigation can return a small result through the previous back-stack entry:

```kotlin
// Destination B
findNavController().previousBackStackEntry
    ?.savedStateHandle
    ?.set("selectedId", selectedId)

// Destination A
findNavController().currentBackStackEntry
    ?.savedStateHandle
    ?.getLiveData<String>("selectedId")
    ?.observe(viewLifecycleOwner) { selectedId ->
        viewModel.select(selectedId)
        findNavController().currentBackStackEntry
            ?.savedStateHandle
            ?.remove<String>("selectedId")
    }
```

Remove a consumed one-time result; otherwise a later observer can receive the
last value again. More complex dialog/back-stack cases should observe the
specific entry and its lifecycle rather than assume “current” always names the
underlying destination.

## 18. Bundle, Parcel, and Binder have different jobs

`Bundle` is a typed key-value container used by intents, arguments, saved
state, and framework APIs. `Parcel` is Android's compact marshaling format for
ordered values; readers and writers must agree on representation. Binder is
the IPC mechanism that transports transactions, including framework calls
that carry parcels.

These layers are connected but not interchangeable. Putting an object in a
Bundle may cause it to be marshaled into a Parcel and transported in a Binder
transaction. That does not make the Bundle a file format, Parcel durable
storage, or Binder an application-data repository.

## 19. Transaction limits are aggregate constraints

Binder uses a limited transaction buffer shared by transactions in progress
for a process. Official guidance currently describes a 1 MB buffer and
recommends keeping saved state small; practical headroom matters because the
limit is not a safe per-Bundle allowance.

`TransactionTooLargeException` can result from the total transaction: several
extras, Fragment arguments, navigation state, View hierarchy state,
`rememberSaveable` values, and nested Bundles can combine. One obviously large
bitmap is not the only failure mode.

Transport IDs, paths, URIs, or compact reconstruction inputs. Put image bytes,
large lists, cached responses, and documents in repository-managed database,
file, or cache storage, then reload by key.

## 20. Parcelable and Serializable are transport encodings

`Parcelable` is Android-oriented and defines how values are written to and
read from a Parcel; tooling such as `@Parcelize` can generate the ceremony.
Java `Serializable` uses Java object serialization. Their performance,
compatibility, and tooling differ, so select them for an actual boundary and
supported types.

Neither is a persistence strategy. Making a bitmap graph Parcelable does not
make it small, durable, versioned, or appropriate for navigation. Making a
model Serializable does not make saved-state restoration guaranteed. Prefer
small stable primitives and IDs when they are enough to reconstruct.

## 21. Place state by ownership and restoration need

| Example | Primary owner | Restoration note |
|---|---|---|
| press animation | View / `remember` | intentionally ephemeral |
| scroll position | View or Compose saveable state | small UI detail when useful |
| expanded section | View / `rememberSaveable` | save only if experience requires it |
| route ID | navigation arguments / `SavedStateHandle` | small reconstruction key |
| filter input used by screen logic | ViewModel + `SavedStateHandle` | restore input, recompute results |
| unfinished form text | UI saveable state or ViewModel handle | choose by logic owner and size |
| loaded profile | Repository → ViewModel presentation state | reload current authoritative data |
| auth token | secure persistent data owner | never View or Bundle convenience state |
| bitmap | file/cache/Image loader | pass a key or URI, not pixels |
| repository cache | Repository | not duplicated into saved state |
| derived UiState | ViewModel | rebuild from inputs and data |

Ask five questions: Who may write it? How long is it meaningful? How large is
it? Must it survive process loss? Can it be reconstructed cheaply and
correctly? A value can cross mechanisms—for example, ViewModel uses a saved
filter—but it must still have one authoritative owner.

## 22. Test restoration and review anti-patterns

Test each ownership boundary rather than one mythical “lifecycle test.”
`ActivityScenario.recreate()` checks Activity recreation. Fragment tests can
destroy and recreate the View. `StateRestorationTester` checks Compose
saveable-state restoration. ViewModel tests can reconstruct a new handle from
a captured small map and verify that repositories are queried again:

```kotlin
@Test
fun `new ViewModel restores key and reloads authoritative data`() = runTest {
    val repository = FakeProductRepository(productId = "p-42")
    val restored = SavedStateHandle(
        mapOf("productId" to "p-42", "filter" to "available"),
    )

    val recreated = ProductViewModel(restored, repository)
    val job = backgroundScope.launch { recreated.uiState.collect() }
    advanceUntilIdle()

    assertEquals("p-42", repository.lastRequestedId)
    assertTrue(recreated.uiState.value is ProductUiState.Content)
    job.cancel()
}
```

This proves reconstruction behavior, not an actual OS kill. A real
process-death-like test needs a harness or device workflow that terminates the
process without treating a normal recreation callback sequence as equivalent.
Validate observable recovery, including missing or stale data and unavailable
saved state.

Review for these smells:

- expecting ViewModel, singleton, or coroutine work to survive process death;
- using Fragment lifecycle for View-bound observers;
- retaining binding after `onDestroyView`;
- relying on `onDestroy` for durable writes;
- launching duplicate collectors on every restart;
- storing repositories, Context, View, NavController, or services in saved state;
- copying authoritative data into ViewModel, Bundle, and Repository;
- passing full objects or image bytes instead of IDs;
- using `remember` when recreation restoration is required;
- using `rememberSaveable` or `SavedStateHandle` for large data;
- assuming Parcelable or Serializable removes Binder limits;
- calling a recreation test complete process-death coverage.

End with the decision sequence: identify the owner, choose the narrowest scope,
decide whether loss is acceptable, save only a small reconstruction recipe,
reload durable data from its source of truth, and test the exact destruction
and restoration boundary you claim to support.
