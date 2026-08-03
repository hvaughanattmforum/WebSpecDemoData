---
name: Product Inventory
---

# TMFC005 – Product Inventory

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Product Inventory | TMFC005 | The Product Inventory component is responsible for storage and exposure of products that are assigned to and used by Parties. This component has functionality that enables creation of inventory items, inventory organization, inventory search or filter, inventory monitoring and tracking, inventory control and inventory auditing. The minimum check to be performed upon inventory item creation or update is for global consistency with related Product Catalog information. | Core Commerce |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.2.11 | L2 | Product Inventory Management | Product Inventory Management is responsible to establish, manage and administer the enterprise's product inventory, as embodied in the Product Inventory repository, and monitor and report on the usage and access to the product inventory, and the quality of the information maintained in it. |
| 1.1.19 | L2 | Loyalty Program Management | Define all aspects of a loyalty program, such as requirements and objectives of a loyalty program, determine the benefits to participants. Develop a program, prototype it, test it, rollout/launch it, amend and evaluate it, and terminate it when it is no longer viable for an enterprise. / Manage all operational aspects of running a loyalty program. Enable parties to become a members of a program, earn currency and rewards, and redeem currency. Manage a loyalty program account, leave a program, and provide operational reports. |
| 1.1.19.2 | L3 | Loyalty Program Operation | Manage all operational aspects of running a loyalty program. Enable parties to become a members of a program, earn currency and rewards, and redeem currency. Manage a loyalty program account, leave a program, and provide operational reports. |
| 1.1.19.2.5 | L4 | Manage Loyalty Program Account | Update a loyalty program account and make changes to loyalty program participant information. Expire, reinstate, transfer in/out, adjust, a loyalty participant's account currency. Prepare and send a loyalty program communication to a participant or for internal use by an enterprise. |
| 1.1.19.2.7 | L4 | Provide Loyalty Program Operation Report | Generate a loyalty program operation report, such as various loyalty program status reports, trend analysis, and reports that identify suspected abuse of a loyalty program. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Product and Offering Instance | Product |
| Loyalty | Loyalty Program |
| Product and Offering Instance | |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC005_eTOM_SID.png)

*(PlantUML source: [TMFC005_eTOM_SID.puml](TMFC005_eTOM_SID.puml); \*\* for Loyalty Program)*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 180 | Assigned Products Maintenance | Assigned Products Maintenance permits defining and update: / - product characteristics / - links with the related service or resource (handsets, SIM cards, ...) needed to deliver the product, ... | ProductRepository Management | ProductInventory Repository Management |
| 197 | Customer Product Storage | Customer Product Storage provides the functionality necessary to store and make available the Products. / services presently being used by the customer. / This function allows: / • to instantiate or update offers and products ordered by the customer, whatever their type (network product, bundle, device, …) or their marketing mode (rented, sold, …), with their configuration, their tariffs and discounts, and their status (initialized with a creation order) / • to update Products status / • to search and read Offer and Product installed base (subscribed offers, configuration of installed products, installed tariffs and discount, statuses, …). | ProductRepository Management | ProductInventory Repository Management |
| 198 | Customer Loyalty Score Balance Management | Customer Loyalty Score Balance Management function calculates the score according to accumulation/decrease rules. When a customer subscribes to the loyalty program with more than one SIM or other ‘traffic objects’, the Score Management accumulates the points into a single balance. The loyalty score could decrease for one of the following events: prize purchase, points expiry or points deletion by Call Centre. The functionality may also include the visualization of Score details (date, description event type, points, final score) via different contact Channels (e.g. via Web, IVR, Call Centre). | ProductRepository Management | Loyalty Account Management |
| 237 | Customer Loyalty Communication | Customer Loyalty Communication function sends information related to Loyalty Programs (Point Balance, Prize Request status, renewed Loyalty Code) to external components in push and pull modes. | ProductRepository Management | Loyalty Account Management |
| 361 | Contract Implementation | Contract Implementation function provide functionality pertaining to the implementation of the contract across fulfillment, assurance, and billing. / Product Agreement Implementation function provides functionality pertaining to the implementation of the Product Agreement (a.k.a. contract) across fulfillment, assurance, and billing according to Product Agreement Specification. / A Product Agreement represents the approval by the Customer and the Vendor of all term or conditions of a ProductOffering. | ProductRepository Management | ProductInventory Agreement Management |
| 362 | Contract Searching | Contract Searching function provides the ability to search for customer contracts based on meta-data and to search text strings within contracts and view customer's existing and previous contracts, | Product Repository Management | Product Inventory Management |
| 363 | Contract Storage | Contract Storage provides the central repository for contract storage as well as the associated contract meta-data. This data can be mined for Campaigns and Lead Generation. / Product Agreement Storage provides functionality necessary to store and make available the Product Agreements. / This function allows: / • to instantiate or update Product Agreement approved by the customer with their party involved, their configuration, their approvals and their status, / • to update Product Agreements status, / • to search and read Product Agreements. | ProductRepository Management | ProductInventory Agreement Management |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC005_API_Context.svg)

*(SVG source: [TMFC005_API_Context.svg](TMFC005_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF637 | Product Inventory Management API | Mandatory | 5 | product | GET, GET /id, POST, PATCH, DELETE |
| TMF637 | Product Inventory Management API | Mandatory | 4 | product | GET, GET /id, POST, PATCH, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC005_Exposed_API.png)

*(PlantUML source: [TMFC005_Exposed_API.yaml](TMFC005_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF620 | Product Catalog Management API | 5 | Mandatory | productOffering, productOfferingPrice, productSpecification | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Mandatory | productSpecification, productOffering, productOfferingPrice | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRoleManagement | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | PartyRoleManagement | GET, GET /id |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET, GET /id |
| TMF651 | Agreement Management API | 4 | Optional | agreement | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress, geographicSubAddress | GET, GET /id |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF675 | Geographic Location Management API | 4 | Optional | geographicLocation | GET, GET /id |
| TMF666 | Account Management API | 5 | Optional | billingAccount | GET, GET /id |
| TMF666 | Account Management API | 4 | Optional | billingAccount | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | individual, organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual, organization | GET, GET /id |
| TMF637 | Product Inventory Management API | 5 | Optional | product | GET, GET /id, POST, PATCH, DELETE |
| TMF637 | Product Inventory Management API | 4 | Optional | product | GET, GET /id, POST, PATCH, DELETE |
| TMF638 | Service Inventory Management API | 5 | Optional | service | GET, GET /id |
| TMF638 | Service Inventory Management API | 4 | Optional | service | GET, GET /id |
| TMF622 | Product Ordering Management API | 5 | Optional | productOrder | GET, GET /id |
| TMF622 | Product Ordering Management API | 4 | Optional | productOrder | GET, GET /id |

![Dependent API diagram](TMFC005_Dependant_API.png)

*(PlantUML source: [TMFC005_Dependant_API.yaml](TMFC005_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF637 | Product Inventory Management API | productCreateEvent, productAttributeValueChangeEvent, productStateChangeEvent, productDeleteEvent, productBatchEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |

![Published Events diagram](TMFC005_Published_Events.png)

*(PlantUML source: [TMFC005_Published_Events.yaml](TMFC005_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF639 | Resource Inventory Management API | resourceDeleteEvent |
| TMF638 | Service Inventory Management API | serviceDeleteEvent |
| TMF620 | Product Catalog Management API | productSpecificationDeleteEvent, productOfferingDeleteEvent, productOfferingPriceDeleteEvent |
| TMF669 | Party Role Management API | partyRoleDeleteEvent |
| TMF651 | Agreement Management API | agreementDeleteEvent |
| TMF666 | Account Management API | billingAccountDeleteEvent |
| TMF672 | User Role Permission Management API | permissionDeleteEvent |
| TMF674 | Geographic Site Management API | geographicSiteDeleteEvent |
| TMF675 | Geographic Location Management API | geographicLocationDeleteEvent |
| TMF632 | Party Management API | individualDeleteEvent, organizationDeleteEvent |
| TMF622 | Product Ordering Management API | productOrderDeleteEvent |
| TMF637 | Product Inventory Management API | productCreateEvent, productDeleteEvent, productAttributeValueChangeEvent, productStateChangeEvent |

![Subscribed Events diagram](TMFC005_Subscribed_Events.png)

*(PlantUML source: [TMFC005_Subscribed_Events.yaml](TMFC005_Subscribed_Events.yaml))*

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

| Standard | Version(s) |
|---|---|
| eTOM | v24.0 |
| SID | v25.0 |
| Functional Framework | v24.0 |
