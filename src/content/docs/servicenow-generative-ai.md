---
title: "ServiceNow Generative AI"
description: "What generative AI means in a ServiceNow instance in practice: which capabilities exist, what they depend on, and how to scope a first use case."
slug: "servicenow-generative-ai"
draft: false
tableOfContents: true
---

Generative AI features arrive as platform capabilities rather than as separate products, which makes scoping the hard part. Start from a task with a measurable before and after, then check which capability covers it.

## ServiceNow Generative AI
Generative AI on the platform arrives as Now Assist skills rather than a raw model endpoint. A skill pairs a large language model with a prompt, a data source, and the access rules of the user who invokes it. That last piece decides whether the feature is safe. Summarization must never surface a record the reader cannot already open. Admins control which skills turn on and which tables feed them. The technology is only as good as the guardrails around the data it reads.
- [servicenow.com](https://www.servicenow.com/now-platform/generative-ai.html)
- [servicenow.com](https://www.servicenow.com/blogs/topics/ai-and-automation.html)
