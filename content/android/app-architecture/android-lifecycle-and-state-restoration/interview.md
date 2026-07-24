# Android Lifecycle and State Restoration — Interview preparation

## Lifecycles and scenarios

### 1. Why are lifecycle and state restoration separate concerns?

**Strong answer:** Lifecycle controls object availability and activity;
restoration reconstructs state for a later object; ownership determines which
mechanism should hold each value.

**Weak answer:** Both mean putting everything in ViewModel.

**Follow-up:** Give one value for View, saved state, ViewModel, and Repository.

### 2. How should you reason about the Activity lifecycle callbacks?

**Strong answer:** As transitions in a state machine used to scope resources
and UI work, not as a guaranteed linear workflow or durable-save protocol.

**Weak answer:** Memorize the six callbacks and save everything in `onDestroy`.

**Follow-up:** Why can durable correctness not depend on `onDestroy`?

### 3. How do Fragment and Fragment View lifecycles differ?

**Strong answer:** A Fragment instance can remain managed or on the back stack
while its View is destroyed; each has a distinct lifecycle and owner.

**Weak answer:** The View exists whenever the Fragment exists.

**Follow-up:** Which objects must be released in `onDestroyView`?

### 4. Why use `viewLifecycleOwner`?

**Strong answer:** It limits View rendering observers and collectors to the
current Fragment View and prevents delivery into a destroyed View.

**Weak answer:** It makes ViewModel live longer.

**Follow-up:** Where should a Flow collection block be launched?

### 5. How does configuration change differ from navigation removal?

**Strong answer:** Configuration change recreates UI while the same logical
owner can retain its ViewModel; popping a destination destroys its back-stack
owner and clears scoped ViewModels.

**Weak answer:** Both always retain ViewModel.

**Follow-up:** What if the destination is covered but remains on the stack?

### 6. How does explicit `finish()` differ from process termination?

**Strong answer:** `finish()` permanently ends that Activity owner by normal
app intent; system process termination removes all memory, possibly followed
later by restoration of eligible task state.

**Weak answer:** Both guarantee `onDestroy` and saved-state restoration.

**Follow-up:** Which durable data remains in either case?

### 7. What exactly survives process death?

**Strong answer:** No process object survives. Previously captured small saved
state and persistent data may be available to newly created objects.

**Weak answer:** ViewModel, singleton, and coroutine scopes survive.

**Follow-up:** Describe the first steps of reconstruction.

## Saved state and presentation reconstruction

### 8. What is `onSaveInstanceState` for?

**Strong answer:** Contributing a small transient snapshot for eligible
framework reconstruction, not slow durable persistence or a guaranteed final
callback.

**Weak answer:** It is always called immediately before any destruction.

**Follow-up:** What values are good and bad candidates?

### 9. What does Saved State Registry add?

**Strong answer:** A keyed public mechanism for lifecycle-aware components to
provide and consume small saved Bundles; higher-level integrations build on it.

**Weak answer:** A persistent database embedded in Activity.

**Follow-up:** Which Bundle constraints still apply?

### 10. What belongs in `SavedStateHandle`?

**Strong answer:** Small supported inputs used by ViewModel logic to
reconstruct a screen, such as an ID, query, filter, or modest draft field.

**Weak answer:** Repository, bitmap, loaded graph, or database snapshot.

**Follow-up:** Who owns the loaded entity?

### 11. Does ViewModel restore itself after process death?

**Strong answer:** No. A new ViewModel can receive restored small inputs, query
repositories, and produce a new presentation state.

**Weak answer:** Android serializes and resumes the old ViewModel.

**Follow-up:** What should its initial UiState communicate?

### 12. How does View hierarchy state restoration work conceptually?

**Strong answer:** Views with stable IDs contribute supported UI-owned state;
built-in widgets handle common properties and custom Views can use
`BaseSavedState`.

**Weak answer:** Every business object referenced by a View is automatically
saved.

**Follow-up:** When should custom View state be hoisted instead?

### 13. Compare `remember` and `rememberSaveable`.

**Strong answer:** `remember` retains a value while its Composition slot
remains; `rememberSaveable` uses saved-state infrastructure for supported small
UI values across eligible recreation.

**Weak answer:** Both persist data through app reinstall.

**Follow-up:** Give a good example for each.

### 14. What is a Compose `Saver`?

**Strong answer:** A contract mapping a small custom UI value to and from a
saveable representation.

**Weak answer:** A way to store arbitrary graphs without Bundle limits.

**Follow-up:** Why prefer IDs and primitives in the saved form?

## Navigation and communication

### 15. What does a `NavBackStackEntry` own?

**Strong answer:** A destination-level lifecycle, ViewModel store, and
saved-state registry for as long as that entry remains on the stack.

**Weak answer:** Only a route string.

**Follow-up:** When is a graph-scoped ViewModel appropriate?

### 16. Compare Fragment Result API and a shared ViewModel.

**Strong answer:** Fragment Result fits a one-time Bundle-compatible result
with lifecycle-aware delivery; shared ViewModel fits ongoing shared UI state
under a deliberate owner.

**Weak answer:** Activity-scoped ViewModel is universally safest.

**Follow-up:** What happens to a pending Fragment result before `STARTED`?

### 17. How can Navigation return a result through saved state?

**Strong answer:** The producer writes a small value to the previous entry's
`SavedStateHandle`; the receiver observes its own entry and removes a consumed
one-time result.

**Weak answer:** Store NavController inside ViewModel with the full result.

**Follow-up:** Why can dialogs require identifying the exact back-stack entry?

## Transport, placement, and tests

### 18. Distinguish Bundle, Parcel, and Binder.

**Strong answer:** Bundle is a typed key-value container, Parcel is Android's
marshaling representation, and Binder transports IPC transactions carrying
parcels.

**Weak answer:** They are three names for durable storage.

**Follow-up:** Where can saved-state data meet Binder limits?

### 19. Why can several small-looking values cause `TransactionTooLargeException`?

**Strong answer:** Binder's transaction buffer is limited and shared by
transactions in progress; arguments, nested Bundles, View state, navigation,
and saveable state can contribute to the aggregate.

**Weak answer:** Only one extra larger than 1 MB can cause it.

**Follow-up:** How would you redesign image transport?

### 20. Compare Parcelable and Serializable.

**Strong answer:** They are different encodings—Android Parcel-oriented versus
Java serialization—with different tooling and costs; neither is persistence
or protection from size constraints.

**Weak answer:** Parcelable makes any object safe for navigation.

**Follow-up:** When is an ID a better transport value?

### 21. How do you choose where state belongs?

**Strong answer:** Identify the authoritative writer, narrowest scope, size,
durability need, process-survival expectation, and reconstructability.

**Weak answer:** Put every state value in SavedStateHandle.

**Follow-up:** Place scroll position, auth token, loaded profile, and filter.

### 22. How would you test restoration accurately?

**Strong answer:** Test Activity recreation, Fragment View recreation, Compose
saveable restoration, and new-ViewModel reconstruction separately, then use a
device or suitable harness for real process-death claims.

**Weak answer:** `ActivityScenario.recreate()` fully simulates an OS process
kill.

**Follow-up:** What observable evidence proves repositories reloaded data?
