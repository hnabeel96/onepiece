#!/usr/bin/env python3
"""
One Piece theory base builder.

Downloads every chapter page and every SBS page from the One Piece Wiki
(onepiece.fandom.com) via the MediaWiki API, and stores in data/:

  chapters/chapter_0001.md ...   chapter summaries written by wiki editors (CC-BY-SA)
  sbs/sbs_volume_001.md ...      SBS *topic index* only - where each question appears
                                 and which wiki topics it links to; the Q&A text is
                                 Oda's and is not stored
  raw/chapters/*.wiki            chapter wikitext (author comments removed) for re-parsing
  onepiece.db                    SQLite: chapters, sbs_index, FTS5 search index
  ATTRIBUTION.txt

Usage:
    python3 scripts/op_scrape.py                # full download
    python3 scripts/op_scrape.py --update       # only pages not stored yet
    python3 scripts/op_scrape.py --reparse      # rebuild from data/raw (no network)
    python3 scripts/op_scrape.py --search "Joy Boy"

Standard library only, Python 3.8+.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://onepiece.fandom.com/api.php"
UA = "OnePieceTheoryKB/1.0 (personal research; github.com/hnabeel96/onepiece)"
OUT = Path(os.environ.get("OP_OUT", "data"))
BATCH = 50          # MediaWiki allows 50 titles per query
PAUSE = 1.0         # seconds between requests, be polite to the wiki

# Sections that are the author's own words (translated), not wiki-written prose.
AUTHOR_SECTIONS = ("Author Comment", "Author's Comment", "Author Note", "Author Notes")


# ---------------------------------------------------------------- network

def api(params, tries=4):
    params = {**params, "format": "json", "formatversion": "2"}
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            wait = 5 * (attempt + 1)
            print(f"  ! request failed ({e}); retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"giving up on {url}")


def fetch_pages(titles):
    """Return {title: wikitext} for existing pages, following redirects."""
    out = {}
    for i in range(0, len(titles), BATCH):
        chunk = titles[i:i + BATCH]
        data = api({
            "action": "query", "prop": "revisions", "rvprop": "content",
            "rvslots": "main", "redirects": "1", "titles": "|".join(chunk),
        })
        q = data.get("query", {})
        back = {}
        for n in q.get("normalized", []):
            back[n["to"]] = n["from"]
        for r in q.get("redirects", []):
            back[r["to"]] = back.get(r["from"], r["from"])
        for p in q.get("pages", []):
            if p.get("missing") or "revisions" not in p:
                continue
            asked = back.get(p["title"], p["title"])
            out[asked] = p["revisions"][0]["slots"]["main"]["content"]
        time.sleep(PAUSE)
    return out


# ---------------------------------------------------------------- parsing

def strip_wikitext(text):
    """Crude but dependency-free wikitext -> plain text."""
    t = text
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", "", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    prev = None
    while prev != t:                                        # nested templates
        prev = t
        t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\{\|.*?\|\}", "", t, flags=re.S)          # tables
    t = re.sub(r"\[\[(?:File|Image|Category):[^\]]*\]\]", "", t, flags=re.I)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)      # [[a|b]] -> b
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)              # [[a]] -> a
    t = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", t)
    t = re.sub(r"'''?", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"^=+\s*(.*?)\s*=+\s*$", r"\n## \1\n", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def infobox_field(text, field):
    m = re.search(r"\|\s*" + re.escape(field) + r"\s*=\s*([^\n|}]*)", text)
    return strip_wikitext(m.group(1)).strip() if m else ""


def section(text, name):
    m = re.search(r"==\s*" + name + r"\s*==(.*?)(?=\n==[^=]|\Z)", text, flags=re.S | re.I)
    return strip_wikitext(m.group(1)) if m else ""


def linked_topics(text):
    """Wiki link targets in a chunk of wikitext (no files/categories), de-duplicated."""
    seen, out = set(), []
    for t in re.findall(r"\[\[([^\]|#]+)", text):
        t = t.strip()
        if t and ":" not in t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def characters_in(text):
    block = re.search(r"==\s*Characters\s*==(.*?)(?=\n==[^=]|\Z)", text, flags=re.S | re.I)
    return linked_topics(block.group(1)) if block else []


def drop_author_sections(wt):
    for name in AUTHOR_SECTIONS:
        wt = re.sub(r"\n==\s*" + re.escape(name) + r"\s*==.*?(?=\n==[^=]|\Z)", "\n",
                    wt, flags=re.S | re.I)
    return wt


def arc_of(wt):
    """The arc navbox, e.g. {{Egghead Arc}}, under 'Arc Navigation' or 'Site Navigation'."""
    nav = re.search(r"==\s*(?:Arc|Site) Navigation\s*==(.*)", wt, flags=re.S | re.I)
    m = re.search(r"\{\{([^{}|]*?\bArc)\s*[|}]", nav.group(1) if nav else wt)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- storage

def open_db():
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(OUT / "onepiece.db")
    db.executescript("""
    DROP TABLE IF EXISTS sbs;
    CREATE TABLE IF NOT EXISTS chapters(
        number INTEGER PRIMARY KEY, title TEXT, volume TEXT, arc TEXT,
        release TEXT, cover TEXT, short_summary TEXT, long_summary TEXT,
        notes TEXT, characters TEXT, fetched_at TEXT);
    CREATE TABLE IF NOT EXISTS sbs_index(
        volume INTEGER, entry INTEGER, chapter INTEGER, page INTEGER,
        topics TEXT, PRIMARY KEY(volume, entry));
    CREATE VIRTUAL TABLE IF NOT EXISTS search USING fts5(
        kind, ref, title, body, tokenize='porter unicode61');
    """)
    return db


def save_raw(kind, name, wt):
    d = OUT / "raw" / kind
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.wiki").write_text(wt, encoding="utf-8")


def index(db, kind, ref, title, body):
    db.execute("DELETE FROM search WHERE kind=? AND ref=?", (kind, str(ref)))
    db.execute("INSERT INTO search VALUES(?,?,?,?)", (kind, str(ref), title, body))


def save_chapter(db, n, wt):
    wt = drop_author_sections(wt)
    save_raw("chapters", f"chapter_{n:04d}", wt)
    title = infobox_field(wt, "title") or infobox_field(wt, "ename")
    rec = dict(
        number=n,
        title=title,
        volume="",                      # filled in from SBS headers by link_volumes()
        arc=arc_of(wt),
        release=infobox_field(wt, "date") or infobox_field(wt, "release"),
        cover=section(wt, "Cover Page"),
        short_summary=section(wt, "Short Summary"),
        long_summary=section(wt, "Long Summary"),
        notes=(section(wt, "Quick References") + "\n" + section(wt, "Trivia")).strip(),
        characters=json.dumps(characters_in(wt)),
        fetched_at=time.strftime("%Y-%m-%d"),
    )
    db.execute("INSERT OR REPLACE INTO chapters VALUES(:number,:title,:volume,:arc,"
               ":release,:cover,:short_summary,:long_summary,:notes,:characters,"
               ":fetched_at)", rec)
    body = "\n\n".join(x for x in [rec["cover"], rec["short_summary"],
                                   rec["long_summary"], rec["notes"]] if x)
    index(db, "chapter", n, title, body)
    write_chapter_md(rec)


def write_chapter_md(rec):
    n = rec["number"]
    meta = "  |  ".join(f"{k}: {rec[k.lower()]}" for k in ("Volume", "Arc", "Release")
                        if rec[k.lower()])
    md = [f"# Chapter {n}: {rec['title']}", ""]
    if meta:
        md += [meta, ""]
    md += [f"Source: https://onepiece.fandom.com/wiki/Chapter_{n} (CC-BY-SA)", ""]
    for head, key in [("Cover page", "cover"), ("Short summary", "short_summary"),
                      ("Long summary", "long_summary"), ("Notes & trivia", "notes")]:
        if rec[key].strip():
            md += [f"## {head}", "", rec[key].strip(), ""]
    chars = json.loads(rec["characters"])
    if chars:
        md += ["## Characters", "", ", ".join(chars), ""]
    (OUT / "chapters").mkdir(exist_ok=True)
    (OUT / "chapters" / f"chapter_{n:04d}.md").write_text("\n".join(md), encoding="utf-8")


def save_sbs(db, v, wt):
    """
    SBS pages are transcripts of Oda's Q&A, so the text itself is NOT stored.
    Only an index is kept: for each question, where it ran (volume, chapter, page)
    and which wiki topics it links to. Read the Q&A itself on the wiki or in the volume.
    """
    db.execute("DELETE FROM sbs_index WHERE volume=?", (v,))
    entries, chap, page = [], None, None
    for part in re.split(r"(\n==[^=].*?==)", wt):
        h = re.match(r"\n==\s*Chapter\s*(\d+)\s*,\s*Page\s*(\d+)", part)
        if h:
            chap, page = int(h.group(1)), int(h.group(2))
            continue
        if part.startswith("\n=="):
            chap = page = None
            continue
        if chap is None:
            continue
        # reader questions start a line with D: (bold or plain)
        for qa in re.split(r"\n\s*(?:'{2,3})?\s*D\s*(?:'{2,3})?\s*:", "\n" + part)[1:]:
            entries.append((chap, page, linked_topics(qa)))
    for i, (chap, page, topics) in enumerate(entries, 1):
        db.execute("INSERT INTO sbs_index VALUES(?,?,?,?,?)",
                   (v, i, chap, page, json.dumps(topics)))
    index(db, "sbs", v, f"SBS Volume {v}", " ; ".join(linked_topics(wt)))

    url = f"https://onepiece.fandom.com/wiki/SBS_Volume_{v}"
    md = [f"# SBS Volume {v}: topic index", "",
          f"Read the Q&A: {url}", "",
          "| # | Chapter | Page | Topics linked in the entry |",
          "|---|---|---|---|"]
    for i, (chap, page, topics) in enumerate(entries, 1):
        md.append(f"| {i} | {chap} | {page} | {', '.join(topics) or '-'} |")
    (OUT / "sbs").mkdir(exist_ok=True)
    (OUT / "sbs" / f"sbs_volume_{v:03d}.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def link_volumes(db):
    """Each SBS volume names the chapters it ran in -> chapter-to-volume map, gaps filled."""
    known = dict(db.execute("SELECT chapter, MIN(volume) FROM sbs_index GROUP BY chapter"))
    anchors = sorted(known.items())
    if anchors:
        for (n,) in db.execute("SELECT number FROM chapters").fetchall():
            if n in known:
                vol = known[n]
            else:
                before = [v for c, v in anchors if c < n]
                after = [v for c, v in anchors if c > n]
                vol = before[-1] if before and after and before[-1] == after[0] else None
            if vol is not None:
                db.execute("UPDATE chapters SET volume=? WHERE number=?", (str(vol), n))
        db.commit()
    cols = [d[1] for d in db.execute("PRAGMA table_info(chapters)")]
    for row in db.execute("SELECT * FROM chapters").fetchall():
        write_chapter_md(dict(zip(cols, row)))


def write_attribution():
    (OUT / "ATTRIBUTION.txt").write_text(
        "Chapter summaries in this folder come from the One Piece Wiki\n"
        "(https://onepiece.fandom.com), written by its contributors and licensed under\n"
        "CC-BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/). Reformatted to plain text.\n\n"
        "SBS files are a topic index only (where each question appears and which wiki\n"
        "topics it links to). The Q&A text itself is Eiichiro Oda's and is not included.\n"
        "Author comments are excluded for the same reason.\n\n"
        "One Piece is (c) Eiichiro Oda / Shueisha. This is a fan research database.\n",
        encoding="utf-8")


# ---------------------------------------------------------------- crawl

def crawl(db, prefix, start, saver, have, step=BATCH, stop_after_empty=2):
    """Fetch numbered pages in batches until two batches in a row come back empty."""
    n, empties, got = start, 0, 0
    while empties < stop_after_empty:
        nums = [k for k in range(n, n + step) if k not in have]
        found = 0
        if nums:
            pages = fetch_pages([f"{prefix}{k}" for k in nums])
            for k in nums:
                wt = pages.get(f"{prefix}{k}")
                if wt:
                    saver(db, k, wt)
                    found += 1
            db.commit()
            got += found
            print(f"  {prefix}{n}-{n + step - 1}: {found} saved")
        any_known = any(k in have for k in range(n, n + step))
        empties = 0 if (found or any_known) else empties + 1
        n += step
    return got


def run(update):
    db = open_db()
    have_ch = {r[0] for r in db.execute("SELECT number FROM chapters")} if update else set()
    have_sbs = ({r[0] for r in db.execute("SELECT DISTINCT volume FROM sbs_index")}
                if update else set())
    print("Chapters...")
    c = crawl(db, "Chapter ", 1, save_chapter, have_ch)
    print("SBS volumes (index only)...")
    s = crawl(db, "SBS Volume ", 1, save_sbs, have_sbs, step=25)
    link_volumes(db)
    write_attribution()
    print(f"\nDone: {c} chapters and {s} SBS indexes added. Data is in {OUT.resolve()}")


def reparse():
    """Rebuild chapters from data/raw without touching the network."""
    db = open_db()
    files = sorted((OUT / "raw" / "chapters").glob("chapter_*.wiki"))
    for f in files:
        save_chapter(db, int(f.stem.split("_")[1]), f.read_text(encoding="utf-8"))
    db.commit()
    link_volumes(db)
    write_attribution()
    print(f"Re-parsed {len(files)} chapters.")


def search(q, limit=15):
    db = open_db()
    rows = db.execute(
        "SELECT kind, ref, title, snippet(search, 3, '[', ']', ' ... ', 18) "
        "FROM search WHERE search MATCH ? ORDER BY rank LIMIT ?", (q, limit)).fetchall()
    if not rows:
        print("No matches.")
    for kind, ref, title, snip in rows:
        label = f"Ch {ref}" if kind == "chapter" else f"SBS Vol {ref}"
        print(f"{label:>12} | {title}\n             {snip}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", action="store_true", help="fetch only pages not yet stored")
    ap.add_argument("--reparse", action="store_true", help="rebuild from data/raw, no network")
    ap.add_argument("--search", metavar="QUERY", help='full-text search, e.g. "Joy Boy"')
    a = ap.parse_args()
    if a.search:
        search(a.search)
    elif a.reparse:
        reparse()
    else:
        run(a.update)
