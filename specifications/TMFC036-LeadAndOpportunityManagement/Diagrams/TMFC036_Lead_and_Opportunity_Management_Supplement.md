### 5.2. Jira References

**eTOM**
- [ISA-710] 1.1.7.4 - Manage Sales Inventory to be reviewed: as currently defined this inventory mixes
  information related to Lead and Opportunities Management (sales prospects) and information related to
  customer orders (actual sales, sales commissions). Do we really need eTOM activities for inventories
  management? And if yes the scope here corresponds to historic CRM solutions we need to split in
  smaller pieces. This L3 needs to be reviewed and at least duplicate entries need to be deleted, and
  granularity of information managed needs to be improved.
- [ISA-711] eTOM 1.1.9 - Selling to be reviewed: this L2 mixes activities related to Opportunity and
  Sales Prospects, but also others related to quotation (sales proposal) or product order initialization
  (cross/up-sell, negotiate sales/contract). A clearer separation is needed.

**SID**
- [ISA-712] Sales Lead & Opportunity ABE improvements:
  - 2 level 2 ABEs could be created for Sales Lead and for Sales Opportunity
  - A relationship between Sales Lead (resp. Sales Opportunity) and Customer Product Order could be added
  - A relationship between Sales Opportunity and Agreement could also be added

**Functional Framework**
- [ISA-713] Functional FK - review Sales Opportunity Aggregate Function content: most of the functions
  classified in this Aggregate Function are not related to Sales Opportunity but to quotation or
  customer product order, so they need to be moved - or deleted if duplicates.

**Open APIs**
TMF699 Sales Management API:
- This API covers Sales Lead and Sales Opportunity management. Sales quotation, as announced in the
  introduction as covered later, is in fact already covered (or should be) by TMF648 Quote Management.
- In the resource model of this API the link between Sales Opportunity and Sales Quote BEs is missing.
- This API appears in the Early Adoption page only: it needs to be released soon.

### 5.3. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 13-Apr-2023 | Amaia White | Final edits prior to publication |
| 1.0.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. |
| 1.0.1 | 15-Aug-2023 | Amaia White | Final edits prior to publication |
| 1.1.0 | 05-Aug-2024 | Gaetano Biancardi | Applied new Component Template; dependent API removed: TMF688 Event Management; exposed API removed: TMF688 Event Management |
| 1.1.0 | 06-Sep-2024 | Amaia White | Final edits prior to publication |
| 1.2.0 | 18-Nov-2024 | Gaetano Biancardi | API version, only major version to be specified |
| 1.2.0 | 27-Dec-2024 | Rosie Wilson | Final edits prior to publication |
| 1.2.1 | 09-Jul-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03-Jun-2025; final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 13-Apr-2023 | Amaia White | Initial release |
| Pre-production | 15-May-2023 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 15-Aug-2023 | Amaia White | New release v1.0.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 06-Sep-2024 | Amaia White | New release v1.1.0 |
| Production | 01-Nov-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 27-Dec-2024 | Rosie Wilson | New release v1.2.0 |
| Production | 07-Mar-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 09-Jul-2025 | Rosie Wilson | New release v1.2.1 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum Component and Canvas project team.

| Team Member | Company | Role |
|---|---|---|
| Gaetano Biancardi | Accenture | Editor |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Ian Turkington | TM Forum | Additional Input |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |
| Matteo Destino | Accenture | Reviewer |
| Elisabeth Andersson | MATRIXX | Reviewer |

