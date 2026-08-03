### 5.2. Jira References

**eTOM**
- Identify a new Service Availability Check/Assessment activity at Service level, as part of L2 Service
  Configuration & Activation, able to provide all the expected results (feasibility status, service
  delivery due date, need of an appointment at customer site, and cost of the technical solution when
  needed)
- Restore the Determine Resource Availability activity at Resource level. Initial definition: "This
  process investigates the ability to be able to satisfy specific service orders as a part of a
  feasibility check. Where the Allocate & Install Resource processes are requested by a pre-feasibility
  resource order, or by the Design Resources processes, these processes determine whether the requested
  resources are available."

**SID**
- Identify a new Service Qualification BE (if we want to register the result of the Service Availability
  Check/Assessment)

**Functional Framework**
- 592 - Service Parameters Reservation should not be classified in Service Availability sub-domain level
  2, but rather in Service Configuration & Activation / Service Configuration
- 571 - Service Delivery Due Date calculation should be classified in Service Availability sub-domain
  level 2 and not in Service Order Initialization
- Add a function to calculate the cost of a technical solution, for complex cases when it cannot be done
  at catalog design time

**API**
- TMF645 (AP-6200 - TMF645 - Add additional information in the response (DONE)) - Service Qualification
  API: be able to receive as an answer not only the qualification result but also the calculated due
  date, the need of an appointment, and the cost of the solution identified

### 5.3. Further resources

As listed in IG1214 - Mapping of ODA Components and ODA Use Cases, this component is involved in the
following use cases described in IG1228 - How to Use ODA - Using Open APIs to Realize Use Cases: UC002,
UC003, UC007, UC008 and UC010.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 05-Aug-2022 | Goutham Babu | Final edits prior to publication |
| 1.0.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. Separated the YAML files to a managed repository. |
| 1.1.0 | 13-May-2024 | Gaetano Biancardi | Component Template Update; ODF 23.5 update; TMF688 removed from exposed and dependent API |
| 1.1.0 | 12-Jul-2024 | Amaia White | Final updates before publication |
| 1.1.1 | 20-Jan-2026 | Rosie Wilson | Updates to description per agreed YAML updated on 03-Jun-2025; final administrative updates prior to publication |
| 1.2.0 | 29-May-2026 | Hugo Vaughan | Gen 5 API Updates |
| 1.2.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 05-Aug-2022 | Goutham Babu | Initial release of document |
| Pre-production | 05-Sep-2022 | Adrienne Walcott | Updated to reflect TM Forum Member Evaluated status |
| Pre-production | 14-Aug-2023 | Amaia White | New release 1.0.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 12-Jul-2024 | Amaia White | New release 1.1.0 |
| Production | 30-Aug-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 20-Jan-2026 | Rosie Wilson | New release 1.1.1 |
| Production | 05-Sep-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | New release 1.2.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum ODA Components & Canvas team.

| Team Member | Company | Role |
|---|---|---|
| Sylvie Demarest | Orange | Editor |
| Ian Turkington | TM Forum | Additional Input |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Rosie Wilson | TM Forum | Additional Input |
| Gaetano Biancardi | Accenture | Additional Input |
| Elisabeth Andersson | MATRIXX | Reviewer |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |
| Matteo Destino | Accenture | Reviewer |

