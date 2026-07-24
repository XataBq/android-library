# Kotlin Structured Concurrency and Supervision — Practice

## Exercise 1 — Predict the Job tree

### Goal

Predict ownership, completion, cancellation, and failure propagation.

### Scenario

Analyze nested `launch`, `async`, `coroutineScope`, and one supervised subtree.
One child fails, one waits indefinitely, and one returns a Deferred result.

### Constraints

- Draw every parent-child edge.
- Distinguish block end from Job completion.
- Trace upward failure and downward cancellation.
- Identify cancelled siblings and every observed/unobserved result.
- Do not infer behavior from thread order.

### Expected deliverable

A Job tree, event timeline, final outcome, and propagation justification.

### Evaluation criteria

The tree is accurate; parent waiting is explicit; regular and supervised edges
are distinguished; all Deferred values are accounted for.

### Optional hints

Mark the lexical scope owner before considering which child fails first.

## Exercise 2 — Design a fail-fast feature load

### Goal

Build one valid aggregate from required concurrent values.

### Scenario

A checkout needs cart, permissions, and current pricing; absence of any value
invalidates the screen result.

### Constraints

- Use `coroutineScope`.
- Start only independent work concurrently.
- Define sibling cancellation and the caller's error boundary.
- Preserve cancellation.
- Include a deterministic sibling-cancellation test.

### Expected deliverable

Suspend contract, Job tree, error policy, and test plan without a full solution.

### Evaluation criteria

Normal return means all children finished; failure cancels remaining work; no
Deferred is forgotten; tests use signals rather than sleeps.

### Optional hints

Ask which requests need another request's ID before starting.

## Exercise 3 — Design a best-effort dashboard

### Goal

Keep independent widgets useful after a peer failure.

### Scenario

Profile, weather, and recommendations load independently, retain separate retry
actions, and may show cached content.

### Constraints

- Use bounded supervision.
- Observe every child outcome.
- Model partial success explicitly.
- Rethrow cancellation.
- Test failure isolation and successful sibling completion.

### Expected deliverable

State model, supervised aggregation sketch, observability/retry policy, and
deterministic tests.

### Evaluation criteria

No failure is lost; valid siblings survive; cancellation still reaches all
children; UI can identify and retry one section.

### Optional hints

Supervision changes propagation, not the need to await and interpret results.

## Exercise 4 — Review long-lived work

### Goal

Replace accidental lifetimes with explicit screen, application, or durable
ownership.

### Scenario

A Repository creates its own scope with SupervisorJob, launches
fire-and-forget uploads, wraps retries in NonCancellable, and is called from a
ViewModel that assumes navigation cancels everything.

### Constraints

- Identify the required lifetime of each operation.
- Remove hidden scopes and broad NonCancellable.
- Choose screen scope, injected application scope, persistence, or WorkManager.
- Define completion, cancellation, and retry contracts.
- Do not prescribe WorkManager for disposable in-process work.

### Expected deliverable

Defect table, corrected ownership diagram, API contracts, and validation tests.

### Evaluation criteria

Every operation has an owner; durable claims have durable scheduling; callers
can observe completion; cleanup is narrow; screen work cannot leak.

### Optional hints

Separate “survive navigation” from “survive process exit or device restart.”
