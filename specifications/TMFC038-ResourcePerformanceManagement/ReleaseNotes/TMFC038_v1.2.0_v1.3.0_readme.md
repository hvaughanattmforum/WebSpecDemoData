# Release note between TMFC038_v1.2.0_v1.3.0

**File:** `specifications/TMFC038-ResourcePerformanceManagement/TMFC038-ResourcePerformanceManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.2.0`)  **Target branch:** `v1.1.0` (component version `1.3.0`)

### Component metadata

- Status changed from **specified** to **roadmap**.
- Publication date changed from **2024-12-17** to **2026-05-21**.
- Functional block changed from **IntelligenceManagement** to **Production**.
- Added eTOM mapping: Enable Resource Performance Management (eTOM 1.5.4.2, v24.5).
- Added eTOM mapping: Resource Readiness and Support (eTOM 1.5.4, v24.5).
- Added eTOM mapping: Monitor Resource Performance (eTOM 1.5.9.1, v24.5).
- Added eTOM mapping: Analyze Resource Performance (eTOM 1.5.9.2, v24.5).
- Added eTOM mapping: Report Resource Performance (eTOM 1.5.9.4, v24.5).
- Added eTOM mapping: Create Resource Performance Degradation Report (eTOM 1.5.9.5, v24.5).
- Added eTOM mapping: Close Resource Performance Degradation Report (eTOM 1.5.9.7, v24.5).
- Added eTOM mapping: Resource Performance Management (eTOM 1.5.9, v24.5).
- Added FF mapping: Resource Performance Event Filtering (Functional Framework 1066, v24.5).
- Added FF mapping: Resource Performance Data Analyzing (Functional Framework 498, v24.5).
- Added FF mapping: Resource Performance Data Aggregation and Trend Analyzing (Functional Framework 499, v24.5).
- Added FF mapping: Resource Performance Event Correlation (Functional Framework 501, v24.5).
- Added FF mapping: Resource Performance Data Accumulation (Functional Framework 502, v24.5).
- Added FF mapping: Anomaly Monitoring (Functional Framework 903, v24.5).
- Added SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Collection ABE > AdhocCollection BE (v25.0).
- Added SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Collection ABE > MeasurementCollectionJob BE (v25.0).
- Added SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Production ABE > MeasurementProductionJob BE (v25.0).
- Added SID mapping: Patterns Domain > Performance ABE > Performance Threshold ABE (v25.0).
- Removed SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Collection ABE > AdhocCollection BE (v25.0).
- Removed SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Collection ABE > MeasurementCollectionJob BE (v25.0).
- Removed SID mapping: Patterns Domain > Performance ABE > Performance Monitoring ABE > Performance Production ABE > MeasurementProductionJob BE (v25.0).
- Removed SID mapping: Patterns Domain > Performance ABE > Performance Threshold ABE (v25.0).

### Dependent APIs

- **TMF673** v4 `geographicAddress`: added GET /id.
- **TMF673** v4 `geographicAddress`: removed GET/id.
- **TMF674** v4 `geographicSite`: added GET /id.
- **TMF674** v4 `geographicSite`: removed GET/id.
- **TMF675** v4 `geographicLocation`: added GET /id.
- **TMF675** v4 `geographicLocation`: removed GET/id.

### Exposed APIs

- **TMF642**: added support for API v5.

### Subscribed events

- Removed subscribed event **GeographicAddressManagement**.
- Added subscribed event **API Place - GeographicAddress**.
