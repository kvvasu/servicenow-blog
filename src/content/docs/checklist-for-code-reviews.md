---
title: "Code Review Checklist"
description: "A ServiceNow code review checklist: query performance, error handling, logging, permission safety and the tests that prove the change works."
slug: "checklist-for-code-reviews"
draft: false
tableOfContents: true
---

Code review is the last cheap place to catch a production problem. This checklist focuses on the platform-specific risks that general review advice misses.

## Checklist for Code Reviews
### Structure
A reviewer first asks whether the script does what the design says. On the platform that means naming the intended table, the trigger, and the condition before reading any code. A Business Rule set to run on insert and update when the design wanted insert only rewrites history on every save. Check the method boundaries too. One giant script include that queries five tables hides the failure and blocks testing.
### Documentation
Comments explain intent, not syntax. A reviewer wants to know why a script include bypasses an ACL, or why a scheduled job skips empty records. ServiceNow keeps description fields on Business Rules, script includes, and flows. Put a short purpose statement there, plus a worked example, so the next admin finds it. Reference the requirement that drove the change. Undocumented custom logic becomes untouchable, and untouchable code never gets safely refactored.
### Variables
Names carry the review. A variable called gr tells a reader nothing, while currentIncident reads on its own. Declare variables close to first use with let or const, and avoid reusing one name for a record and then a string. Watch for accidental globals, because a missing declaration attaches to the shared scope and leaks between records in the same transaction. A leftover global can corrupt a later record.
### Arithmetic Operations
Comparing floating-point values for equality breaks, because binary cannot represent most decimals exactly. Test a tolerance instead, or compare rounded values. The same trap appears with currency and duration fields, where arithmetic on two decimals leaves a surprise tail. ServiceNow provides GlideDuration and GlideDateTime for time math, so use those rather than subtracting raw numbers. Silent rounding errors surface later as reconciliation disputes nobody can trace.
### Loops and Branches
A loop over a GlideRecord walks a cursor, so a nested query on the same table can move the outer pointer and skip records. Break out early once the query finds its target, because an unbroken while can run until the transaction times out. Confirm every branch has a reachable exit and every else covers the remaining cases. Off-by-one faults at a boundary usually hide in the condition, not the body.
### Defensive Programming
Query results and arrays do not always hold what the code assumes. Check length before indexing, and confirm a GlideRecord query returned a row before reading getValue. A null from a missing field becomes the string null when concatenated, then lands in a notification or an outbound payload. Validate input at the boundary where it enters, whether that is a Scripted REST API body or a catalog variable. Guards cost one line.
