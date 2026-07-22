# Learning Sequence Architecture Study

Status: ACCEPTED FOR IMPLEMENTATION

## Decision summary

The project will introduce a separate learning-sequence model.

The learning-sequence model is not part of the canonical competency identity model.
It describes an authored pedagogical path through canonical competencies.

Architecture Study 001 concludes that canonical competency relations are
deferred. This model does not reintroduce them under another name.

## 1. Node type

A learning-sequence node references a canonical competency.

Topics and lessons are not sequence nodes at this stage because:

- competencies already express assessable outcomes;
- topics have not yet been authored;
- using competencies keeps the sequence independent of future content packaging;
- topics can later be mapped to sequence steps without changing the sequence identity.

## 2. Structure

The first model uses ordered stages rather than a general graph.

A sequence contains an ordered list of stages.
Each stage contains one or more competency references.

Competencies inside the same stage are not ordered unless a later version explicitly adds ordering.

This structure provides:

- a clear default learning path;
- limited parallelism;
- no graph algorithm requirement;
- no prerequisite semantics;
- deterministic rendering.

## 3. Semantics

Stage order means:

> The competencies in an earlier stage are recommended to be learned before the competencies in a later stage for this authored learning path.

It does not mean:

- semantic prerequisite;
- mandatory dependency;
- inability to assess the later competency independently;
- canonical relation between competencies.

The sequence is therefore pedagogical and contextual.

## 4. Branching

The first version does not model explicit branches.

Alternative paths should be represented as separate learning sequences, for example:

- Android architecture with Compose;
- Android architecture with Views;
- abbreviated architecture review;
- interview preparation path.

This is simpler and more auditable than adding conditional graph edges prematurely.

## 5. Versioning

Each sequence must reference:

- a stable sequence ID;
- a sequence version;
- the canonical competency set ID;
- the canonical competency set version.

A sequence version must change when stage membership or order changes.

## 6. Minimal conceptual model

```yaml
schema_version: 1
sequence_id: android-app-architecture-foundations
sequence_version: 1
title: Android app architecture foundations
competency_set:
  id: android-app-architecture
  version: 2
status: review

stages:
  - id: platform-constraints
    title: Platform constraints
    competencies:
      - <canonical competency id>

  - id: architectural-boundaries
    title: Architectural boundaries
    competencies:
      - <canonical competency id>
```

Optional fields should be limited to:

- stage rationale;
- sequence description;
- editorial notes.

No edge types, weights, difficulty scores, branching conditions, or learner-state rules are included in version 1.

## 7. First learning sequence

### Stage 1 — Platform constraints

- Explain Android component lifecycle constraints.

Purpose: establish why Android architecture must account for recreation, lifecycle changes, and process termination.

### Stage 2 — Foundational boundaries

- Apply separation of concerns.
- Design independent Android app components.
- Isolate Android framework dependencies.

Purpose: establish ownership and dependency boundaries before introducing concrete layers.

### Stage 3 — State and data principles

- Explain single source of truth.
- Explain unidirectional data flow.
- Persist relevant data models.

Purpose: introduce stable state ownership, state propagation, and durable data before layer-specific implementations.

### Stage 4 — UI architecture

- Explain UI-layer responsibilities.
- Design ViewModel UI state.
- Select UI state holders by scope.
- Handle lifecycle work in Compose UI.

Purpose: apply the state principles to Android UI and lifecycle-aware state consumption.

### Stage 5 — Data architecture

- Explain repository responsibilities.
- Design a data layer around repositories.
- Use coroutines and flows across layers.

Purpose: define data ownership and inter-layer access before optional refinements.

### Stage 6 — Dependency management

- Explain dependency injection.
- Scope dependencies when needed.

Purpose: separate construction from consumption and then introduce lifetime decisions.

### Stage 7 — Application composition

- Design single-activity navigation.
- Evaluate an optional domain layer.
- Evaluate layer-specific models.

Purpose: introduce application-scale design choices only after the core UI and data boundaries are understood.

## 8. Deliberate ordering decisions

Repository responsibilities and data-layer design are placed in the same stage.
The research rejected a canonical dependency between them, but they form one coherent instructional unit.

Dependency injection is placed after UI and data layers because learners need concrete object graphs and boundaries before DI has practical meaning.

Optional domain layers and layer-specific models are late-stage competencies because both are conditional complexity-management decisions rather than universal foundations.

Single-activity navigation is also late-stage because it composes screens and destinations but does not define the fundamental UI/data ownership model.

## 9. Rejected alternatives

### One flat ordered list

Rejected because it creates false precision between competencies that can be learned in parallel.

### General DAG

Rejected because current requirements do not justify explicit edges, cycle validation, branching rules, or graph traversal.

### Topics as nodes

Rejected because reviewed topic content does not yet exist and topics are implementation units rather than stable learning outcomes.

### Prerequisite relations

Rejected because the previous relation study found that most candidate dependencies are pedagogical recommendations rather than semantic requirements.

## 10. Implementation decision

Proceed with a minimal learning-sequence package:

- JSON Schema;
- one reviewed sequence YAML;
- repository validation;
- fixtures and tests;
- author documentation;
- project-state synchronization.

Canonical competency relations remain deferred.
