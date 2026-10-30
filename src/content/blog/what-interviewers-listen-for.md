---
title: "What Interviewers Listen For in Failure Answers"
description: "Integration failure questions are really one question: can you detect, contain and reconcile? The four-part answer that signals real experience."
date: 2026-09-24
tags: ["interviews", "integrations", "career"]
draft: false
---

Ask a candidate how to build an integration. Most people answer well. Ask what happens when the integration half-succeeds. The room gets quiet.

That silence is why failure questions dominate integration interviews. You can learn the mechanics of an API call in an afternoon. Handling 400 records that moved and 60 that did not is a judgement call. Judgement is what the interviewer measures.

## The four-part answer

Structure every failure answer the same way:

1. **Detect** — how would you know it failed?
2. **Contain** — how do you stop the damage spreading?
3. **Alert** — who finds out, and how fast?
4. **Reconcile** — how do the two systems agree on the truth again?

Candidates skip detection. Detection decides whether the failure reaches a customer or a monitoring channel.

## Partial success is the real question

A total failure is easy. Nothing moved, you retry, and you are done. Partial success is the hard case. Some records arrive and some do not. The integration's own status field says "success" because the loop completed.

The answer interviewers want to hear: track the outcome of each record, not the outcome of the run. A run that processed 460 records with 400 successes and 60 failures is not a success. It is 60 pieces of work.

```javascript
var ok = 0, failed = 0, errors = [];
for (var i = 0; i < payloads.length; i++) {
  try {
    send(payloads[i]);
    ok++;
  } catch (e) {
    failed++;
    errors.push({ id: payloads[i].id, why: e.message });
  }
}
gs.info('[sync] ok=' + ok + ' failed=' + failed);
if (failed > 0) {
  gs.error('[sync] failures: ' + JSON.stringify(errors).slice(0, 2000));
}
```

Two counters and a reason list turn an invisible failure into a work item.

## Retries need a reason to be safe

"Retry three times" is a sentence that means nothing without idempotency. If the target system creates a new record on every call, a retry after a timeout can create a duplicate of a record that succeeded.

So the strong answer mentions a key. The sender includes an identifier that the receiver can recognise. The receiver treats a repeat of that identifier as the same operation. Then a retry is safe, and a timeout stops being ambiguous.

Without a key, say so plainly. Retries are only safe on operations that are naturally idempotent, such as an update to a known record.

## Silent emptiness is the failure nobody catches

The worst case fails silently. The response is empty. The code takes the "no work" branch, and every counter shows zero and green.

The answer: assert on volume where you expect volume. If the nightly sync usually moves 400 records, a run that moves zero is an incident. That run throws no exception.

## Backoff is a courtesy and a control

A retry that starts immediately against a struggling endpoint makes the problem worse. A longer gap between attempts gives the far side room to recover. A longer gap also caps the damage that your integration can do to another system.

The interviewer listens for one thing. Do you treat the other system as a partner with limits, or as an endpoint that owes you a 200?

## How to answer when you have not done it

Say what you would check and in what order. Then say what you have not yet run in production. A guess at experience is easy to detect and expensive to repair. A clear method and an honest gap read as competence.

## Sources

- REST and SOAP integration mechanisms, and integration error records, are documented in the ServiceNow product documentation: [servicenow.com/docs](https://www.servicenow.com/docs/) — behaviour differs by release and by integration type.
- The GlideAjax API reference lives in the platform API documentation on the same site; use the page for your own release rather than a remembered path.
