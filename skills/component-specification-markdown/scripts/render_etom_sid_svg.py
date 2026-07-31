"""
Generate the "eTOM L2 - SID ABEs links" diagram (section 2.3) for a TMFCxxx component as a
hand-drawn SVG, for use once the diagram has more than 6 total eTOM+SID elements.

Why this exists: below ~6 elements, plain PlantUML `@startuml` rectangle/database layout with
<--> arrows renders fine. Past that, Graphviz's automatic layout starts crossing lines and
reordering boxes unpredictably -- the same class of problem the API context diagram has. This
draws eTOM activities in a left column and SID entities in a right column, giving every link its
own individually-anchored point on whichever box(es) it touches (spread evenly across that box's
edge) instead of letting automatic layout bundle same-side edges toward one spot.

Usage:
    from render_etom_sid_svg import build_svg
    svg = build_svg(
        component_id="TMFC010",
        etom_entries=[{"key": "ETOM_LIFECYCLE", "label": "L2 - Resource Catalog Lifecycle Management"}, ...],
        sid_entries=[{"key": "SID_SPEC", "label": "Resource Specification ABE"}, ...],
        links=[{"etom": "ETOM_LIFECYCLE", "sid": "SID_SPEC", "direction": "bidirectional"}, ...],
    )
    # direction is one of "produced" (etom -> sid, activity produces the info),
    # "consumed" (sid -> etom, activity consumes the info), or "bidirectional"
"""
import math
import sys
from collections import defaultdict
from xml.sax.saxutils import escape as _esc

BOX_W = 260
BOX_H = 70
BOX_GAP = 30
COL_GAP = 260
MARGIN = 40
TITLE_H = 40
LEGEND_W = 260
FONT = "Helvetica, Arial, sans-serif"
ARROW_LEN = 12
ARROW_W = 8


def _arrowhead(px, py, ux, uy):
    """A filled triangle with its tip at (px, py), pointing along unit vector (ux, uy).

    Drawn as an explicit polygon rather than an SVG <marker> -- svglib (used to rasterize
    this diagram for the PDF and PNG fallback) silently drops <marker> elements entirely,
    which would make the produced/consumed direction vanish without warning.
    """
    bx, by = px - ARROW_LEN * ux, py - ARROW_LEN * uy
    lx, ly = bx + ARROW_W / 2 * -uy, by + ARROW_W / 2 * ux
    rx, ry = bx - ARROW_W / 2 * -uy, by - ARROW_W / 2 * ux
    return f'<polygon points="{px},{py} {lx},{ly} {rx},{ry}" fill="black"/>'


def _rect_dashed(x, y, w, h, label):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" '
             f'stroke-width="1.5" stroke-dasharray="6,3"/>']
    lines = label.split("\n")
    ty = y + h / 2 - (len(lines) - 1) * 7 + 5
    for line in lines:
        parts.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="{FONT}" '
                      f'font-size="12" fill="black">{_esc(line)}</text>')
        ty += 15
    return "\n".join(parts)


def _cylinder(x, y, w, h, label):
    ellipse_h = h * 0.22
    parts = [
        f'<path d="M {x} {y+ellipse_h/2} '
        f'L {x} {y+h-ellipse_h/2} '
        f'A {w/2} {ellipse_h/2} 0 0 0 {x+w} {y+h-ellipse_h/2} '
        f'L {x+w} {y+ellipse_h/2} '
        f'A {w/2} {ellipse_h/2} 0 0 0 {x} {y+ellipse_h/2} Z" '
        f'fill="white" stroke="black" stroke-width="1.5"/>',
        f'<ellipse cx="{x+w/2}" cy="{y+ellipse_h/2}" rx="{w/2}" ry="{ellipse_h/2}" '
        f'fill="white" stroke="black" stroke-width="1.5"/>',
    ]
    lines = label.split("\n")
    ty = y + h / 2 + ellipse_h / 4 - (len(lines) - 1) * 7
    for line in lines:
        parts.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="{FONT}" '
                      f'font-size="12" fill="black">{_esc(line)}</text>')
        ty += 15
    return "\n".join(parts)


def build_svg(component_id, etom_entries, sid_entries, links):
    n_etom, n_sid = len(etom_entries), len(sid_entries)
    etom_col_h = n_etom * BOX_H + max(n_etom - 1, 0) * BOX_GAP
    sid_col_h = n_sid * BOX_H + max(n_sid - 1, 0) * BOX_GAP
    col_h = max(etom_col_h, sid_col_h)

    etom_x = MARGIN
    sid_x = MARGIN + BOX_W + COL_GAP
    canvas_w = sid_x + BOX_W + MARGIN + LEGEND_W
    canvas_h = col_h + MARGIN * 2 + TITLE_H

    etom_y0 = MARGIN + TITLE_H + (col_h - etom_col_h) / 2
    sid_y0 = MARGIN + TITLE_H + (col_h - sid_col_h) / 2

    etom_pos = {e["key"]: etom_y0 + i * (BOX_H + BOX_GAP) for i, e in enumerate(etom_entries)}
    sid_pos = {s["key"]: sid_y0 + i * (BOX_H + BOX_GAP) for i, s in enumerate(sid_entries)}

    etom_link_count, sid_link_count = defaultdict(int), defaultdict(int)
    for link in links:
        etom_link_count[link["etom"]] += 1
        sid_link_count[link["sid"]] += 1
    etom_seen, sid_seen = defaultdict(int), defaultdict(int)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" '
           f'font-family="{FONT}">',
           f'<rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>',
           f'<text x="{MARGIN}" y="{MARGIN + 15}" font-size="16" font-weight="bold" fill="black">'
           f'{_esc(component_id)} eTOM L2 - SID ABEs links</text>']

    # links drawn before boxes so the boxes' fill covers the line ends cleanly
    for link in links:
        ex, ey_base = etom_x + BOX_W, etom_pos[link["etom"]]
        count_e, idx_e = etom_link_count[link["etom"]], etom_seen[link["etom"]]
        etom_seen[link["etom"]] += 1
        ey = ey_base + (idx_e + 1) * (BOX_H / (count_e + 1))

        sx, sy_base = sid_x, sid_pos[link["sid"]]
        count_s, idx_s = sid_link_count[link["sid"]], sid_seen[link["sid"]]
        sid_seen[link["sid"]] += 1
        sy = sy_base + (idx_s + 1) * (BOX_H / (count_s + 1))

        dx, dy = sx - ex, sy - ey
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist

        direction = link["direction"]
        svg.append(f'<line x1="{ex}" y1="{ey}" x2="{sx}" y2="{sy}" stroke="black" stroke-width="1.5"/>')
        if direction in ("produced", "bidirectional"):
            svg.append(_arrowhead(sx, sy, ux, uy))
        if direction in ("consumed", "bidirectional"):
            svg.append(_arrowhead(ex, ey, -ux, -uy))

    for e in etom_entries:
        svg.append(_rect_dashed(etom_x, etom_pos[e["key"]], BOX_W, BOX_H, e["label"]))
    for s in sid_entries:
        svg.append(_cylinder(sid_x, sid_pos[s["key"]], BOX_W, BOX_H, s["label"]))

    lx, ly = sid_x + BOX_W + 50, MARGIN + TITLE_H
    svg.append(f'<rect x="{lx}" y="{ly-10}" width="20" height="14" fill="white" stroke="black" '
                f'stroke-width="1.5" stroke-dasharray="4,2"/>')
    svg.append(f'<text x="{lx+30}" y="{ly}" font-size="12" fill="black">eTOM Business Activity</text>')
    ly += 28
    svg.append(f'<ellipse cx="{lx+10}" cy="{ly-4}" rx="10" ry="6" fill="white" stroke="black" stroke-width="1.5"/>')
    svg.append(f'<text x="{lx+30}" y="{ly}" font-size="12" fill="black">SID Data Entity</text>')
    ly += 28
    svg.append(f'<line x1="{lx}" y1="{ly-4}" x2="{lx+24}" y2="{ly-4}" stroke="black" stroke-width="1.5"/>')
    svg.append(_arrowhead(lx + 24, ly - 4, 1, 0))
    svg.append(f'<text x="{lx+34}" y="{ly}" font-size="12" fill="black">produced by the activity</text>')
    ly += 24
    svg.append(f'<line x1="{lx}" y1="{ly-4}" x2="{lx+24}" y2="{ly-4}" stroke="black" stroke-width="1.5"/>')
    svg.append(_arrowhead(lx, ly - 4, -1, 0))
    svg.append(f'<text x="{lx+34}" y="{ly}" font-size="12" fill="black">consumed by the activity</text>')

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    etom_entries = [
        {"key": "ETOM_LIFECYCLE", "label": "L2 - Resource Catalog Lifecycle Management"},
        {"key": "ETOM_OPREADY", "label": "L2 - Resource Catalog Operational Readiness Management"},
        {"key": "ETOM_CONTENT", "label": "L2 - Resource Catalog Content Management"},
        {"key": "ETOM_PLANNING", "label": "L2 - Resource Catalog Planning Management"},
        {"key": "ETOM_SPECMGMT", "label": "L2 - Resource Specification Management"},
        {"key": "ETOM_DEVRETIRE", "label": "L2 - Resource Specification Development & Retirement"},
    ]
    sid_entries = [
        {"key": "SID_SPEC", "label": "Resource Specification ABE"},
        {"key": "SID_USAGE", "label": "Resource Usage ABE"},
        {"key": "SID_PERF", "label": "Resource Performance ABE"},
        {"key": "SID_CONFIG", "label": "Resource Configuration ABE"},
    ]
    links = [
        {"etom": "ETOM_LIFECYCLE", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_OPREADY", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_SPECMGMT", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_PLANNING", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_CONTENT", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_CONTENT", "sid": "SID_USAGE", "direction": "bidirectional"},
        {"etom": "ETOM_CONTENT", "sid": "SID_PERF", "direction": "bidirectional"},
        {"etom": "ETOM_CONTENT", "sid": "SID_CONFIG", "direction": "bidirectional"},
        {"etom": "ETOM_DEVRETIRE", "sid": "SID_SPEC", "direction": "bidirectional"},
        {"etom": "ETOM_DEVRETIRE", "sid": "SID_USAGE", "direction": "bidirectional"},
        {"etom": "ETOM_DEVRETIRE", "sid": "SID_PERF", "direction": "bidirectional"},
        {"etom": "ETOM_DEVRETIRE", "sid": "SID_CONFIG", "direction": "bidirectional"},
    ]

    svg = build_svg("TMFC010", etom_entries, sid_entries, links)
    out_path = sys.argv[1] if len(sys.argv) > 1 else "TMFC010_eTOM_SID.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", out_path)
