# Competency Import Workflow

## Purpose

Competency import records what one source says before the project interprets,
deduplicates, or normalizes it. The output is a provenance-preserving source
package for review, not a canonical competency registry, prerequisite graph,
learning sequence, educational topic, or learner-progress record.

The first concrete example is
`competencies/sources/android-developers-app-architecture/`, which represents
only the Android Developers publication *Guide to app architecture*.

## Source boundary

One package represents one coherent publication or independently maintained
documentation section. Define that boundary before extraction. Links are useful
for navigation and attribution, but linked pages are not automatically part of
the package. Import a linked publication separately if a later approved task
needs it.

The example package stops at
`https://developer.android.com/topic/architecture`. It does not absorb the
linked architecture recommendations, UI layer, data layer, or domain layer
publications.

## Pre-import checks

Before recording any items:

1. Confirm that the source is publicly accessible or otherwise authorized for
   the intended use.
2. Identify the title, publisher, canonical URL, visible version or update
   label, and actual retrieval date.
3. Select the accurate `repository_usage` value and determine whether source
   artifacts may be stored. A `citation-only` package cannot contain artifacts.
4. Check the material for confidentiality, secrets, access restrictions,
   personal data, and other public-repository risks.
5. Define the publication boundary and list important linked material that is
   outside it.
6. Leave licensing and legal permission for human review. Schema validity does
   not establish permission to copy or redistribute source material.

## Extraction workflow

1. Inspect the entire in-scope source, including its visible hierarchy and
   update label.
2. Record source identity, provenance, scope, repository usage, and repository
   source version in `source.yaml`.
3. Identify meaningful source-level requirements, responsibilities,
   constraints, techniques, and stated benefits.
4. Keep statements reasonably atomic: do not split one rule into fragments or
   merge unrelated rules for a preferred item count.
5. Assign each item a stable semantic kebab-case ID that does not encode array
   position, retrieval date, or a future normalized identity.
6. Preserve the source heading hierarchy in `context` and add a durable locator
   based on visible headings. Use `details` to distinguish multiple items under
   one heading.
7. Add `transcription_notes` only when they explain a real transformation or
   ambiguity, such as condensing an enumerated list or retaining dependent
   clauses together.
8. Validate YAML, the Draft 2020-12 schemas, and repository-level semantics.
9. Manually check wording fidelity, coverage, source boundaries, and locator
   traceability against the live source.
10. Set the package to `review` and request human review. Only a reviewer may
    approve the extraction.

## Good extraction

A good source item is faithful to the source's strength and conditions,
traceable to a visible location, understandable without a full-page copy, and
still clearly source-level. Its scope is narrow enough to review while retaining
clauses that form one rule. The set covers the publication coherently without
gaming a numeric target.

For example, the Android Developers package keeps the source's optionality for
the domain layer, records separate UI, repository, and data-source
responsibilities, and uses heading-based locators with visible best-practice
lead-ins as details.

## Bad extraction

Do not:

- normalize terminology or decide canonical identities during import;
- copy an entire publication into statements or raw artifacts;
- combine a publication with pages that it links to;
- invent difficulty, seniority, role expectations, or recommendation strength;
- add prerequisites, topic mappings, learning order, mastery, or progress;
- use paragraph numbers, DOM selectors, generated IDs, or other fragile
  locators;
- convert optional guidance or recommendations into absolute requirements;
- use transcription notes for teaching commentary or project-specific opinions.

## Versioning and updates

`retrieved_on` records the UTC calendar date on which the source was inspected.
Preserve a visible publication version or update label in `version_label`; it
does not replace the repository's integer `source_version`.

Start `source_version` at `1` and keep it equal in `source.yaml` and
`items.yaml`. Increment it when the represented source changes or an updated
source changes extracted meaning. Formatting-only repository edits do not
require an increment.

On update, compare the complete live publication with the reviewed package.
Preserve item IDs when their source meaning remains the same. Add semantic IDs
for new statements, and never silently assign a removed item's ID to different
meaning. Record removals and material ambiguities for the reviewer.

## Review checklist

- [ ] Both YAML files parse directly.
- [ ] Each file passes its Draft 2020-12 schema.
- [ ] Repository semantic validation discovers and accepts the package.
- [ ] Source ID and source version match across the files and package path.
- [ ] Provenance, retrieval date, visible update label, status, and repository
      usage are accurate.
- [ ] The package represents exactly its declared source boundary.
- [ ] All major in-scope sections were inspected and represented where
      applicable.
- [ ] Statements preserve source wording, conditions, and recommendation
      strength without excessive copying.
- [ ] Every locator is manually traceable against visible source structure.
- [ ] IDs are unique, semantic, and suitable for future stable reference.
- [ ] No canonical IDs, normalization decisions, prerequisites, topic mappings,
      difficulty, mastery, learning order, or learner progress leaked into the
      import.
- [ ] Raw artifacts and undeclared files comply with `repository_usage`.
- [ ] Confidentiality, personal-data, licensing, and public-repository safety
      received human review.
