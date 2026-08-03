### 5.2. Jira References

**eTOM**
[ISA-756] Review eTOM business activities related to agreement and or contract management - TM Forum JIRA

In eTOM 22.5 we have:
- In Business Partner Domain: L2 – Party Agreement Management (1.6.5).
- Its definition includes "all aspects of agreements with parties, including customers" which seems to be an
  anomaly: we should have distinct business activities related to customer and partners
- Its definition also includes "Purchasing agreements for products, services and resources that meet the
  enterprise's needs": whatever the enterprise will need for its internal activities, it will always order
  products and product offerings to its suppliers or partners (nether services nor resources).
- And "Applicable sub-processes are also used by other processes, such as Product Offering Agreement
  Management and Party Privacy Agreement Management.": Product Offering Agreement Management
- In Customer Domain: nothing related to agreement and/or contract management (except for Privacy)
- In Product Domain: L4 – Product Offering Agreement Management (1.2.7.2.4) in L3 – Product Offering
  Development & Retirement (1.2.7.2) in L2 – Product Specification & Offering Development & Retirement (1.2.7),
  with the following definition: "Develop a template agreement that defines the terms/conditions associated
  with a product offering."
- In Market Sales Domain: L3 – Negotiate Sales/Contract (1.1.9.5) in L2 - Selling (1.1.9). Refer to ISA-711
  ticket already created.
- In Enterprise domain: L3 Manage Contract (1.7.14.5) in L2 Enterprise Governance (1.7.14) which definition is
  very generic: "Manage Contract business activity is in charge of managing agreements, from their creation
  through to their execution by chosen party, as well as the termination of contracts."

We need to have a clear set of business activities, defined at consistent levels and able to manage the
different types of agreement and/or contract specification, and their instantiations in their related business
context.

**SID**
[ISA-757] Review SID Agreement ABE - TM Forum JIRA

Describe all the types of agreements and contracts needed by a CSP, such as framework agreements, employees'
contracts, suppliers' contracts, customer contracts with their specific links to other BEs such as catalogs.
Clarify the difference between agreement and contract terms.
Remove the positioning of the Agreement BE as specialization of Business Interaction and replaced it by clear
and explicit relationships to Party and Party Roles.
Review the Service Level Agreement part of the ABE: SLA and SLA conditions can be better described as product
specification and configuration, with their scope of application on other products, and their rating rules
through the product offering subscribed.
Review the definition of BEs such as AgreementTermOrCondition or AgreementItem (not meaningful to link to
Service or Resource levels).

### 5.3. Further resources

*(none currently listed)*

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 13-Jun-2023 | Matteo Destino | Initial draft for Rights and Permissions component, with eTOM, SID and Open API mapping |
| 1.0.0 | | Amaia White | Final edits prior to publication |
| 1.0.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. Separated the YAML files to a managed repository. |
| 1.0.1 | 14-Aug-2023 | Amaia White | Final edits prior to publication |
| 1.1.0 | 27-Aug-2024 | Gaetano Biancardi | New Component template applied. Exposed API: removed: TMF688 Event Management. Dependant API: removed: TMF688 Event Management. Functional Framework Function, following functions added: Customer Framework Agreement Approval 1180, Customer Framework Agreement Definition 1179, Product Agreement Storage 363, Product Agreement Implementation 361, Contract Management 653, Partner Agreement Creation 1042, Partner Agreement Storage and Searching 1043, Partner Agreement Implementation 1044, Partner Agreement Tracking 1045 |
| 1.1.1 | 09-Sep-2025 | Rosie Wilson | Updates to description per agreed YAML updated on 03 Jun 2025. Final administrative updates prior to publication |
| 1.2.0 | 05-Jun-2026 | Hugo Vaughan | Gen 5 API updates |
| 1.2.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 13-Jun-2023 | Amaia White | Initial release of document |
| Pre-production | 17-Jul-2023 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 14-Aug-2023 | Amaia White | New release of document |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 06-Sep-2024 | Amaia White | New release of document |
| Production | | | |
| Pre-production | 09-Sep-2025 | Rosie Wilson | v1.1.1 |
| Production | 14-Nov-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | v1.2.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum Component and Canvas project team.

| Team Member | Company | Role |
|---|---|---|
| Matteo Destino | Accenture | Editor |
| Cecile Ludwichowski | Orange | Additional Input |
| Emmanuel A. Otchere | Huawei | Additional Input |
| Gaetano Biancardi | Accenture | Reviewer |
| Sylvie Demarest | Orange | Reviewer |
| Anastasios Sarantis | Vodafone | Reviewer |
| Hugo Vaughan (TM Forum) | TM Forum | Reviewer |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Elisabeth Andersson | MATRIXX | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |
| Jose Macaluso | Xacria | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Ritu Arora | BT | Reviewer |

