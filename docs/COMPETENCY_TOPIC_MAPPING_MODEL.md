# Competency-to-Topic Mapping Model

## Purpose and ownership

A competency-to-topic mapping is a versioned repository-owned declaration that
an educational topic intentionally teaches knowledge or skills required to
demonstrate a canonical competency. The mapping package owns this relationship.
Canonical competency records, topic packages, and learning sequences do not.

This separate ownership preserves three identities:

- a canonical competency remains a stable demonstrable capability;
- a topic remains an authored educational content package;
- a learning sequence remains a contextual pedagogical order through
  competencies.

Adding or changing a mapping does not change a competency's identity or either
referenced package's version.

## Package structure

Future production packages use:

```text
competency-topic-mappings/<mapping-id>/
в””в”Ђв”Ђ mapping.yaml
```

`mapping.yaml` conforms to
[`schemas/competency-topic-mapping.schema.json`](../schemas/competency-topic-mapping.schema.json).
The initial contract uses `schema_version: 1`, a stable kebab-case `mapping_id`,
a positive `mapping_version`, one exact canonical competency-set reference, and
a non-empty list of competency-to-topic relationships.

There are no production mapping packages yet. Schema fixtures are validation
data and are not educational topics or production mappings.

## Cardinality and reference identity

The relationship is many-to-many:

- one competency entry can reference several topics;
- the same topic can appear under several distinct competencies;
- each mapping package references one exact canonical competency set and
  version;
- every topic reference pins the stable topic ID and exact `content_version`.

Filesystem paths do not replace stable IDs. The repository validator resolves
the recorded IDs and versions against the canonical competency and topic
registries.

## Mapping meaning

A relationship means that the topic intentionally teaches knowledge or skills
needed to demonstrate the competency. It does not mean that:

- a learner has mastered or completed the competency;
- the topic's test is automatically a competency assessment;
- either entity is a prerequisite for another;
- the relationship changes learning-sequence order;
- either referenced package is approved or published;
- the topic completely covers or assesses the competency beyond the declared
  `primary` or `partial` editorial distinction.

Mappings are independent from learning sequences. Sequence stages describe an
authored pedagogical route; mappings describe which content intentionally
teaches a capability. Neither model creates canonical competency relations.

## Coverage

Schema version 1 supports exactly two values:

- `primary`: the topic intentionally teaches the competency as one of its
  primary educational goals;
- `partial`: the topic intentionally teaches only part of the competency.

Coverage is an editorial classification, not a percentage, weight, score,
confidence value, or inference. `partial` should be accompanied by a concise
`rationale` when the limited boundary is not obvious.

## Versioning and status

New packages start with `mapping_version: 1`. Increment the version when a
semantic mapping decision changes, including:

- adding or removing a competency/topic relationship;
- changing `coverage`;
- changing the referenced competency-set version;
- changing a referenced topic `content_version`;
- materially changing a rationale in a way that changes the mapping decision.

Formatting-only changes and typo fixes do not require an increment. Mapping
versioning does not modify canonical competency-set, source-package, topic
content, or learning-sequence versions.

`status` uses the repository editorial vocabulary: `draft`, `review`,
`approved`, or `deprecated`. It describes the mapping package only and does not
approve referenced competencies or topics.

## Validation

JSON Schema Draft 2020-12 enforces the closed version 1 shape, required fields,
stable identifier patterns, positive versions, language and status values,
non-empty mappings and topic lists, the two coverage values, and rejection of
unsupported fields.

Repository semantic validation additionally checks:

- canonical competency-set existence and exact version;
- canonical competency existence in that set;
- topic existence and exact content version;
- duplicate competency entries;
- duplicate topic references within one competency entry;
- duplicate competency/topic pairs across the package;
- duplicate mapping ID/version identities across packages;
- controlled handling of malformed YAML and non-mapping roots;
- deterministic diagnostics.

Run `python -B scripts/validate_competencies.py`. Topic packages remain subject
to `python -B scripts/validate_content.py` independently.

## Deliberate non-goals

Version 1 does not define production mappings, production topics, competency
relations, prerequisites, learning order, assessment mappings, learner
progress, mastery, generated catalogs, inferred coverage, or application
runtime behavior. It contains no ordering, graph, percentage, weight, score,
confidence, or learner-state fields.
