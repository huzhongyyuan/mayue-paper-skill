#!/usr/bin/env python3
"""Fail-closed structural audit for a craft-ccfa-paper workspace.

This checks records, mappings, file presence, and obvious placeholders. It does not
verify scientific truth, citation entailment, novelty, statistics, or venue compliance.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|MISSING|UNVERIFIED|PLACEHOLDER|CITATION\s+NEEDED)\b",
    re.IGNORECASE,
)
BIB_KEY = re.compile(r"@[A-Za-z]+\s*\{\s*([^,\s]+)")
CLAIM_ID = re.compile(r"^C\d{3,}$")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


class Audit:
    def __init__(self, root: Path, final: bool) -> None:
        self.root = root
        self.final = final
        self.findings: list[Finding] = []
        self.claim_ids: set[str] = set()
        self.evidence_ids: set[str] = set()

    def add(self, severity: str, code: str, path: Path | str, message: str) -> None:
        try:
            shown = str(Path(path).resolve().relative_to(self.root))
        except (ValueError, TypeError):
            shown = str(path)
        self.findings.append(Finding(severity, code, shown, message))

    def load_json(self, relative: str) -> dict[str, Any] | None:
        path = self.root / relative
        if not path.is_file():
            self.add("blocker", "FILE_MISSING", path, "required JSON file is missing")
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.add("blocker", "JSON_INVALID", path, f"cannot parse JSON: {exc}")
            return None
        if not isinstance(data, dict):
            self.add("blocker", "JSON_ROOT", path, "JSON root must be an object")
            return None
        return data

    def load_csv(self, relative: str, required: set[str]) -> list[dict[str, str]]:
        path = self.root / relative
        if not path.is_file():
            self.add("blocker", "FILE_MISSING", path, "required CSV file is missing")
            return []
        try:
            with path.open(newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                fields = set(reader.fieldnames or [])
                missing = required - fields
                if missing:
                    self.add(
                        "blocker",
                        "CSV_COLUMNS",
                        path,
                        "missing columns: " + ", ".join(sorted(missing)),
                    )
                    return []
                return [dict(row) for row in reader]
        except (OSError, UnicodeError, csv.Error) as exc:
            self.add("blocker", "CSV_INVALID", path, f"cannot parse CSV: {exc}")
            return []

    def check_value(self, value: Any, path: Path, field: str, *, final_only: bool = False) -> None:
        if final_only and not self.final:
            return
        text = "" if value is None else str(value).strip()
        if not text or PLACEHOLDER.search(text):
            severity = "blocker" if self.final else "major"
            self.add(severity, "VALUE_UNRESOLVED", path, f"unresolved field: {field}")

    def resolve_declared(self, raw: str) -> Path:
        candidate = Path(raw)
        return candidate if candidate.is_absolute() else self.root / candidate

    def check_declared_paths(
        self, values: Iterable[Any], manifest_path: Path, field: str, *, require_one: bool = False
    ) -> None:
        paths = [str(value).strip() for value in values if str(value).strip()]
        if require_one and not paths:
            self.add("blocker" if self.final else "major", "PATHS_EMPTY", manifest_path, f"{field} is empty")
        for raw in paths:
            path = self.resolve_declared(raw)
            if not path.exists():
                self.add("blocker" if self.final else "major", "PATH_MISSING", path, f"declared by {field}")

    def audit_manifest(self) -> None:
        path = self.root / "project_manifest.json"
        data = self.load_json("project_manifest.json")
        if data is None:
            return
        venue = data.get("venue") if isinstance(data.get("venue"), dict) else {}
        story = data.get("story") if isinstance(data.get("story"), dict) else {}
        confidentiality = data.get("confidentiality") if isinstance(data.get("confidentiality"), dict) else {}
        artifacts = data.get("artifacts") if isinstance(data.get("artifacts"), dict) else {}
        for field, value in (
            ("project_id", data.get("project_id")),
            ("title", data.get("title")),
            ("venue.name", venue.get("name")),
            ("venue.rules_url", venue.get("rules_url")),
            ("venue.rules_accessed", venue.get("rules_accessed")),
            ("story.problem", story.get("problem")),
            ("story.one_sentence_contribution", story.get("one_sentence_contribution")),
            ("story.intended_takeaway", story.get("intended_takeaway")),
            ("confidentiality.classification", confidentiality.get("classification")),
        ):
            self.check_value(value, path, field, final_only=field.startswith("venue.") or field.startswith("story."))
        if self.final and data.get("status") not in {"submission_candidate", "camera_ready"}:
            self.add("blocker", "STATUS_NOT_FINAL", path, "status must be submission_candidate or camera_ready")
        if self.final and data.get("accountable_human_approval") is not True:
            self.add("blocker", "HUMAN_APPROVAL", path, "accountable_human_approval must be true")
        if self.final:
            compiled = artifacts.get("compiled_pdfs") if isinstance(artifacts.get("compiled_pdfs"), list) else []
            self.check_declared_paths(
                compiled,
                path,
                "artifacts.compiled_pdfs",
                require_one=True,
            )

    def audit_claims(self) -> None:
        path = self.root / "claims.csv"
        rows = self.load_csv(
            "claims.csv",
            {"claim_id", "statement", "claim_type", "scope", "falsifier", "evidence_ids", "status"},
        )
        if not rows:
            self.add("blocker", "CLAIMS_EMPTY", path, "at least one claim is required")
            return
        for index, row in enumerate(rows, start=2):
            cid = (row.get("claim_id") or "").strip()
            if not CLAIM_ID.match(cid):
                self.add("blocker", "CLAIM_ID", path, f"row {index}: invalid claim_id")
                continue
            if cid in self.claim_ids:
                self.add("blocker", "CLAIM_DUPLICATE", path, f"row {index}: duplicate {cid}")
            self.claim_ids.add(cid)
            for field in ("statement", "claim_type", "scope", "falsifier"):
                self.check_value(row.get(field), path, f"row {index}.{field}", final_only=True)
            evidence = [part.strip() for part in (row.get("evidence_ids") or "").split(";") if part.strip()]
            self.evidence_ids.update(evidence)
            if self.final and not evidence:
                self.add("blocker", "CLAIM_NO_EVIDENCE", path, f"{cid} has no evidence_ids")
            if self.final and (row.get("status") or "").strip() not in {"supported", "qualified"}:
                self.add("blocker", "CLAIM_STATUS", path, f"{cid} is not supported or qualified")

    def audit_experiments(self) -> None:
        path = self.root / "experiments/experiment_registry.csv"
        rows = self.load_csv(
            "experiments/experiment_registry.csv",
            {"experiment_id", "question", "claim_ids", "baselines", "metrics", "raw_result_paths", "status"},
        )
        seen: set[str] = set()
        for index, row in enumerate(rows, start=2):
            eid = (row.get("experiment_id") or "").strip()
            if not eid or eid in seen:
                self.add("blocker", "EXPERIMENT_ID", path, f"row {index}: missing or duplicate experiment_id")
            seen.add(eid)
            linked = {part.strip() for part in (row.get("claim_ids") or "").split(";") if part.strip()}
            unknown = linked - self.claim_ids
            if unknown:
                self.add("blocker", "EXPERIMENT_CLAIM", path, f"{eid} links unknown claims: {', '.join(sorted(unknown))}")
            if self.final and not linked:
                self.add("major", "EXPERIMENT_ORPHAN", path, f"{eid} supports no claim")
            for field in ("question", "baselines", "metrics"):
                self.check_value(row.get(field), path, f"row {index}.{field}", final_only=True)
            raw_paths = [part.strip() for part in (row.get("raw_result_paths") or "").split(";") if part.strip()]
            if self.final:
                self.check_declared_paths(raw_paths, path, f"{eid}.raw_result_paths", require_one=True)
                if (row.get("status") or "").strip() not in {"complete", "documented", "not_applicable"}:
                    self.add("blocker", "EXPERIMENT_STATUS", path, f"{eid} is not complete/documented")

    def audit_figures(self) -> None:
        path = self.root / "figures/figure_manifest.json"
        data = self.load_json("figures/figure_manifest.json")
        if data is None:
            return
        figures = data.get("figures")
        if not isinstance(figures, list):
            self.add("blocker", "FIGURES_TYPE", path, "figures must be an array")
            return
        seen: set[str] = set()
        for index, figure in enumerate(figures):
            if not isinstance(figure, dict):
                self.add("blocker", "FIGURE_ENTRY", path, f"figure {index} must be an object")
                continue
            fid = str(figure.get("figure_id") or "").strip()
            if not fid or fid in seen:
                self.add("blocker", "FIGURE_ID", path, f"figure {index} has missing or duplicate figure_id")
            seen.add(fid)
            linked = {str(x).strip() for x in figure.get("claim_ids", []) if str(x).strip()}
            unknown = linked - self.claim_ids
            if unknown:
                self.add("blocker", "FIGURE_CLAIM", path, f"{fid} links unknown claims: {', '.join(sorted(unknown))}")
            for field in ("title", "reader_question", "intended_inference", "kind"):
                self.check_value(figure.get(field), path, f"{fid}.{field}", final_only=True)
            sources = figure.get("source_paths") if isinstance(figure.get("source_paths"), list) else []
            outputs = figure.get("outputs") if isinstance(figure.get("outputs"), list) else []
            editable = figure.get("editable_outputs") if isinstance(figure.get("editable_outputs"), list) else []
            generator = str(figure.get("generator_path") or "").strip()
            kind = str(figure.get("kind") or "").lower()
            if self.final:
                self.check_declared_paths(sources, path, f"{fid}.source_paths", require_one=True)
                self.check_declared_paths(outputs, path, f"{fid}.outputs", require_one=True)
                if generator:
                    self.check_declared_paths([generator], path, f"{fid}.generator_path")
                else:
                    self.add("blocker", "FIGURE_GENERATOR", path, f"{fid} has no generator_path")
                if kind in {"plot", "diagram", "architecture", "workflow", "table"}:
                    self.check_declared_paths(editable, path, f"{fid}.editable_outputs", require_one=True)
                for review_field in ("caption_status", "semantic_review", "visual_review"):
                    if str(figure.get(review_field) or "").strip() not in {"complete", "passed", "approved"}:
                        self.add("blocker", "FIGURE_REVIEW", path, f"{fid}.{review_field} is not complete/passed")

    def audit_layout(self) -> None:
        path = self.root / "paper/layout_plan.csv"
        rows = self.load_csv(
            "paper/layout_plan.csv",
            {
                "page_or_range",
                "section",
                "reader_question",
                "claim_ids",
                "target_pages",
                "planned_visuals",
                "float_width",
                "entry_state",
                "exit_state",
                "status",
                "notes",
            },
        )
        if not rows:
            self.add("blocker", "LAYOUT_EMPTY", path, "at least one page-plan row is required")
            return
        for index, row in enumerate(rows, start=2):
            linked = {
                part.strip()
                for part in (row.get("claim_ids") or "").split(";")
                if part.strip()
            }
            unknown = linked - self.claim_ids
            if unknown:
                self.add(
                    "blocker",
                    "LAYOUT_CLAIM",
                    path,
                    f"row {index} links unknown claims: {', '.join(sorted(unknown))}",
                )
            if self.final:
                for field in (
                    "page_or_range",
                    "section",
                    "reader_question",
                    "target_pages",
                    "entry_state",
                    "exit_state",
                ):
                    self.check_value(row.get(field), path, f"row {index}.{field}")
                try:
                    target_pages = float((row.get("target_pages") or "").strip())
                except ValueError:
                    target_pages = 0.0
                if target_pages <= 0:
                    self.add(
                        "blocker",
                        "LAYOUT_BUDGET",
                        path,
                        f"row {index}.target_pages must be a positive number",
                    )
                if (row.get("status") or "").strip() not in {"audited", "not_applicable"}:
                    self.add(
                        "blocker",
                        "LAYOUT_STATUS",
                        path,
                        f"row {index}.status must be audited or not_applicable in final mode",
                    )

    def audit_text_artifacts(self) -> None:
        candidates = list((self.root / "paper").rglob("*.tex")) + list((self.root / "paper").rglob("*.md"))
        candidates += list((self.root / "slides").rglob("*.md"))
        for path in sorted(set(candidates)):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.add("major", "TEXT_READ", path, f"cannot read text artifact: {exc}")
                continue
            if PLACEHOLDER.search(text):
                self.add("blocker" if self.final else "major", "TEXT_PLACEHOLDER", path, "contains unresolved placeholder text")

        bibs = list(self.root.rglob("*.bib"))
        for path in bibs:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.add("major", "BIB_READ", path, f"cannot read bibliography: {exc}")
                continue
            if PLACEHOLDER.search(text):
                self.add("blocker" if self.final else "major", "BIB_PLACEHOLDER", path, "contains unresolved bibliography placeholder")
            keys = BIB_KEY.findall(text)
            duplicates = sorted({key for key in keys if keys.count(key) > 1})
            if duplicates:
                self.add("blocker", "BIB_DUPLICATE", path, "duplicate keys: " + ", ".join(duplicates))

    def run(self) -> list[Finding]:
        self.audit_manifest()
        self.audit_claims()
        self.audit_experiments()
        self.audit_figures()
        self.audit_layout()
        self.audit_text_artifacts()
        rank = {"blocker": 0, "major": 1, "minor": 2, "suggestion": 3}
        return sorted(self.findings, key=lambda item: (rank.get(item.severity, 9), item.path, item.code))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--final", action="store_true", help="Apply submission-candidate gates")
    parser.add_argument("--json", type=Path, dest="json_output", help="Write a machine-readable report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.workspace.expanduser().resolve()
    if not root.is_dir():
        print(f"error: workspace is not a directory: {root}", file=sys.stderr)
        return 2

    audit = Audit(root, args.final)
    findings = audit.run()
    counts = {severity: sum(item.severity == severity for item in findings) for severity in ("blocker", "major", "minor", "suggestion")}
    report = {
        "workspace": str(root),
        "mode": "final" if args.final else "working",
        "disclaimer": "Structural audit only; not scientific or venue certification.",
        "counts": counts,
        "findings": [asdict(item) for item in findings],
    }
    if args.json_output:
        target = args.json_output.expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for item in findings:
        print(f"[{item.severity.upper()}] {item.code} {item.path}: {item.message}")
    print("summary: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    print("note: this audit does not verify truth, citation support, novelty, statistics, or venue compliance")
    return 1 if counts["blocker"] or (args.final and counts["major"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
