---
title: "Production-Grade Prompt Ideas"
description: "Prompt patterns that survive contact with real platform work: constrained inputs, explicit output shapes and review steps you can repeat across a team."
slug: "servicenow-production-grade-prompt-ideas"
draft: false
tableOfContents: true
---

A prompt that works once is an anecdote. These patterns are worth keeping. They constrain the input, state the output shape and leave a review step. That sequence makes the result repeatable by someone other than their author.

## ServiceNow Production-Grade Prompt Ideas
A useful prompt for platform work states the artifact, the inputs, and the constraint. Ask for a business rule on the incident table that sets a field when priority changes, and require it to run before the database write. Demand the code explain why it fires once. Naive prompts return scripts that call GlideRecord in a loop or skip ACL checks entirely. Review every answer against the instance, because a model cannot see your access rules or plugins.
### Section 1: The "Architect" Prompts - Designing for the Future
Architect prompts force design decisions before anyone opens Studio. An admin settles scope ownership, table extension points, and record ownership rules first. Skip that step and a later upgrade overwrites customizations, or two scoped apps fight over one table. Questions here cover sys_dictionary field choices, custom versus extended tables, and where a Script Include belongs. A strong answer names the concrete artifact each design choice creates.
### Principle: Security & Access Control
A new table inherits almost nothing useful. The admin defines ACLs for read, write, create, and delete, then decides which roles qualify. Forget the create ACL and any authenticated user inserts rows. Forget field-level ACLs and sensitive columns leak through list views and reports. Naming the table, the roles, and the fields in the prompt yields answers that map to real sys_security_acl records rather than general advice.
### Principle: Data Governance & Integrity
Reference qualifiers and data policies handle most integrity rules, so a Business Rule is often the wrong tool. The prompt names the source field, the target table, and the trigger moment. A before rule on insert and update keeps the value aligned. A display Business Rule does not, because it changes nothing on the stored row. Put the rule on the wrong event and reports show stale data while the form looks correct.
### Principle: Platform-Native Integration Best Practices
Outbound calls belong in RESTMessageV2 with a message record, not a raw outbound call buried inside a Business Rule. Inbound calls belong in a Scripted REST API resource, where the platform handles authentication and transaction logging. The prompt states direction, payload shape, and whether the endpoint sits behind the firewall. A MID Server covers private networks. Hardcoding credentials breaks rotation and exposes secrets through update sets.
### Principle: Automated Change Management and Risk Assessment
Change risk needs a model, not guesswork. The prompt names the CI class, the change model, and the fields that drive assessment. A developer wires risk answers to a calculated risk score, then maps that score to an approval policy. Get the CI class wrong and the change never links to the affected service. Approvers then see an empty impact tree and rubber-stamp risky work.
### Principle: Scalable & Maintainable Data Model
Adding one attribute tempts a developer to extend cmdb_ci_server directly. That choice blocks upgrades and duplicates columns across every server subclass. A better prompt asks whether the attribute belongs on the base class, a subclass, or a related table. Ask about cardinality and reporting needs before deciding. The wrong choice surfaces months later as a dictionary conflict during an upgrade.
### Section 2: The "DevOps Engineer" Prompts - Performance & Reliability
DevOps prompts target operational health: query cost, error handling, retry behavior, and job scheduling. An admin asks for the query behind a slow list, not just a fix. These prompts also cover GlideAggregate versus GlideRecord loops, setLimit discipline, and keeping a scheduled job from overlapping its previous run. Each question should name the table, the row count, and the symptom.
### Principle: Efficient Data Retrieval
A slow report usually means a full table scan or a query built inside a loop. Ask the developer to show the encoded query, the table row count, and whether an index covers the filter columns. Replacing a nested GlideRecord loop with GlideAggregate or one addEncodedQuery often removes seconds. Avoid getRowCount on large tables. Each mistake scales with data, so the report passes in test and dies in production.
### Principle: Resilient Business Rules
An after Business Rule that updates a related table runs inside the same transaction. A failure in the second update rolls back the first, so the user loses both changes and sees an error. Guard against recursion, check the current operation, and use setWorkflow(false) deliberately. The prompt should include the script and ask for recursion paths, transaction scope, and behavior when the target record sits locked.
### Principle: Secure & Maintainable Client Scripts
Client scripts run in the browser, so anyone reads them. A hardcoded sys_id or role list leaks internal identifiers and breaks when somebody clones the instance. Direct DOM manipulation breaks on the next platform upgrade because markup changes. The prompt should ask for g_form methods, a UI Policy alternative, and server-side validation for anything affecting data integrity. A client cannot enforce security.
### Principle: Batch Processing & Scheduled Jobs
A daily feed of thousands of users needs chunking, not one long loop. Set a limit, order by sys_id, and process in pages so the job releases the transaction between chunks. A single pass over thirty thousand records holds locks, times out, and rolls back everything when the last row fails. The prompt should ask about idempotency, per-row error capture, and resume after a partial run.
### Principle: Asynchronous Scripting with the Scoped Flow API
Flows run after the transaction commits, so an after Business Rule that triggers one cannot hand back a result. The prompt should ask why the caller expects a synchronous answer. Use the FlowAPI methods, capture the flow context sys_id, and write it to the record. Ask what happens when the flow fails after the record already saved. That gap confuses developers who expect immediate state.
### Section 3: The "Quality Assurance" Prompts - Debugging & Troubleshooting
Troubleshooting prompts test whether a tool reasons from evidence. A good prompt supplies the artifact, the symptom, and the environment: the script, the log line, the role, the record. Then it asks for a ranked list of causes, each with a test. Vague prompts produce vague answers that name every possible cause. Ask which observation would rule each candidate out.
### Principle: Update Set Sanity & Integrity
An update set carries sys_ids, and the same sys_id can collide across instances. Ask for hardcoded identifiers, unresolved references, and records that belong to a different scope. A missing dependency previews clean and fails on commit. A scope boundary crossed carelessly overwrites a platform record. The prompt should demand every artifact with its scope and its dependencies listed.
### Principle: Comprehensive Error Logging & Analysis
A stack trace names the line, not the cause. The prompt should include the log entry, the script, and the input that triggered it. From there, ask which values could be null at that point and which branch execution took. Wrapping everything in try and catch hides the failure instead of diagnosing it. Log the record sys_id and the operation; that context makes the next occurrence reproducible.
### Principle: Field and ACL Debugging
Field access resolves through several layers: field ACLs, table ACLs, role assignments, and UI Policies. A tool must walk them in order. Ask whether the user reads the field at all, whether a UI Policy makes it read-only, and whether a client script hides it. Debug security as the user to see which ACL denied the write. The visible symptom rarely names the blocking record.
### Principle: UI Policy & Client Script Conflict Resolution
UI Policies and client scripts both run on load, and order decides the winner. A UI Policy sets a field read-only by default; a client script calling setReadOnly afterward reverses it. Ask for execution order, the condition on each rule, and which one the platform evaluates last. Set the execution order explicitly or consolidate the logic into one place. Two rules fighting over one field produce timing-dependent behavior.
### Principle: Integration Monitoring & Payload Analysis
An inbound REST failure needs the payload, the response code, and the authentication method. Ask the developer to reproduce it through REST API Explorer as the same user. Most failures trace to a mismatched content type, a missing role on the integration user, or a payload violating a mandatory field. Scripted REST calls appear in the transaction log. Without logging, the next failure takes just as long to find.
