---
title: "Debug in Order, Not by Instinct (panel rewrite sample)"
description: "Sample rewrite: the same four-step debugging order, restructured into panels that match the visual explainer page."
date: 2026-10-30
tags: ["debugging", "platform", "practice"]
draft: true
---

> **Visual version:** [open the one-page explainer](/explainers/debug-in-order.html) for the flow diagram and the tool-selection table.

The fastest fix usually follows a deliberate order. Most slow debugging sessions do not lack skill. They lack sequence. A developer changed one line to see what would happen, the symptom moved, and now two variables are unknown instead of one.

Language designers spend their working lives in other people's broken code. Their order is worth copying. It has four steps.

## The order, and the step people skip

1. Reproduce on demand.
2. Narrow to one layer.
3. Instrument, do not speculate.
4. Explain, then fix.

A developer who skips the middle starts changing code before the record has a name and a value. The symptom moves. The next change hides the first one. The bug comes back a week later, because nobody wrote down what it was.

## Step one: reproduce on demand

You cannot prove a fix for a bug that you cannot reproduce. Before you change code, get one record and one field to show the wrong value. Do this on purpose, two times.

Write the reproduction down. Do not write "the incident form misbehaves". Write this: incident INC0012345, field `assignment_group`, expected A, actual B, after a save by a user with role X. That sentence is the foundation of the whole investigation. It costs two minutes.

> A reproduction that a second person can run is evidence. A reproduction that only you can run is a memory.

## Step two: narrow to one layer

A record moves through the platform in a sequence. Every step can change it:

- client-side validation and client scripts
- business rules, in their order
- workflow or flow actions
- asynchronous processing after the transaction commits

Name the step that you think produced the wrong value. If you cannot name it, you have not found the bug yet. After this point, everything is a guess.

The useful habit here is halving. Disable the suspect rule and run the reproduction again. If the value is now correct, the fault is in that rule or after it. If the value is still wrong, the fault is earlier. Two or three halvings usually land on the line.

## Step three: instrument, do not speculate

Add logging at the point where the value is set. Read the value back. The value before and the value after are the evidence. Everything else is a theory.

```javascript
gs.info('[dbg] before=' + JSON.stringify(current.getValue('assignment_group')));
// ... the logic under test ...
gs.info('[dbg] after=' + JSON.stringify(current.getValue('assignment_group')));
```

Include the record identifier in every line. A log line that you cannot attach to a record is a line that nobody will use.

## Choose the tool by the question

Two tools answer two different questions. If you swap them, you waste an afternoon.

| Question | Tool | Why |
| --- | --- | --- |
| What already happened, in a transaction that has finished? | Script Tracer | The record is history; there is nothing live to attach to. |
| What is happening at this exact line, right now? | Script Debugger | You need to inspect variables mid-execution. |
| Does it only fail under production traffic? | Tracer, plus logs | You cannot attach a debugger to a user's transaction. |

The classic dead end is a step-through of an intermittent bug. The debugger attaches too late, and the failing transaction is already gone. The other dead end is a trace for a bug that never reproduced. That trace gives a confident explanation for something that did not happen.

## Step four: explain before you fix

Write one sentence: "the value is wrong because rule A runs before rule B, so B reads a stale field."

If that sentence is hard to write, stop. The diagnosis is not finished. If that sentence is easy to write, the fix is usually clear and small. That small fix is exactly what you want in a review.

## Production has one extra rule

Do not change behaviour to collect evidence. Use traces, system logs and read-only queries. Put diagnostic logging behind a level that you can turn off. Turn it off when you verify the fix. Permanent debug logging is noise and a cost.

Some faults need a write to reproduce. For those faults, move to a sub-production instance and copy the record shape with it. A record that does not match the production field set will not reproduce the production bug.

## Sources

- Script Tracer and Script Debugger are documented in the ServiceNow product documentation: [servicenow.com/docs](https://www.servicenow.com/docs/) — read the page for your own release.
- Free developer instances for reproduction work: [developer.servicenow.com](https://developer.servicenow.com/dev.do)
