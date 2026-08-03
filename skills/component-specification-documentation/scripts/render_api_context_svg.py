"""
Generate the "API Context" diagram for a TMFCxxx component as a hand-drawn SVG.

Why this exists: PlantUML's automatic (Graphviz) layout cannot give each API its own straight,
individually-anchored connector at a chosen height on the component box -- it bundles same-side
edges toward roughly one attachment point regardless of box size or spacing hints. This script
draws the diagram directly with exact coordinates instead, guaranteeing:
  - a black component box, sized to fit its contents (not shrink-wrapped)
  - dependent APIs as straight-line sockets, one per API, evenly spaced down the left edge
  - exposed APIs as straight-line lollipops, one per API, evenly spaced down the right edge
  - eTOM activities as rectangles inside the box, grouped near the top
  - SID entities as cylinders inside the box, grouped near the bottom

Usage:
    python render_api_context_svg.py output.svg
(the __main__ block below has the TMFC005 data as a worked example -- for another component,
call build_svg() directly with that component's own lists, or adapt the __main__ block)
"""
import sys
from xml.sax.saxutils import escape as _esc

ROW_HEIGHT = 60
LABEL_COL_WIDTH = 380
BOX_WIDTH = 480
TOP_MARGIN = 40
BOTTOM_MARGIN = 40
CIRCLE_R = 8
FONT = "Helvetica, Arial, sans-serif"


def _wrap_two_lines(id_text, name_text):
    return id_text, name_text


def _socket_arc(cx, cy, r, side):
    """A small arc ')' or '(' bracket next to the circle, on the side facing the component box."""
    if side == "left":
        # box is to the right of the circle -> bracket opens toward the box (right side of circle)
        x = cx + r + 3
        return f'<path d="M {x} {cy-r} A {r} {r} 0 0 1 {x} {cy+r}" fill="none" stroke="black" stroke-width="1.5"/>'
    else:
        x = cx - r - 3
        return f'<path d="M {x} {cy-r} A {r} {r} 0 0 0 {x} {cy+r}" fill="none" stroke="black" stroke-width="1.5"/>'


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
    ty = y + h/2 + ellipse_h/4 - (len(lines)-1)*7
    for line in lines:
        parts.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="black">{_esc(line)}</text>')
        ty += 16
    return "\n".join(parts)


def _rectangle(x, y, w, h, label, dashed=False):
    dash = ' stroke-dasharray="6,3"' if dashed else ""
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" stroke-width="1.5"{dash}/>']
    lines = label.split("\n")
    ty = y + h/2 - (len(lines)-1)*7 + 5
    for line in lines:
        parts.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="black">{_esc(line)}</text>')
        ty += 16
    return "\n".join(parts)


def build_svg(component_id, component_name, dependent_apis, exposed_apis, etom_entries, sid_entries):
    """
    dependent_apis / exposed_apis: list of {"id": "TMF620", "name": "Product Catalog Management API"}
    etom_entries / sid_entries: list of label strings (each may contain \n for a second line)
    """
    n_left = max(len(dependent_apis), 1)
    n_right = max(len(exposed_apis), 1)
    box_height = max(n_left, n_right) * ROW_HEIGHT
    # make sure the box is also tall enough for its internal content
    inner_needed = 70 + len(etom_entries) * 85 + 60 + len(sid_entries) * 85 + 40
    box_height = max(box_height, inner_needed)

    box_x = LABEL_COL_WIDTH
    box_y = TOP_MARGIN
    canvas_w = LABEL_COL_WIDTH * 2 + BOX_WIDTH
    canvas_h = box_height + TOP_MARGIN + BOTTOM_MARGIN

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" '
           f'font-family="{FONT}">']
    svg.append(f'<rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>')

    # component box
    svg.append(f'<rect x="{box_x}" y="{box_y}" width="{BOX_WIDTH}" height="{box_height}" fill="black" stroke="black"/>')
    svg.append(f'<text x="{box_x+BOX_WIDTH/2}" y="{box_y+30}" text-anchor="middle" '
                f'font-size="16" font-weight="bold" fill="white">{_esc(component_id)}</text>')
    svg.append(f'<text x="{box_x+BOX_WIDTH/2}" y="{box_y+50}" text-anchor="middle" '
                f'font-size="16" font-weight="bold" fill="white">{_esc(component_name)}</text>')

    inner_x = box_x + 30
    inner_w = BOX_WIDTH - 60
    y = box_y + 75
    for entry in etom_entries:
        svg.append(_rectangle(inner_x, y, inner_w, 70, entry, dashed=True))
        y += 85
    sid_block_h = len(sid_entries) * 85 - 15
    y = box_y + box_height - 20 - sid_block_h
    for entry in sid_entries:
        svg.append(_cylinder(inner_x, y, inner_w, 70, entry))
        y += 85

    # dependent APIs -- left edge, straight individual sockets
    for i, api in enumerate(dependent_apis):
        cy = box_y + (i + 0.5) * (box_height / n_left)
        cx = box_x - 40
        svg.append(f'<line x1="{box_x}" y1="{cy}" x2="{cx}" y2="{cy}" stroke="black" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{CIRCLE_R}" fill="white" stroke="black" stroke-width="1.5"/>')
        svg.append(_socket_arc(cx, cy, CIRCLE_R, "left"))
        id_text, name_text = _wrap_two_lines(api["id"], api["name"])
        tx = cx - CIRCLE_R - 10
        svg.append(f'<text x="{tx}" y="{cy-6}" text-anchor="end" font-size="13" font-weight="bold" fill="black">{_esc(id_text)}</text>')
        svg.append(f'<text x="{tx}" y="{cy+10}" text-anchor="end" font-size="12" fill="black">{_esc(name_text)}</text>')

    # exposed APIs -- right edge, straight individual lollipops
    for j, api in enumerate(exposed_apis):
        cy = box_y + (j + 0.5) * (box_height / n_right)
        cx = box_x + BOX_WIDTH + 40
        svg.append(f'<line x1="{box_x+BOX_WIDTH}" y1="{cy}" x2="{cx}" y2="{cy}" stroke="black" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{cx}" cy="{cy}" r="{CIRCLE_R}" fill="white" stroke="black" stroke-width="1.5"/>')
        id_text, name_text = _wrap_two_lines(api["id"], api["name"])
        tx = cx + CIRCLE_R + 10
        svg.append(f'<text x="{tx}" y="{cy-6}" text-anchor="start" font-size="13" font-weight="bold" fill="black">{_esc(id_text)}</text>')
        svg.append(f'<text x="{tx}" y="{cy+10}" text-anchor="start" font-size="12" fill="black">{_esc(name_text)}</text>')

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    dependent_apis = [
        {"id": "TMF620", "name": "Product Catalog Management API"},
        {"id": "TMF669", "name": "Party Role Management API"},
        {"id": "TMF639", "name": "Resource Inventory Management API"},
        {"id": "TMF651", "name": "Agreement Management API"},
        {"id": "TMF673", "name": "Geographic Address Management API"},
        {"id": "TMF674", "name": "Geographic Site Management API"},
        {"id": "TMF675", "name": "Geographic Location Management API"},
        {"id": "TMF666", "name": "Account Management API"},
        {"id": "TMF632", "name": "Party Management API"},
        {"id": "TMF637", "name": "Product Inventory Management API (dependent)"},
        {"id": "TMF638", "name": "Service Inventory Management API"},
        {"id": "TMF622", "name": "Product Ordering Management API"},
    ]
    exposed_apis = [
        {"id": "TMF637", "name": "Product Inventory Management API"},
        {"id": "TMF701", "name": "Process Flow Management API"},
    ]
    etom_entries = [
        "1.2.11\nProduct Inventory Management",
        "1.1.19 / 1.1.19.2\nLoyalty Program Management /\nLoyalty Program Operation",
    ]
    sid_entries = [
        "Product and Offering\nInstance / Product",
        "ProductOfferingInstance",
        "Loyalty / Loyalty Program",
    ]

    svg = build_svg("TMFC005", "Product Inventory", dependent_apis, exposed_apis, etom_entries, sid_entries)
    out_path = sys.argv[1] if len(sys.argv) > 1 else "TMFC005_API_Context.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", out_path)
