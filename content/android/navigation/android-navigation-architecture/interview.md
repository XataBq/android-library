# Android Navigation Architecture — Interview Questions

## 1. Why describe navigation as state?

**Strong answer:** The ordered back stack, top entry, saved entry state, and
owner lifetimes determine what is visible and what Back can restore. Calls such
as `navigate` and `pop` are transitions of that state.

**Weak answer:** Navigation is any call that opens another screen.

**Follow-up:** Which parts survive configuration change or process recreation?

## 2. Distinguish destination, route, graph, and back-stack entry.

**Strong answer:** A destination is a declared place, a route identifies a
destination instance with small inputs, a graph structures destinations, and
an entry is a runtime instance with lifecycle, saved state, and ViewModel
store.

**Weak answer:** They are four names for the same screen.

## 3. Who should own NavController?

**Strong answer:** The active UI host or navigation coordinator that owns the
NavHost and its lifecycle. ViewModel can expose a presentation decision;
repositories and use cases return data or outcomes.

**Weak answer:** Put it in ViewModel so every layer can navigate.

**Follow-up:** How would you test the presentation decision without a graph?

## 4. Can business logic decide whether navigation is allowed?

**Strong answer:** Yes. A use case or repository may determine eligibility or
authorization and return an outcome. UI still performs the framework
transition.

**Weak answer:** Either business logic must navigate directly or it cannot
influence navigation.

## 5. What happens when a destination is popped?

**Strong answer:** Its entry is removed, its lifecycle ends, and
destination-scoped ViewModels are cleared. Covering or stopping an entry is not
the same as popping it.

**Weak answer:** The composable or View disappears, but all owners remain
forever.

## 6. How do Back and Up differ?

**Strong answer:** Back reverses chronological history. Up follows the
application's hierarchy toward a parent. Deep-link entry can make their
different task and hierarchy semantics visible.

**Weak answer:** Up is a custom icon that must always call Back.

## 7. Why pass an ID instead of an object?

**Strong answer:** A small stable ID is a reconstruction input. The destination
reloads authoritative current data from a Repository, avoiding stale mutable
copies and large saved-state/Binder payloads.

**Weak answer:** Parcelable makes any object safe and current.

**Follow-up:** Does knowing an ID authorize the user to access it?

## 8. What do type-safe routes guarantee?

**Strong answer:** In supported Navigation versions they align route
declaration, navigation, and argument decoding at compile time. They do not
guarantee data existence, authorization, or safe large payloads.

**Weak answer:** They make all navigation secure and work identically in every
Android project.

**Follow-up:** What version and graph style does the project actually use?

## 9. Where should navigation state and screen state live?

**Strong answer:** History belongs to the back stack; small reconstruction
inputs to arguments or saved state; derived screen state to ViewModel; durable
application data to Repository; ephemeral visual details to local UI.

**Weak answer:** Mirror all of them in one Activity ViewModel.

## 10. Compare a direct callback and ViewModel navigation effect.

**Strong answer:** A callback fits an action in active UI. An effect fits an
asynchronous presentation decision but requires explicit loss, replay,
duplicate, and acknowledgement semantics.

**Weak answer:** A replaying global SharedFlow guarantees exactly-once
navigation.

## 11. How do you prevent duplicate one-off navigation?

**Strong answer:** Choose a delivery policy. For a must-handle transition,
retain a pending effect with an identity and clear it only after matching UI
acknowledgement; for active UI, prefer a direct callback.

**Weak answer:** Add delay or clear every event in `onStart`.

## 12. Explain popUpTo, inclusive, and launchSingleTop.

**Strong answer:** `popUpTo` removes toward a target, `inclusive` also removes
the target, and single-top avoids another target only when it is already top.
Login or onboarding completion commonly clears the completed flow.

**Weak answer:** Together they delete every duplicate route anywhere.

## 13. What does a nested graph own?

**Strong answer:** It structures and encapsulates a navigation flow and may
provide a back-stack owner for shared workflow presentation state. It is not
automatically a domain, Gradle module, or authorization boundary.

**Weak answer:** Every nested graph must be one business module and database.

## 14. When is graph-scoped ViewModel preferable?

**Strong answer:** When several destinations in one bounded workflow genuinely
share presentation state that should clear when that graph is popped.

**Weak answer:** Whenever two screens need any same value, even durable
repository data.

**Follow-up:** What coupling and lifetime does Activity scope add?

## 15. What are multiple back stacks for?

**Strong answer:** They preserve independent histories for top-level
destinations such as bottom-navigation tabs. Save/restore and single-top
options prevent lost history and duplicate roots.

**Weak answer:** Create a new NavController and stack on every tab click.

**Follow-up:** What should reselecting the active tab do?

## 16. How should a destination return a small one-time result?

**Strong answer:** A previous-entry `SavedStateHandle` result or Fragment
Result can fit, depending on UI technology. Consume it once. Use a Repository
for durable changes and graph ViewModel for continuing workflow state.

**Weak answer:** Put the full entity in a global singleton and poll it.

## 17. Compare Fragment Result and shared ViewModel.

**Strong answer:** Fragment Result is lifecycle-aware, one-time, and
Bundle-compatible. A shared ViewModel is ongoing state owned by a chosen
Activity or navigation graph and can outlive individual Fragment Views.

**Weak answer:** Fragment Result is a permanent reactive data store.

## 18. What must happen when a deep link targets a protected screen?

**Strong answer:** Validate route and inputs, establish authentication, perform
resource authorization, handle missing prerequisites or records, and only
then navigate or safely resume a validated target.

**Weak answer:** If the graph matches the URI, access is already approved.

## 19. What does App Link verification establish?

**Strong answer:** It associates verified HTTP(S) links with the app and
improves routing. It does not establish trust in parameters, caller
authorization, or record existence.

**Weak answer:** Every verified link and embedded ID is trusted.

**Follow-up:** Why audit `android:exported` and intent filters separately?

## 20. What can navigation restoration recover?

**Strong answer:** Eligible stack entries, arguments, and small saved state.
Recreated owners use those references to reload authoritative data. Jobs,
services, repositories, and large object graphs are not recovered.

**Weak answer:** The whole process heap and every network request return.

## 21. How do Compose and Fragment navigation boundaries compare?

**Strong answer:** APIs differ, but ownership does not: a Compose NavHost or
Fragment/UI coordinator executes navigation, screens receive callbacks, and
ViewModel plus lower layers remain free of controller types.

**Weak answer:** Compose requires controller access in every composable and
ViewModel, while Fragments require no boundary.

## 22. What should a navigation test suite prove?

**Strong answer:** Route parsing, presentation decisions, graph start and
nested structure, destination changes, stack clearing, multiple histories,
results, deep-link rejection, authorization gates, and recreation. Visual
tests are supplementary.

**Weak answer:** One screenshot of every screen proves navigation.

**Follow-up:** Which assertions depend on the installed Navigation API version?
