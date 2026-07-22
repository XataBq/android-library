# Task 011 вЂ” Minimal Competency-to-Topic Mapping Model implementation report

## Final result

**PASS**

Task 011 implements Variant A as a separate repository domain: one closed
version 1 mapping schema, repository semantic validation, fixture-only example
data, tests, model and authoring documentation, and project-state
synchronization. No production topic or mapping package was created.

## Files

Added:

- `schemas/competency-topic-mapping.schema.json`;
- `schemas/fixtures/competency-topic-mappings/valid/minimal.yaml`;
- `schemas/fixtures/competency-topic-mappings/valid/many-to-many.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/missing-required-field.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/unsupported-schema-version.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/invalid-coverage.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/unexpected-property.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/malformed-root.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/duplicate-competency-entry.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/duplicate-topic-reference.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/duplicate-competency-topic-pair.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/unknown-competency-set.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/wrong-competency-set-version.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/unknown-competency.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/unknown-topic.yaml`;
- `schemas/fixtures/competency-topic-mappings/invalid/wrong-topic-content-version.yaml`;
- `tests/competency_topic_mapping_validator/__init__.py`;
- `tests/competency_topic_mapping_validator/test_validate_competency_topic_mappings.py`;
- `competency-topic-mappings/README.md`;
- this implementation report;
- `docs/COMPETENCY_TOPIC_MAPPING_MODEL.md`;
- `docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md`.

Included unchanged from the supplied task input:

- `tasks/011-minimal-competency-topic-mapping-model.md`.

Modified:

- `scripts/validate_competencies.py`;
- `scripts/validate_content.py`;
- `README.md`;
- `docs/ARCHITECTURE.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

No file was removed.

## Schema decisions

The schema uses JSON Schema Draft 2020-12, `schema_version: 1`, and closed
objects at the package, competency-set reference, mapping-entry, and topic-
reference levels. Required package fields are `schema_version`, `mapping_id`,
`mapping_version`, `language`, `status`, `competency_set`, and `mappings`;
only `description` and `editorial_notes` are optional.

Identifiers follow the existing lowercase kebab-case convention. Language uses
the existing language-tag pattern. Mapping and referenced versions are positive
integers. Mapping status reuses `draft`, `review`, `approved`, and `deprecated`.
Both the mapping list and every topic-reference list are non-empty.

Each mapping entry contains only `competency_id` and `topics`. Each topic
reference requires `topic_id`, `content_version`, and `coverage`; only
`rationale` is optional. Coverage is exactly `primary` or `partial`. The schema
has no ordering, graph, prerequisite, score, weight, percentage, confidence,
assessment, or learner-state field.

Semantic duplicate rules remain in repository validation rather than schema
`uniqueItems`, because duplicate competency entries and competency/topic pairs
must be detected by stable IDs even when other fields differ.

## Semantic validation

The existing competency validator now discovers immediate package directories
under `competency-topic-mappings/`, excluding the documentation-only `reports/`
directory. Every package requires `mapping.yaml`.

Validation resolves:

- the exact canonical competency set ID and version through the existing
  canonical package index;
- every competency ID within that set;
- every topic ID and exact `content_version` through the content validator's
  shared deterministic topic-package discovery function.

It rejects duplicate competency entries, duplicate topic IDs within one
competency entry, duplicate competency/topic pairs, and duplicate mapping
ID/version identities across packages. YAML parsing, schema validation, and
semantic checks remain separate. List and scalar YAML roots receive ordinary
schema diagnostics and cannot crash semantic validation. Diagnostics use the
existing immutable record and sorted, deduplicated rendering.

## Fixtures and tests

Valid fixtures cover a minimal package and a many-to-many package with multiple
competencies, multiple topic references, both coverage values, rationales, and
optional package text.

Invalid fixtures cover a missing required field, unsupported schema version,
invalid coverage, unexpected property, non-mapping YAML root, duplicate
competency entry, duplicate topic reference, duplicate competency/topic pair,
unknown competency set, wrong set version, unknown competency, unknown topic,
and wrong topic content version.

Nineteen focused tests cover Draft 2020-12 meta-validation, valid and invalid
fixtures, every semantic rule, duplicate mapping identity, a missing mapping
file, malformed YAML syntax, list and scalar root regressions, deterministic
diagnostics, and successful repository validation with zero production mapping
packages. The full repository suite contains 105 tests.

## Documentation synchronization

The mapping model defines relationship ownership, many-to-many cardinality,
coverage semantics, exact reference versioning, status, validation, and
non-goals. The authoring guide explains reference selection, `primary` versus
`partial`, version increments, review boundaries, and validation commands.

README, architecture, project state, and roadmap now distinguish implemented
mapping infrastructure from future production topics and mappings. They also
keep mappings independent from canonical identity, learning-sequence order,
topic prerequisites, assessments, and learner state.

## Deferred work

Production educational topics, production mapping packages, mapping editorial
approval, canonical competency relations, assessment mappings, generated
catalogs, learner progress, and client/runtime behavior remain deferred.

## Validation commands and results

Baseline before implementation:

```text
python -B scripts/validate_competencies.py
PASS вЂ” 2 source packages, 1 canonical package, 1 learning-sequence package,
2 templates, 26 schema fixtures

python -B scripts/validate_content.py
PASS вЂ” 0 topic packages, 2 templates, 4 schema fixtures

python -B -m unittest discover
PASS вЂ” 86 tests

git diff --check
PASS
```

After implementation:

```text
python -B -m unittest tests.competency_topic_mapping_validator.test_validate_competency_topic_mappings
PASS вЂ” 19 tests

python -B scripts/validate_competencies.py
PASS вЂ” 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B scripts/validate_content.py
PASS вЂ” 0 topic packages, 2 templates, 4 schema fixtures

python -B -m unittest discover
PASS вЂ” 105 tests

git diff --check
PASS; Git emitted only Windows LF-to-CRLF working-copy warnings for the two
modified validator scripts

repository-local Markdown target check
PASS вЂ” every local link target in added or changed Markdown exists
```

The protected production source, canonical competency, learning-sequence, and
content paths have no diff. `content/` still contains only `.gitkeep`, and
`competency-topic-mappings/` contains documentation and this report rather than
a production package.

No `__pycache__` directory or `.pyc` file exists. The staged file list is empty,
and `HEAD` remains `539ef9c` (`docs(architecture): accept canonical competency
model`); no commit was created.

## Final Git status

```text
 M README.md
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 M scripts/validate_competencies.py
 M scripts/validate_content.py
?? competency-topic-mappings/
?? docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md
?? docs/COMPETENCY_TOPIC_MAPPING_MODEL.md
?? schemas/competency-topic-mapping.schema.json
?? schemas/fixtures/competency-topic-mappings/
?? tasks/011-minimal-competency-topic-mapping-model.md
?? tests/competency_topic_mapping_validator/
```

## Deviations and input reconciliation

No domain or scope deviation was required. The Task 011 file arrived as an
untracked repository input and was read completely; it remains unchanged with
its supplied `READY FOR IMPLEMENTATION` status because repository policy leaves
task status transitions to the human owner.

## Recommended commit message

```text
feat(mappings): add competency-to-topic mapping model
```
