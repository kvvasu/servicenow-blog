---
title: "Requirements Review Checklist"
description: "What to check in a ServiceNow requirements review: traceability, testable acceptance criteria, non-functional requirements and scope boundaries."
slug: "checklist-for-requirements-reviews"
draft: false
tableOfContents: true
---

Requirements reviews are cheap and late changes are expensive, so the checklist exists to find the gaps while they are still cheap. This page covers the areas worth checking before design starts.

## Checklist for Requirements Reviews
### Organization and Completeness
A reviewer first asks whether the document holds together as a whole. Every cross-reference to another requirement should point at an existing, correctly numbered item. The sections should cover the full scope the introduction promises, with no orphaned headings and no duplicated statements. A dangling reference wastes a developer's time later, and it usually signals that someone deleted a requirement without cleaning up its dependents.
### Correctness
Correctness asks whether each requirement is true, buildable, and free of conflict. Two requirements demanding opposite behaviour force a developer to pick one and hope. A duplicated requirement doubles the test effort for the same behaviour. Reviewers should read the whole set, flag contradictions, and merge overlaps. A conflict caught at review costs a comment; the same conflict caught at user acceptance testing costs a release.
### Quality Attributes
Quality attributes cover what requirements usually omit: security, performance, availability, and safety. A requirement that never names who may read the record leaves the access control decision to whoever writes the ACL. One that ignores expected volume fails under real load. Reviewers should ask what happens when the system is slow, unavailable, or attacked, then record the answer as a testable requirement.
### Traceability
Every requirement needs one stable identifier that nobody reuses later. Numbers that shift when someone inserts a paragraph break links from design documents, test cases, and defect reports. The reviewer confirms each identifier is unique, that downstream artifacts reference it correctly, and that the set contains no gaps. Traceability is what lets a team prove later that each requirement was built and verified.
### Special Issues
Requirements describe what the system must do, not how to build it. A document that names a specific table, script include, or two-step workflow removes the team's freedom to choose a better design. It also hands the team a maintenance burden. Reviewers should restate those lines as outcomes, push the implementation detail into the design document, and keep the requirement verifiable from outside the code.
