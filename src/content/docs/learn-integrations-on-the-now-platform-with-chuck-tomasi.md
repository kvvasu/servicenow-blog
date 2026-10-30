---
title: "Integrations on the Now Platform"
description: "Episode notes for the integration series on the Now platform, covering REST, scripted integrations and the error paths."
slug: "learn-integrations-on-the-now-platform-with-chuck-tomasi"
draft: false
tableOfContents: true
---

The integration series works through the mechanism and then the failure path, which is the right order to learn it. This page keeps the episodes together with what to build after each.

## Chuck Tomasi
Chuck Tomasi built a long-running video series that walks an admin through integrations on the Now Platform. Each episode stays short and shows one feature end to end. That suits a developer who learns by watching a screen instead of reading a manual. The catalog covers import sets, inbound email actions, and spokes. Treat the series as a starting map, then build each scenario yourself.
### GETTING STARTED
The opening episodes set vocabulary before touching configuration. They separate an inbound integration from an outbound one and name the tools each direction uses, so a newcomer stops calling every interface an API. Watch these first if terms like import set, transform map, and REST message still blur together. Note which component owns the trigger. That distinction decides where a failure surfaces when data arrives out of order.
- [YouTube video F9npfsOxOQk](https://www.youtube.com/watch?v=F9npfsOxOQk)
- [YouTube video hX39spCtY5M](https://www.youtube.com/watch?v=hX39spCtY5M)
- [YouTube video QwLUhNpv7H4](https://www.youtube.com/watch?v=QwLUhNpv7H4)
- [YouTube video hhUlcEu-s7k](https://www.youtube.com/watch?v=hhUlcEu-s7k)
- [YouTube video iyXzXtR5jPw](https://www.youtube.com/watch?v=iyXzXtR5jPw)
### IMPORT SETS
An import set lands raw rows in a staging table before anything touches a target table. A transform map then moves each row into sys_user, incident, or another target, applying field mappings and coalesce rules. Coalesce decides insert versus update, so a wrong coalesce field creates duplicates on every load. Run the transform in preview first. A scheduled import that fails silently keeps writing bad rows while the load report looks clean.
- [YouTube video 04db1kwdE2w](https://www.youtube.com/watch?v=04db1kwdE2w)
- [YouTube video -Kg9FCdSp9I](https://www.youtube.com/watch?v=-Kg9FCdSp9I)
- [YouTube video iMjSpK3OaUY](https://www.youtube.com/watch?v=iMjSpK3OaUY)
- [YouTube video WZAzleK2vVw](https://www.youtube.com/watch?v=WZAzleK2vVw)
- [YouTube video Hip3nmClZ6A](https://www.youtube.com/watch?v=Hip3nmClZ6A)
- [YouTube video raiAXyvmG8w](https://www.youtube.com/watch?v=raiAXyvmG8w)
- [YouTube video UHRZUCu1jeE](https://www.youtube.com/watch?v=UHRZUCu1jeE)
- [YouTube video dK6LPHZ2kdw](https://www.youtube.com/watch?v=dK6LPHZ2kdw)
- [YouTube video REM3YJFX1F4](https://www.youtube.com/watch?v=REM3YJFX1F4)
- [YouTube video Mhp02bGR_A0](https://www.youtube.com/watch?v=Mhp02bGR_A0)
### EMAIL
Inbound email actions turn a message into a record. ServiceNow matches the sender against sys_user, reads the subject and body, and runs the action registered for that mailbox. A loose condition on an inbound action creates a ticket from every automated notification that reaches the mailbox. An email loop starts when a notification triggers a reply that triggers another notification. Keep the lookups tight, and test with a real mailbox before enabling it.
- [YouTube video zoL0JZYpiqU](https://www.youtube.com/watch?v=zoL0JZYpiqU)
- [YouTube video KZpZDqbRKU4](https://www.youtube.com/watch?v=KZpZDqbRKU4)
- [YouTube video KZpZDqbRKU4](https://www.youtube.com/watch?v=KZpZDqbRKU4)
### Connections and Credentials
A connection alias plus a credential record keeps secrets out of a REST message definition. The alias names the endpoint, and the credential holds the user, password, or OAuth token. Hardcoding a password inside the script exposes it to anyone with read access to the record and to every clone. JSON forms the payload in most modern calls, so a developer must read nested objects and arrays. A malformed body returns an unhelpful remote error.
- [YouTube video kM_KiiYGbCA](https://www.youtube.com/watch?v=kM_KiiYGbCA)
- [YouTube video LA9twQSqD1s](https://www.youtube.com/watch?v=LA9twQSqD1s)
- [YouTube video qQWpTnMCrTc](https://www.youtube.com/watch?v=qQWpTnMCrTc)
- [YouTube video 3lCsO-vg6uw](https://www.youtube.com/watch?v=3lCsO-vg6uw)
- [YouTube video vLUspm6LRIY](https://www.youtube.com/watch?v=vLUspm6LRIY)
- [YouTube video HSnJF3eGqaI](https://www.youtube.com/watch?v=HSnJF3eGqaI)
- [YouTube video 7_gdlmEQBRs](https://www.youtube.com/watch?v=7_gdlmEQBRs)
### Web Services
- Web services overview (6:37)
- [YouTube video Kijvu58uHAQ](https://www.youtube.com/watch?v=Kijvu58uHAQ)
- REST API Explorer (5:50)
- [YouTube video i9YeiHiVzZ0](https://www.youtube.com/watch?v=i9YeiHiVzZ0)
- Built in REST APIs (5:35)
- [YouTube video Fk7noWJt8Q4](https://www.youtube.com/watch?v=Fk7noWJt8Q4)
  - [Scripted REST APIs - Design (8:01)](https://youtu.be/Tw70sHgDc-w)
  - [Scripted REST APIs - Implementation (8:04)](https://www.youtube.com/watch?v=LFHV-Qk1-Yk)
  - [Scripted REST APIs - ACLs (4:17)](https://www.youtube.com/watch?v=5fkHtba2Y54)
- Simple Outbound REST message (4:10)
- [YouTube video S7gl90SsM0s](https://www.youtube.com/watch?v=S7gl90SsM0s)
- Inbound REST API Rate Limiting (3:33)
- [YouTube video KJrxq9gw82k](https://www.youtube.com/watch?v=KJrxq9gw82k)
- Web Services Helpful Resources (4:40)
- [YouTube video nc0Ac_Nl-sA](https://www.youtube.com/watch?v=nc0Ac_Nl-sA)
### IntegrationHub
IntegrationHub packages integrations as spokes, and each spoke ships actions a flow can call. An admin installs a spoke from the store, wires the action into a flow, and gets retry handling without writing the HTTP call. That convenience carries a subscription cost and a version dependency, so confirm the spoke supports the instance release before designing around it. For a one-off endpoint, a scripted step may cost less to maintain.
- [YouTube video RO707H-b5iY](https://www.youtube.com/watch?v=RO707H-b5iY)
- [YouTube video V4xvJN9yFwg](https://www.youtube.com/watch?v=V4xvJN9yFwg)
- [YouTube video IAlqmTpfWXQ](https://www.youtube.com/watch?v=IAlqmTpfWXQ)
- [YouTube video F37zZURAw6E](https://www.youtube.com/watch?v=F37zZURAw6E)
- [YouTube video pAWOMA8d220](https://www.youtube.com/watch?v=pAWOMA8d220)
- [YouTube video rmMWKghthVo](https://www.youtube.com/watch?v=rmMWKghthVo)
- [YouTube video Io5TtlAVY54](https://www.youtube.com/watch?v=Io5TtlAVY54)
### EXPORTING
- Email exports (4:53)
- [YouTube video fEm89zmUrxE](https://www.youtube.com/watch?v=fEm89zmUrxE)
- Manual exports (6:57)
- [YouTube video piVyGrrQHbk](https://www.youtube.com/watch?v=piVyGrrQHbk)
- Export sets (6:33)
- [YouTube video XV_C5OrHzrk](https://www.youtube.com/watch?v=XV_C5OrHzrk)
