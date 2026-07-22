# Competency-to-Topic Mapping Authoring

## Before authoring

Read the [mapping model](COMPETENCY_TOPIC_MAPPING_MODEL.md), the
[canonical competency model](architecture/CANONICAL_COMPETENCY_MODEL.md), and
the [content model](CONTENT_MODEL.md). A production mapping requires real,
reviewed topic packages; none exist yet, so production authoring remains
deferred.

When production topics exist, inspect the complete canonical competency set
and topic content rather than matching titles alone.

## Select exact references

1. Choose one canonical competency set and copy its exact `id` and current
   positive `version` from `competency-set.yaml`.
2. Copy each `competency_id` from that set's `competencies.yaml`. Do not derive
   IDs from titles or outcomes.
3. Select a topic by its stable `topic.yaml` `id` and copy its exact positive
   `content_version`.
4. Confirm that the topic intentionally teaches the capability expressed by
   the complete competency outcome.

Mappings do not change competency or topic identity. A mapping package must be
reviewed when either referenced version changes.

## Choose coverage

Use `primary` when the competency is one of the topic's intentional primary
educational goals. The topic should devote enough authored material to teaching
the capability rather than mentioning it incidentally.

Use `partial` when the topic intentionally teaches a bounded part of the
competency but does not claim the complete capability. Add a concise
`rationale` when reviewers need the boundary stated explicitly.

Do not add a mapping for incidental terminology, inferred relevance, or title
similarity. Coverage is not a score or estimate. A topic test is not
automatically an assessment of the mapped competency, and a mapping does not
prove learner mastery.

## Review relationship boundaries

- A competency may map to several topics when each intentionally teaches it.
- A topic may map to several competencies when it intentionally teaches each
  distinct capability.
- Keep one entry per competency in a package and one reference per topic within
  that entry.
- Do not use mappings to express topic prerequisites, canonical competency
  relations, or learning-sequence ordering.
- Do not treat mapping status as publication approval for a competency or
  topic.

Mappings are independent from learning sequences. A sequence may recommend
when to study a competency; a mapping only identifies authored content that
teaches it.

## Version and review

Start a new package at `mapping_version: 1`. Increment the version for adding
or removing a relationship, changing coverage, changing either referenced
version, or materially changing a rationale so that the mapping decision
changes. Formatting and typo-only edits retain the current version.

Keep a new or revised mapping in `review` until human approval. Do not change
the versions or editorial states of referenced packages as part of mapping
authoring.

## Validate

Run from the repository root:

```bash
python -B scripts/validate_competencies.py
python -B scripts/validate_content.py
python -B -m unittest discover
git diff --check
```

Schema and reference integrity do not replace editorial review of whether the
topic intentionally teaches the competency or whether `primary` versus
`partial` is accurate.
