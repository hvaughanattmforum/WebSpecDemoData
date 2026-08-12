# Release note between TMFC007_v2.0.0_v2.1.0

**File:** `specifications/TMFC007-ServiceOrderManagement/TMFC007-ServiceOrderManagement.yaml`
**Base branch:** `v1.0.0` (component version `2.0.0`)  **Target branch:** `v1.1.0` (component version `2.1.0`)

### Component metadata

- Status changed from **specified** to **production**.
- Added eTOM mapping: Initiate Resource Order Capture (eTOM 1.5.5.6.1, v26.0).
- Added eTOM mapping: Manage Resource Order Capture (eTOM 1.5.5.6, v26.0).
- Added eTOM mapping: Initiate Resource Work Order (eTOM 1.5.5.7.1, v26.0).
- Added eTOM mapping: Manage Resource Work Order (eTOM 1.5.5.7, v26.0).
- Added eTOM mapping: Resource Order Management (eTOM 1.5.5, v26.0).
- Removed eTOM mapping: Issue Resource Order (eTOM 1.5.6.7, v21.5).
- Removed eTOM mapping: Resource Provisioning (eTOM 1.5.6, v21.5).
- Added FF mapping: Installed Resources Identification (Functional Framework 1141, v26.0).
- Added FF mapping: Service Order Needs Identification (Functional Framework 1217, v26.0).
- Added FF mapping: Service Order Request Consistency Check (Functional Framework 1219, v26.0).
- Added FF mapping: Internal Service Order Initialization (Functional Framework 1220, v26.0).
- Added FF mapping: Fallout Automated Correction (Functional Framework 16, v26.0).
- Added FF mapping: Fallout Correction Information Collection (Functional Framework 17, v26.0).
- Added FF mapping: Fallout Management to Fulfillment Application Accessing (Functional Framework 18, v26.0).
- Added FF mapping: Fallout Manual Correction Queuing (Functional Framework 19, v26.0).
- Added FF mapping: Fallout Notification (Functional Framework 20, v26.0).
- Added FF mapping: Fallout Orchestration (Functional Framework 21, v26.0).
- Added FF mapping: Fallout Reporting (Functional Framework 22, v26.0).
- Added FF mapping: Fallout Dashboard System Log-in Accessing (Functional Framework 23, v26.0).
- Added FF mapping: Pre-populated Fallout Information Presentation (Functional Framework 24, v26.0).
- Added FF mapping: Service Termination Points Determining (Functional Framework 632, v26.0).
- Added FF mapping: Fallout Rule Based Error Correction (Functional Framework 756, v26.0).

### Dependent APIs

- **TMF632**: added support for API v5.
- **TMF634**: added support for API v5.
- **TMF638**: added support for API v5.
- **TMF645**: added support for API v5.
- **TMF669**: added support for API v5.

### Subscribed events

- Removed subscribed event **ResourceOrderManagement**.
- Added subscribed event **CommunicationManagementAPI**.
- Added subscribed event **ResourceOrderingManagement**.
