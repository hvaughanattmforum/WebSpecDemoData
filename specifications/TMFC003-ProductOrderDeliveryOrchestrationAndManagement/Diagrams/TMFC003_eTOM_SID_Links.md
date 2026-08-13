# TMFC003 eTOM–SID Links

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Customer Order Processing Management | Customer Product Order ABE | bidirectional | 1.3.3\|Customer_Order_Processing_Management\|v25.5 | Customer_Domain\|Customer_Product_Order_ABE\|v25.5 |
| Product Order Management | Product Order ABE | bidirectional | 1.2.27\|Product_Order_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
| Product Order Management | CustomerProductOfferingOrderItem BE | activity consumes | 1.2.27\|Product_Order_Management\|v25.5 | Customer_Domain\|Customer_Product_Order_ABE\|CustomerProductOfferingOrderItem_BE\|v25.5 |
| Service Activation Management | Product Order ABE | activity consumes | 1.4.5\|Service_Activation_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
| Business Partner Order Management | Business Partner Product Order ABE | bidirectional | 1.6.8\|Business_Partner_Order_Management\|v25.5 | Business_Partner_Domain\|Business_Partner_Product_Order_ABE\|v25.5 |
| Business Partner Order Management | Product Order ABE | activity consumes | 1.6.8\|Business_Partner_Order_Management\|v25.5 | Product_Domain\|Product_Order_ABE\|v25.5 |
