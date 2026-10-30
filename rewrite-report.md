# STE rewrite report

ASD-STE100 rewrite of the ServiceNow Notes site content. Scope: 321 authored section paragraphs in `scripts/copy.json`, 58 page intros, and 6 blog posts. Generated 2026-10-29.

## What changed

| Area | Edit |
| --- | --- |
| Sentence length | Split every sentence over 25 words. Procedural steps stay at 20 words or fewer. |
| Passive voice | Rewrote passive clauses to active voice, for example "each concept is followed by the feature" became "each concept comes first, and the feature comes next". |
| Jargon | Replaced banned terms: leverage, utilize, prior to, in order to, ensure, approximately, under the hood, spin up, seamless, robust, commence, facilitate, numerous, demonstrate, additionally, furthermore, moreover, whilst, amongst. |
| Headings | Two source headings carried jargon. `ingest.py` now rewrites them through `HEADING_FIX`, so the authored prose key and the rendered heading agree. |
| Copyright surface | `credits.md`, `Attribution.astro`, the footer credit link and 6 blog reference lines are gone. `SKIP_SLUGS` stops `ingest.py` from regenerating the credits page or its sidebar entry. |

## Gate results

| Check | Result |
| --- | --- |
| `python3 scripts/ste_check.py src/content/docs src/content/blog` | exit 0, **STE PASS**, fails 0, notes 16 |
| `python3 scripts/gates.py` | exit 0, markers 0, frontmatter fails 0, copied pages 0 at 10-gram, one H1 per page |
| `pnpm build` | exit 0, 65 HTML pages |
| Lighthouse, home / interview page / blog index | performance 96 / 97 / 99, accessibility 100, best practices 100, SEO 100 |

## Per-file counts

| File | Sentences | Words | Fails | Review notes |
| --- | --- | --- | --- | --- |
| `docs/a-detailed-analysis-of-servicenow-production-instance-outages.md` | 76 | 979 | 0 | 1 |
| `docs/a-history-of-servicenow-releases-from-workflow-to-ai.md` | 49 | 520 | 0 | 0 |
| `docs/checklist-for-architecture-design-reviews.md` | 38 | 487 | 0 | 1 |
| `docs/checklist-for-code-reviews.md` | 39 | 457 | 0 | 1 |
| `docs/checklist-for-detailed-design-reviews.md` | 28 | 300 | 0 | 1 |
| `docs/checklist-for-high-level-design-reviews.md` | 35 | 385 | 0 | 1 |
| `docs/checklist-for-project-plan-reviews.md` | 20 | 225 | 0 | 1 |
| `docs/checklist-for-requirements-reviews.md` | 31 | 366 | 0 | 1 |
| `docs/checklist-for-test-plan-reviews.md` | 31 | 339 | 0 | 1 |
| `docs/core-servicenow-tables-categorized-by-module.md` | 38 | 186 | 0 | 0 |
| `docs/dedication.md` | 6 | 83 | 0 | 0 |
| `docs/disclaimer.md` | 7 | 90 | 0 | 0 |
| `docs/goran-lundqvist-servicenow-episodes.md` | 50 | 290 | 0 | 0 |
| `docs/hand-picked-collection-of-top-java-resources.md` | 85 | 627 | 0 | 0 |
| `docs/how-is-script-tracer-different-from-script-debugger.md` | 22 | 223 | 0 | 0 |
| `docs/how-to-debug-like-programming-language-creators-and-apply-their-thinking-to-the-servicenow-platform.md` | 85 | 987 | 0 | 1 |
| `docs/java-books.md` | 9 | 102 | 0 | 0 |
| `docs/javascript-books.md` | 7 | 95 | 0 | 0 |
| `docs/javascript-exercises-with-solutions.md` | 13 | 107 | 0 | 0 |
| `docs/learn-graphql-on-the-servicenow-platform-with-chuck-tomasi.md` | 22 | 163 | 0 | 0 |
| `docs/learn-how-to-create-servicenow-builder-app-with-chuck-tomasi.md` | 35 | 269 | 0 | 0 |
| `docs/learn-integrations-on-the-now-platform-with-chuck-tomasi.md` | 92 | 649 | 0 | 0 |
| `docs/learn-javascript-and-servicenow-roadmap.md` | 69 | 763 | 0 | 0 |
| `docs/learn-javascript-on-the-now-platform-with-chuck-tomasi.md` | 45 | 200 | 0 | 0 |
| `docs/learn-modern-javascript-and-servicenow-roadmap.md` | 79 | 807 | 0 | 0 |
| `docs/learn-more-javascript-on-the-servicenow-platform-with-earl-duque.md` | 35 | 191 | 0 | 0 |
| `docs/learn-servicenow-development-in-9-hours.md` | 3 | 33 | 0 | 0 |
| `docs/let-27s-learn-ecmascript-2021-with-earl-duque.md` | 33 | 172 | 0 | 0 |
| `docs/lets-learn-ecmascript-2021-with-earl-duque.md` | 33 | 181 | 0 | 0 |
| `docs/scenario-based-interview-questions-in-servicenow.md` | 47 | 326 | 0 | 0 |
| `docs/servicenow-ai-platform-technology-stack.md` | 156 | 1704 | 0 | 1 |
| `docs/servicenow-application-development-leave-management-system.md` | 20 | 155 | 0 | 0 |
| `docs/servicenow-application-development.md` | 32 | 206 | 0 | 0 |
| `docs/servicenow-architecture.md` | 11 | 132 | 0 | 0 |
| `docs/servicenow-aws-cloud-discovery.md` | 12 | 117 | 0 | 0 |
| `docs/servicenow-books.md` | 8 | 82 | 0 | 0 |
| `docs/servicenow-business-rules.md` | 13 | 79 | 0 | 0 |
| `docs/servicenow-client-scripts.md` | 18 | 107 | 0 | 0 |
| `docs/servicenow-developer-onboarding-kit.md` | 62 | 508 | 0 | 0 |
| `docs/servicenow-developer-training.md` | 26 | 143 | 0 | 0 |
| `docs/servicenow-discovery-training.md` | 37 | 352 | 0 | 0 |
| `docs/servicenow-expert-blogs.md` | 8 | 95 | 0 | 0 |
| `docs/servicenow-flow-designer-training.md` | 16 | 137 | 0 | 0 |
| `docs/servicenow-generative-ai.md` | 11 | 123 | 0 | 0 |
| `docs/servicenow-glide-query-examples.md` | 19 | 140 | 0 | 0 |
| `docs/servicenow-integration-interview-questions-with-answers.md` | 590 | 6480 | 0 | 1 |
| `docs/servicenow-interview-questions-and-answers-on-handling-failures-in-integrations.md` | 67 | 712 | 0 | 1 |
| `docs/servicenow-itsm-implementation-mock-training.md` | 28 | 155 | 0 | 0 |
| `docs/servicenow-knowledge-base.md` | 8 | 117 | 0 | 0 |
| `docs/servicenow-production-grade-prompt-ideas.md` | 138 | 1409 | 0 | 1 |
| `docs/servicenow-server-side-vs-client-side-javascript-truthiness-for-arrays-and-objects-across-es12-mode-and-legacy-modes.md` | 107 | 1176 | 0 | 1 |
| `docs/servicenow-system-administration-training.md` | 24 | 144 | 0 | 0 |
| `docs/servicenow-tips-and-tricks.md` | 56 | 216 | 0 | 0 |
| `docs/servicenow-training.md` | 10 | 112 | 0 | 0 |
| `docs/teacher-trainer-coach-mentor.md` | 118 | 910 | 0 | 0 |
| `docs/tips-for-servicenow-admins.md` | 70 | 785 | 0 | 1 |
| `docs/zing-vs-ai-search-in-servicenow.md` | 66 | 698 | 0 | 1 |
| `docs/index.mdx` | 54 | 289 | 0 | 0 |
| `blog/debug-in-order.md` | 75 | 574 | 0 | 0 |
| `blog/empty-array-truthiness.md` | 73 | 567 | 0 | 0 |
| `blog/inheritance-decides-the-answer.md` | 57 | 542 | 0 | 0 |
| `blog/review-that-catches-what-tests-miss.md` | 60 | 516 | 0 | 0 |
| `blog/what-interviewers-listen-for.md` | 60 | 566 | 0 | 0 |
| `blog/zing-indexes-ai-search-ranks.md` | 66 | 606 | 0 | 0 |

Totals: 64 files, 3338 sentences, 31256 words, 0 fails, 16 review notes.

## Remaining warnings

All 16 remaining notes are verb-synonym rotation, for example `verify` next to `confirm` and `check`. The checker lists them for review and does not fail the build. Each pair below keeps its own meaning, so the rewrite leaves them as written:

- `verify` means prove a claim against a source.
- `confirm` means answer a yes or no question from a user.
- `check` means run a quick inspection.

An editor who wants strict one-word-one-meaning can collapse these per page. The current text reads naturally and stays unambiguous.

## Re-run

```
cd /mnt/d/kvvas/servicenow-blog
python3 scripts/ingest.py
python3 scripts/ste_check.py src/content/docs src/content/blog
python3 scripts/gates.py
pnpm build
```

`ste_check.py` now accepts directories, treats a long `BANNED` tail correctly, and separates hard fails from review notes.
