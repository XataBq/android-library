# Architecture Study 001 — Phase 2A
# Semantic Profiling of Canonical Competencies

Status: DRAFT FOR ARCHITECTURAL REVIEW
Type: Architecture research
Scope: Current `android-app-architecture` canonical competency set, version 2
Repository: `android-library`

## 1. Purpose

Test the hypothesis that a canonical competency has a useful internal semantic structure that can be analyzed independently from its title and outcome wording.

This phase does **not** change the canonical competency schema. It creates an editorial profile of every current competency and evaluates whether recurring dimensions are:

- stable;
- independently meaningful;
- useful for relation analysis;
- suitable for later formalization;
- or merely artifacts of wording.

## 2. Hypothesis

> A canonical competency can be interpreted through several semantic dimensions, including the demonstrated action, the domain focus, the abstraction level, the expected form of demonstration, and contextual constraints.

The hypothesis is useful only if these dimensions can be applied consistently across the current set without forcing competencies into artificial categories.

## 3. Method

Each competency is profiled using the following provisional dimensions.

### 3.1 Capability mode

The dominant kind of demonstrated capability.

Provisional values:

- `explanation`
- `design`
- `application`
- `evaluation`
- `selection`
- `operation`

These values are research labels, not schema enums.

### 3.2 Domain focus

The primary subject of the capability.

Examples:

- Android lifecycle constraints;
- repository responsibilities;
- UI-state design;
- dependency scoping.

The domain focus is expressed as a phrase rather than mapped to a taxonomy.

### 3.3 Abstraction level

The level at which the competency primarily operates.

Provisional values:

- `architectural-principle`
- `architectural-structure`
- `architectural-decision`
- `component-responsibility`
- `implementation-pattern`
- `platform-specific-practice`
- `technology-specific-practice`

A competency may touch several levels. The profile records the dominant one and notes secondary levels where relevant.

### 3.4 Expected demonstration

What observable evidence would normally show that the competency has been demonstrated.

Examples:

- explain causal constraints;
- propose a valid architecture;
- choose between alternatives and justify the choice;
- implement or apply a practice correctly.

This is not an assessment specification.

### 3.5 Context specificity

How strongly the competency identity depends on Android-specific or technology-specific context.

Provisional values:

- `general-software`
- `android-architecture`
- `android-framework`
- `android-compose`
- `kotlin-android`

### 3.6 Independence

Whether the competency remains independently assessable within the current set.

Values:

- `strong`
- `moderate`
- `question`

`question` does not mean invalid. It means the current boundary should be kept under observation when relations are introduced.

## 4. Profiles

### 4.1 `explain-android-component-lifecycle-constraints`

**Title:** Explain Android component lifecycle constraints

- Capability mode: `explanation`
- Domain focus: Activity recreation, process termination, and state/data retention constraints
- Abstraction level: `platform-specific-practice`
- Expected demonstration: explain why framework components cannot safely own durable application data or state across recreation and process loss
- Context specificity: `android-framework`
- Independence: `strong`
- Notes:
  - The competency explains causal constraints, not a design solution.
  - It may motivate several design competencies, but motivation does not prove a canonical dependency.
  - Its object is a platform behavior and its consequence for ownership.

### 4.2 `design-independent-app-components`

**Title:** Design independent Android app components

- Capability mode: `design`
- Domain focus: independence of activities, services, and broadcast receivers from application-data ownership
- Abstraction level: `component-responsibility`
- Expected demonstration: design component boundaries so Android entry points retrieve relevant data without becoming data owners
- Context specificity: `android-framework`
- Independence: `strong`
- Notes:
  - This is not a narrower restatement of lifecycle constraints.
  - It is a design response to several possible pressures, lifecycle constraints being one of them.
  - The competency combines component independence and data-ownership boundaries.

### 4.3 `apply-separation-of-concerns`

**Title:** Apply separation of concerns

- Capability mode: `application`
- Domain focus: cohesive responsibility and boundary assignment across application units
- Abstraction level: `architectural-principle`
- Expected demonstration: divide responsibilities so unrelated classes do not jointly implement one operation without a clear boundary
- Context specificity: `general-software`
- Independence: `strong`
- Notes:
  - This is the broadest principle-level competency in the current set.
  - It can be applied in many structures represented by other competencies.
  - That broad applicability does not automatically create `broader` relations to every concrete design competency.

### 4.4 `explain-persistent-data-models`

**Title:** Explain persistent data models

- Capability mode: `explanation`
- Domain focus: persistent application-data models and resilience across UI lifecycle, process removal, and connectivity loss
- Abstraction level: `architectural-structure`
- Expected demonstration: explain how persistence decouples application data from transient UI/component lifetimes and unavailable connectivity
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - The competency explains properties and consequences of persistent models.
  - It does not require selecting a persistence technology.
  - It overlaps in motivation with lifecycle constraints but has a distinct subject and success criterion.

### 4.5 `establish-single-source-of-truth`

**Title:** Establish a single source of truth

- Capability mode: `design`
- Domain focus: ownership and mutation control for each data type
- Abstraction level: `architectural-principle`
- Expected demonstration: assign one authoritative owner that exposes data immutably and controls changes through its API
- Context specificity: `general-software`
- Independence: `strong`
- Notes:
  - This is a normative design capability, not merely an explanation.
  - Repository design can realize this principle, but repository identity is not part of the competency.
  - A future relation to repositories would need to distinguish “common realization” from semantic necessity.

### 4.6 `explain-unidirectional-data-flow`

**Title:** Explain unidirectional data flow

- Capability mode: `explanation`
- Domain focus: state flow toward UI and actions/events toward a state owner
- Abstraction level: `implementation-pattern`
- Expected demonstration: explain the state/event cycle and representation of handling results as updated state
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - The current outcome is implementation-oriented but still explanatory.
  - It is not equivalent to designing ViewModel UI state.
  - It may support later design or implementation tasks without being a formal prerequisite.

### 4.7 `explain-ui-layer-responsibilities`

**Title:** Explain UI layer responsibilities

- Capability mode: `explanation`
- Domain focus: division between UI rendering and state-holder responsibilities
- Abstraction level: `component-responsibility`
- Expected demonstration: explain what UI elements and state holders each own and how their lifetimes relate
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - This is a layer-responsibility model.
  - `design-viewmodel-ui-state` is more concrete but differs in action, technology, and expected artifact.
  - A specialization relation is therefore not yet justified.

### 4.8 `design-data-layer-around-repositories`

**Title:** Design a data layer around repositories

- Capability mode: `design`
- Domain focus: data-layer boundaries, application business logic, repositories, and data-source access
- Abstraction level: `architectural-structure`
- Expected demonstration: propose a data-layer design in which repositories expose application data and other layers do not directly access data sources
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - This competency concerns layer structure.
  - `explain-repository-responsibilities` concerns the responsibilities of one abstraction within that structure.
  - The two are strongly associated, but neither outcome semantically contains the other.

### 4.9 `explain-repository-responsibilities`

**Title:** Explain repository responsibilities

- Capability mode: `explanation`
- Domain focus: repository data exposure, mutation centralization, conflict resolution, source hiding, and applicable business logic
- Abstraction level: `component-responsibility`
- Expected demonstration: explain the responsibilities and boundaries of a repository
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - This is not a topic label because the responsibilities are observable and scoped.
  - It can inform data-layer design, but the relation may be pedagogical rather than intrinsic.
  - It should not be treated as a parent concept solely because repositories appear in another title.

### 4.10 `evaluate-optional-domain-layer`

**Title:** Evaluate the need for a domain layer

- Capability mode: `evaluation`
- Domain focus: conditions that justify an optional domain layer
- Abstraction level: `architectural-decision`
- Expected demonstration: analyze complexity and logic reuse, then justify whether introducing a domain layer is warranted
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - This competency is explicitly conditional.
  - It requires decision criteria rather than unconditional layer construction.
  - Its semantic class is materially different from a generic “domain layer” concept.

### 4.11 `explain-dependency-injection`

**Title:** Explain dependency injection

- Capability mode: `explanation`
- Domain focus: externalized object construction and dependency supply
- Abstraction level: `implementation-pattern`
- Expected demonstration: explain how consumers receive dependencies without constructing them and how constructors or framework-aware containers participate
- Context specificity: `general-software`
- Independence: `strong`
- Notes:
  - The outcome includes general DI plus Android-aware container context.
  - `scope-dependencies-when-needed` is adjacent but independently assessable.
  - DI and scoping must not be collapsed into one concept.

### 4.12 `design-single-activity-navigation`

**Title:** Design single-activity navigation

- Capability mode: `design`
- Domain focus: one-Activity hosting, destinations, navigation, and deep links
- Abstraction level: `architectural-structure`
- Expected demonstration: design an Android application with one Activity hosting multiple destinations and route navigation/deep links through in-app navigation
- Context specificity: `android-framework`
- Independence: `strong`
- Notes:
  - This is a concrete Android architecture decision.
  - It is not a specialization of component independence or separation of concerns by definition.
  - Any relation to those principles would express rationale, not semantic containment.

### 4.13 `use-coroutines-and-flows-across-layers`

**Title:** Use coroutines and flows across layers

- Capability mode: `application`
- Domain focus: Flow-based data delivery and suspend-function actions across layers and ViewModels
- Abstraction level: `technology-specific-practice`
- Expected demonstration: apply Kotlin Flow and suspend APIs correctly at layer boundaries and from ViewModels
- Context specificity: `kotlin-android`
- Independence: `strong`
- Notes:
  - Technology identity is essential to the competency.
  - It is not merely an implementation of UDF; flows can be used outside UDF, and UDF does not require these exact technologies.
  - The pair may be commonly taught together without a canonical semantic relation.

### 4.14 `design-viewmodel-ui-state`

**Title:** Design ViewModel UI state

- Capability mode: `design`
- Domain focus: ViewModel data acquisition and StateFlow-based UI-state representation
- Abstraction level: `technology-specific-practice`
- Expected demonstration: design state properties, representation, construction strategy, and ViewModel exposure through StateFlow
- Context specificity: `kotlin-android`
- Independence: `strong`
- Notes:
  - The competency combines an Android component, a state-design concern, and a Kotlin technology.
  - Its relation to UI-layer responsibilities is contextual rather than taxonomically obvious.
  - Its relation to UDF may be an implementation alignment, but “implements” is not sufficiently defined.

### 4.15 `isolate-android-framework-dependencies`

**Title:** Isolate Android framework dependencies

- Capability mode: `design`
- Domain focus: keeping non-framework classes and ViewModels free of Activity, Context, Resources, and Application retention
- Abstraction level: `component-responsibility`
- Expected demonstration: place required platform access behind appropriate UI or data boundaries instead of retaining framework objects in ordinary classes
- Context specificity: `android-framework`
- Independence: `strong`
- Notes:
  - This is a dependency-boundary design capability.
  - It shares rationale with lifecycle independence but is not equivalent to explaining lifecycle constraints.
  - It also overlaps with component independence at a different boundary.

### 4.16 `select-ui-state-holders-by-scope`

**Title:** Select UI state holders by scope

- Capability mode: `selection`
- Domain focus: choosing ViewModels versus plain state-holder classes by UI scope, complexity, reuse, and external control
- Abstraction level: `architectural-decision`
- Expected demonstration: evaluate scope and reuse constraints, choose an appropriate state-holder form, and justify the choice
- Context specificity: `android-compose`
- Independence: `strong`
- Notes:
  - This is decision-making, not state-holder implementation.
  - It depends on comparison criteria but not necessarily on another canonical competency.
  - It may later connect to learning content about ViewModels and state hoisting.

### 4.17 `handle-compose-lifecycle-work`

**Title:** Handle lifecycle work in Compose UI

- Capability mode: `operation`
- Domain focus: lifecycle-aware state collection and other lifecycle-bound work in Compose
- Abstraction level: `platform-specific-practice`
- Expected demonstration: choose and apply lifecycle-aware Compose effects or coroutine APIs instead of Activity lifecycle callbacks
- Context specificity: `android-compose`
- Independence: `strong`
- Notes:
  - This is a concrete operational capability.
  - Android lifecycle understanding plausibly supports it, but the current competency model does not prove a strict dependency.
  - The verb `handle` hides both selection and application behavior.

### 4.18 `scope-dependencies-when-needed`

**Title:** Scope dependencies when needed

- Capability mode: `evaluation`
- Domain focus: dependency lifetime and reuse based on shared mutable state or construction cost
- Abstraction level: `architectural-decision`
- Expected demonstration: determine when container scoping is justified and apply the appropriate lifetime boundary
- Context specificity: `general-software`
- Independence: `strong`
- Notes:
  - The title sounds operational, but the outcome is primarily conditional evaluation.
  - This shows that title verbs alone are not a reliable semantic classifier.
  - The capability includes a decision and a resulting configuration.

### 4.19 `evaluate-layer-specific-models`

**Title:** Evaluate layer-specific models

- Capability mode: `evaluation`
- Domain focus: mapping external or persistence models into layer-specific representations
- Abstraction level: `architectural-decision`
- Expected demonstration: assess complexity and consumer needs, then justify whether separate layer models are beneficial
- Context specificity: `android-architecture`
- Independence: `strong`
- Notes:
  - The competency is explicitly conditional and avoids a universal mapping rule.
  - It may be associated with separation of concerns and layer boundaries, but that association is too general for an initial relation type.
  - Its decision criteria are part of its identity.

## 5. Cross-set findings

### 5.1 Capability mode is real, but not reliably derivable from the title verb

Most competencies can be assigned a dominant capability mode. However:

- `scope-dependencies-when-needed` begins with `scope` but semantically centers on evaluation;
- `handle-compose-lifecycle-work` contains selection and application;
- `establish-single-source-of-truth` is a design capability despite lacking the verb `design`;
- `use-coroutines-and-flows-across-layers` is application-oriented but also contains technology-selection assumptions.

Conclusion:

> Capability mode is a useful editorial dimension, but it must be derived from the full outcome rather than the first title verb.

### 5.2 Domain focus is useful but is not yet a canonical entity

The current competencies clearly operate on recurring domain objects:

- lifecycle;
- app components;
- data models;
- repositories;
- layers;
- state holders;
- dependency injection;
- navigation;
- coroutines and flows.

However, the current data does not define stable canonical concept IDs for these objects.

Conclusion:

> Domain focus can support analysis and search, but formal relations between domain objects would require a separate concept or taxonomy model.

### 5.3 Abstraction level is multi-dimensional

A single linear ladder is insufficient.

For example:

- `apply-separation-of-concerns` is principle-level;
- `design-data-layer-around-repositories` is structural;
- `explain-repository-responsibilities` is responsibility-level;
- `design-viewmodel-ui-state` is technology-specific design;
- `handle-compose-lifecycle-work` is platform-specific operation.

These are not always ordered from broad to narrow. They differ by:

- generality;
- artifact scale;
- technology dependence;
- cognitive operation.

Conclusion:

> `abstraction_level` should not be introduced as a single ordered enum without further evidence.

### 5.4 Expected demonstration is the most stable internal dimension

Every competency can be described by an observable expected demonstration:

- explain;
- design;
- apply;
- choose;
- evaluate;
- operate.

This aligns with the existing canonical rule that a competency must be demonstrable.

Conclusion:

> Expected demonstration is already implicit in the model and could later help assessments, but it does not need to become a canonical field yet.

### 5.5 Context specificity is useful for identity review

The set includes:

- general software capabilities;
- Android architecture capabilities;
- Android framework-specific capabilities;
- Compose-specific capabilities;
- Kotlin/StateFlow/Flow-specific capabilities.

Context specificity helps reviewers decide whether two competencies are equivalent, broader/narrower, or distinct.

Conclusion:

> Context specificity is useful during normalization and relation review, but may be better represented by future scope or concept mappings than by a fixed competency enum.

### 5.6 All current competencies remain independently assessable

No current competency clearly fails the independence test.

Several pairs are strongly associated, but each retains a distinct expected demonstration:

- lifecycle constraints vs independent component design;
- UI-layer responsibility explanation vs ViewModel state design;
- data-layer design vs repository responsibility explanation;
- dependency injection explanation vs dependency-scoping evaluation.

Conclusion:

> Phase 2A does not currently reveal a competency that must be merged or split before relation research continues.

## 6. Important negative result

The semantic profile does **not** support a universal progression such as:

```text
explain → design → apply → evaluate
```

Reasons:

- evaluation may precede design;
- explanation and application can be independently assessed;
- practical capability does not universally imply explanatory mastery;
- different competencies concern different domain objects;
- learning progression depends on curriculum and learner context.

Therefore, capability modes must not be treated as canonical prerequisite edges.

## 7. Refined competency interpretation

A useful editorial interpretation is:

```text
Canonical competency
=
expected demonstration
+
domain focus
+
scope and constraints
+
context
```

The current data does not justify treating all four parts as independent canonical entities.

The canonical outcome remains the authoritative semantic unit.

The profile is an analytical projection of that outcome, not a replacement for it.

## 8. Consequences for relation research

Relations between full competencies remain valid candidates, but every proposed edge must state which semantic dimension makes the relation true.

A relation candidate should answer:

1. Is the relation between the demonstrated capabilities?
2. Is it only between their domain objects?
3. Is it caused by shared context?
4. Is it an instructional progression?
5. Is it a rationale or design motivation?
6. Is it semantic containment?
7. Would the relation remain true if title verbs changed but outcomes retained the same meaning?

If the edge only connects domain objects such as `Repository` and `Data layer`, it does not automatically belong in the competency relation graph.

## 9. Proposed Phase 2B analysis record

Each candidate relation should use a research record like:

```yaml
source_competency_id: design-data-layer-around-repositories
target_competency_id: explain-repository-responsibilities

candidate_relation: requires

dimension:
  - demonstrated-capability
  - domain-focus

claim: >
  Designing a repository-based data layer requires the ability to explain
  repository responsibilities.

domain_or_learning: unresolved

source_support:
  explicit: false
  notes: >
    Current evidence supports both competencies separately but does not explicitly
    assert that one is required for the other.

tests:
  remains_true_across_curricula: unknown
  semantic_necessity: unproven
  duplicate_boundary_risk: low
  more_precise_relation_available: unknown

decision: reject-for-now
```

## 10. Phase 2A conclusion

The hypothesis is **partially confirmed**.

Confirmed:

- competencies have analyzable internal semantic dimensions;
- capability mode, expected demonstration, domain focus, and context are useful;
- these dimensions clarify why intuitive competency relations are often ambiguous;
- title verbs alone are insufficient;
- expected demonstration is especially stable;
- the current competencies remain independently assessable.

Not confirmed:

- that these dimensions should become canonical schema fields;
- that domain objects should become canonical entities;
- that abstraction levels form a stable ordered hierarchy;
- that capability modes imply learning or prerequisite relations;
- that relations should target decomposed subentities instead of competencies.

Decision:

```text
KEEP SEMANTIC PROFILING AS AN EDITORIAL RESEARCH MODEL
DO NOT CHANGE THE CANONICAL COMPETENCY SCHEMA
PROCEED TO PHASE 2B RELATION-CANDIDATE ANALYSIS
```

## 11. Architectural checkpoint

The current canonical model remains valid:

```text
stable capability
+
canonical wording
+
traceable evidence
```

Phase 2A adds an analytical lens, not a new production model.

Any future proposal to formalize semantic fields must independently demonstrate:

- a concrete consumer;
- stable controlled vocabularies;
- cross-source consistency;
- improved validation or product behavior;
- no duplication of meaning already carried by the canonical outcome.
