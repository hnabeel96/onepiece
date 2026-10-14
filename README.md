# One Piece theory base

A searchable knowledge base of every One Piece chapter and SBS volume, built from
[One Piece Wiki](https://onepiece.fandom.com) summaries, as the foundation for theory-crafting.

## What's in `data/`

| Path | Contents |
|---|---|
| `chapters/chapter_0001.md` … | One file per chapter: title, volume, arc, cover story, short + long summary, trivia, characters appearing |
| `sbs/sbs_volume_004.md` … | **Topic index** per SBS volume: every question's chapter and page, plus the wiki topics it links to. The Q&A text is Oda's and isn't stored, so follow the link to read it |
| `onepiece.db` | SQLite with tables `chapters`, `sbs_index` and an FTS5 full-text index `search` |
| `raw/chapters/` | Chapter wikitext (author comments removed), so the parser can be improved and re-run with `--reparse` |
| `ATTRIBUTION.txt` | License notice — keep it with the data |

## How it updates

The **Update One Piece knowledge base** GitHub Action (`.github/workflows/scrape.yml`)
runs every Monday and commits any new chapter/SBS pages. Run it by hand from the
**Actions** tab → *Run workflow*; tick **full** to re-download everything.

## Searching locally

```bash
python3 scripts/op_scrape.py --search "Joy Boy"
python3 scripts/op_scrape.py --search "\"Void Century\" OR \"Poneglyph\""
```

Or query the database directly:

```sql
-- every chapter a character appears in
SELECT number, title FROM chapters WHERE characters LIKE '%"Imu"%';

-- which SBS entries touch a topic (then read them on the wiki)
SELECT volume, chapter, page FROM sbs_index WHERE topics LIKE '%"Joy Boy"%';

-- ranked full-text search across chapters and SBS topics
SELECT kind, ref, title FROM search WHERE search MATCH 'Joy NEAR/5 Boy' ORDER BY rank;
```

## Layout

```
scripts/op_scrape.py      downloader, parser, search CLI (stdlib only)
.github/workflows/        scheduled updater
data/                     generated — don't edit by hand
theories/                 theory write-ups (to come)
```

## License

Wiki-derived text in `data/` is © One Piece Wiki contributors, licensed
[CC-BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). One Piece is © Eiichiro Oda / Shueisha.
This repo holds fan-written summaries only — no manga pages or scans.
Read the chapters themselves on [Manga Plus](https://mangaplus.shueisha.co.jp) or Viz.
