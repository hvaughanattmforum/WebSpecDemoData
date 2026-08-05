# TMFC003 eTOM–SID Links

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Order processing | Customer Product Order | bidirectional | 1.3.3\|Customer_Order_Processing_Management\|v25.5 | Customer_Domain\|Customer_Product_Order_ABE\|v25.5 |
| Product Order Management | Product Order | bidirectional | 1.2.27\|Product_Order_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
| Product Order Management | Customer Product Order | activity consumes | 1.2.27\|Product_Order_Management\|v25.5 | Customer_Domain\|Customer_Product_Order_ABE\|v25.5 |
| Service Activation | Product Order | activity consumes | 1.4.5\|Service_Activation_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
| Partner Order Management | Partner Order  | bidirectional | 1.6.8\|Business_Partner_Order_Management\|v25.5 | Business_Partner_Domain\|Business_Partner_Product_Order_ABE\|v25.5 |
| Partner Order Management | Product Order | activity consumes | 1.6.8\|Business_Partner_Order_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
