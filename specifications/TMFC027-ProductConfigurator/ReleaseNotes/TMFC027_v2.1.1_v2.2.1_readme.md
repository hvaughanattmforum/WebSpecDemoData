# Release note between TMFC027_v2.1.1_v2.2.1

**File:** `specifications/TMFC027-ProductConfigurator/TMFC027-ProductConfigurator.yaml`
**Base branch:** `v1.0.0` (component version `2.1.1`)  **Target branch:** `v1.1.0` (component version `2.2.1`)

### Component metadata

- Status changed from **specified** to **roadmap**.
- Publication date changed from **2023-11-27** to **2026-06-02**.
- Added eTOM mapping: Manage Product Configuration (eTOM 1.2.5.2, v25.0).
- Added eTOM mapping: Product Configuration Management (eTOM 1.2.5, v25.0).
- Removed eTOM mapping: 1.2.5|Product_Domain|Manage_Product_Configuration|v25.0.
- Removed eTOM mapping: 1.2.5|Product_Domain|Product_Configuration_Management|v25.0.

### Dependent APIs

- **TMF620**: added support for API v5.
- **TMF622**: added support for API v5.
- **TMF632**: added support for API v5.
- **TMF637**: added support for API v5.
- **TMF645**: added support for API v5.
- **TMF666**: added support for API v5.
- **TMF669**: added support for API v5.
- **TMF921**: added support for API v5.

### Exposed APIs

- **TMF679** v4 `productOfferingQualification`: added GET /id, PATCH /id.
- **TMF679** v4 `productOfferingQualification`: removed GET/id, PATCH/id.
- **TMF760** v5 `checkProductConfiguration`: removed GET/id.
- **TMF760** v5 `queryProductConfiguration`: removed GET/id.

### Published events

- Removed published event **ProductConfiguration**.
- Added published event **ProductOfferingQualification**.
