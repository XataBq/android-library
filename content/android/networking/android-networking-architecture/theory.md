# Android Networking Architecture

Networking is not “call Retrofit from ViewModel.” It is a Data-layer
implementation that translates an unreliable, versioned HTTP boundary into
stable application contracts. Examples use Retrofit- and OkHttp-style APIs
because they are common, but the ownership model also applies to Ktor, platform
clients, generated clients, and future libraries.

## 1. Networking belongs in the Data layer

UI renders state and sends actions. ViewModel coordinates a UI scenario. An
optional use case owns reusable application logic. A repository exposes
application data. Only the Data implementation knows service declarations,
HTTP clients, wire DTOs, serializers, and transport exceptions.

```kotlin
interface ProfileRepository {
    suspend fun refreshProfile(): Profile
    fun observeProfile(): Flow<Profile>
}

class ProfileViewModel(
    private val profiles: ProfileRepository,
) : ViewModel() {
    fun refresh() {
        viewModelScope.launch {
            profiles.refreshProfile()
        }
    }
}
```

`ProfileRepository` exposes no Retrofit `Response`, OkHttp `Request`, DTO, URL,
or Android connectivity type. The implementation can replace its network
library without rewriting presentation contracts.

## 2. HTTP request anatomy

An HTTP request has a method and target URI. The URI contains scheme,
authority, path, and optional query. Headers carry metadata such as accepted
representation, authorization, validators, and request identity. A body carries
a representation when the method and API contract allow it.

```kotlin
val request = Request.Builder()
    .url(
        HttpUrl.Builder()
            .scheme("https")
            .host("api.example.test")
            .addPathSegments("v1/profiles/p-42")
            .addQueryParameter("include", "settings")
            .build(),
    )
    .header("Accept", "application/json")
    .get()
    .build()
```

Path identifies a resource within the API contract. Query usually modifies
selection or representation. Headers are not a secret vault: intermediaries,
debuggers, and logs can expose them. Bodies must match declared media type and
schema.

## 3. HTTP response anatomy

A response contains a status code, headers, and optional content. Headers may
describe content type, freshness, validators, rate limits, tracing, or retry
advice. Some successful responses intentionally have no body. Redirects may be
followed by the client according to method, security, and configuration.

```kotlin
data class TransportResponse<T>(
    val status: Int,
    val headers: Map<String, String>,
    val body: T?,
)

fun <T : Any> TransportResponse<T>.requireBody(): T =
    body ?: throw MalformedRemoteData("Expected response body for $status")
```

Do not assume `2xx` implies a valid deserialized body. A `204 No Content`,
contract violation, empty stream, or malformed representation needs deliberate
handling.

## 4. Methods, safety, and idempotency

HTTP semantics define GET as safe and idempotent. PUT and DELETE are
idempotent by method semantics, though their responses and server effects can
still vary. POST and PATCH are not inherently idempotent. An API can make a
particular operation safely repeatable through an idempotency key, conditional
request, or operation identifier.

```kotlin
@Serializable
data class CreatePaymentDto(
    val cartId: String,
)

interface PaymentService {
    @POST("v1/payments")
    suspend fun createPayment(
        @Header("Idempotency-Key") operationId: String,
        @Body request: CreatePaymentDto,
    ): PaymentDto
}
```

Idempotent does not mean “cannot fail” or “returns the same bytes.” It means
repeating the same intended request has the same intended effect as performing
it once. Retry still depends on whether the request reached the server and on
the API's explicit contract.

## 5. Status codes need API context

- `2xx`: the request was successfully received and handled according to the
  specific status and endpoint contract.
- `3xx`: redirection or conditional-request outcome; automatic following is
  not always equivalent to application success.
- `4xx`: the request cannot be fulfilled as sent or under current client
  context. Authentication, authorization, conflicts, rate limits, and
  validation are different cases.
- `5xx`: the server failed to fulfill an apparently valid request; retry is
  still conditional, bounded, and operation-aware.

```kotlin
sealed interface HttpDisposition {
    data object Success : HttpDisposition
    data object NotModified : HttpDisposition
    data class ClientFailure(val code: Int) : HttpDisposition
    data class ServerFailure(val code: Int) : HttpDisposition
    data class Unexpected(val code: Int) : HttpDisposition
}

fun classifyStatus(code: Int): HttpDisposition = when {
    code in 200..299 -> HttpDisposition.Success
    code == 304 -> HttpDisposition.NotModified
    code in 400..499 -> HttpDisposition.ClientFailure(code)
    code in 500..599 -> HttpDisposition.ServerFailure(code)
    else -> HttpDisposition.Unexpected(code)
}
```

The endpoint contract gives `404`, `409`, `422`, or `429` application meaning.
Do not turn every `4xx` into “bad request” or every `5xx` into an automatic
retry.

## 6. Service interfaces describe transport endpoints

A declarative interface binds methods, path/query/header/body parameters, and
wire return types. Suspend integration makes the call part of caller-owned
coroutine work. Raw `Response<T>` can be useful for status and headers, but it
must remain inside the remote source.

```kotlin
interface ProfileService {
    @GET("v1/profiles/{id}")
    suspend fun getProfile(
        @Path("id") id: String,
        @Query("include") include: String? = null,
    ): Response<ProfileDto>

    @PUT("v1/profiles/{id}")
    suspend fun replaceProfile(
        @Path("id") id: String,
        @Body body: UpdateProfileDto,
    ): Response<ProfileDto>
}
```

This is Retrofit-style syntax. Retrofit 2 and 3, converter versions, and other
clients differ in supported return types and coroutine behavior. Verify the
installed version and converter contract rather than treating this declaration
as a universal API.

## 7. HTTP client responsibilities

The HTTP client manages calls, connections, pooling, protocol negotiation,
redirect policy, TLS, timeouts, interceptors, authentication challenges, and
optionally an HTTP cache. Reuse a deliberately configured client instead of
building one per request.

```kotlin
val httpClient = OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(20, TimeUnit.SECONDS)
    .writeTimeout(30, TimeUnit.SECONDS)
    .callTimeout(45, TimeUnit.SECONDS)
    .followRedirects(true)
    .build()
```

This shows OkHttp 5-style configuration. Defaults and APIs are
version-sensitive. A derived client may share pools while changing an
endpoint-specific timeout. Client construction belongs to the application's
Data/DI composition, not to a repository method or ViewModel.

## 8. DTOs represent the wire

A DTO mirrors data the server can send, including wire names, optional fields,
version drift, and nullable values. It does not automatically satisfy
application invariants or UI wording.

```kotlin
@Serializable
data class ProfileDto(
    @SerialName("id") val id: String,
    @SerialName("display_name") val displayName: String? = null,
    @SerialName("created_at") val createdAt: String,
    @SerialName("account_state") val accountState: String? = null,
)

data class Profile(
    val id: ProfileId,
    val displayName: String,
    val createdAt: Instant,
    val state: AccountState,
)
```

Keeping the models separate prevents a new nullable server field or wire enum
from invalidating every screen. Small applications may sometimes reuse a model
when meanings truly coincide, but that is a reviewed decision, not a default.

## 9. Serialization is a failure boundary

JSON configuration decides how unknown fields, defaults, explicit nulls, and
coercion behave. Missing required fields and malformed JSON should fail rather
than create an invalid domain object. Dates need a specified format and zone.
Unknown enum values need a forward-compatibility policy. Decimal quantities may
need strings, integers in minor units, or arbitrary precision rather than
binary floating point.

```kotlin
val wireJson = Json {
    ignoreUnknownKeys = true
    explicitNulls = false
    isLenient = false
}

fun decodeProfile(payload: String): ProfileDto =
    wireJson.decodeFromString(payload)
```

These are kotlinx.serialization settings; their defaults and experimental
markers can change by installed version. `ignoreUnknownKeys` aids additive
evolution but can also hide misspelled fields, so contract tests remain useful.

## 10. Mapping protects domain invariants

Mapping belongs at the Data boundary. Validate identifiers, parse time
deliberately, normalize only where the domain allows, and reject data that
cannot form a valid application model. Defaults must express real product
meaning, not merely silence nullability.

```kotlin
fun ProfileDto.toDomain(): Profile {
    val stableId = id.takeIf(String::isNotBlank)
        ?: throw MalformedRemoteData("Blank profile id")
    val name = displayName?.trim()?.takeIf(String::isNotEmpty)
        ?: throw MalformedRemoteData("Missing display name")
    val parsedState = when (accountState) {
        "active" -> AccountState.Active
        "suspended" -> AccountState.Suspended
        null, "unknown" -> AccountState.Unknown
        else -> AccountState.Unknown
    }

    return Profile(
        id = ProfileId(stableId),
        displayName = name,
        createdAt = Instant.parse(createdAt),
        state = parsedState,
    )
}
```

Mapping tests should pin these choices. A default would be valid only if the
product contract gave it real meaning; it must not merely hide missing data.

## 11. Remote source and repository form two boundaries

The remote source confines service calls, raw responses, DTOs, and protocol
interpretation. The repository coordinates remote and local sources, owns
freshness and source-of-truth policy, and exposes application models.

```kotlin
class ProfileRemoteDataSource(
    private val service: ProfileService,
) {
    suspend fun fetch(id: String): ProfileDto {
        val response = service.getProfile(id)
        if (!response.isSuccessful) {
            throw HttpStatusFailure(response.code())
        }
        return response.body()
            ?: throw MalformedRemoteData("Profile body missing")
    }
}

class OfflineFirstProfileRepository(
    private val remote: ProfileRemoteDataSource,
    private val local: ProfileLocalDataSource,
) : ProfileRepository {
    override fun observeProfile(): Flow<Profile> =
        local.observe().map(ProfileEntity::toDomain)

    override suspend fun refreshProfile(): Profile {
        val profile = remote.fetch(local.profileId()).toDomain()
        local.replace(profile.toEntity())
        return profile
    }
}
```

The UI observes one repository path. It does not race network DTOs against
database entities or decide which source won.

## 12. Name failure categories before mapping them

Connection refusal, unavailable route, DNS lookup failure, timeout, TLS
validation failure, owner cancellation, non-success HTTP status, malformed
representation, declared API business error, and domain validation failure are
not interchangeable.

```kotlin
sealed interface RemoteFailure {
    data object Dns : RemoteFailure
    data object Connection : RemoteFailure
    data object Timeout : RemoteFailure
    data object Tls : RemoteFailure
    data class Http(val code: Int, val errorCode: String?) : RemoteFailure
    data class Malformed(val detail: String) : RemoteFailure
}

sealed interface ProfileFailure {
    data object TemporarilyUnavailable : ProfileFailure
    data object NotFound : ProfileFailure
    data object AccessDenied : ProfileFailure
    data class InvalidData(val detail: String) : ProfileFailure
}
```

Cancellation is absent because it normally propagates control flow rather than
becoming a user-facing failure. An API error code inside a valid `4xx` body may
map differently from a transport exception.

## 13. Error mapping is boundary-specific

Upper layers need stable application-facing failures, not `IOException`,
`HttpException`, `SerializationException`, or raw error bodies. One project
might use sealed failures, domain exceptions, or an operation-specific result.
There is no universal `Result<T>` wrapper.

```kotlin
suspend fun <T> translateRemoteFailure(
    block: suspend () -> T,
): T = try {
    block()
} catch (cancelled: CancellationException) {
    throw cancelled
} catch (failure: UnknownHostException) {
    throw ProfileUnavailable(cause = failure)
} catch (failure: SocketTimeoutException) {
    throw ProfileUnavailable(cause = failure)
} catch (failure: SSLException) {
    throw SecureConnectionFailed(cause = failure)
} catch (failure: SerializationException) {
    throw InvalidRemoteProfile(cause = failure)
}
```

Only expected infrastructure failures are translated. Programming defects and
unclassified exceptions remain observable. Ordinary `runCatching` around
suspend work is unsafe because it catches `CancellationException`.

## 14. Cancellation belongs to the caller's lifetime

A suspend network call should be cancelled when its owning ViewModel, request,
worker, or structured parent ends. A cancellation-capable client adapter should
cancel the underlying call. Mapping code must rethrow cancellation, and long
streaming loops must check it cooperatively.

```kotlin
suspend fun ProfileRemoteDataSource.fetchVisibleProfile(
    id: String,
): ProfileDto = try {
    fetch(id)
} catch (cancelled: CancellationException) {
    throw cancelled
} catch (failure: HttpStatusFailure) {
    if (failure.code == 404) throw ProfileDoesNotExist(id)
    throw failure
}
```

Do not show “request cancelled” as an error by default. Cancellation can be a
normal consequence of leaving a screen or replacing a search query.

## 15. Timeouts define waiting budgets

Connect timeout bounds connection establishment. Read timeout bounds inactivity
while reading. Write timeout bounds inactivity while writing. A call timeout
can bound the complete call, including redirects and retries performed by the
client. Exact semantics are library-specific.

```kotlin
val baseClient = OkHttpClient.Builder()
    .connectTimeout(8, TimeUnit.SECONDS)
    .readTimeout(20, TimeUnit.SECONDS)
    .writeTimeout(20, TimeUnit.SECONDS)
    .callTimeout(35, TimeUnit.SECONDS)
    .build()

val largeUploadClient = baseClient.newBuilder()
    .writeTimeout(2, TimeUnit.MINUTES)
    .callTimeout(3, TimeUnit.MINUTES)
    .build()
```

Different endpoints may need different budgets. A coroutine `withTimeout` can
bound a larger application operation, but layering multiple timeouts requires
clear diagnostics. “No timeout” risks indefinite ownership and resource use.

## 16. Retry is a bounded application policy

Retry only failures classified as transient and operations known to be
repeatable. Bound attempts and total elapsed time, use backoff with jitter, and
keep ownership with the caller or repository operation. Respect server advice
such as `Retry-After` only after validating and capping it.

```kotlin
suspend fun <T> retryTransient(
    maxAttempts: Int,
    canRepeat: Boolean,
    delayMillisForAttempt: (Int) -> Long,
    block: suspend () -> T,
): T {
    require(maxAttempts >= 1)
    var lastFailure: IOException? = null

    repeat(maxAttempts) { index ->
        try {
            return block()
        } catch (failure: IOException) {
            lastFailure = failure
            val hasNext = index + 1 < maxAttempts
            if (!canRepeat || !hasNext || !failure.isTransient()) throw failure
            delay(delayMillisForAttempt(index + 1))
        }
    }
    throw checkNotNull(lastFailure)
}

private fun IOException.isTransient(): Boolean =
    this is SocketTimeoutException ||
        this is ConnectException ||
        this is UnknownHostException
```

This catches `IOException`, not every throwable, so coroutine cancellation
propagates. A production delay policy adds capped exponential backoff and
jitter. For ambiguous POST success, use an idempotency key or reconciliation
endpoint rather than blindly repeating a side effect.

## 17. Interceptors handle cross-cutting transport concerns

An interceptor can add stable headers, trace IDs, locale, or client version;
observe timings; or apply carefully scoped transport policy. Ordering matters:
logging before redaction or authentication can leak secrets. Business rules,
database coordination, UI messages, and arbitrary retry loops do not belong
there.

```kotlin
class CommonHeadersInterceptor(
    private val requestIds: () -> String,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .header("Accept", "application/json")
            .header("X-Request-Id", requestIds())
            .build()
        return chain.proceed(request)
    }
}
```

OkHttp distinguishes application and network interceptors and constrains how
often a network interceptor proceeds. Verify the installed OkHttp version
before relying on exact chain behavior.

## 18. Authentication attachment and challenges differ

A request interceptor can attach the current access token. An authenticator
responds to an authentication challenge such as `401` and either constructs a
new request or gives up. Refresh is not ordinary business logic and must avoid
re-entering the same authenticator.

```kotlin
class AccessTokenInterceptor(
    private val tokens: TokenSnapshotProvider,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokens.currentAccessToken()
        val request = if (token == null) {
            chain.request()
        } else {
            chain.request().newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        }
        return chain.proceed(request)
    }
}
```

The snapshot read must match the interceptor's synchronous execution contract.
Do not perform an unbounded database query or token refresh in every request.
Never log the header.

## 19. Concurrent token refresh needs single-flight coordination

Several calls can receive `401` together. They should normally share one
refresh attempt, then retry with the new token. Compare the failed token after
acquiring the lock: another caller may already have refreshed it.

```kotlin
class TokenRefreshCoordinator(
    private val mutex: Mutex,
    private val store: TokenStore,
    private val refreshService: RefreshService,
) {
    suspend fun refreshAfter(failedToken: String): String? =
        mutex.withLock {
            val current = store.accessToken()
            if (current != null && current != failedToken) return@withLock current

            val refreshed = refreshService.refresh(store.refreshToken())
                ?: return@withLock null
            store.replace(refreshed)
            refreshed.accessToken
        }
}
```

This is a suspend coordination sketch, not a universal OkHttp `Authenticator`
implementation: OkHttp's authenticator API is synchronous and version-specific.
An adapter must respect client threading, limit response-chain attempts, and
use a refresh path that cannot invoke the same authenticator. Refresh failure
crosses an explicit session/logout boundary; it must not recurse forever.

## 20. TLS validates the server, not application authorization

HTTPS uses TLS to protect traffic in transit and authenticate the server
identity through a certificate chain, trusted roots, and hostname verification.
Do not install a trust manager or hostname verifier that accepts everything.
Use Android Network Security Configuration for explicit cleartext, trust-anchor,
debug-CA, and domain policies.

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
</network-security-config>
```

Android guidance cautions that certificate pinning is not recommended as a
default because server/CA rotation can strand installed clients. A justified
pinning design needs backup pins, rotation and expiry policy, release-response
capacity, monitoring, and threat-model review. TLS does not authorize a user
or validate a server's business response.

## 21. HTTP cache and repository cache solve different problems

An HTTP cache follows `Cache-Control`, freshness, validators, and request
semantics. `ETag` and `Last-Modified` support conditional requests; a `304`
means reuse a stored representation, not “empty success.” A database cache
provides application-owned persistence, queries, offline behavior, and
observable source-of-truth semantics.

```kotlin
interface ConditionalProfileService {
    @GET("v1/profiles/{id}")
    suspend fun getProfile(
        @Path("id") id: String,
        @Header("If-None-Match") etag: String?,
    ): Response<ProfileDto>
}

class ConditionalProfileRemoteDataSource(
    private val service: ConditionalProfileService,
) {
    suspend fun refreshCached(cached: CachedProfile): RemoteProfile =
        service.getProfile(cached.id, cached.etag).let { response ->
            when {
                response.code() == 304 -> RemoteProfile.Unchanged
                response.isSuccessful -> RemoteProfile.Changed(
                    dto = requireNotNull(response.body()),
                    etag = response.headers()["ETag"],
                )
                else -> throw HttpStatusFailure(response.code())
            }
        }
    }
```

Caching private authenticated responses needs explicit server directives and
data-handling review. Do not confuse “cached bytes” with an authoritative
offline data model.

## 22. Connectivity is a signal, not proof of success

An Android network callback can report that a network is available and
validated at the platform level. The target endpoint can still fail because of
DNS, captive portals, routing, TLS, server health, authorization, or timeout.
Do not gate every call on a prior connectivity Boolean; attempt owned work and
handle its result.

```kotlin
class ConnectivityDataSource(
    private val connectivity: ConnectivityManager,
) {
    fun isCurrentlyValidated(): Boolean {
        val network = connectivity.activeNetwork ?: return false
        val capabilities = connectivity.getNetworkCapabilities(network)
            ?: return false
        return capabilities.hasCapability(
            NetworkCapabilities.NET_CAPABILITY_VALIDATED,
        )
    }
}
```

This Android-specific signal stays in Data/UI infrastructure. It can improve
messaging or scheduling but is not the repository's source of truth. An
offline-first repository serves durable local data and coordinates refresh,
freshness, conflicts, and failures independently of a momentary signal.

## 23. Pagination is a stateful data protocol

Offset/page pagination needs stable ordering and duplicate handling when data
changes. Cursor/token pagination follows server-provided continuation state.
Both need refresh semantics, end detection, cancellation, deduplication, and a
policy for an expired cursor.

```kotlin
@Serializable
data class FeedPageDto(
    val items: List<FeedItemDto>,
    val nextCursor: String? = null,
)

data class Page<Key, Item>(
    val items: List<Item>,
    val nextKey: Key?,
    val endReached: Boolean,
)

fun FeedPageDto.toDomainPage(): Page<String, FeedItem> {
    val unique = items.distinctBy(FeedItemDto::id).map(FeedItemDto::toDomain)
    return Page(
        items = unique,
        nextKey = nextCursor,
        endReached = nextCursor == null,
    )
}
```

Android Paging is a library boundary, not a universal domain model. `PagingSource`
can load one source; `RemoteMediator` can coordinate network into a database
that UI pages as source of truth. Its APIs and experimental markers are
version-sensitive, so verify the installed Paging version.

## 24. Stream uploads and downloads

Large transfers should stream rather than materialize entire bodies in memory.
Define file ownership, temporary names, atomic completion, disk-space failure,
progress cadence, cancellation cleanup, integrity checks, and resumability
only when the server protocol supports it.

```kotlin
class FileRemoteDataSource(
    private val client: OkHttpClient,
    // This diagnostic sink must not throw.
    private val reportCleanupFailure: (Path, IOException) -> Unit,
) {
    suspend fun download(
        request: Request,
        target: Path,
        onProgress: (written: Long, total: Long?) -> Unit,
    ): Unit = withContext(Dispatchers.IO) {
        suspendCancellableCoroutine { continuation ->
            val directory = requireNotNull(target.parent) {
                "Download target must have a parent directory"
            }
            val partial = Files.createTempFile(
                directory,
                "${target.fileName}.",
                ".partial",
            )
            val call = client.newCall(request)

            continuation.invokeOnCancellation {
                // OkHttp cancellation closes the active exchange so an
                // already-blocked network read can fail and unwind.
                call.cancel()
            }

            fun deletePartial() {
                try {
                    Files.deleteIfExists(partial)
                } catch (failure: IOException) {
                    reportCleanupFailure(partial, failure)
                }
            }

            val callback = object : Callback {
                override fun onFailure(call: Call, failure: IOException) {
                    deletePartial()
                    val token = continuation.tryResumeWithException(failure)
                    if (token != null) {
                        continuation.completeResume(token)
                    }
                }

                override fun onResponse(call: Call, response: Response) {
                    var committed = false
                    try {
                        response.use { ownedResponse ->
                            if (!ownedResponse.isSuccessful) {
                                throw HttpStatusFailure(ownedResponse.code)
                            }
                            val body = ownedResponse.body
                                ?: throw MalformedRemoteData("Download body missing")
                            val total = body.contentLength()
                                .takeIf { it >= 0L }

                            body.byteStream().use { input ->
                                Files.newOutputStream(
                                    partial,
                                    StandardOpenOption.WRITE,
                                    StandardOpenOption.TRUNCATE_EXISTING,
                                ).use { output ->
                                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                                    var written = 0L
                                    while (true) {
                                        val count = input.read(buffer)
                                        if (count < 0) break
                                        output.write(buffer, 0, count)
                                        written += count
                                        onProgress(written, total)
                                    }
                                }
                            }

                            if (!continuation.isActive) {
                                throw CancellationException("Download cancelled")
                            }
                            verifyCompletedDownload(partial, total)
                            Files.move(
                                partial,
                                target,
                                StandardCopyOption.ATOMIC_MOVE,
                                StandardCopyOption.REPLACE_EXISTING,
                            )
                            committed = true
                        }

                        val token = continuation.tryResume(Unit)
                        if (token != null) {
                            continuation.completeResume(token)
                        }
                    } catch (failure: Throwable) {
                        val token = continuation.tryResumeWithException(failure)
                        if (token != null) {
                            continuation.completeResume(token)
                        }
                    } finally {
                        if (!committed) deletePartial()
                    }
                }
            }

            try {
                call.enqueue(callback)
            } catch (failure: RuntimeException) {
                deletePartial()
                val token = continuation.tryResumeWithException(failure)
                if (token != null) {
                    continuation.completeResume(token)
                }
            }
        }
    }
}
```

The remote source owns both the `Call` and the response lifetime. Coroutine
cancellation invokes `Call.cancel()`, allowing OkHttp to close the active
exchange so a currently blocked network read fails and the callback unwinds.
`response.use` closes the response and its body; the input and output streams
also close through `use`.

Every operation writes to a unique partial file in the target directory. Any
HTTP, I/O, integrity, or cancellation failure closes resources and deletes that
partial file; cleanup failure is reported for later remediation. After
validation, an atomic move is the commit point. Cancellation observed before
commit deletes the partial file. Cancellation racing with or following commit
can make the caller observe cancellation, but the target is already a complete
committed file, not a partial result. Resume requires a separately designed
server range/token and integrity protocol.

```kotlin
class ProgressRequestBody(
    private val delegate: RequestBody,
    private val onProgress: (Long, Long?) -> Unit,
) : RequestBody() {
    override fun contentType(): MediaType? = delegate.contentType()
    override fun contentLength(): Long = delegate.contentLength()

    override fun writeTo(sink: BufferedSink) {
        val total = contentLength().takeIf { it >= 0L }
        val forwarding = object : ForwardingSink(sink) {
            var written = 0L
            override fun write(source: Buffer, byteCount: Long) {
                super.write(source, byteCount)
                written += byteCount
                onProgress(written, total)
            }
        }
        val countingSink = forwarding.buffer()
        delegate.writeTo(countingSink)
        countingSink.flush()
    }
}
```

Both transfer examples are OkHttp-specific and must be adapted and tested
against the installed major version. `Call.cancel()` behavior, callback
threading, response-body ownership, and atomic-file support are part of that
version/platform audit. Throttle progress before UI presentation.

## 25. Observability, redacted logging, and layered tests

Observability should correlate work without copying secrets or personal data.
Prefer request IDs, method, approved endpoint name or coarse host, status class,
and timing. Exclude authorization, cookies, query values, bodies, and raw error
payloads unless a separately reviewed redaction policy proves they are safe.

```kotlin
data class SafeNetworkEvent(
    val requestId: String,
    val method: String,
    val host: String,
    val statusClass: Int,
    val elapsedMillis: Long,
)

class RedactedMetadataInterceptor(
    private val logger: (SafeNetworkEvent) -> Unit,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val requestId = UUID.randomUUID().toString()
        val request = chain.request().newBuilder()
            .header("X-Request-Id", requestId)
            .build()
        val started = System.nanoTime()
        val response = chain.proceed(request)
        logger(
            SafeNetworkEvent(
                requestId = requestId,
                method = request.method,
                host = request.url.host,
                statusClass = response.code / 100,
                elapsedMillis = (System.nanoTime() - started) / 1_000_000,
            ),
        )
        return response
    }
}
```

Production logging should define sampling and failure-path behavior too. The
example intentionally records no path, query, headers, or body because those
may contain identifiers or credentials.

Mapper tests are pure. Repository tests use fake sources. A mock web server
tests real encoding, headers, status, parsing, timeout, and malformed payload
without calling production. Cancellation tests prove underlying work stops.

```kotlin
@Test
fun refresh_mapsAndPersistsApplicationModel() = runTest {
    val remote = FakeProfileRemote(ProfileDto("p-1", "Ada", VALID_TIME, "active"))
    val local = FakeProfileLocal("p-1")
    val repository = OfflineFirstProfileRepository(remote, local)

    val result = repository.refreshProfile()

    assertEquals(ProfileId("p-1"), result.id)
    assertEquals(result, local.saved.single())
}
```

```kotlin
@Test
fun service_sendsPathAndParsesBody() = runTest {
    server.enqueue(MockResponse(body = """{"id":"p-1","created_at":"$VALID_TIME"}"""))

    val dto = retrofitService(server.url("/")).getProfile("p-1").body()

    assertEquals("/v1/profiles/p-1", server.takeRequest().url.encodedPath)
    assertEquals("p-1", dto?.id)
}
```

```kotlin
@Test
fun malformedRequiredField_failsSerialization() {
    assertFailsWith<SerializationException> {
        wireJson.decodeFromString<ProfileDto>("""{"display_name":"Ada"}""")
    }
}
```

```kotlin
@Test
fun cancellingOwner_cancelsRemoteWork() = runTest {
    val service = SuspendingProfileService()
    val job = launch { service.getProfile("p-1") }
    service.started.await()

    job.cancelAndJoin()

    assertTrue(service.cancelled)
}

private class SuspendingProfileService {
    val started = CompletableDeferred<Unit>()
    var cancelled = false

    suspend fun getProfile(id: String): ProfileDto {
        started.complete(Unit)
        try {
            awaitCancellation()
        } finally {
            cancelled = true
        }
    }
}
```

Also test bounded retry counts, `Retry-After` caps, concurrent `401` single
flight, refresh failure, logging redaction, conditional `304`, pagination
duplicates/end, disk failure, and partial-file cleanup. Real-server integration
tests complement rather than replace deterministic local tests.

## 26. Anti-patterns and decision guide

Avoid:

- Retrofit service, DTO, raw `Response`, `Call`, `Request`, or URL in ViewModel;
- network DTO reused as mutable UI state;
- treating `2xx` as proof of a valid body;
- treating all `4xx` as one domain error;
- ordinary `runCatching` around suspend networking;
- retrying every exception or hiding an infinite retry in an interceptor;
- repeating ambiguous writes without idempotency or reconciliation;
- one authenticator refresh per concurrent `401`, or recursive refresh;
- disabling certificate or hostname validation;
- certificate pinning without backup/rotation/recovery policy;
- tokens, bodies, cookies, or personal data in logs;
- connectivity status used as proof an endpoint will work;
- HTTP cache mistaken for an offline source of truth;
- hardcoded base URLs spread through features;
- a new HTTP client per request or no deliberate timeout;
- a giant interceptor containing repository or business logic;
- paging without stable keys, deduplication, refresh, or end detection;
- whole files loaded into memory or partial files treated as complete;
- large response objects passed through navigation.

Before implementing a network operation, answer:

1. What are the endpoint's method, schema, status, idempotency, and error
   contracts?
2. Which Data component owns client APIs, DTOs, parsing, and mapping?
3. What stable repository data or failure reaches the caller?
4. Who owns cancellation, timeout, and any bounded retry?
5. Can a repeated request duplicate a side effect, and how is ambiguity
   reconciled?
6. How do authentication, concurrent refresh, and logout terminate?
7. What are the TLS, trust, redaction, and sensitive-data policies?
8. Which cache is authoritative, how is freshness validated, and what works
   offline?
9. How do pagination or transfer state survive cancellation and partial
   completion?
10. Which pure, fake-source, mock-server, and integration tests prove the
    contract, and which APIs must be checked against installed versions?
