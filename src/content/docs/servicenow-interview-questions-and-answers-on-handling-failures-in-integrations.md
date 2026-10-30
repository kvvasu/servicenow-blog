---
title: "Interview Questions: Integration Failures"
description: "Interview questions on integration failure handling: retries with backoff, partial success, idempotency and how to make a silent failure visible."
slug: "servicenow-interview-questions-and-answers-on-handling-failures-in-integrations"
draft: false
tableOfContents: true
---

Failures in integrations are the topic candidates most often bluff, and interviewers know it. These questions concentrate on the scenarios where a naive answer breaks: partial success, duplicate delivery and silent emptiness.

## ServiceNow Interview Questions and Answers on Handling Failures in Integrations
Integration failures come from three places: the remote system, the credential, and the mapping. A good answer describes how to detect each one. Check the outbound REST message log and the ecc_queue table for the failing record. Confirm the integration user still holds the right role, because a password reset or a role change breaks a job silently. Then verify the payload fields against the target schema. Retry logic and idempotency decide whether a repeat delivery corrupts data or simply succeeds.
### ServiceNow Interview Questions and Answers on Handling Failures in Integrations
### 1. Network Failures
Network trouble stops an integration before any business logic runs. A MID Server fails DNS resolution, a firewall drops packets, or TLS negotiation breaks because the external certificate expired. RESTMessageV2 then raises an exception, and the payload never leaves the instance. When the script swallows that error, nobody notices until the business process stalls. Log the fault, queue a retry with backoff, and alert the integration owner so a transient outage stays transient.
### 2. Node Failures
ServiceNow runs as a cluster, and a single node can stop responding without warning. A scheduled job or inbound REST call that begins on the failed node aborts mid-transaction, leaving records half written. Sessions bound to that node reset, so users lose unsaved form data. The load balancer usually routes around the bad node, yet long-running scripts may not recover cleanly. Make integrations idempotent, so a replayed call does not duplicate work.
### 3. Service Failures
The endpoint itself goes down, or the instance saturates and slows its own outbound calls. A REST or SOAP request then returns 503, or the semaphore limits queue requests and records wait in an intermediate state. Heavy traffic from one integration starves the others sharing the same node. Throttle outbound calls during peak hours, honor Retry-After headers, and keep payloads small. Unlimited outbound volume protects nobody and degrades the whole instance.
### 4. Dependency Failures
An integration depends on systems the instance does not control. An external API returns malformed JSON, an update set ships a plugin that is not yet activated, or a shared credential rotates without notice. The script then parses nothing and writes empty values into production tables. Validate the response before mapping, check plugin activation during deployment, and fail loudly when a dependency misbehaves instead of storing junk.
### 5. Data Inconsistencies
Bad data damages more than downtime does. A payload field changes type, a transform map maps the wrong source column, or two flows update the same record and the last write wins. Validation rules and transform maps catch shape errors, but they miss semantic drift. Compare record counts, reconcile keys, and store rejected rows in a staging table. Silent mismatches corrupt reporting, and nobody finds them until an audit does.
### 6. Configuration & Deployment Errors
Most production failures trace back to configuration, not code. Someone points an endpoint at the test system. Another admin stores an expired credential in a connection alias, or promotes an update set whose script references a field the target instance lacks. The call fails on its first run in production. Keep connection details in aliases, test the update set in a sub-production instance, and move credentials separately from logic.
### 7. Time-Related Issues (Clock Skew, Timeouts)
Timestamps break integrations quietly. Two systems run different clocks, so a record written at 10:00:03 on one host looks newer than its 10:00:01 copy elsewhere. Incremental syncs then skip rows or replay them forever. Timeouts cut the other way: a call needing ninety seconds dies at sixty, while the remote system finishes the work anyway. Standardize on UTC and set timeouts above the expected response time.
### Cross-cutting Concerns
One shared error table beats logging scattered across scripts. Create a custom table holding integration name, direction, endpoint, payload, error message, and retry state. Write to it from every RESTMessageV2, flow, and transform script. Support staff search one place instead of opening logs on both the MID Server and the instance. Add a scheduled retry job and alert when the same failure repeats.
