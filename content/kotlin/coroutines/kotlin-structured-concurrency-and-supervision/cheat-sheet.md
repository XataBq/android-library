# Kotlin Structured Concurrency and Supervision — Cheat sheet

## Invariants

- Every coroutine has an explicit owner.
- Parent completion waits for children.
- Parent cancellation propagates downward.
- Regular child failure propagates upward and cancels siblings.
- A bounded suspend contract exposes completion or failure.
- Supervision isolates selected child failures; it does not handle them.

## Propagation table

| Event | Regular Job | Supervisor parent |
|---|---|---|
| parent cancellation | cancels children | cancels children |
| child `CancellationException` | normally does not fail parent | isolated |
| child non-cancellation failure | fails parent, cancels siblings | direct siblings continue |
| parent completion | waits for children | waits for children |

## Scope choices

| API | Lifetime | Failure policy |
|---|---|---|
| `coroutineScope` | bounded suspend call | fail-fast |
| `supervisorScope` | bounded suspend call | direct child failures isolated |
| `Job` | owned hierarchy | regular propagation |
| `SupervisorJob` | explicitly managed scope | direct children independent |

Do not attach a fresh `Job()` or `SupervisorJob()` to an arbitrary child
builder; that can sever the inherited tree.

## Fail-fast versus best-effort

- Fail-fast: every value is required for one valid result.
- Best-effort: independent sections remain useful separately.
- Supervision requires an explicit partial-result model.
- Never use supervision merely to “avoid crashes.”

## Partial success

- identify success/failure per independent section;
- keep existing content when the contract permits;
- assign retry ownership;
- observe/log every failure;
- preserve cancellation rather than convert it into unavailable content;
- avoid one universal wrapper when consumers need different decisions.

## Deferred ownership

- Every Deferred has an owner and an eventual result/failure.
- Start it only inside the bounded owner.
- Await every Deferred or explicitly translate its outcome.
- Supervised async still throws from `await`.
- Forgotten Deferred means forgotten failure semantics.

## Timeout

- `withTimeout`: cancels block and throws timeout cancellation.
- `withTimeoutOrNull`: returns `null` for its own timeout.
- Lexical children are cancelled with the timed block.
- Detached work can escape and is a defect.
- Timeout is product policy, not universal lower-level policy.

## Cleanup

- Use `finally`.
- Prefer non-suspending cleanup.
- Use `withContext(NonCancellable)` only for small mandatory suspending cleanup.
- Never place ordinary work, retries, or whole children in NonCancellable.

## Android ownership

- ViewModel scope: screen scenario; cancellation on clearing.
- Lifecycle/Compose scope: current UI owner.
- Injected application scope: in-process work deliberately outliving screen.
- WorkManager: reliable scheduled work that must persist beyond ordinary
  in-process ownership.
- Repository must not invent an ad hoc scope.

## Testing

- use `runTest` and deterministic signals;
- verify parent waiting;
- verify regular sibling cancellation;
- verify supervised sibling survival and observe the failure;
- test downward cancellation and timeout;
- assert `finally` cleanup;
- model partial results;
- finish without leaked child Jobs;
- avoid timing sleeps.

## Common smells

`GlobalScope`, hidden scope creation, arbitrary SupervisorJob, fire-and-forget
Repository work, forgotten Deferred, blanket supervision, swallowed
cancellation, broad NonCancellable, escaped timeout child, wrong Android owner,
and CoroutineExceptionHandler used as business error handling.

## Interview summary

Structured concurrency makes lifetime and completion a tree. Regular scopes
fail fast; supervised scopes isolate selected direct-child failures while
retaining downward cancellation and parent waiting. Select policy from result
invariants, observe every failure, keep cleanup bounded, and choose UI,
application, or durable scheduling ownership deliberately.
