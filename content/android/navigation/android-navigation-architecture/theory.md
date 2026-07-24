# Android Navigation Architecture

Android navigation is easiest to reason about when treated as owned state, not
as scattered calls that happen to replace pixels. This topic uses AndroidX
Navigation 2 terminology and examples while keeping the architectural model
portable across Compose, Fragments, XML graphs, Kotlin DSL graphs, and newer
navigation libraries.

## 1. Navigation is back-stack state

A navigation host maintains an ordered stack of entries. The top entry is the
current place rendered by that host; earlier entries record where Back can
return. A navigation operation changes that state by adding, removing, or
restoring entries.

```kotlin
data class StackModel(
    val entries: List<String>,
) {
    val current: String? get() = entries.lastOrNull()

    fun push(route: String) = copy(entries = entries + route)
    fun pop() = copy(entries = entries.dropLast(1))
}
```

This model is illustrative, not a replacement for `NavController`. Its purpose
is to make the invariant visible: a route string by itself is not the complete
navigation state, because history and each entry's ownership also matter.

## 2. Destination, route, graph, and entry

- A **destination** declares a place the host can show.
- A **route** identifies a destination plus the small inputs needed to reach
  one instance of it.
- A **navigation graph** declares destinations, nested graphs, and their
  relationships for one host.
- A **back-stack entry** is one runtime instance of a destination or graph. It
  owns a lifecycle, saved state, and a ViewModel store.
- The **current destination** is associated with the top active entry; it is
  not necessarily the only retained destination.

Two entries can target the same destination with different inputs. Conversely,
two route encodings can be a migration detail for one conceptual destination.
Architecture should depend on the meaning of the destination, not on string
concatenation tricks.

## 3. The UI host owns navigation

The `NavController` belongs beside the `NavHost`, `Fragment`, `Activity`, or
other UI coordinator whose lifecycle and graph it controls. A ViewModel may
decide that presentation has reached “checkout may open” and expose an intent
or effect. It does not retain or invoke a `NavController`. Repositories and use
cases own data and business decisions; they never navigate.

The simplest reliable boundary is a UI callback:

```kotlin
@Composable
fun ProductScreen(
    state: ProductUiState,
    onProductSelected: (String) -> Unit,
) {
    ProductList(
        products = state.products,
        onClick = { product -> onProductSelected(product.id) },
    )
}

composable<HomeRoute> {
    ProductScreen(
        state = homeState,
        onProductSelected = { id ->
            navController.navigate(ProductRoute(id))
        },
    )
}
```

Business logic may reject an action before the callback is invoked. The UI
still performs the framework transition with the controller it currently
owns.

## 4. Back-stack operations and owner lifetime

`navigate` usually pushes an entry. Back normally pops the top entry. A
replace-like flow is expressed as a push plus removal policy, such as
`popUpTo`, rather than assuming every screen replaces the previous screen.
Popping permanently removes the entry and clears its destination-scoped
ViewModels. Merely covering or stopping it does not.

```kotlin
fun NavController.openReceipt(orderId: String) {
    navigate(ReceiptRoute(orderId))
}

fun NavController.closeReceipt(): Boolean = popBackStack()
```

Configuration change can recreate UI objects while the controller restores
the stack. Process recreation may reconstruct eligible stack and saved state
from a system-saved snapshot. Neither case makes repositories or in-flight
work part of the stack.

## 5. System Back and hierarchical Up

Back is chronological: it reverses the user's navigation history and may leave
the app when no in-app entry remains. Up is hierarchical: it moves toward the
logical parent represented by the app's information structure. Inside a
well-formed in-app stack they often produce the same result, but a destination
entered through a deep link can make the distinction visible.

```kotlin
fun AppCompatActivity.configureUp(navController: NavController) {
    onBackPressedDispatcher.addCallback(this) {
        if (!navController.popBackStack()) finish()
    }

    // The toolbar's Up affordance should call navigateUp(), not synthesize Back.
    binding.toolbar.setNavigationOnClickListener {
        navController.navigateUp()
    }
}
```

Do not invent a parent by navigating to a fresh copy on every Up press. Let the
graph and deep-link task construction define the hierarchy.

## 6. Arguments are reconstruction inputs

Pass small, stable, serializable values such as an ID, filter, or enum. The
destination asks a repository for authoritative data. Passing a mutable domain
object creates stale copies, expands saved-state and Binder payloads, and
confuses ownership.

```kotlin
class ProductViewModel(
    savedStateHandle: SavedStateHandle,
    private val products: ProductRepository,
) : ViewModel() {
    private val productId: String = checkNotNull(savedStateHandle["productId"])

    val state: StateFlow<ProductUiState> =
        products.observeProduct(productId)
            .map(ProductUiState::Content)
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = ProductUiState.Loading,
            )
}
```

An ID is not authorization. The repository or use case must still enforce
access rules when loading the record.

## 7. Type-safe routes are version-sensitive

AndroidX Navigation 2.8.0 introduced official type-safe destinations for
Navigation Compose and Kotlin DSL graphs. The route type is serialized, the
graph registers that type, and the destination reads it with `toRoute`.
Verify the exact API and required serialization plugin against the AndroidX
Navigation version installed in the project. Navigation 3, XML resources with
Safe Args, older string routes, and custom coordinators use different APIs;
there is no universal route syntax.

```kotlin
@Serializable
data object HomeRoute

@Serializable
data class ProductRoute(val productId: String)

@Composable
fun AppNavHost(navController: NavHostController) {
    NavHost(navController = navController, startDestination = HomeRoute) {
        composable<HomeRoute> {
            HomeScreen(
                onOpenProduct = { id ->
                    navController.navigate(ProductRoute(id))
                },
            )
        }
        composable<ProductRoute> { entry ->
            val route = entry.toRoute<ProductRoute>()
            ProductScreen(productId = route.productId)
        }
    }
}
```

Typed routes prevent many encoding and key mismatches. They do not validate
business access, prove that referenced data still exists, or make large
objects suitable as arguments.

## 8. Navigation state and screen state have different owners

Use the narrowest owner that matches the fact:

| Fact | Responsible owner |
| --- | --- |
| destination order and current entry | navigation back stack |
| small route input needed after recreation | arguments / entry `SavedStateHandle` |
| derived loading, content, error, selection | destination or graph ViewModel |
| authoritative product, account, order | Repository |
| transient focus, animation, open menu | local UI state |

```kotlin
data class EditorUiState(
    val title: String,
    val canSave: Boolean,
    val validationMessage: String?,
)

sealed interface EditorAction {
    data class TitleChanged(val value: String) : EditorAction
    data object SaveClicked : EditorAction
}
```

Do not mirror the whole back stack as a Boolean such as `shouldShowEditor` in
screen state. Two competing navigation truths cause loops and duplicate
destinations.

## 9. Direct callbacks, intents, effects, and state

A direct UI callback is best when the event originates in active UI and needs
no asynchronous decision. A ViewModel intent is an input such as
`CheckoutClicked`; it is not a navigation command. A ViewModel effect can
represent a presentation decision completed asynchronously, but requires a
delivery contract. Durable facts belong in state, not an event stream.

```kotlin
sealed interface CheckoutEffect {
    data class OpenReceipt(
        val effectId: Long,
        val orderId: String,
    ) : CheckoutEffect
}

class CheckoutViewModel(
    private val placeOrder: PlaceOrder,
) : ViewModel() {
    private val _effects = MutableSharedFlow<CheckoutEffect>()
    val effects: SharedFlow<CheckoutEffect> = _effects.asSharedFlow()

    fun submit() {
        viewModelScope.launch {
            val orderId = placeOrder()
            _effects.emit(CheckoutEffect.OpenReceipt(nextEffectId(), orderId))
        }
    }
}
```

The use case returns an outcome; the ViewModel translates it to a presentation
effect; active UI collects and navigates. A `SharedFlow` with no replay may
lose an effect without a subscriber. Replay can repeat it after recreation.
Neither setting is universally correct.

## 10. One-off effects need a delivery policy

Choose based on required guarantees:

- direct callback: active UI handles immediately;
- best-effort stream: occurrence may be lost while UI is absent;
- acknowledged pending effect: state retains an ID until UI confirms handling;
- durable workflow outcome: persist it as application data, then derive the
  next screen from that fact.

```kotlin
data class CheckoutUiState(
    val submitting: Boolean = false,
    val pendingNavigation: PendingNavigation? = null,
)

data class PendingNavigation(
    val id: Long,
    val orderId: String,
)

fun CheckoutViewModel.navigationHandled(id: Long) {
    _state.update { current ->
        if (current.pendingNavigation?.id == id) {
            current.copy(pendingNavigation = null)
        } else {
            current
        }
    }
}
```

UI must acknowledge only after executing the matching effect. The ID prevents
an old acknowledgement from clearing a newer one. Do not apply this pattern
mechanically: it deliberately makes the pending transition durable
presentation state.

## 11. Stack options express product history

`launchSingleTop` avoids adding a duplicate when the target is already on top;
it does not search and deduplicate the whole stack. `popUpTo` removes entries
up to a target. `inclusive = true` removes that target too. `saveState` and
`restoreState` preserve eligible destination state for later restoration.

```kotlin
fun NavController.finishLogin() {
    navigate(HomeRoute) {
        popUpTo<LoginGraph> {
            inclusive = true
        }
        launchSingleTop = true
    }
}

fun NavController.selectTopLevel(route: Any) {
    navigate(route) {
        popUpTo(graph.findStartDestination().id) {
            saveState = true
        }
        launchSingleTop = true
        restoreState = true
    }
}
```

Clearing onboarding after completion prevents Back from returning to it.
Top-level selection preserves history only if that matches the product
contract. Reselect behavior—stay, pop to root, or refresh—must be explicit.
Typed `popUpTo<T>` depends on the installed Navigation API; ID-based overloads
remain valid in other graph styles.

## 12. Nested graphs structure navigation

A nested graph can encapsulate an authentication, onboarding, or checkout
flow. Other destinations navigate to the graph boundary rather than knowing
every internal step. A graph can also provide a shared ViewModel owner for the
flow.

```kotlin
@Serializable
data object AuthGraph

@Serializable
data object SignInRoute

@Serializable
data object VerifyCodeRoute

fun NavGraphBuilder.authGraph(navController: NavController) {
    navigation<AuthGraph>(startDestination = SignInRoute) {
        composable<SignInRoute> {
            SignInScreen(onCodeSent = {
                navController.navigate(VerifyCodeRoute)
            })
        }
        composable<VerifyCodeRoute> {
            VerifyCodeScreen()
        }
    }
}
```

A navigation graph is a UI state structure, not automatically a Gradle module,
domain boundary, or security boundary.

## 13. Destination, graph, and Activity ViewModel scopes

Destination scope lasts while one destination entry remains. Graph scope lasts
while that graph entry remains and can coordinate its child destinations.
Activity scope lasts across every destination hosted by that Activity and is
easy to overuse.

```kotlin
@Composable
fun CheckoutAddressDestination(
    navController: NavController,
) {
    val graphEntry = remember(navController) {
        navController.getBackStackEntry<CheckoutGraph>()
    }
    val checkoutViewModel: CheckoutViewModel = viewModel(graphEntry)

    AddressScreen(
        state = checkoutViewModel.addressState,
        onContinue = { navController.navigate(PaymentRoute) },
    )
}
```

This type-safe entry lookup is version-sensitive; ID or route-string overloads
serve older graph styles. Graph scope is appropriate only for state genuinely
shared by that workflow. Activity-scoped ViewModels increase lifetime,
coupling, retained memory, and accidental communication.

## 14. Multiple back stacks preserve top-level history

Bottom navigation often represents parallel top-level histories: explore
detail, switch to profile, then return to the same explore detail. AndroidX
Navigation supports multiple back stacks from 2.4.0, automatically through
appropriate `NavigationUI` integrations or manually with save/restore options.

```kotlin
fun NavController.openTopLevel(destinationId: Int) {
    navigate(destinationId, null, navOptions {
        launchSingleTop = true
        restoreState = true
        popUpTo(graph.findStartDestination().id) {
            saveState = true
        }
    })
}
```

Repeated selection must not create duplicate stacks. Decide whether reselecting
the active tab preserves detail or pops to its root. Saved histories retain
state and possibly ViewModels, so many deep stacks can cost memory; measure
rather than assuming they are free.

## 15. Navigation results are ownership decisions

A previous-entry `SavedStateHandle` fits a small, Bundle-compatible one-time
navigation result. Remove or otherwise consume it once. It is not a durable
data store.

```kotlin
private const val SELECTED_ADDRESS = "selected_address"

fun NavController.finishAddressPicker(addressId: String) {
    previousBackStackEntry
        ?.savedStateHandle
        ?.set(SELECTED_ADDRESS, addressId)
    popBackStack()
}

fun NavBackStackEntry.consumeSelectedAddress(): String? =
    savedStateHandle.remove<String>(SELECTED_ADDRESS)
```

Use a direct callback inside one active composition when no navigation
boundary must survive. Use a shared graph-scoped ViewModel for ongoing workflow
state. Use a repository when selection changes authoritative application data.
AndroidX Navigation saved-state results are available from Navigation 2.3.0;
confirm exact lifecycle behavior in the installed version.

## 16. Fragment Result API and alternatives

Fragment Result API, available from Fragment 1.3.0, delivers a one-time
Bundle-compatible result to a lifecycle-aware listener. It is useful when
Fragments communicate without making each other direct dependencies.

```kotlin
private const val REQUEST_PICK_COLOR = "pick_color"
private const val RESULT_COLOR_ID = "color_id"

class EditorFragment : Fragment(R.layout.editor_fragment) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        parentFragmentManager.setFragmentResultListener(
            REQUEST_PICK_COLOR,
            this,
        ) { _, bundle ->
            viewModel.colorSelected(bundle.getString(RESULT_COLOR_ID)!!)
        }
    }
}

fun ColorPickerFragment.finish(colorId: String) {
    parentFragmentManager.setFragmentResult(
        REQUEST_PICK_COLOR,
        bundleOf(RESULT_COLOR_ID to colorId),
    )
    findNavController().popBackStack()
}
```

A Fragment Result is not for continuous shared state. A graph-scoped
ViewModel fits a multi-screen draft; a callback fits local UI; a repository
fits a durable saved selection. Choose by owner and lifetime, not convenience.

## 17. Deep links reconstruct routes

An explicit deep link is typically created by the app for a `PendingIntent` or
notification. An implicit deep link matches an external URI, action, or MIME
type declared by a destination or Activity. Either can reconstruct a task and
nested graph start entries before the target.

```kotlin
@Serializable
data class OrderRoute(val orderId: String)

fun parseOrderId(uri: Uri): String? =
    uri.lastPathSegment
        ?.takeIf { it.length in 1..64 }
        ?.takeIf { value -> value.all(Char::isLetterOrDigit) }

fun routeForOrder(uri: Uri): OrderRoute? =
    parseOrderId(uri)?.let(::OrderRoute)
```

Treat every deep-link argument as untrusted. Handle missing records, unsupported
route versions, missing prerequisites, and signed-out users. An auth gate
should preserve only the validated intended destination and resume it after
authentication according to product policy.

## 18. App Links and external entry-point security

Android App Links are verified HTTP(S) links associated with an application
and website. Verification improves routing confidence; it does not make URL
parameters trusted. An Activity with matching intent filters may be externally
reachable depending on manifest configuration. Audit `android:exported`
explicitly.

```kotlin
data class ExternalOrderRequest(val orderId: String)

sealed interface EntryDecision {
    data class Open(val route: OrderRoute) : EntryDecision
    data object RequireSignIn : EntryDecision
    data object Reject : EntryDecision
}

suspend fun authorizeEntry(
    request: ExternalOrderRequest,
    session: SessionRepository,
    orders: OrderRepository,
): EntryDecision {
    if (!session.isSignedIn()) return EntryDecision.RequireSignIn
    if (!orders.canCurrentUserRead(request.orderId)) return EntryDecision.Reject
    return EntryDecision.Open(OrderRoute(request.orderId))
}
```

Validate scheme, host, path, input shape, data existence, and user privileges.
Keep secrets and sensitive personal data out of URLs. Internal-only screens
must not become reachable merely because a route name exists. Navigation is
not authorization, and a `PendingIntent` or verified link does not eliminate
server- or repository-side privilege checks.

## 19. Recreation restores references, not application truth

Navigation can restore eligible entries and small saved values after
configuration or process recreation. A new ViewModel can receive route
arguments through `SavedStateHandle` and reload current data. In-memory
objects, jobs, open resources, and uncommitted repository transactions are not
restored automatically.

```kotlin
@Serializable
data class ConversationRoute(val conversationId: String)

class ConversationViewModel(
    savedStateHandle: SavedStateHandle,
    conversations: ConversationRepository,
) : ViewModel() {
    private val route = savedStateHandle.toRoute<ConversationRoute>()

    val state = conversations.observe(route.conversationId)
        .map(ConversationUiState::Ready)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = ConversationUiState.Loading,
        )
}
```

`SavedStateHandle.toRoute` follows the type-safe route APIs introduced in
Navigation 2.8.0. For other styles, read explicitly keyed arguments. Restoration
is best effort and size-limited; repositories remain the source of truth.

## 20. Compose and Fragment boundaries

Compose commonly declares routes in a `NavHost` and passes navigation lambdas
to screen composables. Fragment navigation commonly keeps calls in a Fragment
or UI coordinator and passes events into its ViewModel. Both obey the same
boundary: screen content does not retain a controller, and data/domain layers
do not depend on navigation types.

```kotlin
@Composable
fun ProfileDestination(
    navController: NavController,
    viewModel: ProfileViewModel = viewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    ProfileScreen(
        state = state,
        onEdit = { navController.navigate(EditProfileRoute) },
    )
}
```

```kotlin
class ProfileFragment : Fragment(R.layout.profile_fragment) {
    private val viewModel: ProfileViewModel by viewModels()

    fun onEditClicked() {
        findNavController().navigate(
            ProfileFragmentDirections.openEditProfile(),
        )
    }
}
```

The second example assumes an XML graph with Safe Args; the first assumes
type-safe Compose routes. Neither API style is universally required.

## 21. Test navigation behavior, not screenshots

Separate screen rendering from route execution so tests can call callbacks
directly. For integration tests, use `TestNavHostController`, install a graph,
perform an action, and assert the current destination or route. Test stack
clearing, Back, deep-link rejection, results, and recreation separately.

```kotlin
@Test
fun selectingProduct_opensTypedProductRoute() {
    val controller = TestNavHostController(context).apply {
        navigatorProvider.addNavigator(ComposeNavigator())
        setGraph(testGraph)
    }

    controller.navigate(ProductRoute("p-42"))

    assertTrue(
        controller.currentBackStackEntry
            ?.destination
            ?.hasRoute<ProductRoute>() == true,
    )
}
```

`hasRoute<T>` and type-safe testing helpers depend on recent Navigation
versions; verify them against the installed artifact. ID assertions remain
appropriate for XML graphs.

A small application-owned navigator interface can isolate a ViewModel's
presentation decision without importing `NavController`:

```kotlin
interface CheckoutRouter {
    fun openReceipt(orderId: String)
}

class RecordingCheckoutRouter : CheckoutRouter {
    val openedReceipts = mutableListOf<String>()

    override fun openReceipt(orderId: String) {
        openedReceipts += orderId
    }
}
```

Inject such an interface into a UI coordinator, not into repositories. Test
authorization and route parsing as ordinary functions, then keep a smaller set
of graph integration tests.

## 22. Common anti-patterns

- storing `NavController`, `Activity`, `Fragment`, or composable lambdas in a
  ViewModel;
- allowing Repository or use case code to navigate;
- passing database entities, bitmaps, credentials, or mutable objects as
  arguments;
- representing the current destination twice in both back stack and UI state;
- using replay blindly for one-off effects and navigating again after
  recreation;
- using a global event bus for all navigation;
- Activity-scoping every ViewModel;
- creating duplicate top-level stacks on every selection;
- forgetting to consume one-time navigation results;
- trusting a typed route, verified link, or ID as authorization;
- assuming saved state restores repositories, jobs, or large object graphs;
- testing only pixels while stack and deep-link behavior remain unverified.

Each mistake obscures an owner, lifetime, or trust boundary. Fix the boundary
before adding an event wrapper or another graph.

## 23. A navigation design checklist

For each transition, answer:

1. What entry and history should exist afterward?
2. Is this a direct UI action, a presentation decision, or durable business
   data?
3. Which UI owner has the current controller?
4. What is the minimal validated reconstruction input?
5. Which scope owns shared state, and when is it cleared?
6. Can the effect be lost, repeated, or acknowledged?
7. What should Back, Up, reselect, and process recreation do?
8. Is the entry external, and where are authentication and authorization
   enforced?
9. Which pure, ViewModel, graph, and device tests prove the contract?
10. Which API assumptions must be checked against installed AndroidX versions?

The stable architecture is intentionally small: the back stack owns navigation
state, UI owns framework execution, ViewModel owns presentation state,
repositories own application data, and authorization owns access decisions.
