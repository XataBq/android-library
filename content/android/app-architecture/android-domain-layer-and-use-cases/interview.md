# Android Domain Layer and Use Cases — Interview preparation

## Foundational questions

### 1. Why is the Domain layer optional?

**Strong answer:** UI and Data are the baseline. Domain earns its cost when it
owns complex, reused, or coordinated application operations and improves
ownership or testability.

**Weak answer:** Every professional app needs three layers.

**Follow-up:** What evidence would make you add it later?

### 2. When should a ViewModel call a repository directly?

**Strong answer:** When the operation is simple, screen-specific, and the
ViewModel only maps the repository contract into UI state without reusable
application policy.

**Weak answer:** Never; all calls require an interactor.

**Follow-up:** At what point would you extract a use case?

### 3. What responsibility should one use case have?

**Strong answer:** One coherent application operation or capability with clear
inputs, outputs, expected failures, and focused collaborators.

**Weak answer:** One class for every repository method.

**Follow-up:** Can one use case call several repository methods?

### 4. Is a use case the same as a repository?

**Strong answer:** No. A repository owns application data and source policy; a
use case owns an operation or rule and may coordinate repository contracts.

**Weak answer:** Both are wrappers, so placement is a naming preference.

**Follow-up:** Who should choose between cache and network?

### 5. How do you distinguish UI, Domain, and Data logic?

**Strong answer:** By responsibility: presentation and screen state; stable
application operations and rules; data ownership, source selection, and
synchronization.

**Weak answer:** By which package currently contains the code.

**Follow-up:** Give a behavior whose correct owner depends on product context.

## Design and boundary questions

### 6. When does multi-repository coordination justify a use case?

**Strong answer:** When the coordination forms one stable application operation
that should not belong to any single data owner and benefits from reuse or
independent testing.

**Weak answer:** Whenever two repositories appear in the same function.

**Follow-up:** How do you prevent the use case from becoming a new repository?

### 7. What should a use case depend on?

**Strong answer:** Focused repository abstractions or stable Data APIs plus
plain application policies and values.

**Weak answer:** DAO and Retrofit types because that avoids extra interfaces.

**Follow-up:** Where should source selection occur?

### 8. Should Domain code depend on Android `Context`?

**Strong answer:** Normally no. Pass interpreted values or depend on a narrow
boundary whose implementation can use platform services in the appropriate
layer.

**Weak answer:** Yes whenever a string or system service is needed.

**Follow-up:** Where should localized error text be produced?

### 9. Must Domain live in a dedicated Gradle module?

**Strong answer:** No. Module separation is an implementation trade-off.
Responsibility and dependency direction matter first.

**Weak answer:** Yes; otherwise it is not Clean Architecture.

**Follow-up:** What would justify extracting a module?

### 10. How should models cross the Domain boundary?

**Strong answer:** Reuse models when contracts genuinely match; introduce a
Domain model when it expresses different constraints or protects a stable
operation contract.

**Weak answer:** Copy every model once per layer.

**Follow-up:** What costs does unnecessary mapping create?

## Coroutines, failures, and testing

### 11. When should a use case return `Flow`?

**Strong answer:** When it represents observable application data that can
change. The caller owns collection lifetime and UI lifecycle.

**Weak answer:** Every use case should return Flow for consistency.

**Follow-up:** What is more suitable for a one-shot submit action?

### 12. Who owns coroutine scope and cancellation?

**Strong answer:** The caller owns the structured scope. A use case suspends or
returns Flow and cooperates with cancellation without hidden unmanaged work.

**Weak answer:** Each use case creates an IO scope so work always finishes.

**Follow-up:** What can go wrong with that private scope?

### 13. Should every use case return `Result<T>`?

**Strong answer:** No. Choose a contract that represents expected application
outcomes and required failures; plain values, sealed outcomes, exceptions, and
Flow each have valid uses.

**Weak answer:** One wrapper is mandatory across every layer.

**Follow-up:** How would you represent eligibility rejection?

### 14. How do you test a multi-repository use case?

**Strong answer:** Use controllable fakes and cover success, expected rejection,
repository failure, ordering/coordination where relevant, and cancellation.

**Weak answer:** Verify that every collaborator method was called once.

**Follow-up:** What makes a fake more informative than a forwarding mock test?

### 15. What does framework independence improve?

**Strong answer:** It clarifies ownership and caller lifetime, enables plain
unit tests, and allows the operation to serve multiple presentation surfaces.

**Weak answer:** It only makes code look cleaner.

**Follow-up:** Can a repository implementation still use Android APIs?

## Scenario and trade-off questions

### 16. A use case only calls `users.get(id)` and returns the value. Keep it?

**Strong answer:** Usually remove it unless it establishes a distinct contract,
reuse point, policy, or planned boundary whose current value outweighs the
indirection.

**Weak answer:** Keep it because all repository methods need use cases.

**Follow-up:** What future change could justify extraction?

### 17. A checkout rule is copied across three ViewModels. What would you do?

**Strong answer:** Identify one stable application operation, extract the reused
rule or use case, preserve UI state in each ViewModel, and keep data ownership
in repositories.

**Weak answer:** Move all three ViewModels into the Domain layer.

**Follow-up:** What inputs and outcomes should the operation expose?

### 18. How does Domain-layer design differ in small and large apps?

**Strong answer:** Small apps benefit from fewer boundaries until complexity or
reuse appears. Larger apps may gain more from stable operations, coordination,
team ownership, and independent tests, but size alone does not dictate a
template.

**Weak answer:** Small apps use MVVM; large apps must use Clean Architecture.

**Follow-up:** Which concrete complexity signals matter more than code size?
