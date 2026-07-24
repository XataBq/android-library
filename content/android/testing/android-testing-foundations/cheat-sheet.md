# Android Testing Foundations — Cheat Sheet

## Core model

```text
architecture defines boundaries
boundaries define test seams
each test owns one risk
prefer the smallest reliable test
use higher-level tests for integration and user-observable behavior
```

A test is valuable when it identifies the regression it prevents and observes
a stable contract.

## Test-boundary matrix

| Boundary | Typical subject | Real parts | Primary trade-off |
| --- | --- | --- | --- |
| unit | function/class | subject only | fastest, least integration realism |
| integration | cooperating units/adapters | selected boundaries | contract fidelity |
| component | feature slice | most feature parts | broader diagnosis |
| UI | rendered screen | UI toolkit | user-visible interaction |
| end-to-end | critical workflow | most system wiring | highest cost and realism |

Local versus instrumented describes execution environment. It does not define
scope:

```text
unit ≠ local
integration ≠ instrumentation
UI ≠ end-to-end
```

Always document what is real, replaced, and observed.

## Smallest-reliable-test rule

```text
failure to catch
→ behavior required
→ smallest boundary containing it
→ controlled dependencies
→ public observation
```

- Mapper rule: local unit test.
- Repository coordination: repository plus fake sources.
- HTTP encoding: real client adapter plus mock server.
- SQL query: real Room/SQLite boundary.
- Route intent: callback/fake navigator.
- Back-stack behavior: test navigation controller or UI host.
- Screen semantics: Compose or Espresso UI test.

## Test portfolio

- Many fast, focused tests for rules and transitions.
- Fewer integration tests for real boundaries.
- Few end-to-end tests for critical wiring and journeys.
- Add specialized accessibility, compatibility, performance, and visual tests
  for their own risks.

The pyramid is guidance, not a quota. Optimize confidence, speed, diagnostics,
and maintenance together.

## Arrange–Act–Assert

```text
Arrange: subject, dependencies, precondition
Act: one behavior
Assert: one coherent public outcome
```

Given–When–Then is equivalent. Split unrelated scenarios.

## What to observe

| Observation | Use when |
| --- | --- |
| returned value/state | result is the contract |
| emitted state/effect | stream delivery is the contract |
| collaborator interaction | the interaction itself matters |
| rendered semantics | user-visible behavior matters |
| persisted/network request | adapter contract matters |

Prefer public behavior. Do not verify every internal call or private method.

## Test-double glossary

| Double | Purpose |
| --- | --- |
| dummy | satisfies an unused parameter |
| stub | returns programmed answers |
| fake | lightweight working implementation |
| spy | records observations, possibly delegates |
| mock | enforces programmed interactions |

Definitions differ between tools. State the behavior you rely on.

### Fake versus mock

Prefer a fake for:

- stateful repository behavior;
- cache reads/writes;
- controlled Flow emissions;
- navigation history;
- multiple coherent operations.

Consider interaction verification for:

- audit delivery;
- destructive boundary calls;
- externally meaningful “exactly once” behavior.

Do not verify calls that only describe the current implementation.

## Testability checklist

- Constructor dependencies are explicit.
- Clocks, randomness, IDs, dispatchers, and external sources are controllable.
- Mappers/reducers/rules are pure where practical.
- Repository and platform boundaries are narrow.
- Coroutine work has an owner and observable completion.
- UI receives state and callbacks.
- No static lookup, production test mode, or mutable global registry.
- Interfaces represent real boundaries, not mocking-tool ceremony.

## Coroutine testing

- Use `runTest`.
- Share one `TestCoroutineScheduler`.
- Use `StandardTestDispatcher` for precise production-like scheduling.
- Use `UnconfinedTestDispatcher` deliberately for eager test collection.
- `runCurrent()` runs ready tasks.
- `advanceTimeBy(n)` moves virtual time.
- `advanceUntilIdle()` drains scheduler work.
- `join`, `await`, or cancel owned jobs.
- Virtual time skips coroutine `delay`, not blocking I/O.
- Assert cancellation and cleanup separately from application failure.
- Never swallow `CancellationException`.

Coroutine-test APIs and opt-ins are version-sensitive.

## Main dispatcher

- Replace `Dispatchers.Main` for local tests of `viewModelScope`.
- Reset it unconditionally, usually through a JUnit rule.
- Inject IO/Default dispatchers into code that selects execution policy.
- Make every test dispatcher share the scenario's scheduler.

Main replacement and dispatcher injection solve different seams.

## Flow testing

### Cold finite Flow

Use `first`, `take`, `toList`, or another bounded terminal operator.

### StateFlow

- Assert `value` when current state is the contract.
- Remember conflation: intermediate values may not all be observed.
- A `stateIn` using `Lazily`/`WhileSubscribed` needs an active collector.

### SharedFlow

- Start the subscriber before emitting when `replay = 0`.
- Test replay and buffer policy explicitly.
- Put infinite collection in `backgroundScope` or cancel its Job.

Optional helpers such as Turbine change ergonomics, not semantics.

## ViewModel checklist

- Initial state.
- Public action to loading/content/error.
- Retry and repeated action policy.
- Latest-wins or concurrent-operation policy.
- Cancellation when owner/action changes.
- `SavedStateHandle` reconstruction inputs.
- Effect delivery policy if effects exist.
- No Activity, Fragment, View, or NavController dependency.

Constructing a `SavedStateHandle` is not a process-death test.

## Repository, network, and database

### Repository

- fake remote and local sources;
- cache hit/stale/refresh;
- mapping and persistence;
- error translation;
- cancellation and concurrency;
- source-of-truth result.

### Network

- pure DTO mapping;
- mock server for real request/response adapter;
- malformed body/status/API error;
- timeout and bounded retry;
- owner cancellation cancels the client call;
- no production backend in routine tests.

### Database

- fake DAO for repository policy;
- real Room/SQLite for query, constraint, transaction, invalidation, migration;
- fresh database per test;
- close every database;
- prefer device fidelity for Room implementation tests per current Android
  guidance.

Do not preempt the dedicated Room topic.

## Navigation testing

- Pass callbacks to destinations; test navigation intent with a fake/recording
  navigator.
- Use `TestNavHostController` or the current test controller when graph,
  route, result, deep link, or back stack is the risk.
- Prefer visible destination behavior when controller internals are unnecessary.
- Typed-route and Navigation testing APIs are version-sensitive.

## Compose testing

- Query the semantics tree.
- Prefer text, role, label, state, and content description.
- Perform user actions and assert observable semantics.
- Merged semantics is the default.
- Use unmerged semantics deliberately, often for diagnosis.
- Use test tags only when no stable user semantic fits.
- Recomposition is not Activity recreation or process restoration.

## Espresso and Views

```text
matcher → action → assertion
```

Espresso synchronizes the main message queue and registered idling resources.
It cannot infer arbitrary background work. Prefer deterministic fake
dependencies or an explicit idling boundary. Never replace synchronization
with `Thread.sleep`.

Use ActivityScenario/FragmentScenario for explicit lifecycle states and close
them after use.

## Lifecycle testing

Name the exact transition:

- Activity recreation;
- STOPPED → STARTED;
- Fragment View destruction/recreation;
- navigation pop/owner removal;
- task-stack loss;
- process death/restoration.

`scenario.recreate()` proves recreation, not process death.

## Flakiness checklist

- No real sleeps or arbitrary polling.
- No real backend or uncontrolled filesystem.
- Fixed clock, locale, zone, random seed, and IDs where relevant.
- Stable semantic selectors.
- Animation controlled where it affects observation.
- One scheduler and explicit coroutine ownership.
- Fresh graph/fakes/database/server/scenario per test.
- No order dependence or shared singleton mutation.
- All resources and collectors closed/cancelled.
- Failure messages identify scenario inputs.

## Isolation checklist

- Fresh subject and dependency graph.
- Fresh mutable fake state.
- Reset Main dispatcher and framework rules.
- Clear external storage/database/server fixtures.
- Avoid static caches.
- Tests pass individually, in random order, and in parallel where supported.
- Hilt replacements do not share mutable test state accidentally.

## Snapshot/golden trade-offs

Good for broad visual-regression detection. Weak for accessibility, interaction,
navigation, focus, and business behavior. Stabilize rendering inputs and review
baseline changes carefully; tool APIs are version-specific.

## Interview-ready summary

Testing starts with risk, not a library. Use architecture seams to control
dependencies, time, lifecycle, and ownership. Choose the smallest boundary that
still contains the real behavior. Prefer state and public outcomes over
implementation-call verification. Add real adapter, UI, and end-to-end evidence
only for risks that focused tests cannot cover reliably.
