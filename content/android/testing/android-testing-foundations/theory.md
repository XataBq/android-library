# Android Testing Foundations

Testing is a confidence strategy. Architecture defines boundaries, boundaries
create test seams, and each test should own a specific risk. Prefer the
smallest boundary that can reliably expose that risk; add higher-level tests
for integration and behavior that only exists when real parts collaborate.

Library APIs below are examples, not timeless contracts. The AndroidX,
Compose, Navigation, Room, Hilt, OkHttp, JUnit, and `kotlinx.coroutines.test`
versions installed by a project determine exact artifacts, annotations,
runners, rules, and opt-in requirements. Verify them before copying code.

## 1. A test protects a contract from a specific risk

A useful test answers: “What failure would this catch?” It may protect a
business invariant, mapping contract, state transition, integration boundary,
or user-observable workflow. A test that merely executes lines without a
meaningful assertion supplies coverage, not necessarily confidence.

Refactoring confidence comes from asserting stable public outcomes rather than
private implementation shape:

```kotlin
class ApplyDiscount {
    operator fun invoke(subtotalCents: Int, percent: Int): Int {
        require(subtotalCents >= 0)
        require(percent in 0..100)
        return subtotalCents * (100 - percent) / 100
    }
}

@Test
fun `twenty percent discount preserves the pricing rule`() {
    val discounted = ApplyDiscount()(subtotalCents = 10_000, percent = 20)

    assertEquals(8_000, discounted)
}
```

The assertion protects the pricing rule. It does not check how many arithmetic
operations occurred.

## 2. Scope and execution environment are independent dimensions

Common boundary names vary between teams, so state what is real and what is
replaced:

| Boundary | Typical subject | Real collaborators | Main risk |
| --- | --- | --- | --- |
| unit | one class or function | none or very few | local logic |
| integration | collaborating units | selected adapters | boundary contract |
| component | feature slice | most feature parts | feature behavior |
| UI | rendered screen | UI toolkit and selected state | user interaction |
| end-to-end | complete workflow | most deployed path | system wiring |

Instrumentation describes *where* a test runs: in an Android process on a
physical or virtual device. Local describes host-side execution. A small DAO
test can be instrumented; a broad Robolectric test can be local. Therefore:

```text
unit ≠ local
integration ≠ instrumentation
UI ≠ end-to-end
```

Name the subject, real dependencies, doubles, runner, and protected risk
instead of relying on one overloaded label.

## 3. A test portfolio balances speed, realism, and diagnostics

Many focused tests usually give fast feedback and precise failures. Fewer
integration tests verify real collaboration. A small number of expensive
end-to-end tests protect critical wiring and user journeys. This is portfolio
guidance, not a mandatory pyramid quota.

A realistic test is not automatically valuable. A routine test that depends on
a production backend, wall-clock time, device locale, and prior test data can
be slow yet still miss the intended failure. Select portfolio layers by risk:

- pure policy and state transitions belong near the unit;
- serialization, SQL, dependency graphs, and navigation graphs need their real
  boundary somewhere;
- critical user-visible paths need UI or end-to-end evidence;
- compatibility, accessibility, performance, and visual risks require their
  own specialized checks.

## 4. Prefer the smallest reliable boundary

“Smallest” means the least expensive boundary that still contains the behavior
under test. A mapper failure needs no Activity. A Room query needs real Room and
SQLite semantics. A back-stack bug needs a navigation graph or UI host rather
than a mocked `NavController`.

Use this selection procedure:

```text
target failure
→ behavior required to expose it
→ smallest boundary containing that behavior
→ dependencies to control
→ observable outcome
```

Do not shrink a test until it stops being trustworthy. Do not enlarge it merely
because a device test feels more realistic.

## 5. Arrange–Act–Assert makes causality visible

Arrange creates the subject and preconditions. Act performs the single behavior
under review. Assert observes the public result. The pattern may be expressed
as Given–When–Then and may be compact when the test remains clear.

```kotlin
@Test
fun `empty cart cannot be submitted`() {
    // Arrange
    val checkout = Checkout(Cart(items = emptyList()))

    // Act
    val result = checkout.submit()

    // Assert
    assertEquals(CheckoutResult.EmptyCart, result)
}
```

Avoid a long test that repeatedly acts and asserts unrelated scenarios. A
single meaningful failure reason produces better diagnostics.

## 6. Observe state, interactions, or public behavior deliberately

State verification checks a result or state. Interaction verification checks a
collaborator call. Observable-behavior verification checks what a consumer can
see through the public contract. Prefer the least implementation-coupled
observation that proves the risk is controlled.

Interaction checks are appropriate when the interaction *is* the contract,
such as recording an audit event once:

```kotlin
class RecordingAudit : CheckoutAudit {
    val entries = mutableListOf<String>()
    override fun orderSubmitted(orderId: String) {
        entries += orderId
    }
}

@Test
fun `successful checkout records its order id once`() {
    val audit = RecordingAudit()
    val checkout = Checkout(audit)

    checkout.submit(orderId = "order-7")

    assertEquals(listOf("order-7"), audit.entries)
}
```

Do not verify every internal call, call order, or temporary value. Such tests
freeze implementation and fail during safe refactoring.

## 7. Test doubles have different jobs

Terminology varies, but these distinctions are useful:

- **dummy:** required value that is never used;
- **stub:** returns programmed answers;
- **fake:** lightweight working implementation unsuitable for production;
- **spy:** records observations, often while delegating;
- **mock:** programmed expectations plus interaction verification.

A controllable fake repository can model behavior without a mocking framework:

```kotlin
interface ProfileRepository {
    suspend fun profile(id: String): Profile
}

class FakeProfileRepository : ProfileRepository {
    private val profiles = mutableMapOf<String, Profile>()
    var requestedIds = emptyList<String>()
        private set

    fun seed(profile: Profile) {
        profiles[profile.id] = profile
    }

    override suspend fun profile(id: String): Profile {
        requestedIds = requestedIds + id
        return checkNotNull(profiles[id])
    }
}
```

The test owns the fake. A process-global fake would reintroduce order
dependence.

## 8. Fakes and mocks control different risks

Use a fake when several operations form meaningful stateful behavior: cache
reads and writes, emitted repository values, retry responses, or navigation
history. Use a mock or recording spy when a precise external interaction is
itself important and a state-based outcome cannot expose it.

```kotlin
@Test
fun `profile loader exposes repository result`() = runTest {
    val repository = FakeProfileRepository().apply {
        seed(Profile(id = "p-1", name = "Ada"))
    }
    val loader = LoadProfile(repository)

    val result = loader("p-1")

    assertEquals("Ada", result.name)
}
```

This test does not need to assert `requestedIds` unless selecting the exact ID
is the risk. Excessive call verification turns harmless refactors into
failures.

## 9. Testability is an architectural property

Testable code exposes dependencies and ownership. Constructor injection,
repository interfaces, pure mappers, explicit clocks and random sources,
injected dispatchers, and lifecycle owners let tests control nondeterminism.

```kotlin
class ExpiringSession(
    private val clock: Clock,
    private val expiresAt: Instant,
) {
    fun isExpired(): Boolean = !clock.instant().isBefore(expiresAt)
}

@Test
fun `session expires at the declared instant`() {
    val instant = Instant.parse("2030-01-01T00:00:00Z")
    val session = ExpiringSession(Clock.fixed(instant, ZoneOffset.UTC), instant)

    assertTrue(session.isExpired())
}
```

Do not add meaningless production interfaces only to satisfy a mocking tool.
Extract a boundary when the application genuinely needs ownership,
replacement, or policy separation. Avoid static lookup, mutable global state,
hidden dispatchers, and work that starts without an observable completion
contract.

## 10. Pure logic deserves the fastest focused tests

Validators, reducers, state machines, model mappers, and focused use cases can
usually run as local JVM tests without Android. Table-driven cases make
invariants visible:

```kotlin
@Test
fun `quantity validator rejects values outside purchase range`() {
    val validator = QuantityValidator(min = 1, max = 10)

    listOf(-1, 0, 11).forEach { quantity ->
        assertFalse(validator.isValid(quantity), "quantity=$quantity")
    }
    listOf(1, 5, 10).forEach { quantity ->
        assertTrue(validator.isValid(quantity), "quantity=$quantity")
    }
}
```

Test boundaries and representative edge cases. Avoid duplicating the standard
library or testing private helper methods directly.

## 11. ViewModel tests assert observable state transitions

A ViewModel test supplies fake repositories or use cases, controls the Main
dispatcher when `viewModelScope` uses it, sends public actions, and asserts
initial/loading/content/error states or a documented effect policy.

```kotlin
class ProfileViewModel(
    private val repository: ProfileRepository,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel() {
    private val _state = MutableStateFlow<ProfileUiState>(ProfileUiState.Idle)
    val state: StateFlow<ProfileUiState> = _state.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _state.value = ProfileUiState.Loading
            val id = checkNotNull(savedStateHandle["profile-id"])
            _state.value = ProfileUiState.Content(repository.profile(id))
        }
    }
}
```

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `load publishes content for saved profile id`() = runTest {
    Dispatchers.setMain(StandardTestDispatcher(testScheduler))
    try {
        val repository = FakeProfileRepository().apply {
            seed(Profile("p-1", "Ada"))
        }
        val handle = SavedStateHandle(mapOf("profile-id" to "p-1"))
        val viewModel = ProfileViewModel(repository, handle)

        assertEquals(ProfileUiState.Idle, viewModel.state.value)
        viewModel.load()
        advanceUntilIdle()

        assertEquals(
            ProfileUiState.Content(Profile("p-1", "Ada")),
            viewModel.state.value,
        )
    } finally {
        Dispatchers.resetMain()
    }
}
```

Constructing `SavedStateHandle` verifies the ViewModel's small reconstruction
input, not real process death. Recreation and process-death boundaries require
separate higher-level evidence.

## 12. Coroutine tests control one scheduler and virtual time

`runTest` supplies a `TestScope`, scheduler, and test dispatcher. New work on a
`StandardTestDispatcher` is queued until the test yields with `runCurrent`,
`advanceTimeBy`, `advanceUntilIdle`, `join`, or another suspension. All test
dispatchers involved in one scenario should share one scheduler.

```kotlin
class DelayedSearch(
    private val dispatcher: CoroutineDispatcher,
) {
    suspend fun invoke(query: String): String = withContext(dispatcher) {
        delay(1_000)
        query.trim().uppercase()
    }
}

@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `search completes after debounce budget`() = runTest {
    val search = DelayedSearch(StandardTestDispatcher(testScheduler))
    val result = async { search(" ada ") }

    advanceTimeBy(999)
    assertFalse(result.isCompleted)
    advanceTimeBy(1)
    runCurrent()

    assertEquals("ADA", result.await())
}
```

Virtual time skips `delay`; it does not accelerate arbitrary blocking I/O.
Tests should close or cancel owned work. `runTest` reporting unfinished child
jobs is useful evidence of leaked ownership, not noise to suppress.

Cancellation is a distinct outcome and must not be swallowed:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `owner cancellation reaches repository work`() = runTest {
    var cleanupRan = false
    val job = launch {
        try {
            awaitCancellation()
        } finally {
            cleanupRan = true
        }
    }
    runCurrent()

    job.cancelAndJoin()

    assertTrue(job.isCancelled)
    assertTrue(cleanupRan)
}
```

Do not wrap suspend work in ordinary `runCatching`; it also catches
`CancellationException` unless cancellation is explicitly rethrown.

## 13. Main dispatcher replacement and injection solve different seams

Code that starts `viewModelScope` work uses Main, so a local ViewModel test
normally installs a test Main dispatcher. A reusable JUnit 4 rule centralizes
reset:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    val dispatcher: TestDispatcher = StandardTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(dispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

Inject IO/Default policy into Data or CPU-bound implementations:

```kotlin
class JsonProfileParser(
    private val dispatcher: CoroutineDispatcher,
) {
    suspend fun parse(json: String): ProfileDto = withContext(dispatcher) {
        decodeProfile(json)
    }
}
```

Replacing Main supports framework-owned ViewModel behavior; dispatcher
injection controls application-owned execution. Neither means production code
should expose a “test mode.” Check installed coroutine-test and JUnit APIs:
their annotations and scheduling behavior are version-sensitive.

## 14. Flow tests must respect finite, hot, replay, and conflation contracts

A finite cold Flow can use terminal operators:

```kotlin
@Test
fun `cold flow maps every finite value`() = runTest {
    val actual = flowOf(1, 2, 3)
        .map { it * 10 }
        .toList()

    assertEquals(listOf(10, 20, 30), actual)
}
```

For `StateFlow`, current state is often the stable contract. A `stateIn` using
`Lazily` or `WhileSubscribed` needs an active collector before upstream starts:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `while-subscribed state exposes latest repository value`() = runTest {
    val upstream = MutableSharedFlow<Int>()
    val state = upstream.stateIn(
        scope = backgroundScope,
        started = SharingStarted.WhileSubscribed(),
        initialValue = 0,
    )
    backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
        state.collect { }
    }
    runCurrent()

    upstream.emit(7)

    assertEquals(7, state.value)
}
```

`StateFlow` is conflated, so a test should not assume every intermediate value
is observed unless that is an explicit separately modeled contract.

For `SharedFlow`, start the subscriber before emitting, then cancel infinite
collection through `backgroundScope` or an explicit Job:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `shared flow delivers to an active subscriber`() = runTest {
    val events = MutableSharedFlow<String>(replay = 0)
    val observed = mutableListOf<String>()
    backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
        events.take(2).toList(observed)
    }

    events.emit("first")
    events.emit("second")

    assertEquals(listOf("first", "second"), observed)
}
```

Optional libraries such as Turbine can improve collection ergonomics but do not
change Flow semantics and are not required here.

## 15. Repository tests prove coordination and source-of-truth policy

Test a repository with deterministic remote and local fakes. Cover cache hits,
freshness, refresh, persistence, error mapping, cancellation, and concurrent
coordination according to its contract.

```kotlin
@Test
fun `refresh maps remote profile then updates local source`() = runTest {
    val remote = FakeProfileRemote(
        ProfileDto(id = "p-1", displayName = "Ada"),
    )
    val local = FakeProfileLocal()
    val repository = OfflineFirstProfileRepository(remote, local)

    repository.refresh("p-1")

    assertEquals(Profile("p-1", "Ada"), local.profile("p-1"))
}
```

A repository unit test may fake both sources. Add narrower boundary tests for
the real serializer, HTTP client, DAO, transaction, or cache implementation.
Do not call a production backend in routine tests.

## 16. Network tests separate mapping from transport behavior

Mapping failures are pure and fast:

```kotlin
@Test
fun `unknown server status is rejected by mapper`() {
    val dto = ProfileDto(id = "p-1", displayName = "Ada", status = "future")

    assertFailsWith<ProfileMappingException> {
        dto.toProfile()
    }
}
```

A mock server exercises real request construction, client adapters, status
handling, and serialization without production network dependency:

```kotlin
@Test
fun `service sends profile path and parses response`() = runTest {
    val server = MockWebServer()
    server.start()
    try {
        server.enqueue(
            MockResponse.Builder()
                .code(200)
                .body("""{"id":"p-1","display_name":"Ada"}""")
                .build(),
        )
        val service = createProfileService(server.url("/"))

        val profile = service.profile("p-1")

        assertEquals("Ada", profile.displayName)
        assertEquals("/profiles/p-1", server.takeRequest().url.encodedPath)
    } finally {
        server.close()
    }
}
```

Also cover malformed bodies, declared error payloads, timeout budgets, bounded
retry, and cancellation. Cancellation tests must prove the owned client call
stops; converting `CancellationException` to a network failure is incorrect.
MockWebServer and HTTP client APIs differ across versions, so adapt builders,
packages, and coroutine adapters to installed artifacts.

## 17. Database tests use the real database only for database risks

Fake a DAO when testing repository policy. Use real Room/SQLite when testing
queries, constraints, transactions, invalidation, or migrations. Current
Android guidance recommends device tests for fidelity with device SQLite.

```kotlin
@RunWith(AndroidJUnit4::class)
class ProfileDaoTest {
    private lateinit var database: TestDatabase

    @Before
    fun createDatabase() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(
            context,
            TestDatabase::class.java,
        ).build()
    }

    @After
    fun closeDatabase() {
        database.close()
    }

    @Test
    fun insertThenObserveReturnsProfile() = runTest {
        database.profileDao().upsert(ProfileEntity("p-1", "Ada"))

        assertEquals(
            ProfileEntity("p-1", "Ada"),
            database.profileDao().observe("p-1").first(),
        )
    }
}
```

Every test gets a fresh database and closes it. Migration tests start from
exported old schemas and verify preserved data and the final schema. Exact Room
test helpers are version-sensitive and belong to the future Room topic in more
depth.

## 18. Navigation tests separate intent from graph mechanics

Destinations should accept callbacks rather than `NavController`, so navigation
intent is a plain test seam:

```kotlin
interface CheckoutNavigator {
    fun receipt(orderId: String)
}

class RecordingCheckoutNavigator : CheckoutNavigator {
    val orderIds = mutableListOf<String>()
    override fun receipt(orderId: String) {
        orderIds += orderId
    }
}

@Test
fun `successful submit requests receipt destination`() {
    val navigator = RecordingCheckoutNavigator()
    val presenter = CheckoutPresenter(navigator)

    presenter.onSubmitted("order-9")

    assertEquals(listOf("order-9"), navigator.orderIds)
}
```

Use a real test navigation controller when the graph, destination route, deep
link, result, or back stack is the risk:

```kotlin
@get:Rule
val composeRule = createComposeRule()

@Test
fun `profile action navigates to profile route`() {
    lateinit var controller: TestNavHostController
    composeRule.setContent {
        controller = TestNavHostController(LocalContext.current).apply {
            navigatorProvider.addNavigator(ComposeNavigator())
        }
        AppNavHost(controller)
    }

    composeRule.onNodeWithText("Profile").performClick()

    assertTrue(
        controller.currentBackStackEntry
            ?.destination
            ?.hasRoute<ProfileRoute>() == true,
    )
}
```

Typed route and `TestNavHostController` APIs are Navigation-version-sensitive.
Prefer asserting the displayed destination through user behavior when possible;
inspect controller state when the back-stack contract itself is under test.

## 19. UI tests assert behavior through stable semantics

A UI test should interact as a user would: find meaningful controls, perform an
action, and assert visible or accessibility-relevant state. Prefer text, role,
content description, label, or another stable semantic contract. Use a test tag
or resource ID deliberately when no appropriate user semantic exists.

Avoid pixel coordinates, child positions, internal composable names, private
ViewModel fields, and arbitrary polling. A screen component test can supply
state and callbacks directly; a broader test can use a fake repository through
the test graph.

## 20. Compose tests operate on the semantics tree

Compose tests query semantics nodes, perform actions, and assert observable
properties:

```kotlin
@get:Rule
val composeRule = createComposeRule()

@Test
fun `retry action invokes public callback`() {
    var retried = false
    composeRule.setContent {
        ProfileScreen(
            state = ProfileUiState.Error,
            onRetry = { retried = true },
        )
    }

    composeRule.onNodeWithText("Retry")
        .assertHasClickAction()
        .performClick()

    assertTrue(retried)
}
```

The merged semantics tree is the default consumer-facing view. Use the
unmerged tree for diagnosis or a deliberate lower-level contract, not as the
first response to a failed selector. Test tags are a fallback, not a substitute
for accessible semantics.

State restoration tests require an owner or restoration test facility that
actually saves and restores state. A normal recomposition does not prove
Activity recreation or process reconstruction. Compose test rules and
restoration helpers are version-sensitive; check installed Compose artifacts.

## 21. Espresso synchronizes known View-system work

Espresso uses matcher, action, and assertion APIs:

```kotlin
@RunWith(AndroidJUnit4::class)
class ProfileScreenTest {
    @Test
    fun retryDisplaysLoadedProfile() {
        onView(withId(R.id.retry)).perform(click())

        onView(withText("Ada")).check(matches(isDisplayed()))
    }
}
```

Espresso waits for the main message queue and registered idling resources.
Background work unknown to Espresso needs a lifecycle-aware synchronization
boundary such as an `IdlingResource`, or a fake dependency that exposes
deterministic completion. Register resources before use and unregister them
during cleanup.

`ActivityScenario` and `FragmentScenario` can drive framework lifecycle states.
They do not automatically turn an assertion into an end-to-end test, and their
exact APIs and supported host assumptions are version-sensitive.

## 22. Lifecycle tests name the scenario they reproduce

Recreation, STOPPED/STARTED transitions, Fragment View destruction, navigation
removal, and process death are distinct. Test the exact owner transition:

```kotlin
@RunWith(AndroidJUnit4::class)
class ProfileActivityRecreationTest {
    @Test
    fun selectedTabSurvivesActivityRecreation() {
        ActivityScenario.launch(ProfileActivity::class.java).use { scenario ->
            scenario.onActivity { it.selectTab("posts") }

            scenario.recreate()

            scenario.onActivity {
                assertEquals("posts", it.selectedTab())
            }
        }
    }
}
```

`recreate()` verifies Activity recreation, not operating-system process death.
For lifecycle-aware collection, move the owner below and above `STARTED` and
assert subscription policy. For Fragments, destroy and recreate the View while
the Fragment may remain. Close scenarios and collectors so later tests inherit
no owners.

## 23. Flakiness is uncontrolled input, time, or ownership

Common sources are wall-clock time, real networks, shared mutable state,
test-order dependence, animation, races, unstable selectors, random values,
unclosed databases/servers/scenarios, and asynchronous work without an owner.

This commented line documents the anti-pattern; no test should execute it:

```kotlin
@Test
fun `do not wait for asynchronous state with a sleep`() {
    // Thread.sleep(2_000) // Flaky, slow, and unrelated to actual completion.
}
```

Use virtual time for coroutine delays and framework synchronization for UI:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@Test
fun `retry delay uses virtual time`() = runTest {
    val policy = RetryPolicy(StandardTestDispatcher(testScheduler))
    val result = async { policy.retry { "ready" } }

    advanceUntilIdle()

    assertEquals("ready", result.await())
}
```

For test-graph isolation, Hilt can replace a production module for a suite:

```kotlin
@Module
@TestInstallIn(
    components = [SingletonComponent::class],
    replaces = [ProfileRepositoryModule::class],
)
abstract class FakeProfileRepositoryModule {
    @Binds
    abstract fun bindRepository(
        fake: InMemoryProfileRepository,
    ): ProfileRepository
}
```

Hilt creates test components, but a mutable fake still needs fresh state per
test. `@TestInstallIn`, `@UninstallModules`, `@BindValue`, runner setup, and rule
ordering have distinct current contracts; verify the installed Hilt version.
Never mutate a production singleton as test setup.

## 24. Snapshot and golden tests cover visual regression, not all behavior

A snapshot or golden compares rendered output against an approved artifact. It
can efficiently detect spacing, color, typography, or component drift across a
large visual surface.

Its trade-offs include broad diffs, review fatigue, renderer/font/device
dependence, costly baselines, and accidental approval of a regression. A
matching image does not prove navigation, accessibility semantics, focus,
input behavior, or business correctness. Stabilize environment inputs, keep
baselines reviewable, and pair visual tests with semantic and behavioral tests.
Screenshot APIs are tool- and version-specific; this foundation does not select
one.

## 25. Names and diagnostics should localize one failure

A useful name states precondition, action, and outcome:

```kotlin
@Test
fun `expired cache refreshes remote data and persists mapped result`() = runTest {
    // One scenario; assertions explain the repository contract.
}
```

Prefer domain language to method names. Include relevant IDs, expected/actual
state, virtual time, route, or seed in failure messages. Do not hide a dozen
unrelated assertions behind one giant fixture. Helpers should remove noise,
not conceal the action or outcome.

## 26. Anti-pattern review and test-strategy decision guide

Avoid:

- only UI tests or only mocked unit tests;
- testing private methods instead of public behavior;
- verifying every collaborator call;
- executing `Thread.sleep` or polling an arbitrary timeout;
- using a real backend in routine tests;
- mutating a singleton or sharing fake state;
- relying on test order;
- branching production behavior on test mode;
- swallowing cancellation or leaving background collectors alive;
- asserting implementation-only selectors;
- one giant end-to-end fixture for every risk;
- uncontrolled clocks, locale, randomness, animation, or dispatchers;
- failing to close databases, servers, scenarios, and graphs;
- confusing instrumentation environment with integration scope.

Finish every plan with:

```text
What risk is covered?
What is the smallest reliable boundary?
What dependencies must be controlled?
What time/lifecycle state is involved?
What should be observed?
Why could this test become flaky?
```

Architecture defines boundaries. Boundaries define test seams. Let each test
own one risk, make its nondeterminism explicit, and move upward only when the
real integration or user-observable behavior is necessary evidence.
