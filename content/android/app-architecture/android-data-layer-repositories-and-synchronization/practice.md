# Android Data Layer — Practice

## Exercise 1 — Responsibility classification

### Task

Classify each responsibility as **repository**, **data source**, **UI state holder**, or **active UI**:

1. Execute a user request against a REST service.
2. Decide whether a cached profile is fresh enough.
3. Observe a database record.
4. Combine a remote response with a pending local edit.
5. Convert application data into a localized subtitle.
6. Decide when a screen shows stale-data warning state.
7. Launch a platform document picker.
8. Translate a storage constraint failure into a data-level write outcome.

For each choice, state what information the owner needs.

### Expected reasoning

Concrete source operations belong to data sources. Cross-source policy, freshness, reconciliation, and application-relevant failure translation belong to the repository. Screen presentation decisions belong to its state holder, while the active UI performs framework interactions. Localization normally remains at the UI boundary.

### Reviewer guidance

Require reasons based on ownership and required knowledge. Accept a different boundary only if it does not make UI coordinate sources or make one data source secretly own application-wide policy.

## Exercise 2 — Repository vs wrapper

### Task

Review:

```kotlin
class ProfileRepository(
    private val api: ProfileApi
) {
    suspend fun getProfileResponse(id: String): ProfileResponse =
        api.getProfile(id)
}
```

The UI calls this class, catches transport exceptions, converts the response, decides whether to load a database fallback, and writes successful responses to that database. Explain whether the repository is currently a useful boundary and redesign the public operations without teaching specific storage or transport APIs.

### Expected reasoning

Thin delegation is not inherently wrong, but here the caller owns source selection, persistence, mapping, and failure policy. The class has not established a Data boundary. A redesigned repository can expose application models, observation, refresh, and mutation intentions while keeping coordination behind the interface.

### Reviewer guidance

Do not award full credit for merely adding more forwarding methods or renaming the API. Look for removal of source models/exceptions from UI, one owner for local/remote policy, and an explanation of when a deliberately thin repository would still be reasonable.

## Exercise 3 — Choosing the SSOT

### Task

Choose and justify an SSOT for each case:

1. A news feed should open instantly with previously downloaded stories and refresh when possible.
2. A bank transfer must not appear complete until the server confirms it.
3. A live sensor value is useful only while the current process is running.
4. A draft inspection must remain editable for days without connectivity and synchronize later.

For each, identify whether any cache exists separately from the SSOT and describe stale or unavailable behavior.

### Expected reasoning

The feed and inspection are strong candidates for durable local application views, though their write policies differ. The transfer’s authoritative completion is remote, while local pending state may still be persisted. Repository-owned memory can own a session sensor value. The answer should select authority per data set rather than one technology for the whole app.

### Reviewer guidance

Require the learner to state lifetime, correctness authority, offline promise, and reconciliation. Reject “database is always SSOT” and “server is always SSOT” without product reasoning.

## Exercise 4 — Broken synchronization

### Task

Analyze this sequence:

```text
1. UI writes a new name directly to local storage.
2. UI sends the same change to the network.
3. A background refresh writes an older remote name locally.
4. The network accepts the original change, but the response is lost.
5. Retry sends another update with no operation identity.
6. UI rolls back to the value it saw before step 1.
```

Identify race, duplication, rollback, and visibility problems. Redesign the responsibility flow for either remote-first or offline-queued writes and describe recovery after interruption.

### Expected reasoning

The UI is coordinating sources; refresh can overwrite pending intent; lost acknowledgement creates ambiguous success; blind retry can duplicate an effect; rollback can erase a newer value. A sound redesign gives the repository one operation identity and explicit pending state, defines server/version conflict policy, persists promised intent, and makes refresh respect unsynchronized work.

### Reviewer guidance

Require a chosen success definition, retry classification, idempotency or deduplication plan, conflict rule, and user-visible terminal outcome. A queue name alone is not a synchronization design.

## Exercise 5 — Model-boundary analysis

### Task

A project uses one mutable `User` class for:

- a service response whose `display_name` may be missing;
- a database row where the key and last-sync version are required;
- application rules that require a validated name;
- UI text that includes localization and a “pending” label.

Decide which boundaries need separate models. Sketch mappings and state which fields must not leak. Then describe a smaller project where sharing a model would be acceptable.

### Expected reasoning

Transport nullability and naming, persistence metadata, validated application meaning, and localized presentation change for different reasons. Separate types can isolate those constraints. Last-sync metadata should not become UI business data, and localized strings should not enter the repository model. The mapping cost must still be justified rather than applied by ritual.

### Reviewer guidance

Look for a concrete coupling analysis: API evolution, storage constraints, nullability, presentation formatting, information loss, and test cost. Do not require exactly four models if the learner gives a coherent lower-cost boundary.
