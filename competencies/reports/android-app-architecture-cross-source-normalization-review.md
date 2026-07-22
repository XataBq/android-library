# Android app architecture cross-source normalization review

## Review scope

This review normalizes all 29 items from
`android-developers-architecture-recommendations`, source version 1, against the
complete canonical registry present before Task 008. It records one primary
disposition for every second-source item and updates the Android app architecture
canonical package where the evidence supports a stable capability.

The review does not modify either source package, approve any package, define
relations or prerequisites, create a learning sequence, map topics, or change
the canonical architecture document.

## Input packages and versions

| Input | Version | Status | Role in review |
|---|---:|---|---|
| `android-developers-app-architecture` | 1 | `review` | Existing evidence and uncovered first-source candidates |
| `android-developers-architecture-recommendations` | 1 | `review` | Complete 29-item disposition input |
| `android-app-architecture` | 1 | `review` | Complete pre-normalization canonical registry |

Both source packages were read completely and remain immutable. The original
import and normalization reports were retained as historical records.

## Canonical package before normalization

- Canonical set version: 1
- Status: `review`
- Competency count: 11
- Evidence sources represented: 1
- First-source items represented: 19 of 35
- Second-source items represented: 0 of 29

The registry contained lifecycle, component-independence, responsibility-boundary,
persistent-model, single-source-of-truth, UDF, UI-layer, data-layer, repository,
domain-layer, and dependency-injection capabilities.

## Normalization method

For each second-source item, the review identified the assessable capability,
compared its success criteria with all 11 existing competencies, classified any
partial relationship, and recorded a decision before changing canonical data.
Technology names and recommendation levels were treated as source evidence, not
automatic canonical identity. New competencies were created only after existing
identity, broader or narrower scope, neighboring capabilities, and deferral had
been considered.

Disposition totals are:

| Decision | Items |
|---|---:|
| `attach-existing` | 3 |
| `attach-existing-and-reword` | 3 |
| `create-new` | 13 |
| `split-across-competencies` | 0 |
| `defer` | 10 |
| `blocked-source-issue` | 0 |
| **Total** | **29** |

The 13 `create-new` dispositions jointly support eight new competencies; several
source rows describe complementary evidence for the same capability.

## Complete source-item disposition matrix

| Source item ID | Declared level | Candidate capability | Existing competency candidate | Relationship classification | Decision | Canonical competency ID | Wording change required | Notes |
|---|---|---|---|---|---|---|---|---|
| `define-data-layer-with-repositories` | Strongly recommended | Define a data layer around repositories | `design-data-layer-around-repositories` | `multi-capability` | `attach-existing-and-reword` | `design-data-layer-around-repositories` | Yes | Core layer and repository boundary matches; small-app packaging detail remains source-only. |
| `define-ui-layer` | Strongly recommended | Define UI responsibility and select Compose | `explain-ui-layer-responsibilities` | `multi-capability`; `conflict or tension` | `defer` | — | No | It covers only part of the existing outcome, duplicates a separate Compose row, and contains the source's ambiguous `data layer types` packaging sentence. |
| `expose-data-through-repositories` | Strongly recommended | Prevent UI-to-data-source access | `design-data-layer-around-repositories`; `explain-repository-responsibilities` | `narrower` | `attach-existing` | `design-data-layer-around-repositories` | Yes, jointly with the first row | It completes the layer boundary but does not support the full repository coordination outcome. |
| `communicate-between-layers-with-coroutines-flows` | Strongly recommended | Use Kotlin async streams across layers | None | `distinct capability` | `create-new` | `use-coroutines-and-flows-across-layers` | New record | Combined with the ViewModel-specific coroutine row. |
| `use-domain-layer-in-big-apps` | Recommended in big apps | Evaluate a domain layer for complexity or reuse | `evaluate-optional-domain-layer` | `recommendation-strength difference` | `attach-existing` | `evaluate-optional-domain-layer` | No | Same assessment boundary; big-app priority and ViewModel examples remain source-level. |
| `follow-udf-with-viewmodel-ui-state` | Strongly recommended | Apply state-out/actions-in UDF | `explain-unidirectional-data-flow` | `technology-specific specialization` | `attach-existing-and-reword` | `explain-unidirectional-data-flow` | Yes | ViewModel is an implementation specialization of the existing flow identity. |
| `use-aac-viewmodels-when-beneficial` | Strongly recommended | Use ViewModel as a UI-state producer when beneficial | `explain-ui-layer-responsibilities` | `technology-specific specialization` | `create-new` | `design-viewmodel-ui-state` | New record | A ViewModel design capability is independently assessable from explaining the full UI layer. |
| `collect-ui-state-lifecycle-aware` | Strongly recommended | Collect Compose UI state with lifecycle awareness | `explain-android-component-lifecycle-constraints` | `adjacent`; `technology-specific specialization` | `create-new` | `handle-compose-lifecycle-work` | New record | Combined with the broader lifecycle-effects row to avoid overlapping Compose lifecycle competencies. |
| `process-viewmodel-events-as-state-updates` | Strongly recommended | Convert handled UI events into state updates | `explain-unidirectional-data-flow` | `narrower` | `attach-existing` | `explain-unidirectional-data-flow` | Yes, jointly with the UDF row | Supplies the event-handling portion of the shared UDF cycle. |
| `use-single-activity-with-navigation` | Strongly recommended | Host screens in one Activity and navigate within it | None; first source has an uncovered matching item | `recommendation-strength difference` | `create-new` | `design-single-activity-navigation` | New record | Navigation 3 remains evidence detail, not canonical identity. |
| `use-compose-for-new-apps` | Strongly recommended | Select Compose as the UI toolkit for new apps | `explain-ui-layer-responsibilities` | `technology-specific specialization` | `defer` | — | No | Toolkit adoption alone does not yet define a stable architecture capability. |
| `keep-viewmodels-lifecycle-independent` | Strongly recommended | Isolate ViewModels from framework dependencies | `explain-android-component-lifecycle-constraints`; `design-independent-app-components` | `adjacent` | `create-new` | `isolate-android-framework-dependencies` | New record | The dependency boundary is distinct from state ownership and component coordination. |
| `use-flows-and-suspend-functions-in-viewmodels` | Strongly recommended | Use flows and suspend actions at the ViewModel boundary | None | `technology-specific specialization` | `create-new` | `use-coroutines-and-flows-across-layers` | New record | Complements the layer-level coroutine recommendation without creating a ViewModel-only duplicate. |
| `scope-viewmodels-to-screens` | Strongly recommended | Scope ViewModels to screen-level or explicitly complex UI | `explain-ui-layer-responsibilities` | `adjacent` | `create-new` | `select-ui-state-holders-by-scope` | New record | Selection by UI scope is independently assessable from explaining responsibilities. |
| `use-plain-state-holders-in-reusable-ui` | Strongly recommended | Use hoistable plain holders for reusable UI | `explain-ui-layer-responsibilities` | `adjacent` | `create-new` | `select-ui-state-holders-by-scope` | New record | Forms the reusable-UI side of the state-holder selection boundary. |
| `avoid-androidviewmodel` | Recommended | Remove Application dependencies from ViewModels | `explain-android-component-lifecycle-constraints` | `technology-specific specialization` | `create-new` | `isolate-android-framework-dependencies` | New record | Combined with general framework-isolation evidence rather than creating an AndroidViewModel-only competency. |
| `expose-viewmodel-ui-state` | Recommended | Model and expose ViewModel UI state with StateFlow | `explain-ui-layer-responsibilities` | `technology-specific specialization` | `create-new` | `design-viewmodel-ui-state` | New record | StateFlow construction choices qualify one ViewModel state-design capability. |
| `use-lifecycle-aware-compose-effects` | Strongly recommended | Handle Compose lifecycle work without Activity callbacks | `explain-android-component-lifecycle-constraints` | `adjacent`; `technology-specific specialization` | `create-new` | `handle-compose-lifecycle-work` | New record | The source contains enough API-selection detail for an independently demonstrable Compose capability. |
| `use-constructor-dependency-injection` | Strongly recommended | Supply dependencies through constructor injection | `explain-dependency-injection` | `narrower` | `attach-existing-and-reword` | `explain-dependency-injection` | Yes | Refines the existing general construction identity without making Hilt canonical. |
| `scope-shared-or-expensive-types` | Strongly recommended | Scope shared mutable or expensive dependencies | `explain-dependency-injection` | `adjacent` | `create-new` | `scope-dependencies-when-needed` | New record | Scoping conditions have a separate assessment boundary from explaining DI. |
| `choose-hilt-for-complex-projects` | Recommended | Choose Hilt according to project complexity | `explain-dependency-injection` | `technology-specific specialization`; `conflict or tension` | `defer` | — | No | Hilt selection is narrower than DI identity and differs in prescriptiveness from the first source's Hilt key point. |
| `test-viewmodels-data-layer-and-navigation` | Strongly recommended | Define minimum tests across three architecture areas | None | `multi-capability` | `defer` | — | No | Splitting the row would require evidence from the excluded testing publications to define stable assessment boundaries. |
| `prefer-fakes-to-mocks` | Strongly recommended | Select test doubles | None | `insufficient evidence` | `defer` | — | No | The in-scope statement provides no criteria; the linked test-double publication was not imported. |
| `test-stateflow-values` | Strongly recommended | Test StateFlow values and sharing policy | None | `technology-specific specialization` | `defer` | — | No | Reconsider with imported coroutine-testing evidence rather than canonizing two terse implementation instructions. |
| `separate-layer-models-in-complex-apps` | Recommended | Evaluate layer-specific model mappings | None | `distinct capability` | `create-new` | `evaluate-layer-specific-models` | New record | Preserves complex-app scope and conditional examples. |
| `name-methods-with-verb-phrases` | Optional | Name methods by action | None | `adjacent` | `defer` | — | No | A general code-quality convention is outside this architecture set and needs registry-wide placement review. |
| `name-properties-with-noun-phrases` | Optional | Name properties by entity or state | None | `adjacent` | `defer` | — | No | Reconsider in a code-quality or naming competency set with independent evidence. |
| `name-stream-functions-by-model` | Optional | Apply source-specific stream naming | None | `technology-specific specialization` | `defer` | — | No | The convention is optional, narrow, and unsupported by an independent source. |
| `name-interface-implementations-meaningfully` | Optional | Name concrete and fake implementations | None | `adjacent` | `defer` | — | No | Reconsider with a broader naming source and a registry-wide package decision. |

Every second-source item appears exactly once as a primary matrix row.

## Evidence attached to existing competencies

| Existing competency | Original evidence | New second-source items | Wording changed | Identity and strength analysis |
|---|---|---|---|---|
| `design-data-layer-around-repositories` | `include-ui-and-data-layers`, `organize-data-layer-around-repositories` | `define-data-layer-with-repositories`, `expose-data-through-repositories` | Yes | Both sources assess designing a data layer around repository-mediated access. The second source marks both rows strongly recommended; strength remains evidence metadata. |
| `explain-unidirectional-data-flow` | `use-unidirectional-data-flow` | `follow-udf-with-viewmodel-ui-state`, `process-viewmodel-events-as-state-updates` | Yes | Both sources assess the state-out/action-or-event-back cycle. ViewModel is a narrower implementation, not a new identity. |
| `evaluate-optional-domain-layer` | `add-domain-layer-when-needed` | `use-domain-layer-in-big-apps` | No | Both assess whether complexity or reused logic justifies a domain layer. `Recommended in big apps` is compatible additional scope, not canonical priority. |
| `explain-dependency-injection` | `use-modern-architecture-techniques`, `prefer-dependency-injection-with-hilt` | `use-constructor-dependency-injection` | Yes | The shared identity is moving construction out of consumers and supplying dependencies. Constructor injection broadens evidence without creating a Hilt competency. |

Evidence was not added to `explain-repository-responsibilities` from
`expose-data-through-repositories`: that item supports the repository boundary
but not centralizing changes, resolving conflicts, and the other full
responsibility criteria.

## Existing competencies reworded

All 11 pre-existing IDs remain stable. Their review classifications are:

| Existing competency | Classification |
|---|---|
| `explain-android-component-lifecycle-constraints` | `unchanged` |
| `design-independent-app-components` | `unchanged` |
| `apply-separation-of-concerns` | `unchanged` |
| `explain-persistent-data-models` | `unchanged` |
| `establish-single-source-of-truth` | `unchanged` |
| `explain-unidirectional-data-flow` | `wording-refined` |
| `explain-ui-layer-responsibilities` | `requires-new-neighboring-competency` |
| `design-data-layer-around-repositories` | `wording-refined` |
| `explain-repository-responsibilities` | `unchanged` |
| `evaluate-optional-domain-layer` | `evidence-expanded` |
| `explain-dependency-injection` | `wording-refined` |

Three outcomes changed without changing identity:

### `explain-unidirectional-data-flow`

- Before: Explain how application state flows toward the UI while events flow
  back toward the source of truth that performs data changes.
- After: Explain how application state flows toward the UI, UI actions or
  events flow toward the state owner, and handling results are represented as
  updated state.
- Justification: both sources assess the same directional state-and-event cycle;
  the new wording accommodates the ViewModel formulation without requiring it.

### `design-data-layer-around-repositories`

- Before: Design a data layer that contains application business logic and
  exposes application data through repositories organized by distinct data
  types.
- After: Design a clearly defined data layer that contains application business
  logic and exposes application data through repositories rather than allowing
  other layers to access data sources directly.
- Justification: the revised boundary is supported across both publications and
  preserves the same data-layer design assessment while avoiding one source's
  repository-count formulation.

### `explain-dependency-injection`

- Before: Explain how dependency-injection practices delegate object
  construction to a dependency tree and can provide dependencies to Android
  framework classes.
- After: Explain how dependency injection moves object construction out of
  consumers so dependencies can be supplied through constructors or
  framework-aware containers.
- Justification: constructor injection broadens the evidence for the same
  construction capability. Hilt remains evidence detail, so the stable ID is
  still accurate.

## New canonical competencies

| New competency | Evidence | Distinction from neighbors |
|---|---|---|
| `design-single-activity-navigation` | First source `use-single-activity-container`; second source `use-single-activity-with-navigation` | App composition and navigation, not lifecycle state ownership. |
| `use-coroutines-and-flows-across-layers` | `communicate-between-layers-with-coroutines-flows`, `use-flows-and-suspend-functions-in-viewmodels` | Kotlin inter-layer communication, not UDF direction or concurrency policy. |
| `design-viewmodel-ui-state` | `use-aac-viewmodels-when-beneficial`, `expose-viewmodel-ui-state` | ViewModel-specific state design, not the general UI responsibility explanation. |
| `isolate-android-framework-dependencies` | First source `isolate-android-framework-dependencies`; second source `keep-viewmodels-lifecycle-independent`, `avoid-androidviewmodel` | Dependency isolation, not independent app-component data ownership. |
| `select-ui-state-holders-by-scope` | `scope-viewmodels-to-screens`, `use-plain-state-holders-in-reusable-ui` | State-holder selection and scope, not responsibility explanation. |
| `handle-compose-lifecycle-work` | `collect-ui-state-lifecycle-aware`, `use-lifecycle-aware-compose-effects` | Lifecycle-aware Compose work, not lifecycle constraints on data ownership. |
| `scope-dependencies-when-needed` | `scope-shared-or-expensive-types` | Dependency lifetime and reuse, not object-construction explanation. |
| `evaluate-layer-specific-models` | `separate-layer-models-in-complex-apps` | Conditional model mapping, not persistence or single-source-of-truth ownership. |

No new competency is identified only by a publication, section, recommendation
level, or library name.

## Source items split across competencies

No second-source item was split across multiple competencies, and no evidence
item is reused across canonical competencies in version 2. Multi-capability
rows were either represented by one coherent capability with inseparable
qualifications or deferred when a defensible split required out-of-scope
evidence.

## Deferred source items

| Source item | Reason | Reconsideration condition |
|---|---|---|
| `define-ui-layer` | Partial UI-responsibility overlap, separate Compose claim, and ambiguous packaging wording | A corrected source version or independent UI-layer evidence that supports one complete assessment boundary |
| `use-compose-for-new-apps` | Toolkit adoption alone is not a stable architecture capability | Import Compose architecture guidance that defines a demonstrable capability |
| `choose-hilt-for-complex-projects` | Hilt-specific selection and cross-source prescriptiveness tension | Import Hilt or DI guidance and review technology-selection identity |
| `test-viewmodels-data-layer-and-navigation` | Three test domains in one row; a split would rely on linked testing content | Import the testing publication and define stable test-design boundaries |
| `prefer-fakes-to-mocks` | The in-scope statement lacks selection criteria | Import the linked test-double publication or independent evidence |
| `test-stateflow-values` | Narrow API instructions without broader test rationale | Import coroutine/StateFlow testing evidence |
| `name-methods-with-verb-phrases` | Optional general naming convention outside the current package boundary | Establish a code-quality registry area with independent evidence |
| `name-properties-with-noun-phrases` | Optional general naming convention outside the current package boundary | Establish a code-quality registry area with independent evidence |
| `name-stream-functions-by-model` | Optional source-specific Flow naming convention | Independent naming evidence and registry placement review |
| `name-interface-implementations-meaningfully` | Optional general naming convention outside the current package boundary | Establish a code-quality registry area with independent evidence |

Deferral preserves all source evidence for later work and does not reject the
recommendations themselves.

## Duplicate and near-duplicate review

- A second general UI-layer competency was rejected because
  `explain-ui-layer-responsibilities` already owns that assessment boundary;
  narrower ViewModel and state-holder decisions became distinct neighbors.
- A separate repository-access competency was rejected. Repository-mediated
  layer access belongs to `design-data-layer-around-repositories`; it does not
  duplicate the fuller repository-responsibility explanation.
- A ViewModel-specific UDF competency was rejected because the state/action
  cycle is the same capability as `explain-unidirectional-data-flow`.
- Separate layer-level and ViewModel coroutine competencies were rejected in
  favor of one cross-layer Kotlin communication competency.
- Separate screen-ViewModel and reusable-state-holder competencies were rejected
  in favor of one selection-by-scope capability.
- Separate lifecycle-aware state-collection and Compose-effect competencies
  were rejected in favor of one lifecycle-work capability.
- An AndroidViewModel-only competency was rejected in favor of the broader,
  cross-source framework-dependency isolation capability.
- A Hilt-only competency was rejected because Hilt choice is a technology
  specialization and the sources differ in prescriptiveness.
- A universal one-model-per-layer competency was rejected; the new evaluation
  competency preserves complex-app conditions.
- A Compose-toolkit adoption competency was rejected pending evidence of a
  stable demonstrable architecture capability.

The 19 resulting competencies have distinct primary actions and assessment
boundaries. No semantic duplicate was identified.

## Recommendation-strength observations

- The first source has no item-level `declared_level`; the second source labels
  20 items strongly recommended, four recommended, one recommended in big apps,
  and four optional. Canonical records do not convert these labels into priority.
- Single-activity design is descriptive in the first source and strongly
  recommended in the second. The capability is compatible despite different
  strength.
- Domain-layer use is optional and need-based in the first source and
  recommended in big apps in the second. Both retain complexity or reuse as the
  selection criterion.
- Dependency injection is a key point in the first source and strongly
  recommended in the second. Hilt is broad in the first source but conditional
  on project complexity in the second.
- `use-aac-viewmodels-when-beneficial` is strongly recommended while retaining
  an explicit applicability condition. The canonical wording does not erase it.
- Optional naming conventions remain deferred; optionality was not mistaken for
  learner difficulty or low competency importance.

## Conflicts and tensions

| Area | Classification | Resolution |
|---|---|---|
| Domain-layer size and optionality | `different strength`; compatible elaboration | Attach to the existing evaluation competency and preserve priority in evidence analysis. |
| Hilt versus manual DI | `different scope`; `conflict or tension` in prescriptiveness | Keep DI library-neutral and defer Hilt selection. |
| UI-layer small-app packaging sentence | `actual tension` within the second source wording | Defer the row; do not silently correct `data layer types` to UI-layer types. |
| ViewModel recommendation | `different scope` | Preserve the “when beneficial” condition in the ViewModel competency notes. |
| Single-activity navigation | `different strength`; compatible elaboration | Create one cross-source capability and omit Navigation 3 from canonical identity. |
| Framework isolation | `narrower specialization` | Combine the first source's general rule with ViewModel-specific second-source evidence. |
| Layer-specific models | `different scope` | Preserve the complex-app condition and use an evaluation outcome. |

No contradiction blocks any accepted evidence attachment or new competency.

## Canonical package after normalization

- Canonical set version: 2
- Status: `review`
- Competency count: 19
- Existing IDs preserved: 11 of 11
- Existing competencies with second-source evidence: 4
- Existing competencies reworded: 3
- New competencies: 8
- Evidence sources represented: 2
- First-source items represented: 21 of 35
- Second-source items represented: 19 of 29
- Deferred second-source items: 10
- Source items reused across competencies: 0

The package remains a reviewed canonical registry, not a relation graph,
learning sequence, assessment model, or topic mapping.

## Canonical model validation

| Model capability | Result |
|---|---|
| Multiple source packages | Represented without schema changes |
| Evidence aggregation | Existing competencies contain separate versioned entries for both sources |
| Exact-match attachment | Supported by domain-layer evidence expansion |
| Partial-overlap decisions | Recorded explicitly in the disposition matrix and report |
| New competency creation | Eight distinct capabilities added under the existing schema |
| Source-item reuse or splitting | Evaluated; neither was necessary for the final version |
| Versioned evidence | Both sources resolve at exact `source_version: 1` |
| Stable IDs | All 11 version-1 IDs preserved |
| Package versioning | Metadata and competency list advanced together to version 2 |
| Duplicate prevention | Structural checks pass; semantic duplicates were reviewed manually |
| Human-review traceability | Wording, evidence, deferrals, conflicts, and counts are recorded here |

The model required no unsupported fields, structural workarounds, schema
changes, validator changes, or source mutations. Recommendation strength and
disposition remain editorial report concerns by design. A machine-readable
disposition catalog could be a future convenience, but its absence did not
prevent faithful normalization.

## Model acceptance recommendation

**ACCEPT**

The two-source exercise validates stable identity, evidence aggregation,
versioning, partial-overlap review, new capability creation, and deferral using
the existing model and validator. Remaining limitations are editorial or future
workflow enhancements rather than structural defects. The architecture model
document must nevertheless remain `PROPOSED` until the human owner approves a
status transition.

## Validation results

- `python -B scripts/validate_content.py` passed: 0 topic packages, 2 templates,
  and 4 schema fixtures.
- `python -B scripts/validate_competencies.py` passed: 2 source packages, 1
  canonical package, 2 templates, and 13 schema fixtures.
- `python -B -m unittest discover` passed: 64 tests.
- `git diff --check` passed.
- Direct YAML parsing confirmed version consistency, 19 unique canonical IDs,
  and exact resolution of all 19 normalized second-source items.
- Mechanical report review confirmed 29 unique disposition rows with no missing
  or extra source items.

## Human review checklist

- [ ] Confirm all 29 second-source items appear exactly once in the disposition matrix.
- [ ] Confirm each evidence attachment matches the competency's assessment boundary.
- [ ] Confirm all 11 existing IDs remain stable and all wording changes preserve identity.
- [ ] Confirm all eight new competencies are distinct and independently assessable.
- [ ] Confirm all deferred items have concrete reasons and reconsideration conditions.
- [ ] Confirm recommendation-strength differences and source tensions are accurately preserved.
- [ ] Confirm no semantic duplicate was introduced.
- [ ] Confirm canonical version fields both equal 2 and status remains `review`.
- [ ] Confirm both source packages are byte-for-byte unchanged.
- [ ] Confirm no relations, prerequisites, sequence, topic mapping, difficulty, assessment, or progress fields were added.
- [ ] Confirm the architecture model remains `PROPOSED` pending human approval.
