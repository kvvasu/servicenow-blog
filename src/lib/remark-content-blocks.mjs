// Content components for prose pages: fenced ```filetree blocks become a
// static nested file tree. Kept markdown-only on purpose - the ingest pipeline
// writes plain .md and gates.py parses plain markdown, so directives/MDX would
// fight both.
const esc = (s) =>
  String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const buildTree = (lines) => {
  const nodes = [];
  const roots = [];
  for (const raw of lines) {
    let parent = nodes.length ? nodes[nodes.length - 1] : null;
    if (parent && parent.indent >= raw.indent) {
      while (nodes.length && nodes[nodes.length - 1].indent >= raw.indent) nodes.pop();
      parent = nodes.length ? nodes[nodes.length - 1] : null;
    }
    const node = { indent: raw.indent, name: raw.name, children: [] };
    if (parent) parent.children.push(node);
    else roots.push(node);
    nodes.push(node);
  }
  return roots;
};

const renderNode = (node, isRoot) => {
  const folder = node.name.endsWith('/');
  const label = esc(folder ? node.name.slice(0, -1) : node.name);
  if (!folder) return `<div class="snz-tree-file">${label}</div>`;
  const attrs = isRoot ? ' open' : '';
  const inner = node.children.length
    ? `<div class="snz-tree-children">${node.children.map((c) => renderNode(c, false)).join('')}</div>`
    : '';
  return `<details class="snz-tree"${attrs}><summary class="snz-tree-folder">${label}</summary>${inner}</details>`;
};

export function remarkContentBlocks() {
  const visit = (node) => {
    if (Array.isArray(node.children)) node.children.forEach(visit);
    if (!node || typeof node !== 'object' || node.type !== 'code') return;
    const lang = String(node.lang ?? '').split(/\s+/)[0];
    if (lang !== 'filetree') return;
    const title = /title=["']?([^"'\n]+)["']?/.exec(String(node.meta ?? ''))?.[1] ?? 'File structure';
    const lines = String(node.value ?? '')
      .split('\n')
      .map((l) => ({
        indent: (l.match(/^ */)?.[0] ?? '').replace(/\t/g, '  ').length,
        name: l.trim(),
      }))
      .filter((l) => l.name.length > 0);
    const html = `<div class="snz-tree" data-title="${esc(title)}">${buildTree(lines).map((r) => renderNode(r, true)).join('')}</div>`;
    node.type = 'html';
    node.value = html;
    delete node.lang;
    delete node.meta;
  };
  return (tree) => visit(tree);
}
