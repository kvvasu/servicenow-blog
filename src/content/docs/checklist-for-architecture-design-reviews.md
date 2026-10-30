---
title: "Architecture Design Review Checklist"
description: "A checklist for reviewing ServiceNow architecture designs: integration boundaries, data ownership, scaling assumptions and each decision's failure mode."
slug: "checklist-for-architecture-design-reviews"
draft: false
tableOfContents: true
---

Architecture review is where expensive decisions become visible. This checklist concentrates on boundaries and failure modes, because those are the decisions that are hardest to reverse.

## Checklist for Architecture Design Reviews
### Structure
A design review starts by asking whether the proposed architecture can satisfy every requirement. Reviewers trace each element back to a need, then mark anything that has no home. Missing pieces usually hide in the gaps. No story covers data archival, and no owner signs off on license count. No path handles a record that an integration user creates. A reviewer who accepts a diagram without mapping requirements lets those gaps reach the build phase, where the cost multiplies.
### Correctness
Correctness asks whether the design meets reliability and performance targets before code exists. A reviewer checks expected volumes, peak load, and recovery after failure. On ServiceNow, ask how many records the table will hold and which Business Rules fire on insert. Then check how a job behaves when the MID Server drops offline. A design that ignores throughput produces queries that time out in production, and the fix usually requires rework of the data model.
### Standards and Traceability
Traceability links every design decision to a stated requirement or a documented standard. Without it, no one can prove the build matches what the business asked for, and scope creep hides behind vague modules. A review should verify that each requirement maps to a table, a Flow, or an interface, and that naming follows platform conventions. On ServiceNow, that means correct table prefixes, clear sys_scope values, and update sets belonging to one application.
### Logic
Logic review hunts for states the designer never considered. Ask what happens when a record already exists, when two approvals arrive at once, or when a required field stays empty. On the platform, a before Business Rule can assume a valid current value and throw on insert. A loop that calls GlideRecord inside itself consumes the transaction quota. Reviewers walk each branch aloud, including the error path, because untested branches reach production as incidents.
### Interfaces
Each interface should pass the minimum data needed and nothing more. Sending a whole record where two fields suffice exposes values the caller has no right to read and couples systems together. Reviewers check direction, format, error contract, and identity. A Scripted REST API must define who authenticates, what happens on a bad payload, and which response code the caller sees. Loose interfaces cost more to maintain, because every change ripples into systems the team does not own.
### Clarity
A design that nobody can follow will fail in someone else's hands. Reviewers judge whether the document shows data flow, control flow, and interfaces without requiring an author to explain them in person. Diagrams need labels that match real table names, and sequence of execution must appear. Vague wording such as correct handling or proper validation tells the next developer nothing and forces guesswork during an incident at night.
