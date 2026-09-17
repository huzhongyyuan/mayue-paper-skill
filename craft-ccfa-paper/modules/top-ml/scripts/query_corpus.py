#!/usr/bin/env python3
"""Search the bundled/current paper metadata without loading it into context."""

import argparse
import gzip
import json
import re
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--query", default="", help="Case-insensitive title/author regex")
    ap.add_argument("--conference", choices=["CVPR", "ICCV", "ECCV", "NeurIPS", "ICML"])
    ap.add_argument("--year", type=int)
    ap.add_argument("--presentation", choices=["poster", "spotlight", "highlight", "oral"])
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()
    pattern = re.compile(args.query, re.I) if args.query else None
    shown = 0
    opener = gzip.open if args.corpus.suffix == ".gz" else open
    with opener(args.corpus, "rt", encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if args.conference and row["conference"] != args.conference:
                continue
            if args.year and row["year"] != args.year:
                continue
            if args.presentation and row.get("presentation") != args.presentation:
                continue
            haystack = row["title"] + " " + " ".join(row.get("authors", []))
            if pattern and not pattern.search(haystack):
                continue
            print(json.dumps({
                "conference": row["conference"], "year": row["year"],
                "presentation": row.get("presentation"), "title": row["title"],
                "paper_url": row.get("paper_url"), "pdf_url": row.get("pdf_url"),
            }, ensure_ascii=False))
            shown += 1
            if shown >= args.limit:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
