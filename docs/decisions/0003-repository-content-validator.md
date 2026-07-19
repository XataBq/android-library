# ADR 0003: Use a repository-local content validator

- Status: Accepted
- Date: 2026-07-19

## Context

JSON Schema validates individual topic and test documents but cannot enforce repository-wide identity, relationship, path, scoring, and dependency rules. These rules must be checked before content is consumed by future clients, without coupling validation to an application or database.

## Decision

Provide a repository-local Python command that discovers canonical topic packages, validates YAML against the Draft 2020-12 schemas, and then performs separate semantic validation across files and topics.

Use Python initially because Python 3.12, PyYAML, and `jsonschema` are already available for this repository. Keep schema validation and semantic validation as explicit phases: schemas remain portable document contracts, while Python implements comparisons, repository lookups, and graph checks.

Run validation independently from web, Android, backend, and database clients. Diagnostics use deterministic ordering, stable codes, and process exit codes suitable for local author workflows and later automation.

## Consequences

### Positive

- authors can validate the Git source of truth without running a product client;
- structural and semantic failures remain distinguishable;
- repository-wide references and cycles are checked consistently;
- deterministic output is usable by humans and automation;
- validation adds no new dependency or package manager.

### Negative

- the validator must evolve deliberately with schema and package contracts;
- Python plus the two already-required libraries must be available locally;
- some content-quality and historical identity rules remain outside its scope.

## Alternatives considered

### Encode all rules in JSON Schema

Rejected because cross-file uniqueness, reference existence, path comparison, rubric totals, and graph cycles are outside a portable single-document schema contract.

### Validate inside a product client

Rejected because it would duplicate logic, delay feedback, and couple shared content quality to application implementation.

### Add a validation framework or package manager

Rejected because the standard library, PyYAML, and `jsonschema` are sufficient for the approved scope.

### Auto-fix invalid content

Rejected because validation must report authoring errors without silently changing educational content or stable identities.

## Known limitations

The initial validator does not maintain removed IDs, validate Markdown structure or links, check remote URLs, assess prose or answers, or enforce global question-ID uniqueness. Those concerns require separately approved work.
