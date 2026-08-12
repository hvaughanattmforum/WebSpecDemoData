# Release note between TMFC043_v1.0.0_v1.1.0

**File:** `specifications/TMFC043-FaultManagement/TMFC043-FaultManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.0.0`)  **Target branch:** `v1.1.0` (component version `1.1.0`)

### Component metadata

- Status changed from **specified** to **production**.
- Publication date changed from **2025-03-11** to **2026-05-21**.
- Added eTOM mapping: Service Problem Management (eTOM 1.4.6, v25.0).
- Added eTOM mapping: Resource Trouble Management (eTOM 1.5.8, v25.0).
- Added FF mapping: Service Problem Manual Correction Support (Functional Framework 1067, v25.0).
- Added FF mapping: Resource Diagnostic and Test Analysis (Functional Framework 1155, v25.0).
- Added FF mapping: Resource Trouble Cause Identification (Functional Framework 1186, v25.0).
- Added FF mapping: Resource Trouble Resolution (Functional Framework 1187, v25.0).
- Added FF mapping: Service Problem Prioritization (Functional Framework 610, v25.0).
- Added FF mapping: Service Problem Automatic Correction (Functional Framework 612, v25.0).
- Added FF mapping: Service Problem Tracking & Management (Functional Framework 615, v25.0).
- Added FF mapping: Service Assurance Control Calculation (Functional Framework 979, v25.0).
- Added FF mapping: Service Assurance Trouble Mitigation (Functional Framework 980, v25.0).
- Added SID mapping: Resource Domain > Resource Trouble ABE > AlarmSeverityAssignmentProfile BE (v25.0).
- Added SID mapping: Service Domain > Service Problem ABE (v25.0).

### Exposed APIs

- **TMF642**: added support for API v5.
- **TMF656**: added support for API v5.

### Subscribed events

- Removed subscribed event **EntityCatalogueManagement**.
- Removed subscribed event **GeographicAddressManagement**.
- Added subscribed event **API Place - GeographicAddress**.
- Added subscribed event **EntityCatalogManagement**.
