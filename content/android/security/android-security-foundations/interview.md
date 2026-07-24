# Android Security Foundations — Interview Questions

## 1. What security goals should an Android feature define?

**Strong answer:** Confidentiality, integrity, availability, privacy,
authenticity, and accountability as applicable, tied to named assets and
failure impact.

**Weak answer:** Security means encrypting every field.

**Follow-up:** Which goals can conflict in an audit-log design?

## 2. What belongs in a lightweight threat model?

**Strong answer:** Assets, entry points, actors and capabilities, trust
boundaries, abuse cases, likelihood/impact, controls, negative tests, residual
risk, and owners.

**Weak answer:** A list of every theoretical attack with no product context.

## 3. What does defense in depth mean?

**Strong answer:** Independent controls reduce different failure paths:
minimized exposure, validation, authentication, authorization, data
minimization, detection, and recovery. Each control's limits remain explicit.

**Weak answer:** Add enough client checks and the server can trust the app.

## 4. Distinguish authentication and authorization.

**Strong answer:** Authentication establishes a principal to a confidence
level. Authorization decides whether that principal may perform this action on
this resource now, normally enforced by the trusted service.

**Weak answer:** A logged-in user can access every ID the app can display.

## 5. What does the Android app sandbox protect?

**Strong answer:** It normally isolates app processes and private files by UID
from ordinary apps. It does not fix exported entry points, compromised process
or device, leaked UI/log data, server flaws, or APK-embedded secrets.

**Weak answer:** Anything inside internal storage is safe from every attacker.

## 6. How should exported components be designed?

**Strong answer:** Export only a documented IPC/link use case, set exposure
explicitly, add a narrow permission where appropriate, validate all input,
authorize actions, rate-limit if needed, and test the merged manifest.

**Weak answer:** A permission-protected component can trust every extra.

**Follow-up:** Why can manifest merging change the review outcome?

## 7. Why are Intents untrusted?

**Strong answer:** External callers can control actions, data, extras, flags,
clip data, nested values, sizes, and referenced content. Parse an allowlisted
contract before side effects.

**Weak answer:** An explicit Intent proves its sender is trusted.

## 8. What security does a verified App Link provide?

**Strong answer:** It establishes the configured domain-to-app association and
reduces handler ambiguity. The app must still validate the URI, establish a
session, and obtain resource authorization.

**Weak answer:** `autoVerify=true` makes parameters and actions authorized.

## 9. What is least privilege for Android permissions?

**Strong answer:** Prefer a narrow API or system picker, declare only required
capabilities, ask in context, recheck at use, and handle denial/revocation with
a useful fallback.

**Weak answer:** Request every possible permission at launch once.

## 10. Are Android permissions business authorization?

**Strong answer:** No. They mediate operating-system capabilities such as
camera access. The application/server separately decides whether a subject may
perform a product action on a resource.

**Weak answer:** Camera permission authorizes uploading any user's document.

## 11. How should sensitive local data be placed?

**Strong answer:** Classify sensitivity, sharing, retention, backup, restore,
and deletion; minimize first; use internal app-specific storage for app-only
data; validate anything read from a modifiable shared boundary.

**Weak answer:** Put everything in external storage and encrypt filenames.

## 12. What does Android Keystore provide?

**Strong answer:** Non-exportable cryptographic-key storage and restricted key
use, with device/configuration-dependent hardware protection. It is not an
arbitrary token vault and needs invalidation, rotation, and recovery policy.

**Weak answer:** Store refresh-token strings directly as Keystore keys.

## 13. What are the limits of encryption at rest?

**Strong answer:** It protects stored ciphertext under its key/threat
assumptions. It does not protect plaintext after decryption, leaked logs/UI,
compromised processes, or missing server authorization.

**Weak answer:** Encrypted data can safely be logged after decryption.

## 14. Can a secret be hidden in an APK?

**Strong answer:** A distributed client can be inspected; resources,
`BuildConfig`, native code, encoding, and obfuscation only change extraction
cost. Keep authoritative secrets on trusted systems and restrict exposed IDs.

**Weak answer:** Moving a key to C++ makes it confidential.

## 15. What must Android TLS policy preserve?

**Strong answer:** HTTPS, certificate-chain and hostname validation, explicit
cleartext/trust configuration, and debug/release separation. TLS protects
transport and server identity, not user authorization or payload meaning.

**Weak answer:** A trust-all manager is acceptable when the API uses HTTPS.

## 16. Should every Android app use certificate pinning?

**Strong answer:** No. Current Android guidance does not recommend it by
default because certificate changes can strand clients. A justified case needs
backup pins, expiry, rotation, monitoring, staged rollout, and recovery.

**Weak answer:** Pin one leaf certificate forever for complete protection.

## 17. What is a safe session/token lifecycle?

**Strong answer:** Scoped/short access credentials where supported, tightly
protected refresh credentials, bounded single-flight refresh, redaction,
server authorization per request, revocation, logout cleanup, and restore
reauthentication.

**Weak answer:** A non-expiring token in logs simplifies debugging.

**Follow-up:** How should concurrent `401` responses be coordinated?

## 18. What does biometric authentication prove?

**Strong answer:** Under the selected authenticator policy it can prove recent
local user presence and gate a Keystore cryptographic operation. It does not
prove remote account identity or resource authorization.

**Weak answer:** A successful fingerprint authorizes every server transfer.

## 19. How do you reduce WebView risk?

**Strong answer:** Prefer browser/Custom Tab for untrusted content. Otherwise
allowlist controlled HTTPS origins, validate navigation, disable unused
JavaScript/file/content/mixed-content features, and avoid native bridges to
untrusted content.

**Weak answer:** Enable every setting so pages work, then clear cache.

## 20. Which accidental data-leak channels matter?

**Strong answer:** Logs, analytics, crash reports, URLs, clipboard,
screenshots/recents, notifications, temporary/exported files, backups, support
payloads, and SDK collection, each with minimization and cleanup policy.

**Weak answer:** Private database encryption covers every leak channel.

## 21. What does `FLAG_SECURE` guarantee?

**Strong answer:** It asks Android to block ordinary screenshots and insecure
displays for that window. It is defense in depth and cannot stop another
camera, all OEM defects, or a compromised device.

**Weak answer:** It makes screen content impossible to capture.

## 22. How should backup and restore handle sessions?

**Strong answer:** Exclude tokens and unsafe device-bound state, use
version-appropriate rules, test cloud/device transfer, and reauthenticate or
reconcile after restore because credentials and Keystore-bound ciphertext may
be invalid.

**Weak answer:** `allowBackup=false` is the only policy any version needs.

## 23. What are key mobile supply-chain controls?

**Strong answer:** Restricted repositories, reviewed plugins/transitives,
updates and vulnerability scanning, artifact checksum/signature verification,
protected signing keys, debug/release separation, and packaged-artifact review.

**Weak answer:** Obfuscation proves dependencies and release configuration are
safe.

## 24. How should integrity verdicts influence a decision?

**Strong answer:** Bind them to the protected request, verify package,
request/freshness, and response on the server, then use them as one risk input
for tiered handling with outage/false-positive policy.

**Weak answer:** A passing verdict authenticates the user and authorizes the
purchase.

## 25. What should Android security tests cover?

**Strong answer:** Hostile component/link inputs, permission denial/revocation,
storage/backup/logout, crypto invalidation/tamper, TLS/debug isolation,
sessions, WebView origins, leakage channels, dependencies, and the merged
release artifact at focused boundaries.

**Weak answer:** One happy-path penetration test proves the app is secure.

**Follow-up:** Why should association, parsing, and authorization be separate
link tests?

## 26. Which security anti-patterns deserve immediate review?

**Strong answer:** Client-only authorization, exported broad entry points,
trust-all TLS, arbitrary WebView bridges, APK secrets, unbounded logging,
encryption without key/recovery policy, permanent single pins, and treating
biometrics, App Links, obfuscation, or integrity as authorization.

**Weak answer:** Security is finished once R8 and HTTPS are enabled.
