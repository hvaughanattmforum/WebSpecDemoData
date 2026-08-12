# Release note between TMFC037_v1.2.0_v1.3.0

**File:** `specifications/TMFC037-ServicePerformanceManagement/TMFC037-ServicePerformanceManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.2.0`)  **Target branch:** `v1.1.0` (component version `1.3.0`)

### Component metadata

- Status changed from **specified** to **roadmap**.
- Publication date changed from **2024-12-17** to **2026-05-21**.
- Functional block changed from **IntelligenceManagement** to **Production**.
- Added eTOM mapping: Manage Service Performance Control (eTOM 1.4.7.10, v25.0).
- Added eTOM mapping: Manage Service Performance Reporting (eTOM 1.4.7.11, v25.0).
- Added eTOM mapping: Manage Service Performance Requirement (eTOM 1.4.7.6, v25.0).
- Added eTOM mapping: Manage Service Performance Plan (eTOM 1.4.7.7, v25.0).
- Added eTOM mapping: Manage Service Performance Measure (eTOM 1.4.7.8, v25.0).
- Added eTOM mapping: Manage Service Performance Analysis (eTOM 1.4.7.9, v25.0).
- Added eTOM mapping: Service Performance Management (eTOM 1.4.7, v25.0).
- Added FF mapping: Service Performance Data Collection (Functional Framework 603, v25.0).
- Added FF mapping: Service Performance Event Correlation (Functional Framework 604, v25.0).
- Added FF mapping: Service Performance Monitoring (Functional Framework 605, v25.0).
- Added FF mapping: Service Performance Reporting (Functional Framework 606, v25.0).
- Added SID mapping: Service Domain > Service Performance ABE (v25.0).
- Removed SID mapping: Service Domain > Service Performance ABE  ( v25.0).

### Dependent APIs

- Added new dependent API **TMF642** (v4).
- **TMF628**: added support for API v5.
- **TMF628**: dropped support for API v4.
- **TMF638**: added support for API v5.
- **TMF657** v4 `serviceLevelObjective`: added GET /id.
- **TMF657** v4 `serviceLevelObjective`: removed GET/id.
- **TMF657** v4 `serviceLevelSpecification`: added GET /id.
- **TMF657** v4 `serviceLevelSpecification`: removed GET/id.
- **TMF673** v4 `geographicAddress`: added GET /id.
- **TMF673** v4 `geographicAddress`: removed GET/id.
- **TMF674** v4 `geographicSite`: added GET /id.
- **TMF674** v4 `geographicSite`: removed GET/id.

### Exposed APIs

- **TMF628**: added support for API v5.
- **TMF628**: dropped support for API v4.
- **TMF642**: added support for API v5.

### Published events

- Added published event **PerformanceThresholdManagement**.
- Published event **PerformanceManagement**: removed `thresholdChangeNotification` event.
- Published event **PerformanceManagement**: removed `thresholdCreateNotification` event.
- Published event **PerformanceManagement**: removed `thresholdJobChangedNotification` event.
- Published event **PerformanceManagement**: removed `thresholdJobCreateNotification` event.
- Published event **PerformanceManagement**: removed `thresholdJobResumeNotification` event.
- Published event **PerformanceManagement**: removed `thresholdJobSuspendNotification` event.
- Published event **PerformanceManagement**: removed `thresholdRuleChangedNotification` event.
- Published event **PerformanceManagement**: removed `thresholdRuleCreateNotification` event.
