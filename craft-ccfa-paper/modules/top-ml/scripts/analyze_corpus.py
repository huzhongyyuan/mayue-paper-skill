#!/usr/bin/env python3
"""Analyze title style and a stratified PDF sample without retaining paper text."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import statistics
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install pypdf first: python3 -m pip install pypdf") from exc


PRIORITY = {"oral", "highlight", "spotlight"}
SECTION_RULES = [
    ("abstract", r"^abstract$"),
    ("introduction", r"\bintroduction\b"),
    ("related_work", r"\b(related work|literature review)\b"),
    ("background", r"\b(background|preliminar(?:y|ies)|problem setup|problem formulation)\b"),
    ("method", r"\b(method|methodology|approach|framework|model|algorithm)\b"),
    ("theory", r"\b(theory|theoretical analysis|analysis)\b"),
    ("experiments", r"\b(experiment|evaluation|empirical|results?)\b"),
    ("limitations", r"\b(limitations?|broader impact|societal impact)\b"),
    ("conclusion", r"\b(conclusion|discussion|summary)\b"),
    ("references", r"^references$"),
    ("appendix", r"^(appendix|supplementary material)\b"),
]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*|\d+(?:\.\d+)?", text)


def stable_rank(record: dict) -> str:
    return hashlib.sha256(f'{record["conference"]}|{record["year"]}|{record["title"]}'.encode()).hexdigest()


def quantiles(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    vals = sorted(values)
    def q(p: float) -> float:
        pos = (len(vals) - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        return vals[lo] if lo == hi else vals[lo] * (hi - pos) + vals[hi] * (pos - lo)
    return {
        "n": len(vals), "mean": round(statistics.mean(vals), 2),
        "median": round(statistics.median(vals), 2),
        "p25": round(q(0.25), 2), "p75": round(q(0.75), 2),
    }


def title_stats(records: list[dict]) -> dict:
    groups = defaultdict(list)
    for r in records:
        groups["all"].append(r)
        groups[r.get("presentation", "poster")].append(r)
        groups["priority" if r.get("presentation") in PRIORITY else "poster_only"].append(r)
        groups[f'{r["conference"]}-{r["year"]}'].append(r)
    result = {}
    for name, rows in groups.items():
        lens = [len(words(r["title"])) for r in rows]
        result[name] = {
            "count": len(rows),
            "word_count": quantiles(lens),
            "colon_pct": round(100 * sum(":" in r["title"] for r in rows) / len(rows), 2),
            "question_pct": round(100 * sum("?" in r["title"] for r in rows) / len(rows), 2),
            "acronym_prefix_pct": round(100 * sum(bool(re.match(r"^[A-Z][A-Za-z0-9-]{1,15}\s*:", r["title"])) for r in rows) / len(rows), 2),
        }
    return result


def choose_sample(records: list[dict], priority_per_stratum: int, poster_per_venue: int) -> list[dict]:
    groups = defaultdict(list)
    for r in records:
        label = r.get("presentation", "poster")
        if not r.get("pdf_url"):
            continue
        if label in PRIORITY:
            key = (r["conference"], r["year"], label)
            limit = priority_per_stratum
        else:
            key = (r["conference"], r["year"], "poster")
            limit = poster_per_venue
        groups[(key, limit)].append(r)
    selected = []
    for (key, limit), rows in sorted(groups.items()):
        selected.extend(sorted(rows, key=stable_rank)[:limit])
    return selected


def download_pdf(url: str, max_mb: int = 50) -> bytes:
    with tempfile.TemporaryDirectory(prefix="top-ml-paper-") as td:
        target = Path(td) / "paper.pdf"
        cmd = [
            "curl", "--fail", "--location", "--silent", "--show-error", "--compressed",
            "--retry", "2", "--max-time", "180", "--max-filesize", str(max_mb * 1024 * 1024),
            "--output", str(target), url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        data = target.read_bytes()
    if not data.startswith(b"%PDF"):
        raise ValueError("response is not a PDF")
    return data


def extract_text(data: bytes, max_pages: int) -> tuple[str, int]:
    reader = PdfReader(io.BytesIO(data), strict=False)
    pages = []
    for page in reader.pages[:max_pages]:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    text = "\n".join(pages).replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, min(len(reader.pages), max_pages)


def heading_kind(heading: str) -> str | None:
    plain = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[IVX]+)\s*[.:]?\s*", "", heading, flags=re.I)
    plain = re.sub(r"\s+", " ", plain).strip().lower()
    for kind, rule in SECTION_RULES:
        if re.search(rule, plain, re.I):
            return kind
    return None


def detect_headings(text: str) -> list[tuple[int, str, str]]:
    found = []
    offset = 0
    for raw_line in text.splitlines(True):
        line = raw_line.strip()
        top_numbered = bool(re.match(r"^\s*(?:\d+|[IVX]+)[.:]?\s*", line, re.I)) and not bool(
            re.match(r"^\s*\d+\.\d+", line)
        )
        label = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[IVX]+)[.:]?\s*", "", line, flags=re.I)
        label_key = re.sub(r"[^a-z ]+", "", label.lower()).strip()
        exact_unnumbered = bool(re.match(
            r"^(abstract|introduction|related work|literature review|background|preliminaries|"
            r"problem setup|problem formulation|method|methodology|approach|framework|model|"
            r"experiments?(?: and results?)?|evaluation|results?|limitations?|discussion|"
            r"conclusions?|conclusion and limitations|summary|references|appendix|supplementary material)$",
            label_key,
        ))
        plausible = (
            2 <= len(line) <= 90 and
            len(words(line)) <= 12 and
            not label.endswith((".", ",", ";", "?", "!")) and
            bool(re.match(r"^[A-Z]", label)) and
            (top_numbered or exact_unnumbered)
        )
        kind = heading_kind(line) if plausible else None
        if kind:
            found.append((offset, line, kind))
        offset += len(raw_line)
    # Keep first occurrence of a kind unless a repeated heading is far later.
    deduped = []
    seen = set()
    for item in found:
        if item[2] not in seen:
            deduped.append(item)
            seen.add(item[2])
    return deduped


def section_features(text: str, start: int, end: int) -> dict:
    segment = text[start:end]
    token_count = len(words(segment))
    sentence_count = len(re.findall(r"(?<=[.!?])\s+(?=[A-Z])", segment)) + (1 if token_count else 0)
    return {
        "word_count": token_count,
        "sentence_count": sentence_count,
        "citation_mentions": len(re.findall(r"\[[0-9,; -]+\]|\([A-Z][A-Za-z-]+ et al\.,? \d{4}\)", segment)),
        "figure_mentions": len(re.findall(r"\b(Fig(?:ure)?\.?|Table)\s*\d+", segment, re.I)),
        "first_person_mentions": len(re.findall(r"\b(we|our|ours)\b", segment, re.I)),
        "contribution_cues": len(re.findall(r"\b(our contributions?|we (?:make|introduce|propose|show|demonstrate|develop|present))\b", segment, re.I)),
        "limitation_cues": len(re.findall(r"\b(limitations?|failure cases?|future work|does not|cannot|remain(?:s)? challenging)\b", segment, re.I)),
        "claim_cues": len(re.findall(r"\b(outperform|state[- ]of[- ]the[- ]art|significant(?:ly)?|improv(?:e|es|ed|ement)|superior)\b", segment, re.I)),
    }


def analyze_paper(record: dict, data: bytes, max_pages: int) -> dict:
    text, pages = extract_text(data, max_pages)
    headings = detect_headings(text)
    sections = {}
    for i, (offset, heading, kind) in enumerate(headings):
        if kind in {"references", "appendix"}:
            continue
        start = offset + len(heading)
        end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        sections[kind] = section_features(text, start, end)
    main_order = [h[2] for h in headings if h[2] not in {"references", "appendix"}]
    return {
        "conference": record["conference"], "year": record["year"],
        "title": record["title"], "presentation": record.get("presentation", "poster"),
        "pages_extracted": pages, "total_words_extracted": len(words(text)),
        "headings": [h[1] for h in headings], "section_order": main_order,
        "sections": sections,
    }


def aggregate_analyses(rows: list[dict]) -> dict:
    section_rows = defaultdict(list)
    heading_sequences = Counter()
    by_presentation = Counter()
    for row in rows:
        by_presentation[row["presentation"]] += 1
        heading_sequences[" > ".join(row["section_order"])] += 1
        for kind, features in row["sections"].items():
            section_rows[kind].append(features)
    sections = {}
    for kind, features_list in section_rows.items():
        sections[kind] = {"papers": len(features_list)}
        for field in features_list[0]:
            sections[kind][field] = quantiles([f[field] for f in features_list])
    return {
        "papers_analyzed": len(rows),
        "by_presentation": dict(by_presentation),
        "sections": sections,
        "common_section_orders": heading_sequences.most_common(12),
    }


def process_record(record: dict, max_pages: int) -> tuple[dict | None, dict | None]:
    try:
        return analyze_paper(record, download_pdf(record["pdf_url"]), max_pages), None
    except Exception as exc:
        return None, {
            "conference": record["conference"], "year": record["year"],
            "title": record["title"], "presentation": record.get("presentation"),
            "pdf_url": record.get("pdf_url"), "error": str(exc)[:500],
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True, help="papers.jsonl from collect_corpus.py")
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--priority-per-stratum", type=int, default=12)
    ap.add_argument("--poster-per-venue", type=int, default=8)
    ap.add_argument("--max-pages", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    records = [json.loads(line) for line in args.corpus.read_text(encoding="utf-8").splitlines() if line.strip()]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sample = choose_sample(records, args.priority_per_stratum, args.poster_per_venue)
    analyses, failures = [], []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {pool.submit(process_record, record, args.max_pages): record for record in sample}
        for idx, future in enumerate(as_completed(futures), 1):
            record = futures[future]
            print(f'[{idx}/{len(sample)}] {record["conference"]} {record["year"]} {record["presentation"]}: {record["title"]}', file=sys.stderr)
            analysis, failure = future.result()
            if analysis:
                analyses.append(analysis)
            if failure:
                failures.append(failure)
    with (args.output_dir / "paper_analysis.jsonl").open("w", encoding="utf-8") as fh:
        for row in analyses:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "corpus_records": len(records), "sample_requested": len(sample),
        "sample_succeeded": len(analyses), "sample_failed": len(failures),
        "title_style": title_stats(records),
        "fulltext": aggregate_analyses(analyses),
        "failures": failures,
        "method": "Stable stratified sample by venue-year-presentation; PDFs are discarded after feature extraction.",
    }
    (args.output_dir / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("corpus_records", "sample_requested", "sample_succeeded", "sample_failed")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
