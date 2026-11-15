# ServiceNow Notes

Notes site on the ServiceNow platform: architecture, scripting, ITSM operations,
review checklists and interview preparation. Built with Astro + Starlight.

**Live:** https://servicenow-blog.waasu02.workers.dev
**Repo:** https://github.com/kvvasu/servicenow-blog

## Commands

```
pnpm install
pnpm dev                    # dev server at localhost:4321
pnpm build                  # production build to dist/
pnpm preview                # serve dist/
pnpm explainer [slug]       # render src/explainers/<slug>.md -> public/explainers/<slug>.html
pnpm deploy                 # build output -> Cloudflare Worker (wrangler.jsonc)
```

Deploy: `pnpm build && pnpm deploy`. The worker is `servicenow-blog`; its
static assets come from `dist/` as declared in `wrangler.jsonc`.

Content checks (run before every commit):

```
python3 scripts/ingest.py                                            # regenerate docs from the scrape
python3 scripts/ste_check.py src/content/docs src/content/blog       # ASD-STE100 writing gate
python3 scripts/gates.py                                             # copied-phrase / frontmatter / heading gates
```

## Structure

```
src/content/docs/          57 ingested note pages (starlight docs collection)
src/content/blog/          original blog posts (blog collection)
src/data/sidebar.json      manual sidebar: 9 groups, ~57 entries
src/lib/                   remark plugins (content components)
src/styles/custom.css      skin: tokens, light/dark, component styles
scripts/ingest.py          scrape -> docs tree; authored prose in scripts/copy.json
scripts/ste_check.py       sentence-length / jargon / passive-voice gate
scripts/gates.py           copy-plagiarism, frontmatter and heading gates
src/explainers/            visual explainer drafts (answer-me-with-html)
public/                    favicon, og image, robots.txt
```

## Visual system

The skin is a highlighter-on-paper system:

- **Canvas** warm cream `#ede7e2`, **surfaces** paper `#ffffff`, **ink** `#171717`.
- **Lime** `#f5ff7d` is a surface colour only — the hero band and link hovers.
  It never fills a button, a border or a word.
- **Type** Poppins 600 uppercase for headings (29-37px, 1.2 line-height),
  Montserrat 400 at 17px / 1.5 for body. Both self-hosted via Fontsource.
- **Shape** 25px card radius, 20px image/table/code radius, 100px pills,
  1px ink borders. No shadows; hover paints a 2px outline instead.
- Dark mode keeps the same structure on an ink canvas.

Tokens live in `src/styles/custom.css` as `--rp-*` (palette and semantics) and
are mapped once onto Starlight's `--sl-color-*` hooks.

## Content components

Fenced blocks in the docs collection render as structured content:

````markdown
```filetree title="Scoped app artifacts"
leave-management/
  tables/x_leave_request
  business-rules/check-balance.js
```
````

`src/lib/remark-content-blocks.mjs` turns the fence into a nested,
JS-free `<details>` file tree. Unknown language or bad input falls back to an
ordinary code block. Pages that carry hand-written blocks are listed in
`HAND_EDITED` inside `scripts/ingest.py` so a re-ingest does not wipe them.

## Explainers (experimental)

`src/explainers/*.md` are drafts for the
[answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) renderer.
`pnpm explainer <slug>` writes `public/explainers/<slug>.html` and injects the
blog canonical / description / OG tags. Nothing is linked from the site yet.

## Conventions

- Every page name is plain English (ASD-STE100); the STE gate must stay green.
- Sidebar is manual — autogenerate would flatten 57 pages into one column.
- Tables are wrapped by `rehypeScrollableTables` at build time so they scroll
  inside a keyboard-reachable box.
