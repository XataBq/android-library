# Learning Sequence Model

## Purpose

A learning sequence is a versioned, repository-authored pedagogical path
through canonical competencies. It provides a reviewable default order without
changing competency identity or asserting semantic dependencies.

Learning sequences are shared educational data in Git. They do not contain
learner progress, mastery, completion, or adaptive-routing state.

## Package structure

```text
learning-sequences/<sequence-id>/
├── sequence.yaml
└── README.md
```

`sequence.yaml` conforms to
[`schemas/learning-sequence.schema.json`](../schemas/learning-sequence.schema.json).
The directory name must equal `sequence_id`.

## Stage semantics

A sequence contains an ordered list of stages. Competencies in an earlier stage
are recommended to be learned before competencies in a later stage within that
specific sequence.

This order is pedagogical and contextual. It is not a prerequisite, a mandatory
dependency, a canonical competency relation, or a claim that a later
competency cannot be assessed independently. Competencies within one stage are
not ordered.

Canonical competency relations remain deferred. Version 1 has no edges,
branching, weights, difficulty, or routing rules. Alternative routes are
separate sequence packages rather than branches.

## Identity and references

A sequence has a stable `sequence_id` and positive integer
`sequence_version`. It references one canonical competency set by exact ID and
version. Every stage entry uses an existing competency ID from that version;
titles are never used to reconstruct references.

A sequence version must change when stage order or membership changes. Purely
editorial clarification that does not change interpretation may retain the
version, subject to review.

## Validation

JSON Schema Draft 2020-12 enforces the closed version 1 shape, required fields,
non-empty text, stable identifier syntax, allowed editorial statuses, positive
versions, non-empty stages and competency lists, and unique competencies within
a stage.

Repository validation additionally checks:

- package-directory and sequence-ID consistency;
- unique sequence ID/version pairs;
- unique stage IDs;
- no repeated competency within or across stages;
- canonical competency-set existence and exact version match;
- existence of every referenced canonical competency;
- deterministic diagnostics.

Run:

```bash
python -B scripts/validate_competencies.py
```

The validator checks reference integrity, not whether an authored order is the
best pedagogy.

## Deliberate non-goals

Version 1 does not model:

- canonical competency relations or prerequisites;
- a general DAG or explicit graph edges;
- branching or conditional routes;
- weights, priority, difficulty, or estimated time;
- learner progress, mastery, or adaptation;
- assessments or exercises;
- topic mappings.

Topics are not sequence nodes yet. Future authored educational topics may map
to competencies without becoming part of sequence identity.
