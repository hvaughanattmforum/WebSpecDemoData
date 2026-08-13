### 5.2. Jira References

- SID: to be updated to separate Customer Bill ABE from Party Bill ABE - ISA-847 - TMFC030: Bill
  Generation Management - SID update request (BACKLOG)
- eTOM: to review L3/L4 mapping for (FX-1225): Produce & Distribute Customer Bill; Pricing, Discounting,
  Adjustments & Rebates Application; BP Bill/Invoice Management
- OpenAPI: TMF678_Customer_Bill_Management remove following resources - AP-4648 - TMFC030: Bill
  Generation Management (DONE): Bill Cycle, Bill Cycle Specification
- ODA Component: add new component for Party Communication Mgmt

### 5.3. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 27-Sep-2023 | Gaetano Biancardi | Final edits prior to publication |
| 2.0.0 | 21-Nov-2023 | Gaetano Biancardi | Functional Framework added: 309 Invoice Balance Calculation, 310 Invoice Charges Compilation, 312 Invoice Detail Collection, 311 Invoice Totals Calculation; Open API: TMF666 removed "appliedCustomerBillingRate" resource and related API methods |
| 2.1.0 | 19-May-2024 | Gaetano Biancardi | Updated to new component template; updated to ODF v23.5; removed TMF672 as mandatory dependent API; exposed API removed: TMF688 Event Mgmt, TMF672 User Roles and Permissions; dependent API removed: TMF688 Event Mgmt |
| 2.1.0 | 12-Jul-2024 | Amaia White | Final edits prior to publication |
| 2.2.0 | 21-Oct-2024 | Gaetano Biancardi | Dependent API: added TMF678 Customer Bill Mgmt to retrieve appliedCustomerBillingRate; exposed API: added POST to TMF678 Customer Bill resource |
| 2.2.0 | 03-Dec-2024 | Elisabeth Andersson | Updated YAML file to remove TMF688 and TMF672 from the core specification, as the two APIs are moved to supporting functions |
| 2.2.0 | 27-Dec-2024 | Rosie Wilson | Final edits prior to publication |
| 3.0.0 | 28-Oct-2025 | Julien Rouland | Updated the SID part to include party bill cycle, and updated the exposed API resources associated (TMF678); removed following functions in overlap with bill calc: 1.3.9.4 Pricing, Discounting, Adjustments & Rebates Application, 1.3.9.4.2 Apply Pricing, Discounting, Adjustments & Rebates to Customer Account |
| 3.0.0 | 19-Nov-2025 | Rosie Wilson | Updated description; final edits prior to publication |
| 3.1.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 20-Oct-2023 | Amaia White | Initial release of document |
| Pre-production | 20-Nov-2023 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 20-Dec-2023 | Amaia White | New version release 2.0 |
| Production | 09-Feb-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 12-Jul-2024 | Amaia White | New version release 2.1.0 |
| Production | 30-Aug-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 27-Dec-2024 | Rosie Wilson | Updated to version 2.2.0 |
| Production | 07-Mar-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 19-Nov-2025 | Rosie Wilson | Updated to version 3.0.0 |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | Updated to version 3.1.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum ODA Components & Canvas team.

| Team Member | Company | Role |
|---|---|---|
| Gaetano Biancardi | Accenture | Editor |
| Sylvie Demarest | Orange | Reviewer |
| Elisabeth Andersson | MATRIXX | Additional Input |
| Julien Rouland | Orange | Editor |
| Rosie Wilson | TM Forum | Editor |
| Muhammad Salman Sami | Whalecloud | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Luca Icardi | Accenture | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |

