# Task 026 — Android Security Foundations implementation report

## Implementation summary

**PASS**

Task 026 adds the fourteenth production educational topic in `review`. It
teaches Android application security through one repeatable model:

```text
assets → entry point → trust boundary → validate → authenticate → authorize
       → minimize retained/exposed data → test negative paths
```

The topic treats platform controls as layers with explicit guarantees and
limits. App Links, biometrics, integrity verdicts, obfuscation, encryption, and
Android permissions are never presented as resource authorization.

## Changed files

Created the six canonical files under
`content/android/security/android-security-foundations/` and this report.
Updated `README.md`, `docs/ARCHITECTURE.md`, `docs/PROJECT_STATE.md`,
`docs/ROADMAP.md`, and Task 026 status.

No existing topic package, source, competency, learning sequence, mapping,
schema, validator, fixture, or test-infrastructure file changed.

## Source and evidence audit

Both imported Android Developers source packages, the version 2 canonical
Android app architecture competency set, all thirteen preceding production
topics, and the adjacent implementation reports were inspected.

Primary canonical coverage:

- `isolate-android-framework-dependencies`;
- `explain-android-component-lifecycle-constraints`;
- `apply-separation-of-concerns`.

Repository/Data ownership, UI responsibilities, ViewModel state, coroutine and
Flow ownership, navigation input, networking trust, dependency injection, and
testing are reinforced only at their security boundaries. No competency or
production competency-to-topic mapping changed.

Current official Android Developers, Gradle, and OWASP MASVS material was
inspected for application security, component exposure, permissions, App
Links, storage, Keystore, TLS and Network Security Configuration, biometrics,
WebView, leakage channels, backups, Play Integrity, dependency verification,
and mobile security testing. All 22 metadata references are official
documentation or a primary specification and use the actual inspection date
`2026-07-24`.

## Threat-model and trust-boundary audit

The topic defines confidentiality, integrity, availability, privacy,
authenticity, and accountability before choosing controls. Assets, actors,
capabilities, entry points, data flow, trust boundaries, abuse cases,
likelihood/impact, controls, negative tests, assumptions, residual risk, and
owners form the lightweight threat-model loop.

Defense in depth is presented as independently useful exposure minimization,
validation, authentication, authorization, data minimization, detection, and
recovery. The sandbox's UID/process/private-file guarantees are distinguished
from compromised processes/devices, exported entry points, UI leakage,
embedded APK values, and server-side failures.

## Component, Intent, and deep-link audit

Activities, services, receivers, and providers are treated as OS-mediated IPC
entry points. The topic requires explicit export decisions, minimum exposure,
optional narrow caller permissions, merged-manifest inspection, full input
validation, resource authorization, safe failure, and negative tests.

Intent action, data, extras, flags, clip data, nested values, URI grants, sizes,
and content remain untrusted. No string inside an Intent is presented as caller
identity.

Deep links validate allowlisted scheme, host, path, decoded size, identifiers,
and navigation. Verified App Links establish only the domain-to-app
association. Session establishment, route semantics, replay policy, and
server-side resource authorization remain separate boundaries.

## Permission, storage, and Keystore audit

Least privilege prefers system pickers or narrow APIs over broad permissions.
Runtime grants are checked at the operation boundary and denial, revocation,
auto-reset, version variance, and missing capability have explicit fallbacks.
OS permission and product authorization remain separate.

Storage is chosen after sensitivity, sharing, lifetime, backup, restore,
deletion, and recovery classification. Internal app-specific storage is
recommended for app-only sensitive data without claiming protection from a
compromised app process or device.

Android Keystore owns cryptographic keys rather than arbitrary secret blobs.
Non-exportability, use restrictions, device-dependent hardware capabilities,
invalidation, rotation, migration, and recovery are covered. Authenticated
encryption uses a versioned envelope and does not claim to protect plaintext in
process, UI, logs, analytics, clipboard, notifications, or backup. APK,
resource, `BuildConfig`, native, encoded, and obfuscated values are explicitly
extractable; authoritative secrets remain on trusted systems.

## Network, session, and biometric audit

The network baseline preserves HTTPS, platform certificate-chain and hostname
validation, explicit cleartext policy, and debug/release trust separation.
Trust-all managers and hostname acceptance are rejected.

Current Android guidance is reflected accurately: certificate pinning is not a
default recommendation. A justified exception requires a concrete threat
model, backup pins, expiry, rotation rehearsal, monitoring, staged rollout,
recovery, and owners. Pinning remains transport policy, not authorization.

Sessions use server authorization per protected request, scoped and short-lived
access credentials where supported, protected refresh credentials, bounded
single-flight refresh, redaction, revocation, logout cleanup, and restore
reauthentication. Biometric/device credential confirms local user presence or
gates Keystore-backed key use; it does not prove remote identity or resource
authorization.

## WebView, leakage, and backup audit

A browser or Custom Tab is preferred for untrusted web content. A retained
WebView uses controlled HTTPS origins, navigation validation, disabled unused
JavaScript/file/content/mixed-content features, no native bridge to untrusted
content, patching, and deliberate cache/history behavior.

Leakage coverage includes logs, analytics, crash reports, URLs, screen capture,
recents, clipboard, notifications, temporary/exported files, support payloads,
and SDKs. `FLAG_SECURE`, clipboard sensitive marking, and notification
visibility are presented as bounded defense-in-depth controls.

Backup and device transfer are explicit data flows. Version-appropriate rules
exclude tokens, unsafe device-bound ciphertext, caches, and sensitive state.
Restored sessions reauthenticate, server state is reconciled, unusable
ciphertext is handled, and cloud backup/device transfer/logout/account removal
are tested.

## Build, dependency, and integrity audit

The release boundary covers restricted repositories, reviewed plugins and
transitives, updates and vulnerability scanning, dependency checksums and
signatures, signing-key protection, debug/release separation, and inspection
of the packaged manifest, network config, permissions, native libraries, and
debug flags. Verification integrity/provenance does not prove vulnerability
absence; obfuscation only adds reverse-engineering friction.

Play Integrity and similar verdicts are bound to a protected request using the
current request-hash or nonce contract, verified for package/request/freshness
on the server, protected against replay, and used for tiered risk response with
outage and false-positive policy. They remain risk inputs, not authentication
or resource authorization.

## Security-testing audit

Negative-path coverage includes hostile exported components and links,
permission denial/revocation, storage and backup inspection, key invalidation,
invalid TLS and release/debug isolation, session expiry/revocation/logout,
WebView origins, leakage channels, dependency verification, and packaged
release configuration.

Static analysis, dependency scanning, focused unit/instrumented/server tests,
and authorized penetration testing provide complementary evidence. No tool or
happy path is presented as proof that vulnerabilities are absent.

## Junior Core progress audit

Junior Core status after Task 026:
14 of 17 mandatory topics implemented as production packages in review.
3 mandatory topics remain.

The remaining mandatory topics are:

15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

The Junior/Middle boundary remains deferred until the full Junior Core is
implemented and reviewed. No grading schema, production mapping, or catalog
output was introduced.

## Exact counts

- Package files: 6.
- Numbered theory sections: 26.
- Meaningful Kotlin/XML code blocks/categories in theory: 32
  (25 Kotlin, 7 XML).
- Practice exercises: 4.
- Interview questions: 26.
- Test questions: 10.
- Official/primary references: 22.
- Taxonomy: `android` / `security`.
- Difficulty/status/version/time: `foundation` / `review` / 1 / 240 minutes.
- Prerequisites: 7.
- Production topic packages after Task 026: 14.
- Mandatory Junior Core topics remaining: 3.

The taxonomy, metadata, and prerequisites are schema-valid. Every prerequisite
exists and the graph remains acyclic.

## Validation

```text
python -B scripts/validate_content.py
PASS — 14 topic packages, 2 templates, 4 schema fixtures

python -B scripts/validate_competencies.py
PASS — 2 source packages, 1 canonical package, 1 learning-sequence package,
0 competency-to-topic mapping packages, 2 templates, 41 schema fixtures

python -B -m unittest discover
PASS — 107 tests

git diff --check
PASS
```

## UTF-8 and mojibake audit

All new or modified repository Markdown/YAML source files decode as strict
UTF-8 without BOM. They contain none of the checked mojibake sequences. The
new topic and review diff contain no absolute local path.

## Deferred work

The three remaining Junior Core topics, final Junior/Middle boundary review,
human editorial acceptance/publication, production mappings, catalog
generation, CI, clients, learner database, AI tutor, and specialized security
review remain deferred. Dedicated Room, WorkManager, and Compose topics retain
their full content scope.

## Git status

Literal `git status --short` output after generating the review diff:

```text
 M README.md
 A content/android/security/android-security-foundations/cheat-sheet.md
 A content/android/security/android-security-foundations/interview.md
 A content/android/security/android-security-foundations/practice.md
 A content/android/security/android-security-foundations/test.yaml
 A content/android/security/android-security-foundations/theory.md
 A content/android/security/android-security-foundations/topic.yaml
 M docs/ARCHITECTURE.md
 M docs/PROJECT_STATE.md
 M docs/ROADMAP.md
 A docs/reports/task-026-android-security-foundations-implementation.md
 A tasks/026-add-android-security-foundations-topic.md
?? 026-codex-prompt.md
?? 026-review.diff
```

## Recommended commit message

```text
feat(content): add Android security foundations topic
```
