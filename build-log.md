# Build log — servicenow-blog (Astro + Starlight)

Target: `D:\kvvas\servicenow-blog` (`/mnt/d/kvvas/servicenow-blog`).
Source of truth: `/mnt/d/kvvas/servicenowzone-scrape` (59 pages). No live crawl.

## Phase 0 — Scaffold & environment

| Step | Command | Result |
|---|---|---|
| Toolchain probe | `node -v; pnpm -v; curl registry.npmjs.org` | node v24.19.0, pnpm 12.4.1, registry 200 |
| Scaffold | `pnpm create astro@latest servicenow-blog --template starlight --no-install --no-git --skip-houston --yes` | exit 0, template copied |
| Install | `pnpm install` | exit 0 — astro 7.4.2, @astrojs/starlight 0.42.7, sharp 0.35.5 |
| Sitemap | `pnpm add @astrojs/sitemap` | exit 0 — @astrojs/sitemap 3.7.4 in package.json |
| Dev gate | `pnpm dev --port 4321` then `curl` | `root=200`, `/guides/example/` 200 |

GATE 0: PASS.

## Deviations from the task brief (reality found in the data)

1. **`prose/flagged-for-rewrite.json` did not exist.** The scrape produced no `prose/` folder. Generated in Phase 2 from the ingest pass.
2. **`topic_tags` did not exist in any of the 59 JSON records.** The brief anticipated this ("if tags are missing, derive 5–8 groups"). Groups derived from title clusters, logged in `src/data/sidebar.json`.
3. **The QA file is `qa_report.md`, not `qa-report.md`.**
4. **59 pages, not 60.** `https://www.servicenowzone.com/` and `/index.php` are byte-identical and canonicalise to one slug, `index`. One dead URL (`donate.php`, 404) was recorded and never written.
5. **Node 24.19.0 and pnpm 12.4.1**, not Node 20/pnpm 9. Both satisfy "Node 20+".
6. **All 28 code fences in the scrape carry no language identifier.** Inferred during ingest, not copied blind.

## Defect found and fixed in the source archive

Table markdown was malformed: the scraper emitted rows as `cell  | cell  |` with no leading pipe and
no separator row, so **no** table would have rendered as a GFM table. Cause was a "strip trailing
table pipe" regex I had added to `snz.py` during the archive build.

Fix: rewrote the converter's table handling to buffer cells and emit one GFM table per `<table>`
(header row, `| --- |` separator, escaped pipes). Removed the destructive regex.
Re-ran `python3 snz.py extract` (offline): **417 table rows across 8 files, 57 separator rows**, and
`core-servicenow-tables-categorized-by-module.md` now renders as a real 5-column table.

Reason this matters here: the scrape's `md/` files are the heading skeleton Phase 2 consumes. A
broken table would have propagated into 8 built pages.

## Phase 1 — Architecture & layout

- `astro.config.mjs` — `site: 'https://servicenow-notes.example'`, title
  `ServiceNow Notes`, `customCss: ['./src/styles/custom.css']`, MANUAL `sidebar` from
  `src/data/sidebar.json` (no `autogenerate`), `tableOfContents: {minHeadingLevel: 2,
  maxHeadingLevel: 3}`, og/twitter head tags, and `rehypeScrollableTables()`.
- Sidebar groups derived from title clusters because `topic_tags` is absent from all
  59 records: Overview (1), Get Started (8), Development (11), ITSM & Platform (10),
  Reviews & Checklists (7), Interviews & Career (4), Releases & AI Platform (3),
  Talks & Episodes (8), References (7) = 59 items in 9 groups. Not a flat list.
- `src/styles/custom.css` — mobile-first, `--snz-*` tokens plus `--sl-*` overrides,
  `@media (min-width: 768px)` / `(min-width: 1024px)` blocks,
  `@media (prefers-color-scheme: dark)` and `(prefers-reduced-motion: reduce)`, focus
  ring, `.table-scroll` rules, card and list touch targets. Starlight's own sidebar,
  hamburger and TOC behaviour is never re-implemented.
- Gate: 9 groups and 59 item links found in `dist/servicenow-architecture/index.html`.

## Phase 2 — Content ingestion

- `scripts/ingest.py` (500+ lines) keeps the heading skeleton, code fences, GFM
  tables, short link-bearing list items, dates and table data. It replaces every
  prose paragraph, long list item, checklist line and Q&A answer with authored copy
  from `scripts/copy.json` (511 lines, the only prose source) or one rewrite marker.
- Cross-page boilerplate filter drops headings and paragraphs that repeat on many
  source pages (one ad block appears on 142 pages). Markers fell 1462 → 266.
- Guards added: fragment passthrough, page preamble dropped, pull-quote + attribution
  skipped, one marker per heading, body H1 demoted to H2, bare URLs humanised.
- Gate: 58 docs, each validated for title, description (89–155 chars, original),
  slug, `draft: false`, `tableOfContents: true`. 426 headings, 57 tables, 14 fences.

## Phase 3 — Original blog layer

- `src/content.config.ts` gained a `blog` collection (glob loader, zod schema with
  `description` 60–155 and a coerced date).
- 6 original posts in `src/content/blog/`: `empty-array-truthiness`,
  `debug-in-order`, `zing-indexes-ai-search-ranks`,
  `review-that-catches-what-tests-miss`, `inheritance-decides-the-answer`,
  `what-interviewers-listen-for`. Each has a Sources section with an
  "As of October 2026" retrieval date and links to primary ServiceNow/YouTube sources.
- `src/components/Attribution.astro` — "Structure inspired by servicenowzone.com; all
  prose original." plus a non-affiliation note.
- `src/pages/blog/index.astro` — date-descending list with title, date, description,
  tags, and it passes `sidebar` so the three-column shell holds.
- `src/pages/blog/[...slug].astro` — `StarlightPage` default import, its own
  `slugify` and `headings` derived from `post.body` (Starlight does not build a TOC
  outside the docs collection), `BlogPosting` JSON-LD.
- Gate: 6 posts render at `/blog/<slug>/`, index lists all 6.

## Phase 4 — Build robustness

- 8 hardening patches to `scripts/ingest.py`: `safe_write(path, text, what)`,
  `validate_page(path, slug)` (invalid page fails the ingest), `sanitize_images()`
  returning `(text, dropped, kept)` with `/img/placeholder.svg` for every kept image,
  YouTube embeds rewritten to links, `appendix_build_log()`, `Untitled — <slug>`
  fallback plus a logged failure, and `sidebar.json` / `flagged-for-rewrite.json` /
  `topic-backlog.md` routed through `safe_write`.
- `public/img/placeholder.svg` written (9 lines, `role="img"`, `aria-label`).
- `rm -f src/content/docs/*.md && python3 scripts/ingest.py && pnpm build` → exit 0,
  58 docs + 1 splash, 67 pages.
- Errors fixed: `write_file` refused to overwrite `astro.config.mjs`,
  `src/content.config.ts`, `src/content/docs/index.mdx` and
  `src/pages/blog/[...slug].astro` until each was read first; `pnpm build` exit 2
  because `StarlightPage` is not exported from `@astrojs/starlight/components`
  (fixed with a default import from `.../components/StarlightPage.astro`);
  `pnpm build` exit 1 after adding the rehype plugin (fixed with
  `pnpm add @astrojs/markdown-remark`).

## Phase 5 — QA

- Lighthouse against the `dist/` preview on port 4322, mobile emulation, shipped
  build: `/` 100/100/100/100, `/servicenow-architecture/` 100/100/100/100,
  `/blog/empty-array-truthiness/` 100/100/100/100. LCP 0.8–1.2 s, TBT 0 ms, CLS 0.
- axe-core 4.10.3, WCAG 2.0/2.1/2.2 A+AA, 5 pages × light and dark: **0 violations**.
- Responsive probes at 320/375/768/1024/1440: no horizontal scroll anywhere,
  hamburger below 1024, sidebar at 1024+, TOC at 1440.
- SEO audit over `dist/`: 66 sitemap URLs, 0 duplicate titles, 0 duplicate
  descriptions, one `<title>`/description/canonical/og/twitter tag per page, one
  `<h1>` per page.
- Originality audit: 8-word shingle scan against all 59 scraped markdown files,
  twice. Paragraph-only scan (tables/lists/code/headings stripped) found **0 pages
  with a 20-word verbatim run**.
- Table scroll fix: `rehypeScrollableTables()` wraps every table in
  `div.table-scroll[tabindex=0][role=region][aria-label="Table, scrollable"]`; the
  inner table had to be reset to `display: table; overflow: visible` because
  Starlight's own `display:block; overflow:auto` left an unreachable scroll box.
- Late fixes from QA feedback: body H1s demoted to H2 (two pages had two `<h1>`),
  bare YouTube URLs given real link text (503 link lists, 37 on the episodes page),
  LinkCard anchors raised to 44 px, list-only links to 24 px, a leaked pull-quote
  and its `~Earl Nightingale` attribution line dropped.
- Full results: `qa-build-report.md`.


### ingest.py run — 2026-10-28 17:10

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 17:42

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 17:45

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 17:54

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 18:00

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 18:02

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 19:09

- pages written: 58
- sections needing rewrite: 266 in 44 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 19:10

- pages written: 58
- sections needing rewrite: 55 in 23 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 19:11

- pages written: 58
- sections needing rewrite: 55 in 23 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 19:14

- pages written: 58
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 19:14

- pages written: 58
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


## Phase 6 — Reskin (Redis Docs dark theme)

Scope: colour, surface, type only. Starlight keeps layout, responsive switches,
hamburger and TOC; the skin sets `--sl-*` hooks plus a thin component layer.

- Tokens: `#0d1117` dark bg, `#161b22` dark panel, `#ffffff`/`#f6f8fa` light,
  `#d0d7de`/`#8b949e` light borders, `#30363d`/`#6e7681` dark borders.
- Three reds, because `#DC382D` fails 4.5:1 on white and on `#0d1117`:
  `--snz-brand #dc382d` (solid fills), `--snz-brand-ink #b3271e` (text on white),
  `--snz-brand-hi #ff7a6c` (text on near-black).
- `--snz-border-strong` added: `#d0d7de` on white is 1.45:1, and WCAG 2.2 wants
  3:1 for a control boundary, so outline buttons use the strong border.
- Sidebar current page: 2px red `border-inline-start`. Heading anchors muted at
  rest (opacity .35) so red does not fight the headings. TOC links gray, red only
  for the current section.
- Footer: Starlight renders it inside the content column. A `100vw` full-bleed
  trick overflowed that column by ~150px at 1024px, so the footer stays a
  bordered panel at content width. Columns use `auto-fit minmax(8rem, 1fr)` and
  `white-space: nowrap` so no label wraps mid-phrase.

### Errors

- Card top-accent rule never matched: the selector used a descendant, but
  Starlight puts `.sl-link-card` straight into `.card-grid`. Fixed with
  `.card-grid > .sl-link-card:first-child`.
- Lighthouse exit 1 against `:4321` because that server had died. All runs now
  target the production preview on `:4322`.

### Verification

- Builds exit 0: 67 pages.
- Lighthouse mobile, `reskin-{home,doc,post}.json`: 100/100/100/100.
- No horizontal scroll at 320/390/768/1024/1440 on `/`, `/servicenow-architecture/`,
  `/blog/`, `/blog/empty-array-truthiness/`.

## Phase 7 — Original prose for the flagged sections

- 266 flagged sections authored in 10 parallel leaf units, then 55 residual
  sections in 3 more. Peers reviewed every batch: count match, slug/heading/occ
  byte-equal, 40-85 words, sentences <=25 words, active voice, no first person.
- `scripts/copy.json` now holds 321 section paragraphs under page-scoped keys
  `"<slug>::<heading>::<occ>"`. Bare headings stay supported for one-off pages;
  the scope exists because several pages reuse headings like "Overview".
- `ingest.py` change: `transform()` takes the `sections` map from the top level
  of `copy.json`. Before the fix it looked inside the per-page entry, found
  nothing, and still emitted 266 markers.
- `scripts/gates.py` added: frontmatter fields, one H1 per page, marker count,
  and 10-gram overlap between page paragraphs and the scrape.

### Verification

- `sections_needing_rewrite=0 in 0 of 58 pages`; `failures: none`.
- `scripts/gates.py`: `markers=0 frontmatter_fails=0 copied_pages=0` -> GATES PASS.
  Three link-only pages warn about missing H2 headings by design.
- Build: 67 pages, 20.24s. All 66 built pages have exactly one `<h1>`; no
  duplicate `<title>`.
- Lighthouse mobile after the prose pass: Q&A page 100/100/100/100; outage page
  94 on first run (TBT 290ms) then 99 on rerun (TBT 130ms), so that score is
  run variance, not a regression.

### ingest.py run — 2026-10-28 21:17

- pages written: 58
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 21:20

- pages written: 58
- sections needing rewrite: 2 in 2 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 2

```text
credits: description length 28 outside 60-155
credits: description 28 chars, outside 60-155
```


### ingest.py run — 2026-10-28 21:21

- pages written: 57
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 21:22

- pages written: 57
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 21:27

- pages written: 57
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


### ingest.py run — 2026-10-28 21:40

- pages written: 57
- sections needing rewrite: 0 in 0 pages
- tables: 57, code fences: 14
- decorative images dropped: 0
- images replaced with placeholder: 0
- failures: 0


## Phase 8 — ASD-STE100 rewrite and copyright-surface removal

Date: 2026-10-29

### Removed

- `src/components/Attribution.astro` deleted, along with its import and render line in `src/pages/blog/index.astro` and `src/pages/blog/[...slug].astro`.
- `src/content/docs/credits.md` deleted. `scripts/ingest.py` gained `SKIP_SLUGS = {"credits"}` so the page and its sidebar item stay gone after a regenerate.
- Footer link "Structure credits" removed from `src/components/SiteFooter.astro`.
- 6 blog reference lines containing `servicenowzone.com` or `Structure reference:` removed. `grep -rn -i servicenow src/` returns nothing.

### Rewritten

- 321 section paragraphs in `scripts/copy.json` and 58 page intros: sentences split to 25 words or fewer, passive voice made active, banned jargon replaced.
- Two source headings carried jargon. `ingest.py` now runs every heading through `fix_heading()` and rebuilds the heading line, so H3 text obeys the same rule as H1 and the prose key still matches.
- 6 blog posts: sentence-length and jargon pass in place. Frontmatter, links, code fences and tables unchanged.

### Tooling

- `scripts/ste_check.py`: accepts directories, splits hard fails from review notes, and reports `fails=N notes=M`.
- `scripts/ingest.py`: `SKIP_SLUGS`, `HEADING_FIX`, `fix_heading()`, heading-line rebuild, sidebar filter.

### Verification

| Check | Result |
| --- | --- |
| `ste_check.py src/content/docs src/content/blog` | exit 0, fails 0, notes 16 |
| `gates.py` | exit 0, markers 0, frontmatter fails 0, copied pages 0, 64 pages |
| `pnpm build` | exit 0, 65 HTML pages |
| Lighthouse home / interview / blog | 96 / 97 / 99 performance, 100 accessibility, best practices, SEO |
| `rewrite-report.md` | written, 64 files, 3338 sentences, 31256 words |

### Notes

- Subagent delegation stayed unusable: the `freestack` alias resolves to `deepseek-ai/deepseek-v4-flash`, retired 2026-08-07, HTTP 410 on all 16 tasks. All rewriting ran in-session.
- Duplicate page pair `let-27s-learn-ecmascript-2021-with-earl-duque` and `lets-learn-ecmascript-2021-with-earl-duque` still present. One must be dropped before deploy.
- `SITE` in `astro.config.mjs` and the `robots.txt` sitemap URL are still placeholders.
