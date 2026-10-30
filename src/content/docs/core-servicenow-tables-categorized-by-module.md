---
title: "Core Tables by Module"
description: "Reference tables of core ServiceNow tables grouped by module, with parent table and extendability, for tracing inheritance before you write a query."
slug: "core-servicenow-tables-categorized-by-module"
draft: false
tableOfContents: true
---

Every table you query inherits from something, and that inheritance decides which records a filter will actually match. This page keeps the module-by-module table reference together, so you can look up a parent table and its extendability before you commit to a query.

## Core ServiceNow Tables Categorized by Module
Every record in ServiceNow lives in a table, and the table name tells you which module owns it. Incident work sits in incident, change work in change_request, and user data in sys_user. Configuration items live in cmdb_ci and its children. Knowing the table behind a form saves time, because a query, an ACL, or a Business Rule always points at a specific table name. Grouping those tables by module makes a large schema easier to navigate.
### Agile Development
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Enhancement | rm_enhancement | task | Agile Development | Yes |
| Story | rm_story | task | Agile Development | Yes |
| Epic | rm_epic | task | Agile Development | Yes |
| Feature | rm_feature | task | Agile Development | Yes |
### CMDB
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| cmdb_ci | cmdb_ci | None | CMDB | Yes |
| Computer | cmdb_ci_computer | cmdb_ci | CMDB | Yes |
| Server | cmdb_ci_server | cmdb_ci_computer | CMDB | Yes |
| Windows Server | cmdb_ci_win_server | cmdb_ci_server | CMDB | Yes |
| Linux Server | cmdb_ci_linux_server | cmdb_ci_server | CMDB | Yes |
| Application | cmdb_ci_appl | cmdb_ci | CMDB | Yes |
| Database | cmdb_ci_database | cmdb_ci | CMDB | Yes |
| Service | cmdb_ci_service | cmdb_ci | CMDB | Yes |
| Business Service | cmdb_ci_business_service | cmdb_ci_service | CMDB | Yes |
| CI Relationship | cmdb_rel_ci | None | CMDB | No |
### Change Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Change Request | change_request | task | Change Management | Yes |
| Change Task | change_task | task | Change Management | Yes |
### Customer Service
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Case | sn_customerservice_case | task | Customer Service | Yes |
### Demand Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Demand | dmn_demand | task | Demand Management | Yes |
### Flow Designer
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Flow Context | sys_flow_context | None | Flow Designer | No |
### Global
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Task | task | None | Global | No |
### Governance, Risk, Compliance
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Issue | issue | task | Governance, Risk, Compliance | Yes |
| Policy Exception | policy_exception | task | Governance, Risk, Compliance | Yes |
### HR Service Delivery
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| HR Case | sn_hr_core_case | task | HR Service Delivery | Yes |
| HR Profile | sn_hr_core_profile | None | HR Service Delivery | No |
### Import Sets
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Import Set | sys_import_set | None | Import Sets | No |
| Transform Map | sys_transform_map | None | Import Sets | No |
| Data Source | sys_data_source | None | Import Sets | No |
| Import Log | sys_import_log | None | Import Sets | No |
### Incident Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Incident | incident | task | Incident Management | Yes |
### IntegrationHub
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Spoke | sys_spoke | None | IntegrationHub | No |
| Connection Alias | sys_connection_alias | None | IntegrationHub | No |
### Knowledge Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Knowledge Article | kb_knowledge | None | Knowledge Management | No |
| Knowledge Base | kb_knowledge_base | None | Knowledge Management | No |
### Performance Analytics
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Indicator | pa_indicator | None | Performance Analytics | No |
| Indicator Source | pa_sources | None | Performance Analytics | No |
### Problem Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Problem | problem | task | Problem Management | Yes |
| Problem Task | problem_task | task | Problem Management | Yes |
### Project Portfolio Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Project | pm_project | task | Project Portfolio Management | Yes |
| Project Task | pm_project_task | task | Project Portfolio Management | Yes |
### Risk Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Risk | risk | task | Risk Management | Yes |
### Security Incident Response
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Security Incident | sn_si_incident | task | Security Incident Response | Yes |
### Service Catalog
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Request | sc_request | task | Service Catalog | Yes |
| Requested Item | sc_req_item | task | Service Catalog | Yes |
| Catalog Task | sc_task | task | Service Catalog | Yes |
| Catalog Item | sc_cat_item | None | Service Catalog | No |
| Catalog Category | sc_category | None | Service Catalog | No |
| Service Catalog | sc_catalog | None | Service Catalog | No |
### Service Level Management
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| SLA Definition | contract_sla | None | Service Level Management | No |
| Task SLA | task_sla | None | Service Level Management | No |
### System Definition
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Business Rule | sys_script | None | System Definition | No |
| Script Include | sys_script_include | None | System Definition | No |
| Attachment | sys_attachment | None | System Definition | No |
| Attachment Document | sys_attachment_doc | None | System Definition | No |
| Dictionary Entry | sys_dictionary | None | System Definition | No |
| Table | sys_db_object | None | System Definition | No |
### System Logs
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Audit | sys_audit | None | System Logs | No |
| Log | syslog | None | System Logs | No |
### System Mailboxes
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Email | sys_email | None | System Mailboxes | No |
### System Notification
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Email Template | sys_email_template | None | System Notification | No |
| Notification | sysevent_email_action | None | System Notification | No |
### System Policy
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Event | sysevent | None | System Policy | No |
### System Properties
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| System Property | sys_properties | None | System Properties | No |
### System UI
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Client Script | sys_script_client | None | System UI | No |
| UI Policy | ui_policy | None | System UI | No |
| UI Action | sys_ui_action | None | System UI | No |
### User Administration
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| User | sys_user | None | User Administration | No |
| Group | sys_user_group | None | User Administration | No |
| Group Member | sys_user_grmember | None | User Administration | No |
| Role | sys_user_role | None | User Administration | No |
| User Role | sys_user_has_role | None | User Administration | No |
### Vulnerability Response
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Vulnerability | sn_vul_vulnerability | task | Vulnerability Response | Yes |
### Workflow
| Table Label | Table Name | Parent Table | Module Name | Is Extendable |
| --- | --- | --- | --- | --- |
| Workflow | wf_workflow | None | Workflow | No |
| Workflow Context | wf_context | None | Workflow | No |
