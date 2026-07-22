# Task 008 — Cross-source competency normalization

Status: DONE
Phase: Phase 2 — Competency import
Type: Canonical competency normalization and architecture validation

## Goal

Normalize the second Android Developers source package against the complete existing canonical competency registry.

The task must determine, for every source item in:

```text
competencies/sources/android-developers-architecture-recommendations/
```

whether it:

- supports an existing canonical competency;
- partially overlaps an existing competency and requires an explicit editorial decision;
- supports a new canonical competency;
- should remain deferred because it does not yet justify a stable canonical capability.

The task must update the canonical Android app architecture package only when supported by source evidence and must produce a complete cross-source normalization report.

This task is also the first real architectural validation of the canonical competency model. It must conclude with a documented recommendation on whether the model is ready to move from `PROPOSED` to `ACCEPTED`.

## Inputs

Required repository inputs:

```text
competencies/sources/android-developers-app-architecture/
competencies/sources/android-developers-architecture-recommendations/
competencies/normalized/android-app-architecture/
competencies/reports/android-developers-app-architecture-review.md
competencies/reports/android-developers-architecture-recommendations-review.md
competencies/reports/android-app-architecture-normalization-review.md
docs/COMPETENCY_SOURCE_MODEL.md
docs/COMPETENCY_IMPORT_WORKFLOW.md
docs/COMPETENCY_NORMALIZATION_WORKFLOW.md
docs/architecture/CANONICAL_COMPETENCY_MODEL.md
```

The complete canonical registry must be inspected, not only the package expected to change.

## Preconditions

Task 007 must already be committed.

Both source packages must:

- use `source_version: 1`;
- remain in `review`;
- pass the existing competency validator;
- remain immutable during this task.

The existing canonical package is:

```text
competencies/normalized/android-app-architecture/
├── competency-set.yaml
└── competencies.yaml
```

It currently contains a review-stage pilot derived from the first source.

---

# Architectural rules

## 1. Source packages are immutable

Do not change:

```text
competencies/sources/android-developers-app-architecture/
competencies/sources/android-developers-architecture-recommendations/
```

Normalization may only reference source items through versioned evidence.

If a source extraction error is discovered:

1. do not silently fix it in this task;
2. record it as a blocker or ambiguity;
3. stop normalization of the affected item;
4. report the required source-correction task separately.

## 2. Canonical identity is semantic

A new source does not create a new competency merely because it:

- uses different wording;
- uses a different recommendation level;
- gives a different example;
- names a specific Android library;
- comes from a separate publication;
- is more implementation-oriented.

Attach evidence to an existing competency when a competent reviewer would assess substantially the same underlying capability using substantially the same success criteria.

## 3. Evidence does not define competency identity

The same canonical competency may contain evidence from both sources.

Evidence entries must remain grouped by:

```yaml
source_id:
source_version:
item_ids:
```

Do not create duplicate evidence entries whose item sets differ only in order.

## 4. Preserve semantic scope

Do not broaden an existing competency merely to absorb loosely related source items.

For partial overlaps, explicitly classify the relationship as one of:

```text
narrower
broader
adjacent
multi-capability
technology-specific specialization
recommendation-strength difference
conflict or tension
```

Then decide whether to:

- attach evidence without changing canonical wording;
- revise canonical wording while preserving identity;
- create a distinct competency;
- split a source item across multiple competencies;
- defer the item.

## 5. One coherent capability per competency

Every competency must:

- express one primary demonstrable capability;
- remain source-independent;
- be distinguishable from neighboring competencies;
- remain supportable if either source were later removed;
- avoid unsupported framework labels;
- avoid combining independently assessable actions.

## 6. Recommendation strength

Source-declared levels such as:

```text
Strongly recommended
Recommended
Recommended in big apps
Optional
```

belong to source evidence, not automatically to canonical competency identity.

Do not add recommendation level, difficulty, importance, or learner seniority to the canonical schema.

A difference in recommendation strength may be discussed in normalization notes or the review report when it materially affects interpretation.

## 7. Technology-specific claims

A source-specific technology recommendation may support:

- an existing broader competency;
- a new technology-specific competency;
- no canonical competency yet.

Use a broader existing competency only when the source item genuinely supports its complete outcome.

Do not generalize a technology-specific item beyond what it evidences.

Do not create competencies whose identity is merely a library name unless the demonstrable capability is inherently library-specific and independently useful.

---

# Required work

## 1. Inspect repository state

Before editing:

```bash
git status --short
git log --oneline --decorate -12
python -B scripts/validate_competencies.py
```

Confirm:

- Task 007 is committed;
- the worktree is clean or contains only the Task 008 setup file;
- both source packages validate;
- no source IDs or canonical IDs are duplicated.

Read all required inputs completely.

## 2. Build a source-item disposition matrix

Create a complete editorial matrix covering every item from the second source.

The matrix must be included in the normalization report and contain:

```text
Source item ID
Declared level
Candidate capability
Existing competency candidate
Relationship classification
Decision
Canonical competency ID
Wording change required
Notes
```

Allowed decisions:

```text
attach-existing
attach-existing-and-reword
create-new
split-across-competencies
defer
blocked-source-issue
```

Every source item must appear exactly once as the primary row in the matrix.

When one source item supports several competencies, the matrix row must identify every target competency and explain the split.

## 3. Compare against the complete canonical registry

For each source item:

1. identify the demonstrable capability;
2. search all existing canonical sets;
3. compare outcome and assessment boundary, not title similarity;
4. inspect all existing evidence;
5. classify exact match, partial overlap, distinct capability, or insufficient evidence;
6. record the decision before changing canonical data.

Do not begin by drafting new competencies.

## 4. Update the canonical package

Update:

```text
competencies/normalized/android-app-architecture/competency-set.yaml
competencies/normalized/android-app-architecture/competencies.yaml
```

only as required by approved normalization decisions.

### 4.1 Versioning

The existing canonical set is version 1.

Because this task changes canonical evidence and may change canonical meaning or membership, increment:

```yaml
version: 2
```

and keep:

```yaml
competency_set_version: 2
```

in sync.

The package status must remain:

```yaml
status: review
```

Do not mark it `approved`.

### 4.2 Existing competencies

For an existing competency:

- preserve its ID when semantic identity remains the same;
- add a second evidence entry for the second source;
- revise title or outcome only when broader evidence justifies a clearer source-independent expression;
- add or update `normalization_notes` when the cross-source decision is non-trivial;
- avoid formatting-only rewrites.

Do not rename an existing canonical ID merely to improve style.

A canonical ID change requires evidence that the existing ID is materially misleading, not merely imperfect.

### 4.3 New competencies

Create a new competency only when:

- no existing competency represents the same demonstrable capability;
- the source evidence is sufficient;
- the capability is stable outside the publication;
- it is independently assessable;
- it is neither a broad topic nor a trivial implementation instruction;
- its distinction from neighboring competencies can be explained.

New competencies must use stable action-oriented IDs, titles, and outcomes.

### 4.4 Deferred source items

A source item may remain unnormalized when:

- it states a broad benefit rather than a capability;
- it is too technology-specific to justify canonical identity yet;
- it lacks sufficient detail;
- it overlaps several competencies without a defensible split;
- it requires evidence from an out-of-scope linked publication;
- normalization would invent meaning.

Every deferred item must have a concrete reason and a stated condition for reconsideration.

## 5. Cross-source normalization report

Create:

```text
competencies/reports/android-app-architecture-cross-source-normalization-review.md
```

Do not replace the original Task 006 normalization report. Preserve it as historical review documentation.

Required sections:

```text
# Android app architecture cross-source normalization review

## Review scope
## Input packages and versions
## Canonical package before normalization
## Normalization method
## Complete source-item disposition matrix
## Evidence attached to existing competencies
## Existing competencies reworded
## New canonical competencies
## Source items split across competencies
## Deferred source items
## Duplicate and near-duplicate review
## Recommendation-strength observations
## Conflicts and tensions
## Canonical package after normalization
## Canonical model validation
## Model acceptance recommendation
## Validation results
## Human review checklist
```

## 6. Evidence attachment review

For every existing competency receiving evidence from the second source, document:

- existing competency ID;
- original evidence;
- new source item IDs;
- whether wording changed;
- why the evidence supports the same competency identity;
- whether recommendation-strength differences matter.

No evidence attachment may be justified only by shared terminology.

## 7. Existing competency wording review

Review all existing 11 competencies against both sources.

Do not rewrite all of them automatically.

Classify each as:

```text
unchanged
evidence-expanded
wording-refined
scope-narrowed
scope-broadened-within-identity
requires-new-neighboring-competency
```

Any wording change must include:

- previous title/outcome;
- new title/outcome;
- evidence justification;
- confirmation that the stable ID still represents the same competency.

## 8. Duplicate and near-duplicate review

Compare:

- every new candidate against every existing competency;
- every resulting competency against neighboring competencies;
- technology-specific recommendations against broader competencies;
- ViewModel, UI state-holder, lifecycle, UDF, repository, domain, DI, testing, model, and naming candidates.

Document rejected duplicate candidates.

Do not introduce a semantic duplicate merely to preserve one source row per competency.

## 9. Conflicts and tensions

Explicitly inspect whether the two sources differ in:

- recommendation strength;
- scope;
- terminology;
- optionality;
- application-size conditions;
- framework specificity;
- layer ownership;
- lifecycle assumptions.

Distinguish:

```text
compatible elaboration
narrower specialization
different strength
different scope
actual tension
```

Do not erase a real tension by writing vague canonical wording.

If an actual contradiction prevents stable normalization, defer the affected item and record it.

## 10. Canonical model validation

Evaluate whether the existing canonical model successfully supported:

- multiple source packages;
- evidence aggregation;
- exact-match attachment;
- partial-overlap decisions;
- new competency creation;
- source-item reuse or splitting;
- versioned evidence;
- stable IDs;
- package versioning;
- duplicate prevention;
- human-review traceability.

Document any model limitation discovered.

Do not modify schemas or the architecture model merely because a future convenience field would be useful.

## 11. Model acceptance recommendation

At the end of the report, recommend exactly one:

```text
ACCEPT
KEEP PROPOSED
REVISE BEFORE ACCEPTANCE
```

### ACCEPT

Use only if:

- the second source fits the model without structural workaround;
- canonical identity remains stable;
- evidence aggregation is sufficient;
- no missing required field prevents correct normalization;
- validators enforce the implemented invariants;
- remaining limitations are future enhancements rather than model defects.

### KEEP PROPOSED

Use when:

- the model works, but another source or review cycle is needed for confidence;
- unresolved editorial questions remain but no structural defect is proven.

### REVISE BEFORE ACCEPTANCE

Use when:

- the model cannot faithfully represent required relationships;
- evidence structure is insufficient;
- versioning is ambiguous;
- stable identity cannot be preserved;
- normalization requires unsupported fields or structural workarounds.

Do not change the architecture document's status in this task.

The human owner will approve any later transition from `PROPOSED` to `ACCEPTED`.

## 12. Validator behavior

Run existing validation before changing implementation.

Expected changes should be representable by the existing schemas and validator.

Do not modify:

```text
schemas/
scripts/
tests/
```

unless the new valid canonical state exposes a concrete defect in approved validation behavior.

If a defect is found:

1. stop;
2. report it;
3. do not silently expand the task;
4. wait for architectural approval.

## 13. Documentation synchronization

Update minimally:

```text
README.md
docs/PROJECT_STATE.md
docs/ROADMAP.md
```

State accurately that:

- cross-source normalization has been performed and remains under review;
- the canonical package is version 2 and remains `review`;
- the canonical model acceptance recommendation exists;
- model status remains `PROPOSED` until human approval;
- competency relations and learning sequence remain future work.

Do not mark Phase 2 complete.

Update this task status from `READY` to `REVIEW` after successful implementation.

---

# Explicit non-goals

Do not:

- modify either source package;
- approve source packages;
- change the canonical model document status;
- create competency relations;
- create prerequisite edges;
- define a learning sequence;
- map competencies to topics;
- create educational topics;
- add difficulty or seniority;
- add assessments;
- add learner progress;
- add embeddings or semantic-search tooling;
- create an automatic deduplication system;
- add generated catalogs;
- add CI;
- create a commit;
- push changes.

---

# Required validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Verify source immutability:

```bash
git diff -- competencies/sources/
```

Verify forbidden implementation areas are unchanged:

```bash
git diff -- schemas/ scripts/ tests/ content/ templates/
```

Inspect canonical package changes:

```bash
git diff -- competencies/normalized/android-app-architecture/
```

## Acceptance criteria

Task 008 is accepted only if:

- every second-source item has exactly one documented primary disposition;
- the complete canonical registry was considered;
- evidence is attached to existing competencies where semantically equivalent;
- new competencies are created only for distinct demonstrable capabilities;
- partial overlaps have explicit editorial classifications;
- deferred items have concrete reasons;
- existing IDs remain stable unless a material identity defect is proven;
- package version is incremented consistently to 2;
- package status remains `review`;
- both source packages remain unchanged;
- duplicate and near-duplicate review is complete;
- recommendation-strength differences are preserved in analysis;
- conflicts and tensions are explicitly assessed;
- the report evaluates the canonical model itself;
- exactly one model acceptance recommendation is produced;
- canonical model document remains `PROPOSED`;
- no relation graph, learning sequence, or topic mapping is created;
- all validation commands pass;
- no commit is created.

## Delivery report

Return:

1. Files created and changed.
2. Canonical package version before and after.
3. Total second-source item count.
4. Disposition counts:
   - attach-existing;
   - attach-existing-and-reword;
   - create-new;
   - split-across-competencies;
   - defer;
   - blocked-source-issue.
5. Existing competencies receiving new evidence.
6. Existing competencies reworded.
7. New canonical competencies.
8. Deferred source items and reasons.
9. Duplicate candidates rejected.
10. Conflicts or tensions found.
11. Canonical competency count before and after.
12. Canonical model acceptance recommendation and rationale.
13. Validation results.
14. Source immutability confirmation.
15. Final `git status --short`.
16. Confirmation that no commit was created.

Then stage intended changes and export:

```bash
git add README.md docs/PROJECT_STATE.md docs/ROADMAP.md competencies/normalized/android-app-architecture competencies/reports/android-app-architecture-cross-source-normalization-review.md tasks/008-cross-source-competency-normalization.md
git diff --cached > ..\task-008-review.diff
```

Do not create a commit.
