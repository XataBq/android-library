# Task 022 — Add Android Navigation Architecture Topic

Status: DONE

## Objective

Add the tenth production educational topic in the Junior Core:

```text
android-navigation-architecture
```

The topic must explain Android navigation as a stateful architecture concern rather than a collection of `navigate()` calls.

The learner must understand:

- destinations and routes;
- navigation ownership;
- back stack;
- navigation graph;
- arguments;
- deep links;
- nested graphs;
- scoped ViewModels;
- returning results;
- multiple back stacks;
- state restoration;
- navigation events;
- testing;
- security and exported entry points.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds on:

- Architecture Foundations;
- UI Layer and UDF;
- ViewModel and UI State;
- Lifecycle and State Restoration;
- Kotlin Coroutines Foundations;
- Kotlin Flow and Reactive Streams.

---

## Core teaching position

Navigation is not business logic and not raw UI mutation.

The core model is:

```text
UI action
→ ViewModel decides intent/eligibility where needed
→ UI/navigation owner performs navigation
→ back stack becomes the source of navigation state
```

The topic must preserve these distinctions:

```text
Navigation state
≠ screen UI state
≠ durable application state
≠ one-off event delivery
```

A ViewModel may expose a navigation intent or effect, but it must not own:

- Activity;
- Fragment;
- NavController;
- composable runtime navigation objects;
- Android View references.

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
- all production topic packages;
- Tasks 017, 018, 019, 020, and 021.

Use current official Android documentation for:

- Navigation component;
- Navigation Compose;
- deep links;
- multiple back stacks;
- saved state;
- nested graphs;
- testing;
- type-safe routes where current official APIs support them.

Do not invent undocumented back-stack behavior.

Do not fabricate access dates.

---

## Canonical competency scope

Primary:

```text
explain-ui-layer-responsibilities
explain-android-component-lifecycle-constraints
design-viewmodel-ui-state
```

Strongly reinforced:

```text
explain-unidirectional-data-flow
select-ui-state-holders-by-scope
handle-compose-lifecycle-work
isolate-android-framework-dependencies
```

Contextually reinforced:

```text
apply-separation-of-concerns
use-coroutines-and-flows-across-layers
explain-persistent-data-models
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/navigation/android-navigation-architecture/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: navigation` is invalid, adapt using repository conventions and document the choice.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-navigation-architecture
title: Android Navigation Architecture
track: android
section: navigation
difficulty: foundation
status: review
estimated_minutes: 210
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-ui-layer-and-unidirectional-data-flow
  - android-viewmodel-and-ui-state
  - android-lifecycle-and-state-restoration
  - kotlin-flow-and-reactive-streams
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain navigation as back-stack state.
2. Distinguish destination, route, graph, and back-stack entry.
3. Explain who owns navigation.
4. Keep NavController out of ViewModel.
5. Design navigation intents/effects without duplicating navigation state.
6. Pass minimal arguments.
7. Prefer IDs over large objects.
8. Use typed arguments where supported.
9. Explain nested graphs and graph-scoped ownership.
10. Explain destination-scoped and graph-scoped ViewModels.
11. Handle up, back, and top-level navigation correctly.
12. Explain `popUpTo`, `inclusive`, `launchSingleTop`, and state restoration.
13. Explain multiple back stacks.
14. Handle navigation results.
15. Compare Fragment Result API, saved-state result, shared ViewModel, and callback patterns.
16. Explain deep links and app links.
17. Explain exported entry-point risks.
18. Restore navigation state after recreation.
19. Test navigation independently from screen rendering.
20. Recognize navigation anti-patterns.

---

## Theory requirements

`theory.md` must contain approximately 20–24 substantial sections.

Required coverage:

### 1. Navigation is state

Explain the back stack as the current navigation state.

### 2. Destinations, routes, graphs, entries

Define:

- destination;
- route;
- graph;
- back-stack entry;
- current destination.

### 3. Navigation owner

Explain:

- UI/navigation host owns NavController;
- ViewModel exposes intent or effect only when needed;
- business rules can decide whether navigation is allowed;
- actual navigation remains framework-owned.

### 4. Back stack semantics

Cover:

- push;
- pop;
- replace-like behavior;
- top entry;
- process recreation;
- owner lifecycle.

### 5. `navigateUp()` versus system Back

Explain conceptual differences and hierarchy behavior.

### 6. Arguments

Explain:

- route inputs;
- small serializable values;
- IDs over large objects;
- durable data reload through Repository;
- avoiding mutable object transfer.

### 7. Type-safe navigation

Cover current official type-safe route APIs where supported.

Clearly mark version requirements or API maturity where relevant.

Avoid pretending all projects use the same API style.

### 8. Navigation state versus screen state

Explain what belongs in:

- back stack;
- SavedStateHandle;
- ViewModel;
- Repository;
- UI state.

### 9. Navigation events

Compare:

- direct UI callback;
- ViewModel effect;
- state-driven navigation;
- event stream.

Explain risks:

- duplicate navigation after recreation;
- stale effects;
- event loss;
- treating navigation as durable state.

### 10. One-off navigation effects

Explain delivery policies without prescribing one universal event wrapper.

### 11. `popUpTo`, `inclusive`, `launchSingleTop`

Use concrete scenarios:

- login flow;
- top-level tab;
- duplicate destination avoidance;
- clearing onboarding.

### 12. Nested graphs

Explain:

- feature boundaries;
- auth flow;
- graph-scoped state;
- encapsulation;
- not treating graphs as business modules automatically.

### 13. ViewModel scope

Explain:

- destination scope;
- graph scope;
- Activity scope;
- shared ViewModel trade-offs;
- lifecycle of each owner.

### 14. Multiple back stacks

Cover bottom navigation/top-level destinations:

- independent history;
- save/restore state;
- reselect behavior;
- duplicate stacks;
- memory implications at a high level.

### 15. Navigation results

Compare:

- previous back-stack entry saved-state result;
- Fragment Result API;
- shared ViewModel;
- direct callback;
- repository-mediated durable result.

Explain lifecycle and ownership.

### 16. Deep links

Explain:

- explicit deep link;
- implicit deep link;
- route reconstruction;
- argument validation;
- missing prerequisites;
- auth gates;
- unsupported routes.

### 17. App links and external entry points

Explain:

- verified app links;
- exported Activity;
- intent filters;
- untrusted input;
- authorization after entry;
- route validation.

### 18. Security

Cover:

- exported destinations;
- deep-link parameter tampering;
- privilege checks;
- internal-only screens;
- sensitive data in URLs;
- pending intent/deep-link assumptions;
- navigation not replacing authorization.

### 19. State restoration

Explain:

- process recreation;
- back-stack restoration;
- destination state;
- SavedStateHandle;
- Repository reload;
- limitations.

### 20. Compose and Fragment navigation boundaries

Compare architectural ownership, not API syntax only.

### 21. Testing

Cover:

- fake/test navigator abstraction where useful;
- NavHostController tests;
- graph tests;
- destination assertions;
- deep-link tests;
- result tests;
- back-stack tests;
- avoiding UI screenshot dependence for navigation logic.

### 22. Anti-patterns

At minimum:

- NavController in ViewModel;
- Context-based navigation from Repository;
- passing whole entities;
- global singleton navigator;
- navigation from Domain layer;
- duplicate events after recreation;
- deep links without validation;
- huge navigation graphs without feature boundaries;
- every destination sharing one Activity ViewModel;
- overusing shared ViewModel for results;
- hardcoded route strings everywhere;
- ignoring back-stack semantics;
- rebuilding navigation state separately in UiState;
- assuming destination removal equals configuration change.

### 23. Decision guide

End with:

```text
Who owns navigation?
What must be on the back stack?
What input is minimal?
What scope owns state?
Can this entry come from outside?
How is result returned?
What happens after recreation?
How is it tested?
```

---

## Kotlin example requirements

Include at least:

1. UI-owned NavController with callback;
2. ViewModel navigation intent without NavController;
3. typed route or schema-safe argument example;
4. ID-based argument loading;
5. `popUpTo`;
6. `launchSingleTop`;
7. nested graph;
8. destination-scoped ViewModel;
9. graph-scoped ViewModel;
10. multiple back-stack setup;
11. navigation result via saved-state handle;
12. Fragment Result API comparison example;
13. deep-link validation;
14. external entry authorization;
15. navigation test;
16. duplicate-event anti-pattern and correction.

Examples must be conceptually compilable and version-aware.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- route/destination/graph/back-stack definitions;
- ownership rules;
- arguments checklist;
- state placement;
- navigation effects;
- `popUpTo`/`inclusive`/`launchSingleTop`;
- ViewModel scope guide;
- nested graphs;
- multiple back stacks;
- results comparison;
- deep links;
- security checklist;
- restoration checklist;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Navigation ownership

Refactor a ViewModel that holds NavController and calls navigation directly.

Require:

- explicit UI-owned navigation;
- testable navigation intent;
- duplicate-event policy;
- recreation behavior.

### Exercise 2 — Authentication graph

Design login/onboarding/main graphs.

Require:

- clear stack-clearing rules;
- `popUpTo`;
- auth gating;
- deep-link behavior;
- process recreation.

### Exercise 3 — Bottom navigation

Design three top-level destinations with multiple back stacks.

Require:

- state restore;
- reselect policy;
- no duplicate roots;
- tests.

### Exercise 4 — Deep-link security review

Review an exported deep link that opens a sensitive destination using URL parameters.

Require:

- input validation;
- authorization;
- safe fallback;
- minimal arguments;
- tests.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

Do not provide full solutions.

---

## Interview requirements

`interview.md` must contain approximately 20–24 substantial questions.

Cover:

- navigation ownership;
- back stack;
- destination/route/graph;
- arguments;
- typed routes;
- SavedStateHandle;
- navigation effects;
- duplicate navigation;
- nested graphs;
- ViewModel scopes;
- top-level navigation;
- `popUpTo`;
- `launchSingleTop`;
- multiple back stacks;
- results;
- deep links;
- app links;
- exported components;
- authorization;
- restoration;
- Compose vs Fragment navigation;
- testing;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where useful.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. navigation ownership;
2. back-stack semantics;
3. argument design;
4. ViewModel scope;
5. `popUpTo` and stack clearing;
6. multiple back stacks;
7. result delivery;
8. deep-link validation;
9. exported entry authorization;
10. process recreation and navigation restoration.

Distractors must be plausible.

Explanations must teach architecture, not memorized API calls.

---

## References

Use official Android references.

At minimum inspect:

- Navigation overview;
- Navigation Compose;
- type-safe routes;
- nested graphs;
- multiple back stacks;
- deep links;
- app links;
- testing navigation;
- saved state;
- Fragment Result API;
- exported components and intent filters.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 10 of 17.

The implementation report must record:

```text
Junior Core status after Task 022:
10 of 17 mandatory topics implemented as production packages in review.
7 mandatory topics remain.
```

Remaining mandatory topics:

11. Android Networking Architecture
12. Dependency Injection and Scoping
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

- record Task 022 after successful validation;
- record ten production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that seven topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. navigation ownership audit;
5. back-stack and scope audit;
6. arguments and result audit;
7. deep-link and security audit;
8. restoration audit;
9. testing audit;
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
- Navigation is taught as back-stack state.
- UI owns framework navigation.
- NavController is not stored in ViewModel.
- Minimal argument design is clear.
- Nested graphs and scope are correct.
- Multiple back stacks are covered.
- Results are compared by ownership.
- Deep links and external entry points are validated.
- Authorization remains separate from navigation.
- Restoration behavior is accurate.
- Testing is architecture-focused.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 10/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. ownership/back-stack audit;
5. arguments/results audit;
6. deep-link/security audit;
7. restoration/testing audit;
8. Junior Core progress;
9. exact counts;
10. validation results;
11. UTF-8 audit;
12. deferred work;
13. literal `git status --short`;
14. recommended commit message.

Do not commit.
