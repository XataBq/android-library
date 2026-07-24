# Kotlin Flow and Reactive Streams — Practice

These exercises require a design, representative Kotlin, and tests. They do not
provide complete final solutions.

## Exercise 1 — Cold Flow duplication

### Goal

Diagnose repeated upstream work and choose an intentional cold or shared
contract.

### Scenario

A screen calls `repository.observeFeed()` in three places: one collector renders
items, one derives an unread count, and one records whether content is empty.
The repository Flow opens a database observation and performs an initial remote
refresh on every collection.

### Constraints

- Identify every repeated upstream action and its owner.
- Decide whether the repository contract should remain cold.
- Compare deriving all presentation values from one collection with `stateIn`
  or `shareIn`.
- If sharing is selected, define the exact owner scope, `SharingStarted`
  policy, replay, and failure behavior.
- Do not add a global scope or an unlimited cache.
- Preserve cancellation when the owner ends.

### Expected deliverable

- a subscription diagram before and after the change;
- a short decision record for cold versus shared behavior;
- representative public Flow types and sharing code;
- a test proving the expected number of upstream subscriptions.

### Evaluation criteria

- repeated work is identified rather than merely hidden;
- owner lifetime matches the shared resource;
- initial or replayed values are truthful;
- mutable streams are not exposed;
- the test observes subscriptions deterministically.

### Optional hints

- First ask whether three UI values form one coherent state.
- A single collected source followed by one state mapping may be simpler than
  sharing several derived streams.

## Exercise 2 — Search pipeline

### Goal

Design a latest-wins search stream whose stale work is cancelled.

### Scenario

A user types quickly. Each accepted query may read local suggestions and call a
remote search. Older results must never replace results for the latest query.

### Constraints

- Start from an owned query stream.
- Normalize whitespace and ignore equal consecutive queries.
- Choose and justify a debounce policy.
- Use `flatMapLatest` for obsolete searches.
- Verify both operators' API markers against the installed kotlinx.coroutines
  version and apply any required opt-ins at a narrow boundary.
- Model loading, content, empty, and expected failure states.
- Rethrow cancellation in any broad failure translation.
- Do not use infinite retry.
- Define what an empty query emits.

### Expected deliverable

- an operator pipeline with each operator justified;
- UI-state definitions;
- repository and ViewModel boundary signatures;
- tests for debounce, stale-search cancellation, failure, and empty input.

### Evaluation criteria

- the previous search is cancelled rather than merely ignored at rendering;
- failure handling is upstream-scoped and cancellation-safe;
- virtual time replaces real sleeps;
- state ownership remains in the ViewModel while data ownership remains in the
  repository.

### Optional hints

- A fake repository can record cancellation in `finally`.
- Advance the test scheduler only as far as the debounce contract requires.

## Exercise 3 — Combine application state

### Goal

Produce a coherent screen snapshot from several independently owned data
streams.

### Scenario

A dashboard renders the signed-in user, display settings, and connectivity
status together. A navigation request and snackbar notification also exist,
but they are occurrences rather than durable dashboard state.

### Constraints

- Combine user, settings, and connectivity sources.
- Justify `combine` instead of `zip`.
- Define a truthful initial state before every source emits.
- Decide how one failing source affects the snapshot.
- Keep repositories as owners of their data.
- Keep navigation and snackbar occurrences outside the combined state unless
  their durable outcome is modeled as state.
- Define retry ownership.

### Expected deliverable

- a state model and Flow pipeline;
- an ownership table for Data, Domain, ViewModel, and UI;
- an explanation of partial versus total failure;
- tests for source updates, initial state, and one source failure.

### Evaluation criteria

- every combined value contributes to one renderable snapshot;
- `zip` pairing semantics are not used accidentally;
- unrelated occurrences do not enter durable state;
- the ViewModel produces presentation state without taking repository data
  ownership;
- cancellation ends all owned collection.

### Optional hints

- `combine` waits until each source has emitted at least once.
- Consider whether a source should emit an explicit availability model.

## Exercise 4 — Hot stream review

### Goal

Correct a design that treats StateFlow, SharedFlow, and Channel as
interchangeable.

### Scenario

An application exposes a public `MutableStateFlow` for navigation, a
`MutableSharedFlow(replay = 1000)` as a global event bus, a Channel that several
screens expect to broadcast, and a Fragment collector launched against the
Fragment lifecycle instead of its View lifecycle. Tests use `toList()` on every
hot stream and never cancel.

### Constraints

- Classify each value as current state, durable outcome, broadcast occurrence,
  or work item.
- Select StateFlow, SharedFlow, Channel, or a persisted model for each case.
- Make mutable producers private.
- Define replay, buffer, overflow, and subscriber-timing behavior.
- Correct Fragment and Compose lifecycle collection.
- Bound every infinite test collector.
- Do not create a repository-owned ad hoc CoroutineScope.

### Expected deliverable

- a problem table and corrected contracts;
- owner and lifetime diagrams;
- lifecycle-aware collection examples;
- tests for late subscribers, competing receivers, current state, and
  cancellation.

### Evaluation criteria

- primitive selection follows delivery semantics;
- no global event bus remains;
- important outcomes survive subscriber absence through state or persistence;
- Channel is not claimed to broadcast;
- tests terminate deterministically without leaking jobs.

### Optional hints

- Ask what a late subscriber must know.
- StateFlow tests can often assert the current `value`.
