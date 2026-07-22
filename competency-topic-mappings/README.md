# Competency-to-topic mappings

This directory is the repository domain for versioned relationships between
canonical competencies and authored educational topics. A future production
package will use:

```text
competency-topic-mappings/<mapping-id>/
в””в”Ђв”Ђ mapping.yaml
```

The relationship is owned by the mapping package, not by either referenced
domain. Mapping packages do not change canonical competency identity, topic
identity, topic prerequisites, or learning-sequence order.

No production mapping packages exist yet because no production educational
topics have been authored. Current examples are schema fixtures under
`schemas/fixtures/competency-topic-mappings/` only.

Read the [mapping model](../docs/COMPETENCY_TOPIC_MAPPING_MODEL.md) and
[authoring guide](../docs/COMPETENCY_TOPIC_MAPPING_AUTHORING.md) before adding a
future package. Validate changes with:

```bash
python -B scripts/validate_competencies.py
python -B scripts/validate_content.py
python -B -m unittest discover
```
