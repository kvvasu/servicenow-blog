---
title: "GlideQuery Examples"
description: "GlideQuery examples from Peter Bell, Andrew Barnes and Jace Benson, collected as a working reference for server-side queries without GlideRecord."
slug: "servicenow-glide-query-examples"
draft: false
tableOfContents: true
---

GlideQuery is a different way to read the platform's data: chainable, harder to get wrong, and far less forgiving of the habits GlideRecord taught you. This page collects worked examples from three practitioners and points to their original material.

## ServiceNow GlideQuery Examples by Peter Bell, Andrew Barnes, and Jace Benson
GlideQuery offers a fluent alternative to GlideRecord for server-side reads. Developers chain methods like where, select, and orderBy, then call toArray to run the query. The style reads like a description of the data you want, which makes review easier. GlideQuery also throws an error when a query fails, where GlideRecord returns a false value that code often ignores. Peter Bell, Andrew Barnes, and Jace Benson show real examples. Use it for reads, and keep GlideRecord for updates inside a loop.
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p1/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p2/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p3/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p4/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p5/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p6/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p7/)
- [developer.servicenow.com](https://developer.servicenow.com/blog.do?p=/post/glidequery-p8/)
- [jace.pro](https://jace.pro/post/2020-05-24-glide-freaking-query-wow/)
