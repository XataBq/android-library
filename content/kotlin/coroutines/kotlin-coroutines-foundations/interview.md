# Kotlin Coroutines Foundations — Interview preparation

## Execution model

### 1. What is a coroutine, and how is it different from a thread?

**Strong answer:** A coroutine is a cancellable computation that can suspend;
a thread is the execution resource that runs coroutine segments.

**Weak answer:** A coroutine is simply a lightweight thread.

**Follow-up:** What executes coroutine code while it is running?

### 2. What does `suspend` guarantee?

**Strong answer:** The function may suspend and can call other suspend
functions; it does not create a coroutine or select background execution.

**Weak answer:** Every suspend function automatically runs on IO.

**Follow-up:** Can a suspend function still block Main?

### 3. What is a continuation conceptually?

**Strong answer:** The retained state describing what computation should resume
after a suspension point completes.

**Weak answer:** A dedicated sleeping thread for each coroutine.

**Follow-up:** Must every suspend call actually suspend?

### 4. What owns a coroutine's lifetime?

**Strong answer:** Its CoroutineScope and Job hierarchy, chosen to match the
screen, request, component, or application work owner.

**Weak answer:** The dispatcher owns lifetime.

**Follow-up:** Why is an ad hoc scope risky?

### 5. What is CoroutineContext?

**Strong answer:** A collection of keyed execution elements such as Job,
dispatcher, name, and sometimes an exception handler.

**Weak answer:** Another name for an OS thread.

**Follow-up:** Which elements answer lifetime and scheduling questions?

### 6. Explain basic Job parent-child behavior.

**Strong answer:** Children normally belong to the parent; parent cancellation
reaches children, parent waits for them, and unhandled child failure normally
affects the hierarchy.

**Weak answer:** Every launch is independent.

**Follow-up:** Which advanced policy is intentionally missing here?

### 7. How do Main, Default, and IO differ?

**Strong answer:** Main is UI-confined, Default targets CPU work, and IO
integrates blocking I/O without blocking Main.

**Weak answer:** Each dispatcher is exactly one fixed thread.

**Follow-up:** Where should dispatcher selection usually live?

### 8. When would you use Dispatchers.Unconfined?

**Strong answer:** Only specialized low-level cases where its resumption
behavior is understood; not normal UI, Data, or Domain work.

**Weak answer:** As the fastest universal dispatcher.

**Follow-up:** Why is it unsafe to infer its post-suspension thread?

### 9. Can one coroutine resume on another thread?

**Strong answer:** Yes; the dispatcher and suspension/resumption determine an
eligible thread, while coroutine identity remains independent.

**Weak answer:** A coroutine owns one thread until completion.

**Follow-up:** What does this mean for thread-local assumptions?

## Builders and ordering

### 10. When should you use `launch`?

**Strong answer:** For scope-owned work with no direct result value; it returns
a Job for cancellation, joining, and status.

**Weak answer:** For any suspend function that exists.

**Follow-up:** Does launch guarantee parallel execution?

### 11. When should you use `async`?

**Strong answer:** For deliberate concurrent result-producing work whose
Deferred result will be awaited or explicitly handled.

**Weak answer:** As a faster replacement for every suspend call.

**Follow-up:** What is wrong with a forgotten Deferred?

### 12. Why is immediate `async().await()` usually a smell?

**Strong answer:** Nothing overlaps; it adds Deferred and failure ceremony to a
sequential call.

**Weak answer:** Await always blocks a thread.

**Follow-up:** What simpler call preserves the behavior?

### 13. What does `withContext` do?

**Strong answer:** Runs a sequential child block in a derived context, suspends
the caller, and returns its result without detaching lifetime.

**Weak answer:** Starts permanent background fire-and-forget work.

**Follow-up:** Give a blocking integration use case.

### 14. Distinguish sequential, concurrent, and parallel work.

**Strong answer:** Sequential work is ordered, concurrent lifetimes overlap,
and parallel instructions execute simultaneously on separate resources.

**Weak answer:** Concurrent always means parallel.

**Follow-up:** Why must dependent requests remain sequential?

### 15. Compare `delay` and `Thread.sleep`.

**Strong answer:** Delay suspends a coroutine and releases its thread; sleep
blocks the current thread.

**Weak answer:** Both are equivalent inside a suspend function.

**Follow-up:** What about blocking JDBC called from suspend?

## Cancellation and exceptions

### 16. Why is coroutine cancellation cooperative?

**Strong answer:** Code stops when cancellable suspension or an explicit check
observes the cancelled Job.

**Weak answer:** Cancellation forcibly kills any thread immediately.

**Follow-up:** How should a CPU loop cooperate?

### 17. Why rethrow CancellationException?

**Strong answer:** It carries cancellation control flow; swallowing it can keep
obsolete work running and report false success.

**Weak answer:** Convert it into an empty business result.

**Follow-up:** Where does cleanup belong?

### 18. How do basic `launch` and `async` exception contracts differ?

**Strong answer:** Launch has no result channel; async exposes failure through
await, while both still participate in their Job hierarchy.

**Weak answer:** Async failures never affect parents.

**Follow-up:** Why is CoroutineExceptionHandler not universal catch-all logic?

## Android architecture and tests

### 19. How do Android coroutine scopes differ?

**Strong answer:** `viewModelScope`, lifecycle scopes, restartable lifecycle
blocks, and Compose scopes cancel according to different UI owners.

**Weak answer:** Always choose the longest-lived scope.

**Follow-up:** Who owns work that must outlive a ViewModel?

### 20. Where should dispatcher decisions live across layers?

**Strong answer:** Near the Data or computation implementation that knows it
blocks or consumes CPU, so callers get a main-safe suspend contract.

**Weak answer:** Every ViewModel wraps every call in IO.

**Follow-up:** Must every pure use case receive a dispatcher?

### 21. How do you test delays without waiting in real time?

**Strong answer:** Use `runTest`, test dispatchers sharing one scheduler, and
advance virtual time deliberately.

**Weak answer:** Sleep slightly longer than production delay.

**Follow-up:** What do `runCurrent` and `advanceUntilIdle` establish?

### 22. Which coroutine anti-pattern would you review first?

**Strong answer:** Tie the answer to consequences: unmanaged scope, blocked
Main, swallowed cancellation, hidden work, or forgotten result.

**Weak answer:** Add CoroutineExceptionHandler everywhere.

**Follow-up:** How would you make ownership and completion observable?
