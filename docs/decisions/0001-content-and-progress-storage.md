# ADR 0001: Separate educational content from personal progress

- Status: Accepted
- Date: 2026-07-18

## Context

The platform must provide reusable educational content while also tracking learner-specific progress, attempts, scores, weak areas, and review dates.

Educational content benefits from:

- version control;
- diff-based review;
- Markdown readability;
- portability;
- static validation;
- use outside a specific application.

Personal progress changes frequently and is specific to a user.

## Decision

Store shared educational content and its metadata in the Git repository using Markdown and structured YAML or JSON.

Store personal learning state separately:

1. local storage for the earliest web MVP;
2. a database when persistent synchronization is introduced;
3. a local Android database with synchronization for offline-first support.

Clients refer to topics through stable topic identifiers.

## Consequences

### Positive

- content remains portable and reviewable;
- Git history tracks educational changes;
- Obsidian and GitHub can read the content directly;
- web and Android clients share the same content model;
- personal activity does not create noisy content commits.

### Negative

- synchronization between content versions and progress must be designed;
- topic identifiers must remain stable;
- content publishing requires validation and indexing.

## Alternatives considered

### Store everything in Markdown

Rejected because frequent personal progress updates do not fit a shared public Git workflow.

### Store everything in a database

Rejected for the initial architecture because it reduces content portability and makes educational review less transparent.
