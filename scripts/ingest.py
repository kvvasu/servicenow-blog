#!/usr/bin/env python3
"""Ingest the servicenowzone.com scrape into a Starlight docs tree.

Reads  : /mnt/d/kvvas/servicenowzone-scrape/{json,md}
Writes : src/content/docs/*.md, src/data/sidebar.json,
         prose/flagged-for-rewrite.json, blog/topic-backlog.md
Copy   : scripts/copy.json  (the ONLY source of prose in the output)

Copyright rule enforced here, not by reviewer goodwill:
  KEEP   = heading skeleton, code fences, GFM tables, short link-bearing list
           items (name + URL is a fact), dates, and table data.
  REPLACE = every prose paragraph, long list item, checklist line and Q&A
           answer. Authored copy where copy.json supplies it, otherwise one
           rewrite marker per section.

Drops <img> tags whose alt text is the scrape's generic "External link"
(107 refs, 82 of them meaningless) and logs each one.
"""
from __future__ import annotations

import html
import json
import re
from collections import Counter
import sys
from pathlib import Path

SRC = Path("/mnt/d/kvvas/servicenowzone-scrape")
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
DOCS = PROJ / "src" / "content" / "docs"
DATA = PROJ / "src" / "data"
PROSE = PROJ / "prose"
BLOG = PROJ / "blog"

FAILS: list[str] = []

# ---------------------------------------------------------------- groups
# Derived from title clusters: the scrape carries no topic_tags field.
GROUPS: list[tuple[str, list[str]]] = [
    ("Get Started", [
        "servicenow-architecture",
        "servicenow-developer-onboarding-kit",
        "learn-javascript-and-servicenow-roadmap",
        "learn-modern-javascript-and-servicenow-roadmap",
        "servicenow-training",
        "learn-servicenow-development-in-9-hours",
        "servicenow-knowledge-base",
        "servicenow-expert-blogs",
    ]),
    ("Development", [
        "servicenow-client-scripts",
        "servicenow-business-rules",
        "servicenow-glide-query-examples",
        "servicenow-server-side-vs-client-side-javascript-truthiness-for-arrays-and-objects-across-es12-mode-and-legacy-modes",
        "how-to-debug-like-programming-language-creators-and-apply-their-thinking-to-the-servicenow-platform",
        "how-is-script-tracer-different-from-script-debugger",
        "javascript-exercises-with-solutions",
        "servicenow-application-development",
        "servicenow-application-development-leave-management-system",
        "servicenow-generative-ai",
        "servicenow-production-grade-prompt-ideas",
    ]),
    ("ITSM & Platform", [
        "tips-for-servicenow-admins",
        "servicenow-tips-and-tricks",
        "core-servicenow-tables-categorized-by-module",
        "a-detailed-analysis-of-servicenow-production-instance-outages",
        "servicenow-discovery-training",
        "servicenow-aws-cloud-discovery",
        "servicenow-flow-designer-training",
        "servicenow-system-administration-training",
        "servicenow-developer-training",
        "servicenow-itsm-implementation-mock-training",
    ]),
    ("Reviews & Checklists", [
        "checklist-for-architecture-design-reviews",
        "checklist-for-code-reviews",
        "checklist-for-detailed-design-reviews",
        "checklist-for-high-level-design-reviews",
        "checklist-for-project-plan-reviews",
        "checklist-for-requirements-reviews",
        "checklist-for-test-plan-reviews",
    ]),
    ("Interviews & Career", [
        "servicenow-integration-interview-questions-with-answers",
        "servicenow-interview-questions-and-answers-on-handling-failures-in-integrations",
        "scenario-based-interview-questions-in-servicenow",
        "teacher-trainer-coach-mentor",
    ]),
    ("Releases & AI Platform", [
        "a-history-of-servicenow-releases-from-workflow-to-ai",
        "servicenow-ai-platform-technology-stack",
        "zing-vs-ai-search-in-servicenow",
    ]),
    ("Talks & Episodes", [
        "learn-javascript-on-the-now-platform-with-chuck-tomasi",
        "learn-integrations-on-the-now-platform-with-chuck-tomasi",
        "learn-graphql-on-the-servicenow-platform-with-chuck-tomasi",
        "learn-how-to-create-servicenow-builder-app-with-chuck-tomasi",
        "let-27s-learn-ecmascript-2021-with-earl-duque",
        "lets-learn-ecmascript-2021-with-earl-duque",
        "learn-more-javascript-on-the-servicenow-platform-with-earl-duque",
        "goran-lundqvist-servicenow-episodes",
    ]),
    ("References", [
        "servicenow-books",
        "javascript-books",
        "java-books",
        "hand-picked-collection-of-top-java-resources",
        "credits",
        "disclaimer",
        "dedication",
    ]),
]

GROUP_OF = {s: g for g, items in GROUPS for s in items}
LABEL_OVERRIDE = {
    "let-27s-learn-ecmascript-2021-with-earl-duque": "Let's Learn ECMAScript 2021 with Earl Duque",
    "lets-learn-ecmascript-2021-with-earl-duque": "ECMAScript 2021 with Earl Duque — Session Repost",
}

# ---------------------------------------------------------------- helpers
QUOTE_ATTR = re.compile(r"^[^\n]{0,220}?[.\u201d\"']\s*[-\u2013\u2014]\s*[A-Z][\w .'\u2019-]{2,40}$", re.M)
# "~Earl Nightingale" and "— somebody" are attribution lines for a pull-quote. They
# are someone else's words, so they never belong in the output.
ATTRIB_LINE = re.compile(r"^\s*[~\u2014\u2013-]\s*[A-Z][\w .'\u2019-]{2,40}$")
EMBED = re.compile(r"\[embedded video: (https?://[^\]]+)\]")
FENCE_OPEN = re.compile(r"^```(\w*)\s*$")
HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
TABLE_ROW = re.compile(r"^\|.*\|\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\S")
LINK_IN = re.compile(r"\[[^\]]+\]\([^)\s]+\)")
# "Watch this" or a raw https:// line is not link text a screen reader can use.
# YouTube gets a stable, distinct label; anything else gets its host.
BARE_URL_LINE = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)?(https?://\S+)\s*$")
YT_ID = re.compile(r"(?:youtu\.be/|v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})")
URL_AS_TEXT = re.compile(r"\[(https?://[^\]\s]+)\]\((https?://[^)\s]+)\)")


def humanize_links(text: str) -> str:
    """Give a bare-URL line real link text. Keeps the URL as the href."""
    def label_for(url: str) -> str:
        yt = YT_ID.search(url)
        if "youtube.com" in url or "youtu.be" in url:
            return f"YouTube video {yt.group(1)}" if yt else "YouTube video"
        return url.split("//", 1)[-1].split("/", 1)[0].removeprefix("www.")

    def repl(m: re.Match) -> str:
        bullet = m.group(1) or ""
        url = m.group(2)
        return f"{bullet}[{label_for(url)}]({url})"

    # A markdown link whose visible text is the URL itself reads as "https://..."
    # to a screen reader, so give it a label too.
    text = URL_AS_TEXT.sub(lambda m: f"[{label_for(m.group(2))}]({m.group(2)})", text)
    return "\n".join(BARE_URL_LINE.sub(repl, l) for l in text.split("\n"))
IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BOXART = re.compile(r"[─│┌┐└┘├┤┬┴┼━┃╔╗╚╝║═]")


def fence_lang(body: str) -> str:
    """The scrape emitted 14 fences, none with a language identifier."""
    if re.search(r"^\s*(flowchart|graph|sequenceDiagram|gantt|stateDiagram)", body, re.M):
        return "mermaid"
    if BOXART.search(body):
        return "text"
    if re.search(r"(Class\.create\(\)|function\s+\w+\(|var\s+\w+\s*=|=>|GlideAjax|GlideRecord)", body):
        return "javascript"
    if re.search(r"\b(SELECT|INSERT|UPDATE)\b", body, re.I):
        return "sql"
    return "text"


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            return md[end + 4:].lstrip("\n")
    return md


def src_title(slug: str, md: str) -> str:
    m = re.search(r"^title:\s*(.+)$", md, re.M)
    return html.unescape(m.group(1).strip()) if m else slug.replace("-", " ").title()


def sanitize_images(text: str, slug: str) -> tuple[str, list[str], list[str]]:
    """Drop decorative link thumbnails; replace kept images with a local placeholder.

    No source image is archived locally, so a kept image can only be served by
    hotlinking somebody else's file. Instead every kept image becomes a neutral
    SVG placeholder, and the original path is logged.
    """
    dropped, kept = [], []

    def repl(m: re.Match) -> str:
        alt, src = m.group(1).strip(), m.group(2)
        if not alt or "external link" in alt.lower():
            dropped.append(src)
            return ""
        kept.append(src)
        return f"![{alt}](/img/placeholder.svg)"

    text = IMG.sub(repl, text)
    def _vid(m):
        vid = m.group(1).rstrip("/").split("/")[-1]
        return f"[Watch on YouTube](https://www.youtube.com/watch?v={vid})"
    text = EMBED.sub(_vid, text)
    return text, dropped, kept


SKIP_SLUGS = {"credits"}
HAND_EDITED = {"servicenow-application-development-leave-management-system"}

# Source headings that carry jargon. The rewrite targets the label, not the prose,
# so the authored section key uses the fixed form and this map keeps them aligned.
HEADING_FIX = [
    ("How can you ensure data is not duplicated during integration?",
     "How can you prevent duplicate data during integration?"),
    ("a robust \u201ccontract-first\u201d pattern", "a \u201ccontract-first\u201d pattern"),
]


def fix_heading(head: str) -> str:
    for old, new in HEADING_FIX:
        if old in head:
            head = head.replace(old, new)
    return head


def transform(slug: str, body: str, copy: dict, boiler: set[str] = frozenset(),
              sections: dict | None = None) -> tuple[str, dict]:
    """Heading skeleton + fences + tables + fact lists; prose replaced.

    boiler: heading labels that appear on many source pages. Those are the source
    site's own navigation and advertising, not content, so they are dropped whole.
    """
    sections = sections or copy.get("sections", {})
    # Section prose can be addressed per page as "<heading>::<occurrence>". A bare
    # heading key still resolves, so the older entries keep working. The page scope
    # matters because several pages use headings like "Introduction" or "Overview".
    page_sections = {
        key.split("::", 1)[1]: val
        for key, val in sections.items()
        if key.startswith(slug + "::")
    }
    cur_prose = None                   # authored paragraph for cur_head, if any
    head_seen: dict[str, int] = {}      # how often each heading appeared so far
    out: list[str] = []
    pending: list[str] = []            # buffered prose awaiting a decision
    cur_head = ""
    todos: list[str] = []              # headings left with a rewrite marker
    marked: set[str] = set()           # headings already given a marker
    emitted: set[str] = set()          # headings whose authored prose is in play
    seen_heading = False               # has any heading been written yet?
    in_title = False                   # inside the page-title (H1) section
    skip = False                       # inside a boilerplate section
    stat = {"headings": 0, "tables": 0, "fences": 0, "kept_lists": 0,
            "dropped_prose": 0, "images_dropped": 0}

    def flush():
        """Emit authored prose for the current heading, else one marker."""
        nonlocal pending
        if not pending:
            return
        text = "\n".join(pending).strip()
        pending = []
        if not text:
            return
        stat["dropped_prose"] += 1
        if cur_head in emitted:                # this heading's prose is already in place
            return
        if QUOTE_ATTR.match(text):             # a pull-quote plus its attribution
            return
        # Fragment-only block (a date, a name, a short label): no sentence to
        # rewrite, so keep it as a fact and skip the marker. A short line followed
        # by "~Name" is somebody else's quotation, so drop the pair.
        if not any(len(l.split()) >= 8 for l in text.split("\n")):
            lines_in = text.split("\n")
            kept = []
            for j, l in enumerate(lines_in):
                nxt = lines_in[j + 1] if j + 1 < len(lines_in) else ""
                if ATTRIB_LINE.match(nxt):
                    continue                      # drop the quotation
                if ATTRIB_LINE.match(l):
                    continue                      # drop the attribution
                kept.append(l)
            if kept:
                out.append("\n".join(kept))
                stat["kept_fragments"] = stat.get("kept_fragments", 0) + 1
            return
        prose = cur_prose
        if prose:
            out.append(prose.strip())
            emitted.add(cur_head)
            return
        if not seen_heading or in_title:
            return                            # page preamble
        if cur_head in marked:            # one marker per heading, not per block
            return
        marked.add(cur_head)
        preview = re.sub(r"\s+", " ", re.sub(r"[#*`\[\]]", "", text))[:90]
        todos.append(cur_head or slug)
        # The marker stays in the HTML source so Phase 3 and later passes can find
        # it; it does not render, because 266 visible "pending" boxes would drown
        # the tables and links that are already correct.
        out.append(f"<!-- PROSE-REWRITE-REQUIRED: {preview} -->")

    lines = body.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]

        # fenced code -> keep, with an inferred language tag
        m = FENCE_OPEN.match(ln)
        if m:
            block = [ln]
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append("```")
            flush()
            lang = m.group(1) or fence_lang("\n".join(block[1:-1]))
            block[0] = "```" + lang
            out.append("\n".join(block))
            stat["fences"] += 1
            i += 1
            continue

        if TABLE_ROW.match(ln):                      # GFM table block -> keep
            flush()
            while i < len(lines) and TABLE_ROW.match(lines[i]):
                out.append(lines[i])
                i += 1
            stat["tables"] += 1
            continue

        h = HEADING.match(ln)
        if h:
            flush()
            cur_head = h.group(2).strip()
            skip = cur_head in boiler
            if skip:
                stat["boiler_sections"] = stat.get("boiler_sections", 0) + 1
                i += 1
                continue
            stat["headings"] += 1
            cur_head = fix_heading(cur_head)
            # A second H1 inside the body would give the page two h1 elements. The
            # frontmatter title owns the only H1, so any body H1 becomes an H2.
            # rebuild the heading line so the jargon fix reaches H3+ as well
            out.append(("## " if h.group(1) == "#" else h.group(1) + " ") + cur_head)
            in_title = False
            seen_heading = True
            head_seen[cur_head] = head_seen.get(cur_head, 0) + 1
            cur_prose = (page_sections.get(f"{cur_head}::{head_seen[cur_head]}")
                         or sections.get(cur_head))
            if not in_title and cur_prose and cur_head not in emitted:
                out.append(cur_prose.strip())
                emitted.add(cur_head)
            i += 1
            continue

        if LIST_ITEM.match(ln):                      # list block: facts or prose?
            block = []
            while i < len(lines) and (LIST_ITEM.match(lines[i]) or
                                      (lines[i].startswith(("  ", "\t")) and block)):
                block.append(lines[i])
                i += 1
            joined = "\n".join(block)
            items = [b for b in block if LIST_ITEM.match(b)]
            linked = sum(1 for b in items if LINK_IN.search(b))
            short = all(len(b) <= 140 for b in items)
            if items and short and linked >= max(1, len(items) // 2):
                flush()
                out.append(humanize_links(joined))
                stat["kept_lists"] += 1
            else:
                pending.append(joined)               # treated as prose
            continue

        if not ln.strip():
            if pending:
                flush()
            i += 1
            continue

        pending.append(ln)
        i += 1

    flush()

    text = "\n".join(out)
    text, dropped, kept = sanitize_images(text, slug)
    stat["images_dropped"] = len(dropped)
    stat["images_placeholder"] = len(kept)
    for src in kept:
        FAILS.append(f"{slug}: image not archived locally -> placeholder used ({src})")
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text, {"stats": stat, "todos": todos, "images_dropped": dropped}


def check_desc(slug: str, desc: str) -> str:
    if not (60 <= len(desc) <= 155):
        FAILS.append(f"{slug}: description length {len(desc)} outside 60-155")
    return desc


# ---------------------------------------------------------------- main
def safe_write(path, text: str, what: str) -> bool:
    """Every generated file goes through here, so a failing write is logged, not lost."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return True
    except Exception as exc:                         # noqa: BLE001
        FAILS.append(f"{what}: write failed ({type(exc).__name__}: {exc})")
        return False


def validate_page(path, slug: str) -> bool:
    """Check the written file against the Starlight frontmatter schema.

    Catching this here means an invalid page fails the ingest, not the deploy.
    """
    try:
        head = path.read_text(encoding="utf-8").split("---", 2)[1]
    except Exception as exc:                         # noqa: BLE001
        FAILS.append(f"{slug}: frontmatter unreadable ({type(exc).__name__})")
        return False
    got = {k: v.strip().strip('"') for k, v in
           re.findall(r"^(\w+):\s*(.*)$", head, re.M)}
    missing = [k for k in ("title", "description", "slug", "tableOfContents")
               if not got.get(k)]
    if missing:
        FAILS.append(f"{slug}: frontmatter missing {missing}")
        return False
    n = len(got["description"])
    if not 60 <= n <= 155:
        FAILS.append(f"{slug}: description {n} chars, outside 60-155")
    if got["slug"] != slug or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        FAILS.append(f"{slug}: slug not lowercase-hyphenated, or slug mismatch")
    if got["tableOfContents"] != "true":
        FAILS.append(f"{slug}: tableOfContents is not true (right-hand TOC is required)")
    return True


def appendix_build_log(report: list, flags: dict) -> None:
    """Append this run's outcome to build-log.md so failures survive the terminal."""
    import datetime
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n### ingest.py run — {stamp}", "",
             f"- pages written: {len(report)}",
             f"- sections needing rewrite: {sum(r['todos'] for r in report)} "
             f"in {len(flags)} pages",
             f"- tables: {sum(r['tables'] for r in report)}, "
             f"code fences: {sum(r['fences'] for r in report)}",
             f"- decorative images dropped: "
             f"{sum(r['images_dropped'] for r in report)}",
             f"- images replaced with placeholder: "
             f"{sum(r.get('images_placeholder', 0) for r in report)}",
             f"- failures: {len(FAILS)}", ""]
    if FAILS:
        lines += ["```text", *FAILS, "```", ""]
    try:
        with (PROJ / "build-log.md").open("a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    except Exception as exc:                         # noqa: BLE001
        print(f"  ! build-log.md append failed: {type(exc).__name__}: {exc}")


def main() -> int:
    copy_all = json.loads((HERE / "copy.json").read_text(encoding="utf-8"))
    pages = copy_all["pages"]
    SECTIONS = copy_all.get("sections", {})
    for d in (DOCS, DATA, PROSE, BLOG):
        d.mkdir(parents=True, exist_ok=True)

    # A heading that appears on many source pages is site chrome, not content.
    freq: Counter = Counter()
    for mf in (SRC / "md").glob("*.md"):
        for ln in mf.read_text(encoding="utf-8", errors="replace").split("\n"):
            m = re.match(r"^#{2,6}\s+(.*\S)\s*$", ln)
            if m:
                freq[m.group(1)] += 1
    boiler = {h for h, n in freq.items() if n >= 8}
    print(f"boilerplate_heading_labels={len(boiler)}")

    # index is authored by hand as the splash landing page (src/content/docs/index.mdx),
    # so a re-run must not overwrite it with a converted article body.
    scrape_slugs = sorted(
        p.stem for p in (SRC / "json").glob("*.json")
        if p.stem != "index" and p.stem not in SKIP_SLUGS
    )
    report, flags = [], {}
    missing_copy = [s for s in scrape_slugs if s not in pages]
    if missing_copy:
        print("!! no copy entry for:", missing_copy)

    for slug in scrape_slugs:
        if slug in HAND_EDITED:
            continue  # hand-authored content (e.g. ```filetree blocks) must survive a re-run
        jf, mf = SRC / "json" / f"{slug}.json", SRC / "md" / f"{slug}.md"
        try:
            meta = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as exc:                     # noqa: BLE001
            meta, exc_txt = {}, f"{type(exc).__name__}: {exc}"
            FAILS.append(f"{slug}: json unreadable ({exc_txt})")
            print(f"  ! {slug}: json unreadable -> placeholder page")
        try:
            raw = mf.read_text(encoding="utf-8")
        except Exception as exc:                     # noqa: BLE001
            raw = ""
            FAILS.append(f"{slug}: md unreadable ({type(exc).__name__})")

        cp = pages.get(slug, {})
        if meta:
            title = LABEL_OVERRIDE.get(slug) or cp.get("title") or src_title(slug, raw)
        else:
            # unreadable or empty source record: still publish, but say so on the page
            title = LABEL_OVERRIDE.get(slug) or cp.get("title") or f"Untitled — {slug}"
            FAILS.append(f"{slug}: empty or missing source record -> placeholder page")
        desc = cp.get("description") or f"ServiceNow notes on {slug.replace('-', ' ')}." 
        desc = check_desc(slug, desc)
        body = transform(slug, strip_frontmatter(raw), cp, boiler, SECTIONS)
        assembled = f'---\ntitle: "{title}"\ndescription: "{desc}"\nslug: "{slug}"\ndraft: false\ntableOfContents: true\n---\n\n'
        intro = (cp.get("intro") or "").strip()
        if intro:
            assembled += intro + "\n\n"
        if not meta:
            assembled += (':::danger[Placeholder]\nThis page was ingested from a source record '
                          'that could not be read. Content is a draft.\n:::\n\n')
        assembled += body[0]

        target = DOCS / f"{slug}.md"
        if not safe_write(target, assembled, slug):
            print(f"  ! {slug}: write failed")
            continue
        validate_page(target, slug)

        if body[1]["todos"]:
            flags[slug] = {"title": title, "sections_pending": body[1]["todos"],
                           "source": meta.get("url", "")}
        report.append({"slug": slug, **body[1]["stats"], "todos": len(body[1]["todos"])})

    # sidebar: manual groups, never autogenerate (redis/docs hierarchy)
    sidebar = [{"label": "Overview",
                "items": [{"label": "Home", "link": "/"}]}]
    for label, slugs in GROUPS:
        items = [{"label": LABEL_OVERRIDE.get(s, pages.get(s, {}).get("title")
                                              or s.replace("-", " ")), "slug": s}
                 for s in slugs if s not in SKIP_SLUGS]
        if items:  # a group emptied by SKIP_SLUGS would fail the build
            sidebar.append({"label": label, "items": items})
    safe_write(DATA / "sidebar.json", json.dumps(sidebar, indent=2) + "\n", "sidebar.json")

    safe_write(PROSE / "flagged-for-rewrite.json",
        json.dumps({"generated_from": str(SRC), "pages": flags,
                    "note": ("Sections whose source paragraphs were dropped. Authored prose in "
                             "scripts/copy.json replaces a section; otherwise the page carries a "
                             "PROSE-REWRITE-REQUIRED marker.")}, indent=2) + "\n",
        "flagged-for-rewrite.json")

    # topic backlog for the blog layer
    ranked = sorted(report, key=lambda r: -(r["headings"] + r["tables"] * 2))
    lines = ["# Topic backlog", "",
             "Ranked from the scrape by structural weight (headings + tables).",
             "Each entry is a candidate for an original post; cite the source page and, where",
             "the page only curated someone else's material, cite that primary source instead.",
             ""]
    for r in ranked[:24]:
        t = pages.get(r["slug"], {}).get("title") or r["slug"].replace("-", " ")
        lines.append(f"- **{t}** — `{r['slug']}` — {r['headings']} headings, "
                     f"{r['tables']} tables, {r['fences']} code blocks")
    safe_write(BLOG / "topic-backlog.md", "\n".join(lines) + "\n", "topic-backlog.md")

    # summary
    print(f"pages={len(report)} groups={len(sidebar)}")
    print(f"headings={sum(r['headings'] for r in report)} tables={sum(r['tables'] for r in report)} "
          f"fences={sum(r['fences'] for r in report)} kept_link_lists={sum(r['kept_lists'] for r in report)}")
    print(f"sections_needing_rewrite={sum(r['todos'] for r in report)} "
          f"in {len(flags)} of {len(report)} pages")
    print(f"decorative_images_dropped={sum(r['images_dropped'] for r in report)}")
    print(f"boiler_sections_dropped={sum(r.get('boiler_sections', 0) for r in report)}")
    appendix_build_log(report, flags)
    if FAILS:
        print(f"FAILURES ({len(FAILS)}):")
        for f in FAILS:
            print("  -", f)
    else:
        print("failures: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
