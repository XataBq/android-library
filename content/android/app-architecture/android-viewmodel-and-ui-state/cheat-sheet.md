# Android ViewModel and UI State — Cheat sheet

## Purpose

ViewModel is a scoped screen-level state holder and UI-scenario coordinator. It
exposes state, handles actions, calls repositories/use cases, and maps outcomes
to UI decisions.

It is not a Repository, singleton, event bus, process database, NavController
owner, or container for unrelated features.

## Scope selection

| Owner | Use when |
|---|---|
| destination/screen | one screen owns the state |
| navigation graph | one workflow deliberately shares state |
| Activity | several screens genuinely share Activity-lifetime state |
| plain state holder | reusable UI needs hoistable local complexity |

Use the narrowest owner matching the scenario.

## Lifetime

- Configuration change: same ViewModelStore retains the ViewModel.
- Owner permanently removed: ViewModel cleared; `viewModelScope` cancelled.
- Process death: ViewModel and memory disappear.
- Saved state: small recovery inputs, not authoritative application data.

## UI state checklist

- immutable public contract;
- private mutation;
- truthful initial value;
- coherent snapshot for related values;
- independent flows only for independent data;
- initial load, refresh, submit, and partial failure modeled separately;
- expected outcomes survive recreation when necessary.

## Flow choices

- `StateFlow`: current hot state.
- `SharedFlow`: configurable hot broadcast.
- `Channel`: element handoff to receivers.
- cold `Flow`: upstream runs per collector.
- `stateIn`: share a Flow as StateFlow in a scope.
- `WhileSubscribed`: control upstream from subscriber presence.

Specify replay, loss, multiple collectors, no collector, and failure behavior.

## Safe updates

```kotlin
_uiState.update { it.copy(refreshing = true) }
```

Atomic transformation prevents lost read-modify-write updates. Define
latest-wins, parallel, or serialized request policy separately.

## Coroutine and collection rules

- ViewModel work uses `viewModelScope`.
- No `GlobalScope` or hidden unmanaged scope.
- UI collects with `collectAsStateWithLifecycle` or `repeatOnLifecycle`.
- ViewModel does not own LifecycleOwner.
- Share expensive cold upstream work once when needed.

## SavedStateHandle

Good candidates:

- route ID;
- query;
- filter;
- small in-progress selection.

Wrong candidates:

- bitmap;
- large list;
- cache;
- database snapshot;
- authoritative record.

Restore the input, then reload from repositories.

## Boundary rules

- UI owns lifecycle, rendering, and navigation execution.
- ViewModel owns screen state and scenario coordination.
- optional Domain owns reusable application operations.
- Repository owns data and source policy.
- ViewModel does not retain Activity, Fragment, View, Context, Resources,
  Application, NavController, or Compose runtime objects.

## Testing checklist

- initial state;
- success and expected error;
- refresh versus retained content;
- retry;
- cancellation and latest-wins;
- atomic concurrent updates;
- one shared upstream;
- restored SavedStateHandle input;
- active collector for `WhileSubscribed`.

## Common smells

- public mutable flow;
- unrelated streams with hidden invariants;
- duplicate cold collectors;
- one global loading flag;
- durable outcome emitted only as a transient event;
- Activity-scoped event bus;
- large saved state;
- direct DAO or Retrofit ownership;
- navigation controller in ViewModel.
