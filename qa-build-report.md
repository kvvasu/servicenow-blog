# QA build report — servicenow-blog

Run date: 2026-10-28
Build under test: `pnpm build` → 67 pages in 16.4 s, served from `dist/` on
`http://localhost:4322` (production preview, not the dev server).
Everything below is measured, not estimated.

## Gate summary

| Phase | Gate | Status | Evidence |
| --- | --- | --- | --- |
| 0 Scaffold | dev server 200 | PASS | `curl /` → 200, `curl /docs` → 200 on port 4321 |
| 1 Config | sidebar groups render | PASS | 9 groups, 59 items, all labels present in `dist/servicenow-architecture/index.html` |
| 2 Ingestion | every page valid frontmatter | PASS | 58 docs validated: title + description (89–155 chars) + slug + draft + TOC |
| 3 Blog | index lists ≥5 posts | PASS | 6 posts at `/blog/<slug>/`, index lists all 6 with date, description, tags |
| 4 Robustness | build exits 0 after each phase | PASS | 8 hardening patches, every write through `safe_write`, `validate_page` fails the ingest |
| 5 QA | all checks pass or logged | PASS with logged warnings | see below |

## Mobile-first

Measured with Chrome DevTools device metrics at 320 / 375 / 768 / 1024 / 1440 px
on `/`, `/servicenow-business-rules/`, `/blog/`.

- Horizontal scroll: **0 px delta at every width on every page tested.**
- Sidebar: hidden below 1024 (hamburger present at 320/375/768), visible at 1024 and 1440.
- Right-hand "On this page" TOC: visible at 1440. Below 1152 Starlight hides it by
  design, so it is absent at 1024. Left as is — overriding that breakpoint would
  fight the shell the brief says not to override.
- Content column at 320 px: full width, 320 px usable, no clipping.
- Tap targets: every link that stands alone is ≥24 px tall. The only remaining
  sub-24 px targets are links inside sentences ("Read it", "servicenowzone.com"),
  which WCAG 2.2 AA 2.5.8 exempts as inline text.

Fixed during QA: LinkCard anchors were 22 px tall (now 44 px), list-only links were
19 px (now 24 px), bare YouTube URLs had no usable link text (now "YouTube video
<id>"), and wide tables had a scroll box no keyboard user could reach.

## Lighthouse mobile

Production build, mobile emulation, 3 runs of the shipped output:

| Page | Performance | Accessibility | Best Practices | SEO |
| --- | --- | --- | --- | --- |
| `/` | 100 | 100 | 100 | 100 |
| `/servicenow-architecture/` | 100 | 100 | 100 | 100 |
| `/blog/empty-array-truthiness/` | 100 | 100 | 100 | 100 |

Metrics: LCP 0.8–1.2 s, FCP 0.8–1.0 s, TBT 0 ms, CLS 0.

## Accessibility (WCAG 2.2 AA)

axe-core 4.10.3, tags `wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa`, 5 pages × light
and dark theme = 10 runs.

- **Violations: 0.**
- Contrast: no `color-contrast` failures in either theme. Starlight's default dark
  palette passed; no colour override was needed. Brand accent kept at hsl(212 78% 34%)
  light / hsl(212 88% 46%) dark, both above 4.5:1 on their backgrounds.
- Keyboard: skip link is the first tab stop; 7 consecutive Tabs follow visual order
  (header → sidebar → main → TOC). No focus traps.
- Headings: exactly one `<h1>` per page on all 66 pages. Body-level source H1s are
  demoted to `<h2>` during ingest so no page can gain a second one.
- Images: 107 scraped image refs, 82 with generic "External link" alt dropped; every
  kept image points at `/img/placeholder.svg` with a real alt. No hotlinking.
- Links: no "click here"; raw URLs rewritten to labelled links.
- Forms: none on the site.

Fixed during QA: `scrollable-region-focusable` (table scroll box), focus outline
width, touch target sizes, raw-URL link text.

## SEO

- `site` set in `astro.config.mjs` → canonical + `og:url` on every page.
- Sitemap: **66 URLs** (`dist/sitemap-0.xml`), announced by `public/robots.txt`.
- Duplicate titles: **0**. Duplicate descriptions: **0**.
- Every page: one `<title>`, one `<meta name="description">`, one canonical, one
  `og:title`, one `og:description`, one `og:image`, one `twitter:image`.
- Descriptions: 89–155 chars, all original, none copied from the source site meta.
- Structured data: `BlogPosting` JSON-LD on all 6 posts, valid JSON, `datePublished`
  and `headline` present. No JSON-LD elsewhere, so nothing invalid to report.
- `og.png` 1200×630 in `public/`.

## Markdown hygiene

- 14 code fences, all with a language tag, all closed (verified per file).
- 57 GFM tables, 417 rows, all with a separator row; each wrapped at build time by
  `rehypeScrollableTables()` in `div.table-scroll[tabindex=0][role=region]`.
- 82 rowspan/colspan tables from the source were flattened; logged in the ingest report.
- `draft: true` pages are excluded from the collection query, so none reach `dist/`.
- All 58 slugs lowercase and hyphenated, no `.php` remnants.
- Raw HTML: only the JSON-LD script, the attribution component, and the placeholder
  SVG. All accessible.

## Originality check (hard rule)

Method: 8-word shingle comparison of every built page against all 59 scraped
markdown files, run twice.

1. Whole `<main>`: matches exist, all of them table data, link lists, headings and
   code — the facts the brief allows.
2. Paragraphs only (tables, lists, code, headings stripped): **0 pages with a
   20-word-or-longer verbatim run.**

Also removed: a leaked pull-quote plus its "~Earl Nightingale" attribution line.

## Unresolved warnings

1. `prose/flagged-for-rewrite.json` was never produced by the scrape, so the ingest
   generates it: **266 sections across 44 of 58 pages** still need authored prose.
   They carry `<!-- PROSE-REWRITE-REQUIRED: ... -->` comments in the HTML source and
   no visible banner. Each has a heading, and where the source had them, tables,
   code and link lists. The 6 blog posts are complete.
2. `topic_tags` is absent from all 59 scraped JSON records, so the 9 sidebar groups
   come from title clustering. Mapping is in `src/data/sidebar.json`.
3. Right-hand TOC is absent at exactly 1024 px (Starlight's 1152 px breakpoint).
4. `let-27s-learn-ecmascript-2021-with-earl-duque` and
   `lets-learn-ecmascript-2021-with-earl-duque` are byte-identical in the source.
   Both are kept with distinct titles and descriptions; one could be dropped.
5. 7 broken and 8 unreachable/blocked citations are recorded in the scrape's
   `citations.csv`; the built pages do not link to them.
6. Lighthouse numbers are from a local preview. A CDN or a slow mobile network will
   move Performance; Accessibility, Best Practices and SEO should hold.

## Build and output

```
cd /mnt/d/kvvas/servicenow-blog
pnpm build          # 67 pages, ~16 s, exit 0
pnpm preview --port 4322
```

Deploy-ready output: **`/mnt/d/kvvas/servicenow-blog/dist/`** (4.5 MB, static).
Note: `dist/sitemap-0.xml` and every canonical URL use the placeholder domain
`https://servicenow-notes.example`. Replace `SITE` in `astro.config.mjs` before
deploying for real.
## Post-reskin and post-prose re-verification (2026-10-28)

The gate table above was measured before the reskin and before the prose pass.
These are the numbers that hold now.

| Gate | Result |
| --- | --- |
| Rewrite markers left in `src/content/docs` | 0 (was 266) |
| `flagged-for-rewrite.json` pending pages | 0 |
| Pages with a shared 10-gram against the scrape | 0 |
| Pages with exactly one `<h1>` | 66 of 66 |
| Duplicate `<title>` values | 0 |
| Frontmatter field failures | 0 |
| Build | 67 pages, 20.24 s, exit 0 |
| Lighthouse mobile, Q&A page | 100 / 100 / 100 / 100 |
| Lighthouse mobile, outage page | 94 then 99 on rerun (TBT variance) |
| Lighthouse mobile, home / doc / post (reskin build) | 100 / 100 / 100 / 100 |
| Horizontal scroll, 4 pages x 5 widths | none |

### Notes

- The prose pass added 321 section paragraphs. `scripts/gates.py` compares page
  paragraphs against the scraped markdown at 10-gram granularity and skips link
  lists, tables and code, so shared facts do not count as copying.
- The outage page scored 94 once and 99 on a rerun with the same build. Total
  blocking time moved from 290 ms to 130 ms with no code change, so treat the
  single 94 as measurement noise.
- Three link-only pages (`learn-servicenow-development-in-9-hours`,
  `servicenow-business-rules`, `servicenow-client-scripts`) carry no H2 headings.
  They are curated link lists, so the gate reports a warning instead of a failure.
