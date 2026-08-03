### 5.2. Jira References

**eTOM**
- Review L2 1.2.9 - Product Offering Purchasing and clarify L3 definitions and inbound / outbound
  terminology; delete L3 1.2.9.8 - Report Product Offering Purchase as redundant with 1.3.3.6 - Report
  Customer Order Handling and 1.6.8.6 - Report Business Partner Orders
- Review L3 1.3.3.4 - Complete Customer Order definition as it mixed customer information, customer
  contracts and service orders. Also review L3 1.3.3.7 - Close Customer Order definition and clarify
  close/complete terminology and link with 1.3.3.4 - Complete Customer Order (do we need 2 L3?)
- 1.3.3.8 - Manage Order Fallout: as this L3 is shared by POCV and POOM components (to be consistent with
  Functional Framework mapping), clarify which type of fallout needs to be managed during the order
  delivery orchestration (at POOM level) and which needs to be managed at Product Order Capture and
  Follow-Up level (by POCV)

**SID**
*(none currently listed)*

**Functional Framework**
These updates need to be studied for R22.0 or R22.5:
- Function 204 - Customer Order Completion: rename the function "Customer Order Entry Finalization" as
  "completion" is confusing here
- Function 269 - Installation Preference Configuration: review the definition of this function or delete
  it (why limited to installation? Why a dedicated function to provide an interface for the customer to
  capture a set of information?)
- Add function(s) to describe the closure step of the customer order
- Function 934 - Sales Negotiation Support: review definition and delete part related to service order
  generation

**API**
- How can we trigger the Product Configurator for configuration? Refer to Jira detailed in Product
  Configurator specifications
- How can we evaluate Customer Credit (refer to Function 205 for definition): can this check be added in
  TMF696 - Risk Management API?
  - AP-6002 - TMF696 - create real Task resource(s) (BACKLOG)
- How can we manage/represent mass operations in general, and mass transaction ordering in particular?
- [AP-6617] TMF622 - specialize ProductOrderItem for ProductSpecification and ProductOffering - TM Forum
  Jira

### 5.3. Further resources

This component is involved in use cases described in IG1228 How to use ODA - Using Open APIs to realize
Use Cases.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 29-Mar-2022 | Gaetano Biancardi, Anastasios Sarantis, Sylvie Demarest, Emmanuel A. Otchere | First version of document |
| 1.0.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. Separated the YAML files to a managed repository. |
| 2.0.1 | 19-Aug-2024 | Sylvie Demarest | Updated Component Template; Jira reference AP-6617 added to section 5.2.4 as requested by Olivier Arnaud; final edits prior to publication |
| 2.0.1 | 06-Sep-2024 | Amaia White | Final edits prior to publication |
| 2.1.0 | 12-Nov-2024 | Gaetano Biancardi | API version, only major version to be specified |
| 2.1.0 | 26-Nov-2024 | Amaia White | Final edits prior to publication |
| 2.1.1 | 08-Jul-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03-Jun-2025; Jira reference AP-6617 added to section 5.2.4 as requested by Olivier Arnaud; final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 29-Mar-2022 | Goutham Babu | Initial release |
| Production | 20-May-2022 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 14-Aug-2023 | Amaia White | New release 1.0.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 06-Sep-2024 | Amaia White | New release 2.0.1 |
| Production | 01-Nov-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 26-Nov-2024 | Amaia White | New release 2.1.0 |
| Production | 07-Mar-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 08-Jul-2025 | Rosie Wilson | New release 2.1.1 |

### 6.2. Acknowledgements

| Team Member | Company | Role |
|---|---|---|
| Gaetano Biancardi | Accenture | Reviewer |
| Anastasios Sarantis | Vodafone | Reviewer |
| Sylvie Demarest | Orange | Editor |
| Elisabeth Andersson | MATRIXX | Reviewer |
| Emmanuel A. Otchere | Huawei | Additional Input |
| Ian Turkington | TM Forum | Additional Input |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |
| Matteo Destino | Accenture | Reviewer |
| Rosie Wilson | TM Forum | Additional Input |

