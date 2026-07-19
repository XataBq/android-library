# ADR 0002: Use YAML content metadata with JSON Schema validation

- Status: Accepted
- Date: 2026-07-19

## Context

Educational topics need machine-readable metadata and assessments that remain comfortable to author and review in Git. Future clients need stable contracts without coupling shared content to application models, database entities, or filesystem layout. Personal learning activity has different ownership and update patterns from shared educational content.

## Decision

Author topic metadata and tests in YAML, keep explanatory material in Markdown, and validate YAML data against JSON Schema Draft 2020-12.

Use stable lowercase kebab-case topic IDs that are globally unique and independent from directory paths. Use stable lowercase kebab-case question IDs that are unique within their topic. IDs are not reused after removal.

Keep learner progress, attempts, scores, mastery, review schedules, bookmarks, and personal notes outside the content model.

## Rationale

YAML is readable in source control, supports concise authored structures, and fits the existing Git-centered content workflow. JSON Schema provides a standardized, implementation-independent way to describe required fields, controlled values, types, and question variants. Draft 2020-12 supports reusable definitions and explicit composition while remaining usable by future tooling and clients.

Path-independent IDs allow packages to move as the catalog evolves without breaking future progress references. Excluding learner state preserves the boundary established by ADR 0001 and avoids noisy, user-specific content commits.

## Consequences

### Positive

- authors can read and review metadata without an application;
- schemas provide an explicit contract for tooling and clients;
- controlled objects reject accidental or speculative fields;
- content remains portable across repository reorganizations;
- shared educational content remains separate from personal state.

### Negative

- YAML scalar interpretation requires care, such as quoting date strings;
- schema and templates must evolve together;
- changing a published contract requires deliberate compatibility review;
- validators must enable format checking to enforce URI and date formats.

## Known limitations

JSON Schema validates one document at a time and does not establish repository-wide uniqueness, reference existence, dependency cycles, or consistency between topic and test files. It also does not cleanly verify that answer-key IDs name options in the same question or that option IDs are unique by their `id` property. A later repository validator will enforce those relationships.

## Alternatives considered

### JSON for authoring

Rejected because its stricter punctuation makes routine hand-authoring and review noisier without improving the content boundary.

### A custom YAML validator or dialect

Rejected because a project-specific format would increase maintenance and reduce interoperability.

### Database-backed content metadata

Rejected for this phase because it would reduce portability, couple content to infrastructure, and conflict with the approved Git source-of-truth model.
