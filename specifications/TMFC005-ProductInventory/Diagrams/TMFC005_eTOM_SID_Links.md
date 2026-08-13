# TMFC005 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Product Inventory Management | ProductOfferingInstance | bidirectional | 1.2.11\|Product_Inventory_Management\|v24.0 | **NO MATCH** |
| Product Inventory Management | Product ABE | bidirectional | 1.2.11\|Product_Inventory_Management\|v24.0 | Product_Domain\|Product_and_Offering_Instance_ABE\|Product_ABE\|v25.0 |
| Product Inventory Management | Loyalty Program ABE | activity consumes | 1.2.11\|Product_Inventory_Management\|v24.0 | Product_Domain\|Loyalty_ABE\|Loyalty_Program_ABE\|v25.0 |
| Loyalty Program Management / Loyalty Program Operation | Loyalty Program ABE | bidirectional | 1.1.19\|Loyalty_Program_Management\|v24.0; 1.1.19.2\|Loyalty_Program_Operation\|v24.0 | Product_Domain\|Loyalty_ABE\|Loyalty_Program_ABE\|v25.0 |
