### 5.2. Jira References

Note: Same needs as at Service level for non-tangible products, plus addition of Resource Inventory APIs, to be
consistent.

**SID**
[ISA-1318] Verify role of Test Measure, Test Measure Definition and Test Specification in ServiceTestABE - TM
Forum JIRA

Note: Jira ISA-1318 is raised for an open point - whether Test Measure, Test Measure Definition and Test
Specification Role should be included in ServiceTestABE under Service, Resource, Product tabs.

[ISA-1251] Improve the description of Product/Service/Resource Test ABEs - TM Forum JIRA

The links between ServiceTest and ResourceTest need to be described, at specification and instance levels. For
example:
- a ServiceTestSpecification related to a Service should correspond to an existing ResourceTestSpecification
- a ServiceTest related to a Service should trigger a ResourceTest on the corresponding Resource.

**APIs**
As:
- a ServiceSpecification related to a Service should correspond to an existing ResourceTestSpecification;
- a ServiceTest related to a Service should trigger a ResourceTest on the corresponding Resource.

[AP-6690] TMF769 - add reference to ServiceTest and ResourceTest - TM Forum JIRA: TMF769 Product Test API is
only available in preview, but contains no links to Service Test or Resource Test, where the real tests are done.

[AP-6691] New API: Resource Test API - TM Forum JIRA: no Resource Test Management API identified yet.

### 5.3. Further resources

1. IG1242: please refer to IG1242 for defined use cases with ODA components interactions.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| Draft version 01 | 02-May-2025 | Ritu Arora | Initial draft created |
| Draft Version 0.2 | 13-May-2025 | Ritu Arora | Based on Review on 06th May: SID ABE table containing pattern ABE (TestMeasure, TestMeasureDefinition, TestSpecificationRole, TestSpecification, Test) has been removed and a Jira raised to request clarification for Test Measure, Test Measure Definition and Test Specification Role to be included in ServiceTestABE under Service, Resource, Product tabs. Under Functional Framework: Service Test Result Analysis Policy Configuration continues to be included; Service Test Resources Availability Management has been removed. Dependent APIs: Incident and Trouble Ticket Management APIs have been removed (ServiceOrderManagement API was suggested to be added as a dependent API but later suggested otherwise, so has not been included). All diagrams updated to incorporate these changes. |
| Draft Version 0.3 | 30-May-2025 | Ritu Arora | Based on Review on 13th May: eTOM entries updated to include Service Specification Test Development & Retirement; Dependent APIs Product Test and Product Inventory have been removed. All diagrams updated to incorporate these changes. |
| Draft Version 0.4 | 23-Jun-2025 | Ritu Arora | Changed Service Catalog API to optional in the dependent API list; respective diagram updated to reflect this change |
| 1.0.0 | 18-Jul-2025 | Rosie Wilson | Final Administrative Updates |
| 1.1.0 | 25-May-2026 | Hugo Vaughan | Gen 5 API updates |
| 1.1.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 18-Jul-2025 | Rosie Wilson | Initial release |
| Production | 18-Aug-2025 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | New Release Version 1.1.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum Component and Canvas project team.

| Team Member | Company | Role |
|---|---|---|
| Ritu Arora | British Telecom | Author |
| Milind Bhagwat | British Telecom | Reviewer |
| Marcio Sousa | Altice Labs | Additional Input |
| Sylvie Demarest | Orange | Reviewer |
| Anastasios Sarantis | City Fibre | Reviewer |

