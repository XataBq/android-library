# Task 027 — Local Persistence with Room implementation report

## Implementation summary

**PASS**

Task 027 adds the fifteenth production educational topic in `review`. It
teaches local persistence as a data-modeling, consistency, ownership,
evolution, and verification problem:

```text
persistent schema
→ DAO contract
→ local data source
→ mapper
→ repository policy
→ domain model
```

Room is presented as a checked abstraction over SQLite, not as a replacement
for relational design or as the application's universal model.

## Changed files

Created the six canonical files under
`content/android/data/android-local-persistence-with-room/` and this report.
Updated `README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and Task 027 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test-infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the version 2 canonical
Android architecture competency set, all fourteen preceding production topics,
Tasks 016–026, and their relevant implementation reports were inspected.

Primary canonical coverage:

- `design-data-layer-around-repositories`;
- `explain-persistent-data-models`;
- `use-coroutines-and-flows-across-layers`.

Strongly reinforced:

- `apply-separation-of-concerns`;
- `evaluate-optional-domain-layer`;
- `design-viewmodel-ui-state`.

Framework isolation and UI-layer responsibilities are contextually reinforced.
No competency or production competency-to-topic mapping changed.

Current official Android Developers documentation was inspected for Room and
SQLite, entities, DAOs, asynchronous queries, transactions, relationships,
type converters, Upsert, schema export, manual and auto migrations,
MigrationTestHelper, database testing, Paging integration, SQLite performance,
Data-layer ownership, storage, and backup. All 19 metadata references are
official documentation and use the actual inspection date `2026-07-24`.

Stable persistence principles are separated from Room-version-specific APIs.
The content records that auto migrations require Room 2.4+, `@Upsert` requires
Room 2.5+, and migration/testing connection APIs, schema configuration,
drivers, converters, and Paging integration must be checked against installed
artifacts.

## Entity, schema, and DAO audit

Persistence decisions cover process removal, offline use, startup, user-created
or authoritative local data, deliberate caches, history, retention, deletion,
and cases where memory or saved reconstruction state is sufficient.

Entities define persisted table/column names, nullability, SQL defaults,
primary keys, foreign keys, constraints, and stable meanings. Natural,
surrogate, remote, composite, and temporary local identity are distinguished.
Unique constraints and query-supported indices are separated from
over-indexing and write/storage cost. Cascade behavior requires product review.

Entity, DTO, domain, and UI models remain independent by default. Mapping
confines SQLite representation and application invariants without requiring
ceremonial duplicates for every trivial private shape.

DAOs expose use-case-oriented typed queries and mutations. One-shot suspend
snapshots/writes, null/empty/count behavior, conflict strategies, targeted
updates, and version-aware Upsert are explicit. DAO, entity, Room, Cursor, and
raw SQL types do not cross into ViewModel or Domain by default.

## Flow, transaction, and relation audit

Room Flow queries are described as cold observable queries. Collection starts
observation; relevant-table invalidation causes re-execution, and an update to
a row outside the result can still produce a semantically equal result.
`distinctUntilChanged` is applied only at a boundary with suitable equality.
Flow is not presented as one event per write, and collection lifetime remains
caller-owned.

Transactions protect bounded database atomicity and rollback. Exceptions and
cancellation propagate. Network requests, UI waits, sleeps, and unbounded work
remain outside transactions. A transaction is distinguished from a coroutine
Mutex: the former protects persisted consistency; the latter serializes only
participating in-memory code.

One-to-one, one-to-many, and many-to-many use foreign keys, deliberate deletion
semantics, indexed lookup paths, and junction composite keys. Transactional
`@Relation` aggregates, joins, `@Embedded`, and focused projections are
selected according to query shape. Deep nested graphs and N+1 reads are
explicit performance risks. Type converters are restricted to values that
belong in one column rather than opaque relational JSON.

## Migration audit

Every persisted schema change has a version, exported historical schema,
supported path, release review, and migration evidence. Fresh installs and
upgrades from historical versions must converge on compatible schema and data
meaning.

Manual migration covers create/copy/backfill/drop/rename, required defaults,
invalid legacy data, constraints, indices, and migration chains. The example
uses the classic Android `SupportSQLiteDatabase` path while explicitly
directing learners using a driver-backed Room version to implement its required
`SQLiteConnection` contract.

Auto migration is limited to changes Room can infer from exported schemas.
Ambiguous rename/delete uses an `AutoMigrationSpec`; semantic transforms remain
manual. Generated migrations still require review and old-data tests.

Destructive fallback is presented as data loss. It is permitted only for
explicitly disposable, reconstructable data with product approval and tested
recovery—not user-created or authoritative local state.

## Repository, offline, and conflict audit

The repository owns local-first, stale-while-revalidate, write-through,
remote-first, or authoritative-local policy. A Room database is not
automatically a correct source of truth. Freshness, stale UI, refresh failure,
field ownership, deletion, and reconciliation stay explicit.

The local-first example fetches and maps remotely before entering a short Room
transaction that commits local effects. No network call appears inside a
database transaction.

Offline writes require durable operation identity, pending/sending/failed/
confirmed state, server versions or preconditions, idempotent retry, and
conflict policy. Server-wins, client-wins, last-write-wins, merge, reject, or
user-visible resolution are selected from domain meaning. Room persists the
chosen state but does not solve distributed conflict policy.

## Testing and performance audit

Real Room/device SQLite tests own query, constraint, relation, transaction,
invalidation, and migration risks. Each DAO test gets a fresh database and
closes it. Transaction rollback, representative old data, final schema and
transformed values, every supported path, and fresh-versus-migrated
convergence are covered. Repository policy continues to use deterministic
local/remote fakes.

Performance guidance reads only required rows/columns, moves filtering and
aggregation to SQL, uses bounded pagination, replaces N+1 loops with
joins/projections or deliberate relations, batches writes in short
transactions, and adds indices from measured query plans. Learners use
representative data, device SQLite, query timing, and `EXPLAIN QUERY PLAN`
rather than guessing. WAL is kept at a high-level measured trade-off.

## Security and backup audit

Room databases normally use app-private storage without claiming protection
from a compromised app process or device. Sensitive columns and retention are
minimized. Parameterized DAO queries, logout/account deletion, export/sharing,
encryption threat/key/recovery policy, and restored-session reconciliation are
covered. Database encryption is not authorization.

Backup and device-transfer rules are version- and transport-sensitive.
Sensitive/session databases may be excluded, and restore behavior is tested
for invalid credentials and device-bound keys.

## Junior Core progress audit

Junior Core status after Task 027:
15 of 17 mandatory topics implemented as production packages in review.
2 mandatory topics remain.

The remaining mandatory topics are:

16. Background Work and WorkManager
17. Compose Foundations

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grading schema, production mapping, or catalog
output was introduced.

## Exact counts

- Package files: 6.
- Numbered theory sections: 26.
- Meaningful Kotlin/SQL code blocks/categories in theory: 32
  (31 Kotlin, 1 SQL).
- Practice exercises: 4.
- Interview questions: 26.
- Test questions: 10.
- Official references: 19.
- Taxonomy: `android` / `data`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 240 minutes.
- Prerequisites: 9.
- Production topic packages after Task 027: 15.
- Mandatory Junior Core topics remaining: 2.

The taxonomy, metadata, and prerequisites are schema-valid. Every prerequisite
exists and the graph remains acyclic.

## Validation

```text
python -B scripts/validate_content.py
PASS — 15 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

## UTF-8 and mojibake audit

All new or modified repository Markdown/YAML source files decode as strict
UTF-8 without BOM. They contain none of the checked mojibake sequences. The
new topic and review diff contain no absolute local path.

## Deferred work

The two remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, AI tutor, advanced synchronization,
and specialized database security/performance review remain deferred.
Dedicated WorkManager and Compose topics retain their full content scope.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/data/android-local-persistence-with-room/cheat-sheet.md
 A content/android/data/android-local-persistence-with-room/interview.md
 A content/android/data/android-local-persistence-with-room/practice.md
 A content/android/data/android-local-persistence-with-room/test.yaml
 A content/android/data/android-local-persistence-with-room/theory.md
 A content/android/data/android-local-persistence-with-room/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-027-android-local-persistence-with-room-implementation.md
 A tasks/027-add-android-local-persistence-with-room-topic.md
?? 027-codex-prompt.md
?? 027-review.diff
```

## Recommended commit message

```text
feat(content): add Room persistence foundations topic
```
