---
title: "Script Tracer vs Script Debugger"
description: "Which ServiceNow debugging tool answers which question: reading recorded execution with Script Tracer, or stepping through live logic in the debugger."
slug: "how-is-script-tracer-different-from-script-debugger"
draft: false
tableOfContents: true
---

Both tools show you what your script did, and choosing the wrong one wastes time. The distinction is simple: a trace records what already happened, a debug session shows you what is happening now.

## Script tracer vs Script debugger
These two tools watch different halves of a transaction. Script Debugger runs in the browser and steps through client-side code such as onLoad, onChange, and UI policy scripts. A developer sets breakpoints in the browser developer tools. Script Tracer works on the server, replaying a form transaction and listing the Business Rules, script includes, and GlideRecord operations that fired. Reach for the tracer when the fault hides behind the UI, and use the debugger when a form behaves oddly before any server call runs.
### GETTING STARTED
Start from a record that reproduces the fault rather than an empty test form. Enable the tracer, load the page, and read the output line by line to find which server script runs last. Then open the script debugger on the same form and step through the client logic. Compare the two timelines. Most confusion disappears once a developer sees where client execution ends and the server round trip begins. Practise on a sub-production instance, because tracing writes log data.
- [YouTube video rRJuVkgoG_M](https://www.youtube.com/watch?v=rRJuVkgoG_M)
- [YouTube video drzwGy9OtbY](https://www.youtube.com/watch?v=drzwGy9OtbY)
- [YouTube video 9nozDeAVQow](https://www.youtube.com/watch?v=9nozDeAVQow)
- [YouTube video js0Q-d7HEdA](https://www.youtube.com/watch?v=js0Q-d7HEdA)
- [YouTube video 8Q45xoYEPhI](https://www.youtube.com/watch?v=8Q45xoYEPhI)
- [YouTube video PjZpqlnXJCA](https://www.youtube.com/watch?v=PjZpqlnXJCA)
