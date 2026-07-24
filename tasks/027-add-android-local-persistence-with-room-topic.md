# Task 027 — Add Local Persistence with Room Topic

Status: DONE

## Objective

Add the fifteenth production educational topic in the Junior Core:

```text
android-local-persistence-with-room
```

The topic must explain local persistence as a data-modeling, consistency, ownership, and migration problem rather than as annotation memorization.

The learner must understand:

- when local persistence is justified;
- Room architecture;
- entities;
- DAO contracts;
- queries;
- transactions;
- relations;
- type converters;
- schema evolution;
- migrations;
- destructive migration risks;
- Flow observation;
- repository boundaries;
- offline-first coordination;
- conflict and freshness policy;
- testing;
- performance;
- security and backup implications.

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
- Coroutines;
- Flow;
- Networking Architecture;
- Dependency Injection and Scoping;
- Testing Foundations;
- Security Foundations.

---

## Core teaching position

A database is not a cache API and Room is not the domain model.

The core model is:

```text
persistent schema
→ DAO contract
→ local data source
→ mapper
→ repository policy
→ domain model
```

The topic must preserve these distinctions:

```text
database entity
≠ domain model
≠ network DTO
≠ UI model

transaction
≠ coroutine mutex

schema migration
≠ data refresh

local source of truth
≠ automatically correct source of truth
```

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
- Tasks 016–026.

Use current official or primary documentation for:

- Room;
- entities and DAO;
- observable queries;
- transactions;
- relationships;
- type converters;
- schema export;
- migrations;
- auto migrations;
- destructive fallback behavior;
- database testing;
- performance guidance;
- prepackaged databases where referenced.

Do not fabricate API guarantees.

Do not fabricate access dates.

Clearly distinguish stable persistence principles from Room-specific APIs and version-sensitive behavior.

---

## Canonical competency scope

Primary:

```text
design-data-layer-around-repositories
explain-persistent-data-models
use-coroutines-and-flows-across-layers
```

Strongly reinforced:

```text
apply-separation-of-concerns
evaluate-optional-domain-layer
design-viewmodel-ui-state
```

Contextually reinforced:

```text
isolate-android-framework-dependencies
explain-ui-layer-responsibilities
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/data/android-local-persistence-with-room/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: data` is required, keep it and document the taxonomy choice.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-local-persistence-with-room
title: Local Persistence with Room
track: android
section: data
difficulty: foundation
status: review
estimated_minutes: 240
content_version: 1
prerequisites:
  - android-data-layer-repositories-and-synchronization
  - android-domain-layer-and-use-cases
  - android-viewmodel-and-ui-state
  - kotlin-coroutines-foundations
  - kotlin-flow-and-reactive-streams
  - android-networking-architecture
  - android-dependency-injection-and-scoping
  - android-testing-foundations
  - android-security-foundations
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain when local persistence is justified.
2. Explain Room's role over SQLite.
3. Design entities deliberately.
4. Distinguish entity, DTO, domain model, and UI model.
5. Design DAO interfaces by use case.
6. Use suspend and Flow-returning DAO methods appropriately.
7. Explain observable query invalidation.
8. Use transactions for multi-step atomic work.
9. Distinguish database transactions from in-memory synchronization.
10. Model one-to-one, one-to-many, and many-to-many relationships.
11. Use embedded objects and relation projections deliberately.
12. Use type converters only for suitable value types.
13. Design indices, keys, and constraints.
14. Explain schema versioning.
15. Design and test migrations.
16. Explain auto migration limits.
17. Avoid unsafe destructive fallback.
18. Coordinate local and remote data in repositories.
19. Define freshness, staleness, and source-of-truth policy.
20. Handle conflicts and writes.
21. Test DAO, transaction, migration, and repository behavior.
22. Recognize persistence anti-patterns.

---

## Theory requirements

`theory.md` must contain approximately 22–26 substantial sections.

Required coverage:

### 1. Why persist data

Explain:

- process death;
- offline use;
- fast startup;
- user-created state;
- authoritative local data;
- cache;
- audit/history where appropriate.

Also explain when persistence is unnecessary.

### 2. Room and SQLite

Explain Room as a compile-time-checked abstraction over SQLite, not a replacement for relational modeling knowledge.

### 3. Database boundary

Show:

```text
Repository
→ local data source
→ DAO
→ Room
→ SQLite
```

No DAO or entity types should cross into UI or Domain by default.

### 4. Entities

Cover:

- table mapping;
- primary keys;
- nullable columns;
- defaults;
- column names;
- immutable data objects where practical;
- schema stability.

### 5. Entity versus domain model

Explain separate evolution and mapping.

### 6. Keys and identity

Cover:

- natural key;
- surrogate key;
- remote ID;
- composite key;
- local temporary ID;
- identity stability.

### 7. Indices and uniqueness

Explain:

- lookup performance;
- unique constraints;
- write cost;
- over-indexing;
- foreign-key indices.

### 8. DAO contracts

Explain use-case-oriented methods rather than exposing generic CRUD everywhere.

### 9. Suspend DAO methods

Explain one-shot read/write semantics.

### 10. Flow DAO methods

Explain:

- observable query;
- invalidation-driven re-execution;
- cold Flow behavior;
- emissions after relevant table changes;
- no guarantee that every write produces a distinct semantic value;
- collection ownership.

### 11. Inserts, updates, deletes, and upserts

Explain conflict behavior and policy.

Be version-aware around convenience APIs.

### 12. Transactions

Explain atomicity for multi-step database work.

Cover `@Transaction`, transaction-returning query models, rollback, and coroutine ownership.

### 13. Transaction versus Mutex

Explain database isolation versus in-memory critical section.

### 14. Relationships

Cover:

- one-to-one;
- one-to-many;
- many-to-many;
- junction tables;
- foreign keys;
- cascade risks.

### 15. Embedded objects and projections

Explain `@Embedded`, partial projections, and avoiding giant aggregate loads.

### 16. Type converters

Explain appropriate uses:

- value objects;
- enums with migration strategy;
- timestamps.

Warn against storing opaque JSON blobs instead of relational modeling without a clear reason.

### 17. Database class and lifecycle

Explain singleton-per-process practice, DI ownership, process death, and no Activity Context leakage.

### 18. Threading and dispatch

Explain Room's suspend/Flow integration, main-thread restrictions, and avoiding redundant dispatcher folklore where Room already manages query execution.

Be precise and version-aware.

### 19. Schema versioning

Explain:

- schema version;
- exported schema;
- migration path;
- historical versions;
- release discipline.

### 20. Manual migrations

Cover:

- SQL transformation;
- rename/copy/rebuild patterns;
- data preservation;
- validation;
- migration chain.

### 21. Auto migrations

Explain what they can automate and where explicit specifications or manual migration are required.

Do not present them as universally sufficient.

### 22. Destructive migration

Explain:

- data loss;
- acceptable disposable-cache cases;
- production user-data risk;
- explicit product decision;
- no casual fallback.

### 23. Repository and source of truth

Explain:

- local-first observation;
- refresh;
- write-through;
- stale-while-revalidate;
- remote-only fallback;
- authoritative local data.

No universal policy.

### 24. Offline-first and conflict policy

Cover:

- pending writes;
- sync state;
- server version;
- timestamps;
- idempotency;
- merge/reject/last-write policies;
- user-visible conflict where needed.

Do not preempt advanced distributed systems depth.

### 25. Testing and performance

Testing:

- in-memory database;
- real SQLite behavior;
- DAO tests;
- transaction rollback;
- migration tests;
- repository tests;
- cleanup.

Performance:

- query shape;
- indices;
- pagination;
- avoiding N+1;
- large result sets;
- batching;
- WAL at a high level only where relevant;
- measuring rather than guessing.

### 26. Security, backups, anti-patterns, and decision guide

Security and backups:

- private app storage;
- sensitive columns;
- encryption threat model;
- backup rules;
- logout deletion;
- compromised-device limitations.

Anti-patterns at minimum:

- entity reused everywhere;
- DAO in ViewModel;
- database on every screen;
- `fallbackToDestructiveMigration` for user data;
- missing migration tests;
- opaque JSON blobs for relational data;
- giant transaction;
- transaction around network call;
- no indices on hot foreign-key lookups;
- indexing every column;
- collecting infinite Flow without lifecycle owner;
- whole-table load for paging use case;
- assuming Room solves conflict policy;
- relying on database encryption as authorization;
- mutable singleton database state in tests.

End with:

```text
What data must survive?
Who owns the schema?
What is the identity?
Which constraints must the database enforce?
What is observed as Flow?
What must be atomic?
How does schema evolve?
What happens offline?
How is data migrated and tested?
What data may be deleted?
```

---

## Kotlin/SQL example requirements

Include at least:

1. entity;
2. composite-key entity;
3. indexed entity;
4. DAO suspend query;
5. DAO Flow query;
6. insert/update/upsert policy;
7. transaction;
8. transaction rollback test;
9. one-to-many relation;
10. many-to-many junction;
11. projection;
12. type converter;
13. database class;
14. DI provider;
15. entity-domain mapper;
16. repository local-first Flow;
17. refresh transaction;
18. manual migration;
19. auto-migration declaration;
20. migration test;
21. in-memory DAO test;
22. pagination query;
23. N+1 anti-pattern and correction;
24. destructive migration anti-pattern.

Examples must be conceptually compilable and version-aware.

Do not mix network calls inside a database transaction.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- persistence decision checklist;
- Room architecture;
- entity/domain/DTO distinction;
- keys and indices;
- DAO method guide;
- suspend versus Flow;
- transaction guide;
- relation guide;
- type-converter rules;
- schema-version checklist;
- manual versus auto migration;
- destructive migration warning;
- repository/source-of-truth patterns;
- offline/conflict checklist;
- testing checklist;
- performance checklist;
- security/backup checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Entity and DAO design

Design persistence for users, projects, and memberships.

Require:

- keys;
- relationships;
- indices;
- constraints;
- DAO methods;
- projections;
- mapping boundary.

### Exercise 2 — Migration review

Given a schema change that renames a column, splits one field, and adds a required column:

Require:

- migration strategy;
- data backfill;
- rollback risk;
- migration test;
- auto/manual migration decision.

### Exercise 3 — Offline repository

Design repository behavior for a list that must render cached data immediately and refresh from network.

Require:

- local source of truth;
- refresh policy;
- stale state;
- error handling;
- transaction boundary;
- Flow ownership;
- tests.

### Exercise 4 — Persistence performance audit

Review a feature with whole-table loads, missing indices, N+1 relation reads, and repeated writes.

Require:

- query redesign;
- indices;
- pagination;
- batching;
- measurement plan;
- correctness checks.

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

- Room versus SQLite;
- persistence decisions;
- entities;
- domain mapping;
- keys;
- indices;
- DAO design;
- suspend/Flow;
- invalidation;
- transactions;
- Mutex comparison;
- relationships;
- converters;
- lifecycle/DI;
- schema versioning;
- migrations;
- auto migrations;
- destructive fallback;
- repository source of truth;
- offline-first;
- conflict policy;
- testing;
- performance;
- security/backups;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where useful.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. entity versus domain model;
2. keys and indices;
3. suspend versus Flow DAO;
4. transaction semantics;
5. relationship modeling;
6. type converters;
7. migration strategy;
8. destructive migration;
9. local source of truth/offline behavior;
10. testing and performance.

Distractors must be plausible.

Explanations must teach persistence design, not annotation trivia.

---

## References

Use current primary sources.

At minimum inspect:

- Room overview;
- entities;
- DAO;
- asynchronous queries;
- relationships;
- transactions;
- type converters;
- migrations;
- auto migrations;
- schema export;
- migration testing;
- database testing;
- performance guidance.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 15 of 17.

The implementation report must record:

```text
Junior Core status after Task 027:
15 of 17 mandatory topics implemented as production packages in review.
2 mandatory topics remain.
```

Remaining mandatory topics:

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

- record Task 027 after successful validation;
- record fifteen production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that two topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. entity/schema/DAO audit;
5. Flow/transaction/relation audit;
6. migration audit;
7. repository/offline/conflict audit;
8. testing/performance audit;
9. security/backup audit;
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
- Room is presented as a persistence boundary over SQLite.
- Entities are distinct from domain models.
- DAO contracts are use-case-oriented.
- Flow invalidation semantics are accurate.
- Transactions are distinguished from Mutex.
- Relationships and converters are used deliberately.
- Schema versioning and migrations are central.
- Destructive migration risk is explicit.
- Repository/source-of-truth policy is clear.
- Offline and conflict policy are covered.
- Testing and performance are practical.
- Security and backups are acknowledged.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 15/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. entity/schema/DAO audit;
5. Flow/transaction/relation audit;
6. migration audit;
7. repository/offline/conflict audit;
8. testing/performance/security audit;
9. Junior Core progress;
10. exact counts;
11. validation results;
12. UTF-8 audit;
13. deferred work;
14. literal `git status --short`;
15. recommended commit message.

Do not commit.
