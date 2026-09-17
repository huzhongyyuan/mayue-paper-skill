#!/usr/bin/env node
/** Render the craft-ccfa-paper diagram JSON spec as native PowerPoint shapes. */

import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
let PptxGenJS;
try {
  PptxGenJS = require("pptxgenjs");
} catch (error) {
  console.error("error: pptxgenjs is unavailable; install it in an isolated project or expose the host runtime through NODE_PATH");
  process.exit(2);
}

function usage() {
  console.error("usage: render_diagram_pptx.mjs SPEC.json --output OUT.pptx [--force]");
}

function parseArgs(argv) {
  const result = { spec: null, output: null, force: false };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (!result.spec && !value.startsWith("--")) result.spec = value;
    else if (value === "--output") result.output = argv[++index];
    else if (value === "--force") result.force = true;
    else throw new Error(`unknown argument: ${value}`);
  }
  if (!result.spec || !result.output) throw new Error("spec and --output are required");
  return result;
}

function readJson(file) {
  let value;
  try {
    value = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    throw new Error(`cannot read JSON: ${error.message}`);
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("JSON root must be an object");
  return value;
}

function finite(value, name, positive = false) {
  if (typeof value !== "number" || !Number.isFinite(value) || (positive && value <= 0)) {
    throw new Error(`${name} must be ${positive ? "a positive" : "a finite"} number`);
  }
  return value;
}

function hex(value, fallback) {
  const text = String(value ?? fallback ?? "").replace(/^#/, "").toUpperCase();
  if (!/^[0-9A-F]{6}$/.test(text)) throw new Error(`invalid color: ${value}`);
  return text;
}

function validate(spec) {
  if (String(spec.schema_version ?? "") !== "1.0") throw new Error("schema_version must be 1.0");
  if (!spec.canvas || typeof spec.canvas !== "object") throw new Error("canvas must be an object");
  finite(spec.canvas.width, "canvas.width", true);
  finite(spec.canvas.height, "canvas.height", true);
  if (!Array.isArray(spec.nodes) || spec.nodes.length === 0) throw new Error("nodes must be a non-empty array");
  if (!Array.isArray(spec.edges ?? [])) throw new Error("edges must be an array");
  if (!Array.isArray(spec.groups ?? [])) throw new Error("groups must be an array");
  const groupIds = new Set();
  for (const [index, group] of (spec.groups ?? []).entries()) {
    if (!group || typeof group !== "object") throw new Error(`groups[${index}] must be an object`);
    if (!group.id || groupIds.has(group.id)) throw new Error(`groups[${index}].id is missing or duplicated`);
    groupIds.add(group.id);
    for (const field of ["x", "y", "width", "height"]) finite(group[field], `groups[${index}].${field}`, field === "width" || field === "height");
  }
  const nodeIds = new Set();
  for (const [index, node] of spec.nodes.entries()) {
    if (!node || typeof node !== "object") throw new Error(`nodes[${index}] must be an object`);
    if (!node.id || nodeIds.has(node.id)) throw new Error(`nodes[${index}].id is missing or duplicated`);
    if (!String(node.label ?? "").trim()) throw new Error(`nodes[${index}].label is required`);
    nodeIds.add(node.id);
    for (const field of ["x", "y"]) finite(node[field], `nodes[${index}].${field}`);
    finite(node.width ?? 160, `nodes[${index}].width`, true);
    finite(node.height ?? 70, `nodes[${index}].height`, true);
    if (node.group && !groupIds.has(node.group)) throw new Error(`node ${node.id} refers to unknown group ${node.group}`);
  }
  for (const [index, edge] of (spec.edges ?? []).entries()) {
    if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to)) throw new Error(`edges[${index}] refers to an unknown node`);
    if (!["generic", "data", "control", "loss", "gradient", "feedback"].includes(edge.semantic ?? "generic")) throw new Error(`edges[${index}].semantic is invalid`);
    if (!["train", "inference", "both"].includes(edge.phase ?? "both")) throw new Error(`edges[${index}].phase is invalid`);
  }
}

function center(node) {
  return { x: node.x + (node.width ?? 160) / 2, y: node.y + (node.height ?? 70) / 2 };
}

function anchor(node, toward) {
  const c = center(node);
  const dx = toward.x - c.x;
  const dy = toward.y - c.y;
  if (Math.abs(dx) + Math.abs(dy) < 1e-8) return c;
  const hw = (node.width ?? 160) / 2;
  const hh = (node.height ?? 70) / 2;
  let scale;
  if (["ellipse", "circle"].includes(node.shape ?? "rounded")) {
    scale = 1 / Math.sqrt((dx / hw) ** 2 + (dy / hh) ** 2);
  } else if ((node.shape ?? "rounded") === "diamond") {
    scale = 1 / (Math.abs(dx) / hw + Math.abs(dy) / hh);
  } else {
    scale = Math.min(dx ? hw / Math.abs(dx) : Infinity, dy ? hh / Math.abs(dy) : Infinity);
  }
  return { x: c.x + dx * scale, y: c.y + dy * scale };
}

function pptShape(pptx, shape) {
  const table = {
    rect: pptx.ShapeType.rect,
    rounded: pptx.ShapeType.roundRect,
    ellipse: pptx.ShapeType.ellipse,
    circle: pptx.ShapeType.ellipse,
    diamond: pptx.ShapeType.diamond,
  };
  return table[shape ?? "rounded"] ?? pptx.ShapeType.roundRect;
}

function lineDash(style) {
  if (style === "dashed") return "dash";
  if (style === "dotted") return "dot";
  return "solid";
}

function addLine(slide, pptx, from, to, options, arrow = false) {
  slide.addShape(pptx.ShapeType.line, {
    x: from.x,
    y: from.y,
    w: to.x - from.x,
    h: to.y - from.y,
    line: {
      color: options.color,
      width: options.width,
      dash: options.dash,
      beginArrowType: "none",
      endArrowType: arrow ? "triangle" : "none",
    },
  });
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    usage();
    throw error;
  }
  const specPath = path.resolve(args.spec);
  const outputPath = path.resolve(args.output);
  if (fs.existsSync(outputPath) && !args.force) throw new Error(`refusing to overwrite output: ${outputPath}; pass --force`);
  const spec = readJson(specPath);
  validate(spec);

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "craft-ccfa-paper";
  pptx.subject = "Editable scientific diagram";
  pptx.title = String(spec.title ?? "Structured scientific diagram");
  pptx.company = "";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: String(spec.style?.font_family ?? "Arial"),
    bodyFontFace: String(spec.style?.font_family ?? "Arial"),
    lang: "en-US",
  };

  const slide = pptx.addSlide();
  const slideW = 13.333;
  const slideH = 7.5;
  const margin = 0.18;
  const scale = Math.min((slideW - margin * 2) / spec.canvas.width, (slideH - margin * 2) / spec.canvas.height);
  const offsetX = (slideW - spec.canvas.width * scale) / 2;
  const offsetY = (slideH - spec.canvas.height * scale) / 2;
  const X = (value) => offsetX + value * scale;
  const Y = (value) => offsetY + value * scale;
  const W = (value) => value * scale;
  const style = {
    font: String(spec.style?.font_family ?? "Arial"),
    fontSize: Number(spec.style?.font_size ?? 22),
    titleSize: Number(spec.style?.title_size ?? 34),
    subtitleSize: Number(spec.style?.subtitle_size ?? 18),
    nodeFill: hex(spec.style?.node_fill, "EAF2F8"),
    nodeStroke: hex(spec.style?.node_stroke, "315C86"),
    textColor: hex(spec.style?.text_color, "17202A"),
    edgeColor: hex(spec.style?.edge_color, "566573"),
    groupFill: hex(spec.style?.group_fill, "F7F9F9"),
    groupStroke: hex(spec.style?.group_stroke, "CCD1D1"),
  };

  slide.background = { color: hex(spec.canvas.background, "FFFFFF") };

  for (const group of spec.groups ?? []) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: X(group.x), y: Y(group.y), w: W(group.width), h: W(group.height),
      rectRadius: 0.08,
      fill: { color: hex(group.fill, style.groupFill), transparency: 0 },
      line: { color: hex(group.stroke, style.groupStroke), width: 1.4 },
    });
    if (String(group.label ?? "").trim()) {
      slide.addText(String(group.label), {
        x: X(group.x + 16), y: Y(group.y + 9), w: W(group.width - 32), h: W(32),
        fontFace: style.font, fontSize: Number(group.font_size ?? 18) * scale * 60,
        bold: true, color: hex(group.text_color, style.textColor), margin: 0, valign: "mid",
      });
    }
  }

  const nodeMap = new Map(spec.nodes.map((node) => [node.id, node]));
  const edgeLabels = [];
  for (const edge of spec.edges ?? []) {
    const source = nodeMap.get(edge.from);
    const target = nodeMap.get(edge.to);
    const sc = center(source);
    const tc = center(target);
    const opts = {
      color: hex(edge.color, style.edgeColor),
      width: Number(edge.width ?? 2.4) * 0.55,
      dash: lineDash(edge.style ?? (["loss", "feedback"].includes(edge.semantic) ? "dashed" : edge.semantic === "gradient" ? "dotted" : "solid")),
    };
    if (edge.from === edge.to) {
      const width = source.width ?? 160;
      const height = source.height ?? 70;
      const start = { x: source.x + width, y: source.y + height * 0.62 };
      const end = { x: source.x + width * 0.62, y: source.y };
      const p1 = { x: source.x + width + 58, y: start.y };
      const p2 = { x: p1.x, y: source.y - 48 };
      const p3 = { x: end.x, y: p2.y };
      addLine(slide, pptx, { x: X(start.x), y: Y(start.y) }, { x: X(p1.x), y: Y(p1.y) }, opts, false);
      addLine(slide, pptx, { x: X(p1.x), y: Y(p1.y) }, { x: X(p2.x), y: Y(p2.y) }, opts, false);
      addLine(slide, pptx, { x: X(p2.x), y: Y(p2.y) }, { x: X(p3.x), y: Y(p3.y) }, opts, false);
      addLine(slide, pptx, { x: X(p3.x), y: Y(p3.y) }, { x: X(end.x), y: Y(end.y) }, opts, true);
      edgeLabels.push({ text: edge.label, x: source.x + width + 36, y: source.y - 34, color: opts.color });
    } else {
      const start = anchor(source, tc);
      const end = anchor(target, sc);
      if ((edge.route ?? "straight") === "curve") {
      const dx = end.x - start.x;
      const dy = end.y - start.y;
      const length = Math.max(Math.hypot(dx, dy), 1);
      const nx = -dy / length;
      const ny = dx / length;
      const bend = Number(edge.bend ?? 55);
      const p1 = { x: start.x + dx * 0.32 + nx * bend, y: start.y + dy * 0.32 + ny * bend };
      const p2 = { x: start.x + dx * 0.68 + nx * bend, y: start.y + dy * 0.68 + ny * bend };
      addLine(slide, pptx, { x: X(start.x), y: Y(start.y) }, { x: X(p1.x), y: Y(p1.y) }, opts, false);
      addLine(slide, pptx, { x: X(p1.x), y: Y(p1.y) }, { x: X(p2.x), y: Y(p2.y) }, opts, false);
      addLine(slide, pptx, { x: X(p2.x), y: Y(p2.y) }, { x: X(end.x), y: Y(end.y) }, opts, true);
      edgeLabels.push({ text: edge.label, x: (start.x + end.x) / 2 + nx * bend * 0.72, y: (start.y + end.y) / 2 + ny * bend * 0.72, color: opts.color });
      } else {
        addLine(slide, pptx, { x: X(start.x), y: Y(start.y) }, { x: X(end.x), y: Y(end.y) }, opts, true);
        edgeLabels.push({ text: edge.label, x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 - 9, color: opts.color });
      }
    }
  }

  for (const node of spec.nodes) {
    const fill = hex(node.fill, style.nodeFill);
    const stroke = hex(node.stroke, style.nodeStroke);
    slide.addShape(pptShape(pptx, node.shape), {
      x: X(node.x), y: Y(node.y), w: W(node.width ?? 160), h: W(node.height ?? 70),
      fill: { color: fill, transparency: 0 },
      line: { color: stroke, width: Number(node.stroke_width ?? 2.4) * 0.55 },
      rectRadius: node.shape === "rounded" ? 0.06 : undefined,
    });
    slide.addText(String(node.label), {
      x: X(node.x + 8), y: Y(node.y + 5), w: W((node.width ?? 160) - 16), h: W((node.height ?? 70) - 10),
      fontFace: style.font, fontSize: Number(node.font_size ?? style.fontSize) * scale * 60,
      bold: String(node.font_weight ?? "600") !== "400", color: hex(node.text_color, style.textColor),
      margin: 0.02, align: "center", valign: "mid", breakLine: false, fit: "shrink",
    });
  }

  for (const label of edgeLabels) {
    if (!String(label.text ?? "").trim()) continue;
    const text = String(label.text);
    const widthPx = Math.max(62, text.length * 10 + 20);
    slide.addText(text, {
      x: X(label.x - widthPx / 2), y: Y(label.y - 14), w: W(widthPx), h: W(28),
      fontFace: style.font, fontSize: style.fontSize * 0.67 * scale * 60,
      color: label.color, bold: false, margin: 0.01, align: "center", valign: "mid",
      fill: { color: hex(spec.canvas.background, "FFFFFF"), transparency: 8 },
      line: { color: hex(spec.canvas.background, "FFFFFF"), transparency: 100 },
    });
  }

  if (String(spec.title ?? "").trim()) {
    slide.addText(String(spec.title), {
      x: X(40), y: Y(13), w: W(spec.canvas.width - 80), h: W(52),
      fontFace: style.font, fontSize: style.titleSize * scale * 72,
      color: style.textColor, bold: true, margin: 0, align: "center", valign: "mid", fit: "shrink",
    });
  }
  if (String(spec.subtitle ?? "").trim()) {
    slide.addText(String(spec.subtitle), {
      x: X(55), y: Y(62), w: W(spec.canvas.width - 110), h: W(34),
      fontFace: style.font, fontSize: style.subtitleSize * scale * 72,
      color: "5D6D7E", bold: false, margin: 0, align: "center", valign: "mid", fit: "shrink",
    });
  }
  if (String(spec.footer ?? "").trim()) {
    slide.addText(String(spec.footer), {
      x: X(spec.canvas.width * 0.45), y: Y(spec.canvas.height - 36), w: W(spec.canvas.width * 0.51), h: W(22),
      fontFace: style.font, fontSize: 9, color: "7B7D7D", margin: 0, align: "right", valign: "mid", fit: "shrink",
    });
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  await pptx.writeFile({ fileName: outputPath });
  console.log(`rendered: ${outputPath}`);
}

main().catch((error) => {
  console.error(`error: ${error.message}`);
  process.exit(2);
});
