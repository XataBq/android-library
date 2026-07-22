# Learning Sequence Authoring

## Before authoring

Read the [learning-sequence model](LEARNING_SEQUENCE_MODEL.md) and inspect the
complete canonical registry. Choose an existing competency set and record its
exact `id` and `version`. Copy competency IDs from its `competencies.yaml`; do
not derive IDs from titles.

## Define the path

Choose one audience and learning goal. Group competencies into a small ordered
set of coherent stages:

1. Put competencies together when they form one useful instructional unit and
   do not need a semantic order inside that unit.
2. Order stages by the recommended teaching progression for this particular
   audience and goal.
3. Keep every competency in at most one stage.
4. Do not encode prerequisites or canonical relations through stage wording.

Write each `rationale` to explain why the stage is placed there in this path.
Describe the pedagogical transition, not a universal dependency claim.

If audiences need materially different routes, author separate sequence
packages in version 1. Do not simulate branching with empty stages, conditions,
or undocumented fields.

## Version and review

Use a stable kebab-case `sequence_id` and start `sequence_version` at `1`.
Increment the version whenever stage order or competency membership changes.
Keep new or revised packages in `review` until a human reviewer approves them.

The package README should state its audience, goal, competency-set version,
ordering rationale, non-mandatory order semantics, lack of ordering inside a
stage, and editorial status.

## Validate

Run the repository validators and tests:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Review diagnostics in their sorted output order. Schema success does not replace
human review of the sequence's pedagogical rationale.

## Non-goals

Do not add prerequisites, relation types, graph edges, branching, weights,
difficulty, progress, adaptive routing, topic nodes, or topic mappings. Topics
remain separately authored content, and canonical relations remain deferred.
