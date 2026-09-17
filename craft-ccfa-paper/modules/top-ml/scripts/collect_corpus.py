#!/usr/bin/env python3
"""Collect official metadata for recent CVPR/ICCV/ECCV/NeurIPS/ICML papers.

The script stores metadata, not PDFs. It intentionally records unavailable and
future venue-years so an empty result is never mistaken for a successful crawl.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin


AS_OF = "2026-08-04"
USER_AGENT = "write-top-ml-paper/1.0 (metadata research; respectful rate limiting)"


def fetch(url: str, cache_dir: Path, refresh: bool = False) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".html")
    if target.exists() and not refresh:
        return target.read_text(encoding="utf-8", errors="replace")
    cmd = [
        "curl", "--compressed", "--fail", "--location", "--silent", "--show-error",
        "--retry", "3", "--retry-delay", "2", "--max-time", "180",
        "--user-agent", USER_AGENT, url,
    ]
    data = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout
    target.write_bytes(data)
    time.sleep(0.15)
    return data.decode("utf-8", errors="replace")


def clean(fragment: str) -> str:
    fragment = re.sub(r"<script\b.*?</script>", " ", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<style\b.*?</style>", " ", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def norm_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", html.unescape(value)).lower()
    value = value.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return re.sub(r"[^a-z0-9]+", "", value)


def parse_cvf(page: str, conference: str, year: int, source_url: str) -> list[dict]:
    records = []
    pattern = re.compile(
        r'<dt\s+class="ptitle".*?<a\s+href="([^"]+)">(.*?)</a>\s*</dt>'
        r'\s*<dd>(.*?)</dd>\s*<dd>(.*?)</dd>',
        re.I | re.S,
    )
    for paper_path, title_html, authors_html, links_html in pattern.findall(page):
        authors = re.findall(r'name="query_author"\s+value="([^"]+)"', authors_html, re.I)
        if not authors:
            authors = [x.strip() for x in clean(authors_html).split(",") if x.strip()]
        pdf_match = re.search(r'href=["\']([^"\']+\.pdf)["\']', links_html, re.I)
        paper_url = urljoin(source_url, html.unescape(paper_path))
        records.append({
            "conference": conference,
            "year": year,
            "title": clean(title_html),
            "authors": [html.unescape(a).strip() for a in authors],
            "paper_url": paper_url,
            "pdf_url": urljoin(source_url, html.unescape(pdf_match.group(1))) if pdf_match else None,
            "openreview_url": None,
            "track": "main",
            "presentation": "poster",
            "source_url": source_url,
        })
    return records


def parse_neurips(page: str, year: int, source_url: str) -> list[dict]:
    records = []
    pattern = re.compile(
        r'<li\s+class="([^"]+)"\s+data-track="([^"]+)".*?'
        r'<a\s+title="paper title"\s+href="([^"]+)">(.*?)</a>\s*'
        r'<span\s+class="paper-authors">(.*?)</span>',
        re.I | re.S,
    )
    for css_track, track, paper_path, title_html, authors_html in pattern.findall(page):
        paper_url = urljoin(source_url, html.unescape(paper_path))
        pdf_url = paper_url.replace("/hash/", "/file/").replace("-Abstract-", "-Paper-")
        pdf_url = re.sub(r"\.html$", ".pdf", pdf_url)
        records.append({
            "conference": "NeurIPS",
            "year": year,
            "title": clean(title_html),
            "authors": [a.strip() for a in clean(authors_html).split(",") if a.strip()],
            "paper_url": paper_url,
            "pdf_url": pdf_url,
            "openreview_url": None,
            "track": track or css_track,
            "presentation": "poster",
            "source_url": source_url,
        })
    return records


def parse_pmlr(page: str, year: int, volume: str, source_url: str) -> list[dict]:
    records = []
    for block in re.findall(r'<div\s+class="paper">(.*?)</div>', page, re.I | re.S):
        title_m = re.search(r'<p\s+class="title">(.*?)</p>', block, re.I | re.S)
        authors_m = re.search(r'<span\s+class="authors">(.*?)</span>', block, re.I | re.S)
        abs_m = re.search(r'href="([^"]+\.html)"[^>]*>abs</a>', block, re.I)
        pdf_m = re.search(r'href="([^"]+\.pdf)"', block, re.I)
        or_m = re.search(r'href="(https://openreview\.net/forum\?id=[^"]+)"', block, re.I)
        if not title_m:
            continue
        author_text = clean(authors_m.group(1)) if authors_m else ""
        authors = [a.strip() for a in re.split(r",|;", author_text) if a.strip()]
        records.append({
            "conference": "ICML",
            "year": year,
            "title": clean(title_m.group(1)),
            "authors": authors,
            "paper_url": html.unescape(abs_m.group(1)) if abs_m else None,
            "pdf_url": html.unescape(pdf_m.group(1)) if pdf_m else None,
            "openreview_url": html.unescape(or_m.group(1)) if or_m else None,
            "track": "main",
            "presentation": "poster",
            "source_url": source_url,
            "volume": volume,
        })
    return records


def parse_schedule(page: str, conference: str, year: int, source_url: str) -> list[dict]:
    records = []
    # Event cards contain nested divs, so a non-greedy closing-div regex truncates
    # them. Split on the next card boundary instead.
    for block in re.split(r'(?=<div\s+class="showDetailBtn"(?=\s|>))', page, flags=re.I)[1:]:
        title_m = re.search(r'<div\s+class="maincardBody">(.*?)</div>', block, re.I | re.S)
        authors_m = re.search(r'<div\s+class="maincardFooter">(.*?)</div>', block, re.I | re.S)
        or_m = re.search(r'href="(https://openreview\.net/forum\?id=[^"]+)"', block, re.I)
        if not title_m:
            continue
        or_url = html.unescape(or_m.group(1)) if or_m else None
        forum_id = or_url.split("id=", 1)[1] if or_url and "id=" in or_url else None
        records.append({
            "conference": conference,
            "year": year,
            "title": clean(title_m.group(1)),
            "authors": [a.strip() for a in clean(authors_m.group(1) if authors_m else "").split("⋅") if a.strip()],
            "paper_url": or_url,
            "pdf_url": f"https://openreview.net/pdf?id={forum_id}" if forum_id else None,
            "openreview_url": or_url,
            "track": "main",
            "presentation": "poster",
            "source_url": source_url,
        })
    return records


def parse_event_titles(page: str) -> set[str]:
    titles = set()
    for value in re.findall(
        r'<h3\s+class="event-title">\s*<a\s+href="[^"]+">(.*?)</a>\s*</h3>',
        page, re.I | re.S,
    ):
        titles.add(norm_title(clean(value)))
    if not titles:
        for value in re.findall(r'data-event-title="([^"]+)"', page, re.I):
            titles.add(norm_title(value))
    return titles


def deduplicate(records: list[dict]) -> list[dict]:
    by_key = {}
    for rec in records:
        key = (rec["conference"], rec["year"], norm_title(rec["title"]))
        if not key[2]:
            continue
        old = by_key.get(key)
        if old is None:
            by_key[key] = rec
            continue
        for field in ("authors", "paper_url", "pdf_url", "openreview_url"):
            if not old.get(field) and rec.get(field):
                old[field] = rec[field]
    return sorted(by_key.values(), key=lambda x: (x["conference"], x["year"], x["title"].lower()))


STATUS_GRID = [
    {"conference": "CVPR", "year": 2025, "status": "available"},
    {"conference": "CVPR", "year": 2026, "status": "available"},
    {"conference": "CVPR", "year": 2027, "status": "future"},
    {"conference": "ICCV", "year": 2025, "status": "available"},
    {"conference": "ICCV", "year": 2026, "status": "no-edition", "note": "ICCV is held in odd-numbered years."},
    {"conference": "ICCV", "year": 2027, "status": "future"},
    {"conference": "NeurIPS", "year": 2025, "status": "available"},
    {"conference": "NeurIPS", "year": 2026, "status": "future"},
    {"conference": "NeurIPS", "year": 2027, "status": "future"},
    {"conference": "ECCV", "year": 2025, "status": "no-edition", "note": "ECCV is held in even-numbered years."},
    {"conference": "ECCV", "year": 2026, "status": "not-public", "note": "Official proceedings/accepted-paper list not public at the as-of date."},
    {"conference": "ECCV", "year": 2027, "status": "no-edition", "note": "ECCV is held in even-numbered years."},
    {"conference": "ICML", "year": 2025, "status": "available"},
    {"conference": "ICML", "year": 2026, "status": "available-schedule", "note": "Official schedule/OpenReview links; PMLR volume not used."},
    {"conference": "ICML", "year": 2027, "status": "future"},
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--source-config", type=Path,
                    help="Optional JSON adding newly published paper and presentation sources")
    args = ap.parse_args()
    out = args.output_dir.resolve()
    cache = out / "cache"
    out.mkdir(parents=True, exist_ok=True)

    config = {}
    if args.source_config:
        config = json.loads(args.source_config.read_text(encoding="utf-8"))

    records: list[dict] = []
    source_log = []

    base_sources = [
        ("CVPR", 2025, "https://openaccess.thecvf.com/CVPR2025?day=all", "cvf"),
        ("CVPR", 2026, "https://openaccess.thecvf.com/CVPR2026?day=all", "cvf"),
        ("ICCV", 2025, "https://openaccess.thecvf.com/ICCV2025?day=all", "cvf"),
        ("NeurIPS", 2025, "https://papers.nips.cc/paper_files/paper/2025", "neurips"),
        ("ICML", 2025, "https://proceedings.mlr.press/v267/", "pmlr-v267"),
        ("ICML", 2026, "https://icml.cc/Conferences/2026/Schedule?type=Poster", "schedule"),
    ]
    for item in config.get("paper_sources", []):
        parser = item["parser"]
        if parser not in {"cvf", "neurips", "schedule"} and not parser.startswith("pmlr-"):
            raise ValueError(f"unsupported parser in source config: {parser}")
        base_sources.append((item["conference"], int(item["year"]), item["url"], parser))
    for conference, year, url, parser in base_sources:
        print(f"fetch {conference} {year}: {url}", file=sys.stderr)
        page = fetch(url, cache, args.refresh)
        if parser == "cvf":
            found = parse_cvf(page, conference, year, url)
        elif parser == "neurips":
            found = parse_neurips(page, year, url)
        elif parser.startswith("pmlr-"):
            found = parse_pmlr(page, year, parser.split("-", 1)[1], url)
        else:
            found = parse_schedule(page, conference, year, url)
        records.extend(found)
        source_log.append({"conference": conference, "year": year, "kind": "paper-list", "url": url, "records": len(found)})

    presentation_sources = [
        ("CVPR", 2025, "oral", "https://cvpr.thecvf.com/virtual/2025/events/oral"),
        ("CVPR", 2026, "oral", "https://cvpr.thecvf.com/virtual/2026/events/Oral"),
        ("CVPR", 2026, "highlight", "https://cvpr.thecvf.com/virtual/2026/events/Highlights2026"),
        ("ICCV", 2025, "oral", "https://iccv.thecvf.com/virtual/2025/events/oral"),
        ("ICML", 2025, "oral", "https://icml.cc/virtual/2025/events/oral"),
        ("ICML", 2025, "spotlight", "https://icml.cc/virtual/2025/events/2025SpotlightPosters"),
        ("ICML", 2026, "oral", "https://icml.cc/virtual/2026/events/oral"),
        ("ICML", 2026, "spotlight", "https://icml.cc/virtual/2026/events/2026SpotlightPosters"),
        ("NeurIPS", 2025, "oral", "https://neurips.cc/virtual/2025/loc/san-diego/events/oral"),
        ("NeurIPS", 2025, "spotlight", "https://neurips.cc/virtual/2025/loc/san-diego/events/spotlights-2025"),
    ]
    for item in config.get("presentation_sources", []):
        label = item["presentation"]
        if label not in {"poster", "spotlight", "highlight", "oral"}:
            raise ValueError(f"unsupported presentation label in source config: {label}")
        presentation_sources.append((item["conference"], int(item["year"]), label, item["url"]))
    records = deduplicate(records)
    index = {(r["conference"], r["year"], norm_title(r["title"])): r for r in records}
    for conference, year, label, url in presentation_sources:
        print(f"fetch {conference} {year} {label}: {url}", file=sys.stderr)
        titles = parse_event_titles(fetch(url, cache, args.refresh))
        matched = 0
        for title in titles:
            rec = index.get((conference, year, title))
            if rec:
                old = rec.get("presentation", "poster")
                precedence = {"poster": 0, "spotlight": 1, "highlight": 2, "oral": 3}
                if precedence[label] >= precedence.get(old, 0):
                    rec["presentation"] = label
                matched += 1
        source_log.append({
            "conference": conference, "year": year, "kind": label, "url": url,
            "listed_titles": len(titles), "matched_records": matched,
        })

    counts = {}
    for rec in records:
        key = f'{rec["conference"]}-{rec["year"]}'
        counts.setdefault(key, {"total": 0, "poster": 0, "spotlight": 0, "highlight": 0, "oral": 0})
        counts[key]["total"] += 1
        counts[key][rec["presentation"]] = counts[key].get(rec["presentation"], 0) + 1

    with (out / "papers.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    status_grid = [dict(item) for item in STATUS_GRID]
    status_index = {(item["conference"], item["year"]): item for item in status_grid}
    for override in config.get("status_overrides", []):
        key = (override["conference"], int(override["year"]))
        if key in status_index:
            status_index[key].update(override)
        else:
            item = dict(override)
            item["year"] = int(item["year"])
            status_grid.append(item)
            status_index[key] = item

    manifest = {
        "as_of": config.get("as_of", AS_OF),
        "generated_at_epoch": int(time.time()),
        "record_count": len(records),
        "counts": counts,
        "venue_year_status": status_grid,
        "sources": source_log,
        "limitations": [
            "Presentation labels are matched by normalized official titles.",
            "ICML 2026 PDF links point to OpenReview and may trigger anti-bot protection.",
            "Metadata collection does not imply that every PDF was downloaded or analyzed.",
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(records), "counts": counts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
