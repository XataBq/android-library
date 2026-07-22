# CanonICAL COMPETENCY MODEL

Status: PROPOSED
Version: 1
Scope: Canonical Android competency domain model

## 1. Purpose

This document defines the canonical competency model used by the repository.

The repository imports claims from publications as immutable source items. Those source items are not themselves the final knowledge model. They are evidence used to derive canonical competencies that remain stable across publications, authors, wording styles, and source-package boundaries.

This document defines:

- the terminology of the competency domain;
- what is and is not a canonical competency;
- how evidence supports competencies;
- how source items may be combined or separated;
- how canonical wording is produced;
- how cross-source deduplication works;
- the minimum data model;
- architectural validation rules;
- explicit non-goals and future extensions.

This document does not define a learning path, assessment system, difficulty model, topic taxonomy, mastery model, or user-progress model.

## 2. Problem statement

Imported sources preserve how a publication expresses knowledge. A source package therefore reflects the publication's own structure, vocabulary, granularity, and emphasis.

A durable knowledge platform cannot treat every imported statement as a separate long-lived competency because:

1. Different sources can express the same underlying competency using different wording.
2. One source item can support more than one distinct competency.
3. Several closely related source items can jointly support one competency.
4. Section headings and publication structure are source-specific rather than canonical.
5. A competency must survive the removal, replacement, or addition of any individual source.
6. Future relations, assessments, learning paths, and progress records require stable canonical identifiers.
7. Without canonicalization, repeated imports will create duplicate or near-duplicate competencies.

The repository therefore separates:

```text
publication structure
        ↓
source items
        ↓
evidence links
        ↓
canonical competencies
```

## 3. Terminology

### 3.1 Source

A source is one identified publication imported into the repository as a versioned source package.

Examples:

- an Android Developers guide;
- a book chapter;
- a technical article;
- a conference talk;
- a specification.

A source preserves publication-level provenance.

### 3.2 Source item

A source item is the smallest imported meaning-bearing unit that the import process records from a source.

A source item preserves:

- the source's meaning;
- source-relative context;
- source-relative locator;
- source wording through a faithful transcription or paraphrase;
- source-package version.

A source item is not rewritten merely because the canonical model changes.

### 3.3 Evidence

Evidence is an explicit versioned link from a canonical competency to one or more source items that support that competency.

Evidence answers:

> Which imported source claims justify the existence and wording of this competency?

Evidence is not a claim that the linked source is infallible. It records traceability and support.

### 3.4 Canonical competency

A canonical competency is a stable, source-independent unit of knowledge or skill that a learner or practitioner can demonstrate.

A canonical competency:

- expresses one coherent capability;
- remains meaningful outside any particular publication;
- can be supported by one or many source items;
- can accumulate support from multiple independent sources;
- has a stable identifier;
- has canonical wording owned by the repository;
- is suitable for future linking to assessments, relations, learning paths, and progress records.

### 3.5 Normalization

Normalization is the editorial process that maps source items to canonical competencies.

Normalization may:

- map one source item to one competency;
- map several source items to one competency;
- map one source item to several competencies;
- attach new evidence to an existing competency;
- create a new competency when no equivalent competency exists.

Normalization never modifies the imported source package.

### 3.6 Canonical wording

Canonical wording is the repository-owned title and outcome of a competency.

Canonical wording summarizes the stable capability supported by evidence. It does not reproduce the structure or terminology of any one publication unless that terminology is itself essential.

## 4. What qualifies as a canonical competency

A candidate qualifies as a canonical competency when all of the following are true:

1. It expresses a demonstrable capability.
2. It contains one coherent primary idea.
3. It is meaningful without naming the publication that introduced it.
4. It can be written as an observable learning outcome.
5. Its scope is neither a broad subject area nor a trivial isolated phrase.
6. Its existence is supported by at least one imported source item.
7. Its meaning can remain stable as further evidence is added.
8. It can be distinguished from neighboring competencies by a reviewer.

### 4.1 Examples

| Candidate | Competency? | Reason |
|---|---:|---|
| Repository | No | A concept label, not a demonstrable capability |
| Android app architecture | No | A broad domain |
| Recommended app architecture | No | A source section |
| Explain the responsibilities of a repository | Yes | Demonstrable and scoped |
| Explain why Android framework components should not own application data | Yes | One coherent explanatory capability |
| Use best practices | No | Vague and not independently reviewable |
| Design a data layer that exposes application data through repositories | Yes | Demonstrable design capability |

### 4.2 A competency is not

A competency is not merely:

- a noun;
- a topic;
- a section heading;
- a source paragraph;
- a recommendation copied from a publication;
- a framework or library name;
- a tag;
- a learning activity;
- an assessment item;
- a prerequisite relation;
- a difficulty level.

## 5. Competency granularity

Granularity is determined by demonstrability and semantic independence, not by source paragraph boundaries.

A competency should be small enough that:

- a reviewer can decide whether a learner has demonstrated it;
- its evidence can be reviewed coherently;
- it can participate in future relations without ambiguity.

A competency should be large enough that:

- it represents a meaningful capability;
- it is not a mechanically split clause;
- it does not create excessive fragmentation.

### 5.1 Merge rule

Multiple source items may support one competency only when they describe the same underlying capability or inseparable aspects of that capability.

A merge is valid when all of the following hold:

1. The resulting outcome has one primary action.
2. None of the merged items introduces an independently assessable capability that disappears after merging.
3. The merged wording remains faithful to all linked evidence.
4. The relationship between the items can be explained in `normalization_notes`.
5. A future independent source discussing the same capability could reasonably attach to the same competency.

A merge is invalid when it joins ideas merely because they appear in the same section, layer, pattern, or publication.

### 5.2 Split rule

One source item may support multiple competencies only when it contains multiple independently demonstrable capabilities.

A split is valid when:

1. Each resulting competency is supported by a distinct meaning-bearing part of the source item.
2. Each competency remains independently useful.
3. No competency depends on invented claims not present in the evidence.
4. `normalization_notes` explain the split.

A source item must not be split solely to produce smaller records.

## 6. Evidence model

The canonical relationship is many-to-many:

```text
Source 1 ─┐
          ├─ Source items ─┐
Source 2 ─┘                ├─ Evidence ─ Canonical competency
                           │
Source 3 ─ Source items ───┘
```

Therefore:

- one competency may have evidence from many source items;
- one competency may have evidence from many source packages;
- one source item may support several competencies;
- a source package does not own a competency;
- canonical competency identity is independent from source identity.

### 6.1 Evidence requirements

Every canonical competency must have at least one evidence entry.

Each evidence entry must identify:

- `source_id`;
- `source_version`;
- one or more existing `item_ids`.

Evidence references are versioned because a future source-package version may change its imported item set.

### 6.2 Evidence does not define identity

Two competencies are not different merely because they cite different sources.

A new source that supports an existing capability should normally add evidence to the existing competency rather than create another competency.

## 7. Canonical wording rules

### 7.1 Title

The title is a concise action-oriented label.

Preferred form:

```text
<Action verb> <object or capability>
```

Examples:

- Explain repository responsibilities
- Explain separation of concerns in Android applications
- Design a data layer around repositories
- Explain unidirectional data flow
- Apply dependency injection to component dependencies

Avoid:

- vague verbs such as `understand`, `know`, or `learn`;
- source-relative wording such as `Understand this guide's recommendation`;
- publication headings;
- implementation detail not supported by evidence;
- multiple primary actions joined by `and`.

### 7.2 Outcome

The outcome defines what a learner or practitioner can demonstrate.

The outcome must:

1. begin with an observable action;
2. contain one primary capability;
3. be source-independent;
4. remain faithful to all evidence;
5. include enough scope to distinguish it from nearby competencies;
6. avoid claims not supported by evidence;
7. avoid prescribing one implementation when the source supports a broader principle.

Preferred verbs include:

- explain;
- describe;
- compare;
- analyze;
- design;
- implement;
- apply;
- identify;
- evaluate;
- justify.

### 7.3 Bad and good examples

Bad:

```text
Understand repositories.
```

Good:

```text
Explain how repositories expose application data, centralize data changes,
and coordinate multiple data sources.
```

Bad:

```text
Use MVVM because Android Developers recommends it.
```

Good:

```text
Explain how separating UI state production from UI rendering reduces
responsibility in Android framework components.
```

The second form is acceptable only when the evidence actually supports that capability. A familiar architecture label must not be invented from implication alone.

## 8. Source independence and cross-source identity

Canonical competencies must not encode accidental properties of one source.

A competency should not normally include:

- publication titles;
- section names;
- source-specific ordering;
- source-specific examples;
- editorial wording;
- page-relative references such as "as described above";
- claims imported only from linked but unimported publications.

When a later source is imported, reviewers must compare candidate competencies against the existing canonical set.

The default decision sequence is:

1. Does an existing competency express the same demonstrable capability?
2. If yes, attach evidence to it.
3. If partially, determine whether the candidate is:
   - narrower;
   - broader;
   - a distinct independently assessable capability.
4. Create a new competency only when semantic equivalence cannot be established.

## 9. Duplicate and near-duplicate policy

Two competency records are duplicates when a competent reviewer would assess them using substantially the same evidence and success criteria.

The following do not justify separate competencies by themselves:

- different verbs with the same intended demonstration;
- singular versus plural;
- source-specific terminology;
- title phrasing;
- different evidence sources;
- different examples;
- different source hierarchy.

Possible duplicates must be resolved editorially before acceptance.

Automated validation may detect suspicious similarity later, but semantic deduplication remains a review responsibility.

## 10. Determinism

Normalization should be reproducible but is not assumed to be fully automatic.

Given the same:

- source package;
- existing canonical competency set;
- normalization rules;
- repository state;

independent reviewers should converge on materially equivalent competency boundaries and evidence mappings.

Determinism is improved by:

- explicit merge and split rules;
- canonical wording rules;
- stable identifiers;
- required normalization notes for non-trivial transformations;
- review status before acceptance;
- prohibition on unsupported inference.

## 11. Minimum data model

The initial canonical model contains two package files:

```text
competencies/
    normalized/
        <competency-set-id>/
            competency-set.yaml
            competencies.yaml
```

The directory remains named `normalized/` for repository compatibility. The domain entities stored within it are canonical competencies.

### 11.1 Competency set metadata

Required conceptual fields:

```yaml
schema_version: 1

id: android-app-architecture
title: Android app architecture
description: >
  Canonical competencies related to Android application architecture.

language: en
version: 1
status: review
```

### 11.2 Canonical competency list

```yaml
schema_version: 1

competency_set_id: android-app-architecture
competency_set_version: 1

competencies:
  - id: explain-repository-responsibilities
    title: Explain repository responsibilities
    outcome: >
      Explain how repositories expose application data, centralize data
      changes, and coordinate multiple data sources.

    evidence:
      - source_id: android-developers-app-architecture
        source_version: 1
        item_ids:
          - expose-application-data-through-repositories
          - centralize-data-changes-in-repositories
          - resolve-conflicts-between-data-sources

    normalization_notes: >
      The linked source items describe inseparable responsibilities of the
      repository abstraction and are represented as one explanatory
      competency.
```

The identifiers above are illustrative. Implementations must use actual imported source-item identifiers.

### 11.3 Required competency fields

Required:

- `id`;
- `title`;
- `outcome`;
- `evidence`.

Optional:

- `normalization_notes`.

### 11.4 Stable identifiers

A competency ID describes the canonical capability rather than:

- its source;
- its position;
- its current evidence count;
- its version;
- its implementation technology.

IDs should remain stable when:

- wording is clarified without changing meaning;
- new evidence is added;
- evidence is removed but the competency remains supported;
- the competency moves between files without semantic change.

## 12. Normalization notes

`normalization_notes` record editorial reasoning, not source content.

They are required when:

- several source items are merged;
- one source item supports several competencies;
- canonical wording intentionally generalizes source-specific terminology;
- a candidate was attached to an existing competency rather than creating a new one;
- the evidence-to-outcome mapping is not self-evident.

They should explain:

- why the boundary was chosen;
- what was merged or split;
- why the wording remains faithful;
- how unsupported inference was avoided.

They should not:

- introduce new claims;
- replace missing evidence;
- describe implementation mechanics irrelevant to the competency;
- justify an outcome that the source does not support.

## 13. Architectural validation rules

A canonical competency package is structurally valid only when:

1. Package metadata and competency list conform to their schemas.
2. `competency_set_id` matches the package metadata ID.
3. `competency_set_version` matches the metadata version.
4. Competency IDs are unique within the repository's canonical namespace.
5. Every competency has at least one evidence entry.
6. Every evidence `source_id` resolves to a source package.
7. Every `source_version` matches the referenced package version.
8. Every evidence `item_id` exists in the referenced source package.
9. Every evidence entry contains at least one item ID.
10. Duplicate item IDs within one evidence entry are rejected.
11. Exact duplicate evidence entries are rejected.
12. Empty or whitespace-only titles and outcomes are rejected.
13. Unsupported fields from future models are rejected by the initial schema.
14. Source packages remain unchanged by normalization.
15. The pilot package remains in `review` until separately accepted.

The validator may enforce structural and referential integrity. It cannot fully determine semantic quality, unsupported inference, or duplicate meaning; those remain review responsibilities.

## 14. Editorial review rules

A reviewer must reject a competency when:

- the outcome is broader than its evidence;
- the outcome introduces an unsupported framework, pattern, or term;
- the title is only a topic label;
- multiple independent competencies were merged;
- one capability was split without semantic justification;
- an equivalent canonical competency already exists;
- normalization notes are required but absent;
- source-specific wording prevents cross-source reuse;
- evidence does not directly support the claimed capability.

## 15. Non-goals

The canonical competency model intentionally does not define:

- prerequisites;
- dependency graphs;
- competency relations;
- topic membership;
- tags;
- difficulty;
- seniority levels;
- priority;
- learning order;
- learning paths;
- lessons;
- examples;
- practice tasks;
- interview questions;
- assessments;
- mastery thresholds;
- estimated time;
- user progress;
- recommendations;
- personalization.

These belong to separate models that may reference canonical competency IDs.

## 16. Future extensions

Future models may introduce:

- competency relations;
- prerequisite graphs;
- topic taxonomies;
- learning paths;
- assessment mappings;
- practice mappings;
- aliases and deprecations;
- semantic duplicate reports;
- user mastery and progress.

Those extensions must reference canonical competencies rather than redefining them.

The canonical competency model should remain focused on:

```text
stable capability
+
canonical wording
+
traceable evidence
```

## 17. Consequences

### Positive consequences

- Multiple publications can support one stable competency.
- Imported source packages remain immutable and auditable.
- Canonical identifiers can support future systems.
- Duplicate knowledge is reduced.
- Source wording and canonical wording remain clearly separated.
- The knowledge model can evolve independently of publication structure.
- Editorial decisions become reviewable through normalization notes.

### Costs

- Normalization requires semantic review.
- Automated validation cannot guarantee competency quality.
- Cross-source imports require deduplication work.
- Canonical wording becomes repository-owned and must be maintained carefully.
- Incorrect competency boundaries can affect future relations and assessments.

These costs are accepted because canonical stability is foundational to the repository.

## 18. Decision summary

The repository adopts a source-independent canonical competency model.

Imported source items remain immutable evidence-bearing records.

Canonical competencies are stable, demonstrable units of knowledge or skill. They are connected to source items through explicit versioned evidence references.

Normalization is an editorial process governed by merge, split, wording, deduplication, and traceability rules.

Future learning, assessment, relation, and progress models must reference canonical competency IDs and remain outside this core model.
