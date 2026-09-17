#!/usr/bin/env python3
"""Create a provenance-first CCF-A paper workspace without overwriting files."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"

FILES = {
    "project_manifest.template.json": "project_manifest.json",
    "claims.template.csv": "claims.csv",
    "experiment_registry.template.csv": "experiments/experiment_registry.csv",
    "figure_manifest.template.json": "figures/figure_manifest.json",
    "diagram_spec.example.json": "figures/specs/method.example.json",
    "layout_plan.template.csv": "paper/layout_plan.csv",
}

DIRECTORIES = (
    "literature",
    "experiments/configs",
    "experiments/logs",
    "results/raw",
    "results/processed",
    "figures/scripts",
    "figures/data",
    "figures/rendered",
    "paper/sections",
    "reviews",
    "slides",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path, help="Workspace directory to create")
    parser.add_argument(
        "--into-existing",
        action="store_true",
        help="Allow an existing directory, but still refuse to overwrite any file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.workspace.expanduser().resolve()

    if root.exists() and not args.into_existing:
        print(f"error: target already exists: {root}", file=sys.stderr)
        print("use --into-existing only after inspecting the directory", file=sys.stderr)
        return 2

    conflicts = [root / dest for dest in FILES.values() if (root / dest).exists()]
    references_bib = root / "literature/references.bib"
    search_protocol = root / "literature/search_protocol.md"
    if references_bib.exists():
        conflicts.append(references_bib)
    if search_protocol.exists():
        conflicts.append(search_protocol)
    if conflicts:
        print("error: refusing to overwrite:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        return 2

    root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)

    for source_name, destination in FILES.items():
        source = ASSETS_DIR / source_name
        if not source.is_file():
            print(f"error: bundled asset missing: {source}", file=sys.stderr)
            return 2
        target = root / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    references_bib.write_text(
        "% Add only programmatically retrieved and manually verified entries.\n",
        encoding="utf-8",
    )
    search_protocol.write_text(
        "# Literature search protocol\n\n"
        "- Topic and scope: TODO\n"
        "- Date window: TODO\n"
        "- Sources and access dates: TODO\n"
        "- Query families: TODO\n"
        "- Inclusion/exclusion rules: TODO\n"
        "- Citation chaining: TODO\n"
        "- Deduplication key: DOI, then normalized title\n"
        "- Stop condition and known coverage gaps: TODO\n",
        encoding="utf-8",
    )

    print(f"initialized: {root}")
    print("next: complete project_manifest.json and claims.csv before drafting")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
