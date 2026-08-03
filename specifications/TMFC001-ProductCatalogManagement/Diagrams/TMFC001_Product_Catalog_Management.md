---
name: Product Catalog Management
---

# TMFC001 – Product Catalog Management

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Product Catalog Management | TMFC001 | The product catalog management component is responsible for organizing the collection of products and product offering specifications that identify and define all requirements of a product or a product offering that can be commercialized. | CoreCommerce |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.2.20 | L2 | Product Catalog Lifecycle Management | Catalog Lifecycle Management business process covers a set of business activities that enable manage the lifecycle of an organization’s catalog from design to build according to defined requirements. |
| 1.1.19 | L2 | Loyalty Program Management | *(no description available)* |
| 1.1.19.1 | L3 | Loyalty Program Development & Retirement | *(no description available)* |
| 1.2.7 | L2 | Product Specification & Offering Development & Retirement | Product Specification & Offering Development & Retirement processes develop and deliver new product specifications as well as enhancements and new features, ready for use by other processes. Additionally, they handle the removal of specifications no longer offered. / Product specifications represent the types of services and resources made available as product offerings to the market by an enterprise. / The key measures of this process are how effectively the enterprise’s offerings are broadened by these specifications or new specification features. These processes also manage updates and enhancements to product specifications. Business case development tracking and commitment are key elements of this process. / They also develop new product offerings and their associated features. Pricing for the offerings is also developed, such as standard pricing and feature-based pricing. The offerings and selected processes are included in product catalogs which are also developed by these processes. |
| 1.2.8.7 | L3 | Implement Product Capacity Plan | *(no description available)* |
| 1.6.4 | L2 | Business Partner Offering Development & Retirement | Business Partner Offering Development & Retirement supports the management of on-boarding and off-boarding another Business Partner's product specifications and product offerings that a required to facilitate the business model of the enterprise. / It also manages the involvement the enterprise has with a product specification and product offering. For example, the enterprise may accept an order for one of its offerings, but it may be fulfilled by another Business Partner. / Note: / - Product Specification Development & Retirement and Product Offering Development & Retirement processes are used to manage most of the lifecycle of product specifications and product offerings. This is done to eliminate redundant processes.  For example, the Product Offering Pricing processes are used to manage the prices associated with on-boarded product offerings. / - This process therefore focuses on managing the relationship that parties, including the enterprise, have with product specifications and product offerings as well as the impact of off-boarding specifications and offerings on a provider's service and resource infrastructure. |
| 1.2.8 | L2 | Product Capacity Management | *(no description available)* |
| 1.2.22 | L2 | Product Catalog Content Management | Product Catalog Content Management business process defines and provides the business activities that support the day-to-day operations of Product Catalogs in order to realize the business operations goals. / Product Catalog Content Management business processes include administering the Product Catalog instance in production, maintaining catalog entries, assuring catalogs, managing catalog access, managing entry lifecycle through versioning, handling catalog entity entry and changes, supporting distribution of catalogs as needed, and supporting user-facing activities. |
| 1.2.21 | L2 | Product Catalog Operational Readiness Management | Product Catalog Operational Readiness Management business process establishes and administers the support needed to operationalize Product catalogs for ongoing day-to-day business needs. / These business activities implement the Product Catalog through Release and Deploy business activities. / Release Product Catalog business activity ensure all cross-functional activities needed to support catalog maintenance and operations, such as training and updating the support of the catalog are in place. / Release Product Catalog business activity includes identifying stakeholders, catalog integration, catalog federation etc. for any scenario in support of the organizations business goals, including Release conditions that support users, customers and business partners. |
| 1.2.19 | L2 | Product Catalog Planning Management | Product Catalog Planning Management business process covers a set of business activities that understand and enable establish the plan to define, design and operationalize a catalog in order to meet the needs and objectives of Product cataloging. / The Product Catalog Planning Management business process ensures that the organization is able to identify the most appropriate scheme and goal for its catalog. It includes designing the Catalog plan and developing the specification according to Product management requirement. |
| 1.2.23 | L2 | Product Specification Management | Product Specification Management business process leverages captured product requirements to develop, master, analyze, and update documented standard and personalized conditions that must be satisfied by product design and/or delivery. / Product Specifications Management can result in establishing, in a centralized way, technical (know-how) standards for products. Such standards provide the organization with a means to control and approve the values and inputs of product specification through structure, review, approval and distribution processes to users (including customers and business partners). |
| 1.2.8.7.1 | L4 | Specify Required Product Capacity | *(no description available)* |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Product Offering Specification |  |
| Product Specification |  |
| Product Configuration | ProductConfigSpec BE |
| Party Product Specification and Offering |  |
| Loyalty | Loyalty Program Specification |
| Product Usage | Product Usage Specification |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC001_eTOM_SID.svg)

*(SVG source: [TMFC001_eTOM_SID.svg](TMFC001_eTOM_SID.svg) — hand-drawn rather than
PlantUML: this diagram has 2 eTOM activities + 6 SID entities = 8 elements, past the 6-element threshold
where plain PlantUML layout gets visually messy. Generated by the `component-specification-markdown`
skill's `scripts/render_etom_sid_svg.py`.)*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 3 | Repository Entity Relations Configuration | *(no description available)* | *(no description available)* | *(no description available)* |
| 4 | Repository Entity Grouping Configuration | *(no description available)* | *(no description available)* | *(no description available)* |
| 6 | Repository Entity Data Model Configuration | *(no description available)* | *(no description available)* | *(no description available)* |
| 11 | Repository Entity Hierarchy Management | *(no description available)* | *(no description available)* | *(no description available)* |
| 123 | Product Catalog Browsing | Product Catalog Browsing provides a browsing function to identify products available for purchase by a given customer, provide selected relevant information (e.g. cost, requirements, configurable attributes) to the customer. This information will be used in the step guidance. | Product Specification & Offering Management | Product Specification & Offering Development |
| 210 | Centralized Ordering Rules Management | Centralized Ordering Rules Management provides centralized business rules for ordering (eligibility, compatibility). | Product Specification & Offering Management | Ordering Rules Development |
| 238 | Customer Loyalty Rules Management | Customer Loyalty Rules Management provides Loyalty Program Rules and customer loyalty profiles management | Product Specification & Offering Management | Product Specification & Offering Development |
| 263 | Product Compatibility Checking | Product Compatibility Checking function provides an internet technology driven interface for the customer to check product compatibility. | Product Specification & Offering Management | Product Specification & Offering Development |
| 360 | Product Agreement Specification Design | Product Agreement Specification Design Function creates and maintains predefined Product Agreement options and templates for Product Offerings. It includes general terms or conditions and approval rules. | Product Specification & Offering Management | Product Specification & Offering Development |
| 407 | Product Modeling Support | Product Modeling Support supports Lifecycle Management in the design and build phase of the Product Offerings and Product Specifications. | Product Specification & Offering Management | Product Modeling Support |
| 408 | Product Retirement | Product Retirement Function retires obsolete product offering as part of Lifecycle Management (LM). | Product Specification & Offering Management | Product Specification Lifecycle Management |
| 415 | Product Strategy linking | Product Strategy Linking links strategy to propositions and links propositions to products | Product Specification & Offering Strategy Definition & Analysis | Product Specification & Offering Strategy Management |
| 649 | Product Sourcing Registration | Product Sourcing Registration provides initiation of product instantiation into the service provider product catalog and/or storefront, including product prices. | Business Partner Product Specification and Offering Management | Business Partner Product Specification and Offering Onboarding |
| 650 | Partner Product Certification | Partner Product Certification provides product certification/decertification to be an integrated part of the service provider's value proposition. | Business Partner Product Specification and Offering Management | Business Partner Product Specification and Offering Onboarding |
| 662 | Sourcing Reference Data Collection | Sourcing Reference Data Collection collects definition of products and services, pricing schemes, partner entities and contracts into the system. Easy uploading of reference data from external sources such as XML files. | Business Partner Product Specification and Offering Management | Business Partner Product Specification and Offering Onboarding |
| 721 | Customer Order Rules Configuration | Customer Order Rules Configuration function provides in addition to the Product rules, rules like cross/up sell rules, compatibility rules, eligibility rules, address/service availability rules, etc. Some specific types of rules must be available for all decision-based actions on customer orders. These rules could be customer fraud check, decomposition rules, priority rules, order duplication prevention rules, complex rules involving multi-system checks, etc. | Product Specification & Offering Management | Ordering Rules Development |
| 722 | Order Rules Retrieval | Order Rules Retrieval function makes the Order Rules available to e.g. customer order related applications. | Product Specification & Offering Management | Ordering Rules Development |
| 992 | Entity Management Notification | *(no description available)* | *(no description available)* | *(no description available)* |
| 993 | Entity Management Reporting | *(no description available)* | *(no description available)* | *(no description available)* |
| 1050 | Product Onboarding Management | Product Onboarding Management function supports the managing of the onboarding of a Product Offering sourced from an external source e.g. a business partner. | Business Partner Product Specification and Offering Management | Business Partner Product Specification and Offering Onboarding |
| 1053 | Onboarded Product Workflows Definition | Onboarded Product Workflows Definition function identifies appropriate workflows related to the use of the onboarded product in fulfillment, assurance and billing. | Business Partner Product Specification and Offering Management | Business Partner Product Specification and Offering Onboarding |
| 1076 | Product Specification Design | Product Specification Design Function provides the means to describe for every product commercialized through one or several offers: / • characteristics of the product, and their possible values (ex: speed, volume, duration, phone number, …) / • available operations (ex: create, change of speed) / • functional incompatibilities or prerequisites (deducted from CFS specification incompatibilities or pre-requisites) / • link with the know-how type (CFS specification) from which the intangible product is a restriction (ex: mobile line, VOIP, …), or directly with the resource type for tangible products (ex: smartphone, SIM Card), or to the Supplier product type in case of purchase products. / It includes facilities to design a new Product Specification based on an existing one and integrity rules controls. / The Product Catalogue describes, according to strategy, all the tangible and intangible products that can be commercialized through standard offers, loyalty offers. / Example: / • goodies can be sold or offered as a reward in exchange for fidelity points (same product commercialized through 2 offers) / • a special discount can be granted through a retention offer / • … / A Product Specification restricts a Customer Facing Service Specification (CFSSpec). | Product Specification & Offering Management | Product Specification & Offering Development |
| 1077 | Product Offering Design | Product Offering Design function provides the means to describe Product Offering, according to marketing strategy: / • commercial name / • packaging rules of the contract: mandatory offers, optional offers, offers that can be ordered in number (ex: 1 to 4 mobile lines) / • commercial incompatibilities or prerequisites (ex: necessary to be the holder of a X contract to subscribe Y contract) / • available commercial operations (ex: contract migration) / • available commitment durations / • any commercial criteria such as authorized sales channel or geographic area, customer criteria, … / • tariff specifications – and possible alterations. They are associated with the offer, to commercial operations or usage types and can be recurring or one shot. They are expressed as rules that can consider many criteria (ex: commitment duration, product configuration, sales channel, customer’s age, …) and will be evaluated during the order capture process, or during the rating process for usage. / It includes facilities to design a new Product Offering based on an existing one and integrity rules controls. | Product Specification & Offering Management | Product Specification & Offering Development |
| 1078 | Product Specification and Offering Change Auditing | Product Specification and Offering Change Auditing manages the implications of Product Specifications and Offerings changes to determine the consequences of any given change. Product Specifications and Offerings changes may impact other Product Specifications and / or Offerings according to relationships between them. / The function logs Product Specifications changes and supports the analysis of relationships between Product Specifications. / In addition, it tracks the history of changes in an easy and accessible manner. | Product Specification & Offering Management | Product Specification & Offering Development |
| 1079 | Product Specification and Offering Repository Management | Product Specification and Offering Repository Management is able to create, modify and delete Product Specification and Offering. / This includes the ability to manage the state of an entity during its lifecycle (e.g. planned, deployed, in operation, replaced by, locked…). / It includes Product Specifications and Offerings retrieval, integrity rules check and versioning management. / It also provides Product Specification and Offering views adapted to the different roles. | Product Specification & Offering Management | Product Specification & Offering Development |
| 416 | Product Propositions Operations Planning | Product Propositions Operations Planning supports the planning of the introduction of propositions for new or updated product offerings and/or product specifications, by planning which operating groups are delivering what of the product proposition and where are the organization and operations touchpoints. | Product Specification & Offering Strategy Definition & Analysis | Product Specification & Offering Strategy Management |
| 417 | Product Strategy to Proposition Alignment | Product Strategy to Proposition Alignment captures and manages details of the business strategy and applies them to the propositions for new or updated product offerings and/or product specifications. | Product Specification & Offering Strategy Definition & Analysis | Product Specification & Offering Strategy Management |
| 418 | Product Strategy/Propositions Creation | Product Strategy/Propositions Creation delivers a product strategy and/or propositions for new or updated product offerings and/or product specifications. | Product Specification & Offering Strategy Definition & Analysis | Product Specification & Offering Strategy Management |
| 419 | Product Strategy performance reporting | *(no description available)* | *(no description available)* | *(no description available)* |
| 897 | Building Access Control | Building Access Control checks, stops or allows physical access to facilities according to access roles and rules. | Identification and Permission Management | Permission Control |
| 900 | Authorization Control Management | Authorization Control Function controls permissions according to roles and related rules. / It consists in evaluating if a requester is granted permission to act by providing the required evidence. The evidence corresponds to the condition specified for each right (for instance keying the correct password to use a specific mailbox). If the action is protected via a right which is assigned (possibly via a role) to a person, then the person has to be identified to retrieve their rights and verify if the request to act can be granted. | Identification and Permission Management | Permission Control |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC001_API_Context.svg)

*(SVG source: [TMFC001_API_Context.svg](TMFC001_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF620 | Product Catalog Management API | Mandatory | 5 | productCatalog | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | category | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | exportJob | GET, GET /id, POST, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | importJob | GET, GET /id, POST, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | productOffering | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | productOfferingPrice | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 5 | productSpecification | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | catalog | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | category | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | productSpecification | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | productOffering | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | productOfferingPrice | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | exportJob | POST, GET, GET /id, DELETE |
| TMF620 | Product Catalog Management API | Mandatory | 4 | importJob | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |
| TMF671 | Promotion Management API | Optional | 4 | promotion | GET, GET /id, POST, PATCH, DELETE |

![Exposed API diagram](TMFC001_Exposed_API.png)

*(PlantUML source: [TMFC001_Exposed_API.yaml](TMFC001_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF633 | Service Catalog Management API | 4 | Optional | serviceSpecification | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | partyRole | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | organization | GET, GET /id |
| TMF634 | Resource Catalog Management API | 5 | Optional | resourceSpecification | GET, GET /id |
| TMF634 | Resource Catalog Management API | 4 | Optional | resourceSpecification | GET, GET /id |
| TMF651 | Agreement Management API | 4 | Optional | agreement | GET, GET /id |
| TMF651 | Agreement Management API | 4 | Optional | agreementSpecification | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress | GET, GET /id |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF675 | Geographic Location Management API | 4 | Optional | geographicLocation | GET, GET /id |
| TMF662 | Entity Catalog Management API | 4 | Optional | entitySpecification | GET, GET /id |
| TMF662 | Entity Catalog Management API | 4 | Optional | associationSpecification | GET, GET /id |
| TMF620 | Product Catalog Management API | 5 | Optional | productCatalog | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | category | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | exportJob | GET, GET /id, POST, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | importJob | GET, GET /id, POST, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | productOffering | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | productOfferingPrice | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 5 | Optional | productSpecification | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | catalog | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | category | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | productOffering | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | productSpecification | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | productOfferingPrice | GET, GET /id, POST, PATCH, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | importJob | GET, GET /id, POST, DELETE |
| TMF620 | Product Catalog Management API | 4 | Optional | exportJob | GET, GET /id, POST, DELETE |

![Dependent API diagram](TMFC001_Dependant_API.png)

*(PlantUML source: [TMFC001_Dependant_API.yaml](TMFC001_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF620 | Product Catalog Management API | productSpecificationCreate, productSpecificationDeleteEvent, categoryCreateEvent, categoryDeleteEvent, productOfferingCreateEvent, productOfferingAttributeValueChangeEvent, productOfferingStateChangeEvent, productOfferingDeleteEvent, productOfferingPriceCreateEvent, productOfferingPriceAttributeValueChangeEvent, productOfferingPriceStateChangeEvent, productOfferingPriceDeleteEvent, catalogCreateEvent, catalogDeleteEvent, catalogBatchEvent |
| TMF671 | Promotion Management API | promotionCreateEvent, promotionDeleteEvent, promotionAttributeValueChangeEvent, promotionStateChangeEvent, promotionInformationRequiredEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |

![Published Events diagram](TMFC001_Published_Events.png)

*(PlantUML source: [TMFC001_Published_Events.yaml](TMFC001_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF633 | Service Catalog Management | serviceSpecificationStateChange, serviceSpecificationAttributeValueChangeEvent, serviceSpecificationCreateEvent, serviceSpecificationDeleteEvent, resourceSpecificationCreateEvent, resourceSpecificationChangeEvent, resourceSpecificationDeleteEvent |
| TMF669 | Party Role Management API | partyRoleDeleteEvent |
| TMF632 | Party Management API | individualDeleteEvent, organizationDeleteEvent |

![Subscribed Events diagram](TMFC001_Subscribed_Events.png)

*(PlantUML source: [TMFC001_Subscribed_Events.yaml](TMFC001_Subscribed_Events.yaml))*

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
