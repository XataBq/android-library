# Android Lifecycle and State Restoration — Practice

## Exercise 1 — Place state by responsibility

### Goal

Assign realistic screen values to owners without creating competing sources of
truth.

### Scenario

A product editor has a route ID, loaded entity, scroll position, filter text,
full-resolution bitmap, unsent form input, authentication state, and derived
UiState. It must handle rotation and possible background process termination.

### Constraints

- Classify each value under View/Compose state, ViewModel,
  `SavedStateHandle`, or Repository/persistent storage.
- A value may be read by several layers but must have one authoritative writer.
- Address size, durability, reconstructability, and owner scope.
- Do not put bitmap bytes, auth state, or loaded entities in a Bundle.
- Distinguish configuration recreation from process recreation.

### Expected deliverable

A placement table, rationale per value, and an ordered reconstruction flow for
a newly created ViewModel and UI.

### Evaluation criteria

- Route/filter inputs are separated from loaded authoritative data.
- View-owned details are not promoted without a reason.
- Durable and sensitive state has an appropriate data owner.
- Derived UiState is rebuilt rather than serialized wholesale.
- The process-recreation path explicitly creates new objects.

### Optional hints

Ask what minimum key can reload the entity and whether losing a particular UI
detail would violate the user experience.

## Exercise 2 — Repair a broken Fragment lifecycle

### Goal

Prevent stale View access and duplicate Flow collection.

### Scenario

A Fragment stores a non-null binding field forever, launches a collector in
the Fragment's `lifecycleScope` from every `onStart`, updates Views after
`onDestroyView`, and adds another observer whenever its View is recreated.

### Constraints

- Trace the Fragment and Fragment View lifetimes separately.
- Clear every View-bound reference at the correct callback.
- Use `viewLifecycleOwner`, `lifecycleScope`, and
  `repeatOnLifecycle(STARTED)` appropriately.
- Ensure only one logical collection block is installed per View instance.
- Do not move lifecycle ownership into ViewModel or Repository.

### Expected deliverable

A defect/consequence table, corrected Fragment sketch, and lifecycle timeline
covering View destruction, recreation, stop, and restart.

### Evaluation criteria

- Binding cannot be read after `onDestroyView`.
- Rendering stops with the old View and restarts for the new View.
- Repeated start/stop does not accumulate collectors.
- Fragment instance lifetime is not confused with View lifetime.
- ViewModel continues to expose state without retaining a LifecycleOwner.

### Optional hints

Count installed collectors after three stop/start cycles and after one
destroy/create View cycle.

## Exercise 3 — Design process-recreation recovery

### Goal

Restore a form screen from a small recipe and current application data.

### Scenario

A checkout form contains a route/order ID, delivery option, typed note,
server-backed cart, price quote, payment token, transient validation errors,
and an uploaded receipt image. The process can be terminated in background and
the cart may change before recreation.

### Constraints

- Specify what is saved, persisted, reloaded, recomputed, or deliberately lost.
- Construct a new ViewModel after recreation; do not claim the old one survives.
- Treat Repository/persistent storage as authoritative for cart and upload data.
- Handle missing saved state, stale IDs, reload failure, and an expired session.
- Keep secrets and large objects out of saved instance state.

### Expected deliverable

A state-ownership diagram, restoration sequence, error-state plan, and test
matrix. Include a truthful initial presentation state.

### Evaluation criteria

- Saved values are small and supported.
- Current repository data wins over a stale serialized copy.
- User input policy is explicit rather than accidental.
- Failure paths remain renderable and recoverable.
- Deliberately non-restored state is justified.

### Optional hints

Separate “needed to locate data” from “the data itself,” and decide which draft
values have durable product meaning.

## Exercise 4 — Review a `TransactionTooLargeException`

### Goal

Redesign transport and saved state under an aggregate Binder constraint.

### Scenario

A destination receives a large Parcelable product, image byte array, and
nested Bundle. The Activity also saves list contents, several
`rememberSaveable` drafts, navigation arguments, and a View hierarchy. The
crash appears only after backgrounding a deep navigation stack.

### Constraints

- Identify every likely contributor, not only the largest extra.
- Explain the roles of Bundle, Parcel, and Binder.
- Replace large payloads with exact IDs, URIs, or compact reconstruction state.
- Move data to Repository, database, file, or cache ownership as appropriate.
- Preserve required restoration behavior without relying on Parcelable or
  Serializable to bypass size limits.

### Expected deliverable

A transaction inventory, redesigned data flow, migration checklist, and tests
that exercise deep-stack save/restore behavior.

### Evaluation criteria

- The analysis treats the transaction as aggregate.
- Large data has a durable or cache owner outside the Bundle.
- Navigation and saved state carry only minimal keys.
- Parcelable and Serializable are described as encodings, not storage.
- The redesign covers missing cached data and invalid IDs.

### Optional hints

Inspect everything contributing to Activity state at the failing moment, then
trace how each large value could be reconstructed.
