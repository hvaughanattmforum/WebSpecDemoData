---
name: Service Inventory
---

# TMFC008 – Service Inventory

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Service Inventory | TMFC008 | The Service Inventory component is responsible for storage and exposure of CFS (Customer Facing Services) that are associated to Product Inventory items. It is also responsible for RFS (Resource Facing Service) definition, mapping between CFS and RFS and mapping with infrastructure/network resources. The Service Inventory component has functionality that enables creation of inventory items, inventory organization, inventory search or filter, inventory monitoring and tracking, inventory control and inventory auditing. The minimum check to be performed at inventory item creation or update is for global consistency with the related Service Catalog information. | Production |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.4.4 | L2 | Service Support Readiness | Manage service infrastructure, ensuring that the appropriate service capacity is available and ready to support the SM&O Fulfillment, Assurance and Billing processes. |
| 1.4.4.1 | L3 | Manage Service Inventory | Establish, manage and administer the enterprise's service inventory, as embodied in the Service Inventory Database, and monitor and report on the usage and access to the service inventory, and the quality of the data maintained in it. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Service |  |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC008_eTOM_SID.png)

*(PlantUML source: [TMFC008_eTOM_SID.puml](TMFC008_eTOM_SID.puml))*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 576 | Service Data Retrieval | Service Data Retrieval provides retrieval of appropriate inventory data for example in the context of service end to end testing. | Service Management | Service / Repository Management |
| 593 | Service Inventory Repository Updating | ServiceInventory Repository Updating updates information in the service inventory according to the configuration of specific services | Service Management | ServiceInventory Repository Management |
| 628 | Service to Resource Relationship Management | Service to Resource Relationship Management provides Creation, Update and Deletion of the relations of stand-alone physical or logical resources whose assignment is critical to service's fulfillment, and whose tracking is critical to service operations, assurance, and billing, as well as, resources, which represent a larger resource structure supporting the service, often referred to as an Access Point. | Service Management | ServiceInventory Repository Management |
| 629 | Service to Resource Relationship Synchronization | Service to Resource Relationship Synchronization function entails reconciliation of the data in a Service Inventory Management system with inventory discovered from other sources and synchronizes mismatched service inventory records. | Service Management | ServiceInventory Repository Management |
| 630 | Service-Resource Relationship Management Notifications | Service-Resource Relationship Management Notifications; Notification of Service-Resource Relationship Management actions to relevant stakeholders | Service Management | Service Reporting Service / Repository Management |
| 964 | Onboarded Service Integration Configuration | Onboarded Service Integration Configuration function will configure the on boarded service and the relevant systems to establish integration automatically, when requested. There are several system services in the infrastructure that needs to be aware and integrated with the new service. | Service Management | Service / Repository Management |
| 965 | Service Instance Lifecycle Management | Service Instance Lifecycle Management function will control the starting of new instances and closing of instances of a service as well as other activity states of the service instances. / Software based Services’ performance and availability may be controlled by managing multiple instances of the service with multiple states of activity. | Service Management | ServiceInventory Repository Management |
| 1344 | Service Topology Discovery | Service Topology Discovery function provides the required capability to discover how resources (e.g. network) are related to each other in providing a service. | Service Management | Service / Repository Management |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC008_API_Context.svg)

*(SVG source: [TMFC008_API_Context.svg](TMFC008_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF638 | Service Inventory Management API | Mandatory | 5 | service | GET, GET /id, POST, PATCH, DELETE |
| TMF638 | Service Inventory Management API | Mandatory | 4 | service | GET, GET /id, POST, PATCH, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC008_Exposed_API.png)

*(PlantUML source: [TMFC008_Exposed_API.yaml](TMFC008_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF633 | Service Catalog Management API | 4 | Mandatory | serviceSpecification | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | PartyRole | GET, GET /id |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET, GET /id |
| TMF638 | Service Inventory Management API | 5 | Optional | service | GET, GET /id |
| TMF638 | Service Inventory Management API | 4 | Optional | service | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicSubAddress | GET, GET /id |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF675 | Geographic Location Management API | 4 | Optional | geographicLocation | GET, GET /id |
| TMF641 | Service Ordering Management API | 4 | Optional | serviceOrder | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | organization | GET, GET /id |

![Dependent API diagram](TMFC008_Dependant_API.png)

*(PlantUML source: [TMFC008_Dependant_API.yaml](TMFC008_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF638 | Service Inventory Management API | serviceCreateEvent, serviceAttributeValueChangeEvent, serviceStateChangeEvent, serviceDeleteEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |

![Published Events diagram](TMFC008_Published_Events.png)

*(PlantUML source: [TMFC008_Published_Events.yaml](TMFC008_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF639 | Resource Inventory Management API | resourceDeleteEvent |
| TMF638 | Service Inventory Management API | serviceCreateEvent, serviceAttributeValueChangeEvent, serviceStateChangeEvent, serviceDeleteEvent |
| TMF633 | Service Catalog Management API | serviceSpecificationDeleteEvent |
| TMF669 | Party Role Management API | partyRoleDeleteEvent |
| TMF674 | Geographic Site Management API | geographicSiteDeleteEvent |
| TMF675 | Geographic Location Management API | geographicLocationDeleteEvent |
| TMF632 | Party Management API | individualDeleteEvent, organizationDeleteEvent |
| TMF641 | Service Ordering Management API | serviceOrderDeleteEvent |

![Subscribed Events diagram](TMFC008_Subscribed_Events.png)

*(PlantUML source: [TMFC008_Subscribed_Events.yaml](TMFC008_Subscribed_Events.yaml))*

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
