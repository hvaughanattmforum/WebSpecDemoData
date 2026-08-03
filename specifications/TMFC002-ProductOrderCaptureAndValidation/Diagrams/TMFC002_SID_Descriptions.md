# TMFC002 SID Descriptions

Source: TMFC002_Product_Order_Capture_Validation_v2.1.1.pdf (Section 2.2)

| SID ABE Level 1 | SID ABE L1 Definition | SID ABE Level 2 | SID ABE L2 Definition | Source |
|---|---|---|---|---|
| Customer Product Order | Handles single customer orders and the various types thereof, such as regulated and non-regulated orders. | SalesQuote | Sales Quote Business Entity - manages quote information for customer product orders | v2.1.1 PDF |
| Customer Product Order | Handles single customer orders and the various types thereof, such as regulated and non-regulated orders. | ShoppingCart | Shopping Cart Business Entity - manages shopping cart items and state for customer product orders | v2.1.1 PDF |

## Notes

- The Product Order Capture & Validation component will also trigger creation and update of Product but this information is managed by a dedicated component TMFC005 - Product Inventory.
- All L2 entities under Customer Product Order ABE are implemented.
