# Kotlin Flow and Reactive Streams — Cheat sheet

## Mental model

```text
suspend function = one asynchronous result
cold Flow = upstream starts per collector
StateFlow = hot state holder with a current value
SharedFlow = hot broadcast stream
Channel = send/receive communication primitive
```

A Flow can emit zero, one, or many values. Collection is suspending and owns
the active pipeline.

## Cold and hot

| Contract | Starts | Late collector sees |
|---|---|---|
| cold Flow | once per collector | a new upstream execution |
| StateFlow | independently of collection | current value, then updates |
| SharedFlow | according to producer/sharing owner | replay cache, then updates |
| Channel | according to sender owner | only elements it receives |

Repeated cold collection can repeat I/O or callback registration. Share only
when repeated work is undesirable and a real scope owns the shared lifetime.

## Operator categories

- Build: `flow`, `flowOf`, `callbackFlow`, `channelFlow`.
- Transform: `map`, `filter`, `transform`, `onEach`.
- Latest-wins: `flatMapLatest`, `collectLatest`.
- Combine: `combine`, `zip`, `merge`.
- Throughput: `buffer`, `conflate`.
- Failure: `catch`, `retry`, `retryWhen`, `onCompletion`.
- Terminal: `collect`, `first`, `single`, `toList`, `count`.
- Sharing: `stateIn`, `shareIn`.

Intermediate operators describe a cold pipeline. A terminal operator starts
collection.

## Context and `flowOn`

- Flow preserves collection context.
- Do not emit from arbitrary `withContext` blocks inside `flow`.
- `flowOn(context)` affects only operators before it.
- Downstream and the collector keep the collector's context.
- `flowOn` may introduce a coroutine/buffer boundary.
- Place execution policy next to the upstream work that owns it.

## Error and completion

```kotlin
source
    .catch { failure ->
        when (failure) {
            is CancellationException -> throw failure
            is IOException -> emit(fallback)
            else -> throw failure
        }
    }
    .onCompletion { cause -> record(cause) }
```

- `catch` handles only upstream exceptions.
- It does not catch later operator or collector failures.
- Preserve cancellation; do not turn it into business failure.
- `onCompletion` observes completion but is not blanket recovery.
- Prefer domain values for expected outcomes and exceptions for broken
  execution according to the contract.

## Retry

- Retry re-collects upstream.
- Restrict by expected failure type.
- Bound attempts.
- Define backoff and owner.
- Do not retry programming errors.
- Do not hide infinite retry in a Repository.

## Throughput

| Operator | What happens when downstream is slow |
|---|---|
| none | upstream suspends |
| `buffer(n)` | upstream may run ahead by bounded capacity |
| `conflate()` | intermediate pending values may be skipped |
| `collectLatest` | previous collector block is cancelled |

Use `buffer` when every value matters, `conflate` for latest state, and
`collectLatest` when old processing becomes obsolete.

## Combine, zip, merge

- `combine`: after every source has emitted, recompute from latest values when
  any source changes.
- `zip`: pair values one-to-one.
- `merge`: interleave same-typed emissions without pairing.
- Do not combine unrelated state merely because it shares a screen.

## `flatMapLatest`

Use when a new selector makes the old inner stream obsolete:

```kotlin
queries.flatMapLatest(repository::search)
```

The previous inner collection is cancelled. Do not use it when every operation
must finish.

## Preview and experimental API status

Current kotlinx.coroutines API documentation marks `debounce` as `FlowPreview`
and `flatMapLatest` as `ExperimentalCoroutinesApi`. Use the corresponding
`@OptIn` annotations at the narrowest practical boundary, and verify the
markers against the kotlinx.coroutines version installed in the project.

## StateFlow, SharedFlow, Channel

| Type | Choose it for | Avoid |
|---|---|---|
| StateFlow | current observable state | one-off occurrences by default |
| SharedFlow | broadcast updates with explicit replay/buffer | global event bus |
| Channel | sender/receiver coordination or competing consumers | broadcast assumptions |

Expose `StateFlow`/`SharedFlow`, not their mutable implementations.

## `stateIn` and `shareIn`

```text
stateIn = share latest value + truthful initial state
shareIn = share emissions + configured replay
```

Both require:

- an owner scope;
- a start policy;
- upstream failure policy;
- a reason to share.

`SharingStarted`:

- `Eagerly`: starts immediately and keeps running;
- `Lazily`: starts on first subscriber and keeps running;
- `WhileSubscribed`: starts/stops according to subscribers.

Timeouts and replay expiration are product policy, not universal constants.

## Android lifecycle

- Compose: `collectAsStateWithLifecycle`.
- Fragment/View: `viewLifecycleOwner.repeatOnLifecycle`.
- Collect multiple flows in separate child coroutines.
- ViewModel exposes state; UI chooses the active lifecycle threshold.
- A plain UI `launch { collect }` may continue while the UI is stopped.

## Architecture placement

```text
Data       owns sources, normalization, and authoritative data
Domain     may expose focused Flow contracts
ViewModel  produces immutable presentation state
UI         collects lifecycle-aware
```

Repositories keep data ownership. ViewModel sharing scope owns presentation
state, not source data. Never expose mutable flows across boundaries.

## Testing checklist

- Is the Flow finite or infinite?
- Can `first`, `take`, or `toList` bound collection?
- Is a background collector required for a hot stream?
- Has the sharing coroutine started before emitting test input?
- Are delays driven by the test scheduler?
- Does cancellation end the collector?
- For StateFlow, can the test assert `value` instead of every conflated update?
- Are duplicate subscriptions part of the contract and tested?

## Common smells

- repeated expensive cold collection;
- hidden network work;
- swallowed cancellation;
- unbounded retry or replay;
- ownerless `shareIn`/`stateIn`;
- `flowOn` everywhere;
- `combine` for unrelated concerns;
- StateFlow used as an event queue;
- SharedFlow used as a global bus;
- Channel assumed to broadcast;
- mutable Flow exposed publicly;
- lifecycle-unaware UI collection;
- `collectLatest` used for must-complete commands.

## Interview summary

Flow is a context-preserving, cancellable asynchronous stream. Cold Flow starts
per collector. StateFlow stores current state, SharedFlow broadcasts configured
emissions, and Channel coordinates senders with receivers. Operator choice
defines cancellation, pairing, loss, and throughput semantics. Sharing and
collection are correct only when their scopes match real owners.
