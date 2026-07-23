# Android Data Layer, Repositories, and Synchronization

This topic continues [Android App Architecture Foundations](../android-app-architecture-foundations/theory.md) and [Android UI Layer and Unidirectional Data Flow](../android-ui-layer-and-unidirectional-data-flow/theory.md). Those topics established dependency direction and state-driven UI. Here the focus moves behind that boundary: who owns application data, how sources are coordinated, and what “current” means when local and remote state can disagree.

## Learning outcomes

After completing this topic, you should be able to separate repository and data-source responsibilities, identify a Single Source of Truth (SSOT), trace read and write paths, compare freshness strategies, redesign broken synchronization, and justify model and repository boundaries.

## 1. Why the Data layer exists

Application data may arrive from a service, database, file, sensor, platform service, or memory. Each source has different availability, latency, failure modes, and representations. If every screen chooses among those sources, the application gains several competing policies for the same data.

The Data layer gives application data an owner. It:

- exposes application-oriented data and operations;
- centralizes rules for reading and changing that data;
- coordinates sources when more than one exists;
- translates source failures and representations at an explicit boundary;
- shields consumers from transport and persistence details.

The conceptual read path is:

```text
UI / Domain
     ↓
Repository
     ↓
Coordinate sources
 ↙             ↘
Local        Remote
     ↓
Application data
```

This is a responsibility flow, not a mandatory class diagram. A small repository may talk to one source directly. A larger repository may coordinate several sources or other repositories. What matters is that callers use an application boundary rather than reproduce source policy.

## 2. Repository responsibilities

A repository represents a coherent area of application data, such as users, articles, or payments. Its public operations should express what callers need rather than which technology performs the work:

```kotlin
interface UserRepository {
    fun observeUser(id: String): Flow<User?>

    suspend fun refreshUser(id: String)

    suspend fun updateUserName(
        id: String,
        name: String
    )
}
```

This interface separates three intentions:

- observe the application’s current view of a user;
- request fresher data;
- perform an application change.

The repository decides where those operations read or write. Its responsibilities commonly include exposing data, centralizing mutations, choosing a source-of-truth and freshness policy, reconciling sources, and mapping source models to application models.

A repository is not valuable merely because its class name ends in `Repository`. A one-line delegation can be reasonable when it establishes a stable boundary, but adding an interface and method for every source call without owning any policy can become ceremony. The boundary earns its place through application meaning, replaceable source details, shared policy, or expected evolution.

## 3. Data sources

A data source communicates with one concrete system for one kind of data. Examples include:

- a REST service;
- a local database;
- preferences or typed key-value storage;
- a file system;
- a device sensor;
- an Android platform service.

Its vocabulary is close to that system: request and response models, database entities, file records, or sensor readings. It knows how to perform operations against that source and how that source fails.

A data source should not decide application-wide coordination policy. A network source should not silently fall back to a database, and a database source should not decide when remote data is fresh. Otherwise a class presented as “one source” becomes a hidden repository whose behavior other owners cannot see or test independently.

## 4. Repository vs Data source

| Question | Repository | Data source |
|---|---|---|
| What does it represent? | Application data area | One concrete system |
| Who calls it? | UI state holder or optional Domain layer | Repository |
| Which vocabulary should dominate? | Application operations and models | Source operations and models |
| Does it coordinate sources? | Yes, when the requirement needs it | No |
| Does it own freshness or conflict policy? | Usually | Only source-specific mechanics |
| Can it be thin? | Yes, if the boundary is still useful | Yes |

Suppose `UserRemoteDataSource.getUserResponse(id)` and `UserLocalDataSource.observeEntity(id)` exist. The repository decides whether to expose local observation, when to fetch remotely, how to persist a response, and which error matters to the caller. Neither source should make all four decisions.

Other layers normally should not depend directly on data sources. Direct access lets one screen bypass the repository’s source-of-truth or synchronization policy while another follows it.

## 5. Data ownership

Ownership answers four questions:

1. Who is allowed to change a piece of data?
2. Where is its authoritative state held?
3. Who resolves disagreement between sources?
4. Which boundary exposes it to the rest of the app?

The UI owns rendering state, not the stored user record. A remote service may own the final business truth for an account, while a repository owns the application’s synchronization policy and a database owns the locally observable copy. These statements can coexist because “owner” is qualified by responsibility.

Expose immutable values across the Data boundary so consumers cannot mutate the repository’s state behind its back. Immutability does not mean the data never changes; changes pass through repository operations and produce new observed values.

## 6. Single Source of Truth

SSOT means **one authoritative owner for a particular piece of application data**. It does not mean one storage system for the whole app, and it does not always mean a database.

Possible choices include:

- **Database as SSOT:** durable local observation and offline reads; synchronization must keep it useful.
- **Remote server as SSOT:** appropriate when only server-confirmed data is valid; offline availability is limited.
- **Repository-owned memory as SSOT:** useful for session-scoped or inexpensive data; process death discards it.
- **Cache that is not SSOT:** a copy may accelerate reads while another owner remains authoritative.

The critical rule is that consumers do not independently merge competing authorities. If a repository exposes local data as its application view, remote results should normally update that local source; the remote response should not also race to the UI as a second truth.

Choose SSOT per data set by asking about required lifetime, offline behavior, correctness authority, latency, sharing, and recovery after process death.

## 7. Read paths

A read path defines which source is consulted, what is returned immediately, and what happens on failure.

### Network-first

Attempt the remote source first, then optionally fall back to stored data.

- **Pros:** favors current server state and can avoid showing stale data.
- **Cons:** adds latency and makes reads depend on connectivity.
- **Failure behavior:** must say whether stored data is returned, an error replaces it, or both data and a warning are exposed.
- **Offline implications:** weak unless a fallback exists.

### Cache-first

Return a cached value when acceptable; fetch if missing or invalid, often refreshing in the background.

- **Pros:** low latency and reduced source work.
- **Cons:** correctness depends on invalidation and freshness rules.
- **Invalidation:** may use age, version, explicit mutation, or a server signal.
- **Background refresh:** improves freshness but needs error and race behavior.

### Local-first

Observe a local authoritative source and let refresh persist remote results into it.

- **Pros:** one observable path, fast local display, durable offline reads, and consistent updates.
- **Cons:** synchronization and schema evolution become explicit responsibilities.
- **Offline capability:** strong for data already stored locally.
- **Conflict risk:** local and remote writes can diverge and require resolution.

No strategy is universally best. A payment confirmation may require network-first authority; a news feed may show cached content while refreshing; an offline field tool may require local-first reads.

## 8. Write paths

Writes need a success definition. “The local object changed,” “the server accepted it,” and “all observers see it” are different milestones.

### Remote-first write

Send the change remotely, then update local state after confirmation. It simplifies authority when the server must validate the operation, but it is unavailable offline and can feel slow. If the remote succeeds and local persistence fails, the repository must reconcile that partial failure rather than report that nothing changed.

### Optimistic write

Update the visible or local value before remote confirmation. It improves responsiveness but needs a pending state and a policy for rejection. Rollback is safe only if it will not erase a newer edit; otherwise re-fetch or mark a conflict.

### Offline queued write

Persist the user’s intent locally, mark it pending, and send it later. The queue must survive the lifetime promised by the product. Retrying requires:

- classification of retryable and terminal failures;
- backoff or a suitable trigger;
- an idempotency key or operation identity when duplicates would be harmful;
- an ordering policy for dependent operations;
- a visible failed or conflicted state when automatic progress stops.

Partial failures are normal: remote accepted/local write failed, local accepted/queue write failed, or one item in a batch failed. Model the stages that matter instead of treating every write as one indivisible Boolean.

## 9. Caching

A cache is a reusable copy intended to improve latency, availability, or cost. Persistence describes whether data survives a lifetime boundary such as process death. These are independent:

- an in-memory cache is not persistent;
- a disk cache is persistent but may still be disposable;
- a database can be both persistent storage and SSOT;
- persistent data is not necessarily a cache if it is the authoritative local record.

Every cache needs a policy:

- key and scope;
- maximum lifetime or validity condition;
- invalidation after writes;
- capacity and eviction;
- behavior when stale;
- behavior when refresh fails.

“We cache it” is incomplete until the application knows when the copy can be used.

## 10. Data freshness

Freshness is a product property, not merely a timestamp. A transit arrival may become stale in seconds; a country list may remain useful for months. Define:

- what event makes data stale;
- how old it may be before a refresh is required;
- whether stale data remains usable;
- how the user learns that data may be stale;
- which operation can force refresh.

Useful signals include age, server version, invalidation notification, successful local mutation, app/session start, or user request. Connectivity alone does not prove a refresh is needed or that it will succeed.

Preserve the distinction between **available** and **fresh**. Stale-but-usable data plus a refresh warning can be better than an empty error screen, while safety-critical or financial decisions may forbid stale results.

## 11. Refresh strategies

Refresh connects freshness policy to work. Common triggers include:

- initial access when no usable data exists;
- time-based staleness;
- explicit pull-to-refresh or retry;
- a mutation that invalidates related data;
- a server notification;
- scheduled or constraint-aware background work.

Avoid refreshing solely because rendering happened. Rendering may repeat, and multiple consumers may cause duplicate work. Let a repository operation or application policy own refresh, coalesce duplicate requests if necessary, and specify whether callers wait for completion.

Refresh failure should not automatically delete usable local data. A repository can preserve data and expose refresh status separately when the product benefits from that distinction.

## 12. Offline-first architectures

An offline-first app can perform all or a critical subset of its core behavior without a reliable network. At minimum, its critical reads do not require connectivity. This is a product promise, not a label earned by having a cache.

For a local-first repository, the refresh flow is:

```text
Remote
   ↓
Persist locally
   ↓
Observe local storage
   ↓
Expose updated application data
```

The local source is the exclusive read path for higher layers. Remote data becomes visible by updating local storage. This avoids two competing streams and makes connection changes less disruptive.

Offline writes are an additional promise, not a requirement for every offline-first app. They require durable intent, pending status, retry rules, conflict handling, and user-visible failure semantics. Some operations—such as a real-time authorization—may reasonably remain online-only.

## 13. Synchronization

Synchronization reconciles states that changed independently. It is more than “call refresh” because it must define direction, scope, ordering, and completion.

- **Pull-based:** the app asks for current remote changes, often on navigation or refresh.
- **Push-signaled:** a notification says data is stale; the app then fetches the changed data.
- **Hybrid:** different data sets or circumstances use different triggers.

A synchronization design should answer:

1. What is synchronized: full snapshot, pages, or changes since a version?
2. Which source is authoritative for conflicts?
3. How is progress recorded so interruption can resume safely?
4. Can the same operation run twice without duplicate effects?
5. What triggers retry, and when does retry stop?
6. How do observers distinguish current, stale, pending, failed, and conflicted data?

Persistent background execution may implement parts of this design on Android, but a scheduling API does not define the synchronization policy.

## 14. Conflict handling

A conflict occurs when two valid histories cannot both be applied unchanged. Examples include two devices editing the same field, a local delete racing with a remote edit, or a queued action targeting an object removed elsewhere.

Strategies include:

- server authority rejects or overwrites the local change;
- client authority overwrites remote state when allowed;
- last-write-wins using trustworthy version metadata;
- field-level or operation-level merge;
- explicit user resolution;
- domain-specific rules such as additive counters or append-only events.

Last-write-wins is simple but can silently discard meaningful work, and device wall clocks may be unreliable. Prefer server versions, revision tokens, or operation identities when the infrastructure supports them.

Conflict handling belongs where the business meaning and both histories are visible. A generic network data source rarely has enough context to decide.

## 15. Error boundaries

Sources fail differently:

- **Transport failure:** unreachable service, timeout, or rejected request.
- **Persistence failure:** disk full, corruption, constraint failure, or unavailable storage.
- **Synchronization failure:** sources remain divergent after a multi-stage operation.
- **Retryable failure:** a later attempt may succeed without changing input.
- **Terminal failure:** authorization, validation, or conflict requires another action.
- **Stale-but-usable:** refresh failed, but an older value is still meaningful.

The repository can translate low-level failures into application-relevant outcomes. It should preserve distinctions callers need without leaking every HTTP or database exception.

There is no universal `Result` wrapper that solves all operations. An observed local value may be accompanied by freshness state; a write may return server validation; a queued write may expose durable pending status. Choose explicit contracts for the decision the consumer must make.

## 16. Model mapping

Source and consumer constraints can justify separate models:

```text
UserResponse → UserEntity → User → UserUiModel
```

- `UserResponse` follows a transport contract and API evolution.
- `UserEntity` follows storage keys, normalization, and nullability constraints.
- `User` expresses application meaning without source-specific fields.
- `UserUiModel` contains presentation formatting and interaction-specific values.

Mapping prevents an API rename from becoming a database migration or UI rewrite. It also allows unsafe source nullability to become an explicit application decision.

The cost is more types, mapping code, tests, and potential information loss. A small app may safely share a model across adjacent boundaries when their meanings and change rates align. Do not create four models by ritual; separate them when they protect a real boundary.

Repositories commonly map source models into application models. UI-specific formatting normally belongs at the UI boundary, because putting `displayName` or localized text in a repository couples shared data to one presentation.

## 17. Repository granularity

“One repository per table” and “one repository for the whole app” are both weak defaults. Choose boundaries around cohesive application data and policies.

A repository is probably too broad when unrelated teams or features change it for unrelated reasons, its interface becomes a catalog of the app, or every operation depends on different sources and rules. It may be too narrow when callers must coordinate several repositories to preserve one invariant or when each repository is only a technology-shaped method wrapper.

Repositories may depend on other repositories for a higher-level aggregate when that direction remains clear. Avoid cycles and unclear competing ownership.

Use the smallest number of boundaries that gives each data set a clear owner and keeps operations cohesive. Splitting later is reasonable when a second source or policy reveals a real seam.

## 18. Android examples

### Profile with local-first refresh

```kotlin
class DefaultUserRepository(
    private val local: UserLocalDataSource,
    private val remote: UserRemoteDataSource,
) : UserRepository {
    override fun observeUser(id: String): Flow<User?> =
        local.observeUser(id)

    override suspend fun refreshUser(id: String) {
        val response = remote.fetchUser(id)
        local.save(response.toEntity())
    }

    override suspend fun updateUserName(id: String, name: String) {
        remote.updateUserName(id, name)
        local.updateUserName(id, name)
    }
}
```

The code is intentionally conceptual. Observation uses the local SSOT; refresh maps and persists remote data; a confirmed remote-first write then updates local state. A production design must still define concurrent refreshes, partial failure, validation, and whether offline edits are required.

### Session-scoped device reading

A repository may own an in-memory latest reading from a sensor-backed data source. Memory can be the SSOT when loss at process death is acceptable. Adding a database solely to resemble an offline-first example would add cost without satisfying a requirement.

### Server-authoritative purchase

A purchase repository may require remote confirmation before exposing success. Cached catalog data can remain available offline while purchase submission does not. One application can legitimately use different strategies for different data.

## 19. Common mistakes

- Calling a repository a wrapper while UI still chooses local versus remote.
- Exposing Retrofit, database, or platform models as the application contract by default.
- Letting local and remote sources update UI independently.
- Treating every disk copy as the SSOT.
- Treating “cached” as a complete freshness policy.
- Deleting useful local data when refresh fails.
- Retrying validation or authorization failures indefinitely.
- Retrying non-idempotent writes without operation identity.
- Applying rollback that overwrites a newer user edit.
- Equating network availability with successful synchronization.
- Hiding partial failure behind one success Boolean.
- Putting presentation formatting and Android UI objects in repositories.
- Splitting repositories by table or endpoint without considering ownership.
- Assuming offline reads automatically imply safe offline writes.

## 20. Trade-offs

| Choice | Benefit | Cost or risk |
|---|---|---|
| Network-first read | Favors server freshness | Latency and poor offline behavior |
| Cache-first read | Fast and economical | Invalidation determines correctness |
| Local-first read | Stable observable path and offline access | Synchronization complexity |
| Remote-first write | Clear server confirmation | Weak offline support and partial local failure |
| Optimistic write | Responsive feedback | Pending, rollback, and conflict semantics |
| Offline queue | Preserves user intent | Ordering, retries, idempotency, and visibility |
| Shared boundary model | Less mapping code | Greater coupling across change rates |
| Separate boundary models | Isolation and explicit meaning | More types and mapping tests |
| Fine-grained repositories | Focused interfaces | Cross-repository coordination |
| Coarse repository | Centralized policy | Unrelated responsibilities accumulate |

Android architecture guidance is designed to scale and improve testability, but it remains guidance. Start from product correctness, ownership, lifetime, connectivity, and failure requirements. Adopt only the machinery needed to make those decisions explicit.

## 21. Summary

- The Data layer owns access to application data and the policies that keep it coherent.
- Repositories expose application operations; data sources communicate with concrete systems.
- SSOT is one authoritative owner for a particular data set, not “always use Room.”
- A read strategy must define latency, freshness, failure, and offline behavior.
- A write strategy must define when success occurs and how partial failure is repaired.
- Cache and persistence answer different questions.
- Freshness is a product policy; refresh is the work that applies it.
- Local-first reads expose local storage while remote refresh updates that storage.
- Offline writes require durable intent, retry, idempotency, and conflict semantics.
- Model boundaries protect different contracts only when their isolation justifies mapping cost.
- Repository size follows cohesive ownership and policy, not tables or endpoints.
