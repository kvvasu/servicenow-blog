---
title: "Flow Designer Training"
description: "Flow Designer training notes: how triggers, actions and subflows compose, and when a flow beats a business rule."
slug: "servicenow-flow-designer-training"
draft: false
tableOfContents: true
---

Flow Designer replaces a certain amount of scripting with declared steps, which is a gain when the logic is genuinely a sequence. This page covers how the pieces compose and when to stop using it.

### GETTING STARTED
Flow Designer builds automation without hand-written server scripts, and the designer stores everything in sys_hub_flow. Start with a trigger on a table, add an action that reads or writes a record, and branch on the result. A flow runs as the user who triggered it, so an untested flow can fail on ACLs. An author can set a run-as identity instead. Test each path with the flow log open, and check that no step repeats indefinitely.
- [YouTube video qeSumpq0KVM](https://www.youtube.com/watch?v=qeSumpq0KVM)
- [YouTube video c5sA9LMnbt8](https://www.youtube.com/watch?v=c5sA9LMnbt8)
- [YouTube video HNHHdn5VEa4](https://www.youtube.com/watch?v=HNHHdn5VEa4)
- [YouTube video LrLwhtgBKZA](https://www.youtube.com/watch?v=LrLwhtgBKZA)
- [YouTube video 8l9T2f4u3qs](https://www.youtube.com/watch?v=8l9T2f4u3qs)
- [YouTube video sXuKaV9aSNQ](https://www.youtube.com/watch?v=sXuKaV9aSNQ)
- [YouTube video U898c4PMsWA](https://www.youtube.com/watch?v=U898c4PMsWA)
- [YouTube video yOJx4-hBl5k](https://www.youtube.com/watch?v=yOJx4-hBl5k)
