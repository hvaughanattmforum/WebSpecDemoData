### 5.2. Jira References

**Functional Framework**
- ISA-996 - Master Data Management has repurposed catalog related functions (BACKLOG): As part of
  reviewing the Product, Service and Resource Catalogs to align with the updates to the Functional
  Framework, a lot of functions have either been removed or re-purposed by Master Data Management,
  resulting in a decision to remove these functions from the Components:
  - Removed deleted unclassified functions (1, 2, 5, 7, 9, 10, 12, 14, 15)
  - Removed functions that used to be related to Catalog management but now have been re-purposed by
    Master Data Management (3, 4, 6, 11, 13)

  Concern: catalog functions may be missing due to re-use of Master Data Management.

**Open APIs**
- Work in progress to create a Product Usage API (as Service Usage and Resource Usage APIs) - when ready,
  it would be added to the exposed APIs for the usage specification part
- [AP-6616] TMF620 - rename ProductOffering into ProductOfferingSpecification
- TAC-1289 TMFC001 - update exposed API for TMF767 Product Usage Management
- New ticket to be opened: need for an Open API able to offer TaxDefinition

### 5.3. Further resources

*(none currently listed)*

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 28-May-2021 | Alan Pope | Final edits prior to publication |
| 1.1.0 | 07-Oct-2022 | Alan Pope | Final edits prior to publication |
| 1.2.0 | 13-Apr-2023 | Amaia White | Final edits prior to publication |
| 1.2.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. Separated the YAML files to a managed repository. |
| 1.2.1 | 14-Aug-2023 | Amaia White | Final edits prior to publication |
| 2.0.0 | 23-Apr-2024 | Sylvie Demarest | Updated to latest template; aligned with 23.5 SID, eTOM and Functional Framework; simplified eTOM mapping due to new definitions and clarifications (Loyalty Program Mgt and Product Capacity Mgt removed); Product Capacity ABE and Product Test Specification BE removed from the SID mapping (managed by other components); new functions added, definitions and Aggregate Functions classifications updated, functions classified in Master Data Mgt removed as too generic; TMF623 SLA Mgt API removed from the dependent APIs chapter (old API in V2 in Historic API table) |
| 2.0.0 | 02-May-2024 | Amaia White | Final edits prior to publication |
| 2.1.0 | 12-Nov-2024 | Gaetano Biancardi | TMF688 removed from the core specification, moved to supporting functions; TMF672 removed from the core specification, moved to supporting functions; API version, only major version to be specified |
| 2.1.0 | 26-Nov-2024 | Amaia White | Final edits prior to publication |
| 2.1.1 | 08-Jul-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03-Jun-2025; 5.2.2 added API ticket as requested by Olivier Arnaud |
| 2.1.1 | 15-Jul-2025 | Rosie Wilson | Final edits prior to publication |
| 2.1.2 | 28-Oct-2025 | Gaetano Biancardi, Julien Rouland | Updates to description per agreed YAML updated on 03-Jun-2025; 5.2.2 added API ticket as requested |
| 2.1.2 | 19-Nov-2025 | Rosie Wilson | Final edits prior to publication |
| 2.2.2 | 28-April-2026 | Hugo Vaughan | Gen 5 API update |
| 2.2.2 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 28-May-2021 | Alan Pope | Initial release of document |
| Pre-production | 05-Jul-2021 | Adrienne Walcott | Updated to reflect Member Evaluated status |
| Pre-production | 07-Oct-2022 | Alan Pope | Version 1.1.0 |
| Pre-production | 13-Apr-2023 | Amaia White | Version 1.2.0 |
| Pre-production | 14-Aug-2023 | Amaia White | Version 1.2.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 02-May-2024 | Amaia White | Version 2.0.0 |
| Production | 28-Jun-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 26-Nov-2024 | Amaia White | Version 2.1.0 |
| Production | 07-Mar-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 15-Jul-2025 | Rosie Wilson | Version 2.1.1 |
| Production | 05-Sep-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 19-Nov-2025 | Rosie Wilson | Version 2.1.2 |
| Pre-production | 28-Apr-2026 | Hugo Vaughan | Gen 5 API updates |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | Version 2.2.2 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum ODA Components & Canvas team.

| Team Member | Company | Role |
|---|---|---|
| Gaetano Biancardi | Accenture | Editor/Reviewer |
| Anastasios Sarantis | Vodafone | Reviewer |
| Sylvie Demarest | Orange | Editor |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Ian Turkington | TM Forum | Additional Input |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Elisabeth Andersson | MATRIXX | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |
| Julien Rouland | Orange | Editor/Reviewer |

