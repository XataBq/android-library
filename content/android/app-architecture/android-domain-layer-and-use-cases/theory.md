# Android Domain Layer and Use Cases

This topic assumes the responsibility, UI-state, repository, SSOT, and
synchronization foundations from its three prerequisite topics. It does not
repeat those models. It asks a narrower question: when does an application
operation deserve a boundary between UI state holders and the Data layer?

## Learning outcomes

After this topic, you should be able to decide whether a Domain layer earns its
cost, place logic by responsibility, design focused use cases, coordinate
repositories, select suspend or Flow contracts, preserve framework
independence, and test application rules with fakes.

## 1. The Domain layer is optional

The UI and Data layers form the baseline Android architecture. A Domain layer
sits between them only when it owns meaningful application logic. Its purpose
is not to make a diagram symmetrical; it is to give complex or reused
operations a stable home.

Android guidance identifies two strong signals: logic is complex enough to
obscure a state holder, or the same logic is reused by several state holders.
Coordination across repositories can be another practical signal because the
operation is broader than ownership of one data type. None of these signals
means every application needs a Domain layer.

A small screen that calls one clear repository operation and maps the response
to UI state may be easier to understand without another class. Adding a layer
has costs: more names, dependencies, navigation, tests, and review surface.
Add it when the new responsibility boundary pays those costs.

## 2. Classify logic by responsibility

Class names do not decide ownership. Ask what decision the logic makes.

| Logic category | Typical responsibility | Examples |
|---|---|---|
| UI | Present and interact with one UI | visibility, display formatting, transient selection, screen state |
| Domain/application | Perform a coherent application operation | eligibility, validation policy, multi-repository workflow, reused calculation |
| Data | Own and provide application data | source selection, persistence, synchronization, caching, conflict policy |

Some decisions are contextual. Sorting may be presentation logic when one
screen offers a temporary sort choice, application logic when every consumer
must use a regulated priority, or Data logic when the repository guarantees a
stable query order. State the governing responsibility before choosing a
layer.

## 3. A decision framework

Before adding a Domain boundary, ask:

1. Is the logic complex enough to hide the state holder's UI responsibility?
2. Is the operation reused by multiple ViewModels or other state holders?
3. Does one application operation coordinate multiple repositories?
4. Is it a stable application capability rather than a screen-specific detail?
5. Would independent tests make the rule safer and ownership clearer?
6. Does extraction reduce duplication or coupling rather than merely move code?

Several “yes” answers strengthen the case. A single “yes” may be sufficient
when the rule is important or failure-prone. If the class would only forward
the same parameters and return value to one repository, keep the simpler
boundary until a real responsibility emerges.

## 4. A use case represents one coherent operation

A use case, sometimes called an interactor, exposes an operation meaningful to
the application. “Submit an eligible order,” “observe a dashboard,” or
“change a profile under account rules” describes intent. “Call repository
method” describes plumbing.

Focus does not require one class for every method. One use case may perform
several steps that belong to the same operation: load required data, evaluate a
rule, request changes, and return an application-level outcome. It should not
become an `AppUseCases` container with unrelated profile, checkout, search, and
notification methods.

Names should express the operation. Kotlin's `operator fun invoke` can make a
single-operation object concise, but it does not make a forwarding wrapper
valuable by itself.

## 5. Inputs, outputs, and failures

Constructor parameters are long-lived collaborators, usually repository
abstractions. Invocation parameters are values specific to one operation.
This separation makes dependencies visible and calls easy to reason about.

Return a type that matches the contract:

- a plain value when the operation produces one value and failure is
  exceptional or already represented by the called API;
- a domain-specific outcome when callers must distinguish expected results;
- a suspending function for a one-shot action;
- a `Flow` when callers observe values that can change over time.

Do not force every operation into one universal `Result` wrapper. A profile
update might need `Updated`, `NameRejected`, and `SessionExpired`; a pure price
calculation may simply return `Money`; an observed dashboard may emit a model
through `Flow`. Model the decisions callers genuinely need.

```kotlin
sealed interface SubmitOrderOutcome {
    data class Submitted(val orderId: String) : SubmitOrderOutcome
    data class Rejected(val reasons: List<String>) : SubmitOrderOutcome
}

class SubmitOrder(
    private val cartRepository: CartRepository,
    private val orderRepository: OrderRepository,
    private val eligibilityPolicy: OrderEligibilityPolicy,
) {
    suspend operator fun invoke(customerId: String): SubmitOrderOutcome {
        val cart = cartRepository.currentCart()
        val reasons = eligibilityPolicy.rejectionReasons(customerId, cart)
        if (reasons.isNotEmpty()) return SubmitOrderOutcome.Rejected(reasons)

        val orderId = orderRepository.submit(cart)
        return SubmitOrderOutcome.Submitted(orderId)
    }
}
```

The outcome represents expected application decisions. Transport errors remain
owned and translated according to the repository contracts rather than being
hidden by a generic wrapper.

## 6. Repository interaction and coordination

A repository owns application data and its source policy. A use case owns an
application operation. The use case calls repository abstractions; it does not
open a DAO, construct a Retrofit service, select a cache, or resolve a sync
conflict itself.

Coordinating two repositories can justify extraction when the coordination is a
stable operation:

```kotlin
data class Dashboard(
    val displayName: String,
    val unreadMessages: Int,
)

class ObserveDashboard(
    private val profileRepository: ProfileRepository,
    private val messageRepository: MessageRepository,
) {
    operator fun invoke(userId: String): Flow<Dashboard> =
        combine(
            profileRepository.observeProfile(userId),
            messageRepository.observeUnreadCount(userId),
        ) { profile, unread ->
            Dashboard(profile.displayName, unread)
        }
}
```

Each repository still owns its data. The use case owns the dashboard
composition. It does not become a new source of truth or absorb refresh,
persistence, or retry policy.

## 7. Suspend and Flow boundaries

Use `suspend` for a finite operation such as submitting an order or saving an
approved change. Use `Flow` for observable application data such as a dashboard
whose inputs change.

The caller owns execution lifetime. A ViewModel can invoke a suspending use case
in `viewModelScope` or collect a Flow into UI state. The use case should remain
cooperative with cancellation and should not start `GlobalScope`, retain a
hidden `CoroutineScope`, or silently continue work after its caller is gone.

```kotlin
class DashboardViewModel(
    observeDashboard: ObserveDashboard,
) : ViewModel() {
    val uiState: StateFlow<DashboardUiState> =
        observeDashboard(userId = "current")
            .map(DashboardUiState::Content)
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = DashboardUiState.Loading,
            )
}
```

Lifecycle-aware collection remains a UI responsibility. The Domain operation
provides a stream; it does not own Activity, Fragment, Compose, or lifecycle
state.

## 8. Framework independence

Domain rules should normally be plain Kotlin. Depending on `Activity`,
`Fragment`, `View`, `Context`, `Resources`, or lifecycle objects couples an
application operation to a presentation or platform mechanism.

If a rule needs information supplied by Android, depend on a narrow
application-facing abstraction or pass the already interpreted value. For
example, a use case can depend on `ConnectivityPolicy` if connectivity is truly
part of the operation, while a Data implementation may obtain platform network
signals. Do not pass `Context` merely to reach a system service.

Framework independence makes tests faster, keeps caller ownership explicit,
and allows the same rule to serve multiple UI surfaces.

## 9. Layer-specific models are conditional

A separate Domain model is useful when it protects a stable application
contract from transport, persistence, or presentation changes, or when it
expresses a rule more precisely. It is wasteful when three identical data
classes are copied between layers with no different constraints or consumers.

Ask what each model promises. A network DTO may mirror server fields; a
repository model may represent application data; a Domain outcome may encode
eligibility decisions; a UI model may contain formatted labels. Create a
mapping only when those contracts differ enough to justify it.

## 10. ViewModel versus use case

| ViewModel | Use case |
|---|---|
| owns screen UI state | owns a coherent application operation |
| handles UI actions | applies reusable or complex application rules |
| makes presentation decisions | coordinates repository contracts |
| uses a UI-owned coroutine scope | remains independent of UI lifetime |
| may format or derive screen-specific values | returns application values or outcomes |

A ViewModel may call repositories directly when the interaction is simple and
screen-specific. Extract a use case when the operation gains meaningful policy,
reuse, or coordination. Do not move loading indicators, navigation flags, or
screen text formatting into Domain code.

## 11. Repository versus use case

Repositories are the Data-layer entry points. They expose application data,
centralize changes, hide sources, and own applicable source and consistency
policy. A use case combines repository capabilities into an application
operation or applies a rule outside one repository's data ownership.

Putting checkout eligibility into `OrderRepository` may be reasonable if the
rule is inseparable from order data policy. It may belong in `SubmitOrder` when
it combines account, cart, inventory, and order contracts. The right boundary
follows responsibility, not a rule that “business logic always belongs in
Domain.”

## 12. Dependency direction without ceremony

The conceptual direction is:

```text
UI → Domain → Data contracts / repositories
```

UI may skip the optional Domain layer and call repositories directly.
Implementation packages or Gradle modules may arrange interfaces differently,
but dependencies must still avoid cycles and preserve ownership. A dedicated
Domain Gradle module is not required. Clean Architecture terminology is not
evidence that the responsibilities are correct.

Dependency injection can supply use cases and repositories, but the use case
does not need Hilt annotations or a particular container. Constructor
dependencies are sufficient to express the boundary.

## 13. Testing with fakes

Domain tests should exercise decisions, coordination, success, failure, and
cancellation without Android framework setup. Fakes make collaborator state
and behavior explicit.

```kotlin
class FakeCartRepository(
    var cart: Cart = Cart(emptyList()),
) : CartRepository {
    override suspend fun currentCart(): Cart = cart
}

class FakeOrderRepository : OrderRepository {
    val submitted = mutableListOf<Cart>()

    override suspend fun submit(cart: Cart): String {
        submitted += cart
        return "order-1"
    }
}

@Test
fun `eligible cart is submitted once`() = runTest {
    val carts = FakeCartRepository(cart = eligibleCart)
    val orders = FakeOrderRepository()
    val useCase = SubmitOrder(carts, orders, AllowEligibleOrders)

    val outcome = useCase(customerId = "customer-1")

    assertEquals(SubmitOrderOutcome.Submitted("order-1"), outcome)
    assertEquals(listOf(eligibleCart), orders.submitted)
}
```

Also test rejected input without submission, repository failures according to
the contract, Flow recombination when either fake emits, and cancellation of
suspending work. Avoid tests that only verify one method forwarded to another.

## 14. Common failure modes

- **Use case for every repository method:** ceremony without a new
  responsibility.
- **Pass-through wrapper:** identical inputs, call, and output add navigation
  cost but no policy.
- **Giant `AppUseCases`:** unrelated operations lose cohesion.
- **Direct DAO or Retrofit access:** the use case takes over Data-layer
  implementation details.
- **Android `Context` in Domain code:** platform mechanics leak into the rule.
- **Hidden background scope:** work escapes caller cancellation and ownership.
- **Duplicated rules:** ViewModels and use cases can disagree.
- **Mechanical Domain models:** mappings exist without different contracts.
- **Swallowed failures:** callers cannot make required state decisions.
- **UI state or navigation in a use case:** presentation ownership moves into
  the wrong layer.

This is usually unnecessary:

```kotlin
class GetUser(private val users: UserRepository) {
    suspend operator fun invoke(id: String): User = users.getUser(id)
}
```

Keep the direct repository call unless the operation later gains reuse,
policy, composition, or a distinct contract.

## 15. Worked example: confirming checkout

Consider a checkout screen. The user taps Confirm.

```text
UI action
    → CheckoutViewModel
    → SubmitOrder
    → CartRepository + AccountRepository + OrderRepository
    → SubmitOrderOutcome
    → updated CheckoutUiState
```

The ViewModel owns `CheckoutUiState`, the click action, loading visibility, and
screen messages. `SubmitOrder` owns the coherent workflow: read the cart and
account, apply eligibility policy, and submit only when valid. Repositories own
cart, account, and order data and translate their data-source behavior.

```kotlin
class SubmitOrder(
    private val carts: CartRepository,
    private val accounts: AccountRepository,
    private val orders: OrderRepository,
) {
    suspend operator fun invoke(customerId: String): SubmitOrderOutcome {
        val cart = carts.currentCart()
        val account = accounts.account(customerId)
        val reasons = validateOrder(cart, account)
        if (reasons.isNotEmpty()) {
            return SubmitOrderOutcome.Rejected(reasons)
        }
        return SubmitOrderOutcome.Submitted(orders.submit(cart))
    }
}

class CheckoutViewModel(
    private val submitOrder: SubmitOrder,
) : ViewModel() {
    fun confirm() {
        viewModelScope.launch {
            updateState { it.copy(submitting = true, message = null) }
            try {
                when (val outcome = submitOrder(customerId)) {
                    is SubmitOrderOutcome.Submitted ->
                        updateState { CheckoutUiState.completed(outcome.orderId) }
                    is SubmitOrderOutcome.Rejected ->
                        updateState { it.copy(submitting = false, reasons = outcome.reasons) }
                }
            } catch (failure: IOException) {
                updateState { it.copy(submitting = false, message = "Try again") }
            }
        }
    }
}
```

Cancellation follows `viewModelScope`; the use case starts no private scope.
The example leaves repository retry and source policy in Data. In production,
failure translation should avoid making UI code depend on transport exceptions;
the exact contract depends on which failures the application must distinguish.

## 16. Decision summary

Start without a Domain layer. Identify the operation and write down its owner.
If logic is complex, reused, multi-repository, or independently valuable to
test, extract one focused use case with explicit inputs, outputs, failures, and
repository dependencies. Keep UI lifetime in the caller and data ownership in
repositories. Avoid platform types and hidden scopes. Add models, modules, and
wrappers only when their distinct contracts earn the added cost.
