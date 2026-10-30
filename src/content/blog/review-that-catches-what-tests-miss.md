---
title: "The Review That Catches What Tests Miss"
description: "A code review order for ServiceNow changes: query bounds, swallowed errors, permission safety and the one test that proves the change works."
date: 2026-10-08
tags: ["code-review", "checklists", "quality"]
draft: false
---

A test proves that one path works. A review is the last cheap chance to see the paths that nobody tested. That difference decides where the review time goes. Do not spend that time on style, because a formatter can fix style. Spend it on the places where a change can be wrong while every test passes.

Four checks catch most real defects in platform work.

## One: does every query have a bound?

An unbounded `GlideRecord` query is a performance incident that waits for a table to grow. Check each query and ask two questions. What limits the rows? Which index serves the query?

```javascript
var gr = new GlideRecord('incident');
gr.addQuery('active', true);
gr.addQuery('sys_updated_on', '>=', gs.daysAgoStart(7));
gr.setLimit(500);          // a ceiling, so a surprise cannot become an outage
gr.query();
```

A limit is not a substitute for a filter. A limit is a ceiling. A query that needs a limit for safety usually needs a better filter too.

Then check that the query does not sit inside a loop. One query per iteration turns a fast transaction into a slow one. The symptom appears at scale, not in the developer's instance.

## Two: does the catch block swallow the error?

```javascript
// bad: the failure becomes silence
try { doTheWork(); } catch (e) {}

// better: the failure is recorded and the caller learns about it
try {
  doTheWork();
} catch (e) {
  gs.error('[integration] order sync failed: ' + e.message);
  throw e;
}
```

An empty catch is a promise that the error did not matter. Sometimes that promise is true. Usually it is a guess that nobody revisits. Require a log line and a reason in the comment. If you cannot give a reason, require the rethrow.

## Three: is the permission model still intact?

Client-side checks run in the user's browser. The browser belongs to the user. Anything that only the browser enforces is a suggestion.

So the review must name the server-side rule that enforces the same constraint as the client script. If that rule does not exist, the review has found a real defect, not a style issue. Also check that the script runs with the privileges it needs, not with elevated rights it happens to have.

## Four: is there one test that proves the change?

Do not ask for a suite. Ask for one test, or for one written reproduction. That test must fail before the change and pass after the change. If the author cannot show that test, the change is unproven. Then the review must say so plainly.

## The order matters

Run the four checks in this order: query bounds, error handling, permissions, then the proof. The first three checks catch defects. The fourth check decides if the change is ready.

Reviewing in the other order is common and wasteful. A change with an unbounded query should not get careful comments about its variable names. Fix the blocking defect first. The naming discussion can happen later, or never.

## What to leave in the pull request

- the reproduction or test, with its result before and after
- the reason for each non-obvious choice, in one sentence
- any deliberate simplification, marked as such, with the ceiling named

That last one pays for itself within a release. A reviewer who knows the reason for a limit will not spend an afternoon on the same question.

## Sources

- GlideRecord query APIs and ACL behaviour are documented in the ServiceNow product documentation: [servicenow.com/docs](https://www.servicenow.com/docs/) — check method behaviour for your release.
- Free developer instance for reproducing a reviewed change: [developer.servicenow.com](https://developer.servicenow.com/dev.do)
