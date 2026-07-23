# Android App Architecture Foundations — Interview preparation

## Foundational questions

### 1. Why should an Activity not own application data?

**Interviewer guidance:** Expect the candidate to connect system-controlled recreation and process removal to unstable ownership. Moving data to another in-memory object is not sufficient when durability across process removal is required.

### 2. What does separation of concerns achieve?

**Interviewer guidance:** A good answer discusses clear responsibilities, localized change, independent testing, and predictable ownership. “Smaller files” alone is incomplete.

### 3. Distinguish the UI and Data layers.

**Interviewer guidance:** UI renders state and captures intent. Data owns application data, business rules, mutations, and source coordination. Screen-specific presentation logic remains UI logic.

### 4. When is a Domain layer justified?

**Interviewer guidance:** Look for complex or reused business operations. The candidate should state that the layer is optional and recognize the cost of pass-through abstractions.

### 5. What is a Single Source of Truth?

**Interviewer guidance:** Expect one authoritative owner *per data type*, not necessarily one database for the entire app. Copies may exist, but they must not be competing mutation authorities.

### 6. How does UDF differ from SSOT?

**Interviewer guidance:** SSOT answers who owns mutation; UDF describes how state and actions travel. Strong answers explain how they reinforce each other without treating them as synonyms.

## Scenario questions

### 7. Two screens can update the same bookmark, and each keeps its own mutable Boolean. What would you change?

**Interviewer guidance:** The candidate should assign bookmark ownership to a Data-layer SSOT, route both actions to it, and render both screens from its updates. Listen for conflict and failure handling, not just shared memory.

### 8. A screen calls a database when offline and a network service when online. What boundary is missing?

**Interviewer guidance:** Expect a Data-layer boundary that hides sources and owns selection, reconciliation, and error policy. Connectivity alone is usually not a complete consistency policy.

### 9. A value must survive rotation but not process removal. Where should it live?

**Interviewer guidance:** There is no single class answer in this topic. The candidate should classify it by meaning, keep UI-only state near UI, and distinguish recreation from durability. Award reasoning over API names.

### 10. A checkout rule is copied into three screen state producers. How would you review it?

**Interviewer guidance:** Reuse and business meaning may justify a Domain operation. Data remains responsible for underlying application data. The candidate should avoid moving presentation decisions into Domain.

## Trade-off questions

### 11. Should every repository have an interface?

**Interviewer guidance:** A balanced answer ties interfaces to protected boundaries, multiple implementations, or testing needs. Reject both universal rules: “always” and “never.”

### 12. Is a database always the SSOT?

**Interviewer guidance:** No. It is a common choice for offline-first persistent data. Ownership depends on consistency and lifetime; short-lived UI state or other data can have different authorities.

### 13. When can strict UDF be excessive?

**Interviewer guidance:** Trivial, isolated UI state may not justify a full action-processing pipeline. Application data shared across consumers still benefits from explicit ownership and mutation paths.

### 14. Is Android's optional Domain layer the same as Clean Architecture?

**Interviewer guidance:** No. Android guidance defines a specific optional layer for complex or reused business logic. Clean Architecture is a broader approach with distinct rules; adopting one label does not automatically establish the other.
