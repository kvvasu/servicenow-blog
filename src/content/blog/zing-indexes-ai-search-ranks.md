---
title: "Zing Indexes, AI Search Ranks"
description: "Zing decides what can be found; AI Search decides what is shown. Separating the two stops you tuning the wrong layer when search disappoints."
date: 2026-10-15
tags: ["search", "ai", "platform"]
draft: false
---

When someone says "search is broken", they mean one of two different things. A record that a user should find does not appear at all. Sometimes the record appears in the list, but in an unhelpful position. Those are different faults in different layers. The fix for one does not help the other.

The confusion is easy to understand. Two names cover one stack, and people use the names as if they mean the same thing.

## The split

**Zing** is the indexing engine. It decides which content users can find and how quickly a query reaches the content. If the index has not seen a record, no amount of ranking work will show the record.

**AI Search** is the product layer above it. It decides which records appear and in what order. It uses the indexed content as raw material.

So a missing-result complaint is usually an indexing problem. A ranking complaint is usually a search-configuration problem. Diagnose which one you have before you change either one. The tools are different, and the settings do not overlap.

## The one test that tells them apart

Take the failing query and try one unambiguous term that must exist in the record. If the record still does not appear, the index is the problem. If it appears, the index is fine. Then you are looking at ranking, filtering or interface scoping.

That test costs thirty seconds and removes half the guesswork.

## Ranking complaints are interface complaints too

The same index gives different results, depending on where the user searched. Each of a portal search, a workspace search and a global search can apply different filters and different sources.

So when a user reports missing results, reproduce the query in the interface that the user used. A result that appears in one interface and not the other is not an index fault. It is a filter or a source configuration.

## Tune against evidence, one change at a time

Search is an area where two edits at the same time make the outcome impossible to attribute. Keep it boring:

1. Capture the failing query and the current result order.
2. Change one setting.
3. Re-run the same query and compare.
4. Record what you changed and why, in the change record, not in a notebook.

Keep a short list of real queries from real users. It is the only objective test that you will have after the tuning change. Most teams forget to build the list until they need it.

## Should you migrate?

Migrate for a stated reason. Two are honest:

- ranking quality on a defined query set is measurably worse than you need
- a capability you require does not exist in your current setup

Everything else is motion. A migration without a measurement plan replaces one unknown with another. Then you cannot say if the change helped.

Availability and entitlement decide this more often than capability does. Know which features your instance can run before you design around a feature. Treat every licensing figure that you read online as a claim to discuss with ServiceNow. That rule also applies to the figures in this post.

## What to keep in the runbook

- Missing result: look at the index first, and the interface second.
- Wrong order: look at ranking and sources, not the index.
- Tuning: one change, one query, one comparison.
- Migration: name the measurement before you name the plan.

## Sources

- AI Search and Zing configuration are documented in the ServiceNow product documentation: [servicenow.com/docs](https://www.servicenow.com/docs/) — release-specific behaviour changes, so read the page for your own release.
- Licensing and entitlement claims in this post are deliberately unquantified. Ask ServiceNow about them before you design around a feature.
