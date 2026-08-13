# TMFC036 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Contact/Lead/Prospect Management | Sales Lead ABE | bidirectional | 1.1.11\|Contact/Lead/Prospect_Management\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| Market Sales Support & Readiness | Sales Lead ABE | bidirectional | 1.1.7\|Market_Sales_Support_&_Readiness\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| Market Sales Support & Readiness | Sales Opportunity ABE | activity produces | 1.1.7\|Market_Sales_Support_&_Readiness\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Opportunity_ABE\|v25.0 |
| Selling | Sales Lead ABE | activity consumes | 1.1.9\|Selling\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| Selling | Sales Opportunity ABE | activity consumes | 1.1.9\|Selling\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Opportunity_ABE\|v25.0 |
