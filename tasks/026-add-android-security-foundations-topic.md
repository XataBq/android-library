# Task 026 — Add Android Security Foundations Topic

Status: DONE

## Objective

Add the fourteenth production educational topic in the Junior Core:

```text
android-security-foundations
```

The topic must explain Android application security as layered risk reduction across components, data, network communication, storage, permissions, authentication, authorization, and build configuration.

The learner must understand:

- threat modeling;
- trust boundaries;
- exported components;
- intents and deep links;
- permissions;
- authentication versus authorization;
- secure local storage;
- secrets;
- WebView risks;
- network security;
- logging and analytics;
- backups;
- screenshots and clipboard;
- dependency and build risks;
- testing and review practices.

This task belongs to:

```text
Phase 3 — Learning Content MVP
Junior Core target: 17 mandatory topics
```

The new package must remain in `review`.

It builds on:

- Architecture Foundations;
- Data Layer and Repositories;
- Lifecycle and State Restoration;
- Navigation Architecture;
- Networking Architecture;
- Dependency Injection and Scoping;
- Testing Foundations.

---

## Core teaching position

Security is not one API, one library, or one final audit.

The core model is:

```text
identify asset
→ identify entry point
→ identify trust boundary
→ validate input
→ authenticate identity
→ authorize action
→ minimize exposure
→ detect and test failure modes
```

The topic must preserve these distinctions:

```text
authentication
≠ authorization

encryption
≠ access control

verified App Link
≠ trusted request

private app storage
≠ protection from a compromised device

obfuscation
≠ secret storage
```

---

## Source-of-truth requirements

Before authoring, inspect:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CONTENT_MODEL.md`
- `docs/CONTENT_VALIDATION.md`
- `docs/EDITORIAL_PACKAGE_LIFECYCLE.md`
- all content-authoring documentation;
- canonical Android architecture competencies;
- imported Android Developers source packages;
- all production topics;
- Tasks 016–025.

Use current official or primary documentation for:

- Android app security best practices;
- component exporting;
- intents and intent filters;
- permissions;
- network security configuration;
- WebView security;
- app data storage;
- Keystore;
- encrypted storage guidance where current;
- backups;
- screenshots and secure windows;
- Play Integrity only as a version-sensitive advanced boundary;
- dependency and supply-chain guidance;
- security testing.

Do not fabricate platform guarantees.

Do not fabricate access dates.

Clearly distinguish:

- stable security principles;
- platform-version behavior;
- library-specific APIs;
- defense-in-depth controls;
- advanced hardening options.

---

## Canonical competency scope

Primary:

```text
isolate-android-framework-dependencies
explain-android-component-lifecycle-constraints
apply-separation-of-concerns
```

Strongly reinforced:

```text
design-data-layer-around-repositories
explain-ui-layer-responsibilities
design-viewmodel-ui-state
```

Contextually reinforced:

```text
use-coroutines-and-flows-across-layers
explain-persistent-data-models
```

Do not modify competency files.

Do not create a production competency-to-topic mapping.

---

## Package location

Create exactly:

```text
content/android/security/android-security-foundations/
├── topic.yaml
├── theory.md
├── cheat-sheet.md
├── practice.md
├── interview.md
└── test.yaml
```

No additional package files.

Use schema-valid taxonomy. If `section: security` is invalid, adapt using repository conventions and document the choice.

---

## Topic metadata

Preferred metadata:

```yaml
id: android-security-foundations
title: Android Security Foundations
track: android
section: security
difficulty: foundation
status: review
estimated_minutes: 240
content_version: 1
prerequisites:
  - android-app-architecture-foundations
  - android-data-layer-repositories-and-synchronization
  - android-lifecycle-and-state-restoration
  - android-navigation-architecture
  - android-networking-architecture
  - android-dependency-injection-and-scoping
  - android-testing-foundations
```

Adapt only where required by the actual schema.

---

## Required learning outcomes

The topic must cover outcomes equivalent to:

1. Explain assets, threats, attack surfaces, and trust boundaries.
2. Perform a basic feature-level threat model.
3. Distinguish authentication from authorization.
4. Treat external input as untrusted.
5. Configure exported components deliberately.
6. Validate intents, deep links, and URI inputs.
7. Use permissions with least privilege.
8. Distinguish normal, runtime, signature, and special permissions at a practical level.
9. Protect sensitive local data.
10. Use Android Keystore appropriately.
11. Explain why app secrets cannot be safely hidden in an APK.
12. Secure network communication and certificate validation.
13. Recognize WebView risks.
14. Prevent sensitive data leakage through logs, analytics, clipboard, screenshots, backups, and notifications.
15. Explain secure token/session handling.
16. Explain biometric authentication as a user-presence control, not universal authorization.
17. Understand integrity and tamper signals as risk inputs, not absolute trust.
18. Recognize dependency and supply-chain risks.
19. Test security-sensitive paths.
20. Apply defense in depth without false guarantees.

---

## Theory requirements

`theory.md` must contain approximately 22–26 substantial sections.

Required coverage:

### 1. Security goals

Explain:

- confidentiality;
- integrity;
- availability;
- privacy;
- authenticity;
- accountability at a high level.

### 2. Assets, threats, and attack surface

Define:

- asset;
- attacker capability;
- entry point;
- attack surface;
- trust boundary.

### 3. Basic threat modeling

Teach a lightweight workflow:

```text
What is valuable?
Who can access the feature?
What external input enters?
What component crosses trust boundaries?
What happens if data is changed, replayed, leaked, or unavailable?
```

Do not require a full enterprise methodology.

### 4. Defense in depth

Explain why one control is insufficient.

### 5. Authentication versus authorization

Use concrete examples:

- signed-in user;
- account ownership;
- admin action;
- resource-level authorization.

### 6. Android sandbox

Explain:

- per-app UID;
- private app data;
- process isolation;
- limitations on rooted/compromised devices;
- shared/external surfaces.

Avoid claiming the sandbox makes application data absolutely secure.

### 7. Exported components

Cover:

- Activity;
- Service;
- BroadcastReceiver;
- ContentProvider;
- explicit `android:exported`;
- intent filters;
- internal-only components;
- permission-protected components.

### 8. Intent validation

Explain:

- extras;
- action;
- data URI;
- caller assumptions;
- explicit versus implicit intents;
- malformed or missing values;
- replay and duplicate actions.

### 9. Deep links and App Links

Explain:

- verified origin does not validate route parameters;
- auth gates;
- authorization;
- allowlisted routes;
- sensitive information in URLs;
- safe fallback.

### 10. Permissions and least privilege

Cover:

- only request what is required;
- request at point of need;
- degrade gracefully;
- denial and revocation;
- permission is not business authorization.

### 11. Permission categories

At a practical level distinguish:

- normal;
- dangerous/runtime;
- signature;
- special access.

Be version-aware and avoid exhaustive permission memorization.

### 12. Local data storage

Compare:

- internal files;
- preferences/data store;
- database;
- cache;
- external/shared storage.

Explain sensitivity, retention, deletion, and access scope.

### 13. Android Keystore

Explain:

- key material can be non-exportable;
- key generation and use;
- hardware-backed availability is device-dependent;
- key invalidation;
- authentication-bound keys;
- Keystore stores keys, not arbitrary large data.

### 14. Encryption at rest

Explain:

- what encryption protects;
- what it does not protect;
- key management;
- backups;
- logged/decrypted data;
- compromised process limitations.

Do not prescribe obsolete encrypted-storage APIs as universal defaults.

### 15. Secrets in applications

Explain why these are not secure secrets:

- API keys embedded in code;
- BuildConfig values;
- resources;
- native libraries;
- obfuscation.

Explain backend mediation and scoped credentials.

### 16. Network security

Cover:

- HTTPS;
- certificate chain;
- hostname verification;
- cleartext policy;
- Network Security Config;
- safe debug overrides;
- no disabling TLS validation.

### 17. Certificate pinning

Explain:

- possible protection;
- operational risk;
- rotation;
- backup pins;
- outage risk;
- not a universal default.

### 18. Session and token handling

Cover:

- access token lifetime;
- refresh token sensitivity;
- logout invalidation;
- replay;
- storage;
- redaction;
- concurrent refresh;
- server-side authorization.

### 19. Biometrics and device credentials

Explain:

- user presence/local gate;
- CryptoObject boundary where relevant;
- biometric success does not grant server authorization by itself;
- fallback and enrollment changes;
- version-sensitive APIs.

### 20. WebView security

Cover:

- JavaScript;
- untrusted content;
- JavaScript interfaces;
- file access;
- URL allowlisting;
- mixed content;
- navigation override;
- cookies/session;
- external browser preference where appropriate.

### 21. Data leakage

Cover:

- logs;
- analytics;
- crash reports;
- clipboard;
- screenshots;
- recents thumbnails;
- notifications;
- exported files;
- temporary files.

### 22. Backup and restore

Explain:

- sensitive data in backups;
- auto backup/data extraction rules;
- device-to-device transfer;
- token/session invalidation;
- restore-time assumptions.

### 23. Build, dependencies, and supply chain

Cover:

- dependency updates;
- transitive dependencies;
- repository trust;
- checksum/signature concepts at a high level;
- debug flags;
- signing configuration;
- release build review;
- no production debug endpoints.

### 24. Integrity and tamper signals

Explain:

- Play Integrity or equivalent signals;
- version/device constraints;
- server verification;
- risk scoring;
- no absolute guarantee;
- do not block legitimate users blindly without policy.

### 25. Security testing

Cover:

- manifest review;
- exported component tests;
- deep-link tests;
- authorization tests;
- malformed input;
- storage inspection;
- logging checks;
- WebView tests;
- network configuration tests;
- negative-path testing;
- static/dependency scanning at a high level.

### 26. Anti-patterns and decision guide

At minimum:

- trusting deep-link parameters;
- exported Activity without validation;
- permission treated as authorization;
- secrets in APK;
- disabled hostname verification;
- universal certificate pinning without rotation;
- tokens in logs;
- sensitive data in notifications;
- Activity Context in singleton;
- WebView JavaScript bridge for untrusted content;
- storing refresh token in plain shared storage without threat analysis;
- trusting client-side role flags;
- relying only on obfuscation;
- assuming biometric success equals account authorization;
- accepting all intents;
- leaving debug endpoints in release;
- storing sensitive data in backups unintentionally.

End with:

```text
What asset is protected?
Where does untrusted input enter?
Who authenticates the caller?
Who authorizes the action?
What is exposed outside the app?
Where is sensitive data stored or copied?
What happens on a compromised device?
How is the failure path tested?
```

---

## Kotlin/XML example requirements

Include at least:

1. non-exported Activity declaration;
2. permission-protected exported component;
3. intent validation;
4. deep-link route validation;
5. resource-level authorization boundary;
6. runtime permission request flow;
7. safe denial handling;
8. internal storage example;
9. Keystore key creation/use sketch;
10. encryption wrapper boundary;
11. secret-in-APK anti-pattern;
12. Network Security Config;
13. safe debug network override;
14. token redaction;
15. biometric-bound key use sketch;
16. WebView hardened configuration;
17. screenshot protection example;
18. safe notification content;
19. backup-rule example;
20. exported-component test;
21. deep-link authorization test;
22. log-leak test or audit helper.

Examples must be conceptually compilable and version-aware.

Do not present obsolete APIs as universal recommendations.

---

## Cheat-sheet requirements

`cheat-sheet.md` must be independently useful and include:

- threat-model checklist;
- trust-boundary checklist;
- authentication versus authorization;
- exported-component rules;
- intent/deep-link validation;
- permission rules;
- storage sensitivity matrix;
- Keystore rules;
- secrets guidance;
- TLS/network checklist;
- token/session checklist;
- WebView checklist;
- leakage checklist;
- backup checklist;
- release-build checklist;
- testing checklist;
- common smells;
- interview-ready summary.

---

## Practice requirements

`practice.md` must contain exactly 4 exercises.

### Exercise 1 — Exported component review

Review an exported Activity and BroadcastReceiver that accept extras from other apps.

Require:

- entry-point classification;
- caller assumptions;
- validation;
- authorization;
- permissions;
- negative tests.

### Exercise 2 — Deep-link payment flow

Review a deep link that opens a payment confirmation screen.

Require:

- route validation;
- authentication;
- resource authorization;
- replay handling;
- sensitive URL data review;
- safe fallback.

### Exercise 3 — Sensitive local data

Design storage for access token, refresh token, user profile cache, downloaded document, and encryption key.

Require:

- sensitivity classification;
- lifetime;
- storage location;
- backup policy;
- deletion/logout behavior;
- compromised-device limitations.

### Exercise 4 — WebView and release audit

Review a feature with JavaScript, JavaScript interface, file access, debug logging, and a development endpoint.

Require:

- hardening changes;
- release-build controls;
- domain allowlist;
- token/cookie handling;
- tests.

Each exercise must include:

- goal;
- scenario;
- constraints;
- expected deliverable;
- evaluation criteria;
- optional hints.

Do not provide complete final solutions.

---

## Interview requirements

`interview.md` must contain approximately 22–26 substantial questions.

Cover:

- threat modeling;
- sandbox;
- exported components;
- intents;
- deep links;
- authentication;
- authorization;
- permissions;
- storage;
- Keystore;
- encryption;
- app secrets;
- HTTPS;
- Network Security Config;
- pinning;
- tokens;
- biometrics;
- WebView;
- logs/analytics;
- screenshots/clipboard/notifications;
- backups;
- dependencies/build;
- integrity signals;
- testing;
- anti-patterns.

Each question must include:

- strong-answer criteria;
- weak or misleading answers;
- follow-ups where useful.

---

## Test requirements

`test.yaml` must contain exactly 10 reasoning-focused questions.

Required coverage:

1. threat modeling;
2. exported component;
3. deep-link validation;
4. authentication versus authorization;
5. permissions;
6. storage and Keystore;
7. secrets in APK;
8. TLS/pinning;
9. WebView/data leakage;
10. security testing and defense in depth.

Distractors must be plausible.

Explanations must teach risk boundaries, not security slogans.

---

## References

Use current primary sources.

At minimum inspect:

- Android app security best practices;
- manifest and exported components;
- intents;
- permissions;
- data storage;
- Android Keystore;
- network security configuration;
- WebView security;
- backups/data extraction rules;
- biometric guidance;
- integrity guidance where referenced;
- security testing guidance.

Follow repository metadata conventions.

Do not fabricate access dates.

---

## Relationship to Junior Core

This is mandatory Junior Core topic 14 of 17.

The implementation report must record:

```text
Junior Core status after Task 026:
14 of 17 mandatory topics implemented as production packages in review.
3 mandatory topics remain.
```

Remaining mandatory topics:

15. Local Persistence with Room
16. Background Work and WorkManager
17. Compose Foundations

Do not define the Junior/Middle boundary yet.

---

## Project documentation updates

Update:

- `README.md`;
- `docs/PROJECT_STATE.md`;
- `docs/ROADMAP.md`.

Required updates:

- record Task 026 after successful validation;
- record fourteen production topics in `review`;
- keep Phase 3 current;
- preserve Phase 2 completion;
- maintain the 17-topic Junior Core target;
- state that three topics remain;
- do not create mappings or catalog output;
- do not promote existing topics.

Update `docs/ARCHITECTURE.md` only if explicit counts or lists become stale.

---

## Implementation report

Create the repository-standard implementation report including:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. threat-model and trust-boundary audit;
5. component/intent/deep-link audit;
6. permission/storage/Keystore audit;
7. network/session/biometric audit;
8. WebView/leakage/backup audit;
9. build/dependency/integrity audit;
10. security-testing audit;
11. Junior Core progress audit;
12. exact counts;
13. validation;
14. UTF-8/mojibake audit;
15. deferred work;
16. literal `git status --short`;
17. recommended commit message.

---

## Validation

Run:

```bash
python -B scripts/validate_content.py
python -B scripts/validate_competencies.py
python -B -m unittest discover
git diff --check
```

Also verify:

- exactly six package files;
- exactly four exercises;
- exactly ten tests;
- interview count in range;
- schema-valid taxonomy;
- prerequisites exist;
- no prerequisite cycle;
- no changes to existing topic packages;
- no source, competency, sequence, mapping, schema, validator, or test-infrastructure changes;
- UTF-8;
- no mojibake;
- no local absolute paths.

---

## Acceptance criteria

- Six-file package exists.
- Status is `review`.
- Content version is `1`.
- Security is explained through assets, threats, entry points, and trust boundaries.
- Authentication and authorization are distinct.
- Exported components and external input are handled safely.
- Permission guidance follows least privilege.
- Storage and Keystore guidance is accurate.
- Secrets-in-APK limitations are explicit.
- TLS guidance is safe.
- Pinning is presented cautiously.
- WebView risks are covered.
- Leakage, backup, and release-build risks are covered.
- Security testing is practical.
- Practice has exactly 4 exercises.
- Test has exactly 10 questions.
- Junior Core progress is updated to 14/17.
- Documentation is synchronized.
- All validations pass.

---

## Expected Codex response

Return:

1. implementation summary;
2. changed files;
3. source/evidence audit;
4. threat-model/trust-boundary audit;
5. component/input/permission audit;
6. storage/Keystore/secrets audit;
7. network/session/WebView audit;
8. leakage/build/testing audit;
9. Junior Core progress;
10. exact counts;
11. validation results;
12. UTF-8 audit;
13. deferred work;
14. literal `git status --short`;
15. recommended commit message.

Do not commit.
