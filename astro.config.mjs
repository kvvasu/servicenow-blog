// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import sidebar from './src/data/sidebar.json' with { type: 'json' };
import { remarkContentBlocks } from './src/lib/remark-content-blocks.mjs';

const SITE = 'https://servicenow-notes.example';

// A wide table on a 320px screen must scroll, but a scroll box needs a keyboard
// entry point. Wrap every table at build time so the wrapper can take focus.
function rehypeScrollableTables() {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.map((child) => {
        if (child.tagName === 'table') {
          return {
            type: 'element',
            tagName: 'div',
            properties: {
              className: ['table-scroll'],
              tabIndex: 0,
              role: 'region',
              'aria-label': 'Table, scrollable',
            },
            children: [child],
          };
        }
        walk(child);
        return child;
      });
    };
    walk(tree);
  };
}

export default defineConfig({
  site: SITE,
  markdown: {
    remarkPlugins: [remarkContentBlocks],
    rehypePlugins: [rehypeScrollableTables],
  },
  integrations: [
    starlight({
      title: 'ServiceNow Notes',
      description:
        'Original notes on the ServiceNow platform: architecture, scripting, ITSM operations, review checklists and interview preparation.',
      customCss: ['./src/styles/custom.css'],
      // Redis-Docs-style multi-column footer. Pagination still renders inside it.
      components: { Footer: './src/components/SiteFooter.astro' },
      // Manual sidebar. Autogenerate would flatten 59 pages into one column,
      // which is the source site's worst habit.
      sidebar: /** @type {any} */ (sidebar),
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      head: [
        { tag: 'meta', attrs: { property: 'og:image', content: `${SITE}/og.png` } },
        { tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
        { tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
        { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
        { tag: 'meta', attrs: { name: 'twitter:image', content: `${SITE}/og.png` } },
      ],
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/kvvasu' }],
      pagination: true,
      lastUpdated: false,
    }),
    sitemap({
      filter: (page) => !page.includes('/blog/tags/'),
    }),
  ],
});