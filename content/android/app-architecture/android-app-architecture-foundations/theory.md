# Android App Architecture Foundations

Architecture is the set of decisions that determines where responsibilities live, which parts may depend on which other parts, and how data changes move through an application. This topic develops that mental model. It does not prescribe a library, a project template, or a universal number of classes.

## Learning outcomes

After completing this topic, you should be able to:

- explain why Android framework components should not own application data;
- distinguish the UI, Data, and optional Domain layers;
- explain separation of concerns, dependency direction, Single Source of Truth, and Unidirectional Data Flow;
- identify responsibility violations and justify better boundaries.

## 1. Why architecture exists

An application changes continuously. Screens are redesigned, data sources are replaced, product rules evolve, and failures appear in conditions that were not anticipated. Architecture exists to keep the cost and risk of those changes manageable.

Without explicit boundaries, a change in one concern can force unrelated changes elsewhere. Replacing a remote source might alter screen code. A display change might accidentally change a business rule. Two screens might implement the same rule differently. The problem is not simply that a file is long; it is that the system has no dependable answer to “who is responsible for this decision?”

Good architecture makes that answer explicit. Its practical goals are to:

- preserve data consistency;
- localize the effects of change;
- make important logic testable without constructing a screen;
- let readers predict where behavior belongs;
- survive the lifecycle and resource constraints of Android.

Architecture is therefore a means, not a product feature. A boundary is useful only when it reduces a real risk or makes an important responsibility clearer.

## 2. Problems without architecture

### Framework components become accidental owners

Android can create, stop, destroy, and recreate framework components. The system may recreate a screen because configuration changed, and it may later remove the entire application process. A component that hosts UI is therefore a temporary participant in the application, not a reliable owner of application data.

If an `Activity` is the only place that stores an edited order, the order's lifetime is coupled to that particular `Activity` instance. Recreating the component can discard the data. Keeping the same object in memory longer solves only some recreation cases; it does not make in-memory state durable across process removal.

The architectural response is not “save everything forever.” It is to assign ownership according to the required lifetime. Temporary visual state may belong near the UI. Application data must belong to a component or persistent source whose responsibility and recovery behavior match the data.

### Responsibilities become entangled

A screen that renders widgets, loads records, resolves cache conflicts, calculates prices, and writes changes has many reasons to change. A visual redesign and a pricing-rule change both touch the same code. Tests must reproduce UI conditions to verify rules that are not inherently visual.

### Competing copies drift apart

Suppose a bookmark flag is mutable in the screen, a repository cache, and a database. If all three can update it, which value is authoritative after a failed request or a screen recreation? Multiple writable owners turn synchronization into guesswork.

### Dependencies spread implementation details

When UI code knows whether data came from a database, network endpoint, or file, source changes cross the entire application. The UI is then coupled to data acquisition rather than to the application data it needs to present.

## 3. Mental model

Before choosing classes or packages, ask four questions:

1. **What is the responsibility?** Describe the decision or work in one sentence.
2. **Who owns it?** Name the part that is authoritative for performing or changing it.
3. **How long must its state survive?** Consider screen replacement, configuration change, process removal, and offline use separately.
4. **Who may depend on whom?** Keep volatile details from becoming assumptions throughout the system.

These questions produce boundaries. Layers are one way to organize those boundaries:

```text
user action
    ↓
UI layer
    ↓
optional Domain layer
    ↓
Data layer
    ↓
data sources

new application data and UI state flow back toward the UI
```

The downward arrows show requests and code dependencies in a typical design. The return path shows data and state. This is a reasoning model, not a requirement that every application have the same package tree.

## 4. Layers

### UI layer

The UI layer presents application data and is the primary point of user interaction. It:

- renders UI state;
- captures user actions;
- turns application data into screen-specific state when needed;
- owns UI behavior such as what is visible, selected, expanded, or navigated to.

The UI may coordinate a request to bookmark an article, but it should not decide how that bookmark is stored or reconcile conflicting sources. Its output is user intent; its input is state suitable for rendering.

### Data layer

The Data layer owns application data and the business rules that create, change, and reconcile that data. It:

- exposes application data to the rest of the app;
- centralizes mutations;
- coordinates one or more data sources;
- resolves source conflicts;
- hides acquisition and storage details from callers.

A repository is the usual entry boundary in Android guidance, but the architectural idea is more important than the name: callers ask for application data or request a business change without knowing which source performs the work.

### Optional Domain layer

The Domain layer sits between UI and Data when it earns that position. It is useful for complex business logic or logic reused by multiple UI state producers. A focused operation might combine account policy, inventory, and pricing data into one decision.

This layer is optional. Adding a pass-through class for every repository operation creates indirection without clarifying responsibility. Use it when it isolates meaningful complexity or reuse; omit it when the UI can coordinate directly with a clear Data-layer boundary.

The Android guidance's “Domain layer” is not a synonym for Clean Architecture. Clean Architecture is a broader architectural approach with its own boundary and dependency rules. This topic describes the optional layer in Android's official layered guidance and does not imply adoption of Clean Architecture.

## 5. Responsibility boundaries

A boundary is strong when each decision has one natural home and callers do not need to know its internal details.

| Responsibility | Natural owner | Why |
|---|---|---|
| Draw loading, content, and error states | UI | The decision is about presentation. |
| Record that the user tapped “bookmark” | UI | The action originates at the interaction boundary. |
| Decide how bookmarking changes application data | Data, or Domain when the rule is complex/reused | This is a product rule, not a rendering rule. |
| Reconcile local and remote article records | Data | The decision requires knowledge of data sources and consistency policy. |
| Format a value specifically for one screen | UI | The transformation exists for presentation. |
| Combine reusable policy from several repositories | Optional Domain | The operation coordinates business concepts across Data boundaries. |
| Decide which copy of a record is authoritative | Data owner / Single Source of Truth | Authority must be centralized to prevent conflicts. |

Placement follows the nature of the responsibility, not the amount of code. Five lines that decide a business rule are still business logic. Fifty lines that arrange a complex screen are still UI logic.

A small Kotlin sketch can show the distinction without prescribing APIs:

```kotlin
data class Article(val id: String, val isBookmarked: Boolean)

interface Articles {
    fun current(): List<Article>
    fun setBookmarked(articleId: String, bookmarked: Boolean)
}

class ArticlesScreen(private val articles: Articles) {
    fun onBookmarkSelected(id: String) {
        articles.setBookmarked(id, bookmarked = true)
    }
}
```

`ArticlesScreen` reports intent. The `Articles` boundary owns the meaning and consistency of the change. Whether the data is cached, persisted, or synchronized is deliberately absent from the UI.

## 6. Dependency direction

Dependency direction answers which part must know another part's contract.

In a typical Android layered design:

- UI depends on a Data boundary, or on Domain operations when that optional layer exists;
- Domain depends on Data boundaries;
- Data repositories depend on their data sources;
- Data and Domain do not depend on screens or framework component instances.

This direction prevents lower layers from needing to understand how their results will be displayed. A repository can serve several screens because it exposes application meaning rather than screen widgets. A screen can be redesigned without changing how conflicts between data sources are resolved.

Do not confuse **dependency direction** with **data flow**. UI code may depend on a repository contract while data values flow from the repository toward the UI. A user action then travels toward the data owner. The two directions describe different relationships.

Interfaces are useful when they protect a real boundary, enable multiple implementations, or simplify testing. They are not mandatory at every class boundary. Creating an interface for every type can add ceremony without reducing coupling.

## 7. Single Source of Truth

A Single Source of Truth (SSOT) is the authoritative owner for a particular type of data. Only that owner changes the data; other parts observe immutable values or request changes through the owner's boundary.

“Single” applies per data type or responsibility, not necessarily to the whole application. Authentication state and saved articles can have different owners. An offline-first feature will often use a local persistent source as the authority while network results update it. A short-lived piece of UI state may instead be owned by a UI state holder.

SSOT does not mean there can be only one copy. The UI may receive a snapshot, and a cache may hold a derived copy. The rule is that those copies are not competing authorities. When the user bookmarks an article:

1. the UI sends a request to the owner;
2. the owner validates and applies the change;
3. the owner exposes updated data;
4. the UI renders the new state.

The benefit is traceability. If the value is wrong, there is one mutation path to inspect. A database is a common SSOT for offline-first application data, but it is not a universal answer; the required lifetime and consistency policy determine the owner.

## 8. Unidirectional Data Flow

Unidirectional Data Flow (UDF) gives changes a repeatable route:

```text
state flows to the UI
        ↓
the UI renders state
        ↓
the user produces an action
        ↓
the responsible owner processes the action
        ↓
updated state flows to the UI
```

State and actions travel in opposite legs of one loop, but each kind of information has one direction. The UI does not secretly mutate the application-data snapshot it received. It reports intent and waits for the authoritative result.

UDF helps because:

- visible state can be explained as the result of explicit inputs;
- mutations follow a predictable path;
- the UI and state-producing logic can be tested separately;
- stale local edits are less likely to compete with the data owner.

SSOT and UDF solve related but different problems. SSOT answers **who may change this data?** UDF answers **how do state and change requests move?** UDF can carry state from an owner, but the flow pattern alone does not choose the correct owner.

UDF is a strong default for stateful screens, not a demand for maximum machinery. Trivial, isolated UI element state can remain local when it has no application meaning and no other consumer.

## 9. Android examples

### Saved article

The UI displays whether an article is saved. The Data layer owns saved-article data and reconciles the chosen sources. A tap becomes a save or unsave request. Updated article data returns and is transformed into UI state. Recreating the screen does not erase the bookmark because the screen was never its authoritative owner.

### Search query versus search results

The current text in a search box can be UI state: it describes an interaction in progress. Search results are application data obtained through a Data boundary. If recent queries must survive process removal or be shared with another screen, that requirement may move their ownership into the Data layer. Ownership follows meaning and lifetime, not the word “state.”

### Checkout rule used by two screens

If both cart and confirmation screens calculate the same eligibility rule, copying it into both UI state producers creates drift. A Domain operation may be justified because the rule is reused and coordinates Data-layer information. If only one simple screen calls one repository operation, the extra layer may add no value.

### Configuration change and process removal

A configuration change can replace a UI component while the application process remains. Process removal destroys all in-memory objects. These are different events. Architecture should let the UI reconstruct state from appropriate owners; durability still requires persistent storage when product requirements demand survival across process removal.

## 10. Common mistakes

### Treating an Activity as the application

Putting data access, business decisions, and long-lived mutable data in an `Activity` couples application behavior to a temporary UI host. Keep framework orchestration at the edge and delegate application responsibilities.

### Calling a data source directly from UI

If a screen knows the database or network shape, it must also understand source failures and conflicts. Use a Data-layer boundary that owns those policies.

### Creating several writable owners

Allowing UI, cache, and persistence code to update the same fact independently defeats SSOT. Copies may exist, but one owner must govern mutations and reconciliation.

### Confusing all state with persistent data

Scroll position, an expanded panel, an unsent draft, and a confirmed order have different meanings and lifetimes. Persisting everything is wasteful; keeping everything in UI memory is fragile. Classify first.

### Making the Domain layer mandatory

A layer with only pass-through operations increases navigation and maintenance cost. Add it for demonstrated complexity or reuse.

### Naming a pattern instead of assigning responsibilities

Labels such as “MVVM” or “Clean Architecture” do not prove that data has one owner or that dependencies are controlled. Evaluate the actual responsibilities and flows.

### Splitting by file size alone

Moving code out of a large class is not separation of concerns if the new classes still share unclear ownership or expose every implementation detail.

## 11. Trade-offs

Architecture spends complexity to control complexity. More boundaries can improve isolation, but each boundary adds concepts, navigation, models, and tests.

| Choice | Benefit | Cost or risk |
|---|---|---|
| Clear UI/Data separation | Stable data ownership and testable rules | More coordination than a one-file prototype |
| Repository boundary | Hides sources and centralizes mutations | Can feel ceremonial for very small, temporary data |
| Optional Domain layer | Reuses and isolates complex operations | Adds indirection when operations merely forward calls |
| Separate models at boundaries | Limits accidental coupling | Requires mapping and more types |
| Strict UDF | Predictable mutations and traceable state | Can be excessive for isolated, trivial UI state |
| Persistent SSOT | Survives process removal and can support offline use | Requires storage and conflict policy |

Choose the smallest design that preserves the important guarantees. Start with clear UI and Data responsibilities. Add Domain operations, extra models, or stricter access rules when a concrete change, reuse, lifecycle, or consistency problem justifies them. Revisit the decision as the product evolves.

## 12. Summary

- Architecture assigns responsibilities, ownership, dependencies, and change paths.
- Android framework components are temporary UI participants, not dependable owners of application data.
- The UI layer renders state and reports user intent.
- The Data layer owns application data, business rules, source coordination, and mutation boundaries.
- The Domain layer is optional and is useful for complex or reused business operations.
- Dependency direction and runtime data flow are related but distinct.
- SSOT defines the authoritative owner for each data type.
- UDF gives state and change requests predictable paths.
- Recommendations are design tools, not universal laws; use the least structure that protects the guarantees your application needs.
