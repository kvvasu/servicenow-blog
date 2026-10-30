---
title: "Detailed Design Review Checklist"
description: "Detailed design review points for ServiceNow work: table choices, permission model, script placement and the data migration path."
slug: "checklist-for-detailed-design-reviews"
draft: false
tableOfContents: true
---

Detailed design decides how the build will be maintainable. This checklist covers the choices that are cheap now and painful to change once data exists.

## Checklist for Detailed Design Reviews
### Structure
Detailed design must hold one level of detail throughout. A document that names individual methods in one section and waves at whole subsystems in the next leaves the implementer guessing. Split or merge parts until each carries the same weight. Reviewers cannot estimate effort or spot gaps when granularity shifts without reason.
### Data
Fill every gap the system data description left open. Name each new field, its type, its source and whether it can hold null. State which roles may read and write it. Missing detail here surfaces at build time, when a developer invents a value and the schema drifts from the approved model.
### Correctness and Completeness
Check that the detailed design implements the high-level design with no gaps and no extras. Link each requirement to a module and each module back to a requirement. An unimplemented requirement ships as a defect. An unrequested feature adds maintenance cost and risk that no reviewer approved, and it hides in the same diff.
### Standards and Traceability
Verify the design follows the naming, logging and error-handling standards the team adopted. Link every element to the requirement it satisfies, and note any deviation with its reason. Traceability lets a later change find each affected part. Without it, a reviewer approves work on trust and the first audit finds the gap.
### Robustness
Design must handle failure without destroying data. State what happens when a call times out, a record is missing, or input arrives malformed. The system should log the fault, keep the last good state, then recover or retry. A design that assumes success passes the demo and corrupts records in production.
