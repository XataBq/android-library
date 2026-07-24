# Android Dependency Injection and Scoping — Cheat Sheet

## Mental model

```text
constructor declares dependency
composition root creates implementation
scope defines lifetime and reuse
owner controls destruction
```

DI is graph construction. It is not a service locator, global registry,
annotation processor, or guarantee of good architecture.

## Constructor injection

Prefer it because:

- required dependencies are visible;
- an object cannot be used half-initialized;
- references can be immutable;
- unit tests call an ordinary constructor;
- no hidden container lookup exists.

Field injection is a framework-boundary fallback, not a default.

## Dependency inversion

High-level policy depends on an abstraction shaped for application needs.
Infrastructure implements it. DI supplies the implementation.

```text
ViewModel / use case → Repository interface ← Data implementation
```

Changing an annotation does not fix the wrong dependency direction.

## Composition root and graph

The root:

- chooses implementations;
- constructs transitive dependencies;
- resolves qualifiers;
- defines graph owners and feature factories;
- centralizes framework wiring.

Nodes are objects; edges are constructor dependencies. A cycle usually signals
confused responsibility.

## DI versus service locator

| DI | Service locator |
| --- | --- |
| dependency passed in | object queries container |
| requirement visible in constructor | requirement hidden in implementation |
| local test replacement | shared/global test setup |
| owner creates graph | consumer controls lookup |

Passing `Application`, component, entry point, or a generic map through layers
is still service location.

## Provider and factory

| Need | Use |
| --- | --- |
| create graph now | constructor |
| obtain later | provider |
| memoize one provider result locally | lazy |
| create with runtime input | factory / assisted factory |
| share identity within owner | scoped binding |
| cheap stateless new value | unscoped binding |

Provider does not guarantee same or new identity; scope determines reuse.

## Scope checklist

For every scope name, identify:

1. owner;
2. creation boundary;
3. reuse boundary;
4. destruction boundary.

“Singleton” without a component/owner is incomplete.

## Android owner table

| Owner | Typical lifetime | Notes |
| --- | --- | --- |
| Application / Hilt SingletonComponent | one process | not persistent across process death |
| ActivityRetainedComponent | logical Activity across recreation | no Activity instance binding |
| ActivityComponent | one Activity instance | recreated with Activity |
| FragmentComponent | Fragment instance | can outlive Fragment View |
| View owner | rendered View | release with View destruction |
| ViewModelComponent | one ViewModel | follows its ViewModelStoreOwner |
| NavBackStackEntry ViewModel owner | while destination/graph entry remains | cleared when popped |
| unscoped request | one resolution | still retained by its consumer |

Scope only when shared identity is required for correctness, synchronization,
or measured construction cost.

## ViewModel rules

- Obtain through `ViewModelProvider` or current navigation/Compose helpers.
- Inject repositories/use cases and `SavedStateHandle`.
- `@ViewModelScoped` means one binding per ViewModel component.
- Do not inject Activity, Fragment, View, binding, themed Context, or
  NavController.
- Assisted ViewModel values are not automatically restored after process death.

Hilt and Navigation helpers are version-sensitive; check installed artifacts.

## Navigation graph ownership

A `NavBackStackEntry` can own a shared workflow ViewModel. Hilt does not create
an arbitrary general-purpose navigation-graph component scope merely because a
graph exists.

Use graph scope for coherent workflow state and release it when the entry is
popped.

## Qualifiers

Use typed qualifiers when the same Kotlin type has different semantics:

- public versus authenticated client;
- IO versus Default dispatcher;
- production versus sandbox endpoint;
- application versus Activity Context.

Qualifiers select bindings. They do not create scopes.

## Multibinding

Use sets/maps for independent:

- validators;
- handlers;
- strategies;
- feature/plugin contributions.

Set iteration order is not business policy. Map keys must be unique and stable.
Model priority explicitly when order matters.

## Assisted injection

Use a factory when some inputs come from the graph and others are known only at
runtime. Do not pass shorter-lived UI owners. Use `SavedStateHandle` when a
small route input must survive recreation.

Assisted APIs and ViewModel creation callbacks are framework/version-specific.

## Context rules

- Application Context: process-owned files, resources, preferences, system
  services in UI/Data adapters.
- Activity/themed Context: UI/window/theme work only.
- Never put Activity Context in `@Singleton`.
- Fragment-scoped objects must not retain destroyed Fragment Views.
- Domain and ViewModel normally need no Context.

## Testing checklist

- Construct units directly with fresh fakes.
- Inject fake clocks and dispatchers.
- Give every test a fresh owner/graph.
- Use test modules/components only for integration boundaries.
- Match qualifier and scope when replacing a binding.
- Reset or destroy scoped test graphs.
- Never mutate a production singleton between tests.
- Verify parallel-test isolation.

## Smells

- global locator or static graph;
- container passed through layers;
- field injection by default;
- every binding scoped singleton;
- mutable singleton session without reset contract;
- Activity/Fragment/View/NavController retained too long;
- provider used to hide a huge constructor;
- duplicate bindings without qualifier;
- assumed multibinding order;
- assisted value assumed restorable;
- giant mixed-ownership module;
- delayed lookup hiding a graph cycle;
- Retrofit injected into UI;
- tests mutating production globals.

## Interview-ready summary

Constructor injection exposes dependencies. The composition root selects
implementations and assembles the graph. Scope means reuse inside a concrete
owner lifetime, not immortality. Android component, ViewModel, and navigation
entry lifetimes differ. Framework annotations automate wiring; correct
boundaries, Context use, replacement, and destruction remain architectural
decisions.
