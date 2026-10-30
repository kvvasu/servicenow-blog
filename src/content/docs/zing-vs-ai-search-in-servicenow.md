---
title: "Zing vs AI Search"
description: "How Zing indexing and AI Search differ in architecture, ranking, linguistics and tuning, and which one a given instance should run."
slug: "zing-vs-ai-search-in-servicenow"
draft: false
tableOfContents: true
---

Zing is the indexing engine underneath search on the platform; AI Search is the product layer people actually use. Confusing the two leads to tuning the wrong thing, so this page separates the architecture, the feature differences and the practical migration question.

## Zing vs. AI Search in ServiceNow
Zing and AI Search solve the same problem through different machinery. Zing is the platform's long-standing text search engine; it indexes records and ranks keyword matches. AI Search sits on a newer framework of search profiles, search sources, and search applications, and it handles relevance tuning that plain keyword matching cannot. Licensing differs too, so a team must choose deliberately instead of inheriting a default.
## Zing vs. AI Search in ServiceNow
### Executive Summary
Zing is the original keyword search that ships with the core platform and matches text terms. AI Search adds natural-language understanding, typo tolerance, and Genius Results cards that resolve intent instead of matching strings. AI Search needs a higher license tier, so many organizations run Zing by default. Search quality shapes how quickly employees find answers, and poor results drive users back to phone calls and chat.
### 1. Core Architecture & Technology
| Feature | Zing (Legacy) | AI Search (Modern) |
| --- | --- | --- |
| Search Method | Keyword Matching: Relies on finding exact words or stemmed variations (e.g., "printing" matches "print") within the text index. | Intent & Semantic Search: Uses Natural Language Understanding (NLU) to understand the meaning of a query, not just the words. |
| Indexing | Uses the ts_index table. Indexing happens automatically on task tables when the "text index" attribute is checked. | Uses Indexed Sources. Data is ingested into a separate index structure optimized for ML. Requires explicit configuration of what tables to index. |
| Relevancy Scoring | Static: Based on frequency (TF-IDF), sequence, and field weight (e.g., Short Description > Work Notes). Scores do not change automatically. | Dynamic (ML): Learns from "Search Signals" (clicks, successful sessions). If users constantly click the 3rd result for a query, AI Search promotes it to 1st over time. |
| Content Scope | Strictly internal ServiceNow tables. | Internal tables + External Content (SharePoint, Confluence) via connectors (requires configuration). |
### 2. Feature Comparison
### A. User Experience (UX)
AI Search returns Genius Results cards that answer a question directly, showing a formatted KB article or record above the hit list. It corrects typos and completes queries as someone types. Zing relies on exact terms, so a misspelling returns little or nothing. Auto-complete in Zing suggests known terms but does not interpret intent. The gap matters most on self-service portals, where users type support questions in plain language.
### B. Linguistics & Language Support
Zing applies basic stemming, which strips word endings for English, French, and German. That helps when a user pluralises a term, but it fails on synonyms and phrasing. AI Search uses a language model to map meaning. A search for "laptop won't charge" matches an article titled "battery not powering on." It also handles non-English content better. A multilingual portal therefore gains far more from AI Search than a single-language one.
### 3. Configuration & Administration
### Tuning Search
Zing tuning happens through stop words, which the engine ignores, and synonyms, which map terms such as laptop and notebook. An admin edits those records to change what a keyword query returns. AI Search tunes differently, through search profiles, search sources, boosting rules, and per-language relevance settings that shape result order. Both reward iteration against real query logs, because guesses about user vocabulary usually miss.
### Troubleshooting
Zing debugging relies on text search debug properties. Turning them on shows why a document matched, the computed score, and which fields the indexer read. AI Search troubleshooting moves through search analytics, the query log, and the search profile that shaped the request. A term that returns nothing often points at a stale index or a source that stopped crawling, so check indexing before rewriting the query.
### 4. Licensing & Availability
Zing ships free with every ServiceNow instance as core platform search. AI Search usually requires a Pro or Enterprise package, such as ITSM Pro or CSM Pro, and often counts as a premium capability. Cost drives the decision for many organizations, and Standard license holders keep Zing by default. Some limited AI Search functionality appears without the premium tier, so confirm current entitlement before you promise features to stakeholders.
| Product | Availability / Cost |
| --- | --- |
| Zing | Free / Core Platform. Included with every ServiceNow instance (Standard, Pro, Ent). |
| AI Search | Paid / Premium. Generally bundled with Pro and Enterprise packages (e.g., ITSM Pro, CSM Pro, HRSD Pro). Note: Some basic AI Search capabilities may be present in Next Experience, but advanced features (External connectors, full tuning) usually require the AI Platform license. |
### 5. Where do they appear? (UI Context)
Modern portals such as Employee Center and CSM Portal use AI Search as the default experience. The classic platform backend, including the top-right global search box, still relies on Zing. Agents working in the classic UI therefore get keyword results, while employees on the portal get AI Search. Teams comparing search behaviour across those two surfaces often see different results for identical queries, which confuses tuning and testing.
### 6. Migration Recommendation
Move to AI Search when the organization holds Pro or Enterprise licensing and runs a modern portal. The migration pays off when users struggle to find answers and self-service adoption lags. Stay on Zing if the instance runs on Standard licensing, traffic is low, or the classic UI dominates. Plan a pilot on one portal, measure deflection, and expand only when results improve.
