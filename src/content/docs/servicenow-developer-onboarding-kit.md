---
title: "Developer Onboarding Kit"
description: "A first-week onboarding kit for ServiceNow developers: the instance access, the patterns to read first, and the habits to form before touching production."
slug: "servicenow-developer-onboarding-kit"
draft: false
tableOfContents: true
---

A developer's first week decides whether they learn the platform's grain or fight it. This kit orders the first steps: get a personal instance, read the patterns before writing them, and never experiment in production.

## ServiceNow Developer Onboarding Kit
### The [Team Name] ServiceNow Developer Standard
Version: 2.0 | Status: Active
Target Audience: All Developers & Architects
### 1. The Manifesto: How We Build
Working code is the floor, not the goal. Every change must survive an upgrade, hold under load and stay readable for the next developer. A solution that passes a demo but blocks a clone does damage later. Write the design down, name the objects clearly, and reject anything the platform already does natively.
### The "Never" List (Immediate Rejection)
A Client Script runs in the browser, so a GlideRecord call there opens the database to the form user. It returns records that session should not see. Call GlideAjax against a Script Include instead, and let the server enforce access through ACLs. Synchronous server calls freeze the form for everyone using it.
### The "Always" List
When the user needs no immediate answer, push the work to an Async Business Rule, a scheduled job or a Flow. The current transaction commits first, so a long task cannot block the user's save. Wrap logic in a try/catch, log the failure and let the job retry. Check an update guard flag so a rule does not fire on its own update.
### 2. Server-Side Standard: The "Handler" Pattern
Keep Business Rules thin. A rule should decide when to act and call one method on a Script Include. That class holds the logic, so a second rule or a REST endpoint reuses it instead of copying code. Test the class directly and one fix repairs every caller. Duplicated logic across several rules drifts apart and fails quietly.
### 📄 Copy-Paste Template: `ServiceHandlerBase`
📋 Copy Code
```javascript
var ServiceHandlerBase = Class.create();
ServiceHandlerBase.prototype = {

initialize: function() {
// Controlled by System Property: 'x_scope.debug.enabled'
this.debug = gs.getProperty('x_scope.debug.enabled', 'false') == 'true';
this.logPrefix = '[ServiceHandler]: ';
this.startTime = new Date().getTime();
},

// STANDARD ENTRY POINT
processLogic: function(payload) {
var result = this._initResponse();

try {
this._logDebug('Starting processLogic with payload: ' + JSON.stringify(payload));

// 1. Validate Input
if (!payload) throw new Error('Missing payload parameter.');

// 2. Normalize Data
var dataObj = (typeof payload === 'string') ? JSON.parse(payload) : payload;

// 3. Execute Business Logic
// var recordID = this._internalFunction(dataObj);

// 4. Success Response
result.status = 'success';
result.message = 'Operation complete';
result.data = { processed_at: new GlideDateTime().getDisplayValue() };

} catch (e) {
result.status = 'error';
result.message = e.message;
this._logError('processLogic failed', e);
} finally {
this._logPerformance('processLogic');
}

return result;
},

// --- HELPERS ---

_initResponse: function() {
return { status: 'error', message: '', data: null };
},

_logDebug: function(msg) {
if (this.debug) gs.info(this.logPrefix + msg);
},

_logError: function(msg, errorObj) {
var details = (errorObj) ? ' | Msg: ' + errorObj.message + ' | Stack: ' + errorObj.stack : '';
gs.error(this.logPrefix + 'ERROR: ' + msg + details);
},

_logPerformance: function(methodName) {
if (this.debug) {
var duration = new Date().getTime() - this.startTime;
gs.info(this.logPrefix + 'PERF [' + methodName + ']: ' + duration + 'ms');
}
},

type: 'ServiceHandlerBase'
};
```
### 3. Client-Side Standard: The "Resilient" Ajax
A Client Script that calls the server must also handle a slow or failed answer. Pass a callback to GlideAjax, show a busy indicator, and clear the field when the call returns an error. Never block the browser with synchronous g_form.getReference calls inside a loop. Debounce onChange handlers, or every keystroke fires another round trip.
### 📄 Copy-Paste Template: `GlideAjax`
📋 Copy Code
```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
if (isLoading || newValue === '') return;

// UX: Give feedback
g_form.hideFieldMsg('your_field');
g_form.showFieldMsg('your_field', 'Validating...', 'info');

// 1. PREPARE PAYLOAD (One JSON object)
var payload = {
userID: g_user.userID,
value: newValue,
recordID: g_form.getUniqueValue()
};

// 2. CALL SERVER
var ga = new GlideAjax('x_scope.ServiceHandlerBase');
ga.addParam('sysparm_name', 'processLogic');
ga.addParam('sysparm_data', JSON.stringify(payload));

// 3. HANDLE RESPONSE (Using getXMLAnswer)
ga.getXMLAnswer(function(answer) {
g_form.hideFieldMsg('your_field');

if (!answer) {
g_form.addErrorMessage('Connection Error: No response from server.');
return;
}

try {
var response = JSON.parse(answer);

if (response.status === 'success') {
// SUCCESS LOGIC
// g_form.setValue('target', response.data.val);
} else {
// LOGIC ERROR (e.g. Validation failed)
g_form.showFieldMsg('your_field', response.message, 'error');
}
} catch (e) {
// CRITICAL ERROR (HTML response / 500 Error)
console.error('JSON Parse Error:', e);
g_form.addErrorMessage('System Error. Please contact support.');
}
});
}
```
### 4. The Design Process (TDD)
Before writing code, answer these in the story: which table holds the data, which roles touch it, and what starts the logic. State the expected result for one normal case and two edge cases. Name every object the change touches, and check whether an existing Business Rule or Flow already fires on that table. Vagueness here becomes rework.
### 5. The "Gatekeeper" Checklist (Code Review)
A reviewer rejects a change that queries inside a loop, leaves a GlideRecord unclosed, or hardcodes a sys_id. A new table without ACLs exposes data to every authenticated user. A Business Rule that runs on each insert of a high-volume table slows the instance for everyone. gs.info logging on a hot path fills the log table.
### 6. Expert Toolkit
Save these for emergency debugging.
| Tool | Usage | Purpose |
| --- | --- | --- |
| Cancel Transaction | cancel_my_transaction.do | The "Panic Button" when a script freezes your browser. |
| Node Stats | stats.do | Check memory/semaphore usage. |
| Filter Trick | Table.FILTER | Opens a table without loading data (prevents crashing on massive tables). |
| Cluster Msg | GlideClusterMessage | Used to flush cache across all nodes. |
| Row Lock | setWorkflow(false) | Warning: Disables Activity Stream and sys_updated_on. Use with extreme caution. |
