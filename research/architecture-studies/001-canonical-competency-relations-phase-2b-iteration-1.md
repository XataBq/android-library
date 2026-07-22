# Architecture Study 001 — Phase 2B
# Relation Candidate Review — Iteration 1

Status: DRAFT FOR ARCHITECTURAL REVIEW
Scope: Five high-value candidate pairs from the current `android-app-architecture` canonical competency set, version 2
Purpose: Determine whether the current competency set justifies canonical relations, without expanding the relation vocabulary beyond what the evidence supports.

## 1. Decision method

Each pair is reviewed using four questions:

1. Why do the competencies appear related?
2. Is the apparent connection between the competencies themselves or only between their domain objects?
3. Can either competency be demonstrated independently?
4. What is the narrowest defensible decision?

Allowed decisions:

- `accept`
- `reject`
- `needs-more-evidence`

Working relation labels are provisional. Acceptance here does not yet approve a production schema.

---

## 2. Pair 1

### Source competency

`explain-android-component-lifecycle-constraints`

**Outcome summary:** Explain how Android component recreation and process termination constrain ownership and retention of application state or data.

### Target competency

`design-independent-app-components`

**Outcome summary:** Design Android entry-point components so they remain independent and retrieve relevant application data rather than becoming its durable owners.

### Candidate relation

`supports`

### Why they appear related

The lifecycle competency explains the platform behavior that makes component-owned durable state unsafe. The component-design competency describes one architectural response: keep framework entry points independent from durable application-data ownership.

### Competency relation or domain relation?

This is more than a shared-domain association. The explanatory capability supplies a direct rationale for the design capability.

However, the target competency can also be justified by other principles:

- separation of concerns;
- testability;
- replaceability;
- component-boundary discipline.

Therefore, lifecycle knowledge is not the complete semantic basis of the target competency.

### Independence test

A learner can demonstrate the design competency by producing a valid component-independent architecture, even if their explanation of process death and recreation is incomplete.

A learner can also explain lifecycle constraints without being able to design appropriate component boundaries.

The competencies are independently assessable.

### Decision

`accept supports`

### Rationale

The source capability materially informs and motivates the target design, but it is not a strict prerequisite and is not semantically contained by it.

### Rejected alternatives

- `requires`: too strong; valid design can be demonstrated without separately proving the explanatory competency.
- `specializes`: false; the target is not a narrower form of explaining lifecycle constraints.
- `related`: technically possible but less informative than the supported directional claim.

---

## 3. Pair 2

### Source competency

`explain-android-component-lifecycle-constraints`

### Target competency

`isolate-android-framework-dependencies`

**Outcome summary:** Design non-framework classes, including ViewModels, without retaining Activity, Context, Resources, or Application dependencies, placing platform access behind UI or data boundaries.

### Candidate relation

`supports`

### Why they appear related

Lifecycle constraints help explain why retaining framework-owned objects in longer-lived or ordinary classes is unsafe and why state/data ownership should not depend on transient Android components.

### Competency relation or domain relation?

The two competencies share Android lifecycle and framework boundaries, but their primary subjects differ:

- one explains lifecycle and process constraints;
- the other designs dependency boundaries around framework APIs and objects.

The relation exists at the rationale level, not through identity or containment.

### Independence test

A learner can isolate framework dependencies for testability, portability, or clean boundaries without articulating the full lifecycle/process-death model.

Conversely, a learner can explain lifecycle constraints but still design classes that retain inappropriate Android framework dependencies.

### Decision

`accept supports`

### Rationale

Lifecycle understanding is a meaningful rationale for framework isolation, but framework isolation also has independent architectural motivations.

### Rejected alternatives

- `requires`: not semantically necessary.
- `specializes`: the target is not a subtype of the explanatory competency.
- `implements`: misleading; dependency isolation does not implement lifecycle constraints.

---

## 4. Pair 3

### Source competency

`explain-repository-responsibilities`

**Outcome summary:** Explain repository responsibilities such as exposing data, centralizing mutation, coordinating or hiding data sources, resolving conflicts, and containing appropriate business logic.

### Target competency

`design-data-layer-around-repositories`

**Outcome summary:** Design a clear data layer that exposes application data through repositories and prevents other layers from directly accessing data sources.

### Candidate relations reviewed

- `requires`
- `supports`

### Why they appear related

Repositories are explicit structural elements of the target competency. Understanding repository responsibilities appears useful when designing a repository-based data layer.

### Competency relation or domain relation?

Most of the apparent relation comes from domain-object containment:

`Repository` is part of the proposed `Data layer`.

But the competencies demand different demonstrations:

- explain one abstraction’s responsibilities;
- design a whole layer boundary.

The source outcome includes responsibilities not required by the target outcome, such as conflict resolution and coordination details. The target outcome includes layer-level boundary design not covered by the source competency.

### Independence test

A learner can design a structurally valid repository-based data layer using an established pattern without demonstrating the complete repository-responsibility explanation.

A learner can thoroughly explain repository responsibilities without being able to design a coherent data layer.

### Decision

`reject canonical relation`

### Rationale

The pair is strongly associated, but the current evidence supports thematic and domain-object proximity rather than a stable relation between the complete competencies.

A learning sequence may reasonably place repository responsibilities before data-layer design. That would be a pedagogical relation, not a canonical domain relation.

### Rejected alternatives

- `requires`: disproved by independent demonstrability.
- `supports`: plausible in teaching, but too dependent on learning design and too weakly grounded as an intrinsic competency relation.
- `broader` / `narrower`: neither outcome semantically contains the other.

---

## 5. Pair 4

### Source competency

`explain-ui-layer-responsibilities`

**Outcome summary:** Explain the responsibilities of UI elements and state holders and how their lifetimes and ownership boundaries differ.

### Target competency

`design-viewmodel-ui-state`

**Outcome summary:** Design ViewModel UI state using StateFlow, choosing state properties, representation, and construction strategy according to the presented data.

### Candidate relation

`supports`

### Why they appear related

Understanding UI rendering responsibilities and state-holder responsibilities helps a learner decide what belongs in ViewModel state and what remains in the UI.

### Competency relation or domain relation?

There is a real rationale connection, but the target is substantially more specific:

- ViewModel-specific;
- StateFlow-specific;
- concerned with representation and state construction.

The source is broader and explanatory, but that does not automatically make it a canonical parent or prerequisite.

### Independence test

A learner can follow an established ViewModel/StateFlow pattern and produce a valid state design without being able to fully explain the broader UI-layer responsibility model.

A learner can explain UI-layer responsibilities without designing a robust ViewModel state representation.

### Decision

`needs-more-evidence`

### Rationale

`supports` is plausible, but the present source evidence establishes both capabilities separately rather than explicitly asserting a directional dependency or rationale between the complete competencies.

This pair should remain unresolved until either:

- a source explicitly connects UI responsibility boundaries to ViewModel state design; or
- later relation reviews show that the same `supports` semantics is consistently useful across many equivalent pairs.

### Rejected alternatives

- `requires`: too strong.
- `specializes`: the target combines narrower context with a different demonstrated action; this is not clean semantic specialization.
- `broader` / `narrower`: action and success criteria differ.

---

## 6. Pair 5

### Source competency

`explain-dependency-injection`

**Outcome summary:** Explain how dependency injection moves construction out of consumers and supplies dependencies through constructors or framework-aware containers.

### Target competency

`scope-dependencies-when-needed`

**Outcome summary:** Scope a dependency to a container when mutable state must be shared or an expensive, widely used instance should be reused.

### Candidate relation

`supports`

### Why they appear related

Dependency scoping normally occurs within a dependency-management mechanism or container. Understanding dependency injection makes the meaning of construction, ownership, reuse, and container lifetime easier to reason about.

### Competency relation or domain relation?

The relation is primarily between adjacent dependency-management concepts.

The target requires reasoning about lifetime and sharing conditions. The source explains construction and supply. Neither outcome semantically includes the other.

### Independence test

A learner can understand DI but make incorrect scoping decisions.

A learner can apply a documented scoping rule in a DI framework without being able to explain DI as a general architectural technique.

### Decision

`reject canonical relation`

### Rationale

The pair is naturally adjacent in educational content, but the intrinsic relationship between the complete competencies is not strong enough for a canonical edge.

The likely useful relation is instructional:

`explain dependency injection`
`should-be-learned-before`
`scope dependencies when needed`

That relation belongs to a learning sequence, not the canonical competency graph.

### Rejected alternatives

- `requires`: not proven.
- `supports`: true in a broad educational sense, but not sufficiently distinctive to justify a canonical edge.
- `specializes`: false.

---

## 7. Iteration 1 results

| Pair | Decision |
|---|---|
| Lifecycle constraints → Independent app components | `accept supports` |
| Lifecycle constraints → Framework dependency isolation | `accept supports` |
| Repository responsibilities → Data-layer design | `reject` |
| UI-layer responsibilities → ViewModel UI state | `needs-more-evidence` |
| Dependency injection → Dependency scoping | `reject` |

Totals:

- Accepted: 2
- Rejected: 2
- Needs more evidence: 1

---

## 8. Emerging interpretation of `supports`

The two accepted cases share a specific structure:

1. The source competency explains a platform constraint.
2. The target competency describes an architectural response to that constraint.
3. The target remains independently demonstrable.
4. The source is not the only possible rationale for the target.
5. The direction is meaningful.

Provisional definition:

> `A supports B` when demonstrating A provides a direct, reusable rationale for B, while B remains independently assessable and does not semantically require A.

This definition is narrower than “A is useful for learning B.”

Under this interpretation:

- lifecycle constraints support lifecycle-driven architectural boundaries;
- general concept adjacency does not qualify;
- typical teaching order does not qualify;
- shared terminology does not qualify.

---

## 9. Architectural checkpoint

Iteration 1 does not justify a broad relation vocabulary.

It provides preliminary evidence for one relation type:

`supports`

Even this type should remain research-only until tested against the remaining high-value pairs.

No evidence currently justifies adding:

- `requires`
- `specializes`
- `implements`
- generic `related`

to the production model.

## 10. Next action

Review the remaining high-value candidates using the provisional narrow definition of `supports`.

Suggested next iteration:

- persistent data models → single source of truth;
- separation of concerns → layer-specific models;
- UDF → ViewModel UI state;
- UDF → coroutines and flows across layers;
- UI-layer responsibilities → state-holder selection;
- lifecycle constraints → Compose lifecycle work;
- dependency injection → framework dependency isolation;
- single source of truth → repository responsibilities.

After that iteration, stop research and make one of two decisions:

1. define a minimal `supports` relation model; or
2. defer canonical relations and proceed directly to learning-sequence design.
