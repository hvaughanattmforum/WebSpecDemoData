### 5.2. Jira References

**Open API**
- AP-4088 - Assess the addition of a ResourceUsage API with both ResourceUsage & ResourceUsageSpecification
  (DONE). The UsageSpecification is described in the Catalog Management components — at product, service,
  and resource levels. As part of the Resource Catalog Component specification, the question has arisen
  around the need to assess the addition of a ResourceUsage API with both ResourceUsage &
  ResourceUsageSpecification (feedback from Ludovic Robert and Kamal Maghsoudlou). This will be similar to
  the resource level like TMF727 (ServiceUsage) is for the service level. This is consistent with the SID
  ABE (resourceUsage & resourceUsageSpec).

**Functional Framework**
- ISA-996 - Master Data Management has repurposed catalog related functions (BACKLOG). As part of
  reviewing the Product, Service and Resource Catalogs to align with the updates to the Functional
  Framework, we realized that a lot of functions have either been removed or been re-purposed by Master
  Data Management. Due to this, we had to make a decision to remove all these functions from the
  Components: removed deleted unclassified functions (1, 2, 5, 7, 9, 10, 12, 14, 15); removed functions
  that used to be related to Catalog management but now have been re-purposed by Master Data Management
  (3, 4, 6, 11, 13). Our concern is that we may be missing functions for the catalog due to re-use of
  Master Data Management.

### 5.3. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 05-Aug-2022 | Kamal Maghsoudlou, Gaetano Biancardi, Sylvie Demarest | Final edits prior to publication |
| 1.1.0 | 06-Oct-2022 | Elisabeth Andersson | Added support for federated catalogs and minor fixes. |
| 1.1.1 | 27-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. Separated the YAML files to a managed repository. |
| 1.1.1 | 14-Aug-2023 | Amaia White | Final edits prior to publication |
| 1.2.0 | 19-Apr-2024 | Elisabeth Andersson | Update to latest template; aligned with 23.5 SID and eTOM (removed Resource Test specification BE and process, now managed by Resource Test Mgt); updated with Functional Frameworks 23.5 — added new functions under lvl2 Resource Specification Development (1064, 1082, 1083, 1087, 1088, 1089), updated the description of function 996, removed deleted unclassified functions (1, 2, 5, 7, 9, 10, 12, 14, 15), removed functions re-purposed by Master Data Management (3, 4, 6, 11, 13) |
| 1.2.0 | 30-Apr-2024 | Amaia White | Final edits prior to publication |
| 1.3.0 | 26-Nov-2024 | Elisabeth Andersson | TMF688 removed from the core specification, moved to supporting functions; TMF672 removed from the core specification, moved to supporting functions; removed the minor versions of all APIs as per template |
| 1.3.0 | 24-Dec-2024 | Rosie Wilson | Final edits prior to publication |
| 1.3.1 | 08-Jul-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03 Jun 2025 |
| 1.3.1 | 15-Jul-2025 | Rosie Wilson | Final edits prior to publication |
| 1.3.2 | 13-Oct-2025 | Gaetano Biancardi | Corrected naming format (without spaces) from "Resource Performance Specification BE" to "ResourcePerformanceSpecification BE" |
| 1.3.2 | 19-Nov-2025 | Rosie Wilson | Final edits prior to publication |
| 1.4.0 | 05-Jun-2026 | Hugo Vaughan (TM Forum) | Gen 5 API inclusion |
| 1.4.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 05-Aug-2022 | Goutham Babu | Initial release |
| Pre-production | 07-Oct-2022 | Alan Pope | Version 1.1.0 |
| Pre-production | 14-Aug-2023 | Amaia White | Version 1.1.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 30-Apr-2024 | Amaia White | Version 1.2.0 |
| Production | 28-Jun-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 24-Dec-2024 | Rosie Wilson | Version 1.3.0 |
| Production | 07-Mar-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 15-Jul-2025 | Rosie Wilson | Version 1.3.1 |
| Production | 05-Sep-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 19-Nov-2025 | Rosie Wilson | Version 1.3.2 |
| Production | 16-Jan-2026 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | Version 1.4.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum Component and Canvas project team:

| Team Member | Company | Role |
|---|---|---|
| Elisabeth Andersson | MATRIXX | Editor |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Ian Turkington | TM Forum | Additional Input |
| Gaetano Biancardi | Accenture | Additional Input / Reviewer |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |
| Matteo Destino | Accenture | Reviewer |
| julien rouland | Orange | Additional Input / Reviewer |

