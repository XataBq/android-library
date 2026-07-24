# Task 024 — Add Dependency Injection and Scoping Topic

Status: DONE

## Objective

Add the twelfth production educational topic in the Junior Core:

```text
android-dependency-injection-and-scoping
```

The topic must explain dependency injection as an object-graph and ownership problem, not as annotation memorization.

The learner must understand:

- dependency inversion;
- constructor injection;
- composition root;
- object graph;
- provider/factory semantics;
- scope and lifetime;
- Android component lifecycles;
- ViewModel injection;
- Activity/Fragment/Navigation graph scope;
- singleton misuse;
- qualifiers;
- multibinding;
- assisted injection;
- testing;
- framework isolation.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds on:

- Architecture Foundations;
- UI Layer and UDF;
- Data Layer and Repositories;
- Domain Layer and Use Cases;
- ViewModel and UI State;
- Lifecycle and State Restoration;
- Navigation Architecture;
- Networking Architecture.

---

## Core teaching position

Dependency injection exists to assemble an object graph while preserving explicit ownership and replaceable boundaries.

The core model is:

```text
constructor declares dependency
composition root creates implementation
scope defines lifetime
owner destroys graph when lifetime ends
```

The topic must preserve these distinctions:

```text
DI
≠ service locator
≠ global singleton registry
≠ annotation processor
≠ automatic architecture
```

Frameworks such as Hilt/Dagger/Koin may automate wiring, but they do not decide correct boundaries, ownership, or scope.

---

## Source-of-truth requirements

Before authoring, inspect:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_VALIDATION.md`
- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`
- all content-authoring documentation;
- canonical Android architecture competencies;
- imported Android Developers source packages;
- all production topics;
- Tasks 016–023.

Use current official or primary documentation for:

- dependency injection principles;
- Hilt component hierarchy and scopes;
- ViewModel injection;
- qualifiers;
- multibinding;
- assisted injection where supported;
- testing overrides;
- navigation graph scoping.

Do not fabricate framework guarantees.

Do not fabricate access dates.

Clearly distinguish stable DI concepts from framework-specific APIs and versions.

---

## Canonical competency scope

Primary:

```text
apply-separation-of-concerns
isolate-android-framework-dependencies
select-ui-state-holders-by-scope
```

Strongly reinforced:

```text
design-viewmodel-ui-state
design-data-layer-around-repositories
evaluate-optional-domain-layer
explain-android-component-lifecycle-constraints
```

Contextually reinforced:

```text
explain-ui-layer-responsibilities
use-coroutines-and-flows-across-layers
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/architecture/android-dependency-injection-and-scoping/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: architecture` is required, keep it and document the taxonomy decision.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-dependency-injection-and-scoping
title: Android Dependency Injection and Scoping
track: android
section: architecture
difficulty: foundation
status: review
estimated_minutes: 210
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-data-layer-repositories-and-synchronization
  - android-domain-layer-and-use-cases
  - android-viewmodel-and-ui-state
  - android-lifecycle-and-state-restoration
  - android-navigation-architecture
  - android-networking-architecture
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain dependency injection and dependency inversion.
2. Distinguish DI from service locator.
3. Use constructor injection by default.
4. Explain composition root.
5. Explain object graph.
6. Explain provider and factory semantics.
7. Explain scope as lifetime plus owner.
8. Match dependency lifetime to Android owner lifetime.
9. Distinguish singleton, Activity, Fragment, ViewModel, navigation graph, and unscoped objects.
10. Explain why “singleton” does not mean process-independent or immortal.
11. Inject ViewModel dependencies without passing Activity/Fragment.
12. Distinguish scope reuse from object identity assumptions.
13. Use qualifiers for same-type dependencies.
14. Use multibinding for plugin/handler collections.
15. Use assisted injection for runtime values where appropriate.
16. Keep Context dependencies explicit and narrow.
17. Avoid injecting mutable global state.
18. Replace dependencies in tests.
19. Recognize DI anti-patterns.
20. Design a maintainable application graph.

---

## Theory requirements

`theory.md` must contain approximately 20–24 substantial sections.

Required coverage:

### 1. What dependency injection solves

Explain explicit dependencies, construction, replacement, and ownership.

### 2. Dependency inversion

Explain high-level policy depending on abstractions rather than concrete infrastructure.

### 3. Constructor injection

Explain why it is the default:

- dependencies are visible;
- object cannot exist half-initialized;
- tests are easy;
- no hidden lookup.

### 4. Composition root

Explain where application object graphs are assembled.

### 5. Object graph

Explain nodes, edges, transitive dependencies, cycles, and graph construction.

### 6. DI versus service locator

Compare:

```text
constructor receives dependency
vs
object asks global container for dependency
```

Explain hidden dependencies and testability.

### 7. Manual DI

Show a small composition root without a framework.

### 8. DI frameworks

Explain what Hilt/Dagger/Koin-like tools automate:

- graph generation or runtime resolution;
- provider registration;
- scope reuse;
- entry points;
- test replacement.

Explain what they do not solve.

### 9. Provider and factory

Distinguish:

- same instance within a scope;
- new instance per request;
- lazy creation;
- provider function;
- factory with runtime input.

### 10. Scope is lifetime plus owner

This must be central.

Explain:

```text
scope name
→ owner
→ creation boundary
→ reuse boundary
→ destruction boundary
```

### 11. Unscoped objects

Explain new-instance semantics and why unscoped does not mean “no lifecycle”.

### 12. Application/process scope

Cover:

- process lifetime;
- app component;
- process death;
- no guarantee across restarts;
- avoiding mutable global state.

### 13. Activity and Fragment scope

Explain:

- configuration changes;
- Fragment view lifecycle versus Fragment lifecycle;
- retained state;
- why UI objects must not leak.

### 14. ViewModel scope

Explain:

- ViewModelStoreOwner;
- Activity, Fragment, and navigation graph owners;
- injection into ViewModel;
- no Activity/Fragment references;
- SavedStateHandle.

### 15. Navigation graph scope

Explain graph-owned dependencies and shared ViewModel boundaries.

### 16. Qualifiers

Cover same interface/type with different semantics:

- authenticated client;
- public client;
- IO dispatcher;
- default dispatcher;
- base URLs.

Warn against stringly typed lookup.

### 17. Multibinding

Explain sets/maps of:

- handlers;
- validators;
- strategies;
- feature contributions.

Explain ordering assumptions.

### 18. Assisted injection

Explain compile-time dependencies plus runtime arguments.

Use cases:

- worker input;
- runtime ID;
- factory-created object;
- non-DI-owned framework object.

Clearly mark framework/version specifics where relevant.

### 19. Context injection

Distinguish:

- application Context;
- Activity Context;
- themed Context;
- resource access;
- avoiding accidental leaks.

### 20. Cycles and graph smells

Explain:

- cyclic dependencies;
- mediator abuse;
- giant god object;
- split interfaces;
- event bus as escape hatch;
- over-scoping.

### 21. Testing

Cover:

- constructor replacement;
- fake repository;
- fake clock/dispatcher;
- test component/module override;
- scope reset;
- avoiding hidden global state between tests.

### 22. Framework boundaries

Explain:

- framework annotations in composition layer;
- keeping domain interfaces framework-free;
- when framework annotations in implementation classes are acceptable;
- avoiding DI container APIs in business code.

### 23. Anti-patterns

At minimum:

- field injection by default;
- global service locator;
- injecting NavController into ViewModel;
- Activity Context in singleton;
- every dependency scoped as singleton;
- mutable singleton state;
- static object graph;
- hidden provider lookup;
- injecting Retrofit into UI;
- scope mismatch;
- duplicate bindings without qualifier;
- giant module;
- passing container through layers;
- testing by mutating production singleton;
- accidental graph cycle.

### 24. Decision guide

End with:

```text
What does this object depend on?
Who creates it?
Who owns it?
How long must it live?
Should instances be reused?
What runtime input is required?
How is it replaced in tests?
Can this dependency leak a framework owner?
```

---

## Kotlin example requirements

Include at least:

1. constructor injection;
2. manual composition root;
3. service locator anti-pattern;
4. interface plus implementation binding;
5. provider/factory distinction;
6. unscoped creation;
7. application-scoped dependency;
8. Activity-scoped dependency;
9. Fragment/ViewModel scope example;
10. navigation graph scoped ViewModel;
11. SavedStateHandle injection;
12. qualifier example;
13. multibinding set or map;
14. assisted factory;
15. application Context injection;
16. scope mismatch leak example;
17. fake replacement in unit test;
18. test module/component override;
19. cycle example and refactor;
20. framework-free domain dependency.

Examples must be conceptually compilable and version-aware.

Do not mix incompatible DI frameworks in one code sample.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- DI mental model;
- constructor injection;
- composition root;
- DI versus service locator;
- provider/factory guide;
- scope/lifetime/owner table;
- Android owner mapping;
- ViewModel and navigation graph scope;
- qualifiers;
- multibinding;
- assisted injection;
- Context rules;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Replace service locator

Refactor a screen/ViewModel that pulls Repository and Analytics from a global object.

Require:

- explicit constructor dependencies;
- composition root;
- test replacement;
- no container access from business code.

### Exercise 2 — Scope audit

Given a graph containing API client, Repository, session state, screen presenter, formatter, and Activity Context, choose scopes.

Require:

- owner for each dependency;
- creation and destruction boundary;
- leak analysis;
- justification for unscoped objects.

### Exercise 3 — Navigation graph feature

Design DI ownership for a multi-screen checkout flow.

Require:

- graph-scoped state;
- destination-scoped state;
- runtime order ID;
- ViewModel factories or assisted injection;
- cleanup when graph is removed.

### Exercise 4 — Test isolation

Repair tests that mutate a singleton dependency and fail depending on execution order.

Require:

- replacement strategy;
- graph reset;
- fake dependencies;
- parallel-test safety.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

Do not provide complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 20–24 substantial questions.

Cover:

- DI;
- dependency inversion;
- constructor injection;
- composition root;
- object graph;
- service locator;
- manual DI;
- provider/factory;
- scope;
- application scope;
- Activity/Fragment scope;
- ViewModel scope;
- navigation graph scope;
- qualifiers;
- multibinding;
- assisted injection;
- Context;
- cycles;
- testing;
- framework isolation;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where useful.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. constructor injection;
2. DI versus service locator;
3. composition root;
4. scope ownership;
5. application versus Activity lifetime;
6. ViewModel/navigation graph scope;
7. qualifier use;
8. assisted injection;
9. Context leak;
10. test replacement and singleton isolation.

Distractors must be plausible.

Explanations must teach object ownership and lifetime.

---

## References

Use current primary sources.

At minimum inspect:

- Android dependency injection guidance;
- Hilt component hierarchy;
- Hilt scopes;
- ViewModel injection;
- navigation graph scoped ViewModels;
- qualifiers;
- multibinding;
- assisted injection where referenced;
- testing overrides.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 12 of 17.

The implementation report must record:

```text
Junior Core status after Task 024:
12 of 17 mandatory topics implemented as production packages in review.
5 mandatory topics remain.
```

Remaining mandatory topics:

13. Android Testing Foundations
14. Android Security Foundations
15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

Do not define the Junior/Middle boundary yet.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 024 after successful validation;
- record twelve production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that five topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. DI and composition-root audit;
5. scope/lifetime/owner audit;
6. Android component scope audit;
7. qualifier/multibinding/assisted-injection audit;
8. Context and leak audit;
9. testing and replacement audit;
10. Junior Core progress audit;
11. exact counts;
12. validation;
13. UTF-8/mojibake audit;
14. deferred work;
15. literal `git status --short`;
16. recommended commit message.

---

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Also verify:

- exactly six package files;
- exactly four exercises;
- exactly ten tests;
- interview count in range;
- schema-valid taxonomy;
- prerequisites exist;
- no prerequisite cycle;
- no changes to existing topic packages;
- no source, competency, sequence, mapping, schema, validator, or test-infrastructure changes;
- UTF-8;
- no mojibake;
- no local absolute paths.

---

## Acceptance criteria

- Six-file package exists.
- Status is `review`.
- Content version is `1`.
- DI is explained as graph construction and ownership.
- Constructor injection is the default.
- Composition root is explicit.
- DI and service locator are distinguished.
- Scope is defined as lifetime plus owner.
- Android scopes are mapped correctly.
- ViewModel and navigation graph scope are accurate.
- Qualifiers, multibinding, and assisted injection are covered.
- Context rules prevent leaks.
- Framework types stay out of Domain.
- Testing replacement is explicit.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 12/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. DI/composition-root audit;
5. scope/lifetime audit;
6. Android scope audit;
7. qualifiers/multibinding/assisted-injection audit;
8. testing audit;
9. Junior Core progress;
10. exact counts;
11. validation results;
12. UTF-8 audit;
13. deferred work;
14. literal `git status --short`;
15. recommended commit message.

Do not commit.
