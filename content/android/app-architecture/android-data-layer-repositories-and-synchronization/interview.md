# Android Data Layer — Interview preparation

## Foundational questions

### 1. Why does an application need a Data layer?

**Interviewer guidance:** Expect one owner for application data access and mutation policy, source coordination, and isolation from transport or persistence details.

### 2. Distinguish a repository from a data source.

**Interviewer guidance:** A repository exposes application operations and owns cross-source policy. A data source communicates with one concrete system. Do not require a repository to be large.

### 3. What makes a repository more than a Retrofit wrapper?

**Interviewer guidance:** Look for application vocabulary, mapping, source-of-truth, freshness, write, or error policy. A thin boundary can still be intentional; the candidate should discuss its value.

### 4. Define Single Source of Truth.

**Interviewer guidance:** One authoritative owner for a particular data set. It can be remote, durable local storage, or repository memory; it is not automatically Room.

### 5. How do cache and persistence differ?

**Interviewer guidance:** Cache describes a reusable copy and its validity; persistence describes survival across a lifetime boundary. Either can exist without the other.

### 6. Why expose application models rather than source models?

**Interviewer guidance:** Isolation from API/storage constraints and change rates. Strong answers also mention mapping cost and cases where sharing is acceptable.

## Scenario questions

### 7. A feed must open immediately offline and refresh when connected. Design its read path.

**Interviewer guidance:** Expect local observation as the application path, remote refresh persisted locally, freshness status, and failure that preserves usable data.

### 8. A screen reads the database and network independently. What can go wrong?

**Interviewer guidance:** Competing truths, races, duplicate policy, inconsistent failure handling, and UI coupling to source details.

### 9. A queued write may be retried after its response is lost. What must the design provide?

**Interviewer guidance:** Operation identity or idempotency, durable progress, retry classification, and a way to reconcile ambiguous remote success.

### 10. A refresh fails while week-old data exists. Should the repository return an error?

**Interviewer guidance:** It depends on acceptable staleness. The candidate should separate availability, data, and refresh state rather than force one universal result shape.

### 11. Two devices edit the same field offline. How would you choose a conflict policy?

**Interviewer guidance:** Domain meaning, server versions, possible merge or user resolution, and consequences of last-write-wins. Device timestamps alone deserve skepticism.

### 12. A remote write succeeds but local persistence fails. What is success?

**Interviewer guidance:** Expect explicit partial-failure semantics and a repair/re-fetch path. One Boolean cannot explain both source states.

## Trade-off questions

### 13. Compare network-first, cache-first, and local-first reads.

**Interviewer guidance:** Listen for latency, freshness, fallback, invalidation, offline capability, and synchronization cost—not a universal recommendation.

### 14. Remote-first or optimistic writes?

**Interviewer guidance:** Remote-first favors confirmed authority; optimistic improves responsiveness but requires pending, rejection, rollback, and concurrency semantics.

### 15. When is offline-first worth its cost?

**Interviewer guidance:** Product-critical offline behavior, unreliable networks, and latency can justify it. Synchronization, conflict, testing, storage, and operational complexity are costs.

### 16. One model per layer or a shared model?

**Interviewer guidance:** Boundary-specific models isolate contracts and constraints; shared models reduce mapping. The answer should follow actual divergence, not a fixed count.

### 17. How granular should repositories be?

**Interviewer guidance:** Cohesive data ownership and policy are better guides than tables or endpoints. Mention broad god repositories, tiny wrappers, cross-repository invariants, and cycles.

### 18. Should every repository use one universal result wrapper?

**Interviewer guidance:** No. Reads, confirmed writes, queued work, stale data, and conflicts can require different contracts. Consistency is useful only when it preserves needed meaning.
