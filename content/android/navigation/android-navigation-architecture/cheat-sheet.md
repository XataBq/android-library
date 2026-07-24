# Android Navigation Architecture — Cheat Sheet

## Core ownership

| Concern | Owner |
| --- | --- |
| destination order, current entry, history | navigation host / back stack |
| framework navigation execution | active UI / navigation coordinator |
| presentation state and decisions | destination- or graph-scoped ViewModel |
| authoritative application data | Repository |
| reusable business rule | optional use case |
| authentication and authorization | session/data/domain boundary, not routes |

Keep `NavController`, `Activity`, `Fragment`, `View`, and composable functions
out of ViewModel, Repository, and use-case state.

## Vocabulary

- **Destination:** a place the host can show.
- **Route:** destination identity plus small reconstruction inputs.
- **Graph:** destinations and nested navigation structure for a host.
- **Back-stack entry:** one runtime instance with lifecycle, saved state, and
  ViewModel store.
- **Current destination:** the destination associated with the top entry.

## Stack operations

- `navigate`: normally push a new entry.
- `popBackStack`: remove the top entry and clear its destination owner.
- `launchSingleTop`: avoid another copy only when target is already on top.
- `popUpTo`: remove entries toward a target.
- `inclusive = true`: remove the `popUpTo` target too.
- `saveState` / `restoreState`: retain and restore eligible destination state.

Back reverses history. Up follows app hierarchy. They may coincide, but deep
links can make them differ.

## Argument rule

Pass:

- stable IDs;
- small enums, filters, or route parameters;
- values required to reconstruct the destination.

Do not pass:

- mutable entities;
- repositories or services;
- bitmaps or large collections;
- secrets;
- values assumed to prove authorization.

Reload authoritative data from its Repository. Typed routes reduce encoding
errors; they do not validate access or data existence.

## API and version note

- AndroidX Navigation 2 type-safe Compose/Kotlin DSL routes require 2.8.0+.
- Multiple back-stack support requires 2.4.0+.
- Navigation saved-state results require 2.3.0+.
- Fragment Result API requires Fragment 1.3.0+.
- Navigation 3, Navigation 2 typed routes, XML/Safe Args, and older route
  styles are different valid API families.

Always verify signatures, maturity, serialization setup, and testing helpers
against the AndroidX artifacts installed in the project. Do not copy one API
style into every codebase mechanically.

## Events and effects

Choose one explicit policy:

| Need | Candidate |
| --- | --- |
| active UI action | direct callback |
| best-effort occurrence | non-replaying effect stream |
| must survive recreation until handled | pending effect with ID and acknowledgement |
| durable outcome | Repository data, rendered as state |

Replay can duplicate navigation; no replay can lose it. There is no universal
`Event` wrapper.

## Scopes

- Destination ViewModel: one entry.
- Graph ViewModel: one workflow shared by nested destinations.
- Activity ViewModel: every hosted destination; use only for truly
  Activity-wide presentation state.

Popping the owner clears its ViewModels. Covering an entry does not.

## Multiple top-level histories

For bottom navigation:

- save state when leaving a top-level destination;
- restore its state when returning;
- use single-top behavior to avoid duplicate roots;
- define reselect behavior;
- consider retained memory and depth.

## Result selection

| Result | Prefer |
| --- | --- |
| local active UI response | callback |
| small one-time result to previous entry | previous entry `SavedStateHandle` |
| Fragment-to-Fragment Bundle result | Fragment Result API |
| ongoing workflow draft | graph-scoped ViewModel |
| authoritative saved change | Repository |

Consume one-time results exactly once.

## External entries

For every deep link or App Link:

1. validate scheme, host, path, route version, and argument shape;
2. handle missing or deleted data;
3. authenticate when required;
4. authorize access to the referenced resource;
5. reject unsupported and internal-only routes;
6. keep sensitive values out of URLs.

Verified App Links improve link routing, not trust in parameters. Navigation is
not authorization. Audit `android:exported` and intent filters explicitly.

## Restoration

Saved navigation state may restore entries and small inputs. A recreated
ViewModel reloads current data from repositories. It does not recover:

- in-memory entities;
- jobs and open resources;
- network calls;
- large object graphs;
- uncommitted durable work.

## Test matrix

- pure route parsing and validation;
- presentation decision or coordinator with fakes;
- graph start destination and nested graph;
- destination and typed-route assertion;
- Back, Up, `popUpTo`, and top-level reselect;
- multiple histories;
- result delivery and consumption;
- accepted and rejected deep links;
- authentication and authorization gates;
- recreation from saved inputs.

## Red flags

- `NavController` in ViewModel;
- Repository navigates;
- large object arguments;
- duplicate destination Boolean in UI state;
- global navigation bus;
- Activity scope by default;
- replayed stale effect;
- unconsumed result;
- duplicate top-level stacks;
- deep-link parameter treated as trusted;
- route access treated as authorization;
- screenshot-only navigation tests.
