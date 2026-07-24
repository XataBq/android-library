# Android Networking Architecture — Practice

Each exercise requires a design, representative Kotlin, and focused tests.
Do not provide a complete production implementation.

## Exercise 1 — Restore the repository boundary

### Goal

Refactor a ViewModel that calls a Retrofit-style service and renders raw
responses.

### Scenario

`ProfileViewModel` receives `ProfileService`, branches on `Response.code()`,
stores `ProfileDto` in `UiState`, and catches every exception as “No internet.”
Leaving the screen sometimes still produces an error snackbar.

### Constraints

- Confine service, raw response, DTO, serializer, and transport exceptions to
  Data.
- Introduce a remote data source, mapper, and repository contract.
- Preserve `CancellationException`.
- Distinguish not-found, access denied, malformed payload, timeout, and
  unavailable transport where the product needs them.
- Keep UI wording outside Data.
- Do not prescribe a universal `Result` wrapper.

### Expected deliverable

- before/after dependency diagram;
- service, remote-source, mapper, repository, and ViewModel signatures;
- one cancellation-safe error translation;
- tests for mapping, status handling, repository behavior, and owner
  cancellation.

### Evaluation criteria

- no client or DTO type crosses the repository contract;
- domain/application invariants are validated during mapping;
- cancellation does not become a user-visible failure;
- failures retain enough stable meaning for presentation.

### Optional hints

- Start by listing every type imported from the network library.
- Separate transport classification from UI message selection.

## Exercise 2 — Retry by semantics, not optimism

### Goal

Design retry policies for operations with different side-effect and transfer
contracts.

### Scenario

The app performs GET profile, POST payment, PUT settings, a large upload, and
token refresh. A proposed interceptor retries every `IOException` and `5xx`
five times immediately.

### Constraints

- Analyze DNS, connection, timeout, `408`, `409`, `429`, and `5xx` separately.
- Use HTTP method semantics plus each endpoint's documented contract.
- Address ambiguous server application of a request.
- Define bounded attempts, elapsed budget, capped backoff, jitter, and
  `Retry-After` handling.
- Use idempotency keys or reconciliation where the API supports them.
- Never retry cancellation.
- Define who owns each retry lifetime.

### Expected deliverable

- policy matrix for all five operations;
- operation-identity and ambiguity strategy for payment;
- pseudocode for one bounded retry helper;
- deterministic tests for attempt count, backoff, permanent failure, and
  cancellation.

### Evaluation criteria

- POST is neither mechanically forbidden nor blindly repeated;
- retry depends on failure type and repeatability;
- no hidden infinite loop exists;
- tests use controlled time rather than real sleeps.

### Optional hints

- “Did the response arrive?” and “Did the server apply the operation?” are
  different questions.
- A resumable upload requires a server protocol, not only a client loop.

## Exercise 3 — Coordinate concurrent authentication refresh

### Goal

Design access-token refresh when several calls receive `401` simultaneously.

### Scenario

Five requests use the same expired token. The current authenticator launches
five refresh calls, some overwrite newer credentials, and refresh `401` enters
the same authenticator recursively.

### Constraints

- Keep token attachment separate from challenge handling.
- Permit at most one refresh in flight for the failed token.
- Make waiting callers observe the same success or failure.
- Re-check the current token after acquiring coordination.
- Use a refresh client/path that cannot recursively invoke the authenticator.
- Bound response-chain attempts.
- Define atomic token replacement and logout/session invalidation.
- Redact every credential from logs.
- Respect the synchronous or suspend contract of the installed client API.

### Expected deliverable

- state/concurrency diagram;
- token provider and refresh-coordinator interfaces;
- library-adapter sketch with explicit version assumptions;
- tests for five concurrent `401`s, successful refresh, refresh failure,
  already-refreshed token, and recursion prevention.

### Evaluation criteria

- exactly one refresh serves concurrent callers;
- stale refresh results cannot overwrite newer tokens;
- failure terminates instead of looping;
- threading and blocking assumptions are explicit.

### Optional hints

- Compare the failed request token with the stored token inside the critical
  section.
- Do not copy a suspend mutex directly into a synchronous callback.

## Exercise 4 — Offline paginated feed

### Goal

Design a paginated repository whose local database is the observable source of
truth.

### Scenario

The server returns cursor pages. The feed must open with cached data, refresh
when stale, append without duplicates, retain usable content during temporary
failure, and cancel obsolete searches.

### Constraints

- Define refresh, append, end-of-list, and expired-cursor behavior.
- Persist remote items and continuation keys atomically where required.
- Deduplicate by stable identity.
- Separate HTTP cache from database/application cache.
- Do not treat connectivity state as endpoint truth.
- Preserve stale content while representing refresh/append failure.
- Preserve cancellation and avoid detached loads.
- State whether Android Paging is used and mark version-sensitive APIs.

### Expected deliverable

- data-flow and source-of-truth diagram;
- cursor/page and repository contracts;
- freshness, invalidation, failure, and conflict policy;
- tests for cached opening, refresh, append, duplicates, end, stale failure,
  cursor invalidation, and cancellation.

### Evaluation criteria

- UI observes one coherent local-backed stream;
- refresh and append cannot corrupt one another;
- network failure does not erase valid cached data;
- library-specific Paging types do not leak beyond the chosen boundary.

### Optional hints

- Model continuation keys as data with the page, not as a ViewModel counter.
- Test a refresh arriving while an old append is being cancelled.
