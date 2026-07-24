# Android Domain Layer and Use Cases — Cheat sheet

## Add a Domain layer when

- complex application rules obscure UI-state production;
- the same operation is reused by several state holders;
- one coherent operation coordinates multiple repositories;
- the operation is a stable application capability;
- independent tests materially improve safety and ownership.

## Keep it out when

- a class only forwards one repository method;
- the logic is screen-specific presentation behavior;
- extraction creates names and files but no policy;
- Data ownership or source policy is the real responsibility;
- separate models or modules would be identical ceremony.

## Responsibility table

| UI | Domain/application | Data |
|---|---|---|
| screen state | coherent application operation | application data ownership |
| user actions | reusable or complex rules | repository and source policy |
| presentation decisions | multi-repository coordination | persistence and synchronization |
| lifecycle collection | application outcomes | conflicts, freshness, caching |

Classify the decision, not the class name.

## Use-case checklist

- Does the name describe one operation?
- Are constructor dependencies focused?
- Are call parameters operation-specific?
- Does it add policy, reuse, coordination, or a distinct contract?
- Are output and expected failures explicit?
- Does it leave data ownership in repositories?
- Is it free of UI state, navigation, and Android lifecycle?

## ViewModel, use case, or repository?

- ViewModel: screen state, actions, presentation, UI-owned scope.
- Use case: reusable rule, complex operation, repository coordination.
- Repository: data ownership, source selection, persistence, synchronization.

Direct ViewModel-to-repository calls are valid when the operation is simple.

## Dependency rules

```text
UI → optional Domain → Data contracts / repositories
```

- No circular dependency.
- No DAO, Retrofit service, file, or platform source in a use case.
- No mandatory Gradle module, Clean Architecture template, or DI framework.
- Prefer explicit constructor dependencies.

## Suspend and Flow

- `suspend`: finite action or calculation with suspending collaborators.
- `Flow`: observable application data that can change.
- Caller owns scope, collection, and lifecycle.
- Use case remains cancellation-cooperative.
- Never hide work in `GlobalScope` or an unmanaged private scope.

## Models and failures

- Add a Domain model only when its contract differs meaningfully.
- Do not copy identical models mechanically.
- Represent expected application outcomes explicitly.
- Do not require a universal `Result` wrapper.
- Do not swallow failures the caller must handle.

## Testing checklist

- pure rule cases;
- success and expected rejection;
- repository failure behavior;
- multi-repository coordination;
- Flow changes;
- cancellation;
- fakes instead of Android framework setup.

## Common smells

- one use case per repository method;
- pass-through wrappers;
- giant `AppUseCases`;
- unrelated operations in one class;
- `Context` or lifecycle types in Domain code;
- direct DAO or Retrofit access;
- duplicated rules;
- hidden scopes;
- use case owns UI state or navigation.

## Interview-ready summary

The Domain layer is optional. Add it when a focused application operation owns
complex, reused, or multi-repository logic. Use cases depend on repository
contracts, remain framework-independent, and expose contracts that match the
operation. ViewModels keep UI state and lifecycle ownership; repositories keep
data ownership and source policy.
