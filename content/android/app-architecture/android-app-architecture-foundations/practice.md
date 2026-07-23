# Android App Architecture Foundations — Practice

## Exercise 1 — Classify responsibilities

### Task

A reading app has the following responsibilities. Classify each as **UI**, **Data**, **optional Domain**, or **requires more context**. Explain which responsibility or lifetime constraint drives each choice.

1. Show a progress indicator while articles are being prepared for display.
2. Resolve a conflict between a locally edited bookmark and an older server value.
3. Record the text currently entered in a search box.
4. Apply an eligibility rule reused by the home and subscription screens.
5. Convert an article timestamp into the wording required by one screen.
6. Decide whether recent searches survive process removal and appear on another device.
7. Receive a tap on the bookmark icon.
8. Authoritatively change the saved status of an article.

### Expected reasoning

1. **UI:** loading is presentation state.
2. **Data:** source reconciliation belongs with data ownership.
3. **UI by default:** it is interaction state, unless other requirements give it application meaning.
4. **Domain is justified:** reuse across UI consumers gives the operation a meaningful boundary; Data still supplies application data.
5. **UI:** the transformation is screen-specific.
6. **Requires more context:** this is a product requirement, not an implementation detail. Cross-process or cross-device survival would require Data-layer ownership and suitable persistence/synchronization.
7. **UI:** the interaction originates there; handling the business change belongs elsewhere.
8. **Data / SSOT:** mutation must pass through the authoritative owner.

### Review guidance

A strong answer explains *why*, not merely a layer name. Accept a different placement when the learner states a credible requirement that changes meaning, reuse, or lifetime. Reject answers that put all “state” in UI, all “logic” in Domain, or all work in Data without distinguishing presentation from application rules.

## Exercise 2 — Review a fat Activity

### Task

Review this conceptual Kotlin sketch. It is deliberately incomplete and does not demonstrate Android APIs.

```kotlin
class ArticleActivity {
    private val network = ArticleNetworkSource()
    private val database = ArticleDatabaseSource()
    private var articles: MutableList<Article> = mutableListOf()

    fun onStart() {
        val remote = network.fetchArticles()
        articles = if (remote.isNotEmpty()) remote else database.readArticles()
        render(articles)
    }

    fun onBookmarkTapped(id: String) {
        val article = articles.first { it.id == id }
        article.isBookmarked = !article.isBookmarked
        database.write(article)
        network.send(article)
        render(articles)
    }
}
```

Identify at least five responsibility or ownership violations. Propose boundaries and describe the resulting state/action flow. Do not choose libraries or write a full implementation.

### Expected reasoning

A complete review should identify these concerns:

- a system-controlled UI component owns mutable application data;
- UI accesses concrete network and database sources directly;
- source selection and fallback policy are embedded in UI;
- UI mutates bookmark data, so it competes with persistence as an owner;
- there is no explicit SSOT or conflict policy between local and remote values;
- a business operation is coupled to a lifecycle callback;
- rendering uses a mutable application model rather than a stable UI-state snapshot;
- failure and partial-success cases can leave sources and UI inconsistent.

A better boundary gives the Data layer responsibility for article data, bookmarking, source coordination, and conflict resolution. The UI renders state and forwards the bookmark action. The flow is: Data owner exposes articles → UI state is produced → UI renders → tap becomes a bookmark request → Data owner applies/reconciles it → updated articles produce new UI state.

### Review guidance

Look for ownership and failure reasoning, not only “move code to a ViewModel.” Naming a framework type does not decide where source reconciliation or business mutation belongs. A strong answer also distinguishes component recreation from process removal and says that persistent survival depends on product requirements and storage, not simply on moving the list to another in-memory object.

## Exercise 3 — Design feature boundaries

### Task

Design the layer boundaries for a simple event-booking feature:

- a screen shows events from local and remote sources;
- users can reserve a seat;
- reservation is allowed only when the user is signed in and capacity remains;
- the same eligibility rule will soon be used by the event list and event details screens;
- confirmed reservations must remain visible after process removal and during temporary network loss;
- a selected filter chip only affects the current screen.

Provide:

1. the owner of each important state or rule;
2. dependencies between UI, optional Domain, Data, and data sources;
3. the SSOT for confirmed reservations;
4. the UDF cycle for a reserve action;
5. one deliberate simplification or trade-off.

### Expected reasoning

- **UI:** renders event/reservation UI state, owns the current screen's filter selection, and sends reserve intent.
- **Domain:** a focused reservation-eligibility operation is justified because the rule combines account and capacity data and is reused by two screens.
- **Data:** repositories own event, account, and reservation data; they coordinate local and remote sources and expose application-facing values.
- **SSOT:** a local persistent reservation source is a reasonable authority because confirmed state must survive process removal and remain readable offline. Remote synchronization updates that authority according to an explicit conflict policy.
- **Dependencies:** UI → Domain operation → Data boundaries → sources. Data and Domain do not depend on screens.
- **UDF:** reservation/UI state flows to the screen → user selects reserve → intent goes to the eligibility/booking operation → Data owner validates and records the result → updated reservation data flows back → UI renders it.
- **Trade-off:** keep the filter local because it has no application meaning; avoid adding a Domain operation for simple event reads if UI can use a clear Data boundary directly.

### Review guidance

A strong design derives the optional Domain layer and persistence choice from stated requirements. It does not claim that every app needs the same database, repository count, or strict Domain-only access. Verify that the proposed SSOT is truly authoritative, source conflicts have an owner, and the UI cannot confirm a reservation by changing only its local copy.
