# Architecture Study 001 — Canonical Competency Relations

Status: DEFERRED

## Decision summary

Canonical competency relations were researched against the
`android-app-architecture` canonical competency set version 2 and are deferred.
The current evidence does not justify a production relation model.

The supporting analysis is recorded in:

- `001-canonical-competency-relations-phase-2a-semantic-profiling.md`;
- `001-canonical-competency-relations-phase-2b-iteration-1.md`.

## Findings

The current canonical competencies remain independently assessable. Several
pairs are useful to teach in a particular order, but that instructional value
does not establish semantic necessity, containment, or a universal dependency.
Shared terminology and domain-object proximity also do not establish a
relation between complete demonstrable capabilities.

The research found a narrow provisional meaning for `supports` in two
lifecycle-driven cases, but did not establish a sufficiently complete and
stable relation vocabulary for repository data. In particular, relations such
as `requires`, `recommended-before`, `specializes`, and generic `related` are
not approved for implementation.

## Decision

Do not add canonical relation records or a prerequisite graph. Preserve
canonical competency identity as:

```text
stable capability
+
canonical wording
+
traceable evidence
```

Represent contextual teaching order in a separate learning-sequence model.
Revisit canonical relations only with additional evidence, a concrete consumer,
and an independently approved architecture task.
