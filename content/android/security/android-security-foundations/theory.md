# Android Security Foundations

Android security is not a collection of magic flags. It is a repeated reasoning
process:

```text
assets → entry point → trust boundary → validate → authenticate → authorize
       → minimize retained/exposed data → test negative paths
```

The operating system supplies strong primitives, but the application still
owns product policy, server enforcement, data classification, configuration,
and failure behavior.

## 1. Security goals

Start with what must remain true:

- **confidentiality** — unauthorized parties do not learn protected data;
- **integrity** — unauthorized changes are detected or rejected;
- **availability** — legitimate users can complete important work;
- **privacy** — collection, use, retention, and disclosure are minimized;
- **authenticity** — identities and origins are established to the required
  confidence;
- **accountability** — important actions can be attributed and investigated
  without logging secrets.

Goals can conflict. Hiding every error may harm support; retaining every event
may harm privacy. Record the trade-off rather than calling a feature “secure.”

```kotlin
data class SecurityGoal(
    val asset: String,
    val property: Property,
    val failureImpact: Impact,
)

enum class Property { CONFIDENTIALITY, INTEGRITY, AVAILABILITY, PRIVACY }
enum class Impact { LOW, MATERIAL, CRITICAL }
```

## 2. Assets, threats, and attack surface

An asset may be an access token, account balance, private message, signing key,
local document, user identity, or the ability to perform an action. A threat is
an event that violates a goal; an attacker is an actor with capabilities and
motivation.

Inventory entry points: exported components, links, intents, files, providers,
WebView content, network responses, notifications, backups, clipboard, IPC,
SDKs, and build inputs. Also inventory accidental observers such as analytics,
crash collection, screen sharing, or support logs.

```kotlin
data class AttackSurface(
    val asset: String,
    val entryPoint: String,
    val callerCanControl: Set<String>,
    val boundaryOwner: String,
)
```

## 3. Lightweight threat modeling

Threat modeling can fit into feature design:

1. Name assets and security goals.
2. Draw data flow, owners, entry points, and trust boundaries.
3. Describe plausible abuse cases and attacker capabilities.
4. Rank likelihood and impact.
5. Choose preventive, detective, and recovery controls.
6. Add negative tests and an owner for residual risk.

Do not model an omnipotent attacker when the product decision concerns a
malicious link, and do not assume “inside the app” is trusted when inputs came
from another process or remote system.

```kotlin
data class Threat(
    val abuseCase: String,
    val preconditions: Set<String>,
    val impact: Impact,
    val controls: List<String>,
    val residualRiskOwner: String,
)
```

## 4. Defense in depth and trust boundaries

Each boundary re-establishes trust for its own decision. A verified domain does
not validate a record ID. A valid session does not authorize every record.
Encryption does not make plaintext safe after decryption. Obfuscation raises
reverse-engineering cost but does not create a secret.

Prefer small, independently useful controls: minimize exposure, validate shape,
authenticate identity, authorize the action, constrain data, observe failures,
and recover safely.

```kotlin
suspend fun loadInvoice(request: InvoiceRequest): Invoice {
    val id = InvoiceId.parse(request.rawId) ?: throw InvalidRequest()
    val session = sessionRepository.requireAuthenticated()
    authorizationRepository.requireCanRead(session.subject, id)
    return invoiceRepository.get(id)
}
```

## 5. Authentication is not authorization

Authentication answers “who or what is this?” Authorization answers “may this
principal perform this action on this resource now?” Android permissions answer
whether an app may use an operating-system capability. Biometrics can establish
local user presence. App Links establish an app-domain association. Integrity
verdicts provide risk signals. None is a substitute for resource authorization.

The trusted service should authorize every protected server operation. Client
checks improve UX and reduce accidental misuse, but a modified client can omit
them.

```kotlin
data class AuthorizedRequest(
    val subjectId: String,
    val action: String,
    val resourceId: String,
)

suspend fun deleteDocument(id: String) {
    // The server authorizes subject + action + resource on this request.
    api.deleteDocument(id)
}
```

## 6. Android sandbox and its limits

Android gives each app a distinct UID and normally isolates its process and
private files from ordinary apps. Component export rules, permissions, scoped
storage, and platform mediation extend that boundary.

The sandbox does not protect against your own compromised process, an exported
component with weak validation, a rooted or otherwise compromised device,
debuggable/repackaged builds, screenshots, server compromise, or secrets
embedded in the APK. State assumptions explicitly.

```xml
<application
    android:allowBackup="false"
    android:debuggable="false"
    android:usesCleartextTraffic="false">
    <activity
        android:name=".internal.SettingsActivity"
        android:exported="false" />
</application>
```

Release values are normally controlled by build configuration and manifest
merging; inspect the merged release manifest rather than trusting one source
file.

## 7. Exported components

Activities, services, receivers, and providers are IPC entry points.
Explicitly set `android:exported`. Export only a documented use case. A
permission-protected exported component still needs input validation,
authorization, rate limiting where relevant, and safe failure behavior.

```xml
<permission
    android:name="com.example.app.permission.SYNC"
    android:protectionLevel="signature" />

<service
    android:name=".sync.PartnerSyncService"
    android:exported="true"
    android:permission="com.example.app.permission.SYNC" />
```

Signature permissions can restrict callers signed with an expected
certificate; they do not validate each request or grant business access.
Manifest merging can change effective exposure, so test the packaged manifest.

## 8. Intents are untrusted input

Explicit and implicit intents can contain attacker-controlled actions, URIs,
extras, flags, clip data, and nested parcelables. Validate an allowlisted action
and every field before use. Apply length/range limits and parse into typed
values. Do not infer caller authenticity from a package-shaped string inside
the Intent.

```kotlin
fun parseImport(intent: Intent): ImportRequest? {
    if (intent.action != ACTION_IMPORT) return null
    val uri = intent.data ?: return null
    if (uri.scheme != ContentResolver.SCHEME_CONTENT) return null
    val type = intent.type ?: return null
    if (type !in setOf("text/plain", "application/json")) return null
    return ImportRequest(uri = uri, mimeType = type)
}
```

When consuming a `content://` URI, accept only the required grant, handle
revocation, bound bytes and time, validate content rather than trusting the
extension, and never turn supplied paths into arbitrary filesystem access.

## 9. Deep links and verified App Links

A deep link is a navigation request from outside the current UI. Validate
scheme, host, path, parameter count, decoded size, identifiers, and allowed
destination. Avoid open redirects and never execute a sensitive action merely
because a link arrived.

Verified App Links establish that a web domain is associated with an installed
application. They reduce handler ambiguity; they do not prove that query
parameters are safe, that a user is signed in, or that the user may access a
resource.

```kotlin
fun parseOrderLink(uri: Uri): OrderLink? {
    if (uri.scheme != "https" || uri.host != "orders.example.com") return null
    if (uri.pathSegments.size != 2 || uri.pathSegments[0] != "orders") return null
    val id = uri.pathSegments[1].takeIf { it.matches(Regex("[A-Z0-9]{8,20}")) }
        ?: return null
    return OrderLink(id)
}
```

```xml
<activity
    android:name=".links.OrderLinkActivity"
    android:exported="true">
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="https"
            android:host="orders.example.com"
            android:pathPrefix="/orders/" />
    </intent-filter>
</activity>
```

After parsing, route to a safe screen, establish session state, and let the
server authorize the order. Test verified association separately from
application routing and authorization.

## 10. Least privilege for permissions

Ask whether the feature can use a system picker, narrow API, coarse signal, or
user-supplied document instead of a broad permission. Declare only required
permissions, request them in context, and remove unused declarations from the
merged manifest.

```kotlin
val pickDocument = registerForActivityResult(
    ActivityResultContracts.OpenDocument(),
) { uri ->
    uri?.let(viewModel::onDocumentSelected)
}

fun chooseDocument() {
    pickDocument.launch(arrayOf("application/pdf"))
}
```

The system picker grants access to the selected item and can avoid a broad
storage capability.

## 11. Runtime permission states

Permission behavior varies by Android version and capability: install-time,
runtime, special access, one-time grants, approximate values, auto-reset, and
policy restrictions are different contracts. Check at the operation boundary;
do not cache “granted forever.”

```kotlin
val requestCamera = registerForActivityResult(
    ActivityResultContracts.RequestPermission(),
) { granted ->
    if (granted) viewModel.onCameraAvailable()
    else viewModel.onCameraUnavailable()
}

fun startScan() {
    when {
        ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.CAMERA,
        ) == PackageManager.PERMISSION_GRANTED -> viewModel.onCameraAvailable()
        shouldShowRequestPermissionRationale(Manifest.permission.CAMERA) ->
            showCameraRationale()
        else -> requestCamera.launch(Manifest.permission.CAMERA)
    }
}
```

Denial, “don’t ask again,” revocation, and missing hardware need useful
fallbacks. Never confuse permission denial with authorization denial from the
product service.

## 12. Local storage and data minimization

Classify data by sensitivity, lifetime, sharing, backup, deletion, and
recoverability. Keep app-only sensitive files in internal app-specific storage.
Use shared storage only for deliberately shared user content, and validate
anything read back from a location another actor can modify.

```kotlin
fun writePrivateDraft(context: Context, bytes: ByteArray) {
    context.openFileOutput("draft.bin", Context.MODE_PRIVATE).use { output ->
        output.write(bytes)
    }
}
```

Private storage is a sandbox control, not a promise against a compromised
process or device. Cache is evictable. Deleting a filename does not necessarily
guarantee physical erasure on flash. Store less, retain for less time, and
define logout/account-removal cleanup.

## 13. Android Keystore

Android Keystore stores cryptographic keys so key material can be non-exportable
and key use can be restricted. Hardware-backed protection depends on device and
key configuration; check capabilities when the threat model requires them.
Keystore is not a general-purpose store for tokens or arbitrary secret bytes.

```kotlin
fun createEncryptionKey(alias: String) {
    val generator = KeyGenerator.getInstance(
        KeyProperties.KEY_ALGORITHM_AES,
        "AndroidKeyStore",
    )
    generator.init(
        KeyGenParameterSpec.Builder(
            alias,
            KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
        )
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .build(),
    )
    generator.generateKey()
}
```

Plan for key invalidation, lock-screen or biometric enrollment changes,
restore to another device, rotation, data migration, and unrecoverable
ciphertext.

## 14. Encryption at rest and its limits

Encryption needs an authenticated mode, unique nonce/IV policy, protected key,
versioned envelope, integrity failure behavior, migration, and deletion policy.
Do not invent cryptographic formats.

```kotlin
data class CipherEnvelope(
    val version: Int,
    val iv: ByteArray,
    val ciphertext: ByteArray,
)

fun encrypt(plain: ByteArray, key: SecretKey): CipherEnvelope {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, key)
    return CipherEnvelope(1, cipher.iv, cipher.doFinal(plain))
}
```

Encryption at rest does not protect plaintext after your process decrypts it,
nor data copied to logs, UI, analytics, clipboard, notifications, or backups.
It cannot repair an authorization failure. Minimize plaintext lifetime and
make failures closed and recoverable.

## 15. Secrets cannot be hidden in an APK

APK resources, `BuildConfig`, native libraries, encoded strings, and obfuscated
code can be inspected. Obfuscation increases analysis cost; it does not turn a
client value into an authoritative secret.

```kotlin
// Anti-pattern: extraction from a distributed APK is an expected capability.
private const val ADMIN_API_SECRET = "not-a-secret"

// Better boundary: authenticate the user/app request, then let the server keep
// authoritative credentials and authorize the operation.
suspend fun requestSignedUpload(): UploadGrant = api.createUploadGrant()
```

Public client identifiers may be shipped when designed for exposure. Restrict
keys by API, app signing identity, quota, environment, and monitoring where the
provider supports it. Never put release secrets or signing material in source
control.

## 16. TLS and Network Security Configuration

TLS protects data in transit and authenticates the server through certificate
chain and hostname validation. Preserve platform validation. Never install a
trust-all manager, accept every hostname, or silently fall back to cleartext.
TLS does not validate business payloads or authorize users.

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
```

Use Network Security Configuration for explicit trust and cleartext policy.
Keep a development CA in debug-only configuration:

```xml
<network-security-config>
    <base-config cleartextTrafficPermitted="false" />
    <debug-overrides>
        <trust-anchors>
            <certificates src="@raw/debug_ca" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

Inspect the release artifact so a debug CA or cleartext exception cannot leak
through build variants or manifest/resource merging.

## 17. Certificate pinning is an exceptional control

Current Android guidance does not recommend certificate pinning as the default:
certificate or CA changes can strand installed clients until an update reaches
them. Consider pinning only for a specific on-path threat after evaluating
platform protections and operational cost.

If approved, define multiple backup pins, expiry, rotation rehearsal,
monitoring, staged rollout, emergency recovery, and owners. Never pin one leaf
certificate forever.

```xml
<!-- Illustrative only: values and policy require security review. -->
<domain-config>
    <domain includeSubdomains="true">high-risk.example.com</domain>
    <pin-set expiration="2027-07-01">
        <pin digest="SHA-256">PRIMARY_BASE64_SPKI_HASH=</pin>
        <pin digest="SHA-256">BACKUP_BASE64_SPKI_HASH=</pin>
    </pin-set>
</domain-config>
```

Pinning is transport policy, not user or resource authorization.

## 18. Tokens and session lifecycle

The server authenticates and authorizes every protected request. Access tokens
should be scoped and short-lived where the system supports it. Refresh
credentials are more sensitive, require narrow storage and rotation policy,
and must never appear in logs, analytics, crash reports, URLs, or notifications.

```kotlin
fun redactHeaders(headers: Map<String, String>): Map<String, String> =
    headers.mapValues { (name, value) ->
        if (name.equals("Authorization", ignoreCase = true) ||
            name.equals("Cookie", ignoreCase = true)
        ) "[REDACTED]" else value.take(128)
    }
```

Coordinate concurrent refresh as one bounded operation, prevent recursive
refresh, and distinguish expiry, revocation, network failure, and cancellation.
Logout should invalidate local credentials and sensitive caches; use server
revocation when supported. Restored or copied tokens may be rejected and should
lead to reauthentication, not an infinite refresh loop.

## 19. Biometrics and device credentials

BiometricPrompt or device credential can confirm local user presence and unlock
a Keystore-backed cryptographic operation. Credential Manager is the normal
starting point for account sign-in; local reauthentication is a separate
decision.

```kotlin
fun authenticateForKeyUse(
    prompt: BiometricPrompt,
    promptInfo: BiometricPrompt.PromptInfo,
    cipher: Cipher,
) {
    prompt.authenticate(
        promptInfo,
        BiometricPrompt.CryptoObject(cipher),
    )
}
```

Handle cancellation, lockout, unavailable enrollment, changed enrollment, and
key invalidation. In the prompt success callback, use the returned
`CryptoObject.cipher`; do not recreate or silently bypass it. A successful
prompt does not prove a remote account identity or grant access to every server
resource. The server still authorizes the resulting operation.

## 20. WebView is a high-risk content boundary

Prefer a browser or Custom Tab for untrusted web content and web authentication
when it meets the product need. If WebView is necessary, allowlist controlled
HTTPS origins, disable unused features, validate every navigation, avoid mixed
content, and keep it patched.

```kotlin
fun harden(webView: WebView) = with(webView.settings) {
    javaScriptEnabled = false
    allowFileAccess = false
    allowContentAccess = false
    mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
}
```

JavaScript bridges expose native methods to page frames and are unsafe with
untrusted content. Do not add a bridge to content that can navigate or inject
arbitrary frames. Clear sensitive cache/history when policy requires it, but
do not treat clearing as a substitute for a safe origin boundary.

## 21. Sensitive-data leakage channels

Data escapes through more than files: logs, analytics, crash reports, URLs,
screen recording, recents thumbnails, clipboard previews, notifications,
temporary exports, support attachments, and third-party SDKs. Establish one
redaction and collection policy across all observability tools.

```kotlin
fun safeAudit(event: String, accountId: String): String {
    val pseudonymous = MessageDigest.getInstance("SHA-256")
        .digest(accountId.toByteArray())
        .take(6)
        .joinToString("") { "%02x".format(it) }
    return "event=$event account_hash=$pseudonymous"
}
```

Hashing a low-entropy identifier is not anonymization; prefer a scoped,
rotatable pseudonymous identifier if correlation is required.

For truly sensitive screens, `FLAG_SECURE` can block normal screenshots and
non-secure displays, but it is defense in depth, not protection from another
camera or a compromised device:

```kotlin
fun Activity.protectSensitiveWindow() {
    window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
}
```

Avoid copying secrets. When copying sensitive content is unavoidable, mark it
sensitive on supported versions and expire/clear it according to product
policy:

```kotlin
fun copySensitive(context: Context, label: String, value: String) {
    val clip = ClipData.newPlainText(label, value)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        clip.description.extras = PersistableBundle().apply {
            putBoolean(ClipDescription.EXTRA_IS_SENSITIVE, true)
        }
    }
    context.getSystemService(ClipboardManager::class.java).setPrimaryClip(clip)
}
```

Marking changes previews; it does not make clipboard storage a secret vault.
Notifications should reveal the minimum:

```kotlin
val notification = NotificationCompat.Builder(context, CHANNEL_ID)
    .setSmallIcon(R.drawable.ic_status)
    .setContentTitle("Account update")
    .setContentText("Open the app to view details")
    .setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
    .setPublicVersion(
        NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_status)
            .setContentTitle("Account update")
            .build(),
    )
    .build()
```

Users and device policy ultimately control lock-screen display. Temporary and
exported files need unique names, narrow URI grants, validation, expiry, and
cleanup on success, failure, and cancellation.

## 22. Backup and restore are data flows

Backups and device-to-device transfer cross a trust and lifecycle boundary.
Classify every file and preference: include only what should follow the user,
exclude tokens, Keystore-bound ciphertext, transient caches, and server-derived
sensitive state when restoration is unsafe.

Rules differ across Android versions, so configure and test the applicable
backup formats:

```xml
<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="session.xml" />
        <exclude domain="file" path="sensitive/" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="sharedpref" path="session.xml" />
        <exclude domain="file" path="sensitive/" />
    </device-transfer>
</data-extraction-rules>
```

After restore, treat sessions and device-bound keys as potentially invalid,
reauthenticate, reconcile with the server, and delete unusable ciphertext. Test
cloud backup, device transfer, upgrade, logout, and account removal rather than
assuming `allowBackup` alone describes every version and transport.

## 23. Build, dependencies, signing, and supply chain

The build is a security boundary. Restrict repositories, review dependency and
plugin changes, remove unused libraries, patch known vulnerabilities, verify
artifacts, protect signing keys, and separate debug/release endpoints and
credentials. Generated verification metadata must itself be reviewed from a
trusted baseline.

```kotlin
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
```

Gradle dependency verification can check expected checksums and signatures;
integrity and publisher identity are different questions, and neither proves
that a dependency is vulnerability-free. Produce and inspect a release bill of
materials, merged manifest, network config, native libraries, permissions, and
debug flags. Obfuscation is resilience friction, not authorization or secrecy.

## 24. App and device integrity signals

Play Integrity and similar services can provide server-verified signals about
the recognized app, device, environment, or account context. Bind the verdict
to the sensitive request using the current API's request hash or nonce rules,
verify package/request/freshness server-side, prevent replay, and avoid unsafe
caching.

```kotlin
data class RiskContext(
    val authenticatedSubject: String,
    val action: String,
    val resourceId: String,
    val integrityTier: IntegrityTier?,
)

enum class IntegrityTier { EXPECTED, LIMITED, HIGH_RISK }
```

Use a tiered response: allow, add verification, limit abuse-prone operations,
or review. Plan for unavailable services and false positives. An integrity
verdict is an input to risk policy, not proof of user identity and never the
resource authorization decision itself.

## 25. Security testing and review

Test the negative path at the boundary that owns it:

- inspect merged release manifests and network configuration;
- invoke exported components with missing, malformed, oversized, and hostile
  extras;
- test deep-link association separately from route validation and server
  authorization;
- deny/revoke permissions before and during an operation;
- inspect files, backups, logs, analytics, crash payloads, notifications, and
  screenshots for sensitive data;
- test invalid TLS, cleartext, debug CA isolation, token expiry/revocation,
  logout, restore, WebView navigation, and dependency verification;
- use static analysis, dependency scanning, focused instrumentation, and
  authorized penetration testing as complementary evidence.

```kotlin
@Test
fun exportedOrderLink_neverOpensUnauthorizedOrder() {
    val link = Uri.parse("https://orders.example.com/orders/ABCDEFGH")
    launchActivity<OrderLinkActivity>(Intent(Intent.ACTION_VIEW, link)).use {
        onView(withText("Sign in to continue")).check(matches(isDisplayed()))
        onView(withText("Order total")).check(doesNotExist())
    }
}
```

```kotlin
@Test
fun logger_redactsTokensAndPersonalData() {
    val output = logger.format(
        path = "/orders/{id}",
        authorization = "Bearer access-token",
        email = "person@example.com",
    )
    assertFalse(output.contains("access-token"))
    assertFalse(output.contains("person@example.com"))
}
```

Tests reduce known risk; they do not prove the absence of vulnerabilities.
Track assumptions, evidence, residual risk, and remediation ownership.

## 26. Anti-patterns and a repeatable review

Reject these shortcuts:

- “the value is obfuscated, therefore secret”;
- “biometric success authorizes the account action”;
- “App Link verification makes parameters trusted”;
- “an integrity verdict authorizes the resource”;
- trust-all TLS, disabled hostname verification, or production debug CAs;
- one permanent pin without recovery;
- broad exported components, permissions, storage, logging, or SDK collection;
- authorization only in UI;
- arbitrary WebView content with JavaScript/native bridges;
- encryption without key, nonce, recovery, and plaintext policy;
- backups, restored sessions, and logout left untested.

Use the same review loop for every sensitive feature:

```kotlin
data class SecurityReview(
    val assets: Set<String>,
    val entryPoints: Set<String>,
    val trustBoundaries: Set<String>,
    val validationRules: Set<String>,
    val authentication: String?,
    val authorizationOwner: String,
    val minimizedData: Set<String>,
    val negativeTests: Set<String>,
    val residualRisks: Set<String>,
)
```

Security is maintained when these decisions remain explicit through design,
implementation, release configuration, monitoring, incident response, and
change review.
