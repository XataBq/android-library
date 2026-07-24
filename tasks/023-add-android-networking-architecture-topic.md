# Task 023 — Add Android Networking Architecture Topic

Status: DONE

## Objective

Add the eleventh production educational topic in the Junior Core:

```text
android-networking-architecture
```

The topic must explain how Android applications should design network communication across UI, Domain, and Data layers.

The learner must understand:

- HTTP request/response fundamentals;
- API contracts;
- Retrofit-style service abstractions;
- OkHttp-style client responsibilities;
- serialization;
- DTOs and domain models;
- repository boundaries;
- error taxonomy;
- retries;
- cancellation;
- timeouts;
- authentication;
- interceptors;
- connectivity assumptions;
- caching;
- pagination;
- file transfer;
- testing;
- security.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds on:

- Architecture Foundations;
- Data Layer, Repositories and Synchronization;
- Domain Layer and Use Cases;
- ViewModel and UI State;
- Kotlin Coroutines Foundations;
- Structured Concurrency and Supervision;
- Kotlin Flow and Reactive Streams.

---

## Core teaching position

Networking is a Data-layer implementation concern.

The core model is:

```text
UI
→ ViewModel
→ Use case where justified
→ Repository contract
→ Remote data source / service
→ HTTP client
→ server
```

The topic must preserve these distinctions:

```text
HTTP transport error
≠ protocol error
≠ server business error
≠ serialization error
≠ domain failure
≠ UI message
```

A Repository should not expose Retrofit, OkHttp, raw Response, Call, Request, or framework-specific transport types to upper layers.

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
- all production topics;
- Tasks 016–022.

Use current official or primary documentation for:

- HTTP semantics;
- Android network security;
- Retrofit or equivalent declarative HTTP client behavior;
- OkHttp or equivalent HTTP client behavior;
- Kotlin serialization or equivalent JSON serialization;
- cancellation;
- timeouts;
- interceptors;
- caching;
- TLS;
- testing.

Do not fabricate library guarantees.

Do not fabricate access dates.

When using third-party library examples, clearly distinguish stable architectural principles from library-specific APIs.

---

## Canonical competency scope

Primary:

```text
design-data-layer-around-repositories
use-coroutines-and-flows-across-layers
explain-persistent-data-models
```

Strongly reinforced:

```text
apply-separation-of-concerns
isolate-android-framework-dependencies
evaluate-optional-domain-layer
design-viewmodel-ui-state
```

Contextually reinforced:

```text
explain-ui-layer-responsibilities
explain-unidirectional-data-flow
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/networking/android-networking-architecture/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: networking` is invalid, adapt using repository conventions and document the choice.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-networking-architecture
title: Android Networking Architecture
track: android
section: networking
difficulty: foundation
status: review
estimated_minutes: 240
content_version: 1
prerequisites:
  - android-data-layer-repositories-and-synchronization
  - android-domain-layer-and-use-cases
  - android-viewmodel-and-ui-state
  - kotlin-coroutines-foundations
  - kotlin-structured-concurrency-and-supervision
  - kotlin-flow-and-reactive-streams
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain request/response networking at a practical HTTP level.
2. Distinguish transport, protocol, serialization, server, domain, and UI errors.
3. Keep network-library types inside the Data layer.
4. Design service interfaces and remote data sources.
5. Separate DTOs from domain models.
6. Map nullable and optional API fields safely.
7. Explain HTTP methods and idempotency.
8. Explain status-code classes without oversimplifying semantics.
9. Use headers, query parameters, body, and path parameters appropriately.
10. Configure timeouts deliberately.
11. Use cancellation-aware suspend networking.
12. Design retry policy based on idempotency and failure type.
13. Explain interceptors and authenticators.
14. Handle authentication token refresh without infinite loops.
15. Explain TLS and certificate validation at a practical level.
16. Explain caching and conditional requests.
17. Design pagination.
18. Design upload and download flows.
19. Explain connectivity checks and offline assumptions.
20. Test networking at service, data-source, repository, and integration boundaries.
21. Recognize networking anti-patterns.
22. Design resilient network-backed repository behavior.

---

## Theory requirements

`theory.md` must contain approximately 22–26 substantial sections.

Required coverage:

### 1. Networking belongs in the Data layer

Explain why UI and Domain should not depend on HTTP-client types.

### 2. HTTP request anatomy

Cover:

- method;
- URL;
- path;
- query;
- headers;
- body.

### 3. HTTP response anatomy

Cover:

- status;
- headers;
- body;
- empty body;
- redirects at a high level.

### 4. Methods and idempotency

Explain:

- GET;
- POST;
- PUT;
- PATCH;
- DELETE;
- safe versus idempotent semantics;
- why retry depends on operation semantics.

Avoid simplistic “GET always succeeds” or “POST is never retryable” claims.

### 5. Status codes

Explain classes:

- 2xx;
- 3xx;
- 4xx;
- 5xx.

Also explain that application-specific meaning depends on API contract.

### 6. Service interface

Show a declarative service abstraction.

Explain:

- endpoint declaration;
- parameters;
- suspend integration;
- return type trade-offs;
- raw response confinement.

### 7. HTTP client responsibilities

Explain:

- connection management;
- TLS;
- redirects;
- timeouts;
- interceptors;
- cache;
- pooling at a high level.

Avoid unstable implementation details.

### 8. DTOs

Explain:

- wire representation;
- naming;
- nullability;
- backward-compatible fields;
- version drift;
- why DTOs are not domain models.

### 9. Serialization

Cover:

- JSON parsing;
- unknown fields;
- missing fields;
- malformed payload;
- date/time;
- enum evolution;
- numeric precision where relevant.

### 10. DTO-to-domain mapping

Explain:

- validation;
- defaulting;
- rejecting invalid payloads;
- preserving domain invariants;
- mapping location in Data layer.

### 11. Repository boundary

Show:

```text
Service response
→ Remote data source
→ Mapper
→ Repository
→ domain result
```

### 12. Error taxonomy

Distinguish:

- no network / connection failure;
- DNS;
- timeout;
- TLS failure;
- cancellation;
- non-success HTTP response;
- malformed response;
- API business error;
- domain validation failure.

### 13. Error mapping

Explain that upper layers should receive stable application-facing failures, not raw transport exceptions.

Do not prescribe one universal `Result` wrapper.

### 14. Cancellation

Explain:

- suspend call cancellation;
- owner cancellation;
- why cancellation is not a user-facing failure by default;
- not swallowing `CancellationException`.

### 15. Timeouts

Cover:

- connect timeout;
- read timeout;
- write timeout;
- call timeout at a high level;
- endpoint-specific policy;
- avoiding infinite waits.

### 16. Retry

Explain:

- transient versus permanent errors;
- idempotency;
- bounded retries;
- backoff;
- jitter concept;
- caller ownership;
- no hidden infinite loops;
- duplicate side-effect risks.

### 17. Interceptors

Explain:

- request mutation;
- common headers;
- logging;
- tracing;
- response observation;
- ordering;
- why business logic does not belong there.

### 18. Authentication and token refresh

Explain:

- attaching access token;
- 401 handling;
- single-flight refresh concept;
- refresh failure;
- avoiding recursive refresh;
- logout boundary;
- concurrency.

Do not invent a universal authenticator implementation.

### 19. TLS and certificate validation

Explain:

- HTTPS;
- server identity;
- certificate chain;
- hostname verification;
- trust store;
- why disabling verification is dangerous;
- certificate pinning as an advanced risk-managed choice, not a default slogan.

### 20. Caching

Cover:

- HTTP cache;
- freshness;
- validation;
- ETag;
- Last-Modified;
- cache-control at a high level;
- repository/database cache versus HTTP cache.

### 21. Connectivity and offline assumptions

Explain:

- connectivity signal does not guarantee endpoint success;
- do not gate every request only on network-status checks;
- offline-first design belongs to repository/storage coordination;
- user-facing connectivity state may still be useful.

### 22. Pagination

Explain:

- page/offset;
- cursor;
- next token;
- duplicate prevention;
- end-of-list;
- refresh;
- cancellation;
- Paging library boundary at a high level.

### 23. Uploads and downloads

Cover:

- streaming;
- progress;
- memory;
- file storage;
- cancellation;
- resumability where supported;
- large payload risks.

### 24. Observability and logging

Explain:

- request IDs;
- timing;
- redaction;
- no tokens or personal data in logs;
- debug versus production logging.

### 25. Testing

Cover:

- service contract tests;
- fake service;
- mock web server;
- mapper tests;
- repository tests;
- retry and timeout tests;
- authentication tests;
- malformed payload tests;
- cancellation tests.

### 26. Anti-patterns and decision guide

At minimum:

- Retrofit service in ViewModel;
- raw Response exposed upward;
- network DTO reused as UI model;
- retrying every failure;
- infinite token refresh loop;
- swallowing cancellation;
- disabled TLS verification;
- secrets in logs;
- connectivity check as source of truth;
- giant interceptor with business logic;
- hardcoded base URLs;
- no timeout;
- passing large response objects through navigation;
- loading whole files into memory;
- assuming 2xx body is always valid;
- treating all 4xx as the same domain error.

End with a concise decision checklist.

---

## Kotlin example requirements

Include at least:

1. service interface;
2. remote data source;
3. DTO;
4. DTO-to-domain mapper;
5. repository implementation;
6. cancellation-safe exception mapping;
7. timeout configuration example;
8. bounded retry example;
9. interceptor for common headers;
10. redacted logging example;
11. authentication token attachment;
12. token refresh coordination sketch;
13. ETag or conditional request example;
14. pagination model;
15. file download streaming example;
16. upload progress concept;
17. repository test;
18. mock-server service test;
19. malformed payload test;
20. cancellation test.

Examples must be conceptually compilable and version-aware.

Do not expose network-library types above the Data layer.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- HTTP request/response anatomy;
- method/idempotency guide;
- status-code guide;
- service/client/repository responsibilities;
- DTO/domain separation;
- error taxonomy;
- cancellation;
- timeout guide;
- retry checklist;
- interceptor/authenticator comparison;
- TLS checklist;
- caching;
- pagination;
- upload/download;
- testing;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Repository boundary

Refactor a ViewModel that directly uses a network service and raw response objects.

Require:

- service confinement;
- DTO mapping;
- repository contract;
- error mapping;
- cancellation ownership.

### Exercise 2 — Retry and idempotency

Given several operations, design retry policy for:

- GET profile;
- POST payment;
- PUT settings;
- upload;
- token refresh.

Require reasoning by failure type and idempotency.

### Exercise 3 — Authentication refresh

Design access-token refresh for concurrent 401 responses.

Require:

- one refresh in flight;
- waiting callers;
- refresh failure;
- recursion prevention;
- logout boundary;
- tests.

### Exercise 4 — Offline and pagination

Design repository behavior for paginated remote data with local cache.

Require:

- refresh;
- append;
- duplicate prevention;
- network failure;
- stale data;
- cancellation;
- tests.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

Do not provide complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 22–26 substantial questions.

Cover:

- Data-layer networking;
- HTTP methods;
- idempotency;
- status codes;
- service interface;
- HTTP client;
- DTOs;
- serialization;
- mapping;
- repository boundary;
- error taxonomy;
- cancellation;
- timeouts;
- retry;
- interceptors;
- authenticators;
- token refresh;
- TLS;
- pinning;
- caching;
- connectivity;
- pagination;
- uploads/downloads;
- logging;
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

1. layer boundary;
2. DTO versus domain model;
3. HTTP idempotency;
4. error taxonomy;
5. cancellation;
6. timeout and retry;
7. interceptor versus authenticator;
8. token refresh concurrency;
9. caching/offline;
10. pagination or file-transfer architecture.

Distractors must be plausible.

Explanations must teach architecture rather than library trivia.

---

## References

Use current primary sources.

At minimum inspect:

- HTTP semantics;
- Android network security configuration;
- Retrofit or equivalent service documentation;
- OkHttp or equivalent client documentation;
- serialization documentation;
- cancellation behavior;
- TLS guidance;
- caching;
- testing;
- Paging guidance where referenced.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 11 of 17.

The implementation report must record:

```text
Junior Core status after Task 023:
11 of 17 mandatory topics implemented as production packages in review.
6 mandatory topics remain.
```

Remaining mandatory topics:

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

- record Task 023 after successful validation;
- record eleven production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that six topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. HTTP and transport audit;
5. DTO/mapping/repository audit;
6. error/cancellation/timeout audit;
7. retry/idempotency audit;
8. authentication/TLS audit;
9. caching/pagination/file-transfer audit;
10. testing audit;
11. Junior Core progress audit;
12. exact counts;
13. validation;
14. UTF-8/mojibake audit;
15. deferred work;
16. literal `git status --short`;
17. recommended commit message.

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
- Networking stays inside Data-layer implementation.
- HTTP fundamentals are accurate.
- DTO and domain models are separated.
- Repository boundary is preserved.
- Error categories are distinct.
- Cancellation is preserved.
- Timeouts and retries are deliberate.
- Idempotency informs retry.
- Authentication refresh avoids loops and races.
- TLS guidance is safe.
- Caching and offline assumptions are accurate.
- Pagination and file transfer are covered.
- Testing is layered.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 11/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. HTTP/transport audit;
5. repository and error audit;
6. retry/auth/TLS audit;
7. caching/pagination/testing audit;
8. Junior Core progress;
9. exact counts;
10. validation results;
11. UTF-8 audit;
12. deferred work;
13. literal `git status --short`;
14. recommended commit message.

Do not commit.
