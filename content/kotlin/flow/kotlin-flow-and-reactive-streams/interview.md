# Kotlin Flow and Reactive Streams — Interview preparation

## Questions

### 1. When should an API return Flow instead of using a suspend function?

- **Strong answer:** A suspend function represents one completion; Flow is for
  zero or more values whose changes over time are part of the contract.
- **Weak answer:** “Flow is asynchronous, suspend is synchronous.”
- **Follow-up:** Why is a one-shot network request usually not improved merely
  by wrapping it in `flow {}`?

### 2. What makes a Flow cold?

- **Strong answer:** Its upstream starts independently for each collector;
  repeated collection can repeat I/O, registration, and transformation work.
- **Weak answer:** “Cold means it runs on a background thread.”
- **Follow-up:** How would you test the number of upstream starts?

### 3. What starts a cold Flow pipeline?

- **Strong answer:** A terminal operator such as `collect`, `first`, `toList`,
  or `count`; intermediate operators only build another Flow.
- **Weak answer:** “Declaring the Flow starts it.”
- **Follow-up:** Why can `toList` hang on a hot stream?

### 4. Are Flow operators concurrent by default?

- **Strong answer:** No. Ordinary Flow execution is sequential in the
  collecting coroutine unless an operator such as `buffer`, `flowOn`, or
  sharing introduces a concurrency boundary.
- **Weak answer:** “Every operator runs on a separate coroutine.”
- **Follow-up:** What ordering guarantee remains with `buffer`?

### 5. How do map, filter, transform, and onEach differ?

- **Strong answer:** `map` creates one output, `filter` conditionally retains
  an input, `transform` may emit any number, and `onEach` performs a suspending
  side effect while forwarding the same value.
- **Weak answer:** “They are interchangeable syntax.”
- **Follow-up:** Why can fire-and-forget work inside `onEach` violate ownership?

### 6. What is Flow context preservation?

- **Strong answer:** A Flow encapsulates upstream context, downstream executes
  in the collector's context, and a regular `flow` builder must not emit from an
  arbitrary foreign context.
- **Weak answer:** “Flow always uses Dispatchers.IO.”
- **Follow-up:** When is `channelFlow` appropriate?

### 7. What does `flowOn` affect?

- **Strong answer:** Operators upstream of `flowOn`; it does not move downstream
  operators or the collector and may introduce a coroutine/buffer boundary.
- **Weak answer:** “It changes the dispatcher of the whole chain.”
- **Follow-up:** How does this differ from wrapping collection in `withContext`?

### 8. Which exceptions does `catch` observe?

- **Strong answer:** Exceptions from upstream operators before it. It is
  transparent to downstream collector failures and cancellation.
- **Weak answer:** “It catches every exception anywhere in the stream.”
- **Follow-up:** Where would a failure thrown after `catch` propagate?

### 9. How should cancellation be treated in error translation?

- **Strong answer:** As owner control flow, not business failure. Broad
  translations explicitly rethrow `CancellationException`.
- **Weak answer:** “Emit an error state for every Throwable.”
- **Follow-up:** What bug appears when `flatMapLatest` cancellation becomes an
  error result?

### 10. What is the role of `onCompletion`?

- **Strong answer:** It observes normal completion, failure, or cancellation,
  similar to a declarative `finally`; it is not general exception recovery.
- **Weak answer:** “It is another form of catch.”
- **Follow-up:** When may it safely emit a completion marker?

### 11. How do you design retry safely?

- **Strong answer:** Limit retryable failure types and attempts, define backoff
  and lifetime ownership, and expose user retry when appropriate.
- **Weak answer:** “Use `retry { true }` so the screen heals itself.”
- **Follow-up:** Which failures should normally not be retried?

### 12. What does `buffer` change?

- **Strong answer:** It allows bounded overlap between upstream and downstream;
  the producer can run ahead until capacity is full while values remain part of
  the contract.
- **Weak answer:** “It makes collection parallel and never suspends.”
- **Follow-up:** What costs grow with buffer capacity?

### 13. When is `conflate` correct?

- **Strong answer:** When only the latest state matters and intermediate pending
  snapshots may be skipped.
- **Weak answer:** “Whenever performance is slow.”
- **Follow-up:** Give an example where conflation would corrupt behavior.

### 14. How does `collectLatest` differ from `conflate`?

- **Strong answer:** `conflate` may skip pending upstream values; `collectLatest`
  cancels the previous collector block when a newer value arrives.
- **Weak answer:** “They both just keep the final value.”
- **Follow-up:** What must the collector block do correctly?

### 15. How do `combine`, `zip`, and `merge` differ?

- **Strong answer:** `combine` recomputes from latest values after all sources
  emit; `zip` pairs one-to-one; `merge` interleaves without pairing.
- **Weak answer:** “They all concatenate streams.”
- **Follow-up:** Which fits a UI snapshot made from user and settings state?

### 16. What does `flatMapLatest` guarantee?

- **Strong answer:** A new outer value cancels collection of the previous inner
  Flow and switches to the latest; obsolete work must cooperate with
  cancellation. Current API documentation marks the operator
  `ExperimentalCoroutinesApi`, so code must opt in where required by its
  installed kotlinx.coroutines version.
- **Weak answer:** “It queues every inner Flow in order.”
- **Follow-up:** Why is it dangerous for must-complete commands, and where
  should a required opt-in be scoped?

### 17. What is the contract of StateFlow?

- **Strong answer:** A hot broadcast state holder with an always-available
  current value and equality-based conflation.
- **Weak answer:** “A SharedFlow with any buffer.”
- **Follow-up:** Why must its initial value be truthful?

### 18. Why is StateFlow not a default event queue?

- **Strong answer:** It represents current state, conflates equal/rapid
  assignments, and replays the current value to new collectors; transient event
  delivery needs an explicit policy.
- **Weak answer:** “Events are fine if set back to null.”
- **Follow-up:** When can an event outcome be modeled as durable state instead?

### 19. What does SharedFlow provide?

- **Strong answer:** Hot broadcast emissions with configurable replay,
  additional buffer capacity, and overflow behavior; subscriber timing matters.
- **Weak answer:** “Guaranteed delivery to every future subscriber.”
- **Follow-up:** What happens to a replay-zero emission with no subscribers?

### 20. How does Channel differ from SharedFlow?

- **Strong answer:** Channel coordinates sends and receives; multiple receivers
  normally compete for elements. SharedFlow broadcasts each emission to active
  subscribers.
- **Weak answer:** “Channel is an older SharedFlow.”
- **Follow-up:** What does an unbuffered Channel mean?

### 21. What do `stateIn` and `shareIn` own?

- **Strong answer:** They start one upstream sharing coroutine in the supplied
  scope. `stateIn` retains current state; `shareIn` retains configured replay.
- **Weak answer:** “They cache forever independently of scope.”
- **Follow-up:** Where should upstream failures be handled?

### 22. How do SharingStarted strategies differ?

- **Strong answer:** `Eagerly` starts immediately, `Lazily` starts at the first
  subscriber and then continues, and `WhileSubscribed` starts/stops according
  to subscribers with configurable timing/replay reset policy.
- **Weak answer:** “WhileSubscribed(5000) is always recommended.”
- **Follow-up:** Which product facts determine a stop timeout?

### 23. How should Android UI collect Flow?

- **Strong answer:** Compose uses `collectAsStateWithLifecycle`; Views use the
  appropriate Lifecycle, and Fragment views use
  `viewLifecycleOwner.repeatOnLifecycle`. Parallel streams need child
  collectors.
- **Weak answer:** “Launch collect once in Fragment.onCreate.”
- **Follow-up:** What happens when lifecycle falls below the active state?

### 24. How do you test cold and hot flows?

- **Strong answer:** Use finite operators for bounded cold streams, control
  virtual time, start hot collectors deliberately, assert StateFlow `value`
  where appropriate, and cancel/background infinite collection.
- **Weak answer:** “Call `toList()` on every Flow.”
- **Follow-up:** Why might a `stateIn(WhileSubscribed)` test require an active
  subscriber?
