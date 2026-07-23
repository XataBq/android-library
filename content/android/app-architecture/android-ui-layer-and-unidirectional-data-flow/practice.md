# Android UI Layer and UDF — Practice

## Exercise 1 — Responsibility classification

### Task

Classify each responsibility as **UI element**, **state holder**, **Data layer**, or **framework interaction**:

1. Render a disabled Save button.
2. Compute whether a valid form can be saved.
3. Persist the edited profile.
4. Launch a document picker.
5. Convert profile data into `ProfileUiState`.
6. Capture `RetrySelected`.
7. Reconcile cached and remote profiles.
8. Show a permission dialog.

### Expected reasoning

Rendering and capture belong to the UI element. Screen-wide validation and state transformation fit the state holder. Persistence and reconciliation belong to Data. Picker and permission contracts are framework interactions owned by the active UI. The state holder may decide that business prerequisites are satisfied, but it should not hold the UI framework object.

### Sample answer

1 UI element; 2 state holder (or Domain if it is a reusable product rule); 3 Data; 4 framework interaction; 5 state holder; 6 UI element; 7 Data; 8 framework interaction.

## Exercise 2 — Invalid state combinations

### Task

Analyze:

```kotlin
data class ResultsUiState(
    val isLoading: Boolean,
    val items: List<Item>?,
    val isEmpty: Boolean,
    val error: String?,
)
```

List at least four contradictory or undefined combinations. Propose a safer model and explain its cost.

### Expected reasoning

The model permits loading plus fatal error, `isEmpty` plus non-empty items, null items with no loading/error, and content plus an error without saying whether content is stale. The learner should first decide which conditions may coexist.

### Sample answer

For exclusive initial states, use `Loading`, `Content(items)`, `Empty`, and `Error(message)` variants. If refresh and field-level errors can coexist with content, use a hybrid: exclusive initial load state plus content properties such as `isRefreshing`. The safer model adds variants and mapping work; it should reflect real product states rather than force every screen into a sealed hierarchy.

## Exercise 3 — Broken UDF review

### Task

```kotlin
fun render(state: FeedUiState) {
    if (state.items.isEmpty()) network.loadFeed()
    retryButton.onClick { sharedState.isLoading = true }
}

fun onNetworkResult(items: List<Item>) {
    sharedState.items = items
    sharedState.isLoading = false
}

fun onCacheResult(items: List<Item>) {
    sharedState.items = items
}
```

Identify the violations and redesign the responsibility flow.

### Expected reasoning

Rendering starts work, UI mutates shared state, concrete sources compete to update it, and related properties update separately. Re-rendering can repeat the request, while observers can see impossible intermediate values.

### Sample answer

The UI emits `RetrySelected`. A state holder transitions to loading and delegates one refresh operation to Data. Data owns cache/network policy. The resulting application data returns to the holder, which publishes one coherent `FeedUiState`; the UI only renders it.

### Reviewer guidance

Require a causal flow and one owner for source reconciliation. Merely renaming `sharedState` to `ViewModel` is insufficient.

## Exercise 4 — State versus effect

### Task

Classify: loading indicator, displayed data, validation error, snackbar, navigation, text input, selected tab, and file-picker launch. State the owner, required lifetime, and delivery/replay semantics.

### Expected reasoning

Loading, displayed data, form validation, text, and selected tab are normally state, though lifetime varies. Navigation, picker launch, and permission dialogs are framework interactions. A snackbar can be disposable feedback or a durable pending message depending on importance.

### Sample answer

Keep text and tab local unless screen coordination or restoration requires lifting them. Model validation as state so recreation can render it. Handle navigation and picker launching in the active UI and define whether they may replay. For a critical failure, keep a pending message in state until acknowledged; for noncritical feedback, accept explicitly documented best-effort delivery.

### Reviewer guidance

Accept different classifications only when the learner makes ownership, lifetime, inactivity, and replay behavior explicit.
