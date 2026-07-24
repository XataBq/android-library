# Practice — Local Persistence with Room

## Exercise 1 — Entity and DAO design

### Goal

Design persistence for users, projects, and project memberships without
exposing Room models as the application contract.

### Scenario

Users can belong to many projects and have one role per membership. Projects
can be created offline with a temporary identity and later receive a remote ID.
The list screen needs project name, member count, and the current user's role.

### Constraints

- Choose stable local, optional remote, natural/surrogate, and composite keys.
- Model one-to-many and many-to-many relationships with foreign keys and a
  membership junction.
- Define uniqueness, nullability, deletion behavior, and indices for real query
  paths.
- Design suspend writes and one-shot reads plus a Flow summary query.
- Include a focused projection rather than loading every user entity.
- Define temporary-to-remote identity reconciliation.
- Keep entities, DAO types, DTOs, domain models, and UI state distinct.
- Specify constraint, relation, ordering, and invalidation tests.

### Expected deliverable

An entity/key diagram, Room entity and projection sketches, use-case-oriented
DAO contract, mapper boundary, and database-test matrix.

### Evaluation criteria

- every identity and constraint has a stated reason;
- the junction prevents duplicate membership;
- indices match demonstrated queries;
- DAO methods do not expose generic CRUD policy;
- projection avoids an oversized object graph;
- application consumers do not depend on Room entities.

### Optional hints

- A remote ID can be unique without being the local primary key.
- Count and role can be produced by one join/grouped projection.

## Exercise 2 — Migration review

### Goal

Design and verify a migration that renames a column, splits one field, and adds
a required column.

### Scenario

Schema version 3 stores `contacts.full_name`. Version 4 needs `given_name`,
`family_name`, and non-null `normalized_name`. Existing values include
single-word names, multiple spaces, Unicode, and empty strings.

### Constraints

- Decide which changes are unambiguous and which require manual data logic.
- Define create/copy/backfill/drop/rename or another safe SQL sequence.
- Preserve IDs, foreign keys, uniqueness, and indices.
- Specify policy for ambiguous/invalid legacy names.
- Explain whether an `AutoMigrationSpec` is enough or manual migration is
  required for the split.
- Cover upgrades from every supported earlier version to the latest.
- Seed representative version-3 rows and assert final schema plus data.
- Analyze rollback/release risk and recovery without destructive fallback.
- Check installed Room migration/helper APIs.

### Expected deliverable

A migration decision record, SQL transformation outline, data-backfill table,
version-path graph, migration tests, and release/rollback risk notes.

### Evaluation criteria

- no existing row is silently discarded;
- ambiguous input has explicit product meaning;
- final constraints and indices are recreated;
- auto/manual choice matches transformation complexity;
- tests verify values and schema;
- destructive migration is not used to hide a missing path.

### Optional hints

- A compiler cannot infer how a human name should be split.
- Compare fresh-version-4 schema with a migrated database.

## Exercise 3 — Offline repository

### Goal

Design a repository whose list renders cached data immediately and refreshes
from the network without putting network work inside a database transaction.

### Scenario

An article list must work offline. Cached rows have a last-refresh marker.
Refresh can fail, server rows can be deleted, and two screens can observe the
same list. Users can bookmark articles locally while refresh is running.

### Constraints

- Choose whether Room is the local observable source of truth.
- Define fresh, stale, empty, refreshing, and failed-refresh behavior.
- Expose a mapped repository Flow and assign collection/sharing ownership.
- Fetch and map remotely before a bounded local transaction.
- Preserve local-only bookmark state while replacing server-owned fields.
- Define deletion/tombstone and partial-failure policy.
- Bound/coordinate concurrent refresh without treating a Mutex as a database
  transaction.
- Cover cancellation and do not swallow it as refresh failure.
- Test repository policy with fakes and DAO/transaction behavior with Room.

### Expected deliverable

A read/write sequence diagram, ownership table, freshness policy, transactional
commit outline, observable state contract, and focused test portfolio.

### Evaluation criteria

- useful stale content survives refresh failure;
- remote and local-only field ownership is explicit;
- no network call occurs inside a transaction;
- concurrent observation does not duplicate hidden policy;
- transaction and refresh coordination solve distinct invariants;
- tests cover empty cache, stale data, deletion, cancellation, and rollback.

### Optional hints

- Replace only server-owned columns or merge rows before the transaction.
- “Connected” is not proof that refresh will succeed.

## Exercise 4 — Persistence performance audit

### Goal

Repair a persistence design with whole-table loads, missing indices, N+1
relation reads, and repeated individual writes.

### Scenario

A task screen loads every row and filters in Kotlin, fetches labels once per
task, sorts by an unindexed project/status/date combination, and inserts a
2,000-row refresh one row at a time. Performance degrades with real data.

### Constraints

- Redesign queries to select only required rows and columns.
- Replace N+1 reads with a join/projection or justified relation query.
- Add only indices supported by query and write measurements.
- Define bounded pagination with deterministic ordering.
- Batch related writes inside a short transaction.
- Preserve constraints, observable-query correctness, and cancellation.
- Measure representative sizes on relevant device SQLite versions.
- Use query timing and `EXPLAIN QUERY PLAN`.
- Include regression tests for ordering, duplicates, boundaries, and rollback.
- Do not select WAL or dispatcher changes without a measured invariant.

### Expected deliverable

A before/after query plan, index rationale, projection/pagination contract,
batch-write design, measurement protocol, and correctness/performance tests.

### Evaluation criteria

- work moves to SQL without changing results;
- query count is bounded rather than proportional to rows;
- pagination order is stable;
- indices improve measured plans without excessive write cost;
- batched writes remain atomic;
- performance evidence and correctness evidence are both present.

### Optional hints

- Start by counting queries and bytes/rows returned.
- An index order should reflect actual filtering and ordering prefixes.
