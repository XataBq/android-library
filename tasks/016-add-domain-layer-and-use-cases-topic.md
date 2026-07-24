# Task 016 — Add Android Domain Layer and Use Cases Topic

Status: DONE

## Objective

Add the fourth production educational topic in the Android app architecture foundation:

```text
android-domain-layer-and-use-cases
```

The topic must explain the optional Android Domain layer and the use-case/interactor pattern without turning either into a universal architectural requirement.

The topic must remain grounded in the repository's current canonical competency model and the reviewed source evidence. It should teach learners how to decide whether a Domain layer is justified, how to assign responsibilities to use cases, and how the Domain layer interacts with UI and Data layers.

This task belongs to:

```text
Phase 3 — Learning Content MVP
```

It extends the current three-topic foundation:

1. `android-app-architecture-foundations`
2. `android-ui-layer-and-unidirectional-data-flow`
3. `android-data-layer-repositories-and-synchronization`
4. `android-domain-layer-and-use-cases`

The new topic must remain in `review`.

---

## Product and editorial intent

The topic should prevent two common mistakes:

1. adding a Domain layer mechanically to every application;
2. placing unrelated business logic into large generic use-case classes.

The learner should leave with a responsibility-first decision model:

```text
Is the logic complex?
Is it reused by multiple state holders?
Does it coordinate multiple repositories?
Does extracting it improve ownership and testability?
```

If the answer is no, the logic may remain in the UI state holder or Data layer according to its actual responsibility.

The topic must not present Clean Architecture, use cases, interactors, or a three-layer structure as mandatory for every Android project.

---

## Source-of-truth requirements

Before authoring, inspect:

- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_AUTHORING.md` if present
- `docs/CONTENT_VALIDATION.md`
- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`
- `competencies/normalized/android-app-architecture/competency-set.yaml`
- `competencies/normalized/android-app-architecture/competencies.yaml`
- both imported Android Developers source packages;
- all review and normalization records relevant to:
  - `evaluate-optional-domain-layer`;
  - repository boundaries;
  - UI state holders;
  - layer-specific models;
  - coroutines and flows across layers.

Also inspect all three existing production topic packages to preserve repository style and avoid duplication.

The repository files are the primary source of truth.

Do not silently add claims that are unsupported by the imported evidence or cited references.

When broader explanatory material is needed, use clearly cited official Android documentation and keep it consistent with the repository's canonical competency wording.

---

## Canonical competency scope

The primary canonical competency is:

```text
evaluate-optional-domain-layer
```

Canonical outcome:

```text
Evaluate whether an optional domain layer is justified by complex logic or
logic reused across multiple state holders.
```

The topic may also reinforce, without redefining:

- `apply-separation-of-concerns`;
- `explain-ui-layer-responsibilities`;
- `design-data-layer-around-repositories`;
- `explain-repository-responsibilities`;
- `use-coroutines-and-flows-across-layers`;
- `evaluate-layer-specific-models`.

Do not invent new canonical competencies.

Do not modify competency files.

Do not create a production competency-to-topic mapping in this task.

---

## Package location

Create exactly:

```text
content/android/app-architecture/android-domain-layer-and-use-cases/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional files may be added inside the topic package.

---

## Topic metadata

Use:

```yaml
id: android-domain-layer-and-use-cases
title: Android Domain Layer and Use Cases
track: android
section: app-architecture
difficulty: foundation
status: review
content_version: 1
```

Recommended:

```yaml
estimated_minutes: 120
```

Prerequisites must be:

```yaml
prerequisites:
  - android-app-architecture-foundations
  - android-ui-layer-and-unidirectional-data-flow
  - android-data-layer-repositories-and-synchronization
```

The final metadata must conform to the current schema and repository conventions.

---

## Required learning outcomes

The final topic must cover outcomes equivalent to:

1. Explain the purpose and boundaries of an optional Domain layer.
2. Decide when a Domain layer is justified and when it adds unnecessary indirection.
3. Distinguish UI logic, application/domain logic, and Data-layer responsibilities.
4. Explain the responsibility of a use case or interactor.
5. Design focused use cases around one coherent user or application operation.
6. Compose multiple repositories without exposing data-source details.
7. Keep use cases independent from Android framework types and UI lifecycle.
8. Model inputs, outputs, and failures at an appropriate boundary.
9. Evaluate when logic should remain in a ViewModel, repository, or use case.
10. Test Domain-layer logic without Android framework dependencies.
11. Recognize oversized, pass-through, duplicated, and infrastructure-leaking use cases.
12. Explain how coroutines and flows cross Domain boundaries without making the Domain layer own UI lifecycle.

Wording may be adjusted to match the topic schema and source support.

Do not add outcomes that the actual sources do not support.

---

## Theory requirements

`theory.md` must be a coherent responsibility-first guide, not a list of architecture slogans.

It should contain approximately 14–18 substantial sections.

Required conceptual coverage follows.

### 1. Why the Domain layer is optional

Explain:

- UI and Data layers are the core baseline;
- a Domain layer is introduced only when it owns meaningful application logic;
- the decision depends on complexity and reuse;
- more layers do not automatically mean better architecture.

### 2. Three categories of logic

Provide a practical distinction among:

#### UI logic

Examples:

- visibility;
- formatting for presentation;
- transient UI decisions;
- screen-local interaction state.

#### Application or domain logic

Examples:

- rules that describe an application operation;
- coordination across repositories;
- calculations or decisions reused by multiple state holders;
- workflows independent from rendering and storage APIs.

#### Data logic

Examples:

- data ownership;
- synchronization;
- source selection;
- cache and persistence policies;
- repository-level conflict handling.

Clarify that the exact boundary depends on responsibility, not class names.

### 3. Decision framework for adding a Domain layer

Give an explicit evaluation checklist.

A Domain layer is more likely justified when:

- logic is reused by multiple ViewModels or state holders;
- a user operation coordinates multiple repositories;
- business rules are complex enough to obscure UI-state production;
- logic needs independent testing;
- the operation represents a stable application capability.

It may be unnecessary when:

- the operation is a trivial repository pass-through;
- logic is screen-specific;
- extraction adds only forwarding classes;
- no meaningful domain policy exists.

### 4. Use case / interactor responsibility

Explain that one use case should represent one coherent operation or capability.

Examples may include:

- observe a user dashboard assembled from multiple repositories;
- submit an order after validation;
- update a profile under application rules;
- calculate eligibility;
- synchronize a user-requested workflow.

Avoid domain examples that imply unsupported Android-specific mandates.

### 5. Inputs and outputs

Explain how to choose:

- constructor dependencies;
- operation parameters;
- return types;
- streams versus one-shot results;
- domain-specific result models;
- failure representation.

Do not prescribe a universal `Result` wrapper.

### 6. Repository interaction

Explain:

- use cases depend on repository abstractions or stable Data-layer APIs;
- use cases do not access Retrofit, Room DAOs, files, or platform data sources directly;
- repositories retain data ownership and source coordination;
- a use case may coordinate several repositories without taking over their responsibilities.

### 7. Coroutines and flows

Explain:

- suspending work can model one-shot actions;
- Flow can model observable application data;
- the caller owns UI lifecycle collection;
- a use case should not retain Activity, Fragment, Context, or Compose lifecycle state;
- cancellation should follow structured caller scope rather than hidden unmanaged work.

Only include API-specific claims supported by repository sources or cited official references.

### 8. Framework independence

Explain why Domain code should normally avoid:

- Activity;
- Fragment;
- View;
- Context;
- Resources;
- Android lifecycle ownership.

Distinguish legitimate boundary abstractions from leaking Android implementation details.

### 9. Models across boundaries

Explain that a separate Domain model is conditional.

Use the existing canonical principle:

```text
Evaluate layer-specific models when application complexity and consumer needs
justify them.
```

Do not state that every layer requires a separate model.

### 10. ViewModel versus use case

Provide a decision table or equivalent comparison.

A ViewModel may own:

- screen state;
- UI actions;
- presentation decisions;
- screen-specific orchestration.

A use case may own:

- reusable application rules;
- multi-repository coordination;
- stable operations independent of one screen;
- logic whose testing and ownership benefit from extraction.

### 11. Repository versus use case

Explain:

- repository owns application data and data operations;
- use case owns an application operation or rule;
- a repository should not become a generic dumping ground;
- a use case should not replace repository data ownership.

### 12. Dependency direction

Show a simple conceptual dependency direction:

```text
UI → Domain → Data contracts / repositories
```

Clarify:

- this is a conceptual boundary;
- package/module direction depends on the implementation;
- the repository's existing architecture contracts remain authoritative;
- circular dependencies are not acceptable.

Do not turn this into a mandatory multi-module structure.

### 13. Testing

Include focused examples of:

- testing pure rules;
- testing repository coordination with fakes;
- testing success and failure;
- testing flows or suspending operations;
- avoiding Android framework dependencies in unit tests.

### 14. Common failure modes

At minimum:

- use case for every repository method;
- pass-through use cases with no policy;
- giant `AppUseCases` container;
- one use case with many unrelated operations;
- Android `Context` in Domain logic;
- direct DAO or Retrofit access;
- duplicated logic across ViewModels and use cases;
- Domain models copied mechanically;
- swallowing errors;
- hidden background scopes;
- use cases that own UI state or navigation.

### 15. Worked example

Include at least one end-to-end example that demonstrates:

```text
UI action
→ ViewModel
→ focused use case
→ one or more repositories
→ updated state
```

The example must show responsibility boundaries and failure/cancellation behavior.

Use Kotlin examples that are realistic but not tied to a specific DI framework.

### 16. Decision summary

End with a compact decision process that a learner can apply to a real feature.

---

## Kotlin example requirements

Examples must:

- compile conceptually;
- use idiomatic Kotlin;
- use interfaces or stable abstractions where appropriate;
- avoid fake Android framework ownership;
- avoid global coroutine scopes;
- avoid unnecessary inheritance;
- avoid universal wrapper abstractions;
- show focused constructor dependencies;
- show clear caller ownership.

Examples should include at least:

1. a focused suspending use case;
2. a Flow-returning use case or query;
3. a multi-repository coordination example;
4. a counterexample showing unnecessary pass-through;
5. a unit-test example with fakes.

Do not introduce Hilt-specific implementation unless used only as an optional Android connection and supported by references.

---

## Cheat-sheet requirements

`cheat-sheet.md` must provide a concise review artifact containing:

- when to add a Domain layer;
- when not to add it;
- UI versus Domain versus Data responsibilities;
- use-case design checklist;
- dependency rules;
- coroutine/Flow boundary rules;
- testing checklist;
- common smells;
- interview-ready summary.

It must be usable independently from the full theory.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Responsibility classification

Classify a set of realistic logic examples as:

- UI;
- Domain/application;
- Data;
- ambiguous and requiring context.

Require justification.

### Exercise 2 — Extract or keep

Given a ViewModel and repository scenario, decide which logic should:

- remain in the ViewModel;
- remain in the repository;
- move to a use case.

Require a written responsibility analysis before code.

### Exercise 3 — Multi-repository use case

Design and implement a focused use case that coordinates at least two repository abstractions.

Require:

- inputs;
- output;
- failure behavior;
- cancellation behavior;
- tests with fakes.

### Exercise 4 — Architecture review

Review a deliberately flawed Domain layer containing:

- pass-through use cases;
- direct DAO or Retrofit dependency;
- Android Context;
- unrelated operations;
- hidden coroutine scope.

Require a corrected design and explanation.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints separated from the main solution path.

Do not include complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 15–20 questions.

It must cover:

- why the Domain layer is optional;
- when to add it;
- use cases versus repositories;
- use cases versus ViewModels;
- dependency direction;
- repository coordination;
- Flow and suspend boundaries;
- failure handling;
- framework independence;
- layer-specific models;
- testing;
- common anti-patterns;
- practical feature design;
- trade-offs in small versus large applications.

For each question include:

- what a strong answer should cover;
- common weak or misleading answers;
- at least one follow-up where appropriate.

Avoid treating terminology such as “Clean Architecture” as proof of understanding.

---

## Test requirements

`test.yaml` must contain exactly 10 questions.

Use a balanced mix allowed by the current schema.

The questions must test reasoning, not vocabulary recall.

Required coverage:

1. optionality of the Domain layer;
2. classification of UI/Domain/Data responsibility;
3. pass-through use-case smell;
4. repository versus use-case ownership;
5. multi-repository coordination;
6. Flow/suspend boundary;
7. framework dependency leak;
8. layer-specific model trade-off;
9. testing strategy;
10. architecture scenario with best placement decision.

Distractors must be plausible.

Explanations must teach why the answer is correct.

---

## References

Use official and repository-supported references.

At minimum inspect and use, when supported by current repository conventions:

- Guide to app architecture;
- Domain layer;
- Recommendations for Android architecture;
- Data layer;
- UI layer.

Use the actual current URLs already present in repository sources or existing topic references.

Do not fabricate access dates.

Follow the repository's established reference metadata convention.

Do not cite secondary blogs unless the repository explicitly permits and the source adds necessary value.

---

## Android connections

The topic metadata should include Android-specific connections equivalent to:

- Domain code can isolate reusable application rules from Android UI lifecycle.
- ViewModels may call use cases while continuing to own screen UI state.
- Use cases may coordinate repositories without accessing Room, Retrofit, or platform APIs directly.
- Coroutines and Flow can cross the boundary while lifecycle collection remains in UI-owned scopes.

Final wording must remain source-supported.

---

## Relationship to existing topics

The new topic must not duplicate the three existing topics.

Assume learners already understand:

- architecture foundations;
- UI layer and UDF;
- Data layer, repositories, SSOT, and synchronization.

Briefly recap only what is needed to explain Domain boundaries.

Use links to prerequisite topics where repository conventions support them.

The topic should deepen architecture composition, not repeat repository or ViewModel theory in full.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required state changes:

- record Task 016 as completed only after validation;
- record the fourth production topic in `review`;
- keep Phase 3 current;
- state that four production topics now form the growing Android architecture content foundation;
- do not claim that 10–15 topics are complete;
- do not claim production mappings exist;
- do not create a generated catalog;
- do not promote any existing topic;
- preserve Phase 2 completion from Task 015 if present in the current repository.

Update `docs/ARCHITECTURE.md` only if a current list of production topics would otherwise become stale.

---

## Implementation report

Create the repository-standard implementation report, likely under:

```text
docs/reports/
```

Use actual repository naming conventions.

The report must include:

1. implementation summary;
2. files created and changed;
3. source and evidence audit;
4. canonical competency coverage;
5. prerequisite and duplication audit;
6. theory coverage audit;
7. exercise count;
8. interview-question count;
9. test-question count;
10. metadata and reference audit;
11. validation results;
12. UTF-8 and mojibake audit;
13. deferred work;
14. literal `git status --short`;
15. recommended commit message.

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

- exactly six files exist in the new topic package;
- `practice.md` contains exactly 4 exercises;
- `test.yaml` contains exactly 10 questions;
- topic ID and directory match;
- prerequisite IDs exist;
- no prerequisite cycle is introduced;
- all references are valid;
- all new files are UTF-8;
- no mojibake;
- no absolute local paths;
- no competency, source, sequence, mapping, schema, validator, or existing-topic data changed;
- no package status changed outside the new topic;
- only allowed documentation and report files changed.

---

## Acceptance criteria

- The new six-file topic package exists.
- Metadata conforms to schema.
- Status is `review`.
- Content version is `1`.
- All three current architecture topics are prerequisites.
- The topic is grounded in the optional Domain-layer competency.
- The Domain layer is not presented as mandatory.
- Use cases have focused responsibilities.
- ViewModel, use-case, repository, and data-source boundaries are distinguished.
- Coroutines and Flow are explained without lifecycle leakage.
- Framework independence is explicit.
- Layer-specific models remain conditional.
- Theory includes realistic Kotlin examples and a worked flow.
- Cheat sheet is independently useful.
- Practice has exactly 4 exercises.
- Interview material is substantial.
- Test has exactly 10 reasoning-focused questions.
- Existing topics are not substantially duplicated.
- Project documentation is synchronized.
- All validation commands pass.
- Task becomes `DONE` only after validation succeeds.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source and evidence audit;
4. canonical coverage;
5. content and duplication audit;
6. exact counts for theory sections, exercises, interview questions, and tests;
7. validation results;
8. UTF-8 audit;
9. deferred work;
10. literal `git status --short`;
11. recommended commit message.

Do not commit.
