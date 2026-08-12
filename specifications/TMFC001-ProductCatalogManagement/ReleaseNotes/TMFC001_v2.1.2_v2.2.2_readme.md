# Release note between TMFC001_v2.1.2_v2.2.2

**File:** `specifications/TMFC001-ProductCatalogManagement/TMFC001-ProductCatalogManagement.yaml`
**Base branch:** `v1.0.0` (component version `2.1.2`)  **Target branch:** `v1.1.0` (component version `2.2.2`)

### Component metadata

- Status changed from **specified** to **production**.
- Publication date changed from **2025-11-12** to **2026-05-11**.
- Description text updated.
- Added FF mapping: External Product Specification Development (Functional Framework 1291, v24.0).
- Added FF mapping: External Product Offering Development (Functional Framework 1292, v24.0).
- Added FF mapping: Product Specification Recalls Support (Functional Framework 1293, v24.0).
- Added FF mapping: Product Specification Change Notification (Functional Framework 1341, v24.0).
- Added FF mapping: Product Specification Version Control (Functional Framework 1342, v24.0).
- Added FF mapping: Product Onboarding Support (Functional Framework 651, v24.0).
- Added SID mapping: Product Domain > Loyalty ABE > Loyalty Program Specification ABE (v25.0).
- Added SID mapping: Product Domain > Product Usage ABE > Product Usage Specification ABE (v25.0).
- Removed SID mapping: Product Domain > Loyalty ABE > Product Usage Spec ABE (v25.0).
- Removed SID mapping: Product Domain > Product Usage ABE > Loyalty Program Specification ABE (v25.0).

### Dependent APIs

- **TMF620**: added support for API v5.
- **TMF632**: added support for API v5.
- **TMF632** v4: added `organization` resource.
- **TMF632** v4: removed `organisation` resource.
- **TMF634**: added support for API v4.
- **TMF634**: added support for API v5.
- **TMF634**: dropped support for API v4.1.
- **TMF669**: added support for API v5.

### Exposed APIs

- **TMF620**: added support for API v5.

### Published events

- Published event **ProductCatalogManagement**: added `productSpecificationCreateEvent` event.

### Subscribed events

- Added subscribed event **ResourceCatalogManagement**.
- Subscribed event **ServiceCatalogManagement**: added `serviceSpecificationChangeEvent` event.
- Subscribed event **ServiceCatalogManagement**: removed `resourceSpecificationChangeEvent` event.
- Subscribed event **ServiceCatalogManagement**: removed `resourceSpecificationCreateEvent` event.
- Subscribed event **ServiceCatalogManagement**: removed `resourceSpecificationDeleteEvent` event.
- Subscribed event **ServiceCatalogManagement**: removed `serviceSpecificationAttributeValueChangeEvent` event.
- Subscribed event **ServiceCatalogManagement**: removed `serviceSpecificationStateChange` event.
