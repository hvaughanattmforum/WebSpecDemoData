// Assembles a component-specification-markdown .docx from the JSON payload build_docx.py
// produces. Kept deliberately dumb: all Markdown/YAML interpretation happens in Python;
// this file only turns already-parsed blocks into docx-js objects.
//
// Usage: node build_docx.js payload.json
"use strict";

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, Header, Footer, PageNumber, TableOfContents, PageBreak,
  VerticalAlign,
} = require("docx");

const TMF_RED = "C00000";
const TMF_DARK_GRAY = "404040";
const TABLE_HEADER_BG = "EFEFEF";

// A4 page, same margins (in points, converted to twips: 1pt = 20 twips) as build_pdf.py's
// BASE_CSS `@page` rule, so the Word doc paginates similarly to the PDF.
const PAGE_WIDTH = 11906, PAGE_HEIGHT = 16838;
const MARGIN_TOP = 2000, MARGIN_BOTTOM = 1200, MARGIN_LR = 1200;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LR * 2;

const LOGO_W = 70, LOGO_H = 58.5; // points; matches build_pdf.py's LOGO_W/LOGO_H

function pngSize(filePath) {
  const buf = fs.readFileSync(filePath);
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

function runsToTextRuns(runs, extra) {
  return runs.map(r => new TextRun({
    text: r.text,
    bold: !!r.bold || (extra && extra.bold),
    italics: !!(extra && extra.italics),
    font: r.code ? "Courier New" : undefined,
    size: extra && extra.size,
    color: extra && extra.color,
  }));
}

function headingLevelFor(level) {
  // level 2 (##) -> chapter, 3 (###) -> section, 4 (####) -> sub-section. The doc title
  // (level 1, #) is handled separately and deliberately isn't a Heading style, so Word's
  // TableOfContents field (headingStyleRange "1-3") never picks it up -- same as
  // build_pdf.py's _extract_headings explicitly skipping the H1 title.
  return { 2: HeadingLevel.HEADING_1, 3: HeadingLevel.HEADING_2, 4: HeadingLevel.HEADING_3 }[level];
}

function buildImageParagraph(block, basePath) {
  const absPath = path.isAbsolute(block.path) ? block.path : path.join(basePath, block.path);
  const { width, height } = pngSize(absPath);
  const maxWidthPx = (CONTENT_WIDTH / 1440) * 96; // twips -> inches -> px @96dpi
  const scale = Math.min(1, maxWidthPx / width);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 80 },
    children: [new ImageRun({
      data: fs.readFileSync(absPath),
      type: "png",
      transformation: { width: Math.round(width * scale), height: Math.round(height * scale) },
    })],
  });
}

function buildTable(block) {
  const colWidths = block.colWidthsPct.map(pct => Math.round(CONTENT_WIDTH * pct / 100));
  const headerRow = new TableRow({
    tableHeader: true,
    children: block.header.map((cellRuns, j) => new TableCell({
      width: { size: colWidths[j], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: TABLE_HEADER_BG },
      verticalAlign: VerticalAlign.TOP,
      margins: { top: 60, bottom: 60, left: 80, right: 80 },
      children: [new Paragraph({ children: runsToTextRuns(cellRuns, { bold: true, size: 18 }) })],
    })),
  });
  const bodyRows = block.rows.map(row => new TableRow({
    children: row.map((cellRuns, j) => new TableCell({
      width: { size: colWidths[j], type: WidthType.DXA },
      verticalAlign: VerticalAlign.TOP,
      margins: { top: 60, bottom: 60, left: 80, right: 80 },
      children: [new Paragraph({ children: runsToTextRuns(cellRuns, { size: 18 }) })],
    })),
  }));
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...bodyRows],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
      left: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
      right: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    },
  });
}

function buildBullets(block) {
  return block.items.map(item => new Paragraph({
    bullet: { level: item.level },
    spacing: { after: 40 },
    children: runsToTextRuns(item.runs, { size: 22 }),
  }));
}

function buildBody(blocks, basePath) {
  const out = [];
  for (const block of blocks) {
    if (block.type === "heading") {
      out.push(new Paragraph({
        heading: headingLevelFor(block.level),
        children: runsToTextRuns(block.runs, { color: block.color }),
      }));
    } else if (block.type === "para") {
      out.push(new Paragraph({
        spacing: { after: 120 },
        children: runsToTextRuns(block.runs, { italics: block.italic, size: 22 }),
      }));
    } else if (block.type === "list") {
      out.push(...buildBullets(block));
    } else if (block.type === "table") {
      out.push(buildTable(block));
    } else if (block.type === "image") {
      out.push(buildImageParagraph(block, basePath));
    }
  }
  // A table can't be the last element in a document body (OOXML requires a trailing
  // paragraph) -- only add one here, not after every table, or every table gets an
  // unwanted blank-line gap before whatever follows it.
  if (blocks.length && blocks[blocks.length - 1].type === "table") {
    out.push(new Paragraph({ text: "" }));
  }
  return out;
}

function buildCoverAndNotice(payload) {
  const c = payload.cover;
  const fieldCell = (text) => new TableCell({
    width: { size: CONTENT_WIDTH / 2, type: WidthType.DXA },
    margins: { top: 100, bottom: 100, left: 160, right: 160 },
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, color: TMF_DARK_GRAY, size: 21 })],
    })],
  });
  const borders = {
    top: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    left: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    right: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
    insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "999999" },
  };

  const cover = [
    new Paragraph({
      spacing: { before: 1800 },
      children: [new TextRun({ text: "TM Forum Component", bold: true, color: TMF_RED, size: 40 })],
    }),
    new Paragraph({
      spacing: { before: 480 },
      children: [new TextRun({ text: c.displayName, bold: true, color: TMF_DARK_GRAY, size: 48 })],
    }),
    new Paragraph({ spacing: { before: 3600 }, children: [
      new TextRun({ text: c.id, bold: true, color: TMF_DARK_GRAY, size: 26 }),
    ] }),
    new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH / 2, CONTENT_WIDTH / 2],
      borders,
      rows: [
        new TableRow({ children: [
          fieldCell(`Maturity Level: ${c.maturityLevel}`),
          fieldCell(`Team Approved Date: ${c.teamApprovedDate}`),
        ] }),
        new TableRow({ children: [
          fieldCell(`Release Status: ${c.releaseStatus}`),
          fieldCell(`Approval Status: ${c.approvalStatus}`),
        ] }),
        new TableRow({ children: [
          fieldCell(`Version ${c.version}`),
          fieldCell("IPR Mode: RAND"),
        ] }),
      ],
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ];

  const notice = [
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
      new TextRun({ text: "Notice", bold: true, color: TMF_RED }),
    ] }),
    ...payload.notice.paragraphs.map(p => new Paragraph({
      spacing: { after: 120 },
      children: [new TextRun({ text: p, size: 20 })],
    })),
    new Paragraph({ children: [new PageBreak()] }),
  ];

  return [...cover, ...notice];
}

function buildHeader(runningTitle, logoPath, includeTitle) {
  // LOGO_W/LOGO_H are points (same fixed values build_pdf.py places via fitz.Rect); convert
  // to pixels at 96dpi for docx-js's ImageRun transformation, which stretches to whatever
  // width/height is given regardless of the source PNG's native resolution.
  const logoWidthPx = Math.round(LOGO_W * 96 / 72);
  const logoHeightPx = Math.round(LOGO_H * 96 / 72);
  const children = [];
  if (includeTitle) {
    children.push(new TextRun({ text: runningTitle, italics: true, size: 18 }));
  }
  return new Header({
    children: [new Paragraph({
      tabStops: [{ type: "right", position: CONTENT_WIDTH }],
      children: [
        ...children,
        new TextRun({ text: "\t" }),
        new ImageRun({
          data: fs.readFileSync(logoPath),
          type: "png",
          transformation: { width: logoWidthPx, height: logoHeightPx },
        }),
      ],
    })],
  });
}

function buildFooter(year) {
  return new Footer({
    children: [new Paragraph({
      tabStops: [{ type: "right", position: CONTENT_WIDTH }],
      children: [
        new TextRun({ text: `© TM Forum ${year}. All Rights Reserved.`, size: 18 }),
        new TextRun({ text: "\t" }),
        new TextRun({ text: "Page ", size: 18 }),
        new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
        new TextRun({ text: " of ", size: 18 }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 }),
      ],
    })],
  });
}

function main() {
  const payloadPath = process.argv[2];
  const payload = JSON.parse(fs.readFileSync(payloadPath, "utf-8"));
  const basePath = path.dirname(payloadPath);

  const doc = new Document({
    features: { updateFields: true }, // Word recomputes the ToC page numbers on open
    styles: {
      default: {
        document: { run: { font: "Calibri", size: 22 } },
      },
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN_TOP, bottom: MARGIN_BOTTOM, left: MARGIN_LR, right: MARGIN_LR },
        },
        titlePage: true,
      },
      headers: {
        default: buildHeader(payload.runningTitle, payload.logoPath, true),
        first: buildHeader(payload.runningTitle, payload.logoPath, false),
      },
      footers: {
        default: buildFooter(payload.notice.year),
      },
      children: [
        ...buildCoverAndNotice(payload),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ children: [new PageBreak()] }),
        new Paragraph({
          heading: HeadingLevel.TITLE,
          children: [new TextRun({ text: payload.docTitle, bold: true, color: TMF_RED, size: 44 })],
        }),
        ...buildBody(payload.blocks, basePath),
      ],
    }],
  });

  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(payload.outPath, buffer);
    console.log("wrote", payload.outPath);
  });
}

main();
