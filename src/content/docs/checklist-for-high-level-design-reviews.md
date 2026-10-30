---
title: "High-Level Design Review Checklist"
description: "What a high-level design review should establish: scope, system boundaries, major components and how the pieces will be verified."
slug: "checklist-for-high-level-design-reviews"
draft: false
tableOfContents: true
---

A high-level design review is about shape rather than detail. This checklist keeps it at that level while still producing decisions that can be verified later.

## Checklist for High-Level Design Reviews
### Structure
A reviewer checks whether the design decomposes far enough for the next phase to start. If detailed design cannot begin because a major component stays undefined, the review fails. The high-level design should name the components, their boundaries, and how they talk to each other. Vague decomposition forces developers to invent structure mid-build, and then integrations fight each other.
### Data
Parameterize global constants and passed data rather than embedding them. A Script Include that hardcodes a sys_id, table name, or endpoint breaks as soon as the code moves to another instance. Promote such values into system properties, one property per setting, so an admin retunes behavior without editing script. Parameterized data also lets one artifact serve several domains.
### Correctness and Completeness
Correctness in a design means the parts fit the requirements without a gap. Completeness means every requirement has an owner component. Walk the requirement list against the design and mark each one. A missing piece here costs far more than a missing paragraph, because development builds on the gap for months before anyone notices.
### Standards and Traceability
The design must follow the platform standards the programme already agreed: naming, scope placement, error handling, and where logic belongs. Traceability ties each design element back to a requirement ID. Without that link, a reviewer cannot tell whether the design covers the scope or quietly drops part of it.
### Interfaces
Each interface should carry the minimum data it needs and nothing more. Fat payloads slow integrations and enlarge the attack surface. A reviewer names every interface, the direction of the call, the protocol, and the error path. If an interface has no defined failure behavior, the design is incomplete. A RESTMessageV2 call that times out with no retry strands its request record.
### Robustness
Robustness covers self-test, fail-safe, and degraded mode. A design should state how the system proves it is healthy. It should state what the system does when a dependency dies, and which features it drops first. Flow Designer subflows that skip error handling leave orphaned context records behind. If the design says nothing about degraded operation, the first outage forces an improvised fix.
