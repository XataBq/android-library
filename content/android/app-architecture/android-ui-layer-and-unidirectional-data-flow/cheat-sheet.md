# Android UI Layer and UDF — Cheat sheet

## Responsibility table

| Responsibility | Owner |
|---|---|
| Render state, capture input | UI element |
| Produce screen state, coordinate UI decisions | State holder |
| Change or reconcile application data | Data / optional Domain |
| Navigate, request permission, launch external UI | Active UI |

## UI element versus state holder

| UI element | State holder |
|---|---|
| `Activity`, `Fragment`, Compose UI, `View` | ViewModel or plain state-owning class |
| Knows framework UI APIs | Avoids longer-lived references to UI instances |
| Consumes state | Produces state |
| Forwards actions | Processes or delegates actions |
| Lifetime follows rendered UI | Lifetime matches element or screen scope |

## UDF cycle

```text
User action → UI event → state holder → application operation
      ↑                                      ↓
UI rendering ←────────── updated state ──────
```

This is a responsibility flow, not a required library or class diagram.

## State classification

- **Source data:** owned by Data.
- **Screen state:** everything needed to render the screen.
- **Derived state:** computed from authoritative inputs.
- **Local element state:** affects one nearby UI element.
- **Restoration input:** minimal value needed to reconstruct state.

Ask: Who reads it? Who changes it? How long must it survive? Can it be recomputed?

## Durable state versus one-time effect

| Durable state | One-time effect |
|---|---|
| Remains true until changed | Requests an interaction once |
| Safe to render again | Replay may be harmful |
| Form text, validation, selected tab | Navigation, picker, permission dialog |
| Requires an owner and transition | Requires owner, timing, replay, acknowledgement semantics |

A critical message may be durable state rather than a lossy effect.

## Warning signs

- Rendering starts network or storage work.
- UI mutates a shared state snapshot.
- Several writable properties can be observed inconsistently.
- Loading, content, and error flags form unexplained combinations.
- A ViewModel holds an `Activity`, `View`, or navigation object.
- Every outcome is sent through a universal one-shot wrapper.
- Configuration survival is mistaken for process survival.

## Screen-state checklist

- [ ] Every representable combination has meaning.
- [ ] Exclusive modes are modeled exclusively where useful.
- [ ] Coexisting conditions remain expressible.
- [ ] Source and derived values cannot drift independently.
- [ ] Rendering is side-effect free.
- [ ] Observation follows the UI lifecycle.
- [ ] Restoration matches product requirements.
- [ ] Local state stays local unless sharing or lifetime requires lifting it.
