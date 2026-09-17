#!/usr/bin/env python3
"""Resumable streaming analysis of every accessible paper PDF in a corpus.

The analyzer downloads a PDF into a temporary directory, extracts section and
figure/table features, writes compact rows to SQLite, and discards the PDF by
default. It never treats future, absent, or anti-bot-blocked papers as analyzed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

try:
    import fitz  # PyMuPDF
    import numpy as np
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Install full-corpus dependencies first: "
        "python3 -m pip install -r scripts/requirements-full-corpus.txt"
    ) from exc


ANALYZER_VERSION = "2.6"
USER_AGENT = "write-top-ml-paper/2.6 (academic metadata and structure analysis)"
PRIORITY_ORDER = {"oral": 0, "highlight": 1, "spotlight": 2, "poster": 3}

SECTION_RULES = [
    ("abstract", r"^abstract$"),
    ("introduction", r"\bintroduction\b"),
    ("related_work", r"\b(related works?|literature review|prior works?)\b"),
    ("background", r"\b(background|preliminar(?:y|ies)|problem setup|problem formulation|notation)\b"),
    ("method", r"\b(methods?|methodology|approach|framework|architecture|model|algorithm|system|training|mechanism)\b"),
    ("theory", r"\b(theory|theoretical|proof|guarantee|convergence|regret bound)\b"),
    ("data", r"\b(dataset|benchmark|data collection|annotation)\b"),
    ("experiments", r"\b(experiments?|evaluation|empirical|results?|ablation|implementation)\b"),
    ("limitations", r"\b(limitations?|failure cases?|broader impact|societal impact|ethics)\b"),
    ("conclusion", r"\b(conclusions?|discussion|summary)\b"),
    ("references", r"^references$"),
    ("appendix", r"^(appendix|supplementary material|supplement)\b"),
]

FIGURE_RULES = [
    ("failure_case", r"\b(failure|limitation|error case|negative result)\b"),
    ("ablation_sensitivity", r"\b(ablation|sensitivity|effect of|impact of|component analysis)\b"),
    ("architecture_pipeline", r"\b(overview|architecture|pipeline|framework|workflow|training pipeline|inference pipeline)\b"),
    ("qualitative_comparison", r"\b(qualitative|visual comparison|visual results?|comparison with|compared with)\b"),
    ("quantitative_plot", r"\b(curve|plot|accuracy|performance|scaling|trade[- ]?off|latency|throughput|memory|convergence|loss)\b"),
    ("dataset_examples", r"\b(dataset|samples?|examples?|data collection|annotation)\b"),
    ("representation_visualization", r"\b(attention|feature map|activation|embedding|latent|t-sne|umap|heatmap)\b"),
    ("motivation_teaser", r"\b(teaser|motivation|intuition|illustration|concept)\b"),
]


def iter_corpus(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def paper_id(record: dict) -> str:
    raw = f'{record["conference"]}|{record["year"]}|{record["title"]}'
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*|\d+(?:\.\d+)?", text)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s.strip()]


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", " ")).strip()


def section_category(heading: str) -> str:
    plain = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[IVX]+)\s*[.:|]?\s*", "", heading, flags=re.I)
    plain = normalize_space(plain).lower()
    for category, rule in SECTION_RULES:
        if re.search(rule, plain, re.I):
            return category
    return "other"


def classify_figure(caption: str, page: int, label: str, visual: dict) -> str:
    low = caption.lower()
    for category, rule in FIGURE_RULES:
        if re.search(rule, low, re.I):
            return category
    if page == 1 and re.search(r"(?:fig(?:ure)?\.?\s*)?1\b", label, re.I):
        return "motivation_teaser"
    if visual.get("white_fraction", 0) > 0.72 and visual.get("edge_density", 0) > 0.02:
        return "diagram_or_plot"
    if visual.get("colorfulness", 0) > 0.12:
        return "visual_examples"
    return "other"


def block_text(block: dict) -> tuple[str, float, bool, int]:
    lines, first_sizes, first_bold, span_count = [], [], False, 0
    for line_index, line in enumerate(block.get("lines", [])):
        pieces = []
        for span in line.get("spans", []):
            pieces.append(span.get("text", ""))
            if line_index == 0:
                first_sizes.append(float(span.get("size", 0)))
                font = str(span.get("font", "")).lower()
                first_bold = first_bold or "bold" in font
            span_count += 1
        lines.append("".join(pieces))
    return "\n".join(lines).strip(), (max(first_sizes) if first_sizes else 0.0), first_bold, span_count


def split_text_block(block: dict) -> list[tuple[str, float, bool, int, list[float]]]:
    """Split PDF text blocks that contain multiple top-level sections.

    Some publishers merge a complete column into one block, including lines
    such as ``2. Related Work`` and ``3. Method``. Section detection must see
    each of those as a separate block while retaining the intervening body.
    """
    lines = []
    for line in block.get("lines", []):
        spans = line.get("spans", [])
        text = "".join(span.get("text", "") for span in spans).strip()
        if not text:
            continue
        sizes = [float(span.get("size", 0)) for span in spans if span.get("size", 0)]
        size = max(sizes) if sizes else 0.0
        bold = any("bold" in str(span.get("font", "")).lower() for span in spans)
        bbox = list(line.get("bbox", block.get("bbox", (0, 0, 0, 0))))
        lines.append({"text": text, "size": size, "bold": bold, "spans": len(spans), "bbox": bbox})
    if not lines:
        return []

    body_candidates = [item["size"] for item in lines if len(words(item["text"])) >= 5 and item["size"] > 0]
    local_body = float(np.median(body_candidates)) if body_candidates else max(1.0, lines[0]["size"])
    canonical = re.compile(
        r"^(abstract|introduction|related works?|background|preliminaries|method|methodology|"
        r"approach|experiments?|evaluation|results?|limitations?|discussion|conclusions?|"
        r"references|appendix|supplementary material)$", re.I,
    )
    top_numbered = re.compile(
        r"^\s*(?:\d+|[IVXivx]+)(?:\s*[.:|]\s*|\s+)[A-Z][^\n]{1,99}$"
    )

    groups, current = [], []
    for item in lines:
        plain = normalize_space(item["text"])
        short = len(plain) <= 110 and len(words(plain)) <= 15
        is_heading = short and (canonical.match(plain) or top_numbered.match(plain))
        typography = item["size"] >= local_body * 1.10 or (item["bold"] and item["size"] >= local_body)
        if current and is_heading and typography:
            groups.append(current)
            current = []
        current.append(item)
    if current:
        groups.append(current)

    packed = []
    for group in groups:
        rect = fitz.Rect(group[0]["bbox"])
        for item in group[1:]:
            rect |= fitz.Rect(item["bbox"])
        packed.append((
            "\n".join(item["text"] for item in group),
            group[0]["size"], group[0]["bold"],
            sum(item["spans"] for item in group), list(rect),
        ))
    return packed


def reading_order(page_text_blocks: list[dict], page_rect) -> list[dict]:
    """Approximate scientific two-column reading order for one page."""
    page_w = page_rect.width
    wide, narrow = [], []
    for block in page_text_blocks:
        rect = fitz.Rect(block["bbox"])
        centered = abs((rect.x0 + rect.x1) / 2 - (page_rect.x0 + page_rect.x1) / 2) < page_w * 0.12
        # A short right-column heading can sit close to the page center. Treating
        # every centered block as a full-width separator moves that heading ahead
        # of the left column (e.g. Introduction before Abstract on CVPR page 1).
        if rect.width >= page_w * 0.45 or (centered and rect.width >= page_w * 0.25):
            wide.append(block)
        else:
            narrow.append(block)

    def columns(items):
        left = [b for b in items if b["bbox"][0] + b["bbox"][2] <= page_rect.x0 * 2 + page_w]
        right = [b for b in items if b not in left]
        key = lambda b: (b["bbox"][1], b["bbox"][0])
        return sorted(left, key=key) + sorted(right, key=key)

    result, remaining = [], list(narrow)
    for separator in sorted(wide, key=lambda b: (b["bbox"][1], b["bbox"][0])):
        before = [b for b in remaining if (b["bbox"][1] + b["bbox"][3]) / 2 < separator["bbox"][1]]
        result.extend(columns(before))
        before_ids = {id(b) for b in before}
        remaining = [b for b in remaining if id(b) not in before_ids]
        result.append(separator)
    result.extend(columns(remaining))
    return result


def find_headings(blocks: list[dict]) -> list[dict]:
    body_sizes = [b["font_size"] for b in blocks if len(words(b["text"])) >= 20 and b["font_size"] > 0]
    # References are often one point smaller and can dominate the block count.
    # A modest upper quantile better estimates main-text size without assuming a
    # venue-specific template, and rejects numbered list items as headings.
    body_size = float(np.percentile(body_sizes, 60)) if body_sizes else 9.0
    headings = []
    for idx, block in enumerate(blocks):
        raw = block["text"].strip()
        if not raw:
            continue
        first, *rest = raw.splitlines()
        first = normalize_space(first)
        if re.match(r"^(?:\d+(?:\.\d+)*|[IVX]+)$", first, re.I) and rest:
            first = f"{first}. {normalize_space(rest.pop(0))}"
        key = re.sub(r"[^a-z ]+", "", first.lower()).strip()
        numbered = re.match(
            r"^\s*((?:\d+(?:\.\d+)*)|(?:[IVXivx]+))(?:\s*[.:|]\s*|\s+)([A-Z][^\n]{1,99})$",
            first,
        )
        level = 0
        if numbered:
            token = numbered.group(1)
            level = token.count(".") + 1 if token[0].isdigit() else 1
        exact = bool(re.match(
            r"^(abstract|introduction|related work|background|preliminaries|method|methodology|"
            r"approach|experiments?|evaluation|results?|limitations?|discussion|conclusions?|"
            r"references|appendix|supplementary material)$", key,
        ))
        short = len(first) <= 110 and len(words(first)) <= 15
        typography = (
            block["font_size"] >= body_size * 1.10 or
            (block["bold"] and block["font_size"] >= body_size * 1.05)
        )
        always_unnumbered = key in {"abstract", "references", "appendix", "supplementary material"}
        special_unnumbered = key in {"limitations", "limitation", "broader impact", "societal impact", "conclusion", "discussion"}
        exact_ok = (always_unnumbered and block["font_size"] >= body_size * 1.05) or (
            special_unnumbered and exact and typography and block["font_size"] >= body_size * 1.12
        )
        if not short or not (exact_ok or (numbered and typography)):
            continue
        # Keep top-level headings and explicit unnumbered canonical headings.
        if numbered and level > 1:
            continue
        inline_body = normalize_space(" ".join(rest))
        headings.append({
            "block_index": idx,
            "heading": first,
            "category": section_category(first),
            "page": block["page"],
            "inline_body": inline_body,
            "font_size": block["font_size"],
        })
    # Remove adjacent duplicates produced by two-column extraction or running headers.
    clean = []
    last_main_number = 0
    seen_abstract_heading = False
    for h in headings:
        if clean and h["heading"].lower() == clean[-1]["heading"].lower() and h["page"] == clean[-1]["page"]:
            continue
        if h["category"] == "abstract":
            seen_abstract_heading = True
        number_match = re.match(r"^\s*(\d+)(?:\D|$)", h["heading"])
        if number_match:
            number = int(number_match.group(1))
            # Numbered affiliations such as "1 University ..." appear before
            # Abstract, and equation/list fragments can carry large integers.
            if (h["page"] == 1 and not seen_abstract_heading and h["category"] == "other") or number > 20:
                continue
            if number <= last_main_number:
                continue
            last_main_number = number
        clean.append(h)
    seen_references = False
    seen_experiments = False
    for h in clean:
        if seen_references and h["category"] != "references":
            h["category"] = "appendix"
        if h["category"] == "references":
            seen_references = True
        if h["category"] == "experiments":
            seen_experiments = True
        if h["category"] == "other" and not seen_experiments and not seen_references:
            match = re.match(r"^\s*(\d+)", h["heading"])
            if match and int(match.group(1)) >= 3:
                h["category"] = "method"
    return clean


def rhetorical_roles(text: str) -> dict:
    firsts = []
    for para in re.split(r"\n\s*\n", text):
        ss = sentences(normalize_space(para))
        if ss:
            firsts.append(ss[0].lower())
    joined = "\n".join(firsts)
    return {
        "context_motivation": len(re.findall(r"\b(important|fundamental|central|widely|recent advances?|plays? a (?:key|critical) role)\b", joined)),
        "gap_challenge": len(re.findall(r"\b(however|yet|despite|challenge|limitation|remain(?:s)?|fail(?:s|ed)? to)\b", joined)),
        "proposal": len(re.findall(r"\b(we propose|we introduce|we present|we develop|our method|this work)\b", joined)),
        "mechanism": len(re.findall(r"\b(by|through|via|enables?|allows?|leverag(?:e|es|ing))\b", joined)),
        "evidence": len(re.findall(r"\b(experiments?|results?|evaluation|outperform|improv(?:e|es|ed))\b", joined)),
        "boundary": len(re.findall(r"\b(limitation|failure|only|assume|restricted|future work|does not|cannot)\b", joined)),
        "contribution": len(re.findall(r"\b(contribution|we make|we show|we prove|we demonstrate)\b", joined)),
    }


def section_features(text: str, paragraph_count: int) -> dict:
    toks = words(text)
    ss = sentences(normalize_space(text))
    return {
        "word_count": len(toks),
        "sentence_count": len(ss),
        "paragraph_count": paragraph_count,
        "avg_sentence_words": round(len(toks) / max(1, len(ss)), 2),
        "citation_mentions": len(re.findall(r"\[[0-9,; –-]+\]|\([A-Z][A-Za-z-]+ et al\.,? \d{4}\)", text)),
        "figure_mentions": len(re.findall(r"\bFig(?:ure)?\.?\s*\d+", text, re.I)),
        "table_mentions": len(re.findall(r"\bTable\s*\d+", text, re.I)),
        "equation_mentions": len(re.findall(r"\bEq(?:uation)?\.?\s*\(?\d+\)?", text, re.I)),
        "first_person_mentions": len(re.findall(r"\b(we|our|ours)\b", text, re.I)),
        "hedge_mentions": len(re.findall(r"\b(may|might|could|suggests?|appears?|approximately|typically)\b", text, re.I)),
        "strong_claim_mentions": len(re.findall(r"\b(prove|guarantee|always|never|state[- ]of[- ]the[- ]art|significant(?:ly)?|superior|universal)\b", text, re.I)),
        "contribution_cues": len(re.findall(r"\b(our contributions?|we (?:make|introduce|propose|show|demonstrate|develop|present))\b", text, re.I)),
        "limitation_cues": len(re.findall(r"\b(limitations?|failure cases?|future work|does not|cannot|remain(?:s)? challenging)\b", text, re.I)),
        "role_counts": rhetorical_roles(text),
    }


def infer_visual_bbox(page_rect, caption_bbox, image_bboxes, text_blocks):
    cap = fitz.Rect(caption_bbox)
    page_w, page_h = page_rect.width, page_rect.height
    candidates = []
    for raw in image_bboxes:
        rect = fitz.Rect(raw)
        overlap = max(0.0, min(rect.x1, cap.x1) - max(rect.x0, cap.x0))
        overlap_ratio = overlap / max(1.0, min(rect.width, cap.width))
        above = rect.y1 <= cap.y0 + 8 and cap.y0 - rect.y0 <= page_h * 0.7
        below = rect.y0 >= cap.y1 - 8 and rect.y1 - cap.y1 <= page_h * 0.5
        if overlap_ratio >= 0.15 and (above or below):
            candidates.append(rect)
    if candidates:
        rect = candidates[0]
        for other in candidates[1:]:
            rect |= other
        return rect & page_rect, "image_bbox"

    # Vector diagrams and plots often have no image object. Estimate the column
    # above the caption, bounded by nearby text, then render that region.
    if cap.width >= page_w * 0.58:
        x0, x1, layout = page_rect.x0, page_rect.x1, "full_width"
    elif cap.x0 + cap.x1 < page_w:
        x0, x1, layout = page_rect.x0, page_rect.x0 + page_w / 2, "single_column"
    else:
        x0, x1, layout = page_rect.x0 + page_w / 2, page_rect.x1, "single_column"
    y1 = cap.y0
    y0 = max(page_rect.y0, y1 - page_h * 0.42)
    previous_bottoms = []
    for block in text_blocks:
        b = fitz.Rect(block["bbox"])
        if b.y1 < cap.y0 - 10 and min(b.x1, x1) - max(b.x0, x0) > 10:
            previous_bottoms.append(b.y1)
    if previous_bottoms:
        nearest = max(previous_bottoms)
        if cap.y0 - nearest < page_h * 0.38:
            y0 = nearest + 3
    return fitz.Rect(x0, y0, x1, y1) & page_rect, layout


def visual_features(page, rect, text_blocks) -> dict:
    if rect.is_empty or rect.width < 5 or rect.height < 5:
        return {"bbox_source": "empty"}
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=rect, alpha=False, colorspace=fitz.csRGB)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3]
    gray = arr.mean(axis=2)
    dx = np.abs(np.diff(gray.astype(np.int16), axis=1)) if arr.shape[1] > 1 else np.zeros((1, 1))
    dy = np.abs(np.diff(gray.astype(np.int16), axis=0)) if arr.shape[0] > 1 else np.zeros((1, 1))
    edge_density = (float((dx > 28).mean()) + float((dy > 28).mean())) / 2
    text_spans = 0
    for block in text_blocks:
        if fitz.Rect(block["bbox"]).intersects(rect):
            text_spans += block.get("span_count", 0)
    return {
        "width_px": int(pix.width),
        "height_px": int(pix.height),
        "aspect_ratio": round(rect.width / max(1.0, rect.height), 3),
        "width_page_fraction": round(rect.width / page.rect.width, 3),
        "height_page_fraction": round(rect.height / page.rect.height, 3),
        "colorfulness": round(float((arr.max(axis=2) - arr.min(axis=2)).mean() / 255.0), 4),
        "contrast": round(float(gray.std() / 255.0), 4),
        "white_fraction": round(float((gray > 246).mean()), 4),
        "edge_density": round(edge_density, 4),
        "text_span_count": int(text_spans),
    }


def caption_signals(caption: str) -> dict:
    subs = sorted(set(re.findall(r"\(([a-z])\)", caption.lower())))
    return {
        "word_count": len(words(caption)),
        "sentence_count": len(sentences(caption)),
        "subfigure_count": len(subs),
        "has_takeaway": bool(re.search(r"\b(shows?|demonstrates?|outperforms?|improves?|reveals?|indicates?)\b", caption, re.I)),
        "has_comparison": bool(re.search(r"\b(compare|comparison|versus|vs\.?|baseline|ours)\b", caption, re.I)),
        "has_protocol": bool(re.search(r"\b(dataset|metric|accuracy|resolution|setting|trained|test set|validation)\b", caption, re.I)),
        "defines_panels": len(subs) >= 2,
    }


def analyze_pdf(path: Path, record: dict) -> dict:
    pdf_bytes = path.stat().st_size
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    doc = fitz.open(path)
    page_count = len(doc)
    blocks, visuals = [], []
    total_images = 0
    for page_index, page in enumerate(doc):
        data = page.get_text("dict", sort=True)
        page_text_blocks, image_bboxes = [], []
        for block in data.get("blocks", []):
            if block.get("type") == 0:
                for text, size, bold, span_count, bbox in split_text_block(block):
                    # Some PDFs expose LaTeXML accessibility payloads as tiny
                    # visible text blocks; counting the serialized XML can add
                    # thousands of fake words to a section.
                    if "<latexit" in text.lower() or "sha1_base64=" in text.lower():
                        continue
                    item = {
                        "page": page_index + 1, "text": text, "bbox": bbox,
                        "font_size": size, "bold": bold, "span_count": span_count,
                    }
                    page_text_blocks.append(item)
            elif block.get("type") == 1:
                image_bboxes.append(block.get("bbox", (0, 0, 0, 0)))
        total_images += len(image_bboxes)
        page_text_blocks = reading_order(page_text_blocks, page.rect)
        blocks.extend(page_text_blocks)

        for item in page_text_blocks:
            text = normalize_space(item["text"])
            cap = re.match(
                r"^(Fig(?:ure)?\.?\s*([A-Za-z0-9]+)|Table\s*([A-Za-z0-9]+))\s*[:.\-–]\s+(.+)$",
                text, re.I,
            )
            if not cap:
                continue
            kind = "table" if cap.group(3) else "figure"
            number = cap.group(3) or cap.group(2) or ""
            label = f"{kind.title()} {number}".strip()
            rect, source = infer_visual_bbox(page.rect, item["bbox"], image_bboxes, page_text_blocks)
            visual = visual_features(page, rect, page_text_blocks)
            visual["bbox_source"] = source
            visual["page_position"] = (
                "top" if rect.y0 / page.rect.height < 0.25 else
                "bottom" if rect.y1 / page.rect.height > 0.75 else "middle"
            )
            signals = caption_signals(text)
            visuals.append({
                "kind": kind, "label": label, "page": page_index + 1,
                "caption": text[:4000], "figure_type": classify_figure(text, page_index + 1, label, visual),
                "bbox": [round(v, 2) for v in rect], "visual": visual, "caption_signals": signals,
                "image_object_count": len(image_bboxes),
            })

    headings = find_headings(blocks)
    sections = []
    for order, heading in enumerate(headings):
        start = heading["block_index"]
        end = headings[order + 1]["block_index"] if order + 1 < len(headings) else len(blocks)
        segment_blocks = blocks[start + 1:end]
        text_parts = ([heading["inline_body"]] if heading["inline_body"] else []) + [b["text"] for b in segment_blocks]
        text = "\n\n".join(text_parts)
        features = section_features(text, len(segment_blocks) + (1 if heading["inline_body"] else 0))
        sections.append({
            "section_order": order,
            "heading": heading["heading"][:300],
            "category": heading["category"],
            "page_start": heading["page"],
            "page_end": segment_blocks[-1]["page"] if segment_blocks else heading["page"],
            "font_size": round(heading["font_size"], 2),
            **features,
        })

    all_text = "\n".join(b["text"] for b in blocks)
    doc.close()
    return {
        "paper": {
            "pdf_bytes": pdf_bytes,
            "pdf_sha256": digest,
            "pages": page_count,
            "word_count": len(words(all_text)),
            "section_count": len(sections),
            "figure_count": sum(v["kind"] == "figure" for v in visuals),
            "table_count": sum(v["kind"] == "table" for v in visuals),
            "image_object_count": total_images,
        },
        "sections": sections,
        "visuals": visuals,
    }


def init_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS papers (
      paper_id TEXT PRIMARY KEY, conference TEXT, year INTEGER, title TEXT,
      presentation TEXT, track TEXT, pdf_url TEXT, paper_url TEXT,
      status TEXT NOT NULL DEFAULT 'pending', attempts INTEGER NOT NULL DEFAULT 0,
      analyzer_version TEXT, pdf_bytes INTEGER, pdf_sha256 TEXT, pages INTEGER,
      word_count INTEGER, section_count INTEGER, figure_count INTEGER,
      table_count INTEGER, image_object_count INTEGER, error TEXT,
      updated_at INTEGER
    );
    CREATE INDEX IF NOT EXISTS papers_status_idx ON papers(status);
    CREATE INDEX IF NOT EXISTS papers_venue_idx ON papers(conference, year, presentation);
    CREATE TABLE IF NOT EXISTS sections (
      paper_id TEXT, section_order INTEGER, heading TEXT, category TEXT,
      page_start INTEGER, page_end INTEGER, font_size REAL, word_count INTEGER,
      sentence_count INTEGER, paragraph_count INTEGER, avg_sentence_words REAL,
      citation_mentions INTEGER, figure_mentions INTEGER, table_mentions INTEGER,
      equation_mentions INTEGER, first_person_mentions INTEGER, hedge_mentions INTEGER,
      strong_claim_mentions INTEGER, contribution_cues INTEGER, limitation_cues INTEGER,
      role_counts_json TEXT,
      PRIMARY KEY (paper_id, section_order)
    );
    CREATE INDEX IF NOT EXISTS sections_category_idx ON sections(category);
    CREATE TABLE IF NOT EXISTS visuals (
      paper_id TEXT, visual_order INTEGER, kind TEXT, label TEXT, page INTEGER,
      caption TEXT, figure_type TEXT, bbox_json TEXT, visual_json TEXT,
      caption_signals_json TEXT, image_object_count INTEGER,
      PRIMARY KEY (paper_id, visual_order)
    );
    CREATE INDEX IF NOT EXISTS visuals_type_idx ON visuals(kind, figure_type);
    """)
    conn.execute("UPDATE papers SET status='pending' WHERE status='processing'")
    conn.commit()
    return conn


def seed_db(conn: sqlite3.Connection, records: list[dict]):
    rows = []
    for r in records:
        rows.append((
            paper_id(r), r.get("conference"), r.get("year"), r.get("title"),
            r.get("presentation", "poster"), r.get("track"), r.get("pdf_url"), r.get("paper_url"),
            "pending" if r.get("pdf_url") else "no_pdf", int(time.time()),
        ))
    conn.executemany("""
      INSERT INTO papers(paper_id, conference, year, title, presentation, track,
        pdf_url, paper_url, status, updated_at)
      VALUES(?,?,?,?,?,?,?,?,?,?)
      ON CONFLICT(paper_id) DO UPDATE SET
        presentation=excluded.presentation, track=excluded.track,
        pdf_url=COALESCE(excluded.pdf_url, papers.pdf_url),
        paper_url=COALESCE(excluded.paper_url, papers.paper_url)
    """, rows)
    conn.commit()


def download_pdf(url: str, target: Path, max_mb: int):
    cmd = [
        "curl", "--fail", "--location", "--silent", "--show-error", "--compressed",
        "--retry", "3", "--retry-delay", "2", "--connect-timeout", "30", "--max-time", "300",
        "--max-filesize", str(max_mb * 1024 * 1024), "--user-agent", USER_AGENT,
        "--output", str(target), url,
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        raise RuntimeError(f"curl_exit_{result.returncode}: {result.stderr.strip()[:500]}")
    with target.open("rb") as fh:
        if fh.read(4) != b"%PDF":
            raise ValueError("response_is_not_pdf")


def process_record(record: dict, temp_root: Path, keep_root: Path | None, max_mb: int):
    pid = paper_id(record)
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"paper-{pid}-", dir=temp_root) as td:
        pdf = Path(td) / "paper.pdf"
        download_pdf(record["pdf_url"], pdf, max_mb)
        analysis = analyze_pdf(pdf, record)
        if keep_root:
            dest = keep_root / record["conference"] / str(record["year"]) / f"{pid}.pdf"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf, dest)
        return pid, analysis


def write_success(conn: sqlite3.Connection, pid: str, analysis: dict):
    p = analysis["paper"]
    conn.execute("DELETE FROM sections WHERE paper_id=?", (pid,))
    conn.execute("DELETE FROM visuals WHERE paper_id=?", (pid,))
    conn.execute("""
      UPDATE papers SET status='done', analyzer_version=?, pdf_bytes=?, pdf_sha256=?,
        pages=?, word_count=?, section_count=?, figure_count=?, table_count=?,
        image_object_count=?, error=NULL, attempts=attempts+1, updated_at=?
      WHERE paper_id=?
    """, (
        ANALYZER_VERSION, p["pdf_bytes"], p["pdf_sha256"], p["pages"], p["word_count"],
        p["section_count"], p["figure_count"], p["table_count"], p["image_object_count"],
        int(time.time()), pid,
    ))
    for s in analysis["sections"]:
        conn.execute("""
          INSERT INTO sections VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            pid, s["section_order"], s["heading"], s["category"], s["page_start"], s["page_end"],
            s["font_size"], s["word_count"], s["sentence_count"], s["paragraph_count"],
            s["avg_sentence_words"], s["citation_mentions"], s["figure_mentions"],
            s["table_mentions"], s["equation_mentions"], s["first_person_mentions"],
            s["hedge_mentions"], s["strong_claim_mentions"], s["contribution_cues"],
            s["limitation_cues"], json.dumps(s["role_counts"], sort_keys=True),
        ))
    for idx, v in enumerate(analysis["visuals"]):
        conn.execute("INSERT INTO visuals VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
            pid, idx, v["kind"], v["label"], v["page"], v["caption"], v["figure_type"],
            json.dumps(v["bbox"]), json.dumps(v["visual"], sort_keys=True),
            json.dumps(v["caption_signals"], sort_keys=True), v["image_object_count"],
        ))
    conn.commit()


def write_failure(conn: sqlite3.Connection, pid: str, exc: Exception):
    msg = str(exc)[:1000]
    if re.search(r"\b403\b|\b401\b", msg):
        status = "blocked"
    elif re.search(r"\b404\b", msg):
        status = "not_found"
    else:
        status = "error"
    conn.execute("""
      UPDATE papers SET status=?, error=?, attempts=attempts+1, updated_at=? WHERE paper_id=?
    """, (status, msg, int(time.time()), pid))
    conn.commit()
    return status


def selected_records(records: list[dict], conn: sqlite3.Connection, args) -> list[dict]:
    states = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT paper_id,status,analyzer_version FROM papers")
    }
    result = []
    for r in records:
        if not r.get("pdf_url"):
            continue
        if args.conference and r["conference"] != args.conference:
            continue
        if args.year and r["year"] != args.year:
            continue
        if args.presentation and r.get("presentation", "poster") != args.presentation:
            continue
        status, analyzed_version = states.get(paper_id(r), ("pending", None))
        allowed = {"pending"}
        if args.retry_errors:
            allowed.add("error")
        if args.retry_blocked:
            allowed |= {"blocked", "not_found"}
        if args.reanalyze:
            allowed |= {"done"}
        if status in allowed or (status == "done" and analyzed_version != ANALYZER_VERSION):
            result.append(r)
    result.sort(key=lambda r: (
        PRIORITY_ORDER.get(r.get("presentation", "poster"), 9),
        r["conference"], r["year"], hashlib.sha256(r["title"].encode()).hexdigest(),
    ))
    return result[:args.limit] if args.limit else result


def progress_snapshot(conn: sqlite3.Connection) -> dict:
    counts = dict(conn.execute("SELECT status,COUNT(*) FROM papers GROUP BY status").fetchall())
    done = counts.get("done", 0)
    totals = conn.execute("SELECT COALESCE(SUM(figure_count),0),COALESCE(SUM(table_count),0),COALESCE(SUM(section_count),0),COALESCE(SUM(pdf_bytes),0) FROM papers WHERE status='done'").fetchone()
    return {
        "analyzer_version": ANALYZER_VERSION,
        "papers_by_status": counts,
        "papers_analyzed": done,
        "figures_analyzed": totals[0], "tables_analyzed": totals[1],
        "sections_analyzed": totals[2], "pdf_bytes_streamed": totals[3],
        "updated_at": int(time.time()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--database", type=Path, required=True)
    ap.add_argument("--temp-dir", type=Path, required=True)
    ap.add_argument("--progress-json", type=Path)
    ap.add_argument("--keep-pdfs", type=Path, help="Optional; can require hundreds of GiB")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-pdf-mb", type=int, default=80)
    ap.add_argument("--conference", choices=["CVPR", "ICCV", "ECCV", "NeurIPS", "ICML"])
    ap.add_argument("--year", type=int)
    ap.add_argument("--presentation", choices=["poster", "spotlight", "highlight", "oral"])
    ap.add_argument("--retry-errors", action="store_true")
    ap.add_argument("--retry-blocked", action="store_true",
                    help="Retry authorization failures and missing URLs only after the source changes")
    ap.add_argument("--reanalyze", action="store_true")
    ap.add_argument("--host-block-threshold", type=int, default=3,
                    help="Open a circuit after repeated 401/403 responses from one host")
    args = ap.parse_args()
    records = list(iter_corpus(args.corpus))
    conn = init_db(args.database)
    seed_db(conn, records)
    queue = selected_records(records, conn, args)
    print(json.dumps({"corpus_records": len(records), "queued": len(queue), "database": str(args.database)}, ensure_ascii=False), flush=True)
    args.temp_dir.mkdir(parents=True, exist_ok=True)
    completed = 0
    host_block_counts = {}
    blocked_hosts = set()
    try:
        for offset in range(0, len(queue), max(1, args.jobs)):
            batch = queue[offset:offset + max(1, args.jobs)]
            active_batch = []
            for r in batch:
                host = urlparse(r["pdf_url"]).netloc.lower()
                if host in blocked_hosts:
                    conn.execute(
                        "UPDATE papers SET status='blocked',error=?,attempts=attempts+1,updated_at=? WHERE paper_id=?",
                        (f"host_circuit_open:{host}", int(time.time()), paper_id(r)),
                    )
                    completed += 1
                    continue
                active_batch.append(r)
                conn.execute("UPDATE papers SET status='processing',updated_at=? WHERE paper_id=?", (int(time.time()), paper_id(r)))
            conn.commit()
            if not active_batch:
                continue
            with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
                futures = {
                    pool.submit(process_record, r, args.temp_dir, args.keep_pdfs, args.max_pdf_mb): r
                    for r in active_batch
                }
                for future in as_completed(futures):
                    record = futures[future]
                    pid = paper_id(record)
                    try:
                        _, analysis = future.result()
                        write_success(conn, pid, analysis)
                        outcome = f'done figures={analysis["paper"]["figure_count"]} sections={analysis["paper"]["section_count"]}'
                    except Exception as exc:
                        status = write_failure(conn, pid, exc)
                        outcome = f"failed {str(exc)[:160]}"
                        if status == "blocked":
                            host = urlparse(record["pdf_url"]).netloc.lower()
                            host_block_counts[host] = host_block_counts.get(host, 0) + 1
                            if host_block_counts[host] >= max(1, args.host_block_threshold):
                                blocked_hosts.add(host)
                                print(f"host circuit opened after repeated authorization failures: {host}", flush=True)
                    completed += 1
                    print(f'[{completed}/{len(queue)}] {record["conference"]} {record["year"]} {record.get("presentation")} {outcome} :: {record["title"]}', flush=True)
            snapshot = progress_snapshot(conn)
            if args.progress_json:
                args.progress_json.parent.mkdir(parents=True, exist_ok=True)
                args.progress_json.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except KeyboardInterrupt:
        conn.execute("UPDATE papers SET status='pending' WHERE status='processing'")
        conn.commit()
        print("Interrupted; checkpoint preserved.", file=sys.stderr)
        return 130
    finally:
        snapshot = progress_snapshot(conn)
        if args.progress_json:
            args.progress_json.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        conn.close()
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
