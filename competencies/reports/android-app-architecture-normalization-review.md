# Android app architecture normalization review

## Package summary

- Pilot package: `competencies/normalized/android-app-architecture/`
- Canonical competency count: 11
- Evidence source: `android-developers-app-architecture`, version 1
- Source-item coverage: 19 of 35 imported items
- Package status: `review`

This pilot covers a coherent architecture core. It is not a complete
normalization of the imported publication.

## Evidence coverage

| Canonical competency | Source item evidence |
|---|---|
| `explain-android-component-lifecycle-constraints` | `expect-process-termination`, `keep-state-out-of-activities` |
| `design-independent-app-components` | `keep-app-components-independent`, `keep-entry-points-from-owning-data` |
| `apply-separation-of-concerns` | `define-architecture-boundaries`, `separate-concerns`, `define-module-responsibility-boundaries` |
| `explain-persistent-data-models` | `drive-ui-from-data-models`, `use-persistent-models-for-resilience` |
| `establish-single-source-of-truth` | `assign-single-source-of-truth` |
| `explain-unidirectional-data-flow` | `use-unidirectional-data-flow` |
| `explain-ui-layer-responsibilities` | `render-data-with-ui-elements`, `manage-ui-state-with-state-holders` |
| `design-data-layer-around-repositories` | `include-ui-and-data-layers`, `organize-data-layer-around-repositories` |
| `explain-repository-responsibilities` | `centralize-data-access-in-repositories` |
| `evaluate-optional-domain-layer` | `add-domain-layer-when-needed` |
| `explain-dependency-injection` | `use-modern-architecture-techniques`, `prefer-dependency-injection-with-hilt` |

## Uncovered source items

The following 16 items were intentionally left outside this pilot:

- `use-single-activity-container`
- `handle-form-factor-configuration-changes`
- `implement-adaptive-layouts`
- `choose-source-of-truth-by-app-needs`
- `limit-data-source-responsibility`
- `keep-use-cases-single-purpose`
- `isolate-android-framework-dependencies`
- `expose-minimal-module-api`
- `delegate-boilerplate-to-recommended-libraries`
- `preserve-ui-state-across-configuration-changes`
- `build-reusable-composable-ui`
- `make-parts-testable-in-isolation`
- `let-types-own-concurrency-policy`
- `persist-relevant-fresh-data-for-offline-use`
- `improve-engineering-outcomes-with-architecture`
- `improve-user-outcomes-with-architecture`

They cover navigation composition, adaptive UI, source-of-truth selection,
data-source and use-case boundaries, framework and module API boundaries,
library delegation, testability, concurrency, offline use, and broad
architecture benefits. They remain valid evidence for later normalization.

## Merge decisions

- Process termination and Activity recreation were merged into one explanation
  of lifecycle constraints on retaining application data and state.
- General architecture boundaries, separation of concerns, and module
  responsibilities were merged because they express the same boundary-design
  capability at compatible scopes.
- Persistent-model independence and resilience were merged without prescribing
  a storage technology.
- UI rendering and state-holder responsibilities were retained as complementary
  responsibilities within one UI-layer explanation.
- The data-layer responsibility and repository-organization rule were retained
  together because both are required by the data-layer design outcome.

Items were not merged merely because they shared a publication section.

## Split and reuse decisions

No source item is reused across final pilot competencies. The initial reuse of
`keep-app-components-independent`, `include-ui-and-data-layers`, and
`organize-data-layer-around-repositories` was removed because each final
competency has sufficient narrower evidence without overlapping support. No item
was split to increase the pilot count.

## Canonical wording rationale

Titles use observable actions and avoid publication headings. Outcomes remove
source-relative wording while preserving evidence scope. The dependency-
injection competency generalizes away from Hilt as the canonical identity, but
retains only object construction and framework-container behavior supported by
the evidence. The domain-layer outcome retains the source's optionality rather
than presenting a mandatory pattern.

## Duplicate candidates considered

- Architecture boundaries and separation of concerns were treated as one
  competency rather than near-duplicates.
- Component lifecycle explanation and independent-component design were retained
  as separate capabilities with non-overlapping evidence: one explains platform
  constraints; the other produces a component design under those constraints.
- Data-layer design and repository responsibilities were retained separately:
  one designs the layer boundary, while the other explains the repository's
  coordination contract.
- Persistent models and offline-first persistence were not collapsed. The pilot
  covers model resilience, while the broader offline-use item remains uncovered.
- Domain-layer selection and single-purpose use-case design were not merged. The
  pilot retains the selection competency and leaves use-case design uncovered.

## Rejected or deferred candidates

- MVVM and Clean Architecture competencies were rejected because those labels
  are not explicitly supported by the imported items.
- A Hilt-only canonical identity was rejected as source-specific. Compile-time
  verification was also omitted from the generalized dependency-injection outcome
  because that claim belongs specifically to the imported Hilt recommendation.
- A complete offline-first architecture competency was rejected because one
  persistence recommendation does not support that broader design claim.
- Single-activity navigation, adaptive UI, concurrency, testability, minimal
  module APIs, and architecture-benefit candidates were deferred to keep the
  pilot coherent and limited rather than normalizing all 35 items.

## Task 006.1 editorial review

- Renamed `analyze-android-component-lifecycle-constraints` to
  `explain-android-component-lifecycle-constraints` and narrowed it to Activity
  recreation and process termination. Removed component-independence evidence to
  resolve overlap with component design.
- Narrowed `design-independent-app-components` by removing the unsupported
  `short-lived coordinator` abstraction and the ambiguous `self-contained`
  wording.
- Retained `apply-separation-of-concerns` with a concise outcome and a stronger
  rationale that all three evidence items support cohesive responsibility
  boundaries rather than merely sharing a theme.
- Narrowed persistent-model wording while retaining only lifecycle, process, and
  connectivity effects stated by its two evidence items.
- Removed source-selection and offline-choice evidence from
  `establish-single-source-of-truth`; the final outcome covers ownership,
  immutable exposure, and mutation control.
- Removed the vague phrase `appropriately scoped` from the UI-layer outcome and
  stated the source's explicit state-holder lifetime criterion.
- Narrowed repository responsibilities to the single source item that directly
  states the repository contract. Data-source responsibility remains uncovered.
- Separated optional domain-layer selection from single-purpose use-case design;
  the latter remains uncovered rather than creating a twelfth competency.
- Renamed `apply-dependency-injection` to `explain-dependency-injection` and
  removed the Hilt-specific compile-time verification claim from the generalized
  outcome.
- Removed all three initial evidence reuses. The final pilot contains 11
  competencies, covers 19 of 35 source items, and has no semantic duplicates
  identified by editorial review.
- No unsupported framework labels, claims, or future-model fields were added.

## Task 006.1 technical review

- Both canonical schemas retain `additionalProperties: false` at every object
  level and reject empty or whitespace-only required text.
- Both schemas now fix `schema_version` to the implemented version `1` rather
  than accepting arbitrary future positive integers.
- Canonical evidence resolution continues to require an existing source, an
  exact source version, and existing source item IDs.
- Duplicate evidence comparison now treats `item_ids` as an unordered set, so
  exact evidence repeated in a different item order is rejected.
- Canonical set IDs are checked for duplicates across package directories in
  addition to repository-wide canonical competency ID uniqueness.
- Tests now cover multiple item evidence, within-package and cross-package ID
  duplication, reordered duplicate evidence, whitespace-only text, schema
  version strictness, Boolean versions, malformed canonical YAML, and both
  missing canonical package files.

## Limitations

- Evidence comes from one imported publication, so cross-source identity has not
  yet been exercised by real canonical data.
- Structural validation cannot establish semantic quality or detect semantic
  duplicates; these remain editorial review responsibilities.
- No prerequisites, relations, topics, levels, assessments, learning paths, or
  progress models are included.
- The package remains in `review` and has not been approved.

## Validation

The following commands passed:

```text
python -B scripts/validate_content.py
Content validation passed: 0 topic packages, 2 templates, 4 schema fixtures.

python -B scripts/validate_competencies.py
Competency validation passed: 1 source packages, 1 canonical packages,
2 templates, 13 schema fixtures.

python -B -m unittest discover
Ran 64 tests
OK

python -B -m unittest tests.competency_validator.test_validate_competencies
Ran 49 tests
OK

git diff --check
Exit code 0
```

The Task 005 `source.yaml` and `items.yaml` files were not modified. Their
worktree Git blob hashes match `HEAD`.
