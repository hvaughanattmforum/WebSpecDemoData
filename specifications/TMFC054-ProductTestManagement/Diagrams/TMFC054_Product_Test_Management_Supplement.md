### 5.2. Jira References

Note: Same needs as at Service level for non-tangible products, plus addition of Resource Inventory APIs, to be
consistent.

Note on the Dependent APIs table: no link to this information is currently described in the resource model of the
draft TMF769 API (refer to Jira ticket below). When available, the Resource Test API should be added as a
dependent API, as with the Resource Inventory Management API (refer to Jira ticket below).

**SID**
[ISA-1251] Improve the description of Product/Service/Resource Test ABEs - TM Forum JIRA

The links between ProductTest, ServiceTest and ResourceTest need to be described, at specification and instance
levels. For example:
- a ProductTestSpecification related to an intangible ProductSpecification should correspond to an existing
  ServiceTestSpecification; a ProductTest related to an intangible Product triggers a ServiceTest on the
  corresponding Service.
- a ProductTestSpecification related to a tangible ProductSpecification should correspond to an existing
  ResourceTestSpecification; a ProductTest related to a tangible Product should trigger a ResourceTest on the
  corresponding Resource.

**APIs**
[AP-6690] TMF769 - add reference to ServiceTest and ResourceTest - TM Forum JIRA: TMF769 Product Test API is
only available in preview, but contains no links to Service Test or Resource Test, where the real tests are done.

[AP-6691] New API: Resource Test API - TM Forum JIRA: no Resource Test Management API identified yet.

### 5.3. Further resources

*(none currently listed)*

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 04-Mar-2025 | Sylvie Demarest | Initial version |
| 1.0.0 | 04-Mar-2025 | Rosie Wilson | Final administrative updates prior to publication |
| 1.0.1 | 09-Sep-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03 Jun 2025 |
| 1.1.0 | 25-May-2026 | Hugo Vaughan | Final administrative updates prior to publication |
| 1.1.0 | 25-Jun-2026 | Sannah Sibaya | Gen 5 API updates; Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 04-Mar-2025 | Rosie Wilson | Preparation for initial release |
| Pre-production | 21-Apr-2025 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 09-Sep-2025 | Rosie Wilson | Version 1.0.1 |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | Version 1.1.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum Component and Canvas project team.

| Team Member | Company | Role |
|---|---|---|
| Sylvie Demarest | Orange | Author |
| Gaetano Biancardi | Accenture | Reviewer |
| Anastasios Sarantis | Vodafone | Reviewer |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Ian Turkington | TM Forum | Additional Input |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Elisabeth Andersson | MATRIXX | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |

