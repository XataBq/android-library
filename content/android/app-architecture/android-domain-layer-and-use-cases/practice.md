# Android Domain Layer and Use Cases — Practice

## Exercise 1 — Responsibility classification

### Goal

Classify logic by the decision it owns rather than by its current class.

### Scenario

Review these behaviors:

1. format a balance using the screen's selected locale;
2. decide whether an account may place an order;
3. choose local or remote data during refresh;
4. combine profile and message data for a dashboard shared by two screens;
5. keep an expanded-card selection until the screen closes;
6. sort alerts by a legally mandated priority;
7. translate a network response into the application's stored model;
8. choose whether an expired session should block a user-requested operation.

Classify each as UI, Domain/application, Data, or ambiguous and requiring more
context.

### Constraints

- Justify every classification with the responsibility being protected.
- For ambiguous cases, name the missing fact that would decide ownership.
- Do not use class names or a preferred architecture diagram as evidence.

### Expected deliverable

A table with behavior, classification, owner, justification, and any boundary
contract required.

### Evaluation criteria

- UI, application-rule, and data-ownership decisions are distinguished.
- Ambiguity is acknowledged where product policy changes the answer.
- No layer is treated as the default home for all “business logic.”

### Optional hints

Ask whether each behavior is about presentation, a stable application
operation, or ownership and delivery of data.

## Exercise 2 — Extract or keep

### Goal

Decide whether logic should remain in a ViewModel, remain in a repository, or
move to a focused use case.

### Scenario

A checkout ViewModel:

- owns loading and confirmation UI state;
- reads the cart from `CartRepository`;
- reads account status from `AccountRepository`;
- checks eligibility with 12 lines of reused rules;
- submits through `OrderRepository`;
- converts rejection reasons into localized screen text.

The cart repository also selects local/remote sources and resolves stale cart
data.

### Constraints

- Write a responsibility analysis before proposing code.
- Preserve screen state and localized text in UI ownership.
- Preserve source selection and freshness policy in Data ownership.
- Extract only logic that forms a coherent operation.
- Do not prescribe a DI framework or dedicated Gradle module.

### Expected deliverable

A responsibility table, proposed interfaces, a focused use-case signature if
justified, and a short dependency diagram. Include one alternative where no
use case is extracted and explain why it is weaker or sufficient.

### Evaluation criteria

- The proposed use case adds application policy or coordination.
- The ViewModel keeps presentation and lifecycle responsibilities.
- Repositories keep data ownership.
- The trade-off is argued before code is introduced.

### Optional hints

Separate “what the user operation means” from “how the screen displays it” and
“how each data set is obtained.”

## Exercise 3 — Multi-repository use case

### Goal

Design and implement one focused operation that coordinates at least two
repository abstractions.

### Scenario

Design `ReserveTrip`. It must read traveler eligibility, check an itinerary
quote, and create a reservation. The repositories may fail or suspend. A
rejected traveler is an expected outcome; an infrastructure failure follows
the repository contract.

### Constraints

- Define inputs and a focused output contract.
- State expected failure behavior separately from unexpected failures.
- State how cancellation propagates from the caller.
- Do not access DAO, Retrofit, `Context`, or Android lifecycle types.
- Do not launch a hidden coroutine scope.
- Write tests with controllable fakes for at least two repositories.

### Expected deliverable

Repository contracts, use-case code, a responsibility explanation, and tests
covering success, expected rejection, repository failure, and cancellation.

### Evaluation criteria

- The operation is cohesive and broader than one repository method.
- Data ownership remains in repositories.
- Output and failure semantics support caller decisions.
- Cancellation remains structured.
- Fakes expose meaningful behavior instead of verifying forwarding calls.

### Optional hints

Model expected rejection as an application outcome. Let the caller supply the
scope by invoking a suspending function.

## Exercise 4 — Architecture review

### Goal

Find responsibility and lifetime defects in a deliberately flawed Domain
layer.

### Scenario

Review this sketch:

```kotlin
class AppUseCases(
    private val context: Context,
    private val userDao: UserDao,
    private val ordersApi: OrdersApi,
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    suspend fun getUser(id: String) = userDao.get(id)

    fun loadOrders() {
        scope.launch { ordersApi.orders() }
    }

    fun formatUserName(user: User) =
        context.getString(R.string.user_name, user.name)

    suspend fun updateUser(user: User) = userDao.update(user)
}
```

### Constraints

- Identify pass-through methods, direct infrastructure access, Android
  dependency, unrelated operations, hidden lifetime, and swallowed results.
- Propose a corrected responsibility design, not a line-by-line rewrite.
- Keep simple operations direct when no use case is justified.
- Do not introduce a universal result wrapper or mandatory framework.

### Expected deliverable

A defect table, revised ownership map, selected interfaces, and pseudocode for
at most one justified use case. Explain which wrappers you delete.

### Evaluation criteria

- Every defect is tied to an ownership or lifecycle consequence.
- The corrected design does not merely move the same giant class.
- Repository and UI responsibilities are restored.
- Caller cancellation and observable outcomes are explicit.

### Optional hints

Ask which methods add application policy. A class with a Domain name is not
automatically Domain logic.
