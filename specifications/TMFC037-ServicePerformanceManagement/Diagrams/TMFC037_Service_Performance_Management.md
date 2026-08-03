---
name: Service Performance Management
---

# TMFC037 – Service Performance Management

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Service Performance Management | TMFC037 | Service Performance Management component monitors, analyzes, and reports on end-to-end service performance. This can include a real-time, end-to-end view to ensure that each service is functioning correctly as well as a historical view. These functions build on the Resource Performance data and active end-to-end service performance test data to provide a view of a service. The component provides a key input to determine Quality of Service. | Production |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.4.7 | L2 | Service Performance Management | Service Performance Management business process directs and controls activities that define Service Performance Objectives (e.g. Service Availability, Service Quality, Process efficiency, Service Reliability, etc.), sets performance goals & targets, track performance trends, monitor performance, analyze performance, control performance (optimize, troubleshoot), report or communicate performance, and manage consequences of service performance. Service Performance Management business process supports the Enterprise Performance Management goals. These goals include quality, efficiency, reliability, availability, monetary (cost, profitability, etc.) mandates along with any productivity requirement of service delivery and service engagement by the organization. It includes identifying, establishing the applying the methodologies that define and manage service performance criteria to meet business objectives. / This process was renamed in 23.5 it was named Service Quality Management. |
| 1.4.7.6 | L3 | Manage Service Performance Requirement | Manage Service Performance Requirement business activity controls activities and underlying tasks that define the performance requirements for a service. It sets the standards and expectations for service performance. / Manage Service Performance Requirement's goal is to ensure that the service meets or exceeds predefined performance standards. It involves setting service performance goals and making changes to these goals as necessary. It also includes defining the information required to measure service performance. |
| 1.4.7.7 | L3 | Manage Service Performance Plan | Manage Service Performance Plan business activity controls the creating, implementing, improving, and terminating of plan(s) for service performance. / Manage Service Performance Plan's goal is to ensure that there is a clear and effective plan in place for managing service performance. This includes defining the plan, implementing it, making improvements to the plan over time, and terminating the plan when it is no longer needed. |
| 1.4.7.8 | L3 | Manage Service Performance Measure | Manage Service Performance Measure business activity controls the definition, change, and removal of measures for service performance. / Manage Service Performance Measure's goal is to ensure that service performance is accurately measured and tracked. This includes defining what measures will be used, making changes to these measures as necessary, and removing measures that are no longer relevant or useful. |
| 1.4.7.9 | L3 | Manage Service Performance Analysis | Manage Service Performance Measure business activity controls the definition, change, and removal of measures for service performance. / Manage Service Performance Measure's goal is to ensure that service performance is accurately measured and tracked. This includes defining what measures will be used, making changes to these measures as necessary, and removing measures that are no longer relevant or useful. |
| 1.4.7.10 | L3 | Manage Service Performance Control | Manage Service Performance Control business activity is responsible for monitoring, evaluating, and improving service performance. / Manage Service Performance Control's goal is to maintain control over service performance. This includes monitoring performance on an ongoing basis, evaluating whether performance goals are being met, and providing support for making improvements as necessary. |
| 1.4.7.11 | L3 | Manage Service Performance Reporting | Manage Service Performance Reporting business activity is responsible for creating, changing, and publishing reports on service performance. / Manage Service Performance Reporting's goal is to communicate information about service performance to relevant stakeholders. This includes creating reports that accurately reflect current performance levels, making changes to these reports as necessary, and publishing these reports in a timely manner. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Service Performance |  |
| Performance | MeasurementProductionJob |
| Performance | AdhocCollection |
| Performance | MeasurementCollectionJob |
| Performance | Performance Threshold |
| Resource Trouble | Alarm |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC037_eTOM_SID.svg)

*(SVG source: [TMFC037_eTOM_SID.svg](TMFC037_eTOM_SID.svg) — hand-drawn rather than PlantUML: this diagram
has 6 eTOM activities + 6 SID entities = 12 elements, past the 6-element threshold where plain PlantUML
layout gets visually messy. "Manage Service Performance Plan" is drawn with no connecting links, matching
the source diagram. One additional link not shown above, between two eTOM activities directly rather than
an eTOM-to-SID pair: "Mnge Service Performance Analysis" → "Mnge Service Performance Control"
(one-directional).)*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 603 | Service Performance Data Collection | Service Performance Data Collection collects Service Performance Data from the Resource Management functions related to a specific Service (or directly in the absence of Resource Performance Management function) and Collection of Service Performance data from the end-to-end tests done by the service test functions internally or from external Service Test applications. Including archiving. | Service Quality and Performance Management | Service Quality and Performance Inventory Management |
| 604 | Service Performance Event Correlation | Service Performance Event Correlation maps the performance data to service topology and identifies service related performance problems, event filtering included. | Service Quality and Performance Management | Service Quality and Performance Analysis |
| 605 | Service Performance Monitoring | Service Performance Monitoring provides monitoring of service performance data including notification and accumulation for e.g. Service Performance Dashboard. | Service Quality and Performance Management | Service Quality and Performance Analysis |
| 606 | Service Performance Reporting | Service Performance Reporting provides the necessary functionality required to generate reports about the performance of the service provider's services. These reports may be generated as part of the normal periodic operations ("scheduled") or may be as a result of a specific analysis request ("in-demand").  Report types include near real time, historical view, and trend analysis. Relevant performance reports are also provided to service/network planning to perform network updates. | *(no description available)* | Service Quality and Performance Inventory Management |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC037_API_Context.svg)

*(SVG source: [TMFC037_API_Context.svg](TMFC037_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF628 | Performance Management API | Mandatory | 5 | measurementCollectionJob | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | Mandatory | 5 | onDemandCollection | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | Mandatory | 5 | performanceIndicatorGroupSpecification | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | Mandatory | 5 | performanceIndicatorSpecification | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | Mandatory | 5 | trackingRecord | GET, GET /id |
| TMF649 | Performance Threshold Management API | Mandatory | 4 | threshold | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF649 | Performance Threshold Management API | Mandatory | 4 | thresholdJob | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF642 | Alarm Management API | Optional | 5 | alarm | GET, GET /id, POST |
| TMF642 | Alarm Management API | Optional | 4 | alarm | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC037_Exposed_API.png)

*(PlantUML source: [TMFC037_Exposed_API.yaml](TMFC037_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF628 | Performance Management API | 5 | Optional | measurementCollectionJob | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | 5 | Optional | onDemandCollection | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | 5 | Optional | performanceIndicatorGroupSpecification | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | 5 | Optional | performanceIndicatorSpecification | POST, GET, GET /id, PATCH /id, DELETE /id |
| TMF628 | Performance Management API | 5 | Optional | trackingRecord | GET, GET /id |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET, GET /id |
| TMF642 | Alarm Management API | 4 | Optional | alarm | GET, GET /id |
| TMF638 | Service Inventory Management API | 5 | Mandatory | service | GET, GET /id |
| TMF638 | Service Inventory Management API | 4 | Mandatory | service | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicAddress | GET, GET /id |
| TMF673 | Geographic Address Management API | 4 | Optional | geographicSubAddress | GET, GET /id |
| TMF674 | Geographic Site Management API | 4 | Optional | geographicSite | GET, GET /id |
| TMF657 | Service Quality Management API | 4 | Optional | serviceLevelObjective | GET, GET /id |
| TMF657 | Service Quality Management API | 4 | Optional | serviceLevelSpecification | GET, GET /id |
| TMF701 | Process Flow Management API | 4 | Optional | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | 4 | Optional | taskFlow | PATCH, GET, GET /id |

![Dependent API diagram](TMFC037_Dependant_API.png)

*(PlantUML source: [TMFC037_Dependant_API.yaml](TMFC037_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, processFlowStateDeleteEvent, processFlowStateAttributeValueChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent, taskFlowDeleteEvent, taskFlowAttributeValueChangeEvent, taskFlowInformationRequiredEvent |
| TMF642 | Alarm Management API | alarmStateChange**, alarmCreateEvent**, alarmClearEvent**, alarmAckEvent** |
| TMF628 | Performance Management API | measurementCollectionJobCreateEvent, measurementCollectionJobExecutionStateChangeEvent, measurementCollectionJobDeleteEvent, measurementCollectionJobAttributeValueChangeEvent, measurementCollectionJobFilesReadyEvent, measurementCollectionJobFilesPreparationErrorEvent, onDemandCollectionCreateEvent, onDemandCollectionExecutionStateChangeEvent, onDemandCollectionDeleteEvent, onDemandCollectionAttributeValueChangeEvent, onDemandCollectionFilesReadyEvent, onDemandCollectionFilesPreparationErrorEvent, thresholdCreateNotification, thresholdChangeNotification, thresholdRuleCreateNotification, thresholdRuleChangedNotification, thresholdJobCreateNotification, thresholdJobChangedNotification, thresholdJobSuspendNotification, thresholdJobResumeNotification |

![Published Events diagram](TMFC037_Published_Events.png)

*(PlantUML source: [TMFC037_Published_Events.yaml](TMFC037_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF633 | Service Catalog Management API | serviceSpecificationChangeEvent |
| TMF638 | Service Inventory Management API | serviceCreateEvent, serviceAttributeValueChangeEvent, serviceStateChangeEvent, serviceDeleteEvent |
| TMF639 | Resource Inventory Management API | resourceCreateEvent, resourceAttributeValueChangeEvent, resourceStateChangeEvent, resourceDeleteEvent |
| TMF701 | Process Flow Management API | processFlowCreateEvent, processFlowStateChangeEvent, taskFlowCreateEvent, taskFlowStateChangeEvent |

![Subscribed Events diagram](TMFC037_Subscribed_Events.png)

*(PlantUML source: [TMFC037_Subscribed_Events.yaml](TMFC037_Subscribed_Events.yaml))*

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

| Standard | Version(s) |
|---|---|
| eTOM | n/a |
| SID | v25.0 |
| Functional Framework | n/a |
