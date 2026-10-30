"""Content gates for the built markdown. Run: python3 scripts/gates.py

Checks, in order:
  1. rewrite markers left in the content
  2. frontmatter sanity (title, description length, slug, draft, tableOfContents)
  3. exactly one H1 per page (frontmatter title; body headings are H2+)
  4. verbatim prose runs shared with the scrape (10-gram, prose lines only)

Exit code 1 if any gate fails, so a build step can refuse to ship.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOCS = ROOT / "src" / "content" / "docs"
BLOG = ROOT / "src" / "content" / "blog"
SRC_MD = Path("/mnt/d/kvvas/servicenowzone-scrape/md")

MARKER = "PROSE-REWRITE-REQUIRED"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
WORD = re.compile(r"[a-z0-9']+")
N = 10          # gram size; prose prose prose, not boilerplate


def prose_text(body: str) -> str:
    """Paragraph lines only. Link lists, tables, code and headings are facts, not prose."""
    body = FENCE.sub(" ", body)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    keep = []
    for line in body.split("\n"):
        s = line.strip()
        if len(s.split()) < 12:                 # fragments and link labels
            continue
        if s.startswith(("#", "|", "-", "*", ">", "!", "[", "+")) or re.match(r"^\d+\.", s):
            continue
        if "http" in s or " | " in s or s.endswith(":"):
            continue
        keep.append(s)
    return "\n".join(keep)


def grams(text: str, n: int = N) -> set[tuple[str, ...]]:
    words = WORD.findall(text.lower())
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def main() -> int:
    fails: list[str] = []
    warn: list[str] = []

    doc_pages = sorted(list(DOCS.glob("*.md")) + list(DOCS.glob("*.mdx")))
    blog_pages = sorted(BLOG.glob("*.md"))
    pages = doc_pages + blog_pages
    if not pages:
        print("no pages found", file=sys.stderr)
        return 1

    markers = 0
    for p in doc_pages:          # blog keeps its own frontmatter shape
        if p.name == "index.mdx":   # hand-authored splash page, no slug/draft by design
            continue
        text = p.read_text(encoding="utf-8")
        markers += text.count(MARKER)
        m = FM.match(text)
        if not m:
            fails.append(f"{p.name}: no frontmatter")
            continue
        fm = m.group(1)
        body = text[m.end():]

        for field in ("title:", "description:", "slug:", "draft:", "tableOfContents:"):
            if field not in fm:
                fails.append(f"{p.name}: frontmatter missing {field}")

        cols = re.findall(r"^#{2,6}\s", body, re.M)
        if re.search(r"^# ", body, re.M):
            fails.append(f"{p.name}: body contains an H1")
        if not cols:
            warn.append(f"{p.name}: no H2+ headings (link-only page)")

    # gather scrape side once
    scrape: set[tuple[str, ...]] = set()
    if SRC_MD.is_dir():
        for f in SRC_MD.glob("*.md"):
            scrape |= grams(prose_text(f.read_text(encoding="utf-8", errors="replace")))
        print(f"scrape 10-grams indexed: {len(scrape)}")
    else:
        print(f"WARNING: scrape folder missing at {SRC_MD}")

    copied = []
    if scrape:
        for p in pages:
            text = p.read_text(encoding="utf-8")
            m = FM.match(text)
            body = text[m.end():] if m else text
            hit = grams(prose_text(body)) & scrape
            if hit:
                copied.append(f"{p.name}: {len(hit)} shared 10-gram(s), first: {' '.join(sorted(hit)[0])}")

    print(f"pages={len(pages)} markers={markers} frontmatter_fails={len(fails)} copied_pages={len(copied)}")
    for f in fails[:20]:
        print("  FAIL", f)
    for w in warn[:10]:
        print("  WARN", w)
    for c in copied[:20]:
        print("  COPY", c)

    ok = markers == 0 and not fails and not copied
    print("GATES PASS" if ok else "GATES FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())