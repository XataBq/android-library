# Android Networking Architecture — Cheat Sheet

## Layer boundary

```text
UI → ViewModel → optional use case → Repository
                                      ↓
                         local / remote data sources
                                      ↓
                        service → HTTP client
```

Data owns service declarations, HTTP clients, DTOs, serialization, raw
responses, transport errors, mapping, and source coordination. Do not expose
Retrofit, OkHttp, DTO, URL, `Response`, `Request`, or `Call` types upward.

## Request and response

Request:

- method;
- scheme/host/path;
- query parameters;
- headers;
- optional body and media type.

Response:

- status;
- headers;
- optional body;
- redirect or conditional outcome.

A `2xx` response can legitimately have no body. Status meaning always depends
on the endpoint contract.

## Methods and repeatability

| Method | Safe | Idempotent by HTTP semantics | Retry note |
| --- | --- | --- | --- |
| GET | yes | yes | retry only transient failures, bounded |
| POST | no | no | require API idempotency/reconciliation |
| PUT | no | yes | still confirm endpoint and payload semantics |
| PATCH | no | no | do not assume repeatable |
| DELETE | no | yes | response can differ across repeats |

Idempotent means repeated intended effect, not guaranteed success or identical
response bytes.

## Status guide

- `2xx`: endpoint-specific successful handling.
- `3xx`: redirect or conditional outcome; inspect exact status.
- `4xx`: authentication, authorization, validation, conflict, not-found, and
  rate-limit cases are distinct.
- `5xx`: server failure; not an automatic retry.
- `304`: reuse a validated cached representation; it is not an empty entity.

## Service, client, source, repository

| Component | Responsibility |
| --- | --- |
| service | endpoint declaration and wire types |
| HTTP client | calls, connections, TLS, redirects, timeouts, interceptors, cache |
| remote source | response/status parsing, DTOs, transport translation |
| mapper | wire validation and application-model construction |
| repository | source of truth, local/remote coordination, freshness, stable API |

## DTO versus domain

DTOs model:

- wire names and optional fields;
- version drift;
- server nullability;
- serialized date, enum, and number forms.

Domain/application models preserve:

- validated identifiers;
- invariants;
- meaningful defaults;
- stable application terminology.

Reject invalid required data. Never default merely to silence a parsing error.

## Failure taxonomy

Keep distinct:

- no route or connection refused;
- DNS;
- connect/read/write/whole-call timeout;
- TLS/certificate/hostname failure;
- owner cancellation;
- non-success HTTP response;
- malformed or missing response;
- declared API business error;
- domain validation failure.

Cancellation normally propagates and is not a user-facing error.

## Cancellation-safe mapping

```kotlin
try {
    remoteCall()
} catch (cancelled: CancellationException) {
    throw cancelled
} catch (expected: IOException) {
    throw StableDataFailure(expected)
}
```

Do not wrap suspend networking in ordinary `runCatching`.

## Timeout guide

- connect: establishing a connection;
- read: inactivity while reading;
- write: inactivity while writing;
- call: total client-call budget;
- coroutine timeout: larger caller-owned operation budget.

Set finite, observable, endpoint-appropriate budgets. Verify exact semantics
against the installed client version.

## Retry checklist

- Is the failure transient?
- Is the operation idempotent or protected by operation identity?
- Could the server have applied the first request?
- Are attempts and total time bounded?
- Is backoff capped and jittered?
- Is server `Retry-After` validated and capped?
- Who owns the retry lifetime?
- How is ambiguous success reconciled?

Never retry cancellation, malformed payloads, authorization denial, or every
`4xx`/`5xx` mechanically.

## Interceptor versus authenticator

| Interceptor | Authenticator |
| --- | --- |
| decorates/observes ordinary calls | responds to authentication challenge |
| common headers, request ID, timing | may produce retried request or stop |
| no feature business logic | must bound attempts and prevent recursion |

Token attachment may read a current snapshot. Concurrent `401` refresh needs
single-flight coordination, failed-token comparison, a refresh path that does
not invoke itself, and an explicit logout boundary.

## TLS checklist

- HTTPS required for sensitive traffic.
- Use system hostname and certificate validation.
- Never trust every certificate or hostname.
- Use Network Security Configuration for explicit Android trust policy.
- Keep debug CAs out of production trust.
- Treat pinning as advanced and usually not recommended by Android.
- If justified: backup pins, rotation, expiry, monitoring, recovery, and
  threat-model approval.

TLS protects transport and server identity. It does not authorize users or
validate business data.

## Caching and offline

HTTP cache owns representations, freshness, validators, `ETag`,
`Last-Modified`, and `Cache-Control`.

Repository/database cache owns application persistence, queries, source of
truth, synchronization, and offline behavior.

A connectivity signal does not prove DNS, TLS, server, or endpoint success.
Do not gate every request solely on a connectivity Boolean.

## Pagination

- Define page/offset or cursor/token contract.
- Use stable identity and deduplicate.
- Separate refresh, append, and optional prepend.
- Detect end explicitly.
- Handle expired cursors and reordered data.
- Cancel obsolete loads.
- Keep Paging-library types at their deliberate architecture boundary.

## Upload and download

- Stream; do not buffer the entire file.
- Let the remote source own the HTTP `Call` and response lifetime.
- Connect coroutine cancellation to `Call.cancel()` so an active network read
  is closed rather than checked only between blocking reads.
- Close `Response`/`ResponseBody` and file streams on every path.
- Write to a unique partial file in the target directory.
- Atomically move the validated partial file to the final path as the commit
  point.
- Throttle progress updates.
- Delete the partial file after failure or cancellation and report cleanup
  failure for remediation.
- Validate size/integrity where required.
- Resume only with server-supported protocol and reconciliation.

## Logging

Log bounded metadata such as request ID, endpoint template, status class, and
timing. Redact:

- authorization and cookies;
- refresh/access tokens;
- query secrets;
- personal data;
- request/response bodies by default.

Debug logging policy must not leak into production.

## Test matrix

- DTO serializer: valid, missing, unknown, malformed, enum evolution.
- Mapper: invariants and defaults.
- Remote source: status/body/error mapping.
- Repository: local/remote coordination and stale-data policy.
- Mock server: path, headers, body, parsing, timeout, redirects.
- Retry: classification, bounds, backoff, cancellation.
- Authentication: concurrent `401`, one refresh, recursion, logout.
- Cache: validators, `304`, stale/fresh behavior.
- Pagination: refresh, append, duplicates, end, cancellation.
- Transfer: progress, disk failure, partial cleanup, cancellation.

## Smells

- service or raw response in ViewModel;
- DTO reused as UI model;
- every failure mapped to “no internet”;
- `runCatching` swallows cancellation;
- infinite retry or token refresh;
- disabled TLS verification;
- pinning without rotation;
- secrets or bodies in logs;
- connectivity used as source of truth;
- HTTP cache presented as offline database;
- client created per call;
- no timeout;
- giant business-logic interceptor;
- large files held in memory.

## Interview-ready summary

Networking is a Data-layer adapter around an unreliable HTTP boundary. The
remote source confines client APIs and DTOs; mapping protects application
invariants; the repository owns source coordination and stable contracts.
Cancellation propagates, timeouts and retries are bounded, authentication
refresh is single-flight, TLS validation stays enabled, and each boundary is
tested independently.
