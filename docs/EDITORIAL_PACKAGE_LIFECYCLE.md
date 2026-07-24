# Editorial Package Lifecycle

## Purpose

This policy defines one repository-wide editorial lifecycle for exact,
versioned knowledge and learning packages. It applies to source packages,
canonical competency packages, learning-sequence packages,
competency-to-topic mapping packages, and educational topic packages.

The lifecycle is a human review policy. Existing schemas use different status
vocabularies, so the conceptual state and the value stored in package metadata
are not always spelled the same way. This task does not change schemas,
validators, or existing package statuses.

## Independent status dimensions

```text
Architecture status:
Is this model or decision the repository's approved design?

Package editorial status:
Has this exact package version passed content review?

Task status:
Was the implementation task completed?

Publication artifact status:
Was a derived output generated and released?
```

One status does not imply another:

- Task `DONE` does not accept or publish a package created by that task.
- Architecture `ACCEPTED` does not accept a package that conforms to the
  architecture.
- Package acceptance does not mean that a learner-facing release exists.
- Releasing a generated derivative does not make that derivative canonical
  knowledge.

## Conceptual package states

### `draft`

The package is incomplete or actively being authored. References may be
unstable, validation may fail, and the package is not ready for formal review
or production dependency use.

### `review`

The package is structurally complete enough for formal review and its required
automated validation passes. Its content may still change materially. It is not
approved for stable downstream reliance; any reference to it must acknowledge
review-stage risk.

### `accepted`

The exact package version has passed editorial and technical review. Required
evidence and references have been checked, and its scope and semantics are
stable enough for downstream use. Acceptance is not public release.

Acceptance belongs to one exact version, not permanently to a package ID.
Version N may remain accepted or published while version N+1 is in `review`.
A new review version does not automatically invalidate the accepted version.

### `published`

An accepted exact version has been approved for learner-facing or external
distribution. Release metadata, visibility, and distribution requirements are
satisfied, and every publication artifact remains traceable to that accepted
version. Generated outputs remain derivatives rather than canonical knowledge.

### `deprecated`

The version remains historically addressable, but new downstream work should
not target it. Replacement or migration guidance should be recorded when
available. Deprecation does not erase provenance, earlier references, or
historical learner records.

### `superseded`

A newer version is the preferred continuation. The older version remains
immutable and traceable, and existing exact-version references remain
historically valid unless they are explicitly migrated.

`superseded` is not currently a schema-supported metadata value. It may be
recorded in a review or migration report until a future approved schema policy
provides a machine-readable representation.

## Current machine support

The lifecycle terms above are repository policy; package metadata must continue
to use only the enum defined by its current schema.

| Package type | Schema-supported `status` values | Lifecycle mapping and gaps |
|---|---|---|
| Source package | `draft`, `review`, `approved`, `deprecated` | `approved` represents conceptual `accepted`; `published` and `superseded` are not supported. |
| Canonical competency package | `draft`, `review`, `approved`, `deprecated` | `approved` represents conceptual `accepted`; `published` and `superseded` are not supported. |
| Learning-sequence package | `draft`, `review`, `approved`, `deprecated` | `approved` represents conceptual `accepted`; `published` and `superseded` are not supported. |
| Competency-to-topic mapping package | `draft`, `review`, `approved`, `deprecated` | `approved` represents conceptual `accepted`; `published` and `superseded` are not supported. |
| Educational topic package | `draft`, `review`, `published`, `deprecated` | No distinct machine-supported `accepted`/`approved` state exists; `superseded` is not supported. |

All five schemas support `draft`, `review`, and `deprecated`. No schema supports
`superseded`. Only the topic schema supports `published`. Four
competency-related schemas support `approved`, not the literal value
`accepted`.

For a topic, editorial acceptance must be recorded in a review report until a
future approved schema change provides a distinct metadata state. The topic
must remain on a schema-supported status, and a transition to `published` must
satisfy both acceptance and publication criteria. For other domains,
publication is a separate release decision recorded outside package metadata.
This policy does not authorize adding unsupported values.

## General promotion rules

### Exact versions and changes

Acceptance applies to an exact package version. Accepted or published versions
must not be silently rewritten. A material correction should use an approach
approved for the affected domain, such as a new version, correction release,
explicit return to review, and a migration note. This policy does not define a
full release system.

### Dependencies

A downstream package may be authored against a `review` dependency if that risk
is explicit. An accepted package should normally depend only on accepted exact
versions of canonical dependencies. An exception requires documented
rationale and human approval. Published learner-facing material must not
depend on unresolved review-stage canonical packages.

### Promotion authority

The human repository owner makes the final promotion decision and remains
accountable for it. Automated validation and AI review are evidence, not
authority.

- ChatGPT may review, identify inconsistencies, and recommend approval or
  changes.
- Codex may implement an approved status change, run checks, and prepare
  reports.
- Codex must not independently promote a package.

### Promotion record

A promotion record should identify:

- package ID and exact version;
- old and new conceptual and metadata statuses;
- reviewer and final approver;
- validation results and the review report;
- known limitations;
- replacement or migration notes when relevant;
- decision date if repository conventions later support it.

Promotion records may initially live in repository reports or dedicated review
documents. This policy does not add mandatory date fields to package metadata.

## Domain promotion criteria

### Source packages

Before `review` → `accepted` (stored as `approved`):

- the source and represented version are identifiable;
- provenance is stable and locators are valid;
- extraction, permitted paraphrase, or summary is faithful;
- declared scope has a documented completeness review;
- no claims were invented;
- repository-usage and raw-artifact constraints are satisfied;
- `python -B scripts/validate_competencies.py` passes;
- an extraction review record exists;
- the human owner approves the exact source package version.

Accepted source packages normally remain internal evidence artifacts. External
publication is optional and requires a separate distribution, rights, and
traceability decision; acceptance does not require publication.

See [Competency Source Model](COMPETENCY_SOURCE_MODEL.md) and
[Competency Import Workflow](COMPETENCY_IMPORT_WORKFLOW.md).

### Canonical competency packages

Before `review` → `accepted` (stored as `approved`):

- every competency has valid evidence;
- identifiers are stable and wording is source-independent;
- duplicates and near-duplicates have been reviewed;
- merge and split decisions are explained;
- scope and granularity are coherent;
- cross-source normalization has been reviewed;
- `python -B scripts/validate_competencies.py` passes;
- the human owner explicitly approves the exact package version.

Acceptance of the
[canonical competency model](architecture/CANONICAL_COMPETENCY_MODEL.md) as
architecture does not accept any canonical competency package.

See [Competency Normalization Workflow](COMPETENCY_NORMALIZATION_WORKFLOW.md).

### Learning-sequence packages

Before `review` → `accepted` (stored as `approved`):

- the sequence references one exact canonical competency-set version;
- every referenced competency exists;
- stage order has a clear pedagogical rationale;
- stage order is not presented as canonical competency relations;
- target audience and outcome are coherent;
- omissions and scope are documented;
- `python -B scripts/validate_competencies.py` passes;
- the exact sequence version receives editorial approval.

Before an accepted sequence is `published`, it must be learner-facing ready and
have an approved presentation and distribution context. Publication is not
currently represented by the sequence schema.

See [Learning Sequence Model](LEARNING_SEQUENCE_MODEL.md) and
[Learning Sequence Authoring](LEARNING_SEQUENCE_AUTHORING.md).

### Competency-to-topic mapping packages

Before `review` → `accepted` (stored as `approved`):

- the exact canonical competency-set version is pinned;
- exact topic content versions are pinned;
- all many-to-many references are valid;
- mapping rationale and coverage have been audited;
- no learning-sequence, prerequisite, or canonical-relation semantics are
  imported into the mapping;
- both competency and content validators pass;
- the human owner approves the exact mapping version.

No production competency-to-topic mapping package currently exists.

See [Competency-to-Topic Mapping Model](COMPETENCY_TOPIC_MAPPING_MODEL.md) and
[Mapping Authoring](COMPETENCY_TOPIC_MAPPING_AUTHORING.md).

### Educational topic packages

Before `review` → conceptual `accepted`:

- metadata and exact prerequisite references are valid;
- learning outcomes, theory, cheat sheet, practice, interview material,
  assessment, and references are complete;
- all six canonical files are mutually consistent;
- technical accuracy and editorial clarity have been reviewed;
- `python -B scripts/validate_content.py` passes;
- no blocking review comments remain;
- the human owner approves the exact `content_version`.

Because the topic schema has no distinct accepted value, approval is recorded
in a review report and does not itself authorize `status: published`.

Before conceptual `accepted` → `published`:

- learner-facing formatting is ready;
- the release uses the approved exact content version;
- internal links are valid;
- sources and references have been audited;
- freshness has been reviewed;
- a distribution context is approved;
- the human owner approves the `published` status change.

See [Educational Content Model](CONTENT_MODEL.md) and
[Content Validation](CONTENT_VALIDATION.md).

## Published derivatives

Catalog entries, versioned bundles, web pages, Telegram posts, slides, audio,
AI answers, NotebookLM outputs, and other generated presentations have a
separate release lifecycle. They must identify the exact canonical package or
topic versions from which they were derived. Releasing them does not promote
their inputs and does not make generated material canonical knowledge.

## Correction and rollback

If an accepted or published package is later found to be incorrect:

1. record the defect, affected exact version, impact, and known downstream use;
2. prevent new reliance by deprecating the affected version when appropriate;
3. produce and review a corrected version or correction release;
4. update affected mappings and publication artifacts explicitly;
5. record replacement or migration guidance;
6. preserve provenance and historical traceability.

Do not silently delete evidence, rewrite accepted history, or treat generated
artifacts as the correction source.
