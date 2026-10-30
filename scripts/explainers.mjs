#!/usr/bin/env node
/**
 * Render the visual explainers under src/explainers/ into public/explainers/.
 *
 * The explainer tool writes a complete standalone page. This script adds the
 * metadata the blog needs (canonical, description, Open Graph, noindex) and
 * hides the tool's reader-reply widgets, which do not belong on a public post.
 *
 * Usage:
 *   node scripts/explainers.mjs            # every draft
 *   node scripts/explainers.mjs <slug>     # one draft
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, basename } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const DRAFTS = join(ROOT, 'src/explainers');
const OUT = join(ROOT, 'public/explainers');
const AM = join(ROOT, 'node_modules/answer-me-with-html/skills/answer-me-with-html/scripts/am.mjs');

const site = readFileSync(join(ROOT, 'astro.config.mjs'), 'utf8')
  .match(/const SITE = '([^']+)'/)?.[1]
  ?.replace(/\/?$/, '/');
if (!site) throw new Error('SITE not found in astro.config.mjs');

const frontmatter = (text) => text.match(/^---\n([\s\S]*?)\n---/)?.[1] ?? '';
const field = (text, key) =>
  frontmatter(text).match(new RegExp(`^${key}:\\s*"?(.*?)"?\\s*$`, 'm'))?.[1];

const only = process.argv[2];
const drafts = readdirSync(DRAFTS)
  .filter((f) => f.endsWith('.md') && !f.endsWith('.post.md'))
  .map((f) => basename(f, '.md'))
  .filter((slug) => !only || slug === only);

mkdirSync(OUT, { recursive: true });

for (const slug of drafts) {
  const out = join(OUT, `${slug}.html`);

  execFileSync(process.execPath, [
    AM, 'render', join(DRAFTS, `${slug}.md`),
    '-o', out, '--no-open', '--style', 'strict',
  ], { stdio: 'inherit' });

  const post = readFileSync(join(ROOT, `src/content/blog/${slug}.md`), 'utf8');
  const description = field(post, 'description');
  const title = field(post, 'title') ?? field(readFileSync(join(DRAFTS, `${slug}.md`), 'utf8'), 'title');
  const url = `${site}blog/${slug}/`;

  const head = [
    `<meta name="description" content="${description}">`,
    `<meta name="robots" content="noindex,follow">`,
    `<link rel="canonical" href="${url}">`,
    `<meta property="og:type" content="article">`,
    `<meta property="og:title" content="${title}">`,
    `<meta property="og:description" content="${description}">`,
    `<meta property="og:url" content="${url}">`,
    `<meta property="og:image" content="${site}og.png">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<style>.am-btn--reply,.am-btn--remark,.am-comment-btn,.am-comment,.am-reply,.am-reply-bar,.am-feedback,.am-colophon,[data-am="copy"]{display:none!important}</style>`,
  ].join('\n');

  const html = readFileSync(out, 'utf8').replace('</head>', `${head}\n</head>`);
  writeFileSync(out, html);

  console.log(`✓ ${slug}.html  ${(Buffer.byteLength(html) / 1024).toFixed(0)} KB  → ${url}`);
}
