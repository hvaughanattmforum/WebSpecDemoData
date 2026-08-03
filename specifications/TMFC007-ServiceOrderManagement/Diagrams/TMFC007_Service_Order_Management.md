---
name: Service Order Management
---

# TMFC007 – Service Order Management

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Service Order Management | TMFC007 | Service Order Management (SOM) component is the entry point to the Production Domain. It oversees delivery of Customer-Facing-Service (CFS) resources (network and service platform equipment). The SOM exposes the API ServiceOrder. It is triggered when the Product Order Delivery Orchestration And Management component calls this API to request CFS delivery. To achieve delivery of a CFS, the SOM orchestrates the CFS delivery process which identifies possible RFS and chooses one, using the catalog and technical inventory. It selects the resources (servers, equipment, etc.) and their instances, and requests the Resource Order Management (ROM) component to update selected resource instances to deliver CFS. Requests sent to the ROM contain the CFS and the list of configured resource instances to be updated. | Production |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.4.5 | L2 | Service Configuration & Activation | Allocation, implementation, configuration, activation and testing of specific services to meet customer requirements. |
| 1.4.5.1 | L3 | Design Solution | Develop an end-end specific service design which complies with a particular customer's requirement |
| 1.4.5.2 | L3 | Allocate Specific Service Parameters to Services | Issue service identifiers for new services. |
| 1.4.5.3 | L3 | Track & Manage Service Provisioning | Ensure service provisioning activities are assigned, managed and tracked efficiently. |
| 1.4.5.4 | L3 | Implement, configure & activate service | Implement, configure and activate the specific services allocated against an issued service order. |
| 1.4.5.6 | L3 | Issue Service Order | Issue correct and complete service orders |
| 1.4.5.7 | L3 | Report service provisioning | Monitor the status of service orders, provide notifications of any changes and provide management reports. |
| 1.4.5.8 | L3 | Close Service Order | Close a service order when the service provisioning activities have been completed |
| 1.5.6 | L2 | Resource Provisioning | *(no description available)* |
| 1.5.6.7 | L3 | Issue Resource Order | *(no description available)* |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Service Order |  |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC007_eTOM_SID.png)

*(PlantUML source: [TMFC007_eTOM_SID.puml](TMFC007_eTOM_SID.puml))*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 584 | Service Activation Planning | Service Activation Planning provides planning of service activation to access, plan and gather additional information for service activation. | Service Order Management | Service Order Orchestration |
| 588 | Service Orchestration Configuration | Service Orchestration Configuration function provides composition of a service configuration plan according to the required service actions and sent to Service Order Orchestration and/or Service Activation Management. | Service Order Management | Service Order Orchestration |
| 591 | Service Parameters Allocation | Service Parameters Allocation provides allocation of the right service parameters to fulfill service orders. | Service Order Management | Service Order Orchestration |
| 596 | Service Order Transfer Supervision | Oversees the transfer of Service Order Requests to appropriate resource providers. | Service Order Management | Service Order Orchestration |
| 598 | Service Order Orchestration | The Service Order Orchestration function provides workflow and orchestration capabilities for a dedicated Service (CFS) Order. / Orchestration is needed when: / the technical solution includes the expansion of the operator Installed Resources or the purchase of a partner product (ex: local loop purchase) / a work order is necessary at the delivery address or somewhere in the operator network / part of the delivery process or checks needs to be delegated to another Service Order Manager / contributing or support systems must be informed / Example: to deliver a VOIP service, it will orchestrate actions on Access Network Factory, VOIP service platform and CPE. / Service Order Orchestration will also orchestrate and manage dependencies between related Service Order items of Service Order. | Service Order Management | Service Order Orchestration |
| 733 | Service Order Decomposition | The Service Order Decomposition Function allows in the context of a Service Order to prepare Resource Order, Service Order which will be delegated to another system, Supplier Order, Stock Item Order or Work Order with the necessary information (the effective update in the order repositories will be supported by the corresponding Order Repository Management functions). / In the case of a Service associated with an existing Internal Resource Type, this function also allows to: / • Check if a corresponding Installed Resource is operational in the resource installed base, and determine the operation to be performed at Resource level (creation or modification) / • Eventually group in the same Resource order several ordered services, based on the same Customer Facing Service Specification (a.k.a. CFS specification), and/or identified to be delivered at the same time by the Service Order Delivery Orchestration. | Service Order Management | Service Order Delivery Preparation |
| 734 | Service Data Collection | The Service Data Collection function gathers any needed service data to aid in the verification and issuance of a complete and valid service order as well as data necessary to address dependencies between service and/or resource orders. | Service Order Management | Service Order Orchestration |
| 963 | Service Task Item Decomposition | Service Task Item Decomposition: By a request for an orchestration of a service the service needs to be analyzed and decomposed into the part-actions necessary to take to fulfill the requested orchestration. The Service may consist of several services and may use a number of Resources. It may also be controlled by several parameters for optional behaviors. This composition of the Service is given by configuration data available from Catalog applications and the Service Capability Orchestration application. | Service Order Management | Service Order Orchestration |
| 968 | Service Work Item Sequence Execution | Service Work Item Sequence Execution function executes each individual item in sequence of the service orchestration to fulfill, or roll back according to a pre-defined configuration, and reports the sequence execution result. / Because of the “Service Decomposition” of an orchestration request the result may be several actions that needs to take place in a specific sequence. | Service Order Management | Service Order Orchestration |
| 969 | Service Work Item Sequence Execution Configuration | The “Service Work Item Sequence Execution" function controls so that the sequence is fulfilled or rolled back. The rules for the sequence execution will set the conditions for the fulfillment, or roll-back, and for the reporting and notification. The “Service Task Item Sequence Carry Through configuration" is a management of the application function that defines how the execution of the orchestration sequence will be done. | Service Order Management | Service Order Orchestration |
| 571 | Service Delivery Due Date Calculation | Service Delivery Due Date Calculation functions calculates the service delivery due date using network capacity, access provider selection and work center intelligence (including workload and capacity). | Service Order Management | Service Order Initialization |
| 1061 | Service Order Initiation | Service Order Initiation function issues valid and complete service orders. / As part of order issuing/publication, additional data might be obtained or derived to support downstream functions that are not provided in the service order request. | Service Order Management | Service Order Initialization |
| 595 | Service Order Completion | Completes the service order when all resource orders have been completed. | Service Order Management | Service Order Completion |
| 600 | Service Order Validation | The Service Order Validation function validates the service order request based on contract, catalog, and provisioning rules. | Service Order Management | Service Order Completion |
| 583 | Activation Notification | Activation Notification function provides notifications on successful activation and, in cases of exceptions send fallouts to Service Order Orchestration and manage rollbacks activities (if applicable). | Service Order Management | Service Order Repository Management |
| 594 | Service Order Storage | Service order Storage function stores the service order into an appropriate data store. | Service Order Management | Service Order Repository Management |
| 597 | Service Order Exposure | Service Order Exposure provides exposure of the status on the overall service order. | Fulfillment Integration Management | Service Fulfillment Access Management |
| 599 | Service Order Tracking | The Service Order Tracking function tracks and manages the events and the lifecycle related to the Service (CFS) Order and to its items (e.g.: service order lines). / It gathers Service Order items delivery events from Service Order Orchestration and manages related Service Order lifecycle and Installed CFS lifecycle (via the Installed Service Management function). / Depending on the Service Order (or any of its elements) events, and on the implemented business rules, this function can decide to notify other systems (for example in case of delivery problems or delays) – via the business event publication function. | Service Order Management | Service Order Repository Management |
| 735 | Access Provider Selection | Access Provider Selection function selects an access provider among identified available access providers or access technologies at the given location, based on business rules. | Service Order Management | Service Technical Solution Identification |
| 341 | Service Activation | Service Activation function for services/products sold by affiliates. | Service Configuration & Activation | Service Activation |
| 342 | Mass Service Pre-activation | Mass Service Pre-activation of services to prepare for a swift activation at sales. E.g., subsequent affiliate sales. | Service Configuration & Activation | Service Activation |
| 570 | Solution Services Design Management | Solution Services Design Management function supports the end to end service design. It applies engineering rules to determine required network facilities, equipment configurations and the method and access path to the customer site or location of service termination. / This function also establishes and manages the detailed design tasks required to issue the work orders. | Service Configuration & Activation | Service Configuration |
| 589 | Cross Services Dependencies Configuration | Cross Services Dependencies Configuration function provides support for appropriately considered cross service dependencies as part of the configuration activities to fulfill a service order. | Service Configuration & Activation | Service Configuration |
| 590 | Service Configuration | The Service Configuration function is in charge of configuring the specific service and its parameters as appropriate for the fulfillment of a service order. | Service Configuration & Activation | Service Configuration |
| 585 | Service Configuration Activation | Service Configuration Activation implements and activates the specific service configuration against the service configuration plan (including activation of CPE if part of the service). | Service Configuration & Activation | Service Activation |
| 592 | Service Parameters Reservation | Service Parameters Reservation reserves the right service parameters based on service specification and service inventory for a service order. | Service Order Management | Service Availability |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC007_API_Context.svg)

*(SVG source: [TMFC007_API_Context.svg](TMFC007_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF641 | Service Ordering Management API | Mandatory | 4 | serviceOrder | GET, GET /id, POST, PATCH, DELETE |
| TMF641 | Service Ordering Management API | Mandatory | 4 | cancelServiceOrder | GET, GET /id, POST |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | GET, GET /id, POST, DELETE /id |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | GET, GET /id, PATCH /id |

![Exposed API diagram](TMFC007_Exposed_API.png)

*(PlantUML source: [TMFC007_Exposed_API.yaml](TMFC007_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF632 | Party Management API | 5 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | organization | GET, GET /id |
| TMF633 | Service Catalog Management API | 4 | Mandatory | serviceSpecification | GET, GET /id |
| TMF634 | Resource Catalog Management API | 5 | Optional | resourceSpecification | GET, GET /id |
| TMF634 | Resource Catalog Management API | 4 | Optional | resourceSpecification | GET, GET /id |
| TMF638 | Service Inventory Management API | 5 | Mandatory | service | GET, GET /id, POST, PATCH, DELETE |
| TMF638 | Service Inventory Management API | 4 | Mandatory | service | GET, GET /id, POST, PATCH, DELETE |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET, GET /id |
| TMF640 | Service Activation Management API | 4 | Optional | monitor | GET, GET /id |
| TMF641 | Service Ordering Management API | 4 | Optional | serviceOrder | GET, GET /id, POST, PATCH, DELETE |
| TMF641 | Service Ordering Management API | 4 | Optional | cancelServiceOrder | GET, GET /id, POST |
| TMF645 | Service Qualification Management API | 5 | Optional | checkServiceQualification | GET, GET /id, POST, PATCH |
| TMF645 | Service Qualification Management API | 5 | Optional | queryServiceQualification | GET, GET /id, POST, PATCH |
| TMF645 | Service Qualification Management API | 4 | Optional | checkServiceQualification | GET, GET /id, POST, PATCH |
| TMF645 | Service Qualification Management API | 4 | Optional | queryServiceQualification | GET, GET /id, POST, PATCH |
| TMF646 | Appointment Management API | 4 | Optional | appointment | GET, GET /id, POST, PATCH |
| TMF646 | Appointment Management API | 4 | Optional | searchTimeSlot | GET, GET /id, POST, PATCH |
| TMF652 | Resource Order Management API | 4 | Optional | resourceOrder | GET, GET /id, POST, PATCH, DELETE |
| TMF652 | Resource Order Management API | 4 | Optional | cancelResourceOrder | GET, GET /id, POST, PATCH, DELETE |
| TMF653 | Service Test Management API | 4 | Optional | serviceTest | GET, GET /id |
| TMF653 | Service Test Management API | 4 | Optional | serviceTestSpecification | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | partyRole | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicSubAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddressValidation | GET, GET /id, POST |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicLocation | GET, GET /id |
| TMF675 | Geographic Location Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF681 | Communication Management API | 4 | Optional | communicationMessage | GET, GET /id |
| TMF697 | Work Order Management API | 4 | Optional | workOrder | GET, GET /id |
| TMF701 | Process Flow Management API | 4 | Optional | processFlow | POST, GET, GET /id, PATCH |

![Dependent API diagram](TMFC007_Dependant_API.png)

*(PlantUML source: [TMFC007_Dependant_API.yaml](TMFC007_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF641 | Service Ordering Management API | serviceOrderCreateEvent, serviceOrderStateChangeEvent, serviceOrderDeleteEvent, serviceOrderAttributeValueChangeEvent, serviceOrderInformationRequiredEvent, serviceOrderMilestoneEvent, serviceOrderJeopardyEvent, cancelServiceOrderCreateEvent, cancelServiceOrderStateChangeEvent, cancelServiceOrderInformationRequiredEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |

![Published Events diagram](TMFC007_Published_Events.png)

*(PlantUML source: [TMFC007_Published_Events.yaml](TMFC007_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF634 | Resource Catalog Management API | resourceOrderStateChange, resourceOrderAttributeValueChangeEvent, resourceOrderInformationRequiredEvent, cancelResourceOrderStateChange, cancelResourceOrderInformationRequiredEvent |
| TMF645 | Service Qualification Management API | checkServiceQualificationStateChangeEvent, queryServiceQualificationStateChangeEvent |
| TMF681 | Communication Management API | communicationMessageStateChangeEvent |
| TMF697 | Work Order Management API | workOrderStateChange |

![Subscribed Events diagram](TMFC007_Subscribed_Events.png)

*(PlantUML source: [TMFC007_Subscribed_Events.yaml](TMFC007_Subscribed_Events.yaml))*

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

| Standard | Version(s) |
|---|---|
| eTOM | v21.5 |
| SID | v25.0 |
| Functional Framework | v21.5 |
