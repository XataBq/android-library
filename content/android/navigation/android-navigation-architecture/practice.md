# Android Navigation Architecture — Practice

Complete each exercise with a short design explanation, representative Kotlin,
and focused tests. Full production code is not required.

## Exercise 1 — Refactor navigation ownership

### Goal

Remove framework navigation from a ViewModel without losing the asynchronous
checkout decision.

### Scenario

`CheckoutViewModel` stores a `NavController`. After `placeOrder()` succeeds it
navigates to a receipt. Rotation sometimes opens two receipts, and a unit test
requires Android navigation infrastructure.

### Constraints

- Repository and use case must return data or business outcomes only.
- ViewModel may expose presentation state or an explicitly governed effect.
- UI must own the current `NavController`.
- Define loss, replay, duplicate, and acknowledgement behavior.
- Pass only the new order ID.
- Preserve cancellation with the ViewModel owner.

### Expected deliverable

- an ownership diagram before and after;
- revised ViewModel and UI boundary signatures;
- a reasoned choice between direct callback, best-effort effect, and pending
  acknowledged effect;
- tests for success, failure, recreation, and duplicate collection.

### Evaluation criteria

- no Android UI object crosses into ViewModel or lower layers;
- navigation occurs exactly according to the stated policy;
- order data remains repository-owned;
- the test distinguishes presentation decision from graph execution.

## Exercise 2 — Design a checkout graph and its stack

### Goal

Define history and ViewModel scope for cart, address, payment, confirmation,
and login detour.

### Scenario

Checkout shares an editable draft across three destinations. After successful
payment, Back must not return to payment. A signed-out user must authenticate
and resume only a validated checkout destination.

### Constraints

- Draw the root and nested graphs.
- Select destination, graph, or Activity scope for each piece of state.
- Specify `popUpTo`, `inclusive`, and `launchSingleTop` behavior.
- Explain Back and Up from every step.
- Do not treat the graph as an automatic domain or security boundary.
- Explain what is restored after process recreation.

### Expected deliverable

- graph and stack diagrams for happy path and auth detour;
- scope/lifetime table;
- representative route and stack-option code;
- tests for payment completion, auth cancellation, Back, Up, and recreation.

### Evaluation criteria

- graph-scoped state ends when checkout leaves the stack;
- authoritative cart and order data remain in repositories;
- clearing behavior cannot reopen completed payment;
- deep-link resume is validated and authorized.

## Exercise 3 — Preserve bottom-navigation histories

### Goal

Implement and test three top-level destinations with independent histories.

### Scenario

Explore opens a product detail, Profile opens settings, and Inbox opens a
conversation. Switching tabs currently creates duplicate root destinations and
loses each detail screen.

### Constraints

- Use the installed AndroidX Navigation API style.
- Apply `saveState`, `restoreState`, and single-top behavior deliberately.
- Define active-tab reselect behavior.
- Set a high-level memory policy for deep retained histories.
- Do not add a global event bus or mirror all stacks in ViewModel state.

### Expected deliverable

- before/after stack traces;
- representative top-level navigation code;
- rationale for reselect and history limits;
- tests for switching, reselecting, Back, and duplicate prevention.

### Evaluation criteria

- each top-level destination preserves the intended history;
- reselect behavior is deterministic;
- no duplicate root or parallel controller ownership appears;
- version-sensitive API assumptions are documented.

## Exercise 4 — Secure an external order route

### Goal

Design a verified App Link entry that remains safe under parameter tampering,
missing data, sign-out, and process recreation.

### Scenario

`https://example.test/orders/{orderId}` opens an order detail. The current
implementation trusts any path value and considers a matching App Link proof
that the caller may read the order.

### Constraints

- Validate URI structure and the bounded ID format.
- Separate link verification, authentication, and authorization.
- Keep sensitive data out of the URL.
- Define behavior for unsupported route versions and missing orders.
- Choose how a validated pending destination survives an auth flow.
- Reload order data from a Repository.
- Audit the exported Activity and its intent filters.

### Expected deliverable

- threat and trust-boundary table;
- parser, entry-decision, and route types;
- manifest review notes;
- tests for valid, malformed, unauthorized, deleted, and signed-out cases;
- a recreation test using only small saved inputs.

### Evaluation criteria

- route matching never substitutes for authorization;
- invalid input is rejected before navigation;
- internal-only destinations cannot be reached externally;
- repository data, navigation state, and saved inputs keep distinct owners.
