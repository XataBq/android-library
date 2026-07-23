# Android UI Layer and UDF — Interview preparation

## Foundational questions

### 1. What is UI state?

**Interviewer guidance:** Expect a renderable snapshot of what the interface should display, not a synonym for source data.

### 2. Distinguish a UI element from a state holder.

**Interviewer guidance:** UI renders, captures input, and uses UI-scoped framework APIs. A holder produces state and delegates application work. ViewModel is one screen-level implementation, not the definition.

### 3. Explain the UDF cycle.

**Interviewer guidance:** Look for action → handling/delegation → new state → rendering, plus the reason UI must not mutate received state.

### 4. Why expose immutable UI state?

**Interviewer guidance:** It makes snapshots stable and mutation paths explicit. It does not imply that application data never changes.

### 5. When is a sealed state hierarchy useful?

**Interviewer guidance:** Exclusive screen modes and exhaustive rendering. The candidate should mention variant growth and coexisting conditions.

## Scenario questions

### 6. A screen shows content while refreshing and can also show a field error. How would you model it?

**Interviewer guidance:** Independent properties or a hybrid can express coexistence better than mutually exclusive whole-screen variants; invariants still matter.

### 7. Rendering an empty list starts a request. What is wrong?

**Interviewer guidance:** Rendering can repeat. An explicit action or initialization input should start work; `Empty` must differ from “not loaded.”

### 8. A ViewModel emits navigation while no UI is active. What must be decided?

**Interviewer guidance:** Ownership, delivery, replay, and acknowledgement. Prefer durable state for meaningful results; UI owns the actual framework call.

### 9. Which state survives rotation but not process death?

**Interviewer guidance:** ViewModel-held memory survives configuration changes, not system process death. Reconstruction needs saved inputs or persistent data.

### 10. Where should a selected tab live?

**Interviewer guidance:** As low as possible unless coordination or restoration requirements justify screen-level ownership.

## Trade-off questions

### 11. One UI-state property or several?

**Interviewer guidance:** One gives coherent snapshots; several can reduce unrelated updates but risk inconsistent related values.

### 12. Should every user outcome be a one-time event?

**Interviewer guidance:** No. Results that remain meaningful should usually become state. True effects need explicit loss/replay semantics.

### 13. Must every reusable UI component have a ViewModel?

**Interviewer guidance:** No. Plain/local state holders fit reusable UI logic; screen ViewModels are useful when their lifetime and application access are needed.

### 14. Why observe state with lifecycle awareness?

**Interviewer guidance:** To align rendering/effects with an active consumer and avoid duplicate or background work, without changing Data ownership.
