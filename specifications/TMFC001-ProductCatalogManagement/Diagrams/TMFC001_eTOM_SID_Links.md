# TMFC001 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram (page 8 of 28),
verified by tracing every line and arrowhead in the rendered page image at up to 600 dpi, cropped tightly
around each connector to confirm which cylinder/box every curve actually terminates at. The component-root
`TMFC001_Product_Catalog_Management.pdf` had already been overwritten by this skill's own generated output
in an earlier run before this file existed, so the true original was recovered from git history (commit
`78aba22`, "Add files via upload" — the initial upload predating any skill-generated regeneration).

Both eTOM boxes in the diagram connect, bidirectionally, to all 6 SID entities (2 x 6 = 12 links total).
The existing `TMFC001_eTOM_SID.svg` currently encodes only 7 of these 12 links (it is missing box 1's links
to Party Product Specification and Offering / Product Configuration / Loyalty, and box 2's links to Product
Specification / Product Usage) — that file needs to be regenerated from this corrected link set.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| 1.2.7 Product Specification & Offering Development & Retirement | Product Offering Specification | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Offering_Specification_ABE\|v25.0 |
| 1.2.7 Product Specification & Offering Development & Retirement | Product Specification | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Specification_ABE\|v25.0 |
| 1.2.7 Product Specification & Offering Development & Retirement | Product Usage | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Usage_ABE\|Product_Usage_Specification_ABE\|v25.0 |
| 1.2.7 Product Specification & Offering Development & Retirement | Party Product Specification and Offering | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Business_Partner_Domain\|Party_Product_Specification_and_Offering_ABE\|v25.0 |
| 1.2.7 Product Specification & Offering Development & Retirement | Product Configuration | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Configuration_ABE\|ProductConfigSpec_BE\|v25.0 |
| 1.2.7 Product Specification & Offering Development & Retirement | Loyalty | bidirectional | 1.2.7\|Product_Specification_&_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Loyalty_ABE\|Loyalty_Program_Specification_ABE\|v25.0 |
| 1.2.23 Product Specification Management | Product Offering Specification | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Product_Domain\|Product_Offering_Specification_ABE\|v25.0 |
| 1.2.23 Product Specification Management | Product Specification | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Product_Domain\|Product_Specification_ABE\|v25.0 |
| 1.2.23 Product Specification Management | Product Usage | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Product_Domain\|Product_Usage_ABE\|Product_Usage_Specification_ABE\|v25.0 |
| 1.2.23 Product Specification Management | Party Product Specification and Offering | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Business_Partner_Domain\|Party_Product_Specification_and_Offering_ABE\|v25.0 |
| 1.2.23 Product Specification Management | Product Configuration | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Product_Domain\|Product_Configuration_ABE\|ProductConfigSpec_BE\|v25.0 |
| 1.2.23 Product Specification Management | Loyalty | bidirectional | 1.2.23\|Product_Specification_Management\|v24.0 | Product_Domain\|Loyalty_ABE\|Loyalty_Program_Specification_ABE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Product Offering Specification | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Offering_Specification_ABE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Product Specification | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Specification_ABE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Product Usage | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Usage_ABE\|Product_Usage_Specification_ABE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Party Product Specification and Offering | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Business_Partner_Domain\|Party_Product_Specification_and_Offering_ABE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Product Configuration | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Product_Configuration_ABE\|ProductConfigSpec_BE\|v25.0 |
| 1.6.4 Business Partner Offering Development & Retirement | Loyalty | bidirectional | 1.6.4\|Business_Partner_Offering_Development_&_Retirement\|v24.0 | Product_Domain\|Loyalty_ABE\|Loyalty_Program_Specification_ABE\|v25.0 |
