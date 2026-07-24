# Interview Questions — Android Testing Foundations

## 1. What does a valuable test protect?

**Strong answer:** It protects an explicit contract or risk: a business
invariant, state transition, adapter behavior, integration, or user-observable
workflow. It gives refactoring confidence through stable public observations
and useful failure diagnostics.

**Weak or misleading answer:** A test is valuable whenever it increases line
coverage.

**Follow-up:** Name a high-coverage test that could still provide little
confidence.

## 2. How do unit, integration, component, UI, instrumentation, and end-to-end tests differ?

**Strong answer:** Unit/integration/component/UI/end-to-end describe scope and
real collaboration, while local/instrumented describe execution environment.
Names vary, so describe subject, real dependencies, doubles, runner, and risk.
A small DAO test can be instrumented; a broad UI simulation can be local.

**Weak or misleading answer:** Every unit test is local and every instrumented
test is end to end.

**Follow-up:** How would you classify an on-device Room DAO test?

## 3. Is the test pyramid a mandatory ratio?

**Strong answer:** No. It communicates a cost tendency: many focused tests,
fewer integration tests, and few expensive end-to-end tests. A portfolio should
instead balance feature risks, feedback speed, realism, diagnostics, device
coverage, and maintenance.

**Weak or misleading answer:** Exactly 70% of every project must be unit tests.

**Follow-up:** What could justify more integration tests in one subsystem?

## 4. What is the smallest reliable test?

**Strong answer:** The least expensive boundary that still contains the real
behavior needed to expose the target failure. A mapper needs no Activity; a SQL
query needs real database semantics; a back-stack defect needs navigation
behavior. “Small” must not remove the behavior being verified.

**Weak or misleading answer:** Always mock everything and test one method.

**Follow-up:** Why is a fake DAO insufficient for verifying a Room query?

## 5. What does Arrange–Act–Assert contribute?

**Strong answer:** It makes precondition, causal action, and observed result
visible. It is a clarity tool, not a law; Given–When–Then is equivalent, and
small tests may express the structure without comments.

**Weak or misleading answer:** Every test must have exactly three comment
blocks.

**Follow-up:** When should a test with several Act phases be split?

## 6. Compare state, interaction, and observable-behavior verification.

**Strong answer:** State verification checks a result, interaction verification
checks a meaningful collaborator call, and observable behavior checks the
public consumer outcome. Prefer the least implementation-coupled observation
that proves the risk. Verify interactions when the interaction itself is a
contract.

**Weak or misleading answer:** Verify every internal call to ensure complete
coverage.

**Follow-up:** Give one interaction where “exactly once” could be a real
requirement.

## 7. Define dummy, stub, fake, spy, and mock.

**Strong answer:** A dummy is unused input; a stub gives programmed answers; a
fake is a lightweight working implementation; a spy records observations,
often while delegating; a mock enforces programmed interactions. Terminology
varies, so teams should state relied-on behavior.

**Weak or misleading answer:** They are all interchangeable names for Mockito
objects.

**Follow-up:** Why can framework terminology differ from these definitions?

## 8. When is a fake preferable to a mock?

**Strong answer:** When coherent stateful behavior matters across several
operations: repository cache behavior, controlled Flow emissions, persistence,
or navigation history. Fakes make public outcomes easy to assert and avoid
freezing implementation call sequences.

**Weak or misleading answer:** Fakes are always better, so interaction
verification is never useful.

**Follow-up:** What isolation problem can a mutable fake introduce?

## 9. How does architecture affect testability?

**Strong answer:** Explicit constructors, narrow repository/platform
boundaries, pure transformations, injected clocks/dispatchers, and owned
coroutines expose controllable seams. Static lookup, global state, hidden time,
and fire-and-forget work make tests nondeterministic.

**Weak or misleading answer:** Add an interface around every class solely so a
mocking framework can replace it.

**Follow-up:** When is an interface unnecessary for a test?

## 10. Which logic should be tested without Android?

**Strong answer:** Pure validators, reducers, mappers, state machines, pricing
rules, and focused use cases usually belong in fast local tests. Test important
equivalence classes and edge cases rather than Android framework behavior or
private helpers.

**Weak or misleading answer:** All production code needs an emulator because
the app is Android.

**Follow-up:** When would a mapper still need an integration test?

## 11. What should a ViewModel test observe?

**Strong answer:** Initial state, public actions, loading/content/error
transitions, retry/concurrency policy, cancellation, saved reconstruction
inputs, and any explicit effect-delivery contract. Build it with fakes and
control Main; do not assert private fields or start an Activity by default.

**Weak or misleading answer:** Verify that every private method is called in
the expected order.

**Follow-up:** Does constructing a `SavedStateHandle` prove process restoration?

## 12. What does `runTest` provide?

**Strong answer:** A `TestScope`, a test dispatcher, one controllable scheduler,
virtual-time operations, and detection/waiting behavior for owned coroutine
work. New work on `StandardTestDispatcher` is queued until the test yields or
advances it.

**Weak or misleading answer:** It runs all coroutines immediately and makes
every blocking API virtual.

**Follow-up:** Why should all test dispatchers share one scheduler?

## 13. How should virtual time be used?

**Strong answer:** Use `runCurrent` for ready tasks, `advanceTimeBy` for a
specific delay boundary, and `advanceUntilIdle` when draining all scheduled
work matches the assertion. Virtual time skips coroutine `delay`; it does not
speed blocking network or file calls.

**Weak or misleading answer:** Replace every synchronization problem with
`advanceUntilIdle`.

**Follow-up:** When does a precise `advanceTimeBy` assertion teach more?

## 14. Main dispatcher replacement or dispatcher injection?

**Strong answer:** Replace Main in local tests for framework-owned constructs
such as `viewModelScope`, and reset it unconditionally. Inject dispatchers where
application code chooses IO/CPU execution. Both should use the same test
scheduler within a scenario.

**Weak or misleading answer:** Hardcode `Dispatchers.IO` everywhere and use
real threads in tests.

**Follow-up:** What can go wrong if two test dispatchers have different
schedulers?

## 15. How do you test cold Flow, StateFlow, and SharedFlow?

**Strong answer:** Bound finite cold Flow with `first`, `take`, or `toList`.
Treat `StateFlow` as current state when appropriate and account for conflation.
Start a collector for lazily/while-subscribed `stateIn`. For `SharedFlow`,
define replay/buffer/subscriber timing and cancel infinite collection.

**Weak or misleading answer:** Call `toList()` on every Flow and wait for it to
finish.

**Follow-up:** Why might a `stateIn(WhileSubscribed)` value never update in a
test?

## 16. How do you test repository behavior?

**Strong answer:** Use deterministic remote/local fakes for cache, freshness,
refresh, source-of-truth, mapping, failure, concurrency, and cancellation
policy. Add separate boundary tests for real serializers, HTTP adapters, DAOs,
transactions, and migrations.

**Weak or misleading answer:** Mock the repository itself while claiming to
test the repository.

**Follow-up:** Which test should own the “remote success is persisted” rule?

## 17. Fake service or mock web server?

**Strong answer:** A fake service isolates repository policy. A mock server
exercises real request construction, client adapters, status handling, and
serialization without a production backend. Use each for its distinct risk.

**Weak or misleading answer:** Always call staging because it is more
realistic.

**Follow-up:** How would you prove owner cancellation stops the client call?

## 18. When should Room be real in a test?

**Strong answer:** When verifying SQL queries, constraints, transactions,
invalidation, or migrations. A fake DAO is appropriate for repository policy.
Use a fresh database, device fidelity when required, exported schema history
for migrations, and unconditional cleanup.

**Weak or misleading answer:** An in-memory fake collection proves every Room
query and migration.

**Follow-up:** Why can host SQLite differ from device behavior?

## 19. How should navigation be tested?

**Strong answer:** Pass navigation callbacks to destinations and test intent
with a recording fake. Use a test navigation controller or rendered host for
graph, route, deep-link, result, and back-stack risks. Prefer visible
destination behavior unless controller state is the contract.

**Weak or misleading answer:** Inject `NavController` into every ViewModel and
mock all calls.

**Follow-up:** When is checking the current back-stack entry justified?

## 20. What makes a good Compose UI assertion?

**Strong answer:** It queries stable semantics such as text, role, label, state,
or content description, performs a user action, and asserts an observable
semantic result. Merged semantics is the default; unmerged queries and test
tags are deliberate tools, not automatic fixes.

**Weak or misleading answer:** Find the third composable child by position and
assert its implementation name.

**Follow-up:** Why do accessible semantics often improve testability?

## 21. What does Espresso synchronize?

**Strong answer:** Main message-queue work and registered idling resources.
Unknown background work needs an explicit synchronization boundary or a
deterministic fake. Register/unregister idling resources and do not use
`Thread.sleep` as a substitute.

**Weak or misleading answer:** Espresso automatically knows when every network
and coroutine operation in the process finishes.

**Follow-up:** What belongs in an `IdlingResource`, and what should it avoid
retaining?

## 22. How do lifecycle and recreation tests differ from process-death tests?

**Strong answer:** Activity recreation, STARTED/STOPPED transitions, Fragment
View destruction, navigation removal, task loss, and process death are distinct
owners and events. `ActivityScenario.recreate()` checks recreation, not
operating-system process death.

**Weak or misleading answer:** Rotation proves all state survives process
death.

**Follow-up:** How would you test Fragment View collection restart?

## 23. What usually makes Android tests flaky?

**Strong answer:** Uncontrolled wall time, real network, shared globals, test
order, races, animation, unstable selectors, random/locale inputs, leaked
resources, and ownerless async work. Control inputs, use scheduler/framework
synchronization, isolate graphs, and close everything.

**Weak or misleading answer:** Add a longer sleep or retry the test three times.

**Follow-up:** How do you distinguish a product race from a test race?

## 24. What do snapshot/golden tests prove, and what do they miss?

**Strong answer:** They detect visual-rendering differences efficiently but
carry environment, baseline, broad-diff, and review costs. They do not by
themselves prove accessibility semantics, navigation, focus, interaction, or
business behavior.

**Weak or misleading answer:** A matching screenshot proves the whole screen is
correct.

**Follow-up:** Which inputs must be stabilized for a trustworthy golden?

## 25. How do you keep tests isolated?

**Strong answer:** Give each test a fresh subject, graph, mutable fake,
database/server/scenario, clock/seed, and owned collectors. Reset Main and
framework rules in cleanup. Tests should pass independently, reordered, and in
parallel where supported.

**Weak or misleading answer:** Reuse a process singleton for speed and reset it
only when a test fails.

**Follow-up:** Why does replacing a Hilt binding not automatically reset fake
state?

## 26. Name common Android testing anti-patterns.

**Strong answer:** Only UI tests, only mocked unit tests, private-method tests,
verifying every call, real sleeps/backends, singleton mutation, order
dependence, production test modes, swallowed cancellation, implementation-only
selectors, giant fixtures, uncontrolled clocks/randomness, and missing cleanup.

**Weak or misleading answer:** The only anti-pattern is low coverage.

**Follow-up:** Given a flaky end-to-end test, how would you decide whether to
repair, split, or remove it?
