---
title: "ServiceNow AI Platform Technology Stack"
description: "The Australia release technology stack layer by layer, from data and AI services up to the interfaces people use, as a reference for platform talks."
slug: "servicenow-ai-platform-technology-stack"
draft: false
tableOfContents: true
---

Platform conversations go wrong when two people mean different layers by the same word. This page keeps the stack visible in one view. The view runs from the data and AI services at the base to the applications at the top, so a discussion can name its layer.

## ServiceNow AI Platform® Technology Stack
The ServiceNow AI Platform Technology Stack describes how tables, workflow engines, and AI services layer together. A record lives in a GlideRecord row, a BusinessRule in sys_script reacts to it, and flows or workflows act on the change. Each layer trusts the one beneath, so a broken ACL or a slow before-query rule degrades everything above it. Admins who understand the stack order debug faster, because they know which tier actually broke.
### Introduction
A release note list rarely explains what an upgrade means for a working instance. The Australia release moves ServiceNow further from pure workflow automation toward agentic execution, where AI agents complete tasks instead of only suggesting them. That shift changes what an admin must review before upgrades. Custom sys_script business rules, ACLs, and RESTMessageV2 integrations all deserve a sub-production test, because drift discovered in production costs far more.
### ServiceNow AI Platform® - Australia Release
```text

┌────────────────────────────────────────────────────────────────────┐
│  Business Applications / Workflow Products                         │
│  ITSM | CSM | HRSD | FSM | ITOM | ITAM | SecOps | IRM/GRC          │
│  SPM | Source-to-Pay | Sales CRM | ESM | Industry Workflows        │
│  Public Sector | Retail | Telecom | Financial Services             │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  AI Experience and Agentic Layer                                   │
│  Now Assist | Now Assist Center | AI Search | AI Agents            │
│  AI Agent Studio | AI Agent Advisor | AI Desktop Actions           │
│  Now Assist Panel | Virtual Agent | AI Lens                        │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  AI Governance, Control, and Trust Layer                           │
│  AI Control Tower | AI Gateway | AI Risk and Compliance            │
│  AI Asset Lifecycle | AI Model / Prompt / Dataset Assets           │
│  Guardrails | Approvals | Monitoring | Audit | Compliance          │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  Workflow and Automation Layer                                     │
│  Workflow Studio | Flow Designer | Playbooks | Decision Tables     │
│  Decision Builder | Integration Hub | RPA Hub | Process Mining     │
│  Predictive Intelligence in Flows                                  │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  App Development and Creator Layer                                 │
│  App Engine Studio | ServiceNow Studio | Creator Studio            │
│  Build Agent | UI Builder | Service Catalog | Catalog Builder      │
│  ATF | ServiceNow SDK | CLI | IDE                                  │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  Data, Context, and Intelligence Layer                             │
│  CMDB | CSDM | Service Graph | Workflow Data Fabric                │
│  Data Catalog | Data Products | Zero Copy Connectors               │
│  Zero Copy Connector Hub | Knowledge Graph | AI Search             │
│  Knowledge | Documents | External Content Connectors               │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  Integration, API, and Eventing Layer                              │
│  REST | SOAP | Scripted REST APIs | Table API | Import Sets        │
│  Integration Hub Spokes | MID Server | Stream Connect              │
│  Apache Kafka | Hermes Messaging Service | Remote Process Sync     │
│  MCP Server Console | Webhooks | OAuth | mTLS                      │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  Security, Identity, Governance, and Platform Operations           │
│  ACLs | Roles | Groups | Identity | Authentication                 │
│  Encryption | Key Management | ServiceNow Vault                    │
│  Domain Separation | Data Privacy | Security Center                │
│  Instance Scan | Audit | Upgrade Console | Clone Admin             │
│  Setup Hub | Subscription Management | Platform Analytics          │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│  User Experience and Interface Layer                               │
│  Next Experience | Workspaces | Employee Center                    │
│  Service Portal | Mobile | Configurable Workspace                  │
│  UI Builder Pages | Theme Builder | Notifications | Sidebar        │
└────────────────────────────────────────────────────────────────────┘

```
### Main AI Platform developments in Australia
-
### Agentic AI becomes more operational.
Now Assist AI Agents move past conversation into execution. An agent reads a goal, selects a tool, and calls the platform action that satisfies it. That autonomy makes the agent a real actor in the instance. Governance therefore matters more. An agent can write records without a scoped ACL or a review step, and it changes data faster than any reviewer notices.
### AI Agent Advisor is introduced.
AI Agent Advisor reads real instance data and recommends which agent use cases fit the work already happening. An admin reviews the analysis, sees where a recurring manual task wastes time, and decides whether an agent belongs there. The tool informs a decision rather than making it. Treating its suggestion as approval skips harder questions, like which role the agent runs as and who owns the failure when it acts wrongly.
### AI Control Tower becomes the governance backbone.
AI Control Tower gives AI stewards one workspace to inventory agents, models, and their owners. Instead of hunting through separate records, a steward sees what runs in the instance and whether each item has an accountable owner. Governance fails quietly when nobody can list the AI a platform executes. An unowned agent still consumes licenses and still touches production data, so an incomplete inventory hides real risk from auditors.
### Now Assist Center becomes the AI administration hub.
Now Assist Center collects the switches that turn AI features on or off, so an admin stops chasing them across plugins and properties. Central control helps, but it also concentrates the blast radius. An admin who enables a skill globally without checking group-level entitlement exposes capabilities to users who should never see them. Test a skill on a small role first, then widen it deliberately.
### MCP Server Console arrives for governed AI interoperability.
MCP Server Console exposes selected ServiceNow capabilities through the Model Context Protocol, with governance wrapped around the exposure. A developer registers which tools an external AI client may call, rather than opening the whole instance. That boundary is the point. Broad exposure lets an outside model script record changes through paths nobody monitors. Scope every published capability to a service account with least privilege.
### Knowledge Center improves knowledge quality for AI-powered work.
Knowledge Center manages articles from one place, which matters because retrieval-augmented AI answers inherit the quality of the knowledge base behind them. A duplicate or stale article teaches the model the wrong procedure, and the model repeats it confidently. Knowledge owners who retire outdated articles and merge duplicates protect every AI answer built on that content. Poor knowledge quality surfaces as wrong answers, not as obvious errors.
### AI Desktop Actions extends agents beyond ServiceNow screens.
AI Desktop Actions lets an agent drive desktop software outside the browser, automating screens that offer no API. That reach solves a real gap, because many legacy tools still require a human to click through them. It also breaks the usual assumption that platform ACLs govern every action. An agent clicking a client application acts as whatever user account owns that desktop session, so the session credentials matter as much as the ACL.
### Build Agent and “vibe coding” move into ServiceNow Studio.
Build Agent inside ServiceNow Studio turns a plain-language request into a working application, generating tables, form layouts, and scripts. Speed tempts developers to skip review. Generated code still runs on the instance with the developer's rights, and a generated BusinessRule can query large tables without a filter. Read the artifact before saving it, because the platform stores whatever the agent produced, mistakes included.
### Security and platform hardening are not optional.
Release hardening tightens defaults that instances once tolerated. Read-only fields gain protection, and finer controls let an admin restrict what a role may change. These changes break customizations that wrote to protected fields directly. A script that wrote to a protected field without the right role now fails at runtime. Review custom business rules and client scripts against the new defaults before upgrading production.
### New AI Platform tiers: Foundation, Advanced, Prime.
ServiceNow groups AI capabilities into tiers such as Foundation, Advanced, and Prime, and each tier carries different entitlements. A feature can appear in release notes yet stay unavailable on an instance that lacks the entitlement. Admins who promise a capability without checking the tier create avoidable disappointment. Confirm what the instance actually licenses before planning an AI rollout, and verify in a sub-production instance.
| Tier | Practical meaning |
| --- | --- |
| Foundation | AI basics / AI agents and skills for insights |
| Advanced | AI agents and skills to improve productivity across selected use cases |
| Prime | Autonomous AI capabilities, including creating your own AI agents and skills |
### Below are key highlights of the ServiceNow AI Platform®, Australia release:
Australia spreads Now Assist across more of the enterprise, so generative features reach teams that previously had none. The highlights cluster around four themes: broader assistants, agentic execution, centralized AI governance, and stronger platform hardening. Reading them as separate announcements hides the pattern. Together they describe a platform where AI both answers questions and performs work, which changes how a team validates its instance.
### 1. Core Platform Foundation
| Layer | Technology / Capability | Practical Meaning |
| --- | --- | --- |
| Platform runtime | ServiceNow AI Platform | The base SaaS platform where records, workflows, experiences, integrations, and AI capabilities run. |
| Data model | Tables, fields, dictionary, relationships, reference fields | The structural foundation for every application such as Incident, Change, User, CI, Catalog Item, Case, and Asset. |
| Server-side logic | Business Rules, Script Includes, Script Actions, Scheduled Jobs, Fix Scripts | Used for validation, automation, data processing, integration handling, and enterprise logic. |
| Client-side logic | Client Scripts, UI Policies, Catalog Client Scripts, UI Actions | Used to control user experience, form behavior, catalog behavior, and interactive logic. |
| Access control | Roles, ACLs, groups, domains | Protects data and controls who can read, write, create, delete, or execute platform capabilities. |
| Upgrade management | Upgrade Center, Upgrade Console, skipped records, plugin lifecycle | Required for safe movement from earlier releases to the Australia release. |
### 2. AI and Agentic AI Stack
The AI and agentic stack sits above the platform core. A large language model reasons over grounded context pulled from tables, knowledge articles, and search indexes, then calls a tool that changes a record. Every layer above the core depends on permissions defined below it, so an ACL gap silently widens what an agent can reach. Audit the permission chain, not only the prompt.
| AI Stack Component | Purpose | Australia Release Relevance |
| --- | --- | --- |
| Now Assist | Generative AI experience across ServiceNow | Improves self-service, recommends actions, provides answers, summarizes information, and improves search experiences. |
| Now Assist AI Agents | Agentic AI solutions that perceive, decide, and act toward goals | Supports AI-native testing, tool-output widgets, improved agentic workflows, issue tracing, and optimization suggestions. |
| AI Agent Advisor | Finds automation opportunities inside the instance | Analyzes instance data, identifies high-impact automation opportunities, maps them to existing agents, and helps deploy new agents. |
| AI Desktop Actions | Automates repetitive desktop tasks | Allows AI agents to perform desktop-level actions and repetitive task automation. |
| Now Assist Center | Central admin hub for Now Assist | Provides a unified place for administrators to set up and manage generative AI capabilities. |
| Generative AI Controller | Connects ServiceNow AI capabilities to third-party LLM providers | Supports third-party large language model configurations and bring-your-own-key patterns. |
| AI Control Tower | AI governance, monitoring, and stewardship | Provides central governance for AI assets, security scoring, output monitoring, policy monitoring, and lifecycle governance. |
| MCP Server Console | Governed access to ServiceNow functions through Model Context Protocol | Enables secure and governed access to ServiceNow capabilities from external AI clients and employee experiences. |
| Build Agent | Conversational full-stack app creation and metadata editing | Helps developers create apps, workflows, agents, skills, tests, and platform artifacts using a conversational interface. |
### 3. AI Product Tiering
Product tiering separates what every customer receives from what a paid subscription adds. Foundation, Advanced, and Prime sit at different points on that line, and the boundary decides whether a skill even appears in the instance. A test plan that assumes a capability exists wastes a sprint. Check the entitlement first, then design the process around what the instance truly runs.
| Tier | Meaning |
| --- | --- |
| Foundation | AI basics, AI agents, and skills for insights and productivity. |
| Advanced | Advanced AI capabilities that improve productivity across specific business and technology use cases. |
| Prime | Broader autonomous action, advanced agents, skills, AI asset creation, and enterprise-scale AI execution. |
### 4. Data, Context, and Knowledge Stack
Grounded AI needs trusted context, and that context comes from tables, knowledge articles, and the search index that spans them. A stale CMDB record or a duplicated knowledge article degrades an answer without raising an error. Data stewards therefore own part of AI quality, whether they intend to or not. Clean the source data first, then expect the model to behave.
| Component | Purpose | Why It Matters |
| --- | --- | --- |
| CMDB | Stores configuration items and relationships | Provides operational context for ITSM, ITOM, ITAM, SecOps, and AI use cases. |
| CSDM | Common Service Data Model | Standardizes service, application, business capability, and technical service relationships. |
| Service Graph Connectors | Bring external configuration and operational data into ServiceNow | Helps enrich CMDB and Service Graph with trusted external data. |
| Workflow Data Fabric | Foundation for governed data interfaces and data products | Supports creation and management of reusable data products and governed data access. |
| Data Catalog | Self-service discovery of data assets | Allows teams to find published data products, metadata, lineage, documentation, and access pathways. |
| Data Products | Governed reusable data interfaces | Allows data stewards to package reusable data products for discovery and consumption. |
| Zero Copy Connectors | Real-time access to external data without copying it into ServiceNow | Helps ServiceNow use external enterprise data while reducing unnecessary duplication. |
| Knowledge Graph | Natural language understanding of connected enterprise entities | Helps users ask natural language questions about services, servers, databases, and CI relationships. |
| Knowledge Center | Central knowledge-quality management | Provides dashboards and actions for improving knowledge article quality and coverage. |
| Now Assist in Document Intelligence | Extracts, summarizes, and answers questions from documents | Improves document processing, document Q&A, summarization, extraction, and attachment-based insights. |
### 5. Application Development and Low-Code Stack
Low-code tools let a citizen developer build a form, a flow, and a report without writing a script. That reach is the risk. A flow that runs on every record insert can trigger other flows, and an unguarded loop consumes instance resources until a transaction times out. Platform governance, such as application scope and a review before deployment, keeps citizen-built apps maintainable.
| Development Tool | Purpose |
| --- | --- |
| ServiceNow Studio | Unified development environment for custom apps, metadata, flows, UI files, and app artifacts. |
| Build Agent | Conversational app creation, metadata editing, test generation, UI validation, and semantic artifact discovery. |
| App Engine Studio | Low-code app creation for creators with varying skill levels. |
| Creator Studio | No-code and citizen development style app creation. |
| UI Builder | Builds workspace pages, custom pages, portals, and Next Experience interfaces. |
| Workflow Studio | Consolidates flows, subflows, actions, decision tables, playbooks, and integrations into one design environment. |
| ServiceNow IDE | Browser-based IDE based on Visual Studio Code for the Web. |
| ServiceNow SDK | Supports local source-code development with Visual Studio Code Desktop. |
| ServiceNow CLI | Supports command-line operations from the local system. |
| ATF | Automated Test Framework for regression testing and platform validation. |
| ReleaseOps | Supports deployment and validation of code across development-to-production pipelines. |
### 6. Workflow, Automation, and Orchestration Stack
| Component | Purpose |
| --- | --- |
| Flow Designer | Low-code automation using triggers, actions, conditions, and subflows. |
| Workflow Studio | Unified environment for designing workflows, subflows, integrations, playbooks, and decision logic. |
| Decision Tables | Externalizes business decisions from code for approvals, routing, categorization, prioritization, and policy decisions. |
| Playbooks | Provides guided process execution for agents, case workers, and operations teams. |
| Process Mining | Finds bottlenecks and inefficiencies in real business and IT workflows. |
| Intelligent Approvals | Supports AI-assisted approval routing and decision-making based on business context. |
| RPA Hub | Supports end-to-end automation for repetitive tasks, especially across desktop and legacy systems. |
| AI Desktop Actions | Extends automation to desktop tasks executed by AI agents. |
### 7. Integration and API Stack
Integration carries most of the risk in any ServiceNow estate, because the platform talks to systems it does not control. A developer chooses between a Scripted REST API, a RESTMessageV2 outbound call, and an Import Set, and each choice changes how errors surface. An outbound call without a timeout and retry policy stalls the transaction that made it. Design for the remote system failing.
| Integration Technology | Purpose |
| --- | --- |
| REST APIs | Standard API access for CRUD operations, integrations, and system-to-system communication. |
| Scripted REST APIs | Custom REST endpoints for custom business logic and external consumers. |
| SOAP APIs | Legacy enterprise integration support where required. |
| IntegrationHub | Extends Workflow Studio automation by integrating ServiceNow data with external systems. |
| Spokes | Prebuilt IntegrationHub connectors and actions for common enterprise systems. |
| MID Server | Secure communication bridge for on-premises systems, discovery, orchestration, LDAP, integrations, and operational data collection. |
| Stream Connect, Hermes, and Kafka | Supports event-streaming style integrations and real-time enterprise event processing. |
| Remote Process Sync | Synchronizes process data across systems and provides visibility into processing status. |
| Zero Copy Connectors | Allows ServiceNow to query external data in real time without duplicating it into the instance. |
| MCP Server Console | Opens governed ServiceNow functionality to AI applications and external MCP clients. |
### 8. User Experience Stack
| UX Component | Purpose |
| --- | --- |
| Next Experience | Modern ServiceNow user experience shell. |
| Configurable Workspace | Workspace experience for agents, case managers, help desks, and managers. |
| UI Builder | Builds workspace and custom experiences using Next Experience components. |
| Service Portal | Mobile-friendly self-service portal framework for employees and customers. |
| Employee Center and Employee Center Pro | Unified employee service experience across HR, IT, workplace, legal, and other services. |
| Mobile Platform | Mobile access to ServiceNow experiences. |
| Theme Builder | Visual customization and branding of the platform experience. |
| Adoption Services | In-product support and adoption guidance for users. |
### 9. Analytics, Intelligence, and Observability Stack
| Component | Purpose |
| --- | --- |
| Platform Analytics | Provides dashboards, analytics, visualizations, and operational insights. |
| Now Assist in Platform Analytics | Allows users to ask natural language questions and convert them into insights and visualizations. |
| Performance Analytics | Supports KPI tracking, trends, scorecards, targets, breakdowns, and executive reporting. |
| Process Mining | Discovers bottlenecks and workflow inefficiencies from actual process data. |
| Predictive Intelligence | Supports classification, prediction, similarity, routing, and model-based automation. |
| Usage Insights | Provides adoption and usage visibility. |
| Performance Analyzer | Provides page-load time data, trends, waterfall visualization, and UX framework performance diagnostics. |
### 10. Security, Risk, and Governance Stack
| Security / Governance Layer | Purpose |
| --- | --- |
| Roles and ACLs | Core authorization model for controlling access to data and platform capabilities. |
| Authentication and Identity | Supports SSO, MFA, identity provider integration, and user lifecycle controls. |
| Domain Separation | Segregates data and processes for MSPs or multi-tenant enterprise operating models. |
| Encryption, Key Management, and Vault | Protects sensitive data, secrets, credentials, and platform integrations. |
| Data Privacy | Helps manage privacy-sensitive data and privacy-related platform controls. |
| Security Center | Provides security posture and platform security visibility. |
| AI Control Tower | Supports AI governance, AI asset management, model/provider visibility, security scoring, output monitoring, and lifecycle governance. |
| Code Signing | Helps protect the integrity of code and applications. |
| Instance Scan | Detects configuration, development, and best-practice issues. |
| Upgrade Console | Helps manage release upgrades, skipped changes, and compatibility risk. |
### 11. Core Business Application Stack
The core applications, ITSM, ITOM, HRSD, and their peers, turn platform capability into business outcome. They also multiply the surface an AI feature can touch, because each application carries its own tables, roles, and processes. An agent enabled in one application can read data another application owns unless an ACL prevents it. Map data ownership before enabling anything broadly.
| Product Area | Typical Modules |
| --- | --- |
| IT Service Management | Incident, Problem, Change, Request, Knowledge, Major Incident, Service Operations Workspace. |
| IT Operations Management | Discovery, Service Mapping, Event Management, AIOps, Operational Intelligence. |
| IT Asset Management | Hardware Asset Management, Software Asset Management, Enterprise Asset Management. |
| Customer Service Management | Case Management, Customer Service Workspace, customer workflows, and field-service-connected experiences. |
| HR Service Delivery / Employee Service Management | HR cases, Employee Center, knowledge, journeys, and lifecycle events. |
| Field Service Management | Work orders, dispatch, scheduling, mobile workforce, and field operations. |
| Security Operations | Security Incident Response, Vulnerability Response, Threat Intelligence. |
| Governance, Risk, and Compliance / Integrated Risk Management | Risk, compliance, audit, policy, third-party risk, and operational resilience. |
| Strategic Portfolio Management | Demand, project, portfolio, resource, agile, and investment planning. |
| Source-to-Pay Operations | Procurement, purchase orders, supplier lifecycle, and accounts payable operations. |
| Sales CRM and Industry Workflows | Telecommunications, financial services, public sector, manufacturing, retail, healthcare, and other industry workflows. |
### 12. Practical Skills Required for Australia Release
| Role Area | Required Skills |
| --- | --- |
| Admin / Platform Engineer | User/group/role management, ACLs, tables, forms, lists, notifications, imports, upgrades, and plugin management. |
| ServiceNow Developer | JavaScript, GlideRecord, GlideAjax, Business Rules, Script Includes, Flow Designer, Scripted REST APIs, and scoped apps. |
| Low-Code Developer | App Engine Studio, Flow Designer, Workflow Studio, Decision Tables, Catalog Builder, and UI Builder. |
| AI Platform Developer | Now Assist, Build Agent, AI Agents, AI Agent Advisor, Skill Kit, prompt design, and ATF with AI support. |
| Integration Developer | REST, SOAP, OAuth, IntegrationHub, MID Server, spokes, Kafka, Stream Connect, and Remote Process Sync. |
| Data / CMDB Specialist | CMDB, CSDM, Service Graph Connectors, data quality, reconciliation, and identification rules. |
| AI Governance Lead | AI Control Tower, AI asset lifecycle, model/provider visibility, data privacy, security scoring, and policy monitoring. |
| UX Developer | Next Experience, Workspace, UI Builder, Service Portal, Employee Center, and responsive design. |
| QA / Release Engineer | ATF, Instance Scan, ReleaseOps, update sets/source control, regression packs, and upgrade testing. |
| Analytics Lead | Platform Analytics, Performance Analytics, Process Mining, Predictive Intelligence, and AI-generated insights. |
### 13. Recommended Learning Priority
Start with the platform fundamentals, not the AI features on top. An admin reads an agent failure correctly after learning table inheritance, ACL evaluation order, and GlideRecord query behaviour. The cause usually lives in the layer beneath. Jumping straight to generative features leaves that foundation missing. Learn the core first, then the AI layer on it.
### 14. Summary
The Australia release moves ServiceNow from a workflow platform that automates steps toward one where AI agents perform work. Governance, data quality, and permissions decide whether that shift helps or hurts, because an agent inherits every weakness in the layers below it. The summary matters less than the sequence: harden the platform, ground the data, then grant autonomy carefully.
### 15. Official Reference Links
Official reference links point to ServiceNow documentation, and they matter because third-party summaries age faster than the platform does. A blog post written before a patch release can describe behaviour an instance no longer shows. When a claim about AI features or entitlement drives a decision, open the linked product documentation and confirm it against the instance. Treat every summary, this one included, as a starting point.
-  [ ServiceNow Australia Release Notes ](https://www.servicenow.com/docs/r/release-notes/rn-learn-landing-page.html)
-  [ ServiceNow AI Platform ](https://www.servicenow.com/in/platform.html)
-  [ Now Assist Release Notes ](https://www.servicenow.com/docs/r/release-notes/now-assist-rn-landing.html)
-  [ Now Assist AI Agents Release Notes ](https://www.servicenow.com/docs/r/release-notes/now-assist-ai-agents-rn.html)
-  [ AI Agent Advisor Release Notes ](https://www.servicenow.com/docs/r/release-notes/ai-agent-advisor-rn.html)
-  [ AI Control Tower Release Notes ](https://www.servicenow.com/docs/r/release-notes/ai-control-tower-rn.html)
-  [ MCP Server Console Release Notes ](https://www.servicenow.com/docs/r/release-notes/mcp-server-console-rn.html)
-  [ Build Agent Release Notes ](https://www.servicenow.com/docs/r/release-notes/build-agent-rn.html)
-  [ Generative AI Controller Release Notes ](https://www.servicenow.com/docs/r/release-notes/generative-ai-controller-rn.html)
-  [ Data Products Release Notes ](https://www.servicenow.com/docs/r/release-notes/data-products-rn.html)
-  [ Zero Copy Connectors Release Notes ](https://www.servicenow.com/docs/r/release-notes/zero-copy-connectors-rn.html)
-  [ IntegrationHub Release Notes ](https://www.servicenow.com/docs/r/release-notes/integration-hub-rn.html)
-  [ ServiceNow Studio Release Notes ](https://www.servicenow.com/docs/r/release-notes/servicenow-studio-rn.html)
-  [ ServiceNow SDK Release Notes ](https://www.servicenow.com/docs/r/release-notes/servicenow-sdk-rn.html)
