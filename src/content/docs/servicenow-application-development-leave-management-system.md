---
title: "Leave Management Application"
description: "A worked walkthrough of building a leave management application on the platform: the table design, the approval path and the reporting it needs."
slug: "servicenow-application-development-leave-management-system"
draft: false
tableOfContents: true
---

Leave management is a small, honest application: one record, one approval path, one balance that must stay correct. Building it end to end teaches scoping, because every part of it maps to a decision you will meet again in larger work.

### GETTING STARTED
A leave management application makes a good first scoped build because the data model stays small. Create a scoped application, then add tables for leave requests and balances. Define fields for the employee reference, dates, type, and approval state. Add a Flow that routes each request to the manager, and a Business Rule that checks the balance before insert. Test with a user who holds only the end-user role, because an admin bypasses the ACLs that protect the records.

### Scoped app artifacts

```filetree title="Scoped app artifacts"
leave-management/
  tables/x_leave_request
  tables/x_leave_balance
  business-rules/check-balance.js
  flows/manager-approval
  acls/check-leave-balance-acl
```

- [YouTube video 2u3yqgyioi4](https://www.youtube.com/watch?v=2u3yqgyioi4)
- [YouTube video S-0xfjDq_Tc](https://www.youtube.com/watch?v=S-0xfjDq_Tc)
- [YouTube video WGdfk17NshU](https://www.youtube.com/watch?v=WGdfk17NshU)
- [YouTube video ZktM9fLE4rY](https://www.youtube.com/watch?v=ZktM9fLE4rY)
- [YouTube video D6R2UBOrWmg](https://www.youtube.com/watch?v=D6R2UBOrWmg)
- [YouTube video 2OA-lxkrow8](https://www.youtube.com/watch?v=2OA-lxkrow8)
- [YouTube video LPX5LjdEquo](https://www.youtube.com/watch?v=LPX5LjdEquo)
- [YouTube video fKam0Q5LdqY](https://www.youtube.com/watch?v=fKam0Q5LdqY)
- [YouTube video P7datk5Ae3A](https://www.youtube.com/watch?v=P7datk5Ae3A)
- [YouTube video _s9qYqFYB8M](https://www.youtube.com/watch?v=_s9qYqFYB8M)
- [YouTube video rwpLKyEocJU](https://www.youtube.com/watch?v=rwpLKyEocJU)
