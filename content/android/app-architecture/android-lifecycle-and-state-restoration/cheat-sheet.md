# Android Lifecycle and State Restoration — Cheat sheet

## Core distinction

- Lifecycle: when an owner or UI object exists and is active.
- Restoration: what a later owner can reconstruct.
- Ownership: which layer may authoritatively change the value.
- Persistence: where durable data survives process and device restarts.

No one API covers all four.

## Activity callback summary

| Callback | Practical meaning |
|---|---|
| `onCreate` | create the Activity instance and initialize UI |
| `onStart` | Activity becomes visible |
| `onResume` | Activity is ready for foreground interaction |
| `onPause` | foreground interaction is being lost |
| `onStop` | Activity is no longer visible |
| `onDestroy` | this Activity instance is destroyed, when called |

Callbacks are transitions, not business guarantees. The system can terminate a
process without calling `onDestroy`.

## Activity, Fragment, and Fragment View

| Owner | Can outlive | Bind to it |
|---|---|---|
| Activity | its current Views | Activity-wide UI resources |
| Fragment | one or more Fragment Views | Fragment-instance state |
| Fragment View | nothing View-bound after `onDestroyView` | binding, adapters, UI observers, collectors |

Use `viewLifecycleOwner` for work that reads or writes a Fragment's View. Clear
binding references in `onDestroyView`.

## Configuration change, removal, and process loss

- Configuration change: new UI instance; same logical ViewModel owner can
  retain its ViewModel.
- Destination covered but still on stack: entry and scoped ViewModel can remain.
- Destination popped: entry destroyed; scoped ViewModel cleared.
- Explicit `finish()`: Activity owner is permanently done.
- Background process termination: all memory and ViewModels disappear.
- Process recreation: new instances may receive captured small saved state.
- Force stop or task dismissal: do not assume restoration remains available.

## Ownership and state placement

| State | Prefer |
|---|---|
| animation or press state | View / `remember` |
| scroll, selection, expanded UI | View state / `rememberSaveable` when worth restoring |
| coherent in-memory screen presentation | ViewModel |
| route ID, filter, small draft input used by screen logic | `SavedStateHandle` |
| loaded entity, auth, durable draft, cache | Repository / persistent storage |
| bitmap or document | file/cache owner; transport a key or URI |

Decide by owner, scope, size, durability, and reconstructability.

## ViewModel, SavedStateHandle, and Repository

- ViewModel survives configuration recreation for the same retained owner.
- ViewModel does not survive process death.
- `SavedStateHandle` restores small supported inputs into a new ViewModel.
- Repository retains ownership of authoritative application data.
- New ViewModel + restored key + current repository data → rebuilt UiState.

Never store a Repository, service, Context, View, NavController, bitmap, or
database snapshot in `SavedStateHandle`.

## Saved instance state

- `onSaveInstanceState`: contributes a small transient snapshot.
- Saved State Registry: coordinates keyed providers and restored Bundles.
- Saved state is not a guaranteed final persistence callback.
- State written too late may not enter the captured snapshot.
- A future restoration opportunity is not guaranteed.
- All Bundle-backed mechanisms share size constraints.

## View and Compose restoration

- Stable View IDs enable hierarchy-state matching.
- Built-in Views restore supported small properties.
- Custom Views use `BaseSavedState` for View-owned UI details.
- `remember`: survives recomposition while its Composition slot remains.
- `rememberSaveable`: restores supported small UI state across eligible
  Activity/process recreation.
- `Saver`: maps a custom type to a minimal saveable representation.
- Saveable state is not durable business persistence.

## Navigation and results

- `NavBackStackEntry` owns lifecycle, ViewModel store, and saved-state registry.
- Destination scope: destination-local state.
- Graph scope: coherent workflow shared by several destinations.
- Fragment Result API: one-time Bundle-compatible result, delivered
  lifecycle-aware.
- Shared ViewModel: ongoing shared UI state with a scoped contract.
- Navigation `SavedStateHandle` result: small result for a back-stack entry;
  remove it after one-time consumption.
- Direct callback: suitable when parent-child ownership is explicit.

## Bundle, Parcel, and Binder

- `Bundle`: typed key-value container.
- `Parcel`: Android marshaling representation.
- Binder: IPC transport for transactions carrying parcels.
- Parcelable: Android-oriented parcel encoding.
- Serializable: Java object serialization.
- Neither encoding is persistence or permission to send a large graph.

## `TransactionTooLargeException` checklist

- Count the aggregate transaction, not just one extra.
- Inspect nested Bundles, arguments, hierarchy state, saved-state providers,
  `rememberSaveable`, and results together.
- Never put bitmap bytes, large lists, responses, or documents in saved state.
- Store large data in database/file/cache ownership.
- Transport compact IDs, URIs, paths, filters, and reconstruction keys.
- Leave headroom; the Binder buffer is shared by transactions in progress.

## Testing checklist

- Activity recreation with `ActivityScenario.recreate()`.
- Fragment View destruction/recreation with View-bound assertions.
- Compose restoration with `StateRestorationTester`.
- New ViewModel reconstructed from small saved inputs.
- Repository queried again for authoritative data.
- Missing, stale, invalid, and absent restored values.
- Device/harness process-death workflow when that exact claim matters.
- Never describe a simple recreation test as a full OS process-kill simulation.

## Common smells

- “ViewModel survives process death.”
- “`onDestroy` always saves.”
- binding used after `onDestroyView`;
- Fragment lifecycle used for View rendering;
- collectors duplicated after every start;
- full objects passed through navigation;
- large Parcelable or Serializable payloads;
- same source of truth copied into Bundle, ViewModel, and Repository;
- `remember` used for required restoration;
- `rememberSaveable` used as a database.

## Interview-ready summary

Lifecycle determines object availability; restoration reconstructs a later
owner. Retain screen memory in a correctly scoped ViewModel across
configuration change, save only small reconstructable UI inputs, reload
authoritative data from repositories, bind View work to the View lifecycle,
and keep Bundle-backed transport small enough for Binder boundaries.
