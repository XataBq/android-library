# Android ViewModel and UI State — Practice

## Exercise 1 — Design a coherent UiState

### Goal

Design a renderable screen contract instead of accumulating unrelated flags.

### Scenario

A search screen needs initial loading, content, empty results, refresh over
existing content, retry, a recoverable terminal error, query input, filter
selection, and an optional field error.

### Constraints

- Decide between one state object, sealed variants, or a justified combination.
- Separate source data from derived presentation values.
- Prevent impossible combinations.
- State which values must change atomically.
- Do not solve navigation or persistence inside the state model.

### Expected deliverable

A Kotlin state model, invariants, transition table, and justification for one
state object versus multiple independent flows.

### Evaluation criteria

- Initial, refresh, empty, content, and error scenarios are renderable.
- Related values form coherent snapshots.
- Derived values cannot silently drift.
- The public contract is immutable.

### Optional hints

Ask whether refresh failure should erase usable content and whether a field
error can coexist with a valid result list.

## Exercise 2 — Repair a broken ViewModel

### Goal

Diagnose ownership, state, event, and concurrency defects.

### Scenario

Review a ViewModel that exposes public `MutableStateFlow`s, collects the same
cold repository Flow twice, performs read-then-assign updates, uses one loading
Boolean for refresh and submit, emits navigation through an unbuffered event
when no collector may exist, and retains a `Context`.

### Constraints

- Identify consequences, not just style violations.
- Consolidate only values that share invariants.
- Define durable outcome versus transient effect behavior.
- Use atomic updates and one deliberate sharing boundary.
- Remove framework and navigation ownership.
- Do not introduce a universal event wrapper.

### Expected deliverable

A defect table, corrected ViewModel contract, action API, sharing policy, and
short Kotlin sketch.

### Evaluation criteria

- Mutable state becomes private.
- Duplicate upstream work is removed.
- concurrency and loading policies are explicit;
- event loss/replay behavior is intentional;
- UI retains lifecycle and navigation ownership.

### Optional hints

Trace what happens during rotation, with two collectors, and when refresh and
submit overlap.

## Exercise 3 — Saved state and process death

### Goal

Design a recovery flow rather than attempting to serialize the whole screen.

### Scenario

A detail screen has a route `itemId`, typed filter text, a loaded entity, a
large bitmap, a transient expanded-card set, and repository-managed favorite
state. The process may be killed after the UI moves to the background.

### Constraints

- Decide what belongs in `SavedStateHandle`.
- Decide what belongs in persistent Repository ownership.
- Identify what is recomputed or reloaded.
- Identify what may be intentionally lost.
- Account for task-stack removal.
- Do not store the bitmap or repository snapshot in saved state.

### Expected deliverable

A classification table and ordered restoration flow from new ViewModel
construction to rendered state.

### Evaluation criteria

- Small recovery inputs are separated from authoritative data.
- Process death is distinguished from configuration change.
- Restoration uses the ID/query to reload current data.
- Limitations of saved-state availability are explicit.

### Optional hints

Save enough information to reconstruct, not the reconstructed object graph.

## Exercise 4 — ViewModel contract tests

### Goal

Design coroutine-aware tests around observable behavior.

### Scenario

A results ViewModel restores a query, converts a cold repository Flow with
`stateIn(WhileSubscribed)`, cancels old searches when a query changes, supports
retry, and preserves content during refresh failure.

### Constraints

- Cover initial state, success, error, cancellation, latest-wins, repeated
  collector protection, and restored input.
- Use fakes and coroutine test control.
- Keep a collector active when testing subscriber-driven sharing.
- Assert public state and collaborator behavior, not private methods.
- Do not use sleeps or Android instrumentation.

### Expected deliverable

A test matrix, fake contracts, virtual-time plan, and representative test
sketches without complete production implementation.

### Evaluation criteria

- Every required scenario has a deterministic trigger and assertion.
- Tests distinguish no-subscriber behavior from collection behavior.
- Duplicate upstream collection is observable.
- Cancellation and stale-result prevention are verified.

### Optional hints

Track subscription count and query-specific cancellation in the fake
repository.
