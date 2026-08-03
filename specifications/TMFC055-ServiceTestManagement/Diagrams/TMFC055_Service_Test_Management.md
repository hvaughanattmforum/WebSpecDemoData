---
name: Service Test Management
---

# TMFC055 – Service Test Management

## 1. Overview

| Component Name | ID | Description | ODA Function Block |
|---|---|---|---|
| Service Test Management | TMFC055 | Service Test Management is responsible for managing the service test specification and executing tests based on this specification to ensure the service operates correctly.      Service test specification involves capturing potential tests for each Service Specification that can be initiated either automatically or manually by the service user. These tests are derived from those available at the service specification or resource specification level. The scope of the component includes the end-to-end execution and reporting of tests, tailored to the specific context and actor involved. | Production |

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM business activities

eTOM business activities this ODA Component is responsible for:

| Identifier | Level | Business Activity Name | Description |
|---|---|---|---|
| 1.4.1 | L2 | Service Strategy Management | Enable the development of a strategic view and a multi-year business plan for the enterprise’s services and service directions, and the parties who will supply the required services. |
| 1.4.1.8 | L3 | Service Test Strategy | Service Test Strategy develops the strategies of the enterprise for Service Test. / This process is in charge of identifying types of Service Test to be conducted according to different context (i.e. business activities) for types of Services. / The different context for Service Test are: / - Service Development & Retirement to qualify the capacity to deliver Services before validating a new ServiceSpecification / - Service Configuration & Activation to test the Service before closing the ServiceOrderItem / - Service Quality Management to test Service Quality / - Service Problem Management to test Service functioning / - Service Test Management to conduct tests not specific to a customer’s product |
| 1.4.3.8 | L3 | Service Specification Test Development & Retirement | Service Test Development & Retirement is in charge of the Service Test catalogue. / A type of Service Test aims at measuring proper functioning and capacities of a Service. / Service Test Development & Retirement includes: / - Specifying in detail each Service Test according to the different context. It includes specifying: / - the roles authorized to use the Test and quotas for each type of role / - the method to conduct the Test / - the rules that define the strategies for conducting the test (including  the test plan) / - the thresholds and related actions / - the relationships with lower level tests (Resource Test) / - the report of test results with rules for enrichment of Resource Tests results according to role asking for it / - Specifying test scenarios defining sequence of Tests with rules about context and planning to trigger it. It includes roles allowed for asking test scenario and corresponding quotas. |
| 1.4.1.9 | L3 | Analyze Service Test Quality | Analyze Service Test Quality process performs quality analysis of service testing processes, in order to continuously fine-tune and improve them. / Service Test Quality Analysis processes provide an offline analysis of the performance of service testing processes to ensure their continuous fitness for purpose, and eventually propose modifications or enhancements to the current service test specifications (including: service testing methods, quota, authorized users, recommendations and course of action if needed). / The analysis is done using statistical service test usage data to evaluate service tests performance and required improvements if needed. / Following the analysis, typical course of action can be: / - No changes needed currently, / - Creation of additional service tests, / - Improving existing service tests, / - Removing service tests that are no longer relevant. |

### 2.2. SID ABEs

SID ABEs this ODA Component is responsible for:

| SID ABE Level 1 | SID ABE Level 2 (or set of BEs) |
|---|---|
| Service Test | ServiceTest BE |
| Service Test | ServiceTestSpec BE |

### 2.3. eTOM L2 - SID ABEs links

![eTOM L2 - SID ABEs links diagram](TMFC055_eTOM_SID.png)

*(PlantUML source: [TMFC055_eTOM_SID.puml](TMFC055_eTOM_SID.puml))*

### 2.4. Functional Framework Functions

| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |
|---|---|---|---|---|
| 625 | Service Test Operation Control | Service Test Operation Control function provides the necessary functionality to access, command and control the various service test devices required to perform service testing. | Service Capability Management | Service Test Resource Check |
| 1136 | Service Test Specification and Scenario Management | Service Test Specification and Scenario Management Function includes: / Test scenario management: for example, a home equipment self-test can trigger a test scenario that verifies the functioning of all the services associated, depending on the installed products of the user. Thus, the box could test its internal configuration and functioning and its capacity to connect to internet and VoIP services. / Managing service test capabilities: some resources used to implement services have limited capabilities for executing tests, especially for multiple parallel testing. All the constraints linked to limited resources test capabilities and depending on the execution context must be aggregated and managed at service test level. / Managing initiator authorization: some tests are restricted to some user roles (internal or external) so the authorization are defined at the Service Test Strategy and Policy Management. | Service Test Specification Development | Service Test Policy Management |
| 566 | Service Test Result Analysis Policy Configuration | Service Test Result Analysis Policy Configuration functions provide the necessary functionality to manage how the test results should be interpreted. / Strategies can range from simple (e.g. - check the status of a router) to complex (e.g. - perform an end-to-end test on a circuit and sectionalize the problem). | Service Test Specification Development | Service Test Policy Management |
| 573 | Service Testing Rules Management | Service Testing Rules Management provides management of service testing rules. | Service Test Specification Development | Service Test Policy Management |
| 581 | Automated Service Test Invocation | Automated Service Test Invocation provides automated invocation of Service Test Services for test and retrieval of results from the resource testing capabilities. | Service Test Management | Service Test Conducting |
| 1138 | Service Test Reporting Rules Management | Service Test Reporting Rules Management Function includes: / Test rules defining the enrichment of test results. / -   For example: enrichment of internet bandwidth measure based on installed product / Test rules defining the restitution of the result depending on test execution context / -   For example: a test result of ok/not ok can be enough for a user whereas customer care requires more details in the result of the test. | Service Test Specification Development | Service Test Policy Management |
| 582 | Manual Service Test Invocation | Manual Service Test Invocation provides a user interface (GUI) function that provides the means to access the testing capabilities. | Service Test Management | Service Test Conducting |
| 627 | Service Test Strategy Management | Service Test Strategy Management functions provide the necessary functionality to manage the local rules that define the strategies for conducting a test as well as how the test results should be interpreted. | Service Strategy Management | Service Strategy Design and Planning |
| 1137 | Service Test Rules Management | Service Test Rules Management Function includes: / Test rules defining the strategies for setting up test configuration / Test rules defining how to carry out the service test. / - For example: to choose the next test in a scenario depending on the results of the previous tests. | Service Test Specification Development | Service Test Policy Management |
| 575 | Service Test Results Reporting | Service Test Results Reporting provides reporting of service end-to-end test results back to the client. | Service Test Management | Service Test Reporting |
| 626 | Service Testing Management | Service Testing Management functions provides the necessary functionality to manage the end-to-end lifecycle of a test of a service. / Including the management of scheduling, retrieval of appropriate inventory data, setting up the test configuration, acquisition and management of test resources, test results interpretation, reporting of test results and close down of the test of the service. | Service Test Management | Service Test Repository Management |
| 577 | Service End to End Test Scheduling | Service End to End Test Scheduling provides scheduling of end-to-end testing of services. | Service Test Specification Development | Service Test Policy Management |
| 579 | Service End to End Testing | Service End to End Testing provides test execution of the end-to-end service testing. | Service Test Management | Service Test Conducting |

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram](TMFC055_API_Context.svg)

*(SVG source: [TMFC055_API_Context.svg](TMFC055_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-markdown`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |
|---|---|---|---|---|---|
| TMF653 | Service Test Management API | Mandatory | 4 | serviceTest | GET, POST, GET /id, PATCH /id, DELETE /id |
| TMF653 | Service Test Management API | Mandatory | 4 | serviceTestSpecification | GET, POST, GET /id, PATCH /id, DELETE /id |
| TMF701 | Process Flow Management API | Optional | 4 | processFlow | POST, GET, GET /id, DELETE |
| TMF701 | Process Flow Management API | Optional | 4 | taskFlow | PATCH, GET, GET /id |

![Exposed API diagram](TMFC055_Exposed_API.png)

*(PlantUML source: [TMFC055_Exposed_API.yaml](TMFC055_Exposed_API.yaml))*

### 3.3. Dependent APIs

| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |
|---|---|---|---|---|---|
| TMF632 | Party Management API | 5 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 5 | Optional | organization | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | individual | GET, GET /id |
| TMF632 | Party Management API | 4 | Optional | organization | GET, GET /id |
| TMF669 | Party Role Management API | 5 | Optional | partyRole | GET, GET /id |
| TMF669 | Party Role Management API | 4 | Optional | partyRole | GET, GET /id |
| TMF633 | Service Catalog Management API | 4 | Optional | serviceSpecification | GET, GET /id |
| TMF638 | Service Inventory Management API | 5 | Mandatory | service | GET, GET /id |
| TMF638 | Service Inventory Management API | 4 | Mandatory | service | GET, GET /id |
| TMF639 | Resource Inventory Management API | 4 | Optional | resource | GET, GET /id |
| TMF701 | Process Flow Management API | 4 | Optional | processFlow | GET, GET /id, POST, PATCH |
| TMF701 | Process Flow Management API | 4 | Optional | taskFlow | GET, GET /id, POST, PATCH |

![Dependent API diagram](TMFC055_Dependant_API.png)

*(PlantUML source: [TMFC055_Dependant_API.yaml](TMFC055_Dependant_API.yaml))*

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF653 | Service Test Management API | serviceTestCreateEvent, serviceTestStateChangeEvent, serviceTestSpecificationCreateEvent, serviceTestSpecificationDeleteEvent, serviceTestAttributeValueChangeEvent, serviceTestDeleteEvent, serviceTestSpecificationAttributeValueChangeEvent |

![Published Events diagram](TMFC055_Published_Events.png)

*(PlantUML source: [TMFC055_Published_Events.yaml](TMFC055_Published_Events.yaml))*

#### Subscribed Events

| API ID | API Name | Event Resources |
|---|---|---|
| TMF633 | Service Catalog Management API | serviceSpecificationCreateEvent, serviceSpecificationDeleteEvent |
| TMF632 | Party Management API | organizationDeleteEvent, individualDeleteEvent |

![Subscribed Events diagram](TMFC055_Subscribed_Events.png)

*(PlantUML source: [TMFC055_Subscribed_Events.yaml](TMFC055_Subscribed_Events.yaml))*

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

| Standard | Version(s) |
|---|---|
| eTOM | v24.5 |
| SID | v25.0 |
| Functional Framework | v24.0 |
