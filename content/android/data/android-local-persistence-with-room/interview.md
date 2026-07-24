# Local Persistence with Room — Interview Questions

## 1. When is local persistence justified?

**Strong answer:** When named data must survive process/device restart, support
offline behavior or startup, retain user-created/authoritative state, or serve
an intentional cache/history with retention and deletion policy.

**Weak answer:** Every model should be stored because disk is cheap.

**Follow-up:** When are memory and saved state enough?

## 2. What is Room's relationship to SQLite?

**Strong answer:** Room is a compile-time-checked mapping, DAO, async, and
migration abstraction over SQLite. Relational schema, SQL, indices,
transactions, and query plans still determine correctness and performance.

**Weak answer:** Room replaces the need to understand SQL.

## 3. What should a Room entity represent?

**Strong answer:** A stable persisted row/table contract with deliberate
primary key, columns, names, nullability, defaults, constraints, and schema
evolution.

**Weak answer:** The one universal model used by network, domain, and UI.

## 4. Why separate entity and domain model?

**Strong answer:** Persistence representation, network protocol, application
invariants, and presentation evolve independently. Mapping confines those
changes and validation to a boundary.

**Weak answer:** Rename the entity `DomainModel` and expose it everywhere.

## 5. How do you choose a primary key?

**Strong answer:** From identity stability: natural, surrogate, remote,
composite, or temporary local identity, including foreign references and
offline reconciliation.

**Weak answer:** Always use an auto-increment integer regardless of domain.

## 6. What do uniqueness and indices provide?

**Strong answer:** Uniqueness enforces a data invariant. Indices accelerate
specific lookup/join/order patterns at storage and write cost. Use measured
query plans and index hot foreign-key columns.

**Weak answer:** Index every column because reads become free.

## 7. What makes a good DAO contract?

**Strong answer:** Use-case-oriented, typed read/write methods with explicit
ordering, filtering, null/empty/count, conflict, and atomicity semantics,
remaining behind the Data boundary.

**Weak answer:** One generic CRUD DAO shared directly by every ViewModel.

## 8. When should a DAO method be suspend?

**Strong answer:** For a one-shot snapshot or bounded insert/update/delete. The
return contract should state missing rows, counts, and constraint failures.

**Weak answer:** Suspend makes a query observable forever.

## 9. How does a Flow DAO query work?

**Strong answer:** Collection starts a cold observable query. Room tracks
referenced tables, reruns after invalidation, and emits the new result; an
unrelated row update can trigger an equal result.

**Weak answer:** It emits exactly one event for every changed row.

**Follow-up:** Where can `distinctUntilChanged` belong?

## 10. Compare insert, update, upsert, and replace.

**Strong answer:** Insert creates and applies a declared conflict strategy;
update targets an existing key; upsert inserts or updates by key; replace can
delete/reinsert. Choose according to data invariants and Room version.

**Weak answer:** `REPLACE` is always the safest upsert.

## 11. What does a database transaction guarantee?

**Strong answer:** Atomic commit/rollback for bounded database operations under
SQLite transaction semantics. Keep it short, propagate cancellation/failure,
and never wait on network or UI inside it.

**Weak answer:** It rolls back an HTTP request made in the block.

## 12. How does a transaction differ from Mutex?

**Strong answer:** A transaction protects persisted consistency across database
connections/operations. A Mutex serializes in-memory code that shares that
Mutex and provides no database rollback.

**Weak answer:** They are interchangeable locking syntax.

## 13. How do you model one-to-many?

**Strong answer:** Put a foreign key on the child, index hot lookup columns,
choose deletion semantics, and query through a join/projection or a
transactional `@Relation` aggregate.

**Weak answer:** Store child objects as a JSON list in the parent.

## 14. How do you model many-to-many?

**Strong answer:** Use a junction table with both foreign keys and normally a
composite primary key, then query with joins or `@Relation`/`@Junction`.

**Weak answer:** Duplicate each full object into the other table.

## 15. When are `@Embedded` and projections useful?

**Strong answer:** Embedded flattens a cohesive value into columns. A
projection selects the exact columns/aggregate needed, reducing coupling and
oversized loads.

**Weak answer:** Always load a complete nested entity graph for every screen.

## 16. What belongs in a type converter?

**Strong answer:** A value that semantically fits one column, such as a
timestamp or stable value object. Its stored form needs version and migration
policy.

**Weak answer:** The whole relational graph serialized to opaque JSON.

## 17. Who owns the Room database lifecycle?

**Strong answer:** An application-scoped composition/DI owner builds normally
one instance per process using application Context and supplies DAOs/local
sources. Screens do not construct or retain it.

**Weak answer:** Each Activity creates and closes its own singleton.

## 18. Should every suspend DAO call use `withContext(IO)`?

**Strong answer:** No. Room's suspend/Flow integration owns query execution and
blocks main-thread access by default. Add dispatcher boundaries only for work
outside Room that actually needs them, checking the installed version/driver.

**Weak answer:** Nested IO switching is required for every Room annotation.

## 19. Why export Room schema history?

**Strong answer:** It records exact historical schemas for review, auto
migration, migration testing, and convergence between fresh and upgraded
installs.

**Weak answer:** Only the latest entity source matters after release.

## 20. When do you need a manual migration?

**Strong answer:** For complex or semantic transformations, backfills,
rebuild/copy operations, and changes auto migration cannot infer safely.
Preserve constraints, data meaning, and all supported paths.

**Weak answer:** Change the entity and let users reinstall.

## 21. What can auto migration do?

**Strong answer:** From Room 2.4 it can generate understood changes from
exported schema diffs. Ambiguous rename/delete needs a spec; semantic data
transformation may need manual SQL. It still requires review and tests.

**Weak answer:** It can infer any business transformation from property names.

## 22. When is destructive migration acceptable?

**Strong answer:** Only for explicitly disposable, reconstructable data with
product approval, recovery behavior, and tests. It is data loss and is unsafe
for user-created or authoritative local state.

**Weak answer:** Whenever writing a migration takes too long.

## 23. How can Room be a local source of truth?

**Strong answer:** The repository exposes local observation and commits mapped
remote results according to explicit freshness/write policy. The database owns
the observable copy; the repository owns coordination; remote authority may
still exist.

**Weak answer:** Installing Room automatically makes every local row correct.

## 24. What does offline write support require?

**Strong answer:** Durable operation identity/state, idempotent retry,
sync/error status, server versions/preconditions, conflict policy,
reconciliation, and user-visible outcomes where necessary.

**Weak answer:** Queue a lambda in memory and use last timestamp wins.

## 25. How should Room behavior be tested?

**Strong answer:** Use real device Room/SQLite for queries, constraints,
transactions, invalidation, and migrations; seed representative old versions,
verify schema plus data, isolate/close databases, and fake sources for
repository policy.

**Weak answer:** Mock every DAO and assume migration annotations work.

**Follow-up:** Why compare a fresh install with a fully migrated database?

## 26. How do you review persistence performance and security?

**Strong answer:** Measure query count/time/plans and rows/columns, index real
paths, page/batch, avoid N+1 and giant transactions; minimize sensitive data,
define encryption/backup/logout policy, and test on representative devices.

**Weak answer:** Add indices everywhere, enable encryption, and performance and
authorization are solved.
