# TMFC036 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| L2 - Contact/Lead/Prospect Management | Sales Lead | bidirectional | 1.1.11\|Contact/Lead/Prospect_Management\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| L2 - Market Sales Support & Readiness | Sales Lead | bidirectional | 1.1.7\|Market_Sales_Support_&_Readiness\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| L2 - Market Sales Support & Readiness | Sales Opportunity | activity produces | 1.1.7\|Market_Sales_Support_&_Readiness\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Opportunity_ABE\|v25.0 |
| L2 - Selling | Sales Lead | activity consumes | 1.1.9\|Selling\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Lead_ABE\|v25.0 |
| L2 - Selling | Sales Opportunity | activity consumes | 1.1.9\|Selling\|v23.0 | Market_&_Sales_Domain\|Sales_Lead_and_Opportunity_ABE\|Sales_Opportunity_ABE\|v25.0 |
