---
title: "AWS Cloud Discovery"
description: "How cloud discovery differs from agent-based discovery for on-premise estate, and what to verify first in a cloud CMDB."
slug: "servicenow-aws-cloud-discovery"
draft: false
tableOfContents: true
---

Cloud discovery changes the assumptions: resources appear and disappear without a ticket, and ownership is tagged rather than installed. This page notes what to verify first when you bring cloud assets into the CMDB.

## ServiceNow AWS Cloud Discovery by GlideFast Consulting
Cloud Discovery for AWS pulls infrastructure data into the CMDB without installing agents on every resource. A MID Server with credentials calls the AWS APIs and creates Configuration Items for instances, volumes, and security groups, plus the relationships between them. Dependency mapping carries the real value: an incident on an application can name the instance and network it relies on. Credentials and API throttling cause most failures.
- [YouTube video Rdn9DypfTTc](https://www.youtube.com/watch?v=Rdn9DypfTTc)
- [YouTube video ULI5x6v0xFU](https://www.youtube.com/watch?v=ULI5x6v0xFU)
- [YouTube video ZexH6ZBxnzQ](https://www.youtube.com/watch?v=ZexH6ZBxnzQ)
