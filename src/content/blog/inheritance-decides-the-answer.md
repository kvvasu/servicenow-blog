---
title: "Before You Query: Inheritance Decides the Answer"
description: "Why a query against a parent table returns child records too, and how to read a table's parent and extendability before writing the filter."
date: 2026-10-01
tags: ["data-model", "tables", "itsm"]
draft: false
---

Most surprising query results on the platform are not query bugs. They are inheritance.

Every table extends another table. A query against a parent table returns the parent records and the child records. That result is either exactly what you wanted or the bug that you are about to write. The only way to know which one it is: read the parent before you write the filter.

## The one question to ask first

Before any query, answer this: **what is the top of this table's chain?** **Does my filter match records in the children too?**

Take a table that extends task. If you query the task table for records updated in the last day, you get incidents, problems and changes. You also get every custom table that extends task. All of those records are tasks. A report that says "we had 400 tasks yesterday" can be correct and completely misleading.

Do not abandon the parent table. The parent table gives you a cross-process view, and that view is often the point. Filter on the specific child table when you mean the child.

## Reading the model

Three facts about a table decide what a query will do:

- **parent** — what it extends, which determines the fields it inherits
- **extendable** — whether something else can extend it, which predicts what will appear in it later
- **hierarchy** — the full chain, which is what actually determines the returned set

People skip the third fact. Two levels up is still inside the scope of the query.

## A pattern that survives schema changes

Sometimes you need all tasks, with a count for each kind. Then query the parent and group the results in code. Do not guess:

```javascript
var gr = new GlideRecord('task');
gr.addQuery('sys_updated_on', '>=', gs.daysAgoStart(1));
gr.setLimit(1000);
gr.query();
var byTable = {};
while (gr.next()) {
  var t = gr.getTableName();
  byTable[t] = (byTable[t] || 0) + 1;
}
gs.info('[audit] tasks by table: ' + JSON.stringify(byTable));
```

`getTableName()` answers the question that the parent query hides. Run this code once against a real instance. Then the hierarchy stops being abstract. The child tables that appear are the tables that your reports have been quietly including.

## Where inheritance bites hardest

Three places, in my experience:

1. **Reports and dashboards.** A filter that is correct against the parent gives numbers that nobody can reconcile with the process owner's numbers.
2. **ACLs.** Permissions on a parent apply across the chain. A rule that seems limited to one process can quietly control another.
3. **Custom tables.** A new table that extends task joins every existing task query as soon as it exists. Nobody changed a query. The answers changed anyway.

That third case is the reason to check `extendable` before you design custom work. A heavily queried parent is convenient to extend now. It stays that way forever.

## What to keep beside the query

Write three lines next to any non-obvious query:

- table queried, and its parent chain
- why the parent is the right level, or why the child is
- the ceiling on rows, and what happens when it is reached

The third line turns a performance problem into a decision. You can discuss a query with a stated ceiling. A query that has never reached its limit has never been tested.

## Sources

- Table dictionary, inheritance and extendability are documented in the ServiceNow product documentation: [servicenow.com/docs](https://www.servicenow.com/docs/) — read the dictionary entry for your own release before relying on a parent chain.
- A free developer instance is the fastest place to run the counting snippet above: [developer.servicenow.com](https://developer.servicenow.com/dev.do)
