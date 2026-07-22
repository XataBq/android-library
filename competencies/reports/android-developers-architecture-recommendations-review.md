# Android Developers architecture recommendations import review

## Package summary

- Source ID: `android-developers-architecture-recommendations`
- Source version: `1`
- Package status: `review`
- Source title: *Recommendations for Android architecture*
- Publisher: Android Developers
- Canonical English URL:
  https://developer.android.com/topic/architecture/recommendations?hl=en
- Retrieved on: 2026-07-22 UTC
- Visible update label: `Last updated 2026-04-26 UTC`
- Repository usage: `citation-only`
- Imported item count: 29

The package awaits human review. This report records extraction decisions and
does not approve the source package or perform normalization.

## Source boundary

The package represents exactly the live English publication at the canonical
URL above. The in-scope content begins with the publication introduction and
priority definitions, continues through the recommendation sections from
Layered architecture to Naming conventions, and includes qualifications shown
inside each recommendation row.

The boundary does not include navigation chrome, linked publications,
Additional resources content, code samples, feedback controls, footer content,
or material inferred from general Android knowledge. The general *Guide to app
architecture* page remains represented by its existing, separate source
package.

## Extraction approach

Each of the page's 29 visible recommendation rows became one source item. A row
was kept intact when its bullets supplied conditions, examples, exceptions, or
technology choices for the same recommendation. Section introductions and the
page-level priority framework were recorded as context rather than turned into
items. Code blocks were inspected but not extracted as separate statements.

Statements are concise owner-authored summaries suitable for
`citation-only`. Stable semantic IDs describe source-level recommendations,
`context` preserves the visible section, and each locator uses the section
heading plus the displayed recommendation label. No canonical identity,
evidence attachment, deduplication, or competency wording decision is encoded.

## Recommendation priority handling

The page says its guidance is not a set of strict requirements and should be
adapted to the app. Its priority definitions distinguish practices that should
normally be implemented, practices likely to improve an app, and practices
useful only in some circumstances. Every row's displayed label is preserved
verbatim in `declared_level`.

The page also uses `Recommended in big apps` for the domain-layer row even
though the introductory list names only `Strongly recommended`, `Recommended`,
and `Optional`. The extraction retains that fourth displayed label instead of
collapsing it into `Recommended`.

| Declared level | Items |
|---|---:|
| `Strongly recommended` | 20 |
| `Recommended` | 4 |
| `Recommended in big apps` | 1 |
| `Optional` | 4 |
| **Total** | **29** |

## Section coverage

| In-scope section | Strongly recommended | Recommended | Recommended in big apps | Optional | Total |
|---|---:|---:|---:|---:|---:|
| Introduction and priority definitions | 0 | 0 | 0 | 0 | 0 |
| Layered architecture | 4 | 0 | 1 | 0 | 5 |
| UI layer | 6 | 0 | 0 | 0 | 6 |
| ViewModel | 4 | 2 | 0 | 0 | 6 |
| Lifecycle | 1 | 0 | 0 | 0 | 1 |
| Handle dependencies | 2 | 1 | 0 | 0 | 3 |
| Testing | 3 | 0 | 0 | 0 | 3 |
| Models | 0 | 1 | 0 | 0 | 1 |
| Naming conventions | 0 | 0 | 0 | 4 | 4 |
| Additional resources | 0 | 0 | 0 | 0 | 0 |
| **Total** | **20** | **4** | **1** | **4** | **29** |

The introduction produced no item because it defines the page's purpose,
non-binding recommendation semantics, and priority vocabulary rather than an
independent recommendation row. Additional resources produced no item because
it is a list of out-of-scope linked publications.

Section item IDs are:

- **Layered architecture:** `define-data-layer-with-repositories`,
  `define-ui-layer`, `expose-data-through-repositories`,
  `communicate-between-layers-with-coroutines-flows`,
  `use-domain-layer-in-big-apps`.
- **UI layer:** `follow-udf-with-viewmodel-ui-state`,
  `use-aac-viewmodels-when-beneficial`,
  `collect-ui-state-lifecycle-aware`,
  `process-viewmodel-events-as-state-updates`,
  `use-single-activity-with-navigation`, `use-compose-for-new-apps`.
- **ViewModel:** `keep-viewmodels-lifecycle-independent`,
  `use-flows-and-suspend-functions-in-viewmodels`,
  `scope-viewmodels-to-screens`,
  `use-plain-state-holders-in-reusable-ui`, `avoid-androidviewmodel`,
  `expose-viewmodel-ui-state`.
- **Lifecycle:** `use-lifecycle-aware-compose-effects`.
- **Handle dependencies:** `use-constructor-dependency-injection`,
  `scope-shared-or-expensive-types`, `choose-hilt-for-complex-projects`.
- **Testing:** `test-viewmodels-data-layer-and-navigation`,
  `prefer-fakes-to-mocks`, `test-stateflow-values`.
- **Models:** `separate-layer-models-in-complex-apps`.
- **Naming conventions:** `name-methods-with-verb-phrases`,
  `name-properties-with-noun-phrases`, `name-stream-functions-by-model`,
  `name-interface-implementations-meaningfully`.

## Item inventory

| Item ID | Section | Declared level | Extraction note |
|---|---|---|---|
| `define-data-layer-with-repositories` | Layered architecture | Strongly recommended | Keeps repository creation and small-app packaging with the data-layer row. |
| `define-ui-layer` | Layered architecture | Strongly recommended | Retains Compose scope and the source's ambiguous small-app packaging sentence. |
| `expose-data-through-repositories` | Layered architecture | Strongly recommended | Keeps all displayed data-source examples as one repository-boundary recommendation. |
| `communicate-between-layers-with-coroutines-flows` | Layered architecture | Strongly recommended | Limited to communication between layers. |
| `use-domain-layer-in-big-apps` | Layered architecture | Recommended in big apps | Preserves app-size scope and both stated reasons for a domain layer. |
| `follow-udf-with-viewmodel-ui-state` | UI layer | Strongly recommended | Preserves the page's ViewModel state/action formulation of UDF. |
| `use-aac-viewmodels-when-beneficial` | UI layer | Strongly recommended | Retains the condition that ViewModel benefits apply. |
| `collect-ui-state-lifecycle-aware` | UI layer | Strongly recommended | Keeps the named lifecycle-aware Compose collection API. |
| `process-viewmodel-events-as-state-updates` | UI layer | Strongly recommended | Keeps immediate processing and state update together. |
| `use-single-activity-with-navigation` | UI layer | Strongly recommended | Retains the multi-screen condition and Navigation 3 scope. |
| `use-compose-for-new-apps` | UI layer | Strongly recommended | Limited to new apps and the listed form factors. |
| `keep-viewmodels-lifecycle-independent` | ViewModel | Strongly recommended | Retains prohibited lifecycle-related dependencies and the layer-reconsideration condition. |
| `use-flows-and-suspend-functions-in-viewmodels` | ViewModel | Strongly recommended | Keeps receive and action mechanisms in one row. |
| `scope-viewmodels-to-screens` | ViewModel | Strongly recommended | Keeps screen/destination scope and the direct composable-scoping qualification. |
| `use-plain-state-holders-in-reusable-ui` | ViewModel | Strongly recommended | Preserves reusable-UI scope and externally controlled state. |
| `avoid-androidviewmodel` | ViewModel | Recommended | Keeps the alternative class and dependency relocation. |
| `expose-viewmodel-ui-state` | ViewModel | Recommended | Keeps StateFlow choices, unrelated-data exception, and UI-state representation options together. |
| `use-lifecycle-aware-compose-effects` | Lifecycle | Strongly recommended | Keeps four task-specific lifecycle API choices; excludes the code sample. |
| `use-constructor-dependency-injection` | Handle dependencies | Strongly recommended | Preserves constructor injection as the main approach when possible. |
| `scope-shared-or-expensive-types` | Handle dependencies | Strongly recommended | Retains both conditions for dependency-container scope. |
| `choose-hilt-for-complex-projects` | Handle dependencies | Recommended | Keeps manual DI for simple apps and the three example Hilt criteria. |
| `test-viewmodels-data-layer-and-navigation` | Testing | Strongly recommended | Keeps the hello-world exception and minimum test categories together. |
| `prefer-fakes-to-mocks` | Testing | Strongly recommended | Imports the recommendation label without linked-page detail. |
| `test-stateflow-values` | Testing | Strongly recommended | Keeps both testing instructions in one item. |
| `separate-layer-models-in-complex-apps` | Models | Recommended | Preserves complex-app scope and treats mappings as examples. |
| `name-methods-with-verb-phrases` | Naming conventions | Optional | Keeps the displayed method-name convention. |
| `name-properties-with-noun-phrases` | Naming conventions | Optional | Keeps the displayed property-name convention. |
| `name-stream-functions-by-model` | Naming conventions | Optional | Preserves singular and plural stream naming. |
| `name-interface-implementations-meaningfully` | Naming conventions | Optional | Keeps meaningful, `Default`, and `Fake` naming cases together. |

## Linked material intentionally excluded

No linked page was used as an extraction source. Excluded linked material
includes:

- the general Architecture guidance and Guide to app architecture;
- data-layer, repository, UI-layer, domain-layer, and UDF publications;
- coroutine and Flow guidance;
- ViewModel, UI-event, state-holder, lifecycle, and saved-state publications;
- Compose, Navigation 3, deep-link, adaptive UI, and Views-specific guidance;
- dependency injection, manual DI, Hilt, WorkManager, and navigation-back-stack
  publications;
- Android testing, test-double, StateFlow, and Compose-testing publications;
- external Medium, Kotlin, and GitHub examples;
- the Additional resources links for Compose UI Architecture, Jetpack Compose
  architectural layering, and Recommendations for Android architecture (Views).

Link labels and technologies visible inside a recommendation row were retained
only where needed to preserve that row's own meaning. Linked explanations,
samples, and implementation details were not imported.

## Potential overlap for future normalization

The following are candidate comparison areas for Task 008, not final
equivalence or merge decisions:

- defined UI and data layers may overlap the existing layered-architecture
  source items and canonical layer-responsibility competencies;
- repository-mediated data access may overlap existing repository boundary and
  responsibility evidence;
- UDF and ViewModel-exposed UI state may overlap the existing UDF pilot while
  adding a more implementation-specific formulation;
- the big-app domain-layer condition may overlap the existing optional-domain
  guidance, but its size qualification and ViewModel-specific reasons require
  review;
- dependency injection and Hilt guidance may overlap the existing dependency
  management source item, while constructor injection, scoping, and project
  complexity may be distinct;
- lifecycle-independent ViewModels and lifecycle-aware UI collection may
  overlap existing component-independence or state-holder boundaries without
  necessarily being equivalent;
- the single-activity recommendation may overlap the first source's app
  composition item, with Navigation 3 adding source-specific scope;
- UI rendering, state holders, repositories, and use cases may overlap existing
  responsibilities but must be compared using the actual item text;
- testing, model mapping, naming conventions, Compose-only lifecycle effects,
  and several ViewModel details may be new candidate capabilities rather than
  overlaps.

No evidence was attached, no canonical competency was created or edited, and no
duplicate resolution was made.

## Ambiguities and transcription decisions

- The page says recommendations are adaptable and not strict requirements;
  item wording and `declared_level` preserve that framing.
- `Recommended in big apps` is displayed for the domain layer but is not one of
  the three priorities defined in the introduction. It remains exact.
- The clearly defined UI-layer row says that “data layer types” may be placed in
  a `ui` package or module in small apps. The extraction retains and flags the
  wording rather than silently changing it to “UI layer types.”
- The AAC ViewModel row is strongly recommended but expressly conditioned on
  its benefits applying to the app.
- The screen-level ViewModel row discourages ViewModels in reusable UI and also
  presents `rememberViewModelStoreOwner()` for more complex or state-driven
  composables. Both statements remain in one item because the source presents
  them in the same row.
- The UI-state row allows multiple properties for unrelated data and different
  StateFlow construction approaches. These are qualifications, not separate
  recommendations.
- The Hilt row permits manual DI in simple apps and supplies example indicators
  of complexity. It was not broadened into a universal Hilt requirement.
- The testing row exempts only projects as simple as hello world and presents a
  minimum list. The list remains inseparable from the recommendation.
- The model row is limited to complex apps and uses conditional examples; it was
  not converted into a universal one-model-per-layer rule.
- Three code snippets illustrate state collection, ViewModel state exposure,
  and lifecycle effects. They were inspected for context but not extracted as
  items.

## Public-repository safety

The package is `citation-only`. It stores metadata, locators, and concise
owner-authored summaries rather than page HTML, code samples, or a full-text
copy. No `raw/` directory or artifact is included. Schema validity does not
establish copyright or licensing permission; final repository-use review
remains a human responsibility.

## Validation results

- `python -B scripts/validate_content.py` passed: 0 topic packages, 2 templates,
  and 4 schema fixtures.
- `python -B scripts/validate_competencies.py` passed: 2 source packages, 1
  canonical package, 2 templates, and 13 schema fixtures.
- `python -B -m unittest discover` passed: 64 tests.
- `git diff --check` passed.
- Direct YAML parsing confirmed 29 unique item IDs and the priority and section
  counts reported above.

## Human review checklist

- [ ] Confirm the package boundary is exactly the live English publication.
- [ ] Confirm every in-scope section and all 29 recommendation rows are accounted for.
- [ ] Confirm every `declared_level` matches the displayed source priority.
- [ ] Confirm conditions, exceptions, size qualifications, and technology scope are faithful.
- [ ] Confirm every heading and recommendation-label locator is manually traceable.
- [ ] Confirm item granularity follows recommendation rows without splitting qualifications.
- [ ] Confirm no linked-page or code-sample content leaked into statements.
- [ ] Confirm no normalization, evidence attachment, or canonical wording leaked into the package.
- [ ] Confirm citation-only summaries and metadata are suitable for public-repository review.
