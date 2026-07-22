# Android Developers App Architecture Import Review

## Package

- Source package ID: `android-developers-app-architecture`
- Source title: *Guide to app architecture*
- Official URL: https://developer.android.com/topic/architecture
- Publisher: Google / Android Developers
- Retrieved on: 2026-07-21 UTC
- Visible source update label: `Last updated 2026-04-14 UTC`
- Source version: `1`
- Package status: `review`
- Repository usage: `citation-only`
- Extracted item count: 35

The package awaits human review. This report does not approve the extraction.

## Sections inspected and represented

The complete live publication was inspected. Extracted items represent:

- App composition, including Multiple form factors, Resource constraints, and
  Variable launch conditions;
- Common architectural principles, including Separation of concerns, Adaptive
  layouts, Drive UI from data models, Single source of truth, and
  Unidirectional data flow;
- Recommended app architecture, including Modern app architecture, UI layer,
  Data layer, and the optional Domain layer;
- Manage dependencies between components;
- General best practices;
- Benefits of architecture.

## Intentionally excluded material

The page introduction was treated as framing rather than split into an
additional item. Figure images and alt text, diagrams, navigation chrome,
feedback controls, footer content, license text, and sample links were not
imported. No code sample, image, screenshot, PDF, HTML snapshot, cached page, or
other source artifact was stored.

Every linked publication remains outside this package. In particular, the
following were not opened as extraction sources and their content was not
imported:

- Architecture recommendations;
- UI layer;
- Data layer;
- Domain layer.

The same boundary applies to other linked pages, including app components,
adaptive layouts, Compose guidance, unidirectional data flow, dependency
injection, Hilt, modularization, samples, and design galleries. Link text visible
inside the in-scope publication was used only to understand its own statements.

## Extraction approach

Items are concise English transcriptions of source-level principles,
responsibilities, constraints, techniques, or stated benefits. IDs are semantic
kebab-case names rather than sequence numbers. `context` follows visible source
headings from broadest to most specific. Locators use visible headings; where
several items share a heading, `details` records a recognizable lead-in from the
same publication.

The extraction preserves recommendation strength and conditions. For example,
the domain layer remains optional and conditional, the database is described as
the typical source of truth for offline-first application data rather than a
universal rule, and general best practices remain recommendations rather than
schema-enforced requirements.

## Notable transcription decisions

- The Variable launch conditions item retains the lifecycle premise with the
  paired prescriptions to avoid separating the reason from the rule.
- The two reasons given for persistent models were condensed into one resilience
  statement.
- The Modern app architecture technique list and repository responsibility list
  were each condensed without extending their scope.
- Closely related engineering-team benefits were condensed into one item; the
  separately stated user impact remains a separate item.
- General best-practice lead-ins are visible labels rather than nested headings
  in the extracted document structure, so locators use `General best practices`
  as the heading and preserve each lead-in in `details`.

## Known ambiguities

The publication uses recommendation language alongside one explicit dependency
injection key point. The extraction preserves that distinction but does not
assign enforcement levels. The source uses “persistent models” without choosing
one storage technology, so the items do not infer one. Examples such as
ViewModel, Jetpack Compose, and Hilt are retained only where the in-scope page
uses them to state the guidance; their linked documentation was not consulted
for item meaning.

## Repository-safety declaration

The package is `citation-only`. It contains short faithful transcriptions,
metadata, and locators, not a full-text reproduction. Licensing permission and
final repository-use approval remain the human reviewer's responsibility.

No raw source artifact or `raw/` directory exists. No normalization,
deduplication, prerequisite design, topic mapping, learning sequence, difficulty,
mastery, or learner-progress work was performed.
