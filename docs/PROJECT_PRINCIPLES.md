# Project Principles

These principles guide product, architecture, content, and implementation decisions.

## 1. Learning comes first

The platform exists to improve engineering competence. Development work must not permanently displace actual learning.

Target time allocation:

- approximately 70% learning;
- approximately 30% platform development.

## 2. Content is interface-independent

Educational content must remain usable without a specific application.

The same content should be readable through:

- the Git repository;
- a Markdown editor or Obsidian;
- the web client;
- the Android client.

## 3. Git stores shared educational content

Git is the source of truth for:

- topics;
- roadmap metadata;
- theory;
- cheat sheets;
- tests;
- practice;
- interview materials;
- schemas;
- documentation;
- content history.

User-specific progress does not belong in shared content files.

## 4. Personal state is separate

The following are personal state:

- completed lessons;
- attempts and answers;
- scores;
- mastery;
- weak areas;
- review schedule;
- bookmarks;
- personal notes;
- activity history.

This state may begin in local storage and later move to a database.

## 5. Architecture precedes implementation

Before implementing a meaningful feature:

1. define the problem;
2. identify the domain model;
3. define boundaries and ownership;
4. approve important decisions;
5. implement the smallest useful increment.

## 6. Prefer the simplest viable architecture

Do not add a custom backend, message broker, distributed cache, microservices, or complex infrastructure before the product requires them.

## 7. Quality over volume

One reviewed, coherent topic is more valuable than many shallow generated files.

## 8. Every topic must be actionable

A complete topic should contain:

- learning outcomes;
- theory;
- examples;
- common mistakes;
- a cheat sheet;
- assessment;
- practice;
- interview preparation;
- relevant Android or JVM connections where applicable;
- sources.

## 9. AI assists; humans remain accountable

AI may:

- explain;
- structure;
- generate drafts;
- create tasks;
- implement approved changes;
- review;
- assess answers.

AI output must not be treated as automatically correct.

## 10. Small, reviewable iterations

Each task should:

- have a clear goal;
- have explicit acceptance criteria;
- remain focused;
- be reviewable as a small diff;
- avoid unrelated refactoring.

## 11. Decisions must remain explainable

Important architectural and product choices must be recorded as ADRs.

## 12. Offline capability is a long-term requirement

Core educational content and previously synchronized progress should eventually remain available without a network connection. AI-only features may require connectivity.
