# Android ViewModel and UI State — Interview preparation

## Purpose and lifetime

### 1. What is the architectural purpose of ViewModel?

**Strong answer:** A scoped UI-layer state holder that exposes screen state,
handles UI actions, and coordinates repositories or use cases for one UI
scenario.

**Weak answer:** A class that survives rotation.

**Follow-up:** Which responsibilities remain outside it?

### 2. What does ViewModelStoreOwner control?

**Strong answer:** The identity, sharing boundary, and clearing lifetime of a
ViewModel instance.

**Weak answer:** It is only an internal factory detail.

**Follow-up:** How can choosing an Activity instead of a destination change
behavior?

### 3. How do configuration change and process death differ?

**Strong answer:** Configuration recreation retains the ViewModelStore and
in-memory ViewModel; process death destroys both and later creates a new
instance.

**Weak answer:** ViewModel automatically handles both.

**Follow-up:** How should authoritative data return after process death?

### 4. When is `onCleared()` called and what is it for?

**Strong answer:** When the owner permanently releases the ViewModel; it marks
cleanup/cancellation, not configuration change or guaranteed persistence.

**Weak answer:** On every Activity destruction.

**Follow-up:** What happens to `viewModelScope`?

### 5. How do you select Activity, destination, graph, or composable scope?

**Strong answer:** Choose the narrowest owner matching the coherent UI scenario
and intentional sharing lifetime.

**Weak answer:** Activity scope is safest because it lives longest.

**Follow-up:** What should reusable UI use?

## State and streams

### 6. What makes a good UiState contract?

**Strong answer:** Immutable, renderable, coherent, explicit about loading and
failure, and protected by one write boundary.

**Weak answer:** A list of MutableStateFlows for every field.

**Follow-up:** How do you prevent impossible combinations?

### 7. One state object or multiple flows?

**Strong answer:** One snapshot for values sharing invariants or atomic
transitions; separate streams for genuinely independent data and consumers.

**Weak answer:** One approach is always correct.

**Follow-up:** Give an invariant that requires one snapshot.

### 8. Why is StateFlow suitable for UI state?

**Strong answer:** It is hot, has a current value, and gives new collectors the
latest state.

**Weak answer:** It guarantees every intermediate event is delivered.

**Follow-up:** Why is it not a queue?

### 9. Compare SharedFlow, Channel, and cold Flow.

**Strong answer:** SharedFlow is configurable hot broadcast, Channel transfers
elements to receivers, and cold Flow runs upstream per collector.

**Weak answer:** They are interchangeable event types.

**Follow-up:** Which loss/replay questions must be specified?

### 10. Should navigation be state or an event?

**Strong answer:** It depends on whether the outcome must survive recreation
and how acknowledgement works; UI always executes navigation.

**Weak answer:** Navigation must always be a Channel event.

**Follow-up:** What happens if emission occurs without a collector?

### 11. Why use `MutableStateFlow.update`?

**Strong answer:** It performs atomic read-modify-write and avoids losing a
concurrent change.

**Weak answer:** It automatically makes every request latest-wins.

**Follow-up:** What else defines concurrency policy?

## Coroutines and lifecycle

### 12. What lifetime does viewModelScope have?

**Strong answer:** It belongs to the ViewModel and is cancelled when that
ViewModel is cleared.

**Weak answer:** Its work survives process death and navigation.

**Follow-up:** Where should durable background work live?

### 13. How can duplicate collectors cause duplicate work?

**Strong answer:** A cold Flow runs its upstream per collector; repeated
collection can duplicate queries, subscriptions, or transformations.

**Weak answer:** Flow automatically shares every upstream.

**Follow-up:** How would you share deliberately?

### 14. What does `stateIn` do?

**Strong answer:** Converts a Flow to hot StateFlow in a scope, keeps the latest
value, and shares one upstream according to a start policy.

**Weak answer:** Persists state through process death.

**Follow-up:** Where should upstream errors be handled?

### 15. How do SharingStarted strategies differ?

**Strong answer:** Eagerly starts immediately, Lazily on first subscriber and
continues, WhileSubscribed follows subscriber presence and configured timers.

**Weak answer:** `WhileSubscribed(5000)` is mandatory.

**Follow-up:** How would you choose the timeout?

### 16. Who owns lifecycle-aware collection?

**Strong answer:** Compose or View UI, using APIs such as
`collectAsStateWithLifecycle` or `repeatOnLifecycle`.

**Weak answer:** ViewModel should receive the Fragment lifecycle.

**Follow-up:** How does collection affect WhileSubscribed?

## Restoration and boundaries

### 17. What belongs in SavedStateHandle?

**Strong answer:** Small recoverable inputs such as route IDs, query text, and
filters that help reconstruct state.

**Weak answer:** Loaded entities, bitmaps, caches, and database snapshots.

**Follow-up:** What happens after task-stack removal?

### 18. Why should ViewModel not own NavController or Context?

**Strong answer:** They are UI/platform objects with different lifetimes;
retaining them couples state to a stale owner and obscures navigation/UI
responsibility.

**Weak answer:** It is forbidden only because unit tests are harder.

**Follow-up:** How can localized errors and navigation be requested instead?

### 19. When is a shared ViewModel appropriate?

**Strong answer:** For one coherent workflow intentionally shared under a graph
or Activity owner, with explicit reset and lifetime semantics.

**Weak answer:** As a global event bus between arbitrary screens.

**Follow-up:** What coupling does broad scope introduce?

### 20. How do you test a ViewModel using stateIn and latest-wins search?

**Strong answer:** Use fakes and virtual time, keep a collector active for
WhileSubscribed, change queries, verify cancellation, and assert public state.

**Weak answer:** Sleep until values appear and verify private calls.

**Follow-up:** How would you prove the upstream is collected only once?
