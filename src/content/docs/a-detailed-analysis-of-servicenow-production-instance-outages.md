---
title: "Production Instance Outage Analysis"
description: "A structured way to reason about ServiceNow outages by layer: platform, cloud infrastructure, edge routing, application, and your own configuration."
slug: "a-detailed-analysis-of-servicenow-production-instance-outages"
draft: false
tableOfContents: true
---

When an instance is unreachable, the useful question is not who to blame but which layer failed. This page arranges outage causes by layer, adds the diagnostic evidence that separates them, and keeps the summary comparison table as a working reference.

## ServiceNow Production Instance Outage – Deep Analysis Report
An outage on a production instance rarely starts with the platform. A single fault can take the instance down. A recursive Business Rule, a scheduled job over an unindexed table, or an integration that floods the inbound queue each does it. The analysis that matters identifies the first failing component, the blast radius, and the missing guardrail. A post-incident review should end with a dated action, an owner, and a test that would catch the same fault next time.
### Executive Summary
Outages on a ServiceNow production instance rarely start in one place. A platform maintenance window can take the instance offline. A cloud region fault, a bad routing change, or a runaway Business Rule produces the same symptom. Users simply cannot load the instance. Triage separates layers instead of guessing. Confirm whether every user fails or one network fails, then check the ServiceNow trust status page before touching configuration.
### ServiceNow Platform-Level Issues
ServiceNow patches its platform on a published schedule, and every upgrade carries risk. A maintenance window can run long, leaving the instance unavailable past the announced time. A platform defect in a new release sometimes breaks custom scripts that relied on older behaviour. Administrators reduce the blast radius by checking the upgrade notes for deprecated APIs before the family upgrade lands.
### Infrastructure and Cloud Issues
ServiceNow hosts production instances inside managed data centres, usually across paired availability zones. When one zone loses power or cooling, the platform fails traffic over to its pair. A full region outage leaves no healthy zone, so the instance stops answering until the provider restores capacity. Redundancy protects against a single component fault, never against an entire region going dark.
### Network Routing and Edge Services
Traffic reaches a ServiceNow instance through several networks that the customer does not control. A misconfigured BGP advertisement or a dropped peering session silently discards packets, so users see timeouts while the instance itself stays healthy. Content delivery and edge services can also cache stale responses or reject a certificate after renewal. Engineers prove this layer by tracing the route from the affected network, not from a laptop on a different path.
### Backend and Application Layer Failures
Behind every ServiceNow page sits a database and a mid-tier that render records for the browser. When either slows, pages hang, transactions time out, and background jobs pile up. A long-running query or an unindexed GlideRecord scan can starve the whole instance. Administrators watch the transaction log and slow query logs to find the offending script before it drags every user down.
### Configuration, Customizations, and Integrations
Configuration mistakes cause more outages than hardware does. A restrictive ACL or a wrong HTTP proxy entry blocks traffic that the business expects to work. A costly Business Rule on a high-volume table, such as sys_user, fires on every insert and update until the queue backs up. Administrators isolate the change, disable the offending artifact, and review why change control missed it.
### Network and Connectivity
Most users reach ServiceNow through a corporate VPN, SD-WAN, or MPLS circuit. When that tunnel fails or a firewall rule changes, the instance looks down to everyone behind the path while remote staff keep working. Help desks waste hours escalating to ServiceNow before anyone tests basic reachability. Confirming that a user on a different network loads the instance separates a customer-side fault from a platform fault.
### Rare and Administrative Causes
Hardware faults and data corruption stay rare, but they do happen. A failed disk in a storage array or a memory error can corrupt a record or crash a node. Administrative mistakes cause more damage: someone runs a mass update that deactivates the wrong accounts, or deletes a critical table entry. Audit logs and the sys_audit table trace these changes, so the team can reverse the damage quickly.
### Diagnostic Tools & Commands
Diagnosis starts outside the platform. A ping to the instance hostname proves basic reachability, and a traceroute shows which hop drops packets. Browser developer tools reveal whether the page fails to load or a single API call stalls. Administrators then check the ServiceNow instance node logs and the transaction table for server-side errors. Each test narrows the fault to one layer instead of chasing every possibility at once.
### Summary Comparison Table
| Scenario | Likelihood | Impact | Detection Method | Remediation Time |
| --- | --- | --- | --- | --- |
| Scheduled Maintenance/Upgrade | High | High (planned) | Instance status page, Now Support notices【21†L110-L114】 | Wait ~1–2 hr |
| ServiceNow Platform Outage | Low | Critical | Official status/503Radar, multi-tenant reports | Hours (ServiceNow-driven) |
| Instance-Level Failure | Medium | High | Stats/threads.do, sys_cluster_state【71†L46-L54】【36†L218-L221】 | Minutes–hrs (restart node) |
| DC/Region Outage | Rare | Critical | Cloud provider status, Sys Diag offlines | Hours to days (failover) |
| Cloud Provider Issue | Rare | Critical | AWS/Azure/GCP status, trace, DNS check【56†L203-L211】 | Resolved by provider (hrs) |
| BGP Routing Problem | Rare | Medium–High | Traceroute, BGP looking glass (MANRS blog)【73†L195-L203】 | Usually auto-heal (<3 hr) |
| DNS Resolution Issue | Medium | Medium | dig/nslookup, compare regions | Minutes (cache flush) |
| CDN/Edge Failure | Uncommon | Medium | Browser dev tools, CDN status page | Minutes–hrs (CDN fix) |
| Load Balancer Failure | Rare | High | Stats.do (F5 status)【71†L46-L54】 | Hours (failover LB) |
| Firewall/WAF/IP Block | Uncommon | Variable | Firewall logs, try alternate IP/network | Minutes–hrs (rule fix) |
| IP Geofencing | Uncommon | Medium | Test from disallowed country, check ACL | Minutes (ACL update) |
| DDoS Attack | Low–Medium | High | Traffic spikes, SN trust site info【60†L105-L112】 | Minutes–hrs (scrubbing) |
| Rate Limiting (429) | Possible | Low–Med | 429 errors, semaphore queue in stats | Minutes (adjust rules) |
| Auth/SSO/IdP Failure | Possible | High (login) | SSO error logs, IdP status | Minutes–hrs (config fix) |
| DB/Mid-tier Degradation | Possible | High | Stats.do (DB response), syslogs | Minutes–hrs (tune/restore) |
| Cluster/Failover Issue | Rare | High | sys_cluster_state status【36†L218-L221】 | Hours (SN fix) |
| Config/ACL Error | Possible | Medium | Audit recent changes, test external access | Minutes (rollback) |
| Custom Code/Integration Bug | Possible | Medium | System logs, isolate recent updates | Minutes–hrs (disable code) |
| VPN/MPLS/ISP Failure | Possible | Medium | Test from various networks, ISP status | Minutes–hrs (reroute) |
| Time Zone Maintenance | Possible | Medium | Correlate outage with schedule | Minutes–hrs (reschedule) |
| Hardware/Data Corruption | Rare | Critical | SN internal alert | Hours (restore from backup) |
| Licensing/Account Suspension | Very Rare | Critical | Check Now Support account status | Hours (account resolution) |
| Legal/Regulatory Block | Very Rare | Critical | Government/ISP announcements | Days+ (appeal) |
### Network Diagram (Example)
Traffic reaches a ServiceNow instance through DNS, a content delivery layer, and the data centre load balancers before any application thread runs. When something breaks, that path tells a responder where to look. A resolver returning a stale address produces failures that look like a platform outage but never touch it. Document the hops, the owner of each component, and the health check that proves a layer works. Without that map, triage wastes the first critical minutes.
```mermaid
flowchart LR
subgraph Users
U1[User (APMEA Region)]
U2[User (EU/US Region)]
end
subgraph Internet
DNS["DNS Resolver"]
LB[Load Balancer (F5/Cloud LB)]
end
subgraph ServiceNow_Instance
App1[App Server Node 1 (melbourne)]
App2[App Server Node 2 (melbourne)]
DB[(Database Cluster)]
end
U1 -- Internet --> DNS
U2 -- Internet --> DNS
DNS --> LB
LB --> App1
LB --> App2
App1 --> DB
App2 --> DB

```
### Failover Path Diagram (Hypothetical)
A failover moves the instance to another region, and the customer usually learns about it afterwards. Databases, file attachments, and MID Server connections must all follow, which is why the switch takes time and occasionally needs manual intervention. Sessions drop, and any in-flight job may fail or repeat. Teams that plan will know the recovery point, the communication channel, and which integrations need a restart. Teams that do not will discover all of this during the outage.
```mermaid
flowchart LR
A[Primary DC (Melbourne)] -->|Replication| B[Secondary DC (Sydney)]
A --(if failed)--> B
A -- Normal --> Users[ServiceNow Users]
B -- Failover --> Users

```
### Conclusion
No single checklist clears every ServiceNow outage, because each layer fails differently. Work from the outside in: confirm the instance answers, check the ServiceNow status page, then examine recent configuration changes. Most incidents trace back to a maintenance window, a routing change, or a custom artifact shipped without review. Recording what the team ruled out turns a painful hour into a faster diagnosis next time.
