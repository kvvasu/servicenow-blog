---
title: "The Empty Array That Lies to You"
description: "Why an empty array can read as false in one ServiceNow execution context and true in another, and the three-state check that ends the ambiguity."
date: 2026-10-28
tags: ["javascript", "integrations", "debugging"]
draft: false
---

An integration returns nothing. There is no exception, no error record and no retry. The scheduled job reports success and continues. Three weeks later, somebody sees that no records have moved since the last release.

I have seen this failure reported as a platform bug, as a browser bug and as a vendor problem. It is none of those. It is a disagreement about the meaning of an empty container. The disagreement only becomes visible when a value crosses from one execution context to another.

## Two rules, one value

ECMAScript defines the rule clearly: an empty array and an empty object are both truthy. So `if ([])` takes the true branch, and `if ({})` does the same. Every browser follows that.

Legacy server-side modes in the platform have not always agreed. In older engine modes, an empty array can evaluate as false. ES12 mode is closer to the specification. ServiceNow warns that a mode change can change the outcome of existing scripts. That warning is the whole story. The fix is not a setting. The fix is a test pass.

## Why the symptom appears so far from the cause

An empty response is not an error. Nothing throws, nothing logs and nothing alerts. The code takes the false branch. It decides that there is no work to do, and it exits cleanly. The script reports success. From the point of view of the script, that report is true. The script did exactly what it was told.

That is why this class of bug survives a review. The reviewer reads `if (result)` and sees a guard clause. The bug lives in the gap between the two meanings of the guard.

## Three states, not two

If you collapse these states, you lose the information that you need to react correctly:

- **Missing** — the key never arrived. Something upstream changed its contract.
- **Empty** — the key arrived and the answer was "nothing". This is a valid answer.
- **Invalid** — the key arrived with the wrong shape. This is the one you must not ignore.

Each state needs a different response. Missing means fix the contract. Empty means decide whether zero is acceptable. Invalid means stop and log the payload that you received.

## The check I use

```javascript
function isFilledArray(value) {
  return Array.isArray(value) && value.length > 0;
}

if (!isFilledArray(result)) {
  gs.warn('empty or malformed response: ' + JSON.stringify(result).slice(0, 500));
  return;
}
```

`Array.isArray` answers the shape question. `length > 0` answers the emptiness question. Neither call asks the engine about coercion. That is the point.

On the client side, use the same discipline one layer out. A client-callable script include should always answer in the same envelope, with a success field. Then the caller tests a field and not a value:

```javascript
// server: always answer in this shape
{ ok: true,  data: [] }
{ ok: false, error: 'reason' }

// client: decide on the field, not on the payload
if (!answer || answer.ok !== true) { /* handle */ }
```

The envelope costs two lines. It removes the whole ambiguity class from the integration.

## What makes silence impossible

Check the counts. An integration that reports success and moves zero records is worse than an integration that fails. A failure is visible. Log the record count on every run. Set an alert for zero when zero is unexpected. If the count is the only number in your log, it is also the only number that you will read.

Then run the integration test again in both engine modes. Do not do this because one mode is wrong. Do it because the difference between the modes is the fault that you want to catch.

## Sources

- ECMAScript 2021 language specification: [262.ecma-international.org/12.0](https://262.ecma-international.org/12.0/)
- MDN on truthiness: [Glossary: Truthy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy)
- MDN on Boolean coercion: [Boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Boolean)
- ServiceNow product documentation for engine-mode behaviour: [servicenow.com/docs](https://www.servicenow.com/docs/) — read the current release notes before you change modes.
