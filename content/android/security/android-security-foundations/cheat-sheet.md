# Android Security Foundations — Cheat Sheet

## Core review loop

```text
assets → entry point → trust boundary → validate → authenticate → authorize
       → minimize retained/exposed data → test negative paths
```

Name the security goal, attacker capability, control, limit, failure behavior,
and residual-risk owner.

## Threat-model checklist

- Name assets and confidentiality, integrity, availability, and privacy goals.
- List entry points, actors, capabilities, and externally controlled values.
- Draw process, OS, storage, network, SDK, server, and human trust boundaries.
- Write concrete abuse cases and rank likelihood/impact.
- Choose preventive, detective, and recovery controls.
- Record negative tests, assumptions, residual risk, and owners.

## Trust-boundary checklist

- What identity or origin evidence arrives?
- Which values remain attacker-controlled?
- Is shape/size/freshness validated before side effects?
- Where is the principal authenticated?
- Where are subject, action, resource, and current state authorized?
- What data crosses, persists, logs, backs up, or leaves through UI?
- How does denial, tamper, cancellation, restore, or outage fail?

## Identity and policy

| Mechanism | What it establishes | What it does not establish |
| --- | --- | --- |
| authentication | principal identity to stated confidence | permission for every action/resource |
| authorization | whether this principal may do this action now | operating-system capability grant |
| Android permission | access to an OS capability | business/resource authorization |
| biometric/device credential | local user presence or key-use gate | remote account identity/authorization |
| verified App Link | domain-to-app association | trusted parameters, session, resource access |
| integrity verdict | app/device/environment risk signal | user or resource authorization |
| obfuscation | reverse-engineering friction | secrecy or access control |

Enforce protected server operations on the server for every request.

## Components, intents, and links

- Set `android:exported` explicitly.
- Export only a documented IPC/link use case.
- Add a narrow permission where caller identity warrants it.
- Validate action, URI, extras, flags, clip data, sizes, ranges, and formats.
- Treat attacker-controlled `content://` data as untrusted bytes.
- Never infer caller authenticity from an Intent string.
- App Links reduce handler ambiguity; route input and authorization remain.
- Inspect and test the merged release manifest.

## Permissions

- Prefer system picker or narrow API over broad access.
- Declare only capabilities the feature needs.
- Request in context, not mechanically at startup.
- Check again at the operation boundary.
- Handle denial, “don’t ask again,” revocation, auto-reset, missing hardware,
  and version-specific behavior.
- Permission denial and business authorization denial are different states.

## Storage and cryptography

| Data | Default location/policy | Extra questions |
| --- | --- | --- |
| access credential | minimum-lived private session storage | scope, expiry, redaction, logout |
| refresh credential | narrow private storage; server rotation/revocation | restore, theft, concurrent refresh |
| app-only sensitive file | internal app-specific storage | retention, backup, encryption, deletion |
| deliberately shared document | user-mediated shared destination/URI | grants, validation, expiry |
| temporary sensitive data | internal cache/temp with owned cleanup | failure, cancellation, eviction |
| cryptographic key | Android Keystore | hardware capability, invalidation, rotation |

- Classify sensitivity, sharing, retention, backup, restore, and deletion.
- Use internal app-specific storage for app-only sensitive data.
- Validate data read from shared or externally modifiable locations.
- Store cryptographic keys—not arbitrary secret blobs—in Android Keystore.
- Hardware backing and key restrictions depend on configuration/device.
- Plan key invalidation, rotation, migration, and unrecoverable ciphertext.
- Use authenticated encryption and a versioned envelope.
- Encryption at rest does not protect plaintext in process, UI, logs, backups,
  clipboard, or notifications.
- Secrets embedded in APK/resources/native code remain extractable.

## Network and sessions

- Require HTTPS for sensitive traffic.
- Preserve system certificate and hostname validation.
- Disable cleartext deliberately with Network Security Configuration.
- Keep debug CAs out of release artifacts.
- Pinning is an exceptional, threat-model-approved control and is not generally
  recommended by current Android guidance. If approved: backup pins, rotation,
  expiry, monitoring, staged rollout, and recovery.
- Redact authorization, cookies, tokens, URLs, bodies, and personal data.
- Keep access tokens scoped/short-lived where supported.
- Treat refresh credentials as highly sensitive.
- Bound and single-flight concurrent refresh.
- Logout clears local session/caches and invokes server revocation when
  supported.
- TLS and token presence do not replace resource authorization.

## WebView

- Prefer browser/Custom Tab for untrusted content.
- Allowlist controlled HTTPS origins and validate navigation.
- Disable JavaScript, file/content access, and mixed content unless required.
- Never expose a native bridge to untrusted or navigable content.
- Keep WebView patched and define cache/history cleanup.

## Leakage and lifecycle

- Do not place secrets/PII in logs, analytics, crash reports, URLs, or support
  payloads.
- Treat `FLAG_SECURE` as defense in depth, not absolute capture prevention.
- Avoid clipboard for secrets; a sensitive flag hides previews, not the value.
- Use redacted/private/secret notification content and remember user policy wins.
- Give temp/exported files narrow grants, expiry, and cleanup.
- Exclude tokens, device-bound ciphertext, and unsafe state from backup.
- After restore, reauthenticate and reconcile server/device-bound state.

## Build, dependency, and integrity

- Restrict dependency repositories and review new plugins/transitives.
- Patch and scan dependencies; remove unused ones.
- Verify checksums/signatures from a trusted baseline.
- Protect signing keys and separate debug/release endpoints/configuration.
- Inspect release permissions, manifest, network config, and debug flags.
- Bind integrity requests to the protected action; verify verdict and freshness
  on the server; use tiered risk response.
- Integrity signals and obfuscation are not authorization.

## Negative test matrix

- component: exported/non-exported, permission, hostile/missing/large extras;
- link: association, parser, unauthenticated state, unauthorized resource;
- permission: denial, revocation, auto-reset, version variants;
- storage: file location/mode, cleanup, backup/restore, logout;
- crypto: invalidation, tamper, migration, unavailable key;
- network: cleartext, bad certificate/hostname, debug CA isolation;
- session: expiry, revocation, concurrent refresh, restore, logout;
- WebView: off-origin navigation, file/content access, bridge exposure;
- leakage: logs, analytics, crash reports, clipboard, recents, screenshots,
  notifications, temp files;
- supply chain: merged release artifact and dependency verification failure.

## Review questions

1. Which assets and goals matter?
2. Which actors control each input?
3. Where are trust boundaries crossed?
4. What validates shape, authenticity, and freshness?
5. Who authenticates and who authorizes the exact resource action?
6. Is exposure, permission, collection, retention, and logging minimized?
7. What happens on denial, cancellation, tamper, restore, and outage?
8. Which negative tests and operational recovery prove the intended control?
9. Which assumptions and residual risks have named owners?

## Common smells

- authorization performed only in UI;
- broad exported components, permissions, storage, or SDK collection;
- Intent or deep-link values used before parsing;
- App Links, biometrics, integrity, or obfuscation described as authorization;
- APK-embedded authoritative secrets;
- trust-all TLS, permissive hostname checks, or release debug CA;
- one permanent certificate pin without recovery;
- arbitrary WebView content with native bridges;
- tokens or personal data in logs, URLs, analytics, crash reports, or alerts;
- encryption without key, nonce, migration, plaintext, and recovery policy;
- backup, restore, logout, and release artifact left untested.

## Interview-ready summary

Android security is layered risk reduction. Name assets and boundaries, minimize
component and permission exposure, validate external input, authenticate the
principal, authorize each protected resource action at the trusted service,
minimize retained and observable data, preserve platform TLS, use Keystore and
biometrics only for their actual guarantees, harden WebView and release inputs,
and test negative paths in the packaged artifact. App Links, integrity signals,
obfuscation, encryption, and biometrics never replace authorization.
