---
title: "ServiceNow Architecture"
description: "How the ServiceNow platform fits together: the AI platform layers, where business logic executes, and how RaptorDB differs from a plain MariaDB deployment."
slug: "servicenow-architecture"
draft: false
tableOfContents: true
---

Before you write a single line of server-side code, you need a mental model of where that code runs. This page maps the platform layers, the execution boundaries between client and server, and the storage engine question that decides how you think about queries.

## ServiceNow Architecture
### ServiceNow AI Platform Architecture Overview
[Watch on YouTube](https://www.youtube.com/watch?v=eXp7_FACDfc)
### ServiceNow – RaptorDB vs MariaDB
ServiceNow moved its platform database layer from MariaDB to RaptorDB, a PostgreSQL-derived engine. The change matters mostly to database administrators, because the platform hides most SQL behind GlideRecord and the ORM. Query plans, index behaviour, and maintenance tasks shift with the engine, so performance tuning looks different. Integrators rarely notice unless a database view or a direct JDBC connection sits in the design. Design against the platform API, not against one database's syntax.
