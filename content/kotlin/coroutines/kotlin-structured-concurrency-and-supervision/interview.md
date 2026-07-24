# Kotlin Structured Concurrency and Supervision — Interview preparation

### 1. What is structured concurrency?

**Strong answer:** Owned bounded Job trees with parent waiting and predictable
propagation. **Weak answer:** Using async everywhere. **Follow-up:** What does
normal return guarantee?

### 2. How do you read a Job tree?

**Strong answer:** Identify scope receiver and inherited Job for every builder.
**Weak answer:** Infer parents from indentation only. **Follow-up:** What breaks
an inherited edge?

### 3. Why does a parent wait for children?

**Strong answer:** Its completion includes owned subtree completion.
**Weak answer:** Parent finishes at its last statement. **Follow-up:** What does
this provide to suspend callers?

### 4. What propagates downward?

**Strong answer:** Parent cancellation recursively requests child cancellation.
**Weak answer:** Cancellation forcibly kills threads. **Follow-up:** What must
CPU/blocking work do?

### 5. What propagates upward in a regular hierarchy?

**Strong answer:** Non-cancellation child failure cancels/fails the parent.
**Weak answer:** All exceptions stay only in children. **Follow-up:** What about
CancellationException?

### 6. Why are siblings cancelled after regular child failure?

**Strong answer:** Failed parent cancels its remaining subtree for fail-fast
consistency. **Weak answer:** Dispatcher decided it. **Follow-up:** When is this
desirable?

### 7. What does `coroutineScope` guarantee?

**Strong answer:** Lexical child ownership, waiting, fail-fast propagation, and
caller cancellation. **Weak answer:** Application-long scope. **Follow-up:** How
does it return a value?

### 8. When should aggregation fail fast?

**Strong answer:** When every child result is required for a valid aggregate.
**Weak answer:** Never cancel useful work. **Follow-up:** Give an Android case.

### 9. What changes in `supervisorScope`?

**Strong answer:** Direct child failure does not cancel its siblings; caller
cancellation and waiting remain. **Weak answer:** Exceptions disappear.
**Follow-up:** What if the block itself throws?

### 10. Compare `Job` and `SupervisorJob`.

**Strong answer:** Regular child failure cancels a Job parent; SupervisorJob
isolates direct children. **Weak answer:** SupervisorJob retries. **Follow-up:**
Who owns a long-lived SupervisorJob?

### 11. Compare `supervisorScope` and an arbitrary `SupervisorJob`.

**Strong answer:** The first is bounded lexical supervision; replacing a child
Job can detach structure. **Weak answer:** They are interchangeable.
**Follow-up:** What safer long-lived construction exists?

### 12. Why is supervision not error handling?

**Strong answer:** It changes sibling propagation but every failure still needs
observation and representation. **Weak answer:** It prevents errors.
**Follow-up:** What happens to ignored async failure?

### 13. What is best-effort execution?

**Strong answer:** Independent outcomes are collected into an explicit partial
model. **Weak answer:** Ignore failures and show successes. **Follow-up:** Who
owns retry?

### 14. How should partial success be modeled?

**Strong answer:** Per-section outcome matching consumer decisions, without
converting cancellation. **Weak answer:** One universal Boolean. **Follow-up:**
How is cached content represented?

### 15. Who owns a Deferred?

**Strong answer:** Its bounded scope retains and awaits/translates its result.
**Weak answer:** Runtime logs it automatically. **Follow-up:** Does supervision
make await optional?

### 16. Distinguish cancellation and failure.

**Strong answer:** Cancellation means owner no longer needs result; failure
means useful work could not complete. **Weak answer:** Both become empty data.
**Follow-up:** Why rethrow CancellationException?

### 17. How do timeout APIs affect children?

**Strong answer:** They cancel lexical timed subtree; withTimeout throws and
withTimeoutOrNull returns null for timeout. **Weak answer:** They kill detached
work. **Follow-up:** How can a leak escape timeout?

### 18. Where does cleanup belong?

**Strong answer:** In finally, preferably non-suspending. **Weak answer:** In a
new global launch. **Follow-up:** When is suspending cleanup justified?

### 19. Why constrain NonCancellable?

**Strong answer:** It delays/ignores cancellation, so only small mandatory
suspending cleanup belongs there. **Weak answer:** Wrap retries and uploads.
**Follow-up:** Why not use it as a launch Job?

### 20. When is an external application scope appropriate?

**Strong answer:** Explicitly owned disposable in-process work that must outlive
a screen. **Weak answer:** Every Repository creates one. **Follow-up:** Should
the caller join?

### 21. When does WorkManager become the boundary?

**Strong answer:** Reliable scheduled work required beyond screen/app process
ownership. **Weak answer:** Every suspend call. **Follow-up:** What remains an
ordinary coroutine?

### 22. How do you test propagation?

**Strong answer:** runTest plus deterministic signals for sibling cancellation,
supervised survival, waiting, timeout, cleanup, and no leaks. **Weak answer:**
Thread.sleep and log order. **Follow-up:** How do you observe both failures?
