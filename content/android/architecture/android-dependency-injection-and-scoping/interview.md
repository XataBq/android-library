# Android Dependency Injection and Scoping — Interview Questions

## 1. What problem does dependency injection solve?

**Strong answer:** It makes required collaborators explicit, separates object
use from construction, centralizes implementation selection, enables
replacement, and supports deliberate ownership.

**Weak answer:** It adds annotations so objects construct themselves.

## 2. How does dependency inversion differ from DI?

**Strong answer:** Dependency inversion is a dependency-direction principle:
policy depends on suitable abstractions and infrastructure implements them. DI
is a construction technique used to supply implementations.

**Weak answer:** They are two names for Hilt.

## 3. Why prefer constructor injection?

**Strong answer:** Dependencies are visible, required at creation, naturally
immutable, and directly replaceable in tests; no hidden lookup or
half-initialized object remains.

**Weak answer:** Constructor injection removes the need to design interfaces.

**Follow-up:** What does an oversized constructor tell you?

## 4. What is a composition root?

**Strong answer:** The narrow application or feature boundary that chooses
implementations and assembles the object graph near framework entry.

**Weak answer:** Any class that calls a global container.

## 5. Explain an object graph.

**Strong answer:** Objects are nodes, required dependencies are directed edges,
transitive construction must resolve all edges, scopes define reuse, and owners
bound lifetime. Cycles usually reveal design problems.

**Weak answer:** It is a list of annotations in one module.

## 6. DI versus service locator?

**Strong answer:** DI supplies dependencies through the construction contract.
A locator lets the consumer query hidden dependencies, coupling behavior and
tests to container state.

**Weak answer:** A global `resolve<T>()` call is constructor injection.

## 7. When is manual DI sufficient?

**Strong answer:** For a small or stable graph where explicit containers and
feature factories remain understandable. Framework automation becomes useful
when wiring, scopes, and variants create costly boilerplate.

**Weak answer:** Manual DI means constructing repositories inside ViewModel
methods.

## 8. What can a DI framework not decide?

**Strong answer:** Correct repository/domain boundaries, cohesive
responsibilities, appropriate owner lifetime, safe Context use, or whether
global mutable state is valid.

**Weak answer:** If the graph compiles, architecture and ownership are correct.

## 9. Compare provider, lazy, and factory.

**Strong answer:** Provider obtains on demand under its binding/scope semantics;
lazy memoizes one obtained value for its wrapper; factory creates using explicit
runtime input. None alone defines a global scope.

**Weak answer:** All always return one singleton.

## 10. What does scope mean?

**Strong answer:** Reuse within a concrete owner/component instance, with
creation, reuse, and destruction boundaries. The owner and lifetime are part of
the definition.

**Weak answer:** A scope annotation makes an object immortal.

## 11. What does unscoped mean?

**Strong answer:** The container normally creates a new instance per resolution.
The object still has a finite lifetime through whichever consumer retains it.

**Weak answer:** It has no owner and cannot be garbage-collected.

## 12. What does Hilt @Singleton guarantee?

**Strong answer:** One instance per `SingletonComponent`, normally one
application process. It does not survive process death, represent persistence,
or automatically reset on logout.

**Weak answer:** One instance forever across restarts and tests.

## 13. Compare ActivityScoped and ActivityRetainedScoped.

**Strong answer:** Activity scope follows one Activity instance and is recreated
on configuration change. Activity-retained scope follows the logical Activity
across recreation and ends after final destruction.

**Weak answer:** Both are aliases for process scope.

## 14. What is the Fragment scope trap?

**Strong answer:** Fragment scope follows the Fragment instance, which can
outlive its View. A Fragment-scoped object must not retain a destroyed View or
binding.

**Weak answer:** Fragment and Fragment View always have identical lifetimes.

## 15. How should ViewModel dependencies be injected?

**Strong answer:** Through its constructor and the current
ViewModelProvider/Hilt factory path, with repositories/use cases and
SavedStateHandle. Never retain UI owners or request the ViewModel as an ordinary
graph object.

**Weak answer:** Field-inject the ViewModel and Activity into each other.

## 16. How does navigation graph ViewModel scope work?

**Strong answer:** A `NavBackStackEntry` is the `ViewModelStoreOwner`; the
ViewModel survives while that entry remains and clears when popped. Hilt helpers
provide its factory but do not create a universal arbitrary graph scope.

**Weak answer:** Every nested graph automatically makes all dependencies
singletons.

## 17. When are qualifiers necessary?

**Strong answer:** When bindings share a Kotlin type but carry different
semantics, such as public/authenticated clients or IO/Default dispatchers.
Qualify provider and consumer.

**Weak answer:** Use string names inside a locator.

## 18. What problem does multibinding solve?

**Strong answer:** Independent modules contribute set/map handlers or strategies
without one central list. Keys must be stable; set order is not business policy.

**Weak answer:** It guarantees validators run in source-file order.

## 19. When should assisted injection be used?

**Strong answer:** When graph-known dependencies combine with deliberate
runtime input for factory-created or framework-owned objects. Restoration and
shorter-lived inputs still require explicit policy.

**Weak answer:** Pass Activity, View, and any large runtime object to a
singleton factory.

## 20. Which Context should be injected?

**Strong answer:** Application Context for process-owned platform adapters;
Activity/themed Context only for UI-owned themed/window work. Domain and
ViewModel generally need a narrower abstraction instead.

**Weak answer:** Any Context is interchangeable because the type is identical.

## 21. How should a dependency cycle be fixed?

**Strong answer:** Revisit responsibilities, split the minimal contract, invert
information flow, or introduce a cohesive higher owner. Do not hide it with a
global bus or delayed lookup.

**Weak answer:** Add providers until the cycle compiles.

## 22. How do unit and integration replacement differ?

**Strong answer:** Unit tests directly construct the subject with fresh fakes.
Integration tests can replace component/module bindings and create a fresh test
graph per test.

**Weak answer:** Both mutate a production singleton and restore it if the test
passes.

## 23. Where may framework annotations live?

**Strong answer:** At composition and concrete UI/Data implementation
boundaries where they serve wiring. Domain contracts and business code should
not query containers or depend on framework lifecycle types.

**Weak answer:** Every domain interface needs Hilt annotations to be
testable.

## 24. What are the most dangerous DI anti-patterns?

**Strong answer:** Global locator, hidden container parameters, blanket
singletons, mutable global state, Context/UI leaks, scope mismatch, giant
modules, ambiguous bindings, assumed multibinding order, test-global mutation,
and providers hiding cycles or oversized classes.

**Weak answer:** The only DI problem is slow annotation processing.

**Follow-up:** Which of these can still compile successfully?
