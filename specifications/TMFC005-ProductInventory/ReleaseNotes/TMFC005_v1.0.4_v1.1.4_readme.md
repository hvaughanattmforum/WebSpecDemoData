# Release note between TMFC005_v1.0.4_v1.1.4

**File:** `specifications/TMFC005-ProductInventory/TMFC005-ProductInventory.yaml`
**Base branch:** `v1.0.0` (component version `1.0.4`)  **Target branch:** `v1.1.0` (component version `1.1.4`)

### Component metadata

- Status changed from **specified** to **production**.
- Publication date changed from **2024-06-27** to **2026-05-21**.
- Added FF mapping: Product Configuration Check (Functional Framework 1201, v24.0).
- Added SID mapping: Product Domain > Product and Offering Instance ABE (v25.0).
- Removed SID mapping: Product Domain > ProductOfferingInstance ABE (v25.0).

### Dependent APIs

- **TMF620**: added support for API v5.
- **TMF622**: added support for API v5.
- **TMF632**: added support for API v5.
- **TMF637**: added support for API v5.
- **TMF638**: added support for API v5.
- **TMF666**: added support for API v5.
- **TMF669**: added support for API v5.

### Exposed APIs

- **TMF637**: added support for API v5.

### Published events

- Removed published event **Productinventory**.
- Added published event **Product Inventory**.

### Subscribed events

- Removed subscribed event **UserRolePermissionManagement**.
- Added subscribed event **User Roles And Permissions**.
