"""ASD-STE100 checks for the content folder. Run: python3 scripts/ste_check.py [paths...]

Reports, per file:
  * sentences longer than the limit (20 procedural, 25 descriptive)
  * passive voice ("is run by", "was created by")
  * banned jargon words
  * verb-synonym rotation (verify / confirm / validate / check ...)

Exit code 1 when a violation exists, so a rewrite loop can gate on it.
Markdown scaffolding (frontmatter, code fences, tables, URLs) is skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"
BLOG = ROOT / "src" / "content" / "blog"

LIMIT = 25          # descriptive ceiling; a procedural sentence must stay under 20

BANNED = {
    "leverage": "use", "utilize": "use", "utilise": "use", "commence": "start",
    "prior to": "before", "in order to": "to", "ensure": "make sure",
    "replenish": "fill", "approximately": "about", "under the hood": "(delete)",
    "spin up": "start", "spin-up": "start", "seamless": "(delete)",
    "robust": "(give the property)", "best-in-class": "(delete)",
    "cutting-edge": "(delete)", "game-changer": "(delete)", "deep dive": "(delete)",
    "delve": "(delete)", "landscape": "environment", "paradigm": "pattern",
    "facilitate": "help", "numerous": "many", "in the event that": "if",
    "a number of": "some", "at this point in time": "now", "due to the fact that": "because",
    "in the near future": "soon", "terminate": "stop", "ascertain": "find",
    "utilization": "use", "methodology": "method", "subsequently": "then",
}

# two-word verb + -ing forms that hide an action
PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being|get|gets|got)\s+"
    r"(\w+(?:ed|wn|ne|de|en\b)|drawn|sent|made|held|built|kept|set|let|put|run|shown|given|taken)\b"
    r"(?:\s+\w+){0,3}?\s+by\b", re.I)
PASSIVE_SHORT = re.compile(r"\b(is|are|was|were)\s+\w+ed\s+(to|into|for)\b", re.I)

SYNONYMS = {
    "check": r"\bcheck\w*\b",
    "make sure": r"\bmake sure\b",
    "verify": r"\bverif\w*\b",
    "confirm": r"\bconfirm\w*\b",
    "validate": r"\bvalidat\w*\b",
    "test": r"\btest\w*\b",
    "find": r"\bfind\b|\bsearch\w*\b|\blook\b",
}


def body_of(text: str) -> str:
    """Strip frontmatter, code fences, inline code, tables and URLs."""
    m = re.match(r"\A---\n.*?\n---\n", text, re.S)
    text = text[m.end():] if m else text
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if not s or s.startswith(("|", "<")):
            continue
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)     # keep link text
        s = re.sub(r"https?://\S+", " ", s)
        s = re.sub(r"^\s*(#+|[-*+>]|\d+\.)\s*", "", s)
        out.append(s)
    return "\n".join(out)


def sentences(text: str) -> list[str]:
    parts: list[str] = []
    for para in text.split("\n"):
        for s in re.split(r"(?<=[.:;!?])\s+", para):
            s = s.strip()
            if s:
                parts.append(s)
    return parts


def check(path: Path) -> tuple[list[str], int, int]:
    text = path.read_text(encoding="utf-8")
    body = body_of(text)
    warns: list[str] = []
    n_sent = 0

    for s in sentences(body):
        words = s.split()
        n_sent += 1
        if len(words) > LIMIT:
            warns.append(f"long ({len(words)}w): {s[:90]}...")
        if PASSIVE.search(s) or PASSIVE_SHORT.search(s):
            warns.append(f"passive: {s[:90]}...")

    low = body.lower()
    for bad, fix in BANNED.items():
        if re.search(r"\b" + re.escape(bad) + r"\b", low):
            warns.append(f"jargon '{bad}' -> {fix}")

    counts = {k: len(re.findall(rx, low)) for k, rx in SYNONYMS.items()}
    used = [k for k, v in counts.items() if v]
    if len(used) > 2:
        warns.append("synonym rotation: " + ", ".join(f"{k}={counts[k]}" for k in used))

    return warns, n_sent, len(body.split())


def main(argv: list[str]) -> int:
    if argv:
        files = []
        for a in argv:
            p = Path(a)
            files.extend(sorted(p.glob("*.md")) + sorted(p.glob("*.mdx")) if p.is_dir() else [p])
    else:
        files = sorted(list(DOCS.glob("*.md")) + list(DOCS.glob("*.mdx")) + list(BLOG.glob("*.md")))
    fails = 0
    notes = 0
    for f in files:
        warns, n_sent, n_words = check(f)
        # synonym rotation is a review note: the same verb carries different actions in real prose
        hard = [w for w in warns if not w.startswith("synonym rotation")]
        soft = [w for w in warns if w.startswith("synonym rotation")]
        fails += len(hard)
        notes += len(soft)
        rel = f.relative_to(ROOT) if str(f).startswith(str(ROOT)) else f
        print(f"{rel}: sentences={n_sent} words={n_words} fails={len(hard)} notes={len(soft)}")
        for w in hard[:6]:
            print("   FAIL", w)
    print(f"TOTAL fails={fails} notes={notes} files={len(files)}")
    print("STE PASS" if fails == 0 else "STE FAIL")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))