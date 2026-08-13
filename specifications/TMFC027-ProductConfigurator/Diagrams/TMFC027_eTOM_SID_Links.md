# TMFC027 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram (page 6), verified by
tracing every line and arrowhead in the rendered page image (embedded raster, not vector — no `<line>`
elements to extract programmatically, so each connector was confirmed visually at up to 1200 dpi crops);
cross-checked against the line count already present in the existing `TMFC027_eTOM_SID.svg`. That existing
SVG contains 6 lines/SID boxes, but only 3 of them are backed by an actual connector in the original PDF —
the other 3 ("Product Offering", "Party Product Spec. & Offering", "Product Configuration**", all inside the
TMFC001 - Product Catalog group) are drawn in the PDF purely as sibling context boxes within that group with
no line/arrowhead reaching them. Of the 3 links that are real, only the one below remains applicable — the
other two pointed to `Product_Specification_ABE` and `Product_and_Offering_Instance_ABE|Product_ABE`, SIDs
that were removed from this component's YAML as cross-component duplicates (owned by TMFC001 and TMFC005
respectively).

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Product Configuration Management | ProductConfiguration BE | bidirectional | 1.2.5\|Product_Configuration_Management\|v25.0 | Product_Domain\|Product_Configuration_ABE\|ProductConfiguration_BE\|v25.0 |
