# Practice — Android Testing Foundations

## Exercise 1 — ViewModel test plan

### Goal

Design a deterministic contract-test suite for a ViewModel with loading, retry,
cancellation, and navigation behavior.

### Scenario

`OrderViewModel` loads an order by an ID from `SavedStateHandle`. A retry waits
with bounded backoff. Starting another load makes the previous load obsolete.
Successful confirmation asks the UI host to navigate to a receipt.

### Constraints

- Use a fake repository with controllable success, failure, and suspension.
- Define initial, loading, content, error, retry, and latest-wins assertions.
- Use one coroutine test scheduler and virtual time.
- Prove obsolete repository work is cancelled without converting cancellation
  into an error state.
- Define whether navigation is durable state, a consumable effect, or a direct
  callback, and test its delivery contract.
- Test the saved order ID separately from real recreation/process restoration.
- Do not use real sleeps, Android owners in the ViewModel, or private-method
  assertions.

### Expected deliverable

A test matrix plus focused Kotlin test skeletons showing fixtures, dispatcher
control, actions, observations, and cleanup.

### Evaluation criteria

- every test names one risk;
- scheduler ownership is consistent;
- state transitions are observable;
- cancellation and application failure remain distinct;
- navigation delivery has an explicit policy;
- recreation claims match the boundary actually exercised.

### Optional hints

- A Main-dispatcher JUnit rule can support `viewModelScope`.
- Put never-ending collectors in `backgroundScope`.
- Assert `StateFlow.value` when current state is the contract.

## Exercise 2 — Repository integration boundary

### Goal

Design tests for repository coordination between deterministic remote and local
data sources.

### Scenario

`OfflineFirstCatalogRepository` reads the local source of truth, refreshes stale
records from a remote DTO service, maps them to validated application models,
and persists the result transactionally.

### Constraints

- Cover a fresh cache hit with no remote request.
- Cover stale data followed by a successful refresh.
- Cover remote failure while cached data remains observable.
- Cover malformed DTO/mapping failure without corrupting local truth.
- Cover owner cancellation during remote work and during persistence.
- Control freshness with an injected clock.
- Use fake remote/local sources for repository policy.
- Identify separate real-client and real-database boundary tests.
- Do not call a production backend or preempt full Room migration coverage.

### Expected deliverable

A boundary diagram, risk-to-test table, fake contracts, and a compact suite
outline separating repository policy, network adapter, mapper, and DAO risks.

### Evaluation criteria

- source-of-truth policy is explicit;
- each double has a deliberate role;
- cancellation is preserved;
- time and data are deterministic;
- real integrations are tested only where their behavior is required;
- cleanup and failure diagnostics are specified.

### Optional hints

- A behavior-rich in-memory fake may be clearer than many mocks.
- A mock server tests HTTP shape; a fake service tests repository policy.
- A real in-memory Room database tests SQL/Room behavior, not remote refresh
  policy.

## Exercise 3 — Flaky UI test repair

### Goal

Repair an unreliable UI test while preserving the user-visible risk it protects.

### Scenario

A checkout UI test waits with `Thread.sleep`, clicks the third text node,
depends on a process-global fake cart, leaves an Activity scenario open, and
sometimes observes navigation before asynchronous confirmation completes.

### Constraints

- Replace sleeps with Compose/Espresso/framework synchronization or a
  deterministic fake completion boundary.
- Replace positional selection with stable user-facing semantics or a justified
  tag/resource ID.
- Give every test a fresh dependency graph and cart.
- Close scenarios, servers, databases, collectors, and idling resources.
- Preserve one real navigation or UI integration risk.
- Add failure messages or diagnostic state that localizes failures.
- Explain animation and lifecycle-state control.
- Do not add production “test mode” branches.

### Expected deliverable

A before/after diagnosis, revised test skeleton, setup/cleanup policy, and a
short explanation of why each original source of flakiness is removed.

### Evaluation criteria

- no real-time waiting remains;
- selectors express stable behavior;
- test order and parallel execution cannot change state;
- asynchronous completion has an owner;
- the retained boundary still catches the target failure;
- resources are unconditionally released.

### Optional hints

- First ask whether this risk needs a full UI graph or a screen component test.
- Hilt replacement and resetting a mutable fake are separate concerns.
- `scenario.recreate()` is not a process-death test.

## Exercise 4 — Balanced checkout test portfolio

### Goal

Create a risk-based test strategy for a checkout feature without turning every
case into an end-to-end test.

### Scenario

Checkout validates a cart, calculates discounts, reads inventory, creates an
idempotent payment request, persists the receipt, navigates to confirmation,
and renders Compose UI. One critical happy path must be covered end to end.

### Constraints

- Include unit tests for rules, reducers, and mapping.
- Include repository/integration tests for inventory, payment, and persistence
  coordination.
- Include HTTP and database adapter boundary tests.
- Include navigation callback and graph tests.
- Include focused Compose semantics tests.
- Select one end-to-end path and state what is real or replaced.
- Map every test group to a failure risk, expected runtime, realism, and
  diagnostic cost.
- Include cancellation, duplicate submission, lifecycle recreation, isolation,
  and cleanup.
- Treat the pyramid as guidance rather than a fixed percentage.

### Expected deliverable

A portfolio table, boundary diagram, execution schedule, and rationale for
which risks deliberately are not duplicated at every level.

### Evaluation criteria

- the smallest reliable boundary is selected per risk;
- expensive tests are justified;
- external systems are controlled;
- critical wiring and user behavior receive higher-level evidence;
- cancellation and idempotency are covered;
- flakiness and maintenance costs are explicit.

### Optional hints

- Test business arithmetic without Android.
- Test request encoding with a mock server, not a mocked request builder.
- A visual snapshot cannot replace accessibility or interaction assertions.
