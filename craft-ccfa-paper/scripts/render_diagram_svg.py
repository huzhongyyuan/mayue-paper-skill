#!/usr/bin/env python3
"""Validate or render a structured paper-diagram JSON spec as editable SVG."""

from __future__ import annotations

import argparse
import json
import math
import sys
import textwrap
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


SHAPES = {"rect", "rounded", "ellipse", "circle", "diamond"}
LINE_STYLES = {"solid", "dashed", "dotted"}
EDGE_SEMANTICS = {"generic", "data", "control", "loss", "gradient", "feedback"}
EDGE_PHASES = {"train", "inference", "both"}
HEX_COLOR = "#RRGGBB"

SCHEMA = {
    "schema_version": "1.0",
    "canvas": {"width": 1200, "height": 620, "background": "#FFFFFF", "padding": 40},
    "title": "optional",
    "subtitle": "optional",
    "style": {
        "font_family": "Arial",
        "font_size": 22,
        "title_size": 34,
        "node_fill": "#EAF2F8",
        "node_stroke": "#315C86",
        "text_color": "#17202A",
        "edge_color": "#566573",
    },
    "groups": [
        {"id": "g1", "label": "Group", "x": 20, "y": 120, "width": 500, "height": 350}
    ],
    "nodes": [
        {
            "id": "n1",
            "label": "Node",
            "x": 80,
            "y": 180,
            "width": 180,
            "height": 72,
            "shape": "rounded",
            "group": "g1",
        },
        {
            "id": "n2",
            "label": "Output",
            "x": 320,
            "y": 180,
            "width": 180,
            "height": 72,
            "shape": "rounded",
            "group": "g1",
        },
    ],
    "edges": [
        {
            "from": "n1",
            "to": "n2",
            "label": "optional",
            "style": "solid",
            "route": "straight",
            "semantic": "data",
            "phase": "both",
        }
    ],
    "footer": "optional",
}


class SpecError(ValueError):
    pass


def read_spec(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SpecError(f"cannot read JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecError("JSON root must be an object")
    return data


def number(value: Any, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise SpecError(f"{name} must be a finite number")
    result = float(value)
    if positive and result <= 0:
        raise SpecError(f"{name} must be > 0")
    return result


def color(value: Any, name: str) -> str:
    text = str(value or "")
    if len(text) != 7 or not text.startswith("#"):
        raise SpecError(f"{name} must use {HEX_COLOR}")
    try:
        int(text[1:], 16)
    except ValueError as exc:
        raise SpecError(f"{name} must use {HEX_COLOR}") from exc
    return text.upper()


def validate(spec: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    schema_version = str(spec.get("schema_version") or "").strip()
    if not schema_version:
        warnings.append("schema_version is missing; add schema_version: 1.0")
    elif schema_version != "1.0":
        raise SpecError(f"unsupported schema_version: {schema_version}")
    canvas = spec.get("canvas")
    if not isinstance(canvas, dict):
        raise SpecError("canvas must be an object")
    width = number(canvas.get("width"), "canvas.width", positive=True)
    height = number(canvas.get("height"), "canvas.height", positive=True)
    color(canvas.get("background", "#FFFFFF"), "canvas.background")

    style = spec.get("style", {})
    if not isinstance(style, dict):
        raise SpecError("style must be an object")
    for key in ("node_fill", "node_stroke", "text_color", "edge_color", "group_fill", "group_stroke"):
        if key in style:
            color(style[key], f"style.{key}")
    for key in ("font_size", "title_size", "subtitle_size", "edge_width", "node_stroke_width"):
        if key in style:
            number(style[key], f"style.{key}", positive=True)

    groups = spec.get("groups", [])
    nodes = spec.get("nodes")
    edges = spec.get("edges", [])
    if not isinstance(groups, list) or not isinstance(nodes, list) or not isinstance(edges, list):
        raise SpecError("groups, nodes, and edges must be arrays")
    if not nodes:
        raise SpecError("nodes must contain at least one node")

    group_ids: set[str] = set()
    for index, item in enumerate(groups):
        if not isinstance(item, dict):
            raise SpecError(f"groups[{index}] must be an object")
        gid = str(item.get("id") or "").strip()
        if not gid or gid in group_ids:
            raise SpecError(f"groups[{index}].id is missing or duplicated")
        group_ids.add(gid)
        x = number(item.get("x"), f"groups[{index}].x")
        y = number(item.get("y"), f"groups[{index}].y")
        w = number(item.get("width"), f"groups[{index}].width", positive=True)
        h = number(item.get("height"), f"groups[{index}].height", positive=True)
        for key in ("fill", "stroke", "text_color"):
            if key in item:
                color(item[key], f"groups[{index}].{key}")
        if x < 0 or y < 0 or x + w > width or y + h > height:
            warnings.append(f"group {gid} extends outside the canvas")

    node_ids: set[str] = set()
    boxes: dict[str, tuple[float, float, float, float]] = {}
    for index, item in enumerate(nodes):
        if not isinstance(item, dict):
            raise SpecError(f"nodes[{index}] must be an object")
        nid = str(item.get("id") or "").strip()
        label = str(item.get("label") or "").strip()
        if not nid or nid in node_ids:
            raise SpecError(f"nodes[{index}].id is missing or duplicated")
        if not label:
            raise SpecError(f"nodes[{index}].label is required")
        node_ids.add(nid)
        x = number(item.get("x"), f"nodes[{index}].x")
        y = number(item.get("y"), f"nodes[{index}].y")
        w = number(item.get("width", 160), f"nodes[{index}].width", positive=True)
        h = number(item.get("height", 70), f"nodes[{index}].height", positive=True)
        boxes[nid] = (x, y, w, h)
        shape = str(item.get("shape", "rounded"))
        if shape not in SHAPES:
            raise SpecError(f"nodes[{index}].shape must be one of {sorted(SHAPES)}")
        group = str(item.get("group") or "").strip()
        if group and group not in group_ids:
            raise SpecError(f"node {nid} refers to unknown group {group}")
        for key in ("fill", "stroke", "text_color"):
            if key in item:
                color(item[key], f"nodes[{index}].{key}")
        if x < 0 or y < 0 or x + w > width or y + h > height:
            warnings.append(f"node {nid} extends outside the canvas")

    ids = list(boxes)
    for i, left_id in enumerate(ids):
        ax, ay, aw, ah = boxes[left_id]
        for right_id in ids[i + 1 :]:
            bx, by, bw, bh = boxes[right_id]
            overlap_w = min(ax + aw, bx + bw) - max(ax, bx)
            overlap_h = min(ay + ah, by + bh) - max(ay, by)
            if overlap_w > 2 and overlap_h > 2:
                warnings.append(f"nodes {left_id} and {right_id} overlap")

    for index, item in enumerate(edges):
        if not isinstance(item, dict):
            raise SpecError(f"edges[{index}] must be an object")
        source = str(item.get("from") or "")
        target = str(item.get("to") or "")
        if source not in node_ids or target not in node_ids:
            raise SpecError(f"edges[{index}] refers to an unknown node")
        if str(item.get("style", "solid")) not in LINE_STYLES:
            raise SpecError(f"edges[{index}].style must be one of {sorted(LINE_STYLES)}")
        if str(item.get("route", "straight")) not in {"straight", "curve"}:
            raise SpecError(f"edges[{index}].route must be straight or curve")
        if str(item.get("semantic", "generic")) not in EDGE_SEMANTICS:
            raise SpecError(f"edges[{index}].semantic must be one of {sorted(EDGE_SEMANTICS)}")
        if str(item.get("phase", "both")) not in EDGE_PHASES:
            raise SpecError(f"edges[{index}].phase must be one of {sorted(EDGE_PHASES)}")
        if "color" in item:
            color(item["color"], f"edges[{index}].color")
    return warnings


def merged_style(spec: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "font_family": "Arial, Helvetica, sans-serif",
        "font_size": 22,
        "title_size": 34,
        "subtitle_size": 18,
        "node_fill": "#EAF2F8",
        "node_stroke": "#315C86",
        "node_stroke_width": 2.4,
        "text_color": "#17202A",
        "edge_color": "#566573",
        "edge_width": 2.4,
        "group_fill": "#F7F9F9",
        "group_stroke": "#CCD1D1",
        "group_label_size": 18,
    }
    result.update(spec.get("style", {}))
    return result


def node_center(node: dict[str, Any]) -> tuple[float, float]:
    return float(node["x"]) + float(node.get("width", 160)) / 2, float(node["y"]) + float(node.get("height", 70)) / 2


def anchor(node: dict[str, Any], toward: tuple[float, float]) -> tuple[float, float]:
    cx, cy = node_center(node)
    dx, dy = toward[0] - cx, toward[1] - cy
    if abs(dx) + abs(dy) < 1e-8:
        return cx, cy
    hw = float(node.get("width", 160)) / 2
    hh = float(node.get("height", 70)) / 2
    shape = str(node.get("shape", "rounded"))
    if shape in {"ellipse", "circle"}:
        scale = 1 / math.sqrt((dx / hw) ** 2 + (dy / hh) ** 2)
    elif shape == "diamond":
        scale = 1 / (abs(dx) / hw + abs(dy) / hh)
    else:
        scale = min(hw / abs(dx) if dx else float("inf"), hh / abs(dy) if dy else float("inf"))
    return cx + dx * scale, cy + dy * scale


def dash(style: str) -> str:
    return {"solid": "", "dashed": ' stroke-dasharray="10 7"', "dotted": ' stroke-dasharray="3 6"'}[style]


def split_label(text: str, max_chars: int) -> list[str]:
    explicit = text.splitlines() or [text]
    lines: list[str] = []
    for part in explicit:
        if len(part) <= max_chars or not part.strip():
            lines.append(part)
            continue
        if " " in part:
            lines.extend(textwrap.wrap(part, width=max_chars, break_long_words=False, break_on_hyphens=False))
        else:
            lines.extend(part[i : i + max_chars] for i in range(0, len(part), max_chars))
    return lines[:5]


def text_element(
    label: str,
    cx: float,
    cy: float,
    width: float,
    font_size: float,
    font_family: str,
    fill: str,
    *,
    weight: str = "600",
) -> str:
    max_chars = max(4, int(width / max(font_size * 0.58, 1)))
    lines = split_label(label, max_chars)
    line_height = font_size * 1.22
    first_y = cy - line_height * (len(lines) - 1) / 2
    tspans = []
    for index, line in enumerate(lines):
        y = first_y + index * line_height
        tspans.append(f'<tspan x="{cx:.2f}" y="{y:.2f}">{escape(line)}</tspan>')
    return (
        f'<text text-anchor="middle" dominant-baseline="middle" '
        f'font-family="{escape(font_family)}" font-size="{font_size:.2f}" '
        f'font-weight="{weight}" fill="{fill}">' + "".join(tspans) + "</text>"
    )


def render(spec: dict[str, Any]) -> str:
    validate(spec)
    canvas = spec["canvas"]
    width, height = float(canvas["width"]), float(canvas["height"])
    background = str(canvas.get("background", "#FFFFFF"))
    style = merged_style(spec)
    nodes = {str(node["id"]): node for node in spec["nodes"]}

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" role="img">',
        f'<title>{escape(str(spec.get("title") or "Structured scientific diagram"))}</title>',
        "<defs>",
        f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{style["edge_color"]}"/></marker>',
        "</defs>",
        f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" fill="{background}"/>',
    ]

    title = str(spec.get("title") or "").strip()
    subtitle = str(spec.get("subtitle") or "").strip()
    if title:
        out.append(text_element(title, width / 2, 46, width - 80, float(style["title_size"]), str(style["font_family"]), str(style["text_color"]), weight="700"))
    if subtitle:
        out.append(text_element(subtitle, width / 2, 83, width - 100, float(style["subtitle_size"]), str(style["font_family"]), "#5D6D7E", weight="400"))

    for group in spec.get("groups", []):
        x, y = float(group["x"]), float(group["y"])
        w, h = float(group["width"]), float(group["height"])
        fill = str(group.get("fill", style["group_fill"]))
        stroke = str(group.get("stroke", style["group_stroke"]))
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        label = str(group.get("label") or "").strip()
        if label:
            out.append(
                f'<text x="{x + 18:.2f}" y="{y + 30:.2f}" font-family="{escape(str(style["font_family"]))}" '
                f'font-size="{float(group.get("font_size", style["group_label_size"])):.2f}" font-weight="700" '
                f'fill="{group.get("text_color", style["text_color"])}">{escape(label)}</text>'
            )

    edge_labels: list[tuple[str, float, float, str]] = []
    for edge in spec.get("edges", []):
        source, target = nodes[str(edge["from"])], nodes[str(edge["to"])]
        sc, tc = node_center(source), node_center(target)
        edge_color = str(edge.get("color", style["edge_color"]))
        edge_width = float(edge.get("width", style["edge_width"]))
        semantic = str(edge.get("semantic", "generic"))
        default_style = "dashed" if semantic in {"loss", "feedback"} else "dotted" if semantic == "gradient" else "solid"
        line_style = str(edge.get("style", default_style))
        route = str(edge.get("route", "straight"))
        if source is target:
            x, y = sc
            sx, sy = x + float(source.get("width", 160)) / 2, y
            path = f"M {sx:.2f} {sy:.2f} C {sx + 70:.2f} {sy - 80:.2f}, {sx - 50:.2f} {sy - 100:.2f}, {sx - 10:.2f} {sy - 5:.2f}"
            lx, ly = sx + 35, sy - 72
        else:
            sx, sy = anchor(source, tc)
            tx, ty = anchor(target, sc)
            if route == "curve":
                dx, dy = tx - sx, ty - sy
                length = max(math.hypot(dx, dy), 1)
                nx, ny = -dy / length, dx / length
                bend = float(edge.get("bend", 55))
                c1x, c1y = sx + dx * 0.33 + nx * bend, sy + dy * 0.33 + ny * bend
                c2x, c2y = sx + dx * 0.67 + nx * bend, sy + dy * 0.67 + ny * bend
                path = f"M {sx:.2f} {sy:.2f} C {c1x:.2f} {c1y:.2f}, {c2x:.2f} {c2y:.2f}, {tx:.2f} {ty:.2f}"
                lx, ly = (sx + tx) / 2 + nx * bend * 0.75, (sy + ty) / 2 + ny * bend * 0.75
            else:
                path = f"M {sx:.2f} {sy:.2f} L {tx:.2f} {ty:.2f}"
                lx, ly = (sx + tx) / 2, (sy + ty) / 2 - 10
        out.append(
            f'<path d="{path}" fill="none" stroke="{edge_color}" stroke-width="{edge_width:.2f}"'
            f'{dash(line_style)} marker-end="url(#arrow)" stroke-linecap="round"/>'
        )
        label = str(edge.get("label") or "").strip()
        if label:
            edge_labels.append((label, lx, ly, edge_color))

    for node in spec["nodes"]:
        x, y = float(node["x"]), float(node["y"])
        w, h = float(node.get("width", 160)), float(node.get("height", 70))
        fill = str(node.get("fill", style["node_fill"]))
        stroke = str(node.get("stroke", style["node_stroke"]))
        stroke_width = float(node.get("stroke_width", style["node_stroke_width"]))
        shape = str(node.get("shape", "rounded"))
        if shape == "diamond":
            points = f"{x + w / 2:.2f},{y:.2f} {x + w:.2f},{y + h / 2:.2f} {x + w / 2:.2f},{y + h:.2f} {x:.2f},{y + h / 2:.2f}"
            out.append(f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.2f}"/>')
        elif shape in {"ellipse", "circle"}:
            out.append(f'<ellipse cx="{x + w / 2:.2f}" cy="{y + h / 2:.2f}" rx="{w / 2:.2f}" ry="{h / 2:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.2f}"/>')
        else:
            radius = min(18, h / 4) if shape == "rounded" else 0
            out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.2f}"/>')
        out.append(
            text_element(
                str(node["label"]),
                x + w / 2,
                y + h / 2,
                w - 18,
                float(node.get("font_size", style["font_size"])),
                str(style["font_family"]),
                str(node.get("text_color", style["text_color"])),
                weight=str(node.get("font_weight", "600")),
            )
        )

    for label, x, y, edge_color in edge_labels:
        font_size = float(style["font_size"]) * 0.68
        box_width = max(44, len(label) * font_size * 0.58 + 18)
        box_height = font_size * 1.6
        out.append(f'<rect x="{x - box_width / 2:.2f}" y="{y - box_height / 2:.2f}" width="{box_width:.2f}" height="{box_height:.2f}" rx="7" fill="{background}" fill-opacity="0.92"/>')
        out.append(text_element(label, x, y, box_width - 8, font_size, str(style["font_family"]), edge_color, weight="500"))

    footer = str(spec.get("footer") or "").strip()
    if footer:
        out.append(
            f'<text x="{width - 36:.2f}" y="{height - 22:.2f}" text-anchor="end" '
            f'font-family="{escape(str(style["font_family"]))}" font-size="14" fill="#7B7D7D">{escape(footer)}</text>'
        )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate", help="Validate a JSON spec")
    validate_parser.add_argument("spec", type=Path)
    render_parser = sub.add_parser("render", help="Render a JSON spec to SVG")
    render_parser.add_argument("spec", type=Path)
    render_parser.add_argument("--output", required=True, type=Path)
    render_parser.add_argument("--force", action="store_true", help="Allow replacing the exact output file")
    sub.add_parser("schema", help="Print an illustrative schema")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "schema":
        print(json.dumps(SCHEMA, indent=2, ensure_ascii=False))
        return 0
    try:
        spec = read_spec(args.spec.expanduser().resolve())
        warnings = validate(spec)
        if args.command == "validate":
            print("valid")
            for warning in warnings:
                print(f"warning: {warning}")
            return 0
        output = args.output.expanduser().resolve()
        if output.exists() and not args.force:
            raise SpecError(f"refusing to overwrite output: {output}; pass --force")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render(spec), encoding="utf-8")
        print(f"rendered: {output}")
        for warning in warnings:
            print(f"warning: {warning}")
        return 0
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
