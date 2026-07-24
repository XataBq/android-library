# Android Dependency Injection and Scoping — Practice

Each exercise requires an ownership explanation, representative Kotlin, and
focused tests. Do not provide a complete production implementation.

## Exercise 1 — Replace a service locator

### Goal

Make a screen's graph explicit and independently testable.

### Scenario

`OrdersViewModel` pulls `OrderRepository`, `Analytics`, and `Clock` from
`GlobalServices`. Tests replace global entries and fail when executed in a
different order.

### Constraints

- Move every required collaborator to constructor parameters.
- Keep Repository and Domain contracts free from container APIs.
- Define an application or feature composition root.
- Decide which objects are reused and which are unscoped.
- Provide direct fake replacements in the ViewModel/use-case unit tests.
- Do not pass the container or `Application` into business code.

### Expected deliverable

- before/after dependency graph;
- constructors and composition-root wiring;
- owner and lifetime table;
- isolated tests that require no global reset.

### Evaluation criteria

- the public construction contract shows every required dependency;
- implementation selection exists only at composition boundaries;
- unit tests own fresh fakes;
- no service lookup remains below the entry layer.

### Optional hints

- A constructor that grows may reveal more than one responsibility.
- A provider parameter is still explicit, but its identity contract needs
  documentation.

## Exercise 2 — Audit scopes and leaks

### Goal

Choose the narrowest correct owner for each object.

### Scenario

One graph contains an HTTP client, repository, mutable session state, screen
presenter, stateless formatter, analytics sink, and Activity Context. A proposed
module marks every binding singleton.

### Constraints

- Name owner, creation, reuse, and destruction boundaries for every object.
- Distinguish Application, Activity-retained, Activity, Fragment/View, and
  ViewModel lifetimes.
- Justify every scoped binding and every unscoped binding.
- Explain process death and account logout separately.
- Locate Context and UI-object leaks.
- State thread-safety/reset policy for shared mutable state.

### Expected deliverable

- scope matrix with rationale;
- graph diagram across configuration change and process death;
- leak findings and corrected dependencies;
- tests for identity within and across owner instances.

### Evaluation criteria

- `@Singleton` is not treated as persistent or immortal;
- Activity Context never enters process scope;
- stateless cheap objects may remain unscoped;
- session lifetime and process lifetime are not conflated.

### Optional hints

- Ask whether shared identity is required for correctness.
- Fragment scope can be longer than Fragment View scope.

## Exercise 3 — Own a navigation checkout graph

### Goal

Design DI and ViewModel ownership for a multi-screen checkout workflow.

### Scenario

Address, payment, and confirmation share a checkout draft. Each destination
also has local presentation state. An order ID arrives at runtime, and all flow
objects must clear when the checkout graph is popped.

### Constraints

- Select graph-entry and destination ViewModel owners.
- Separate durable repository data from workflow presentation state.
- Choose `SavedStateHandle` or assisted input for the order ID and justify
  restoration semantics.
- Define factories or Hilt ViewModel creation using the installed API version.
- Do not invent a generic Hilt navigation-graph component scope.
- Do not inject `NavController`, Fragment, Activity, or View into ViewModel.

### Expected deliverable

- navigation-entry/object-graph diagram;
- owner and destruction table;
- ViewModel/factory boundary signatures;
- tests for sharing, destination isolation, graph pop, and recreation.

### Evaluation criteria

- shared workflow state has exactly one graph owner;
- destination-local objects are not over-scoped;
- runtime input and restored input are distinguished;
- popping the graph releases workflow state.

### Optional hints

- A graph-scoped ViewModel can be the workflow owner.
- Assisted values do not automatically become saved state.

## Exercise 4 — Restore test isolation

### Goal

Repair integration tests that mutate production singletons.

### Scenario

Tests replace a process-global repository and clock, reuse one mutable fake, and
sometimes observe calls from another parallel test. Cleanup runs only after a
successful test.

### Constraints

- Use constructor replacement for unit tests.
- Define test component/module override for integration tests.
- Match production qualifiers without importing production mutable state.
- Give every test a new scoped graph and fake instances.
- Ensure destruction/reset runs after failure.
- Analyze parallel execution.
- Mark Hilt test APIs as version-sensitive.

### Expected deliverable

- failure timeline for current tests;
- unit and integration replacement strategies;
- graph setup/teardown lifecycle;
- deterministic sequential and parallel isolation tests.

### Evaluation criteria

- no test mutates a production singleton;
- graph and fake ownership belong to one test;
- cleanup is unconditional;
- test order and parallelism do not change results.

### Optional hints

- Prefer `@TestInstallIn` for shared Hilt test replacement and direct
  construction for units, subject to installed-version verification.
- Replacing a binding and resetting its mutable instance are separate concerns.
