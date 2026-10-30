# ServiceNow Notes

Notes site on the ServiceNow platform: architecture, scripting, ITSM operations,
review checklists and interview preparation. Built with Astro + Starlight.

## Commands

```
pnpm install
pnpm dev                    # dev server at localhost:4321
pnpm build                  # production build to dist/
pnpm preview                # serve dist/
pnpm explainer [slug]       # render src/explainers/<slug>.md -> public/explainers/<slug>.html
```

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
