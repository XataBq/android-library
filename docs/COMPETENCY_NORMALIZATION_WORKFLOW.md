# Competency Normalization Workflow

## Purpose

Normalization begins after a source has been extracted into a
provenance-preserving package and its evidence is ready for editorial review.
It converts source evidence into repository-owned canonical capabilities. It
does not rewrite the source package or turn each source item automatically into
a competency.

Use the [competency import workflow](COMPETENCY_IMPORT_WORKFLOW.md) to create
source packages. Use the
[canonical competency model](architecture/CANONICAL_COMPETENCY_MODEL.md) as the
authority for competency boundaries, wording, evidence, and review rules.

## Required inputs

Before normalization, reviewers need:

- one source package whose extraction is review-quality;
- the complete existing canonical competency registry, across every competency
  set;
- the canonical competency model;
- the actual source-item text, context, and locators;
- existing import and normalization reports relevant to the source or domain.

Do not normalize from item IDs, headings, or summaries alone. Read the source
item statements and inspect their locators before deciding what capability the
evidence supports.

## Decision sequence

For each source item or coherent group of source items:

1. Identify the demonstrable capability directly supported by the evidence.
2. Search the entire canonical registry for the same capability, including
   competencies in other sets.
3. Classify the candidate as an exact semantic match, partial overlap, distinct
   capability, or insufficient or unsuitable evidence.
4. For an exact semantic match, attach versioned evidence to the existing
   competency instead of creating a duplicate.
5. For partial overlap, determine whether the source claim is narrower, broader,
   or contains multiple independently demonstrable capabilities.
6. Create a new competency only when no existing competency expresses the same
   demonstrable capability and the evidence supports a stable boundary.
7. Defer evidence that does not justify a stable competency. Do not strengthen
   weak evidence through canonical wording.
8. Record every non-trivial merge, split, reuse, rejection, and deferral in
   `normalization_notes` or the normalization report, as appropriate.

### Classification guidance

- **Exact semantic match:** the existing outcome would be assessed with
  substantially the same success criteria. Add evidence to that competency.
- **Partial overlap:** the candidate shares meaning with an existing competency
  but differs materially in breadth or demonstrable capability. Review the
  boundary before changing wording or creating a record.
- **Distinct capability:** the evidence supports an independently demonstrable
  capability absent from the registry. A new competency may be created under
  controlled review.
- **Insufficient or unsuitable evidence:** the item is too broad, too narrow,
  source-specific, non-demonstrable, or otherwise unable to support a stable
  canonical capability. Reject or defer it and record why.

## Evidence attachment and controlled creation

Evidence references must include the exact `source_id`, `source_version`, and
existing `item_ids`. Evidence is support, not identity: a new publication does
not justify a second competency when an existing competency already expresses
the capability.

Before creating a competency, verify that it has one primary capability, an
action-oriented title, an observable source-independent outcome, and direct
evidence. Search all competency sets for semantic duplicates. Add
`normalization_notes` when evidence is merged or split, one source item is
reused, wording meaningfully generalizes source terminology, or the mapping is
not self-evident.

## Review rules

- Do not infer competencies that the imported evidence does not support.
- Source packages are immutable during normalization.
- Canonical wording is repository-owned and source-independent.
- Each competency expresses one primary demonstrable capability.
- Evidence does not define competency identity.
- Different publications do not justify duplicate competencies.
- Semantic duplicate review is a human editorial responsibility.
- Every evidence reference is versioned and resolves to real source items.
- Merge only inseparable aspects of the same capability; do not merge items
  because they share a source section.
- Split only independently demonstrable capabilities; do not split to increase
  the registry size.
- Reuse a source item only when it genuinely supports separate capabilities.
- Keep source and canonical packages in `review` until human approval.

## Cross-source normalization

When a second or later source is imported, compare every candidate against the
whole canonical registry, not only the most related package. Attach evidence to
an existing competency when the demonstrable capability is equivalent.

Canonical wording may be clarified when broader evidence warrants it, but only
if the competency's meaning remains stable. Keep wording independent from
publication names, source hierarchy, and source-specific examples. Record
conflicts and materially different claims for review; do not silently weaken an
obligation or strengthen a recommendation to make sources appear consistent.

Cross-source review must document:

- evidence attached to existing competencies;
- new competencies and why no existing one matched;
- merges, splits, and justified source-item reuse;
- rejected or deferred candidates and their reasons;
- conflicting scope or recommendation strength;
- uncovered source items and evidence coverage.

## Output package and report

Canonical competency sets use:

```text
competencies/normalized/<competency-set-id>/
├── competency-set.yaml
└── competencies.yaml
```

The set metadata identifies the package and its version. Each competency records
canonical wording and versioned evidence. Normalization decisions, coverage,
rejections, deferrals, conflicts, and limitations are recorded in a review
report under:

```text
competencies/reports/
```

## Validation and manual review

Run:

```bash
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Automated validation checks schema and reference integrity; it cannot decide
semantic equivalence or evidence sufficiency. A reviewer must also:

- read the actual source-item text rather than relying on IDs;
- inspect every evidence link, source version, and locator;
- review semantic duplicates across all competency sets;
- verify competency and evidence counts, uncovered items, and deferred items;
- verify that source packages are unchanged by normalization;
- verify that the package and report describe the same mappings and decisions.

## Non-goals

This workflow does not define or create:

- prerequisite or other competency relations;
- a learning sequence;
- difficulty or seniority levels;
- assessments;
- topic mappings;
- learner progress or mastery;
- automatic semantic similarity or duplicate detection;
- embeddings;
- automatic competency or educational-topic generation.
