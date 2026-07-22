# Competency Source Model

## Purpose and boundary

The competency source model records what an external or owner-created source says before the platform interprets it. A source item is evidence for later analysis; it is not a canonical competency, educational topic, prerequisite, learning-sequence entry, or learner-progress record.

This boundary preserves duplicate, overlapping, ambiguous, and source-specific statements until a separately reviewed normalization process can resolve them.

## Source package

A future source package uses:

```text
competencies/sources/<source-id>/
├── source.yaml
├── items.yaml
└── raw/                 Optional permitted artifacts
```

`source.yaml` records identity, provenance, repository safety, source version, and optional source-declared scope. `items.yaml` contains faithful extracted statements and precise locators. `raw/` is optional and must contain only declared artifacts that may legally be stored.

Templates are under `templates/competency-source/`. Canonical competency sets
are stored under `competencies/normalized/`, and import and normalization review
records are stored under `competencies/reports/`. These separate areas do not
change or own source packages.

## Source metadata

Every `source.yaml` requires:

| Field | Meaning |
|---|---|
| `id` | Globally unique, stable lowercase kebab-case source ID. |
| `title` | Human-readable source title. |
| `source_type` | Controlled description of the source kind. |
| `language` | Practical BCP 47-style source language tag. |
| `source_version` | Positive repository version of represented source material. |
| `status` | Extraction review state: `draft`, `review`, `approved`, or `deprecated`. |
| `repository_usage` | Declared basis for representation in the public repository. |
| `provenance` | Citation and optional source-identification details. |

`source_type` is one of `competency-matrix`, `curriculum`, `assessment-framework`, `role-expectations`, `job-description`, `roadmap`, `personal-analysis`, `standard`, or `other`.

Optional `scope` arrays preserve source wording for roles, declared levels, platforms, and technologies. An empty array means the source does not declare that dimension; these values do not define platform taxonomy.

## Source items and locators

Every `items.yaml` declares the matching `source_id`, matching `source_version`, and at least one item. Each item requires:

- `id`: stable lowercase kebab-case ID unique within the source;
- `statement`: the original statement or a faithful transcription;
- `locator`: a location with `type` and human-readable `value`.

Locator types are `page`, `section`, `heading`, `row`, `cell`, `item`, `timestamp`, and `other`. Optional `details` can add precision.

Optional item fields are:

- `context`: unique source hierarchy labels;
- `declared_level`: the source's own level wording;
- `transcription_notes`: formatting loss, ambiguity, OCR uncertainty, translation handling, or other extraction caveats.

Do not normalize terminology, combine statements, resolve duplicates, or record platform decisions in these fields. When verbatim storage is not legally or practically appropriate, use only a permitted faithful transcription, short excerpt, or owner-authored summary consistent with `repository_usage`, and explain unavoidable extraction issues in `transcription_notes`.

## Stable identifiers and versions

Source IDs remain stable and globally unique. Item IDs remain stable after review, are unique within one source, do not encode mutable array positions, and are not reused after removal.

The stable future cross-source reference form is:

```text
<source-id>:<item-id>
```

For example, `example-source-2026:activity-lifecycle` identifies one source-local item without making it canonical.

Start `source_version` at `1`. Increment it when represented source material changes or an updated source changes extracted meaning. Formatting-only repository edits do not require an increment. `source.yaml` and `items.yaml` must use the same version. This version is independent from educational `content_version`.

## Provenance and public-repository safety

Provenance always requires a concise `citation`. It may also record publisher, absolute HTTP or HTTPS URL, publication and retrieval dates, the source's own `version_label`, and notes.

Every source declares one repository-usage value:

- `public`: publicly accessible material that may be represented under applicable terms;
- `owned`: material created and owned by the repository owner;
- `permission-granted`: storage or transcription permission was obtained;
- `citation-only`: only metadata, locators, short permitted excerpts, or owner-authored summaries may be committed.

`citation-only` packages cannot declare or contain committed raw artifacts. Never commit confidential employer material, proprietary or access-controlled exports, personal data, secrets, or copyrighted full text without permission. Schema validation confirms the declaration, not legal permission; the human reviewer remains responsible.

## Raw artifacts

Optional artifact entries require a package-relative `raw/...` path, MIME media type, and exactly 64 lowercase hexadecimal SHA-256 characters. An optional description may explain the file.

Semantic validation requires every declared artifact to stay inside that package's `raw/` directory, exist as a regular file, and match its checksum. Artifact paths must be unique. Every regular file under `raw/` must be declared. The validator does not download sources or check remote URLs.

## Validation boundaries

JSON Schema Draft 2020-12 checks document structure, required fields, strings, identifier and language-tag shapes, enums, dates, HTTP/HTTPS URLs, artifact metadata, and controlled objects.

Run repository validation with:

```bash
python -B scripts/validate_competencies.py
```

Semantic validation checks package/file identity, matching source versions, global source-ID uniqueness, source-local item-ID uniqueness, artifact paths, existence, regular-file type, checksums, undeclared raw files, and the `citation-only` restriction. It also verifies templates and valid/invalid fixture expectations with deterministic diagnostics.

Normalization is a separate editorial workflow. The validator checks canonical
package structure and evidence-reference integrity, but it does not infer
cross-source duplicates, create canonical competencies, decide equivalence or
merges, define prerequisite or related-competency edges, map items to topics,
create learning sequences, or modify files.

## Author workflow

1. Verify that the source is safe to represent publicly.
2. Copy `templates/competency-source/` to `competencies/sources/<source-id>/`.
3. Record accurate provenance and repository usage in `source.yaml`.
4. Extract source statements faithfully without normalization.
5. Add a precise locator to every item.
6. Add raw artifacts only when storage is permitted and declare their SHA-256 values.
7. Run `python -B scripts/validate_competencies.py`.
8. Submit the extraction for human review.
9. Do not change source status to `approved` until human review is complete.
