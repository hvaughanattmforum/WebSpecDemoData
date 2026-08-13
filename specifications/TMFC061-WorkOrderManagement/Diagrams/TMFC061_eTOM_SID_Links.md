# TMFC061 eTOM–SID Links

Source: transcribed from the original PDF's "2.3. eTOM L2 - SID ABEs links" diagram — embedded as a raster
image at the *top* of the page immediately following the "2.3." heading's own page (the heading's own page
ends with only the intro sentence "eTOM L2 vS SID ABEs links for this ODA Component.", then the picture
starts at the top of the next page, directly above that page's "2.4. Functional Framework Functions"
heading — same page-boundary pattern documented elsewhere in this skill for raster-embedded diagrams).
Recovered from git history (this component's original `TMFC061_Work_Order_Management.pdf` had already been
overwritten by this skill's own generated output before this file existed — the true original was
retrieved via `git show HEAD:...` on the branch's starting commit).

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Resource Specification Management | Work Specification ABE | bidirectional | 1.5.19\|Resource_Specification_Management\|v23.5 | Enterprise_Domain\|Workforce_ABE\|Work_Specification_ABE\|v25.0 |
| Resource Order Management / Manage Resource Work Order | Work Specification ABE | activity consumes | 1.5.5\|Resource_Order_Management\|v23.5; 1.5.5.7\|Manage_Resource_Work_Order\|v23.5 | Enterprise_Domain\|Workforce_ABE\|Work_Specification_ABE\|v25.0 |
| Resource Order Management / Manage Resource Work Order | Work Order ABE | activity produces | 1.5.5\|Resource_Order_Management\|v23.5; 1.5.5.7\|Manage_Resource_Work_Order\|v23.5 | Product_Domain\|Project_ABE\|Work_Order_ABE\|v25.0 |

Naming note: the diagram's second box is hand-labeled "Resource Order Management/Manage Resource Order"
(word order/wording differs slightly from the current YAML's "Manage Resource **Work** Order") — read as
the same L3 activity by context (it's the only L3 child of 1.5.5 in the YAML), not a different one.
