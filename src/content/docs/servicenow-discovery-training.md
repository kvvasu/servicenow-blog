---
title: "Discovery Training"
description: "Discovery training material covering how the platform finds and models infrastructure, and the data quality work that follows every run."
slug: "servicenow-discovery-training"
draft: false
tableOfContents: true
---

Discovery is only half a product; the other half is what you do with the data it returns. This page covers the discovery process and the reconciliation work that decides whether the CMDB is usable.

## ServiceNow Discovery Training Videos
Discovery builds the CMDB by probing the network and turning answers into configuration items. Before watching any recording, an admin should understand what the MID Server does and how the ECC Queue carries commands. These sessions move from that foundation into schedules, credentials and patterns. Work through them in order, because each one assumes the previous topic.
- What is Discovery in ServiceNow (21:39)
- [YouTube video j0lPKE7IOzo](https://www.youtube.com/watch?v=j0lPKE7IOzo)
Discovery builds the CMDB by probing the network and turning answers into configuration items. Before watching any recording, an admin should understand what the MID Server does and how the ECC Queue carries commands. These sessions move from that foundation into schedules, credentials and patterns. Work through them in order, because each one assumes the previous topic.
- [YouTube video W_ZdvzY_fI4](https://www.youtube.com/watch?v=W_ZdvzY_fI4)
- [YouTube video TyUwvSdmHIE](https://www.youtube.com/watch?v=TyUwvSdmHIE)
- [YouTube video HZZWxxRa-8w](https://www.youtube.com/watch?v=HZZWxxRa-8w)
- [YouTube video pkhEmYYqr3I](https://www.youtube.com/watch?v=pkhEmYYqr3I)
### Runjay Patel
A long walkthrough of Discovery in a live environment. The recording follows one run from credential setup through probe execution and CI creation, with commentary at each screen. Useful where a shorter clip skips the parts that break real deployments, such as an unreachable subnet or an expired credential. Set aside a full afternoon and follow along.
- [YouTube video pkhEmYYqr3I](https://www.youtube.com/watch?v=pkhEmYYqr3I)
### Alikutty Abdulrazak
Cloud Discovery works differently from scanning on-premise hosts. This session covers Azure, showing how a service account and an API gather subscriptions, resource groups and virtual machines without opening a firewall port. The same shape applies to AWS and GCP. Watch it when a CMDB holds servers but nothing from the cloud.
- [YouTube video 5rru32xQXU0](https://www.youtube.com/watch?v=5rru32xQXU0)
- [YouTube video MjG__siORn4](https://www.youtube.com/watch?v=MjG__siORn4)
### Jeff Thies
This session pairs Discovery fundamentals with a live demonstration. It explains what a pattern does and how the classifier picks one. Identification and reconciliation rules then decide whether a scan creates a CI or merges into an existing record. That last step explains most duplicate CIs, so give it close attention.
- [YouTube video hVIpcN6mHh4](https://www.youtube.com/watch?v=hVIpcN6mHh4)
