# Android App Architecture Foundations — Cheat sheet

## Definitions

- **Architecture:** decisions about responsibilities, ownership, dependencies, and change paths.
- **Separation of concerns:** assigning distinct responsibilities to clear boundaries so one kind of change does not spread unnecessarily.
- **UI layer:** renders UI state, captures user actions, and owns presentation behavior.
- **Data layer:** owns application data, business rules, data-source coordination, and mutations.
- **Domain layer:** optional boundary for complex or reused business operations between UI and Data.
- **Single Source of Truth (SSOT):** the one authoritative owner allowed to change a particular type of data.
- **Unidirectional Data Flow (UDF):** state follows one path to consumers; actions follow a defined path back to the responsible owner.

## Responsibility table

| Responsibility | Place it in |
|---|---|
| Render loading, content, or error state | UI |
| Capture a tap or text change | UI |
| Apply a product rule to application data | Data, or Domain when complex/reused |
| Reconcile database, network, or cache values | Data |
| Combine reusable logic across repositories | Optional Domain |
| Decide how a value is displayed | UI |
| Authoritatively mutate a data type | Its SSOT |

## Dependency rules

```text
UI → optional Domain → Data → data sources
```

- UI depends on application-facing boundaries, not concrete data sources.
- Domain, when present, depends on Data boundaries and does not know screens.
- Data does not depend on UI or framework component instances.
- State/data can flow toward UI even when UI code depends toward Data.
- Add interfaces where they protect a real boundary; they are not mandatory everywhere.

## Common violations

- An `Activity` owns application data or implements product rules.
- UI calls a database, network client, or file source directly.
- UI and Data both mutate the same fact.
- A repository returns source-specific details that every caller must understand.
- A Domain operation only forwards every Data call and adds no policy or reuse.
- “MVVM” or “Clean Architecture” is used as a substitute for explaining ownership.

## Architecture checklist

- [ ] Can each responsibility be stated in one sentence?
- [ ] Is one owner authoritative for each type of data?
- [ ] Does ownership match the required lifecycle and durability?
- [ ] Can UI be recreated from state supplied by appropriate owners?
- [ ] Does UI report intent instead of directly mutating application data?
- [ ] Are storage and network details hidden behind the Data boundary?
- [ ] Do dependencies avoid pointing from Data or Domain into UI?
- [ ] Is each extra layer justified by complexity, reuse, or change isolation?
- [ ] Are optional Android recommendations presented as choices, not laws?
