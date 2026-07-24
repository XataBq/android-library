# Android Networking Architecture — Interview Questions

## 1. Why is networking a Data-layer concern?

**Strong answer:** Service declarations, clients, DTOs, serializers, and
transport failures are volatile infrastructure. Data adapts them to stable
repository contracts consumed by ViewModel and optional Domain.

**Weak answer:** Every layer should call the service directly to avoid classes.

**Follow-up:** Which types must not cross the repository boundary?

## 2. What makes up an HTTP request?

**Strong answer:** Method, target URI including path/query, headers, and an
optional representation body with media type, all interpreted by the endpoint
contract.

**Weak answer:** Only a URL and JSON body.

## 3. What makes up an HTTP response?

**Strong answer:** Status, headers, and optional content. Empty success,
redirect, conditional result, and malformed expected body require different
handling.

**Weak answer:** Every successful response is a non-null DTO.

## 4. What do safe and idempotent mean?

**Strong answer:** Safe methods are intended as read-only semantics.
Idempotent means repeating the intended request has the same intended effect
as one request, not identical responses or guaranteed success.

**Weak answer:** Idempotent means a request cannot fail.

## 5. Can a POST ever be retried?

**Strong answer:** Not mechanically. It may be repeatable when the API provides
an idempotency key, operation identity, or reconciliation and the failure
policy accounts for ambiguous server application.

**Weak answer:** POST is always safe to retry, or POST can never be retried.

## 6. Why are status-code classes insufficient?

**Strong answer:** Classes give broad protocol categories, while exact statuses
and error bodies derive meaning from the API contract. `401`, `403`, `404`,
`409`, `422`, and `429` are not one domain failure.

**Weak answer:** Every `4xx` means invalid input and every `5xx` means retry.

## 7. What belongs in a declarative service interface?

**Strong answer:** Endpoint method/path, parameters, headers/body, suspend or
call contract, and wire return types. Raw responses remain confined to Data.

**Weak answer:** UI state, retry messages, and database transactions.

## 8. What does the HTTP client own?

**Strong answer:** Calls, connections/pooling, protocol negotiation, TLS,
redirects, timeouts, interceptors, authenticators, and optional HTTP cache.

**Weak answer:** Product authorization rules and ViewModel state.

**Follow-up:** Why should clients usually be reused?

## 9. Why separate DTO and domain model?

**Strong answer:** DTO follows wire names, nullability, and version drift;
mapping validates and constructs stable application meaning and invariants.

**Weak answer:** Rename the DTO “DomainModel” and use it everywhere.

## 10. How should unknown and missing JSON fields differ?

**Strong answer:** Ignoring unknown additive fields can aid compatibility.
Missing required fields should fail; optional fields need explicit meaningful
defaults or null handling. Serializer policy and contract tests must agree.

**Weak answer:** Default every missing value to empty or zero.

## 11. Where does DTO-to-domain mapping belong?

**Strong answer:** At the Data boundary, often in a mapper or remote source,
before repository results cross upward. It parses, validates, normalizes, and
rejects invalid payloads.

**Weak answer:** In each composable because it knows what to display.

## 12. What is the repository's networking role?

**Strong answer:** It exposes application contracts and coordinates remote,
local, cached, freshness, and source-of-truth policy. It hides endpoints and
transport details.

**Weak answer:** It is a pass-through alias for one Retrofit service.

## 13. Build a practical network error taxonomy.

**Strong answer:** Distinguish route/connection, DNS, timeouts, TLS,
cancellation, non-success HTTP, malformed representation, API business error,
and domain validation, then map only where the next boundary needs stability.

**Weak answer:** Everything is “no internet.”

## 14. Why must CancellationException be rethrown?

**Strong answer:** It communicates owner-controlled coroutine cancellation.
Converting it to failure lets obsolete work continue or produces false UI
errors. Catch expected exceptions narrowly or rethrow cancellation first.

**Weak answer:** Cancellation is just another retryable server failure.

## 15. Compare connect, read, write, and call timeouts.

**Strong answer:** They bound connection establishment, read inactivity, write
inactivity, and the whole client call respectively. Exact semantics are
library-specific and budgets can differ by endpoint.

**Weak answer:** One timeout has identical meaning in every library and phase.

## 16. What makes retry safe enough?

**Strong answer:** Transient classification, operation repeatability,
idempotency/identity, bounded attempts and elapsed time, capped backoff with
jitter, cancellation, and reconciliation of ambiguous outcomes.

**Weak answer:** Retry all exceptions until success.

## 17. What should an interceptor do?

**Strong answer:** Narrow transport cross-cutting work such as common headers,
request IDs, redacted timing, or observation. Ordering and proceed semantics
depend on the client.

**Weak answer:** Hold repositories, perform feature decisions, and navigate.

## 18. How does an authenticator differ?

**Strong answer:** It responds to an authentication challenge and may return a
new request or stop. It must bound attempts, avoid refreshing itself, and
respect the library's execution contract.

**Weak answer:** It is merely a logging interceptor with unlimited retries.

## 19. How do you handle simultaneous 401 responses?

**Strong answer:** Coordinate one refresh for the failed token, re-check current
credentials inside the critical section, publish one result to waiters, retry
with the new token, and terminate on refresh failure.

**Weak answer:** Launch one refresh per failed request and let the last write
win.

**Follow-up:** How do you prevent recursive refresh?

## 20. What does TLS validate?

**Strong answer:** Encryption/integrity in transit and server identity via
certificate chain, trusted roots, and hostname verification. It does not
authorize the app user or prove payload business validity.

**Weak answer:** HTTPS makes all server content and users trusted.

## 21. Should every Android app pin certificates?

**Strong answer:** No. Android cautions against default pinning because
certificate or CA rotation can break installed clients. A justified exception
needs backup pins, expiry/rotation, monitoring, recovery, and threat modeling.

**Weak answer:** Pin one leaf certificate forever for complete security.

## 22. Compare HTTP cache and database cache.

**Strong answer:** HTTP cache stores protocol representations under freshness
and validation rules. Database cache owns application persistence, queries,
offline source-of-truth, and synchronization.

**Weak answer:** An HTTP disk cache automatically creates an offline-first app.

## 23. Why not check connectivity before every request?

**Strong answer:** A network signal is a momentary capability hint, not proof
that DNS, TLS, routing, server, or endpoint will work. Attempt owned work and
handle its outcome; use signals for UX or scheduling where useful.

**Weak answer:** “Connected” guarantees every endpoint succeeds.

## 24. What must pagination model?

**Strong answer:** Key/cursor semantics, stable identity, deduplication,
refresh/append/prepend, end detection, reordering, expired keys, failure, and
cancellation. Library boundaries remain deliberate.

**Weak answer:** Increment a page integer in the composable.

## 25. How should large uploads and downloads work?

**Strong answer:** Stream with bounded memory from a remote source that owns the
HTTP call and response. Link coroutine cancellation to call cancellation so a
blocked read is closed, close response/body and streams, write a unique partial
file, delete it on pre-commit failure or cancellation, and atomically move only
after validation. Resume still requires server protocol support.

**Weak answer:** Convert every file to one byte array and retry from zero
forever.

**Follow-up:** What happens when cancellation races with the atomic commit?

## 26. What should networking tests cover?

**Strong answer:** Serialization and mapping; remote status/body behavior;
repository coordination; mock-server encoding; timeout/retry/cancellation;
concurrent auth refresh; caching; pagination; transfer cleanup; and selected
real integration contracts.

**Weak answer:** One manual call to production proves the entire architecture.

**Follow-up:** Which tests should remain deterministic and offline?
