# Practice — Android Security Foundations

## Exercise 1 — Exported component review

### Goal

Review and harden an exported Activity and BroadcastReceiver that accept data
from other applications.

### Scenario

`PartnerImportActivity` accepts a document URI, account ID, and display name.
`SyncReceiver` accepts an action, account ID, and force-refresh flag. Both are
exported without a permission, trust every extra, and start account work before
checking the current session.

### Constraints

- Classify both operating-system entry points and the protected assets.
- State which fields an external caller can control.
- Reject assumptions based only on Intent action, package-shaped extras, or
  component name.
- Define allowlisted actions, typed parsing, URI grants, size/range limits, and
  malformed-input behavior.
- Decide whether each component should remain exported.
- If export is required, evaluate a signature permission or another documented
  caller contract without treating it as resource authorization.
- Require authentication and server-side account/resource authorization before
  sensitive work.
- Add negative tests for unauthorized callers, missing/malformed/oversized
  extras, revoked URI access, locked-out session, and denied resource access.
- Inspect the merged release manifest.

### Expected deliverable

A compact threat model, revised manifest and parser skeletons, authorization
flow, and component-focused negative-test table.

### Evaluation criteria

- entry points, assets, callers, and trust boundaries are explicit;
- exposure is minimized and justified;
- validation happens before side effects;
- permission and product authorization remain distinct;
- failure reveals no protected account data;
- tests target the packaged component contract.

### Optional hints

- An explicit Intent identifies the destination, not a trustworthy sender.
- A permission can narrow callers while request data still needs validation.

## Exercise 2 — Deep-link payment flow

### Goal

Review a deep link that opens a payment confirmation flow without allowing an
external request to authorize or replay a payment.

### Scenario

The app accepts
`https://pay.example.com/confirm/{paymentId}?amount=...&token=...&returnTo=...`.
It displays the amount from the URL, performs payment on screen open, and
assumes a verified App Link proves that the current user owns the payment.

### Constraints

- Validate an allowlisted scheme, host, path, payment ID, parameter count, and
  decoded length before navigation.
- Remove sensitive credentials and authoritative amounts from URLs.
- Establish current authentication separately from link association.
- Require the server to authorize subject, action, payment resource, amount,
  state, and expiry.
- Define one-time operation identity or another server-owned replay policy.
- Remove or strictly allowlist `returnTo` to prevent an open redirect.
- Provide safe fallbacks for malformed link, signed-out user, expired payment,
  replay, unauthorized resource, network failure, and unknown route.
- Test App Link association separately from parsing and authorization.
- Do not use biometrics, App Link verification, or an integrity verdict as
  payment authorization.

### Expected deliverable

A link contract, navigation/authentication state flow, server authorization and
replay boundary, sensitive-data review, and negative-test matrix.

### Evaluation criteria

- no URL value becomes authoritative without server validation;
- association, parsing, authentication, authorization, and replay are separate;
- opening a link never performs payment automatically;
- fallbacks leak no payment details;
- redirects are constrained;
- tests cover malicious and stale links.

### Optional hints

- Let the link identify a pending operation, then ask the trusted service for
  its current authorized state.
- Confirmation and execution can require distinct server operations.

## Exercise 3 — Sensitive local data

### Goal

Design storage for an access token, refresh token, user profile cache,
downloaded document, and encryption key.

### Scenario

A prototype stores every value in one preference file, embeds an encryption
password in `BuildConfig`, includes all data in backup, and leaves files after
logout.

### Constraints

- Classify every value by sensitivity, lifetime, sharing, recoverability, and
  compromised-device impact.
- Choose the minimum required local retention and storage location.
- Treat access and refresh token scope, expiry, rotation, redaction, and server
  revocation separately.
- Use Android Keystore for cryptographic keys, not arbitrary token strings.
- Define authenticated-encryption envelope, key invalidation, migration, and
  unrecoverable-ciphertext behavior where encryption is justified.
- Explain why a `BuildConfig`, resource, native, encoded, or obfuscated secret
  remains extractable.
- Define backup exclusions and restore reauthentication.
- Define logout/account-removal and temporary/partial-document cleanup.
- State the limits on rooted/compromised devices and plaintext inside the app
  process.

### Expected deliverable

A sensitivity and lifetime matrix, storage/key boundary diagram, backup rules,
logout/restore sequence, and failure-test plan.

### Evaluation criteria

- each value has a justified owner, location, and retention period;
- collection and storage are minimized before encryption;
- keys, ciphertext, and session credentials are distinct;
- backup, restore, invalidation, and deletion behavior is explicit;
- no embedded authoritative secret remains;
- compromised-device limitations are honest.

### Optional hints

- Recovery policy is part of cryptographic design.
- A downloaded user document and a short-lived cache may need different
  persistence and sharing contracts.

## Exercise 4 — WebView and release audit

### Goal

Review a feature with JavaScript, a JavaScript interface, file access, debug
logging, and a development endpoint.

### Scenario

A support Activity loads an arbitrary URL into WebView, enables JavaScript,
adds an account-capable native bridge, enables file/content access, logs cookies
and headers, and uses a development CA and endpoint that can reach a release
variant.

### Constraints

- Decide whether a browser or Custom Tab can replace WebView.
- If WebView remains, allowlist controlled HTTPS origins and navigation.
- Disable JavaScript, native bridge, file/content access, and mixed content
  unless a narrowly documented requirement survives review.
- Define token/cookie boundaries, cache/history cleanup, downloads, popups, and
  external navigation behavior.
- Restore platform TLS validation and disable cleartext in release.
- Isolate the development endpoint, CA, logging, and debuggability to
  non-release variants.
- Inspect the packaged release manifest and Network Security Configuration.
- Redact logs, analytics, crash reports, and support attachments.
- Test off-origin content, script/bridge access, file URLs, invalid
  certificates/hostnames, cleartext, and release-build isolation.

### Expected deliverable

A before/after threat-boundary diagram, WebView decision and configuration,
release-build controls, domain allowlist, token/cookie policy, and test matrix.

### Evaluation criteria

- untrusted web content cannot reach native account capabilities;
- unused WebView features are disabled;
- development trust/configuration cannot reach release;
- observability contains no secrets or personal data;
- failure behavior is safe and diagnosable;
- tests inspect both behavior and packaged configuration.

### Optional hints

- Clearing WebView cache does not repair an unsafe origin or native bridge.
- Debug and release separation should be demonstrated in the built artifact.
