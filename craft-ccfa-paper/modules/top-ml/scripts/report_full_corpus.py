#!/usr/bin/env python3
"""Generate aggregate guidance plus per-section/per-figure exports from SQLite."""

from __future__ import annotations

import argparse
import gzip
import json
import math
import sqlite3
import statistics
from collections import Counter, defaultdict
from pathlib import Path


PRIORITY = {"oral", "highlight", "spotlight"}


def qstats(values):
    vals = sorted(float(v) for v in values if v is not None)
    if not vals:
        return {"n": 0}
    def q(p):
        pos = (len(vals) - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        return vals[lo] if lo == hi else vals[lo] * (hi - pos) + vals[hi] * (pos - lo)
    return {
        "n": len(vals), "mean": round(statistics.mean(vals), 2),
        "median": round(statistics.median(vals), 2),
        "p25": round(q(0.25), 2), "p75": round(q(0.75), 2),
    }


def pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


def export_rows(conn, output_dir: Path):
    figure_query = """
      SELECT p.paper_id,p.conference,p.year,p.title,p.presentation,v.visual_order,
        v.kind,v.label,v.page,v.caption,v.figure_type,v.bbox_json,v.visual_json,
        v.caption_signals_json,v.image_object_count
      FROM visuals v JOIN papers p USING(paper_id) WHERE p.status='done'
      ORDER BY p.conference,p.year,p.title,v.visual_order
    """
    section_query = """
      SELECT p.paper_id,p.conference,p.year,p.title,p.presentation,s.*
      FROM sections s JOIN papers p USING(paper_id) WHERE p.status='done'
      ORDER BY p.conference,p.year,p.title,s.section_order
    """
    for name, query in (("figures.jsonl.gz", figure_query), ("sections.jsonl.gz", section_query)):
        with gzip.open(output_dir / name, "wt", encoding="utf-8") as fh:
            cur = conn.execute(query)
            columns = [d[0] for d in cur.description]
            for row in cur:
                item = dict(zip(columns, row))
                for key in ("bbox_json", "visual_json", "caption_signals_json", "role_counts_json"):
                    if key in item and item[key]:
                        item[key[:-5] if key.endswith("_json") else key] = json.loads(item.pop(key))
                fh.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def build_summary(conn):
    status = dict(conn.execute("SELECT status,COUNT(*) FROM papers GROUP BY status").fetchall())
    analyzer_versions = dict(conn.execute(
        "SELECT COALESCE(analyzer_version,'unprocessed'),COUNT(*) FROM papers GROUP BY analyzer_version"
    ).fetchall())
    processed_versions = [key for key in analyzer_versions if key != "unprocessed"]
    venue = []
    for row in conn.execute("""
      SELECT conference,year,COUNT(*),SUM(status='done'),SUM(status='blocked'),
        SUM(status='error'),SUM(status='not_found'),SUM(status='no_pdf'),
        COALESCE(SUM(CASE WHEN status='done' THEN figure_count END),0),
        COALESCE(SUM(CASE WHEN status='done' THEN table_count END),0)
      FROM papers GROUP BY conference,year ORDER BY conference,year
    """):
        venue.append(dict(zip(
            ["conference", "year", "records", "done", "blocked", "error", "not_found", "no_pdf", "figures", "tables"], row
        )))

    done_papers = conn.execute("SELECT COUNT(*) FROM papers WHERE status='done'").fetchone()[0]
    done_priority = conn.execute(
        "SELECT COUNT(*) FROM papers WHERE status='done' AND presentation IN ('oral','highlight','spotlight')"
    ).fetchone()[0]

    quality_counts = Counter()
    quality_examples = []
    for pid, title, section_count, figure_count in conn.execute(
        "SELECT paper_id,title,section_count,figure_count FROM papers WHERE status='done'"
    ):
        rows = conn.execute(
            "SELECT section_order,category,word_count FROM sections WHERE paper_id=? ORDER BY section_order", (pid,)
        ).fetchall()
        categories = {row[1] for row in rows}
        flags = []
        for category in ("abstract", "introduction", "method", "experiments", "conclusion", "references"):
            if category not in categories:
                flags.append(f"missing_{category}")
        if (section_count or 0) <= 4:
            flags.append("low_section_count")
        if (figure_count or 0) == 0:
            flags.append("zero_detected_figures")
        if any((row[2] or 0) > 6000 and row[1] not in {"references", "appendix"} for row in rows):
            flags.append("oversized_main_section")
        abstract_order = next((row[0] for row in rows if row[1] == "abstract"), None)
        intro_order = next((row[0] for row in rows if row[1] == "introduction"), None)
        if abstract_order is not None and intro_order is not None and abstract_order > intro_order:
            flags.append("abstract_after_introduction")
        quality_counts.update(flags)
        if flags and len(quality_examples) < 50:
            quality_examples.append({"title": title, "flags": flags})

    section_rows = conn.execute("""
      SELECT p.paper_id,p.presentation,s.category,s.heading,s.word_count,s.sentence_count,
        s.paragraph_count,s.avg_sentence_words,s.citation_mentions,s.figure_mentions,
        s.table_mentions,s.equation_mentions,s.first_person_mentions,s.hedge_mentions,
        s.strong_claim_mentions,s.contribution_cues,s.limitation_cues,s.role_counts_json
      FROM sections s JOIN papers p USING(paper_id)
      WHERE p.status='done' AND s.category NOT IN ('references','appendix','other')
    """).fetchall()
    section_groups = defaultdict(list)
    section_papers = defaultdict(set)
    for row in section_rows:
        item = {
            "paper_id": row[0], "presentation": row[1], "category": row[2], "heading": row[3],
            "word_count": row[4], "sentence_count": row[5], "paragraph_count": row[6],
            "avg_sentence_words": row[7], "citation_mentions": row[8], "figure_mentions": row[9],
            "table_mentions": row[10], "equation_mentions": row[11], "first_person_mentions": row[12],
            "hedge_mentions": row[13], "strong_claim_mentions": row[14],
            "contribution_cues": row[15], "limitation_cues": row[16],
            "role_counts": json.loads(row[17] or "{}"),
        }
        audience = "priority" if item["presentation"] in PRIORITY else "poster"
        section_groups[(item["category"], audience)].append(item)
        section_papers[(item["category"], audience)].add(item["paper_id"])

    section_summary = {}
    for (category, audience), rows in section_groups.items():
        section_summary.setdefault(category, {})[audience] = {
            "sections": len(rows), "papers": len(section_papers[(category, audience)]),
            "word_count": qstats([r["word_count"] for r in rows]),
            "sentence_count": qstats([r["sentence_count"] for r in rows]),
            "avg_sentence_words": qstats([r["avg_sentence_words"] for r in rows]),
            "citations": qstats([r["citation_mentions"] for r in rows]),
            "figure_mentions": qstats([r["figure_mentions"] for r in rows]),
            "strong_claims": qstats([r["strong_claim_mentions"] for r in rows]),
        }

    orders = Counter()
    for pid, in conn.execute("SELECT paper_id FROM papers WHERE status='done'"):
        categories = [r[0] for r in conn.execute(
            "SELECT category FROM sections WHERE paper_id=? AND category NOT IN ('references','appendix','other') ORDER BY section_order",
            (pid,),
        )]
        if categories:
            orders[" > ".join(categories)] += 1

    visual_rows = conn.execute("""
      SELECT p.paper_id,p.presentation,v.kind,v.figure_type,v.page,v.visual_json,
        v.caption_signals_json,v.visual_order
      FROM visuals v JOIN papers p USING(paper_id) WHERE p.status='done'
    """).fetchall()
    visual_groups = defaultdict(list)
    first_figures = {}
    for row in visual_rows:
        visual = json.loads(row[5] or "{}")
        signals = json.loads(row[6] or "{}")
        item = {
            "paper_id": row[0], "presentation": row[1], "kind": row[2], "figure_type": row[3],
            "page": row[4], "visual": visual, "signals": signals, "order": row[7],
        }
        audience = "priority" if item["presentation"] in PRIORITY else "poster"
        visual_groups[(item["kind"], item["figure_type"], audience)].append(item)
        if item["kind"] == "figure" and (item["paper_id"] not in first_figures or item["order"] < first_figures[item["paper_id"]]["order"]):
            first_figures[item["paper_id"]] = item

    visual_summary = {}
    for (kind, ftype, audience), rows in visual_groups.items():
        visual_summary.setdefault(kind, {}).setdefault(ftype, {})[audience] = {
            "count": len(rows),
            "page": qstats([r["page"] for r in rows]),
            "width_page_fraction": qstats([r["visual"].get("width_page_fraction") for r in rows]),
            "aspect_ratio": qstats([r["visual"].get("aspect_ratio") for r in rows]),
            "colorfulness": qstats([r["visual"].get("colorfulness") for r in rows]),
            "white_fraction": qstats([r["visual"].get("white_fraction") for r in rows]),
            "edge_density": qstats([r["visual"].get("edge_density") for r in rows]),
            "caption_words": qstats([r["signals"].get("word_count") for r in rows]),
            "subfigures": qstats([r["signals"].get("subfigure_count") for r in rows]),
            "takeaway_pct": pct(sum(bool(r["signals"].get("has_takeaway")) for r in rows), len(rows)),
            "comparison_pct": pct(sum(bool(r["signals"].get("has_comparison")) for r in rows), len(rows)),
            "protocol_pct": pct(sum(bool(r["signals"].get("has_protocol")) for r in rows), len(rows)),
        }

    first_figure_types = Counter(v["figure_type"] for v in first_figures.values())
    first_figure_pages = qstats([v["page"] for v in first_figures.values()])
    return {
        "status": status, "analyzer_versions": analyzer_versions,
        "mixed_analyzer_versions": len(processed_versions) > 1,
        "report_state": "in_progress" if status.get("pending", 0) or status.get("processing", 0) else "complete",
        "venue_year": venue,
        "papers_analyzed": done_papers, "priority_papers_analyzed": done_priority,
        "extraction_quality": {"flag_counts": dict(quality_counts), "examples": quality_examples},
        "sections": section_summary,
        "common_section_orders": orders.most_common(20),
        "visuals": visual_summary,
        "first_figure_types": first_figure_types.most_common(),
        "first_figure_pages": first_figure_pages,
    }


def render_markdown(summary: dict) -> str:
    out = [
        "# Full-corpus paper writing and figure analysis",
        "",
        "This report is descriptive. It does not claim that a layout or phrase causes acceptance.",
        "",
        "## Coverage",
        "",
        f'- Report state: **{summary["report_state"]}**',
        f'- Papers analyzed: {summary["papers_analyzed"]:,}',
        f'- Priority papers analyzed: {summary["priority_papers_analyzed"]:,}',
        f'- Status counts: `{json.dumps(summary["status"], sort_keys=True)}`',
        f'- Analyzer versions: `{json.dumps(summary["analyzer_versions"], sort_keys=True)}`',
        "",
        "| Venue-year | Records | Done | Blocked | Error | Figures | Tables |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    if summary.get("mixed_analyzer_versions"):
        out.insert(10, "- Warning: aggregates currently mix analyzer versions; resume migration before treating them as a stable snapshot.")
    for r in summary["venue_year"]:
        out.append(f'| {r["conference"]} {r["year"]} | {r["records"]:,} | {r["done"]:,} | {r["blocked"]:,} | {r["error"]:,} | {r["figures"]:,} | {r["tables"]:,} |')

    out += ["", "## Extraction quality diagnostics", "",
            "These are review flags, not automatic proof of parser failure; some paper genres legitimately omit a canonical section.", ""]
    quality = summary.get("extraction_quality", {})
    if quality.get("flag_counts"):
        for name, count in sorted(quality["flag_counts"].items(), key=lambda item: (-item[1], item[0])):
            out.append(f"- `{name}`: {count:,}")
    else:
        out.append("- No extraction-quality flags in the current completed set.")

    out += ["", "## Section construction", "", "Medians are shown as `poster / priority`.", "",
            "| Section | Paper count | Words | Sentences | Sentence length | Citations | Figure refs |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    order = ["abstract", "introduction", "related_work", "background", "method", "theory", "data", "experiments", "limitations", "conclusion"]
    for category in order:
        groups = summary["sections"].get(category, {})
        p, q = groups.get("poster", {}), groups.get("priority", {})
        def pair(field):
            return f'{p.get(field, {}).get("median", "-")} / {q.get(field, {}).get("median", "-")}'
        out.append(
            f'| {category} | {p.get("papers",0):,} / {q.get("papers",0):,} | {pair("word_count")} | '
            f'{pair("sentence_count")} | {pair("avg_sentence_words")} | {pair("citations")} | {pair("figure_mentions")} |'
        )
    out += ["", "Common detected section orders:", ""]
    for order_name, count in summary["common_section_orders"][:12]:
        out.append(f"- `{order_name}` — {count:,} papers")

    out += ["", "## Figure construction", "", "| Figure type | Poster / priority count | Median page | Median width/page | Median aspect | Caption words | Takeaway % |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    for ftype, audiences in sorted(summary["visuals"].get("figure", {}).items(), key=lambda kv: -sum(x.get("count", 0) for x in kv[1].values())):
        p, q = audiences.get("poster", {}), audiences.get("priority", {})
        def pair(field):
            return f'{p.get(field, {}).get("median", "-")} / {q.get(field, {}).get("median", "-")}'
        out.append(
            f'| {ftype} | {p.get("count",0):,} / {q.get("count",0):,} | {pair("page")} | '
            f'{pair("width_page_fraction")} | {pair("aspect_ratio")} | {pair("caption_words")} | '
            f'{p.get("takeaway_pct","-")} / {q.get("takeaway_pct","-")} |'
        )
    out += ["", "First-figure roles:", ""]
    for ftype, count in summary["first_figure_types"][:12]:
        out.append(f"- {ftype}: {count:,}")

    out += ["", "## Table construction", "", "| Table role | Poster / priority count | Median page | Caption words | Protocol % | Comparison % |",
            "|---|---:|---:|---:|---:|---:|"]
    for ftype, audiences in sorted(summary["visuals"].get("table", {}).items(), key=lambda kv: -sum(x.get("count", 0) for x in kv[1].values())):
        p, q = audiences.get("poster", {}), audiences.get("priority", {})
        def table_pair(field):
            return f'{p.get(field, {}).get("median", "-")} / {q.get(field, {}).get("median", "-")}'
        out.append(
            f'| {ftype} | {p.get("count",0):,} / {q.get("count",0):,} | {table_pair("page")} | '
            f'{table_pair("caption_words")} | {p.get("protocol_pct","-")} / {q.get("protocol_pct","-")} | '
            f'{p.get("comparison_pct","-")} / {q.get("comparison_pct","-")} |'
        )

    out += [
        "", "## How to use the figure evidence", "",
        "- Make Figure 1 carry the problem contrast, central mechanism, or end-to-end promise.",
        "- Use architecture figures to show input-to-output flow, stage boundaries, train/test differences, and the claimed novelty.",
        "- Use qualitative grids with fixed rows/columns, identical crops, visible failure cases, and captions that state the comparison protocol.",
        "- Use quantitative plots for one question per panel; expose uncertainty, axes, units, and compute/data conditions.",
        "- Use ablations to map one visual intervention to one method claim; avoid panels that merely repeat the main table.",
        "- Use table groups and protocol columns to expose which numbers are genuinely comparable; bold only within valid groups.",
        "- Treat the median dimensions above as diagnostics, not templates. The scientific question determines the layout.",
        "", "## Files", "",
        "- `summary.json`: machine-readable aggregates",
        "- `figures.jsonl.gz`: one row per detected figure/table with caption and visual features",
        "- `sections.jsonl.gz`: one row per detected section with writing features",
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--database", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.database)
    summary = build_summary(conn)
    export_rows(conn, args.output_dir)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "full-corpus-report.md").write_text(render_markdown(summary), encoding="utf-8")
    conn.close()
    print(json.dumps({
        "papers_analyzed": summary["papers_analyzed"],
        "priority_papers_analyzed": summary["priority_papers_analyzed"],
        "output_dir": str(args.output_dir),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
