# Local Persistence with Room — Cheat Sheet

## Persistence decision

- What must survive process removal or device restart?
- What is required offline or for fast startup?
- Is the data user-created, authoritative local state, a cache, or history?
- Who owns mutation, freshness, conflicts, retention, backup, and deletion?
- Would memory or small saved reconstruction state satisfy the requirement?
- Is the schema/migration/privacy cost justified?

## Room architecture

```text
UI / optional Domain
        ↓
Repository policy
        ↓
Local data source
        ↓
DAO → Room → SQLite
```

Room adds compile-time query checks, mapping, async integrations, and migration
support over SQLite. SQL and relational modeling still determine correctness.

## Keep models distinct

| Model | Owns |
| --- | --- |
| entity | tables, columns, keys, constraints, persisted representation |
| network DTO | wire names, nullability, protocol version |
| domain/application model | validated application meaning and invariants |
| UI model/state | rendering and interaction state |

Map when independent evolution or invariants justify it. Do not reuse an entity
everywhere by default.

## Keys, constraints, and indices

- Natural key: meaningful and stable.
- Surrogate key: generated row identity.
- Remote ID: server identity; may not exist before sync.
- Composite key: identity across several columns, often a junction.
- Temporary ID: must have reconciliation and retry policy.
- `UNIQUE` encodes a constraint, not merely an optimization.
- Index measured filters, joins, ordering, and hot foreign-key lookups.
- Indices cost storage and every write; do not index every column.
- Review cascade behavior explicitly.

## DAO method guide

- Name use-case-specific queries and mutations.
- `suspend`: one-shot snapshot or bounded write.
- `Flow<T>`: cold observable query driven by table invalidation.
- Return nullable/empty/count values deliberately.
- Check affected-row counts when missing rows matter.
- Keep DAO/entity/Room types in Data by default.
- Avoid generic raw-query or universal CRUD contracts.

## Suspend versus Flow

| Need | DAO shape |
| --- | --- |
| one current snapshot | `suspend fun find(id): Entity?` |
| one insert/update/delete | `suspend fun ...` |
| current query result over time | `fun observe(...): Flow<Result>` |
| durable event history | explicit event table/query, not Flow emissions |

Room re-runs an observable query when a referenced table is invalidated. A
write may trigger an equal result; use domain-appropriate
`distinctUntilChanged()` when needed. Collection lifetime belongs to the
collector.

## Write/conflict guide

- `@Insert(ABORT)`: reject duplicate constraint violations.
- `@Update`: update matching primary key; inspect affected count.
- `@Upsert`: insert or update by key; available from Room 2.5.
- `REPLACE`: understand delete/reinsert and relationship consequences.
- SQL update: useful for targeted columns and compare-and-set conditions.
- Database conflict handling is not remote synchronization conflict policy.

## Transaction guide

- Use for a bounded multi-step persisted invariant.
- Exception/cancellation must roll back and propagate.
- Keep it short and database-only.
- Never call network, await UI, sleep, or do unbounded work inside.
- `@Transaction` is also used for consistent multi-query relation results.
- A transaction protects database atomicity/isolation.
- A `Mutex` protects only in-memory work using that same Mutex.

## Relation guide

- One-to-one/one-to-many: child foreign key.
- Many-to-many: junction table with composite key.
- `@Relation`: convenient multi-query aggregate; pair with `@Transaction`.
- `JOIN` projection: precise shape and often better for focused screens.
- `@Embedded`: flatten a cohesive value into columns; prefix collisions.
- Avoid deep nested graphs and N+1 loops.
- Choose CASCADE/RESTRICT/SET NULL/manual cleanup from product meaning.

## Type converters

- Store one-column values such as timestamps or stable value objects.
- Persist enums with a stable explicit representation and migration policy.
- Converter scope and built-ins are Room-version-sensitive.
- Never use opaque JSON to hide relational structure without a deliberate
  query/migration trade-off.

## Database lifecycle

- One database instance per process is the normal practice.
- Construct from application Context under application-scoped DI.
- Supply focused DAOs/local sources to repositories.
- Do not retain Activity Context or create a database per screen.
- Process death destroys objects, not the persisted file.
- Room/SQLite driver, executor, KMP, and API behavior is version-sensitive.

## Schema-version checklist

- Increment version for persisted schema changes.
- Export schema history and commit it.
- Review fresh-install and upgrade schemas.
- Preserve paths from every supported historical version.
- Define null/default/backfill and invalid legacy data.
- Recreate indices, foreign keys, and constraints.
- Test data meaning, not only final schema shape.
- Verify exact installed Room plugin/KSP configuration.

## Manual versus auto migration

| Manual migration | Auto migration |
| --- | --- |
| explicit SQL/data transformation | generated from exported schema diff |
| handles rebuild/copy/backfill rules | handles understood simple changes |
| supports complex semantic conversion | rename/delete ambiguity needs spec |
| must match selected driver API | available from Room 2.4 |

Auto generation still requires review and migration tests. Manual migration
cannot use generated DAOs and must match the installed Room driver API.

## Destructive migration warning

`fallbackToDestructiveMigration()` turns a missing migration path into
drop/recreate and data loss. Use only for explicitly disposable,
reconstructable data with product approval and tested recovery. Never add it
casually for user-created or authoritative local data.

## Repository/source-of-truth patterns

- local-first observation plus explicit refresh;
- stale-while-revalidate with content and refresh status;
- write-through after server confirmation;
- optimistic local write with durable pending state;
- remote-first with optional cache fallback;
- authoritative local user-created state.

No universal choice. Room does not decide freshness, authority, or error UX.
Fetch remotely before entering a local transaction; transactionally commit the
mapped local snapshot afterward.

## Offline/conflict checklist

- Which reads and writes work offline?
- What durable operation ID prevents duplicate retry?
- What are pending/sending/failed/confirmed states?
- What server version or precondition detects stale writes?
- Who wins or merges, and why?
- Is a conflict visible to the user?
- How are cancellation, partial failure, retry, and reconciliation handled?
- Are timestamps trustworthy for the chosen policy?

## Testing checklist

- fresh in-memory/device Room database per DAO test;
- representative null, ordering, constraint, and relation rows;
- transaction success and rollback;
- Flow invalidation and semantic equality;
- migration from every supported version with preserved/transformed data;
- fresh install versus migrated final schema;
- repository policy with deterministic local/remote fakes;
- cleanup and database close on every path.

Use real Room/SQLite for database behavior and fakes for repository policy.
Current Android guidance prefers device SQLite fidelity for database tests.

## Performance checklist

- read only needed rows and columns;
- push filtering, sorting, grouping, and aggregation into SQL;
- inspect `EXPLAIN QUERY PLAN`;
- index measured hot paths;
- use bounded/paged queries for large sets;
- avoid N+1 and deep nested relation graphs;
- batch related writes in a short transaction;
- measure representative data/device versions;
- evaluate WAL and durability trade-offs, not folklore.

## Security and backup

- Databases are normally app-private, not safe from a compromised process/device.
- Minimize sensitive columns and retention.
- Parameterize inputs; Room binds DAO parameters.
- Encryption needs a threat/key/recovery model and is not authorization.
- Define logout/account-removal deletion.
- Configure version-appropriate backup/device-transfer rules.
- Test restored sessions, device-bound keys, and server reconciliation.

## Common smells

- entity reused as DTO/domain/UI;
- DAO or database in ViewModel;
- database per screen;
- generic CRUD leaking everywhere;
- `REPLACE` without consequence analysis;
- network inside transaction;
- Mutex described as rollback;
- missing exported schemas or migration tests;
- destructive fallback for valuable data;
- JSON blob replacing relational modeling;
- no index on hot joins or index on every column;
- unbounded whole-table reads;
- N+1 relation loops;
- infinite Flow without an owner;
- Room expected to solve sync conflicts;
- mutable singleton database shared across tests.

## Interview-ready summary

Room is a Data-layer abstraction over SQLite. Design durable identity,
constraints, query shapes, and schema evolution first; expose use-case-oriented
DAO methods through a local source and repository; use suspend for one-shot
operations and Flow for invalidation-driven observation; keep transactions
short and database-only; map entities away from domain/UI contracts; test real
queries and every migration; and make offline, conflict, performance, security,
backup, and destructive-data decisions explicit.
