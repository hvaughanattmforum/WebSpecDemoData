---
name: Agreement Management
---

# TMFC039 – Agreement Management

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Agreement Management | TMFC039 | The Agreement Management component is responsible for creating, storing, editing, and tracking agreed arrangements with related terms and conditions over a lifecycle. The component manages offers, records acceptance, and associated considerations and intentions to establish agreements as legally binding. This component also provides workflows and templates that facilitate collaboration, communication and negotiation of agreements between parties, and administers the translation of agreements into contracts, when required. It provides secure storage, version control, compliance management, and renewal notifications for agreements. | PartyManagement |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.6.5 | L2 | Party Agreement Management | Party Agreement Management manages all aspects of agreements with parties, including customers.  Agreements include: / Purchasing agreements for products, services, and resources that meet the enterprise’s needs / On-boarding agreements for a Party's offerings / Service Level Agreements with one or more other parties / Agreements to use a Party as a sales channel / Reusable template agreements that can be used to create any of the above. |
| 1.7.14 | L2 | Enterprise Governance | Enterprise Governance business process manages activities that ensure accountability and control of the strategic direction of the organization. |
| 1.7.14.5 | L3 | Manage Contract | Manage Contract business activity is in charge of managing agreements, from their creation through to their execution by chosen party, as well as the termination of contracts. / Manage Contract business activity cover tasks that include managing contract creation, execution of contracts, analysis of contracts to maximize operational and financial performance and reducing financial risk. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Agreement | Agreement BE |
| Agreement | AgreementItem BE |
| Agreement | AgreementTermOrCondition BE |
| Agreement | AgreementAuthorization BE |
| Agreement | AgreementApproval BE |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC039_eTOM_SID.png)

*(PlantUML source: [TMFC039_eTOM_SID.puml](TMFC039_eTOM_SID.puml))*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 1026 | Partner Collaboration Constraints Collection | Partner Collaboration Constraints Collection function collect external and internal constraints that can impact a partner collaboration. The partner strategy definition is impacted by various factors, like partner’s geographical location, governmental regulatory, product and services offered etc. The function also provides capability to consider security and financial risks, environmental and legal issues and existing agreements etc. | Purchasing Strategy Management | Purchasing Strategy Definition |
| 1045 | Partner Agreement Tracking | Partner Agreement Tracking function keeps the association of the partner product offerings with the agreements and tracks anomalies for single products or group of products of the partner. | Business Partner Management | Business Partner Agreement Management |
| 1043 | Partner Agreement Storage and Searching | Partner Agreement Storage and Searching function provides the ability to view Partner's existing agreements, search for partner agreements based on meta-data and to search text strings within agreements. The data can also be mined for partner strategy, negotiation, workflow and interaction purposes. | Business Partner Management | Business Partner Agreement Management |
| 1044 | Partner Agreement Implementation | Agreement Implementation function provides support for the implementation of the agreement’s terms and conditions to be used by related organizations during operations. | Business Partner Management | Business Partner Agreement Management |
| 1042 | Partner Agreement Creation | Partner Agreement Creation function provides the functionality to automate the creation of an agreement based on templates or from scratch. The function allows to create and maintain predefined agreement options and templates with terms and conditions (e.g. pricing information, payment clauses, legal texts, etc.) for different purposes and services. | Business Partner Management | Business Partner Agreement Management |
| 1180 | Customer Framework Agreement Approval | Customer Framework Agreement Approval Function manages all approval of Party Roles involved in the Framework Agreement (Customer Roles as well as CSP roles). | Sales Management | Framework Agreement Management |
| 1179 | Customer Framework Agreement Definition | The Customer Framework Agreement Definition Function consists in defining the agreement that describes the commitments and company features valid for associated customer orders. / It defines a subset of catalog offers and products which will be marketed to a customer with particular conditions (configurations of product, rates, discounts, SLA such as availability rate, restoration time guaranties, and associated penalties for the CSP). | Sales Management | Framework Agreement Management |
| 363 | Product Agreement Storage | Product Agreement Storage provides functionality necessary to store and make available the Product Agreements. / This function allows: / • to instantiate or update Product Agreement approved by the customer with their party involved, their configuration, their approvals and their status, / • to update Product Agreements status, / • to search and read Product Agreements. | Product Agreement Management | Product Agreement Storage |
| 361 | Product Agreement Implementation | Product Agreement Implementation function provides functionality pertaining to the implementation of the Product Agreement (a.k.a. contract) across fulfillment, assurance, and billing according to Product Agreement Specification. / A Product Agreement represents the approval by the Customer and the Vendor of all term or conditions of a ProductOffering. | Product Management | Product Agreement Implementation |
| 653 | Contract Management | Contract Management, including establishment, modification, and termination. | Business Partner Management | Business Partner Agreement Management |
| 1042 | Partner Agreement Creation | Partner Agreement Creation function provides the functionality to automate the creation of an agreement based on templates or from scratch. The function allows to create and maintain predefined agreement options and templates with terms and conditions (e.g. pricing information, payment clauses, legal texts, etc.) for different purposes and services. | Business Partner Management | Business Partner Agreement Management |
| 1043 | Partner Agreement Storage and Searching | Partner Agreement Storage and Searching function provides the ability to view Partner's existing agreements, search for partner agreements based on meta-data and to search text strings within agreements. The data can also be mined for partner strategy, negotiation, workflow and interaction purposes. | Business Partner Management | Business Partner Agreement Management |
| 1044 | Partner Agreement Implementation | Agreement Implementation function provides support for the implementation of the agreement’s terms and conditions to be used by related organizations during operations. | Business Partner Management | Business Partner Agreement Management |
| 1045 | Partner Agreement Tracking | Partner Agreement Tracking function keeps the association of the partner product offerings with the agreements and tracks anomalies for single products or group of products of the partner. | Business Partner Management | Business Partner Agreement Management |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC039_API_Context.svg)

*(SVG source: [TMFC039_API_Context.svg](TMFC039_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF651 | Agreement Management API | Mandatory | 4 | agreement | GET, GET /id, POST, PATCH /id, DELETE /id |
| TMF651 | Agreement Management API | Mandatory | 4 | agreementSpecification | GET, GET /id, POST, PATCH /id, DELETE /id |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC039_Exposed_API.png)

*(PlantUML source: [TMFC039_Exposed_API.yaml](TMFC039_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF632 | Party Management API | 5 | Mandatory | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Mandatory | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Mandatory | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Mandatory | organization | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | partyRole | GET, GET /id |
| TMF620 | Product Catalog Management API | 5 | Optional | productOffering | GET, GET /id |
| TMF620 | Product Catalog Management API | 5 | Optional | productOfferingPrice | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Optional | productOffering | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Optional | productOfferingPrice | GET, GET /id |
| TMF637 | Product Inventory Management API | 5 | Optional | product | GET, GET /id |
| TMF637 | Product Inventory Management API | 4 | Optional | product | GET, GET /id |
| TMF667 | Document Management API | 4 | Optional | document | GET, GET /id |
| TMF701 | Process Flow Management API | 4 | Optional | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | 4 | Optional | taskFlow | PATCH, GET, GET /id |

![Dependent API diagram](TMFC039_Dependant_API.png)

*(PlantUML source: [TMFC039_Dependant_API.yaml](TMFC039_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF651 | Agreement Management API | agreementCreateEvent, agreementAttributeValueChangeEvent, agreementStateChangeEvent, agreementSpecificationCreateEvent, agreementSpecificationAttributeValueChangeEvent |

![Published Events diagram](TMFC039_Published_Events.png)

*(PlantUML source: [TMFC039_Published_Events.yaml](TMFC039_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF632 | Party Management API | individualDeleteEvent, organizationDeleteEvent |

![Subscribed Events diagram](TMFC039_Subscribed_Events.png)

*(PlantUML source: [TMFC039_Subscribed_Events.yaml](TMFC039_Subscribed_Events.yaml))*

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

| Standard | Version(s) |
|---|---|
| eTOM | v23.0 |
| SID | v25.0 |
| Functional Framework | v23.0 |
