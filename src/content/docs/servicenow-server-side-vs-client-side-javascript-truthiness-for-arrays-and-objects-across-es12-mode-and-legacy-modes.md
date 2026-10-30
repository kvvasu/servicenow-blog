---
title: "JavaScript Truthiness: ES12 vs Legacy Modes"
description: "Why an empty array can read as false in legacy server-side modes, and how to treat missing, empty and invalid as three separate states."
slug: "servicenow-server-side-vs-client-side-javascript-truthiness-for-arrays-and-objects-across-es12-mode-and-legacy-modes"
draft: false
tableOfContents: true
---

This is the failure mode that eats a weekend. A payload arrives, an empty array is treated as false, and an integration silently does nothing. The page works through the cause, the shapes that break most often, and a contract-first pattern that removes the ambiguity.

## Why ES12 changes the game
### Executive summary
Arrays and objects are objects, so every standard JavaScript runtime treats them as truthy. That includes an empty array and an empty object. Browsers follow the specification, and modern server-side scripting on the platform does too. Legacy server engines diverged for some cases. A check like if (response) can therefore pass in the browser and fail in the script that runs elsewhere. Treat truthiness as an unreliable test for emptiness and compare length or a key count instead.
### Your observation, explained
The test shows why truthiness and emptiness are separate ideas. The browser evaluates an empty array as an object, and objects are truthy, so the branch runs. The code then reads the array as if it held records. When that same script runs where the engine disagrees, the branch skips and the integration returns an empty payload. Neither outcome reflects the actual data. A developer who checks response.length gets the same answer everywhere.
```javascript
// Standard JavaScript behavior (browsers, and spec):
var response = [];
if (response) {
// Runs, because [] is an object and therefore truthy
}
```
### Why this becomes a “weeks of debugging” integration bug
The bug hides because both environments claim to run JavaScript. A browser console test passes, so the developer trusts the logic and ships it. The integration script runs elsewhere, takes the other branch, and returns nothing. Logs show a successful call, so attention moves to the remote system, the credentials, and the network. Time passes before anyone prints the response object itself. Mixed runtimes turn a one-line guard clause into a long investigation.
### The golden rule: treat “missing”, “empty”, and “invalid” as three different states
Anti-pattern (bug magnet):
📋 Copy Code
```text
// BAD: ambiguous. What does "truthy" mean here?
if (items) {
process(items);
} else {
throw new Error("Integration failed");
}
```
Production-grade pattern (explicit):
📋 Copy Code
```javascript
function isNonEmptyArray(x) {
return Array.isArray(x) && x.length > 0;
}
function isPlainObject(x) {
return x !== null && typeof x === "object" && !Array.isArray(x);
}
function hasKeys(obj) {
return isPlainObject(obj) && Object.keys(obj).length > 0;
}

// Now your intent is explicit:
if (isNonEmptyArray(items)) {
process(items);
} else if (Array.isArray(items)) {
// empty-but-valid
processEmptyResult();
} else {
// missing or invalid
throw new Error("Invalid response shape");
}
```
### Four real-world shapes that routinely break integrations
Gateways return an empty array when no rows match, an empty object when the call fails, and a single object when exactly one row exists. Each shape passes a naive truthiness check. A Scripted REST API might wrap the payload in a result key, so the expected field sits one level deeper. MID Server scripts add another layer, because a proxy can substitute an HTML error page for JSON. Validate the shape before reading fields and fail loudly when it does not match.
### 1) Array of arrays
A batch integration often returns pages, and each page is itself an array of records. Nested arrays never help here, because an empty outer array remains a truthy object. A guard like if (payload.data) passes even when nothing arrived. Iterate with a counted loop, test the length before processing, and return early on an empty page. Otherwise the script reports success while skipping the entire batch.
```javascript
// Example response:
var pages = [
  [ {id:"A1"}, {id:"A2"} ],
  [] // page 2 is empty (valid)
];

// BAD:
if (pages[1]) {                 // might be treated falsy server-side in legacy modes
gs.info("Page 2 has data");
} else {
gs.info("Page 2 failed");     // wrong: empty page isn't failure
}

// GOOD:
if (Array.isArray(pages[1]) && pages[1].length === 0) {
gs.info("Page 2 is empty (valid). Stop paging.");
} else if (Array.isArray(pages[1])) {
gs.info("Page 2 has " + pages[1].length + " rows.");
} else {
gs.error("Page 2 missing/invalid");
}
```
### 2) Array of objects
An API that returns incidents hands back an array of objects. That array stays truthy whenever it exists, even with zero elements inside. So if (response.body.incidents) cannot separate an empty result from a populated one. Check Array.isArray on the first element and confirm the length, then guard inside the loop in case an element arrives null. Count the records that actually inserted.
```javascript
// Example response:
var incidents = []; // empty means "nothing to sync", not "failure"

// BAD:
if (incidents) {
sync(incidents);
} else {
// In legacy server-side mode, this branch might run:
throw new Error("Sync failed");
}

// GOOD:
if (!Array.isArray(incidents)) throw new Error("Invalid incidents array");
if (incidents.length === 0) {
gs.info("No incidents to sync (valid).");
} else {
sync(incidents);
}
```
### 3) Object of arrays
A gateway that groups results by category returns an object whose properties are arrays. The container object stays truthy no matter what. Reading payload.data.closed on a response that omitted that key yields undefined, and any length check then throws. Test each key explicitly, or normalize the response before use. Server-side scripts hit the same trap in legacy mode and in ES12 mode.
```javascript
// Example response:
var payload = {
users: [],
groups: ["G1","G2"]
};

// BAD:
if (payload.users) { // empty array might look falsy server-side (legacy)
gs.info("Users present");
} else {
gs.info("User fetch failed"); // wrong
}

// GOOD:
if (!payload || typeof payload !== "object") throw new Error("Bad payload");
if (!Array.isArray(payload.users)) throw new Error("payload.users must be an array");
if (payload.users.length === 0) {
gs.info("Users array is empty (valid).");
}
```
### 4) Object of objects
A nested metadata block looks like an ordinary object, and JavaScript treats every object as true. A check on the parent tells you nothing about whether the inner status block exists. Reading response.result.errors.count while result is undefined raises a TypeError that aborts the whole script. Walk each level with optional chaining or explicit checks, because one missing layer otherwise fails the entire integration run.
```javascript
// Example response:
var resp = {
ok: true,
data: {
account: { id: "ACCT-9", region: "IN" },
metrics: {} // empty metrics is valid, means "not provided"
}
};

// BAD:
if (resp.data.metrics) { // {} is always truthy in spec, but don't rely on truthiness anyway
useMetrics(resp.data.metrics);
}

// GOOD:
function hasKeys(obj) {
return obj && typeof obj === "object" && !Array.isArray(obj) && Object.keys(obj).length > 0;
}
if (hasKeys(resp.data.metrics)) {
useMetrics(resp.data.metrics);
} else {
gs.info("No metrics provided (valid).");
}
```
### GlideAjax + client-callable Script Include: a “contract-first” pattern
A client script calls GlideAjax, which invokes a server-side Script Include. Mark that Script Include client-callable, extend AbstractAjaxProcessor, and expose only the methods the UI needs. Return one JSON string from getParameters, then parse it on the client. Validate input on the server, because clients can send anything. This contract keeps logic in one place. If you return objects directly, browsers coerce types differently and the UI silently breaks.
### Server side (Script Include: Client callable)
📋 Copy Code
```javascript
var IntegrationAjax = Class.create();
IntegrationAjax.prototype = Object.extendsObject(AbstractAjaxProcessor, {

// Client calls sysparm_name=getOrders
getOrders: function () {
var customerId = this.getParameter("sysparm_customer_id");

var out = {
ok: true,
data: [],
error: null,
meta: { customerId: customerId, count: 0 }
};

try {
if (!customerId) throw new Error("Missing sysparm_customer_id");

// --- Example: pretend we called an external API and got an array back ---
// IMPORTANT: empty array means "0 orders", NOT "failed"
var orders = []; // could be empty

if (!Array.isArray(orders)) throw new Error("orders must be an array");

out.data = orders;
out.meta.count = orders.length;

return JSON.stringify(out);

} catch (e) {
out.ok = false;
out.error = String(e);
out.data = [];
out.meta.count = 0;
return JSON.stringify(out);
}
},

type: "IntegrationAjax"
});
```
### Client side (Client Script)
A Client Script runs in the browser, so the ES12 mode setting never applies to it. The truthiness trap survives anyway. g_form.getValue returns a string, a GlideAjax callback returns an object, and a bare if check accepts both. Guard with a type test plus a length check before touching the data. A client script that assumes a populated array throws in the console and leaves the form unsaved.
```javascript

function fetchOrders(customerId) {
var ga = new GlideAjax("IntegrationAjax");
ga.addParam("sysparm_name", "getOrders");
ga.addParam("sysparm_customer_id", customerId);

ga.getXMLAnswer(function (answer) {
var payload;
try {
payload = JSON.parse(answer);
} catch (e) {
console.error("Bad JSON from server", e, answer);
return;
}

if (payload.ok !== true) {
console.error("Server reported error:", payload.error);
return;
}

// Now data handling is explicit and stable across modes:
if (!Array.isArray(payload.data)) {
console.error("Invalid data shape");
return;
}

if (payload.data.length === 0) {
console.log("No orders (valid).");
// show empty state in UI
return;
}

console.log("Orders:", payload.data);
// render list
});
}
```
### Industry-standard best practices for avoiding truthiness traps
Treat missing, empty, and populated as three separate states instead of collapsing them into one boolean. Test arrays with Array.isArray plus a length comparison, and objects with an explicit key lookup or hasOwnProperty. Never let truthiness alone drive business logic, because the same expression behaves differently depending on the engine. Write one small helper, use it everywhere, and unit test it with empty payloads.
### Industry-standard best practices for integration-safe JavaScript in ServiceNow
Integration code runs against many payloads, so never trust bare truthiness for arrays or objects. An empty array stays truthy in JavaScript, and an empty object does too. Test length or keys explicitly instead. Check Array.isArray before looping, verify Object.keys(...).length before reading fields. In ES12 mode, ServiceNow enforces stricter syntax, but truthiness rules never changed. Guess wrong and a loop processes zero records while the integration reports success.
### Takeaway
Every integration bug from truthiness burns hours because the code runs without errors. A bare if (value) tells you nothing about whether value holds data. Write explicit checks, return predictable types, and log the shape of what arrives. On the server, GlideRecord and JSON parsing behave consistently; the client adds browser quirks. Fix the ambiguity at the source and future debugging gets short.
### Summary:
Truthiness is a language quirk, not a business rule. An empty array and an empty object both evaluate to true, so conditionals built on them accept missing data as valid. Decide what absence means for each integration, then test for it directly. That removes the difference between legacy and ES12 execution, makes tests meaningful, and stops silent data loss before it reaches production tables.
### References and acknowledgements (numbered footnotes)
Cite the source that pins down any behaviour your code relies on. ECMA-262 states that ToBoolean returns true for every object, so the specification itself guarantees this trap. MDN documents optional chaining and Array.isArray with runnable examples. ServiceNow product documentation lists which engine each server-side script type uses. Keep those links beside the code, so a maintainer verifies the assumption instead of trusting a comment.
