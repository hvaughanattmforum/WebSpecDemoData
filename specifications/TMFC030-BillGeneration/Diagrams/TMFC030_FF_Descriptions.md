# TMFC030 Functional Framework Function Descriptions

Source: transcribed from `TMFC030_ Bill Generation Management 3.1.0 (TAC-1316) (Gen 5 APIs)-v9-Fx_only_source.docx`, section 2.4 (Functional Framework Functions),
gap-filled from the Functional Framework spreadsheet for IDs the document scores out or omits.

| Function ID | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 | Version | Document Name | Alignment Notes |
|---|---|---|---|---|---|---|
| 65 | Bill Image Presentation provides presentation of an exact bill image or after invoking a transactional document generation function. | Invoice Management | Invoicing | v24.0 | Bill Image Presentation | Matches YAML (v23.0) |
| 62 | Invoice Items Listing lists all invoice items for a specific invoice. | Invoice Management | Invoicing | v24.0 | Invoice Items Listing | Matches YAML (v23.0) |
| 63 | Invoice Listing function will list all invoices for a customer both over time and for customers with multiple invoices. | Invoice Management | Invoicing | v24.0 | Invoice Listing | Matches YAML (v23.0) |
| 329 | "Invoice Tax Calculation provides the necessary functionality to calculate taxes, including surcharges and fees, where applicable. / This function can occur within the Invoicing application or through the use of an external Tax module." | Invoice Management | Invoicing | v24.0 | Invoice Tax Calculation | Matches YAML (v23.0) |
| 309 | Provides the means to calculate the balance due for an invoice/bill. | Invoice Management | Invoicing | v24.0 | Invoice Balance Calculation | Matches YAML (v23.0) |
| 310 | Invoice Charges Compilation assembles charges (including charge distribution- charges incurred by other customers), credits, taxes, fees and adjustments that affect the balance due. | Invoice Management | Invoicing | v24.0 | Invoice Charges Compilation | Matches YAML (v23.0) |
| 312 | Provides appropriate levels of detail regarding items on the invoice. This detail is provided to revenue reporting and/or Bill Format &; Render. | Invoice Management | Invoicing | v24.0 | Invoice Detail Collection | Matches YAML (v23.0) |
| 311 | Provides subtotals and totals at various levels. | Invoice Management | Invoicing | v24.0 | Invoice Totals Calculation | Matches YAML (v23.0) |
