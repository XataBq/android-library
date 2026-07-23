# Android Data Layer — Cheat sheet

## Repository responsibilities

- Expose application-oriented data and operations.
- Centralize read and write policy.
- Coordinate local, remote, and platform sources.
- Define the source of truth and freshness rules.
- Reconcile source disagreements.
- Translate source models and failures at an explicit boundary.
- Keep storage and transport details away from consumers.

## Repository vs data source

| Repository | Data source |
|---|---|
| Represents cohesive application data | Represents one concrete system |
| Called by UI state holders or Domain | Called by a repository |
| Owns coordination policy | Owns source-specific operations |
| Uses application vocabulary | Uses transport, storage, file, sensor, or platform vocabulary |
| May coordinate several sources | Must not secretly coordinate application-wide sources |

## Cache vs persistence

| Cache | Persistence |
|---|---|
| Reusable copy for latency, cost, or availability | Data survives a defined lifetime boundary |
| Needs invalidation and eviction policy | Needs durability and recovery policy |
| May live in memory or on disk | Usually disk-backed |
| May or may not be authoritative | May or may not be authoritative |

A disk cache is persistent but disposable. A database can be persistent SSOT. An in-memory SSOT can be valid for session-only data.

## SSOT checklist

- [ ] Which exact data set is in scope?
- [ ] Who is authoritative for that data?
- [ ] Do all consumers observe it through one boundary?
- [ ] How do remote results update the authoritative application view?
- [ ] What lifetime must it survive?
- [ ] May stale data remain usable?
- [ ] Who resolves disagreement?

SSOT means one authoritative owner for a particular piece of application data. It does not mean “always use a database.”

## Read strategy comparison

| Strategy | Best fit | Main benefit | Main risk |
|---|---|---|---|
| Network-first | Server confirmation is required | Favors current remote state | Latency and offline failure |
| Cache-first | Fast reuse is acceptable within a validity policy | Low latency and source cost | Invalid or stale copies |
| Local-first | Stable observation and offline reads matter | One observable path | Synchronization complexity |

For every strategy, define fallback, stale-data behavior, refresh trigger, and duplicate-request behavior.

## Synchronization checklist

- [ ] Direction: pull, push-signaled, or hybrid.
- [ ] Unit: snapshot, page, entity, or changes since a version.
- [ ] Progress survives the interruption promised by the product.
- [ ] Retries distinguish transient from terminal failure.
- [ ] Repeated writes are idempotent or carry operation identity.
- [ ] Dependent operations have an ordering policy.
- [ ] Conflicts have an authority or merge rule.
- [ ] Pending, failed, stale, and conflicted states are observable where needed.
- [ ] Partial success has a repair path.

## Freshness checklist

- What makes the value stale?
- How long is it acceptable?
- Is stale-but-usable distinct from unavailable?
- What triggers refresh?
- Does refresh preserve old data on failure?
- Can users force refresh?
- Which signal proves a newer version exists?

## Model boundary summary

```text
UserResponse → UserEntity → User → UserUiModel
 transport      storage    application  presentation
```

Separate models when contracts, constraints, or change rates differ. Share models when meanings align and coupling is acceptable. Four models are not a requirement.

## Warning signs

- UI decides between local and remote sources.
- A data source performs hidden fallback or reconciliation.
- Local and remote values race directly to consumers.
- “Cached” has no freshness or invalidation definition.
- A failed refresh deletes usable data.
- Every failure is retried identically.
- A duplicate queued write can repeat a harmful effect.
- Rollback can overwrite a newer edit.
- Transport or database types become every layer’s model accidentally.
- Repository boundaries mirror endpoints or tables without cohesive ownership.
- A universal result wrapper hides pending, stale, or partial-success states.
