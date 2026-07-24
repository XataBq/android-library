# Local Persistence with Room

Room is useful only after the persistence problem is defined. The durable path
in this topic is:

```text
persistent schema
→ DAO contract
→ local data source
→ mapper
→ repository policy
→ domain model
```

The database schema, network protocol, domain language, and screen state evolve
for different reasons. Keeping those boundaries explicit prevents an
annotation change from becoming an application-wide contract.

## 1. Decide why data must persist

Persistence is justified when data must survive process removal, support
offline reads, speed startup, retain user-created work, serve as authoritative
local state, maintain a deliberate cache, or preserve required history.
“Maybe useful later” is not enough: persistence adds schema evolution, cleanup,
privacy, backup, testing, and corruption behavior.

```kotlin
data class PersistenceDecision(
    val mustSurviveProcessRemoval: Boolean,
    val neededOffline: Boolean,
    val owner: String,
    val retention: Duration,
    val deletionTrigger: String,
)
```

Keep transient rendering state in memory. Use saved state for small
reconstruction inputs, not database snapshots. A remote-only value may not
need a local copy when offline behavior and startup latency do not justify it.
An audit trail requires an explicit product and security requirement; do not
retain sensitive history by accident.

## 2. Room is an abstraction over SQLite

SQLite remains the relational engine. Room adds compile-time query checking,
entity/DAO mapping, asynchronous integrations, migrations, and test support.
It does not choose keys, normalize relations, define conflict policy, or make
an inefficient query efficient.

```sql
CREATE TABLE projects (
    project_id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    updated_at_epoch_ms INTEGER NOT NULL
);
```

Understand tables, rows, keys, constraints, joins, transactions, indices, query
plans, and migration SQL. Room should reduce unsafe boilerplate without hiding
the data model.

## 3. Keep the database behind the Data layer

The normal dependency path is:

```text
UI / optional Domain
        ↓
Repository
        ↓
Local data source
        ↓
DAO → Room → SQLite
```

```kotlin
interface ProjectLocalDataSource {
    fun observeProjects(): Flow<List<ProjectRecord>>
    suspend fun replaceProjects(records: List<ProjectRecord>)
}
```

ViewModels and use cases do not receive a DAO, `RoomDatabase`, entity,
`Cursor`, or raw SQL result by default. A local data source can confine
Room-specific vocabulary, while the repository owns whether local data is a
cache, source of truth, or one participant in synchronization.

## 4. Entities define persistent rows

An entity maps a class to a table. Choose explicit table/column names, primary
key, nullability, SQL-compatible defaults, and stable persisted meanings.
Immutable data classes are practical when writes replace values deliberately.

```kotlin
@Entity(tableName = "projects")
data class ProjectEntity(
    @PrimaryKey
    @ColumnInfo(name = "project_id")
    val id: String,
    @ColumnInfo(name = "display_name")
    val displayName: String,
    @ColumnInfo(name = "updated_at_epoch_ms")
    val updatedAtEpochMs: Long,
    @ColumnInfo(name = "archived", defaultValue = "0")
    val archived: Boolean,
)
```

Kotlin defaults and SQL column defaults answer different creation paths.
Changing a property name, nullability, or default can be a schema change even
when application code still compiles. Treat persistent names and meanings as a
released contract.

## 5. Entity is not DTO, domain, or UI state

One class reused everywhere couples database migrations to network and UI
changes. Map at the boundary when independent evolution, validation, or
meaning justifies it:

```kotlin
data class Project(
    val id: ProjectId,
    val name: String,
    val updatedAt: Instant,
)

fun ProjectEntity.toDomain(): Project = Project(
    id = ProjectId(id),
    name = displayName,
    updatedAt = Instant.ofEpochMilli(updatedAtEpochMs),
)

fun Project.toEntity(): ProjectEntity = ProjectEntity(
    id = id.value,
    displayName = name,
    updatedAtEpochMs = updatedAt.toEpochMilli(),
    archived = false,
)
```

Mapping is not mandatory ceremony for every trivial private table. It becomes
valuable when persistent representation, application invariants, network
nullability, or presentation state differ. Never call an entity “domain” only
to avoid a mapper.

## 6. Keys express stable identity

Choose identity before annotations:

- a **natural key** is meaningful and stable in the domain;
- a **surrogate key** is generated only to identify the row;
- a **remote ID** identifies a server resource but may not exist before sync;
- a **composite key** identifies a relation or value by several columns;
- a **temporary local ID** supports offline creation and needs reconciliation.

```kotlin
@Entity(
    tableName = "project_memberships",
    primaryKeys = ["project_id", "user_id"],
)
data class ProjectMembershipEntity(
    @ColumnInfo(name = "project_id") val projectId: String,
    @ColumnInfo(name = "user_id") val userId: String,
    val role: String,
)
```

Do not replace a temporary key silently when other rows reference it. Define
whether the server accepts a client-generated operation/resource ID, whether a
mapping table is needed, and how retries remain idempotent.

## 7. Constraints and indices encode real invariants

A unique index can enforce identity beyond the primary key. A normal index can
accelerate measured filters, joins, sorting, and foreign-key lookups, at the
cost of storage and slower writes.

```kotlin
@Entity(
    tableName = "tasks",
    foreignKeys = [
        ForeignKey(
            entity = ProjectEntity::class,
            parentColumns = ["project_id"],
            childColumns = ["project_id"],
            onDelete = ForeignKey.CASCADE,
        ),
    ],
    indices = [
        Index(value = ["project_id", "position"]),
        Index(value = ["remote_id"], unique = true),
    ],
)
data class TaskEntity(
    @PrimaryKey @ColumnInfo(name = "task_id") val id: String,
    @ColumnInfo(name = "project_id") val projectId: String,
    @ColumnInfo(name = "remote_id") val remoteId: String?,
    val position: Int,
    val title: String,
)
```

Review cascade deletion against product meaning; it can remove much more than
the directly deleted row. Index hot foreign-key lookups and verify query plans.
Do not index every column mechanically.

## 8. DAOs expose database use cases

A DAO is a database contract, not a generic repository. Prefer methods that
state required query and mutation semantics:

```kotlin
@Dao
interface ProjectDao {
    @Query(
        """
        SELECT project_id, display_name, updated_at_epoch_ms, archived
        FROM projects
        WHERE project_id = :id
        """,
    )
    suspend fun findById(id: String): ProjectEntity?

    @Query("DELETE FROM projects WHERE archived = 1")
    suspend fun deleteArchived(): Int
}
```

`getAll`, generic raw queries, or universal CRUD can allow callers to bypass
ordering, filtering, constraints, and policy. DAO methods may return entities
or focused database projections; the repository remains the application
boundary.

## 9. Suspend DAO methods are one-shot operations

Use `suspend` for a read snapshot or one bounded write. Nullable, empty-list,
row-count, and constraint-failure behavior are part of the contract.

```kotlin
@Dao
interface TaskCommandDao {
    @Query("SELECT * FROM tasks WHERE task_id = :id")
    suspend fun snapshot(id: String): TaskEntity?

    @Query(
        "UPDATE tasks SET title = :title WHERE task_id = :id",
    )
    suspend fun rename(id: String, title: String): Int
}
```

A suspend DAO call is asynchronous from its caller's perspective; it is not an
observable subscription. Check the affected-row count when “missing row” has
different meaning from success.

## 10. Flow DAO methods observe invalidation

A Room DAO can return a cold `Flow`: collection starts observation and query
execution. When an observed table is invalidated, Room re-runs the query and
emits its result. An update to any row in a referenced table may trigger
re-execution even if the result set is semantically unchanged.

```kotlin
@Dao
interface ObservableProjectDao {
    @Query(
        """
        SELECT * FROM projects
        WHERE archived = 0
        ORDER BY display_name COLLATE NOCASE
        """,
    )
    fun observeActive(): Flow<List<ProjectEntity>>
}
```

Apply `distinctUntilChanged()` at a boundary that understands equality if
duplicate semantic results matter. Flow does not promise one emission per
write, an event log, or lifetime beyond its collector. Repositories map the
stream; ViewModel/UI owners collect or share it under their own lifetimes.

## 11. Insert, update, upsert, and delete need conflict policy

`@Insert`, `@Update`, `@Delete`, SQL queries, and `@Upsert` express different
contracts. `REPLACE` can have deletion/reinsertion consequences and should not
be a default shortcut. Decide whether conflict means reject, ignore, update
selected columns, or replace the whole row.

```kotlin
@Dao
interface ProjectWriteDao {
    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insert(project: ProjectEntity)

    @Update
    suspend fun update(project: ProjectEntity): Int

    @Upsert
    suspend fun upsert(projects: List<ProjectEntity>)
}
```

`@Upsert` is available from Room 2.5.0; verify the installed Room version and
its supported parameter/partial-entity contract. Convenience APIs do not
define server conflict resolution or freshness.

## 12. Transactions protect bounded database invariants

A transaction makes a sequence of database operations atomic: all commit or
all roll back. Use it when intermediate states must not become visible.

```kotlin
@Dao
abstract class ProjectTransactionDao {
    @Query("DELETE FROM tasks WHERE project_id = :projectId")
    protected abstract suspend fun deleteTasks(projectId: String)

    @Insert
    protected abstract suspend fun insertTasks(tasks: List<TaskEntity>)

    @Transaction
    open suspend fun replaceTasks(
        projectId: String,
        tasks: List<TaskEntity>,
    ) {
        require(tasks.all { it.projectId == projectId })
        deleteTasks(projectId)
        insertTasks(tasks)
    }
}
```

An exception causes rollback; cancellation must remain cancellation. Keep
transactions small and database-only. Never wait for network, user input, or
unbounded computation while holding a database transaction.

## 13. Transaction is not Mutex

A database transaction protects persisted consistency and participates in
SQLite isolation/locking. A coroutine `Mutex` protects an in-memory critical
section only among code that uses the same Mutex.

```kotlin
class RefreshCoordinator {
    private val mutex = Mutex()

    suspend fun <T> singleFlight(block: suspend () -> T): T =
        mutex.withLock { block() }
}
```

A Mutex does not roll back rows and other processes/connections do not honor
it automatically. A transaction does not protect an unrelated in-memory map.
Sometimes both are justified, but each needs a separate invariant and owner.

## 14. Model relationships according to reads and constraints

One-to-one and one-to-many normally use a foreign key. `@Relation` can assemble
objects through multiple queries and should be used with `@Transaction` for a
consistent aggregate:

```kotlin
data class ProjectWithTasks(
    @Embedded val project: ProjectEntity,
    @Relation(
        parentColumn = "project_id",
        entityColumn = "project_id",
    )
    val tasks: List<TaskEntity>,
)

@Dao
interface ProjectRelationDao {
    @Transaction
    @Query("SELECT * FROM projects WHERE project_id = :id")
    suspend fun projectWithTasks(id: String): ProjectWithTasks?
}
```

Many-to-many needs a junction row whose key prevents duplicate membership:

```kotlin
@Entity(
    tableName = "task_labels",
    primaryKeys = ["task_id", "label_id"],
    indices = [Index("label_id")],
)
data class TaskLabelCrossRef(
    @ColumnInfo(name = "task_id") val taskId: String,
    @ColumnInfo(name = "label_id") val labelId: String,
)
```

Deep nested relations may load large graphs and execute several queries. Prefer
an explicit join/projection when the screen needs only a slice. Choose cascade,
restrict, set-null, or manual cleanup from product semantics.

## 15. Embedded objects and projections shape database results

`@Embedded` flattens cohesive value fields into columns; prefix names to avoid
collisions:

```kotlin
data class AuditColumns(
    @ColumnInfo(name = "created_at_epoch_ms") val createdAt: Long,
    @ColumnInfo(name = "updated_at_epoch_ms") val updatedAt: Long,
)

@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey @ColumnInfo(name = "note_id") val id: String,
    val body: String,
    @Embedded val audit: AuditColumns,
)
```

A projection reads only required columns and avoids turning every query into a
giant aggregate:

```kotlin
data class ProjectSummaryRow(
    @ColumnInfo(name = "project_id") val id: String,
    @ColumnInfo(name = "display_name") val name: String,
    @ColumnInfo(name = "open_task_count") val openTaskCount: Int,
)

@Query(
    """
    SELECT p.project_id, p.display_name, COUNT(t.task_id) AS open_task_count
    FROM projects p
    LEFT JOIN tasks t
      ON t.project_id = p.project_id AND t.archived = 0
    GROUP BY p.project_id, p.display_name
    ORDER BY p.display_name
    """,
)
fun observeProjectSummaries(): Flow<List<ProjectSummaryRow>>
```

Room validates mapped columns at compile time. Still test SQL meaning, empty
relations, grouping, nullability, and ordering with representative rows.

## 16. Type converters are for one-column values

A converter maps a value to a SQLite-supported column representation:

```kotlin
class InstantConverters {
    @TypeConverter
    fun fromEpochMillis(value: Long?): Instant? =
        value?.let(Instant::ofEpochMilli)

    @TypeConverter
    fun toEpochMillis(value: Instant?): Long? =
        value?.toEpochMilli()
}
```

Suitable examples include timestamps, stable value objects, and enums with an
explicit persisted representation and migration policy. Room has versioned
built-in converter behavior, including enum support in modern versions; verify
the installed version. Do not serialize relational data into an opaque JSON
blob merely to avoid tables, keys, constraints, and queryable migrations.

## 17. Database lifecycle belongs to application DI

The database class defines entities, version, converters, migrations, and DAO
access:

```kotlin
@Database(
    entities = [
        ProjectEntity::class,
        TaskEntity::class,
        ProjectMembershipEntity::class,
        TaskLabelCrossRef::class,
    ],
    version = 2,
    exportSchema = true,
)
@TypeConverters(InstantConverters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun projectDao(): ProjectDao
    abstract fun taskDao(): TaskCommandDao
}
```

One instance per process is the normal practice because a database is
expensive and coordinates connections. Let an application-scoped DI owner
build it from application Context:

```kotlin
@Provides
@Singleton
fun provideDatabase(
    @ApplicationContext context: Context,
): AppDatabase = Room.databaseBuilder(
    context,
    AppDatabase::class.java,
    "app.db",
)
    .addMigrations(MIGRATION_1_2)
    .build()
```

Do not retain Activity Context or create a database per screen. Process death
closes in-memory objects; the file is reopened and validated/migrated in the
next process.

## 18. Let Room own its query execution boundary

Room rejects main-thread database access by default and integrates suspend and
Flow DAO methods with its executors. Do not wrap every Room suspend call in
`withContext(Dispatchers.IO)` mechanically. Add a dispatcher boundary for
blocking work outside Room or substantial CPU mapping only when that owner
requires it.

```kotlin
class RoomProjectLocalDataSource(
    private val dao: ObservableProjectDao,
) : ProjectLocalDataSource {
    override fun observeProjects(): Flow<List<ProjectRecord>> =
        dao.observeActive().map { entities ->
            entities.map(ProjectEntity::toRecord)
        }

    override suspend fun replaceProjects(records: List<ProjectRecord>) {
        dao.replace(records.map(ProjectRecord::toEntity))
    }
}
```

Exact executor, driver, transaction, and KMP behavior changes across Room
versions. Verify installed APIs rather than copying dispatcher folklore.

## 19. Schema versions and exported history are release artifacts

Increment the database version when the persisted schema changes. Export each
schema version, review it, and commit its history so auto migration and
migration tests can compare real versions.

```kotlin
plugins {
    id("androidx.room")
}

room {
    schemaDirectory("$projectDir/schemas")
}
```

The Room Gradle plugin schema configuration is available in current Room
versions; older projects use annotation-processor/KSP arguments. A fresh
install at version N and an upgrade from every supported historical version
must converge on a compatible final schema and data meaning.

## 20. Manual migrations preserve and transform data

Manual migration is required when SQL/data transformation cannot be inferred
safely. A rename-plus-transform often uses create/copy/drop/rename:

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            """
            CREATE TABLE projects_new (
                project_id TEXT NOT NULL PRIMARY KEY,
                display_name TEXT NOT NULL,
                updated_at_epoch_ms INTEGER NOT NULL DEFAULT 0,
                archived INTEGER NOT NULL DEFAULT 0
            )
            """.trimIndent(),
        )
        db.execSQL(
            """
            INSERT INTO projects_new(
                project_id, display_name, updated_at_epoch_ms, archived
            )
            SELECT id, name, 0, 0 FROM projects
            """.trimIndent(),
        )
        db.execSQL("DROP TABLE projects")
        db.execSQL("ALTER TABLE projects_new RENAME TO projects")
    }
}
```

This example targets the classic Android `SupportSQLiteDatabase` migration
path. Current Room also has driver-based `SQLiteConnection` APIs; implement the
overload required by the installed driver/version. Migration steps run in a
transaction, cannot use generated DAOs, and must define backfill, invalid data,
constraints, indices, and every supported version chain.

## 21. Auto migration handles only understood changes

Auto migrations compare exported schemas. They are available from Room 2.4.
Simple unambiguous changes may be generated; renames and deletions need an
`AutoMigrationSpec`, and complex data transformation still needs manual SQL.

```kotlin
@RenameColumn(
    tableName = "projects",
    fromColumnName = "name",
    toColumnName = "display_name",
)
class Migration1To2Spec : AutoMigrationSpec

@Database(
    entities = [ProjectEntity::class],
    version = 2,
    exportSchema = true,
    autoMigrations = [
        AutoMigration(
            from = 1,
            to = 2,
            spec = Migration1To2Spec::class,
        ),
    ],
)
abstract class AutoMigratedDatabase : RoomDatabase()
```

Generation is not proof of semantic correctness. Review the diff and test old
data. A manual migration takes precedence when manual and automatic paths
overlap; verify exact path selection against the installed Room version.

## 22. Destructive migration is an explicit data-loss decision

This is unsafe for user-created or authoritative local data:

```kotlin
// Anti-pattern for valuable data: a missing path silently becomes data loss.
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .fallbackToDestructiveMigration()
    .build()
```

Destructive fallback drops/recreates when a required path is absent. It can be
acceptable only for explicitly disposable, reconstructable data with a tested
recovery path and product approval. Prepackaged database behavior and fallback
overloads are version-sensitive; never add a broad fallback merely to stop a
migration crash.

## 23. Repository policy turns Room into a source of truth

Room does not become correct merely by existing. The repository chooses local
observation, refresh, write-through, stale-while-revalidate, remote-only
fallback, or authoritative local behavior per data set.

```kotlin
class OfflineFirstProjectRepository(
    private val database: AppDatabase,
    private val dao: ProjectSyncDao,
    private val remote: ProjectRemoteDataSource,
) : ProjectRepository {
    override fun observeProjects(): Flow<List<Project>> =
        dao.observeAll().map { rows -> rows.map(ProjectEntity::toDomain) }

    override suspend fun refresh() {
        val response = remote.fetchProjects() // Network is outside transaction.
        val entities = response.map(ProjectDto::toEntity)
        database.withTransaction {
            dao.replaceServerSnapshot(entities)
        }
    }
}
```

The transaction commits only local effects after remote work completes. A
remote call inside it would hold database resources during an unbounded
external operation and cannot be rolled back remotely. Expose stale local data
plus refresh status/error when that is the intended UX; do not erase useful
content because refresh failed.

## 24. Offline writes require conflict and sync state

Offline mutation is a durable promise. Store operation identity, payload or
target state, attempts, status, server version, and timestamps only when the
protocol needs them:

```kotlin
@Entity(
    tableName = "pending_project_writes",
    indices = [Index(value = ["status", "created_at_epoch_ms"])],
)
data class PendingProjectWriteEntity(
    @PrimaryKey @ColumnInfo(name = "operation_id") val operationId: String,
    @ColumnInfo(name = "project_id") val projectId: String,
    val kind: String,
    val payload: String,
    val status: String,
    @ColumnInfo(name = "base_server_version") val baseServerVersion: Long?,
    @ColumnInfo(name = "created_at_epoch_ms") val createdAtEpochMs: Long,
)
```

Choose server-wins, client-wins, last-write-wins, merge, reject, or
user-visible resolution from domain meaning—not convenience. Timestamps need a
trusted interpretation; “latest clock wins” can lose changes. Use idempotency
and version/precondition checks so retries do not duplicate effects. Room
persists state but does not solve distributed conflict policy.

## 25. Test correctness and measure performance

Use real Room/SQLite for query, constraint, transaction, invalidation, and
migration risks. Give every test a fresh database and close it:

```kotlin
@RunWith(AndroidJUnit4::class)
class ProjectDaoTest {
    private lateinit var database: AppDatabase

    @Before
    fun createDatabase() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java,
        ).build()
    }

    @After
    fun closeDatabase() = database.close()
}
```

Prove rollback with a deliberate failure:

```kotlin
@Test
fun replaceRollsBackWhenSecondWriteViolatesConstraint() = runTest {
    dao.insertTasks(listOf(validTask))

    assertFails {
        dao.replaceTasks(projectId, listOf(taskWithMissingParent))
    }

    assertEquals(listOf(validTask), dao.tasks(projectId))
}
```

Migration tests start an old schema, seed representative data, run the exact
path, validate the final schema, and assert transformed data:

```kotlin
@Test
fun migrate1To2PreservesProjectName() {
    helper.createDatabase(DB_NAME, 1).use { oldDb ->
        oldDb.execSQL(
            "INSERT INTO projects(id, name) VALUES('p-1', 'Roadmap')",
        )
    }

    helper.runMigrationsAndValidate(
        DB_NAME,
        2,
        true,
        MIGRATION_1_2,
    ).use { migrated ->
        migrated.query(
            "SELECT display_name FROM projects WHERE project_id = 'p-1'",
        ).use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals("Roadmap", cursor.getString(0))
        }
    }
}
```

`MigrationTestHelper` constructors and connection types changed across Room
versions; adapt this classic Android helper shape to the installed
`room-testing` artifact and test all supported paths.

Do not load an unbounded table for a scrolling screen:

```kotlin
@Query(
    """
    SELECT * FROM tasks
    WHERE project_id = :projectId
    ORDER BY position, task_id
    LIMIT :limit OFFSET :offset
    """,
)
suspend fun page(
    projectId: String,
    limit: Int,
    offset: Int,
): List<TaskEntity>
```

For Paging 3, supported Room versions can return `PagingSource`; verify the
installed Room/Paging integration. Offset pagination is only an example and
can become expensive or unstable for changing large data; keyset or
library-owned paging may fit better.

Avoid N+1 reads:

```kotlin
// Anti-pattern: one query for projects, then one query per project.
val projects = dao.projects()
val tasksByProject = projects.associateWith { dao.tasks(it.id) }

// Better: one use-case-specific JOIN/projection or a deliberate @Relation.
@Query(
    """
    SELECT p.project_id, p.display_name, COUNT(t.task_id) AS task_count
    FROM projects p
    LEFT JOIN tasks t ON t.project_id = p.project_id
    GROUP BY p.project_id, p.display_name
    """,
)
suspend fun projectCounts(): List<ProjectTaskCountRow>
```

Measure representative data and device SQLite with query timing and
`EXPLAIN QUERY PLAN`. Read fewer rows/columns, filter/sort in SQL, index
measured paths, batch writes, avoid giant nested graphs and transactions, and
consider WAL only with its actual consistency/durability constraints.

## 26. Security, backup, anti-patterns, and decision guide

Room databases normally live in app-private storage, but a compromised process
or device can still access plaintext. Minimize sensitive columns and retention;
define logout/account-removal deletion, export/sharing, encryption threat
model, key recovery, and backup/device-transfer rules. Database encryption is
not authorization.

```xml
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="database" path="session.db" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="database" path="session.db" />
    </device-transfer>
</data-extraction-rules>
```

Backup rules and behavior vary by Android version and transport. Test restore,
invalid session/device-bound keys, and server reconciliation.

Avoid:

- entity reused as DTO, domain, and UI model;
- DAO or database in ViewModel;
- database instance created per screen;
- destructive fallback for user data;
- missing migration/schema history tests;
- opaque JSON blobs for relational data without a reason;
- giant transaction or network call inside a transaction;
- no index on a hot foreign-key lookup, or indices on every column;
- infinite Flow collection without a lifecycle owner;
- whole-table load for a paging use case;
- assuming Room defines freshness or conflict policy;
- database encryption presented as authorization;
- shared mutable singleton database state across tests.

Finish with:

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
