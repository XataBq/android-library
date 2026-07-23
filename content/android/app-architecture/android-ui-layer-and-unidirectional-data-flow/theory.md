# Android UI Layer and Unidirectional Data Flow

This topic continues [Android App Architecture Foundations](../android-app-architecture-foundations/theory.md). It focuses on the UI layer: how state is produced, how user intent enters the system, and how an Android interface remains coherent across change and recreation.

## Learning outcomes

After completing this topic, you should be able to model screen state, compare state representations, trace a UDF cycle, classify actions and effects, and justify lifecycle and restoration boundaries.

## 1. Why the UI layer needs explicit boundaries

An interface sits between two volatile worlds. Product data can change because of user work, synchronization, or failure; Android can replace the component displaying it. If rendering, data access, business decisions, and framework interactions share one owner, a lifecycle callback or click handler can become an accidental application architecture.

An explicit UI boundary answers:

- what the screen should display now;
- which part captures an interaction;
- which part transforms inputs into UI state;
- which operation owns an application change;
- which framework work requires an active UI.

The foundations topic established that UI does not own application data. Here the narrower rule is: **UI elements render and forward intent; state producers make screen state; application owners make application changes.**

## 2. UI elements and state holders

**UI elements** include an `Activity`, `Fragment`, Compose UI, custom `View`, or reusable component. They render state, capture input, forward actions, and interact with UI-scoped framework APIs such as navigation, permissions, messages, and external activity launches.

A **state holder** owns state and logic for a particular UI scope. It may:

- combine application data and interaction inputs;
- produce a renderable state snapshot;
- accept actions that require coordination;
- delegate business work to Data or optional Domain boundaries;
- preserve screen-level processing across configuration changes when its lifetime supports that.

`ViewModel` is Android's common screen-level example when the state producer accesses application operations and should survive configuration change. It is not the definition of a state holder. A plain class or the UI itself can hold short-lived, reusable element state. Hold state as close to its consumer as possible while preserving correct ownership and lifetime.

## 3. What UI state represents

UI state is data describing what the interface should display at a particular moment. A useful screen state is sufficiently complete that rendering does not need to query a database, infer whether a request is running, or mutate a hidden shared object.

UI state is not identical to source data. A user record may contain a birth date; UI state may contain a display name, an age label, whether editing is enabled, and which validation message is visible. The state is a presentation contract.

Useful distinctions are:

| Kind | Example | Typical owner |
|---|---|---|
| Source data | Stored profile | Data layer |
| Screen UI state | Profile plus loading and editability | Screen state holder |
| Derived UI state | “Save enabled” from form validity | Closest state producer with the inputs |
| Local element state | One menu is expanded | UI element or local state holder |
| Restoration input | Profile ID or draft text | Saved state or persistent owner, by requirement |

## 4. Modeling complete screen states

One model uses independent properties:

```kotlin
data class ProfileUiState(
    val isLoading: Boolean = false,
    val userName: String? = null,
    val errorMessage: String? = null,
)
```

This supports partial updates and simultaneous conditions. A screen might keep old content visible while refreshing or show a field error beside editable content. But it can also represent unexplained combinations: loading with an error and no decision about whether stale content should remain; neither loading, content, nor error; or content plus an error that rendering treats inconsistently.

A mutually exclusive model narrows representable states:

```kotlin
sealed interface ProfileUiState {
    data object Loading : ProfileUiState
    data class Content(val userName: String) : ProfileUiState
    data object Empty : ProfileUiState
    data class Error(val message: String) : ProfileUiState
}
```

Every variant has an explicit rendering branch, and contradictory top-level states cannot compile into the model. The cost is extensibility: “content while refreshing,” independent field errors, or several concurrently loaded regions can make variants multiply or become deeply nested.

Neither form is universally correct. Use mutually exclusive variants when the whole screen genuinely occupies one mode. Use a data class when important conditions can coexist, but define invariants and defaults so every representable combination has meaning. Hybrid models are also reasonable: a sealed top-level load state containing a data class for interactive content.

## 5. The Unidirectional Data Flow cycle

The core responsibility flow is:

```text
User action
    ↓
UI event
    ↓
State holder
    ↓
Application or data operation
    ↓
Updated state
    ↓
UI rendering
```

This is not a mandatory class diagram, event wrapper, reactive library, or MVI framework. Simple UI logic may stop inside the UI; an action with business meaning travels to the responsible application boundary. The important guarantee is that rendered state has a known producer and the UI does not secretly mutate the snapshot it received.

UDF creates a repeatable explanation: an input was processed, an owner changed or recomputed state, and the UI rendered the new snapshot.

## 6. User actions and state transitions

A **user action** is what the user attempted: `RetrySelected`, `NameChanged`, or `SaveSelected`. A **UI event** is an input that the UI layer handles. Its destination depends on meaning:

- expanding a local panel can update local element state;
- refreshing profile data is delegated through the state holder to an application operation;
- pressing “open settings” can be handled as UI behavior using a framework API.

A **state transition** is the result, such as `Error → Loading → Content`. The transition should be owned where its inputs and rules are known. Rendering must not initiate a network request merely because it encountered `Loading`; otherwise repeated rendering repeats work and makes causality unclear.

## 7. Immutable state

An immutable UI-state value is a snapshot. Consumers can render it but cannot alter the producer's version. Changes create a new snapshot through the owner, which makes transitions traceable and prevents two UI elements from editing shared state behind each other's backs.

This does not mean all application data is immutable forever. A bookmark, order, or profile changes over time. Immutability describes the values exposed across the UI boundary; controlled owners still perform mutations and publish new values.

## 8. Source state and derived UI state

Derived state is computed from other state: whether “Save” is enabled, the count label for filtered items, or which empty message applies. Derive it where all inputs are available and where its meaning belongs.

Do not store both a source value and a derived value as independently mutable facts unless there is a synchronization rule. If `query`, `items`, and `visibleItems` can all change separately, they can disagree. Prefer computing `visibleItems` from authoritative inputs or updating the whole snapshot in one transition.

Derivation can happen in a state holder for screen-wide or testable logic, or near an element for cheap presentation-only logic. Avoid expensive recomputation in rendering, but do not introduce a distant owner for a trivial label.

## 9. Loading, content, empty and error modeling

These labels are product states, not automatic boilerplate:

- **Loading:** required information is not ready.
- **Content:** useful information can be rendered.
- **Empty:** loading succeeded, but the result intentionally contains no items.
- **Error:** an operation failed and the UI must express recovery or limitation.

Ask whether conditions are exclusive. An initial load may replace the screen with `Loading`; a refresh may retain `Content` and add `isRefreshing`. A validation error can coexist with an editable form, while a fatal load error may replace content. “Empty” should not be inferred merely from the initial empty list before loading finishes.

## 10. Durable state and one-time effects

**Durable state** remains true until something changes it: the current form text, validation result, selected tab, or pending confirmation. A new UI instance should usually be able to render it again.

A **one-time effect** requests interaction with an external or framework-owned mechanism: open a permission dialog, launch a file picker, navigate, or display a transient snackbar. Effects require explicit ownership and delivery semantics:

- Who decides the effect is needed?
- Must it happen if the UI was temporarily inactive?
- May it repeat after recreation?
- How is completion or acknowledgement represented?

Do not adopt a universal `Event<T>` wrapper. Often the meaningful result should become durable state—for example, a payment failure remains visible until acknowledged. UI-originated navigation or a picker launch can be handled by the active UI after any business decision returns. If a transient message is essential, model the pending message and its acknowledgement so it is not silently lost. Different effects have different replay requirements.

## 11. Lifecycle-aware observation

UI state may outlive a particular UI element, but rendering and framework work must respect whether that element is active. Lifecycle-aware observation starts consumption when the UI can present results and stops it when presentation is no longer valid. This avoids background rendering work, duplicate collectors after recreation, and effects delivered to an unavailable UI.

Lifecycle awareness does not change data ownership. Stopping observation must not cancel or discard application data that another layer owns. Exact collection APIs depend on the UI toolkit; this topic's invariant is to match observation and framework effects to the consumer's lifecycle.

## 12. Configuration changes and process recreation

A configuration change commonly replaces the host UI component. A screen-level `ViewModel` can retain in-memory state and pipelines across that replacement, which avoids unnecessary reloading. It still does not survive system-initiated process death.

Process recreation requires a reconstruction plan:

- persist application data in the Data layer when it must be durable;
- save only small inputs needed to rebuild UI state, such as an ID, query, or draft;
- recompute derived state from restored inputs and source data;
- decide which transient effects should not replay.

Saving a whole large screen snapshot is rarely the best default. Restoration is a product requirement and storage trade-off, not a property gained merely by using a state-holder class.

## 13. Local UI state versus screen state

Keep state local when it affects one element, has no application meaning, and no longer-lived consumer needs it: an expanded menu, pressed animation, or temporary focus request.

Lift state to a screen state holder when several elements coordinate around it, it is derived from application data, business work changes it, or it must outlive an element. Move it to persistent ownership when product meaning requires survival beyond the screen or process.

Text input and selected tabs are contextual. A disposable filter may stay local; a search query that must return after process recreation needs restoration. Ownership follows meaning, sharing, and lifetime—not the type of widget.

## 14. Android-oriented examples

### Profile refresh

The state holder exposes `Loading`, `Content`, or `Error`. The UI sends `RetrySelected`; the holder delegates loading to Data and publishes a new state. Rendering never starts the request itself.

### Edit form

Draft text, validation, and save availability can coexist, so a data class is often clearer than a variant for every field combination. A successful save updates application data; navigation remains a UI framework interaction with an explicit “navigate once” decision.

### File attachment

The UI launches the picker because it owns the framework contract. The selected URI becomes an action for the state holder. If uploading is business work, it is delegated; progress and failure return as state.

## 15. Common mistakes

- Fetching data from rendering code.
- Letting UI mutate a state snapshot directly.
- Treating `ViewModel` as a place for `Activity`, navigation, permission, or resource objects.
- Exposing several mutable fields that can be observed between related updates.
- Using nullable values and flags without defining valid combinations.
- Converting every result into a fire-and-forget event that can be lost while UI is inactive.
- Replaying navigation or external launches after every recreation.
- Assuming configuration survival implies process survival.
- Lifting every tiny element detail into a screen-level state holder.
- Using a sealed hierarchy even when screen conditions legitimately coexist.

## 16. Trade-offs

| Choice | Benefit | Cost or risk |
|---|---|---|
| One screen-state property | Coherent snapshots | Large states can update more often than needed |
| Several state properties | Independent observation | Related values can become temporarily inconsistent |
| Data class with properties | Partial updates and coexistence | Invalid combinations need explicit invariants |
| Sealed variants | Exhaustive, exclusive rendering | Variant growth and awkward partial content |
| Screen state holder | Lifecycle and testing boundary | Unnecessary ceremony for trivial local state |
| Durable message state | Reliable redisplay and acknowledgement | Requires consumption semantics |
| Transient effect | Direct framework interaction | Loss or replay bugs without a clear contract |

Use the smallest model that makes invalid states difficult and important transitions explainable. Android guidance is adaptable; UDF is a strong responsibility pattern, not a requirement to maximize classes or streams.

## 17. Summary

- UI elements render, capture actions, and own UI-scoped framework interactions.
- State holders produce state and delegate application work to its owner.
- UI state is a complete renderable snapshot, not raw source data.
- Property models and sealed variants solve different state-shape problems.
- UDF gives actions, operations, state transitions, and rendering an explicit route.
- Immutable snapshots prevent consumers from becoming competing owners.
- Durable state and one-time effects require different replay semantics.
- Lifecycle-aware observation protects the active consumer; persistence protects required data.
- Configuration change and process recreation are different restoration problems.
- Keep local state local until sharing, meaning, or lifetime justifies lifting it.
