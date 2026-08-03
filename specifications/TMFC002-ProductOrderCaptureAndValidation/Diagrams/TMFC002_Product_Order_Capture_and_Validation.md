---
name: Product Order Capture And Validation
---

# TMFC002 – Product Order Capture And Validation

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Product Order Capture And Validation | TMFC002 | This component captures what a customer wants to order based on the CSP's Product Catalog. It enables configuration of the product offerings and products desired, provides quotes, checks the eligibility of the customer order, and completes it with information needed such as the related parties or associated billing account and the delivery appointment. This component owns quote management, order capture and validation, using dedicated components (eg Offering Configurator, Service Qualification, Party Management) when needed. After the delivery of the customer product order items, this component is also in charge of the commercial closure of the order. It includes update of the Product Inventory (status and starting/end date of tariffs and discounts) and potential commercial rules control (eg receipt of the contract document signed by the customer). | CoreCommerce |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.1.9 | L2 | Selling | Responsible for managing prospective customers, for qualifying and educating customers, and matching customer expectations. Managing prospective parties with whom an enterprise may do business, such as potential existing or new customers and partners, for qualifying and educating them, and ensuring their expectations are met. |
| 1.1.9.2 | L3 | Develop Sales Proposal | Develop a sales proposal to respond to the customer's requirements. Develop a sales proposal to respond to a sales prospect's requirements. |
| 1.1.9.5 | L3 | Negotiate Sales/Contract | Close the sale with terms that are understood by the customer and are mutually agreeable to both the customer and the service provider. Close the sale with terms that are understood by the sales prospect, which now becomes a customer or some other party that make an enterprise's offerings to the market, such as a partner, and are mutually agreeable to both the customer or party and an enterprise. |
| 1.3.3 | L2 | Customer Order Handling | Responsible for accepting and issuing orders. Customer Order Processing Management business process directs and controls all activities that operationally realize orders for customer. Customer Order Processing Management assures the capture, processing, fulfillment, "shipping", delivery and reporting of customer orders from feasibility assessment, purchasing, payment, fulfillment and follow up with the customer for closure. |
| 1.3.3.10 | L3 | Manage Customer Order Placement | Manage Customer Order Placement business activity directs and controls the capture of information to enable create customer order, change customer order and validate customer order based on ordering information from customer. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Customer Product Order | SalesQuote BE |
| Customer Product Order | ShoppingCart BE |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC002_eTOM_SID.png)

*(PlantUML source: [TMFC002_eTOM_SID.puml](TMFC002_eTOM_SID.puml))*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 16 | Fallout Automated Correction | Fallout Automated Correction function tries to automatically fix fallouts in workflows before they go to a human for handling. This includes a Fallout Rules Engine that provides the capability to handling various errors or error types based on built rules. These rules can facilitate autocorrection, correction assistance, placement of errors in the appropriate queues for manual handling, as well as access to various systems. | Fallout Management | Fallout Correction Management |
| 17 | Fallout Correction Information Collection | Fallout Correction Information Collection collects relevant information for errors or situations that cannot be handled via Fallout Auto Correction. The intent is to reduce the time required by the technician in diagnosing and fixing the fallout. | Fallout Management | Fallout Correction Management |
| 18 | Fallout Management to Fulfillment Application Accessing | Fallout Management to Fulfillment Application Accessing function provides a variety of tools to facilitate Fallout Management access to other applications and repositories to facilitate proper Fallout Management. This can include various general access techniques such as messaging, publish and subscribe, etc. as well as specific APIs and contracts to perform specific queries or updates to various applications or repositories within the fulfillment domain. | Fallout Management | Fallout Repository Management |
| 19 | Fallout Manual Correction Queuing | Fallout Manual Correction Queuing function provides the required functionality to place error fallout into appropriate queues to be handled via various staff or workgroups assigned to handle or fix the various types of fallout that occurs during the fulfillment process. This includes the ability to create and configure queues, route errors to the appropriate queues, as well as the ability for staff to access and address the various fallout instances within the queues. | Fallout Management | Fallout Correction Management |
| 20 | Fallout Notification | Fallout Notification function provides the means to alert people or workgroups of some fallout situation. This can be done via a number of means, including email, paging, (Fallout management interface bus) etc. This function is done via business rules. | Fallout Management | Fallout Repository Management |
| 21 | Fallout Orchestration | The Fallout Orchestration function provides workflow and orchestration capability across Fallout Management. | Fallout Management | Fallout Correction Management |
| 22 | Fallout Reporting | Fallout Reporting provides various reports regarding Fallout Management, including statistics on fallout per various times periods (per hour, week, month, etc.) as well as information about specific fallout. | Fallout Management | Fallout Repository Management |
| 23 | Fallout Dashboard System Log-in Accessing | Fallout Dashboard System Log-in Accessing provides auto logon capability into various applications needed to analyze and fix fallout | Fallout Management | Fallout Repository Management |
| 24 | Pre-populated Fallout Information Presentation | Pre-populated Fallout Information Presentation automatically position the analyzer on appropriate screens pre-populated with information about the order(s) that's subject for fallout handling. | Fallout Management | Fallout Correction Management |
| 120 | Customer Order Capturing | Customer Order Capturing provides access to Order capture and negotiation capabilities or receives the captured Customer Order data from channels. Takes care of persistence using Customer Order Lifecycle Management. Including support of contract printing, integration with a locally installed cash management/cash register and a retail inventory system for order completion and ordered product versioning. | Product Configuration & Activation | Offer and Product Configuration |
| 176 | Customer Order Capturing Access | Customer Order Capturing Access provides front end support for the Customer Order Capturing functions defined by the order management. | Fulfillment Integration Management | Customer Fulfillment Access Management |
| 177 | Customer Order Take-over Management | Customer Order Take-over Management provides an ability to take over governance of orders handled by other channels (e.g., self-service) amend and relinquish while preserving all the captured data. | Customer Order Management | Customer Order Completion |
| 181 | Product Order Data Collection | Product Order Data Collection provides an aid in verification and issuance of a complete and valid customer order. This function checks delivery address, link with a payment, a billing account, a certified holder, etc. | Customer Order Management | Customer Order Completion |
| 204 | Customer Order Completion | The Customer OrderCompletion Entry Finalization function enables completion and finalization of the Customer Order with collection of Customer Data or installed base data according to the Catalog. It allows to complete the configuration element not necessary for the quotation. The complements could also concern links with actors, dates, address, billing account. | Customer Order Management | Customer Order Completion |
| 217 | Customer Order Establishment Tracking | Customer Order Establishment Tracking provides the functionality necessary to track and manage the distributed requests decomposed by Customer Order Distribution.This capability needs to be provided in both an ability to query in real time and a publish/subscribe mechanism to enable the use of the information wherever required. | Customer Order Management | Customer Order Repository Management |
| 236 | Customer Loyalty Subscription Management | Customer Loyalty SubscriptionManagement Configuration function manages information for subscription and deactivation to a Loyalty program. Subscription management includes: checking customer requirements, assigning one or more subgroups to which the customer belongs, assigning welcome points & send welcome messages, generate the unique Loyalty-identifier. Loyalty Subscription Management can assign multiple traffic channels to loyalty subscriptions (sim-cards, PBX, Call Data Network etc.). | Product Configuration & Activation | Offer and Product Configuration |
| 259 | External Call Center Access | External Call Center Access provides access to call center self-empowered fulfillment function providing an internet technology driven interface for the customer to undertake a variety of fulfillment functions directly for themselves. | Customer Order Management | Customer Order Repository Management |
| 277 | Shopping Cart Purchasing Access | *(no description available)* | *(no description available)* | *(no description available)* |
| 317 | Product Availability Area Checking | *(no description available)* | *(no description available)* | *(no description available)* |
| 343 | Mass Transaction Ordering | *(no description available)* | *(no description available)* | *(no description available)* |
| 379 | Product Customization Offering Management | *(no description available)* | *(no description available)* | *(no description available)* |
| 388 | Sales Order Reporting | *(no description available)* | *(no description available)* | *(no description available)* |
| 756 | Fallout Rule Based Error Correction | *(no description available)* | *(no description available)* | *(no description available)* |
| 934 | Sales Negotiation Support | *(no description available)* | *(no description available)* | *(no description available)* |
| 1063 | Sales Quote Management | *(no description available)* | *(no description available)* | *(no description available)* |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC002_API_Context.svg)

*(SVG source: [TMFC002_API_Context.svg](TMFC002_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF648 | Quote Management API | Optional | 4 | quote | POST, GET, GET /id, PATCH, DELETE |
| TMF663 | Shopping Cart Management API | Mandatory | 5 | shoppingCart | GET, GET /id, POST, PATCH, DELETE |
| TMF663 | Shopping Cart Management API | Mandatory | 4 | shoppingCart | POST, GET, GET /id, PATCH, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC002_Exposed_API.png)

*(PlantUML source: [TMFC002_Exposed_API.yaml](TMFC002_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF620 | Product Catalog Management API | 5 | Mandatory | productOffering | GET, GET /id |
| TMF620 | Product Catalog Management API | 5 | Mandatory | productOfferingPrice | GET, GET /id |
| TMF620 | Product Catalog Management API | 5 | Mandatory | productSpecification | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Mandatory | productCategory | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Mandatory | productOffering | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Mandatory | productOfferingPrice | GET, GET /id |
| TMF620 | Product Catalog Management API | 4 | Mandatory | productSpecification | GET, GET /id |
| TMF637 | Product Inventory Management API | 5 | Mandatory | product | GET, GET /id, POST, PATCH |
| TMF637 | Product Inventory Management API | 4 | Mandatory | product | GET, GET /id, POST, PATCH |
| TMF679 | Product Offering Qualification Management API | 4 | Optional | productOfferingQualification | GET, GET /id, POST, PATCH |
| TMF646 | Appointment Management API | 4 | Optional | appointment | GET, GET /id, POST, PATCH, DELETE |
| TMF646 | Appointment Management API | 4 | Optional | searchTimeSlot | GET, GET /id, POST, PATCH, DELETE |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicSubAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddressValidation | GET, GET /id, POST, PATCH |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF716 | Resource Reservation | 4 | Optional | resourceReservation | GET, GET /id, POST, PATCH, DELETE |
| TMF716 | Resource Reservation | 4 | Optional | cancelResourceReservation | GET, GET /id, POST |
| TMF687 | Stock Management API | 4 | Optional | checkProductStock | GET, GET /id, POST, DELETE |
| TMF687 | Stock Management API | 4 | Optional | queryProductStock | GET, GET /id, POST, DELETE |
| TMF687 | Stock Management API | 4 | Optional | reserveProductStock | GET, GET /id, POST, DELETE |
| TMF687 | Stock Management API | 4 | Optional | productStock | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | organization | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | partyRole | GET, GET /id |
| TMF666 | Account Management API | 5 | Optional | billingAccount | GET, GET /id |
| TMF666 | Account Management API | 4 | Optional | billingAccount | GET /id, GET |
| TMF676 | Payment Management API | 4 | Optional | payment | GET /id, GET |
| TMF683 | Party Interaction Management API | 5 | Optional | partyInteraction | GET, GET /id |
| TMF683 | Party Interaction Management API | 4 | Optional | partyInteraction | GET /id, GET |
| TMF638 | Service Inventory Management API | 5 | Optional | service | GET, GET /id |
| TMF638 | Service Inventory Management API | 4 | Optional | service | GET /id, GET |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET /id, GET |
| TMF701 | Process Flow Management API | 4 | Optional | processFlow | POST, PATCH, GET, GET /id |
| TMF701 | Process Flow Management API | 4 | Optional | taskFlow | POST, PATCH, GET, GET /id |
| TMF760 | Product Configuration Management API | 5 | Optional | checkProductConfiguration | GET, GET /id, POST |
| TMF760 | Product Configuration Management API | 5 | Optional | queryProductConfiguration | GET, GET /id, POST |
| TMF651 | Agreement Management API | 4 | Optional | agreement | GET, GET /id |

![Dependent API diagram](TMFC002_Dependant_API.png)

*(PlantUML source: [TMFC002_Dependant_API.yaml](TMFC002_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF648 | Quote Management API | quoteStateChangeEvent, quoteCreateEvent, quoteAttributeValueChangeEvent, quoteDeleteEvent, quoteInformationRequiredEvent |
| TMF663 | Shopping Cart Management API | shoppingCartCreateEvent, shoppingCartAttributeValueChangeEvent, shoppingCartDeleteEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |

![Published Events diagram](TMFC002_Published_Events.png)

*(PlantUML source: [TMFC002_Published_Events.yaml](TMFC002_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF679 | Product Offering Qualification Management API | productOfferingQualificationStateChangeEvent |
| TMF673 | Geographic Address Management API | geographicAddressValidationStateChangeEvent |
| TMF670 | Payment Management API | paymentCreateEvent, paymentStateChangeEvent |
| TMF716 | Resource Reservation | resourceReservationCreateEvent, resourceReservationAttributeValueChangeEvent, resourceReservationDeleteEvent, resourceReservationStateChangeEvent, resourceReservationInformationRequiredEvent, cancelResourceReservationCreateEvent, cancelResourceReservationStateChangeEvent, cancelResourceReservationInformationRequiredEvent |

![Subscribed Events diagram](TMFC002_Subscribed_Events.png)

*(PlantUML source: [TMFC002_Subscribed_Events.yaml](TMFC002_Subscribed_Events.yaml))*

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
