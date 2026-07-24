# Android Dependency Injection and Scoping

Dependency injection is an object-construction technique. It makes required
collaborators visible, moves implementation selection to a composition
boundary, and gives every reused object an owner. Hilt, Dagger, Koin, and manual
containers can implement DI; none can decide the correct architecture merely
from annotations.

## 1. What dependency injection solves

An object should receive what it needs instead of constructing or locating
hidden collaborators. Construction then becomes replaceable, dependencies are
reviewable at the API boundary, and lifetime decisions move to an owner.

```kotlin
class SyncProfile(
    private val profiles: ProfileRepository,
    private val clock: Clock,
) {
    suspend operator fun invoke(userId: String): Profile =
        profiles.refresh(userId, refreshedAt = clock.instant())
}
```

The constructor declares dependencies. A composition root chooses their
implementations. A scope may decide reuse. The owner destroys or releases the
graph when its lifetime ends.

## 2. Dependency inversion is a direction rule

Dependency inversion means higher-level policy depends on an abstraction
appropriate to its needs, while lower-level infrastructure implements that
abstraction. DI is one way to supply the implementation; the two concepts are
related but not identical.

```kotlin
interface ProfileRepository {
    suspend fun refresh(userId: String, refreshedAt: Instant): Profile
}

class NetworkBackedProfileRepository(
    private val remote: ProfileRemoteDataSource,
    private val local: ProfileLocalDataSource,
) : ProfileRepository {
    override suspend fun refresh(
        userId: String,
        refreshedAt: Instant,
    ): Profile = TODO("coordinate sources and return application data")
}
```

`SyncProfile` depends on an application contract, not Retrofit or Room.
Changing wiring does not repair a badly chosen abstraction.

## 3. Constructor injection is the default

Constructor injection makes invalid half-initialized objects difficult to
create. Required dependencies are visible, immutable references are natural,
and tests call an ordinary constructor. Field or method injection is reserved
for framework-created objects that cannot use constructor injection directly.

```kotlin
class CheckoutViewModel(
    private val loadCheckout: LoadCheckout,
    private val submitOrder: SubmitOrder,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel()
```

A growing constructor is useful design feedback. Do not hide it with a
container parameter; ask whether the class owns too many responsibilities.

## 4. Composition root chooses concrete objects

A composition root is the narrow boundary where implementations are selected
and the graph is assembled. An Android app can have an application root plus
smaller Activity or feature roots. Construction belongs near framework entry,
not scattered through business methods.

```kotlin
class AppCompositionRoot(
    application: Application,
) {
    private val json = Json { ignoreUnknownKeys = true }
    private val httpClient = buildHttpClient(application)
    private val profileService = createProfileService(httpClient, json)
    private val profileDatabase = createProfileDatabase(application)

    val profileRepository: ProfileRepository =
        NetworkBackedProfileRepository(
            remote = ProfileRemoteDataSource(profileService),
            local = ProfileLocalDataSource(profileDatabase.profileDao()),
        )
}
```

This manual root contains construction details. It should not become a global
bag that arbitrary objects query.

## 5. An object graph has nodes, edges, and owners

Objects are nodes. Constructor requirements are directed edges. Transitive
dependencies form a graph. A graph builder must resolve every required edge,
select a binding when several candidates exist, and reject cycles that cannot
be constructed.

```kotlin
data class CheckoutGraph(
    val viewModelFactory: CheckoutViewModelFactory,
    val paymentCoordinator: PaymentCoordinator,
)

fun createCheckoutGraph(app: AppCompositionRoot): CheckoutGraph {
    val validator = CheckoutValidator()
    val coordinator = PaymentCoordinator(app.profileRepository, validator)
    return CheckoutGraph(
        viewModelFactory = CheckoutViewModelFactory(coordinator),
        paymentCoordinator = coordinator,
    )
}
```

Whether two consumers receive the same `PaymentCoordinator` is an explicit
reuse decision. Reachability from `CheckoutGraph` bounds its lifetime.

## 6. DI is not service location

With DI, a class receives dependencies. With a service locator, the class asks
a container during execution. Lookup hides requirements, moves mistakes to
runtime, couples tests to global state, and makes non-process scopes awkward.

```kotlin
// Anti-pattern: the dependency is absent from the public construction contract.
class HiddenCheckoutViewModel : ViewModel() {
    private val repository =
        GlobalServices.resolve<CheckoutRepository>()
}
```

Passing a container, `Application`, or `Map<KClass<*>, Any>` through layers is
still service location. Framework entry points are narrow adapters for objects
the framework owns; they are not permission for business code to query Hilt.

## 7. Manual DI exposes the mechanics

Manual DI is sufficient for small graphs and useful for learning. A container
can own long-lived objects and create short-lived feature graphs through
explicit methods.

```kotlin
class AppContainer(
    private val application: Application,
) {
    val sessionStore: SessionStore by lazy {
        EncryptedSessionStore(application.applicationContext)
    }

    val accountRepository: AccountRepository by lazy {
        DefaultAccountRepository(sessionStore)
    }

    fun createLoginGraph(): LoginGraph =
        LoginGraph(
            login = Login(accountRepository),
            analytics = LoginAnalytics(),
        )
}
```

The application owns `AppContainer`; the UI owner holds `LoginGraph` only while
the flow exists. Avoid a public static `AppContainer.instance`.

## 8. Frameworks automate wiring, not architecture

Compile-time tools such as Dagger/Hilt generate graph construction and validate
many missing, duplicate, or cyclic bindings. Runtime containers resolve
registrations while the app runs. Frameworks may automate providers, scopes,
entry points, and test replacement. They do not decide repository boundaries,
safe Context use, correct owner lifetime, or whether mutable global state is
appropriate.

```kotlin
interface Analytics {
    fun record(event: AnalyticsEvent)
}

class FileAnalytics @Inject constructor(
    private val sink: AnalyticsSink,
) : Analytics {
    override fun record(event: AnalyticsEvent) = sink.append(event)
}

@Module
@InstallIn(SingletonComponent::class)
abstract class AnalyticsModule {
    @Binds
    abstract fun bindAnalytics(
        implementation: FileAnalytics,
    ): Analytics
}
```

This is Hilt/Dagger syntax, not universal DI vocabulary. The official Hilt page
showed Hilt 2.57.1 on `2026-07-24`; use the versions and processor configuration
installed in the actual project.

## 9. Provider, lazy, and factory have different contracts

A provider answers “obtain an instance now.” An unscoped provider may create a
new instance per request; a scoped provider returns the scoped instance. Lazy
usually memoizes one provider result for that injected lazy wrapper. A factory
accepts runtime input and states creation semantics explicitly.

```kotlin
fun interface Provider<T> {
    fun get(): T
}

class ReportFactory(
    private val formatterProvider: Provider<ReportFormatter>,
) {
    fun create(reportId: String): ReportSession =
        ReportSession(reportId, formatterProvider.get())
}
```

Do not infer object identity from the word “provider.” Document whether each
call creates, reuses, or delegates to another owner.

## 10. Scope is lifetime plus owner

A scope name is incomplete without:

```text
owner
→ creation boundary
→ reuse boundary
→ destruction boundary
```

```kotlin
class OwnedScope<T : AutoCloseable>(
    private val create: () -> T,
) : AutoCloseable {
    private val lazyValue = lazy(create)

    fun instance(): T = lazyValue.value

    override fun close() {
        if (lazyValue.isInitialized()) lazyValue.value.close()
    }
}
```

Real DI containers manage this differently, but the ownership question is the
same. A scope annotation describes reuse within one component instance; it does
not make an object immortal.

## 11. Unscoped does not mean ownerless

Hilt and Dagger bindings are unscoped by default: each request normally creates
a new instance. That instance still becomes reachable from a scoped or
framework-owned consumer and dies when nothing owns it.

```kotlin
class PriceFormatter @Inject constructor(
    private val localeProvider: LocaleProvider,
)

class ProductPresenter @Inject constructor(
    val titleFormatter: PriceFormatter,
    val subtitleFormatter: PriceFormatter,
)
```

Without a scope, the two formatter requests may receive different instances.
That is correct for stateless cheap objects. Scope only when shared identity is
required for correctness, synchronization, or measured construction cost.

## 12. Application scope is process scope

Hilt's `SingletonComponent` is created for the Android application process and
destroyed with it. `@Singleton` means one instance per component instance, not
across process death, device restart, account, or test process.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DataModule {
    @Provides
    @Singleton
    fun provideHttpClient(
        auth: AccessTokenInterceptor,
    ): OkHttpClient = buildSharedHttpClient(auth)
}
```

Long-lived repositories and clients can fit process ownership. Mutable session
facts still need an explicit synchronized owner and logout/reset contract.
Process scope is not persistence.

## 13. Activity, retained Activity, Fragment, and View differ

In Hilt, `ActivityComponent`/`@ActivityScoped` follows one Activity instance and
does not survive its recreation. `ActivityRetainedComponent` survives
configuration changes for the logical Activity and ends at its final
destruction. `FragmentComponent`/`@FragmentScoped` follows the Fragment
instance, not its shorter View lifecycle.

```kotlin
@ActivityScoped
class ActivityUiCoordinator @Inject constructor(
    @ActivityContext private val activityContext: Context,
)

@FragmentScoped
class FragmentMenuCoordinator @Inject constructor(
    private val menuPolicy: MenuPolicy,
)
```

A Fragment-scoped object must not retain a Fragment View or binding after
`onDestroyView`. A View- or render-lifetime collaborator should be created and
released with that UI owner instead.

## 14. ViewModel scope follows ViewModelStoreOwner

A ViewModel is owned by a `ViewModelStoreOwner`: Activity, Fragment,
destination, navigation graph entry, or another explicit owner. Hilt creates a
`ViewModelComponent` for a Hilt ViewModel. `@ViewModelScoped` reuses one binding
inside that ViewModel graph; different ViewModels get different instances.

```kotlin
@HiltViewModel
class ProductViewModel @Inject constructor(
    private val products: ProductRepository,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel() {
    private val productId: String =
        checkNotNull(savedStateHandle["productId"])
}
```

Obtain Hilt ViewModels through `ViewModelProvider`, `by viewModels()`, or the
appropriate Compose/navigation helper; do not request them as ordinary injected
objects. Never inject Activity, Fragment, View, binding, or `NavController`
into a ViewModel.

## 15. Navigation graph scope is entry ownership

A navigation graph entry can be the `ViewModelStoreOwner` for workflow state.
The ViewModel and its `@ViewModelScoped` dependencies end when that entry is
permanently popped. Hilt does not define a general custom “navigation graph
component scope” for arbitrary objects merely because a graph exists.

```kotlin
@AndroidEntryPoint
class PaymentFragment : Fragment(R.layout.payment_fragment) {
    private val checkout: CheckoutViewModel by hiltNavGraphViewModels(
        R.id.checkout_graph,
    )
}
```

The shown Views API is artifact- and version-sensitive. Compose Navigation and
Navigation 3 use different current helpers and entry models. Verify installed
Navigation/Hilt integrations. Graph scope is for one coherent workflow, not an
Activity-wide event bus.

## 16. Qualifiers distinguish semantic bindings

When two bindings have the same Kotlin type but different meaning, use a typed
qualifier. Qualify both provider and injection site. Avoid string keys and
unqualified “default” bindings that silently choose the wrong client,
dispatcher, or endpoint.

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class PublicApi

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class AuthenticatedApi

class AccountRemoteDataSource @Inject constructor(
    @AuthenticatedApi private val client: OkHttpClient,
)

class CatalogRemoteDataSource @Inject constructor(
    @PublicApi private val client: OkHttpClient,
)
```

Qualifiers express semantic identity; they do not create a scope or a second
instance by themselves.

## 17. Multibinding assembles contributions

Set or map multibindings let features contribute handlers, validators, or
strategies without a central module listing every implementation. A set has no
business ordering guarantee. A map needs stable unique keys and an explicit
selection policy.

```kotlin
interface CheckoutValidator {
    fun validate(draft: CheckoutDraft): List<ValidationIssue>
}

@Module
@InstallIn(ViewModelComponent::class)
abstract class CheckoutValidationModule {
    @Binds
    @IntoSet
    abstract fun bindAddressValidator(
        validator: AddressValidator,
    ): CheckoutValidator

    @Binds
    @IntoSet
    abstract fun bindPaymentValidator(
        validator: PaymentValidator,
    ): CheckoutValidator
}

class ValidateCheckout @Inject constructor(
    private val validators: Set<@JvmSuppressWildcards CheckoutValidator>,
)
```

The wildcard detail is Dagger/Kotlin-specific and can vary with toolchain
versions. If order matters, model priority explicitly and sort; do not depend
on iteration accident.

## 18. Assisted injection combines graph and runtime input

Assisted injection supplies normal graph dependencies plus a value known only
at runtime. A factory makes that boundary explicit. It is appropriate for some
Workers, runtime sessions, and objects the DI owner cannot preconstruct.

```kotlin
class ExportSession @AssistedInject constructor(
    private val exporter: ReportExporter,
    @Assisted private val destination: Uri,
) {
    @AssistedFactory
    interface Factory {
        fun create(destination: Uri): ExportSession
    }
}
```

Hilt ViewModel assisted injection is supported by current Hilt APIs but is
version-sensitive and has special creation callbacks. Assisted values are not
automatically saved across process recreation. Prefer `SavedStateHandle` for
small restorable route inputs; never pass a shorter-lived Activity, Fragment,
View, or binding as an assisted argument.

## 19. Context kind and scope must match

Application Context is process-owned and appropriate for Data adapters that
need application resources, files, or system services. Activity or themed
Context is UI-owned and required for theme-aware inflation or window work.
Inject the narrowest semantic type and never place an Activity Context into a
process-scoped object.

```kotlin
@Singleton
class PreferencesStore @Inject constructor(
    @ApplicationContext context: Context,
) {
    private val preferences =
        context.getSharedPreferences("settings", Context.MODE_PRIVATE)
}

@ActivityScoped
class DialogPresenter @Inject constructor(
    @ActivityContext private val context: Context,
)
```

If Domain or ViewModel appears to need Context for formatting or services,
move that platform concern behind UI/Data abstraction rather than injecting
Context everywhere.

## 20. Cycles reveal misplaced responsibilities

Constructor cycles cannot be assembled without delayed lookup and usually
signal confused ownership or collaboration.

```kotlin
// Smell: neither object can be constructed first.
class SessionRepository(
    private val analytics: Analytics,
)

class Analytics(
    private val sessionRepository: SessionRepository,
)
```

Split the minimal information needed, invert event delivery at the composition
boundary, or introduce a cohesive mediator owned above both—not a global event
bus that hides the same cycle.

```kotlin
fun interface SessionSnapshot {
    fun currentSessionId(): String?
}

class Analytics(
    private val sessions: SessionSnapshot,
)

class DefaultSessionRepository : SessionSnapshot {
    override fun currentSessionId(): String? = TODO()
}
```

Also question giant god objects, provider chains, split interfaces created only
to silence a cycle, and broad scopes used to make construction “easier.”

## 21. Tests replace dependencies at the right boundary

Constructor-injected units need no DI framework in a unit test. Build the
subject with fakes, clocks, and test dispatchers. Each test owns a fresh graph.

```kotlin
@Test
fun syncProfile_usesRepositoryAndClock() = runTest {
    val repository = FakeProfileRepository()
    val clock = Clock.fixed(INSTANT, ZoneOffset.UTC)
    val sync = SyncProfile(repository, clock)

    sync("user-1")

    assertEquals(INSTANT, repository.refreshes.single().refreshedAt)
}
```

For Hilt integration tests, replace a production module or binding with a test
binding and let the framework create a fresh test component.

```kotlin
@Module
@TestInstallIn(
    components = [SingletonComponent::class],
    replaces = [AnalyticsModule::class],
)
abstract class FakeAnalyticsModule {
    @Binds
    @Singleton
    abstract fun bindAnalytics(
        fake: FakeAnalytics,
    ): Analytics
}
```

`@TestInstallIn`, `@UninstallModules`, and `@BindValue` have different scope and
build-cost trade-offs. Verify current Hilt testing APIs. Never make tests pass
by mutating a production singleton that leaks state into later or parallel
tests.

## 22. Keep framework APIs at the composition boundary

Domain contracts and ordinary business classes should not depend on `@Inject`,
Hilt components, container APIs, Android Context, or generated factories.
Annotations in concrete Data/UI implementation constructors can be acceptable
when they remain wiring metadata and do not change business semantics.

```kotlin
// Framework-free Domain policy.
class ApproveCheckout(
    private val creditPolicy: CreditPolicy,
    private val inventory: InventoryRepository,
) {
    suspend operator fun invoke(draft: CheckoutDraft): Approval =
        creditPolicy.approve(draft, inventory.availableFor(draft))
}
```

Entry points and field injection are framework-boundary escape hatches for
objects the framework constructs. Keep them narrow; do not pass an entry point
or component into the resulting business graph.

## 23. Scope and graph anti-patterns

```kotlin
// Leak: an Activity-owned object is captured by a process-scoped object.
@Singleton
class GlobalScreenRegistry @Inject constructor() {
    var currentActivity: Activity? = null
}
```

Avoid:

- field injection by default when constructor injection is possible;
- a global service locator or static object graph;
- passing the container through layers;
- every dependency annotated `@Singleton`;
- mutable process-global state without explicit synchronization/reset policy;
- Activity Context, View, Fragment, binding, or NavController in a singleton or
  ViewModel;
- Fragment-scoped objects retaining a destroyed Fragment View;
- injecting Retrofit/service types into UI;
- duplicate same-type bindings without qualifiers;
- assuming multibinding order;
- provider lookup hiding an oversized constructor;
- assisted values assumed to survive process death;
- giant modules that mix unrelated ownership;
- test setup mutating production singletons;
- a delayed provider used only to conceal a graph cycle.

Annotations can make all of these compile. Compilation proves wiring
consistency, not ownership correctness.

## 24. Dependency graph decision guide

For every object, answer:

1. What does it depend on, and are those dependencies visible in its
   constructor?
2. Does high-level policy depend on a stable abstraction?
3. Which composition root creates or binds the implementation?
4. Who owns the object, and when is that owner created and destroyed?
5. Must several consumers share identity, or should creation remain unscoped?
6. Does a provider need lazy access, or does a factory need runtime input?
7. Do same-type bindings need semantic qualifiers?
8. Are contributions unordered, or is explicit priority required?
9. How is the dependency replaced with a fresh fake or test binding?
10. Can Context, UI objects, container APIs, or broad scope leak a shorter-lived
    framework owner?

The stable model is independent of annotation spelling:

```text
constructor declares dependency
composition root creates implementation
scope defines lifetime and reuse
owner controls destruction
```
