# Release note between TMFC035_v1.1.1_v1.2.1

**File:** `specifications/TMFC035-PermissionsManagement/TMFC035-PermissionsManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.1.1`)  **Target branch:** `v1.1.0` (component version `1.2.1`)

### Component metadata

- Status changed from **specified** to **preview**.
- Publication date changed from **2023-08-18** to **2026-05-21**.
- Added FF mapping: Application Access (Functional Framework 1025, v26.0).
- Added FF mapping: Party Role Assignment (Functional Framework 1181, v26.0).
- Added FF mapping: Permission Perimeter Configuration (Functional Framework 1182, v26.0).
- Added FF mapping: Anonymous User Account Creation (Functional Framework 260, v26.0).
- Added FF mapping: Building Access Control (Functional Framework 897, v26.0).
- Added FF mapping: Application Security Management (Functional Framework 898, v26.0).
- Added FF mapping: Single Sign-On Access Control (Functional Framework 899, v26.0).
- Added FF mapping: Authorization Control (Functional Framework 900, v26.0).
- Added FF mapping: PKI and Digital Certificates Systems Integration (Functional Framework 906, v26.0).

### Dependent APIs

- **TMF632**: added support for API v5.
- **TMF632** v4 `individual`: added GET /id.
- **TMF632** v4 `individual`: removed GET/id.
- **TMF632** v4 `organization`: added GET /id.
- **TMF632** v4 `organization`: removed GET/id.

### Exposed APIs

- **TMF669**: added support for API v5.
- **TMF669** v4 `partyRole`: added DELETE /id, GET /id, PATCH /id.
- **TMF669** v4 `partyRole`: removed DELETE/id, GET/id, PATCH/id.
- **TMF672** v4 `permission`: added DELETE /id, GET /id, PATCH /id.
- **TMF672** v4 `permission`: removed DELETE/id, GET/id, PATCH/id.
- **TMF672** v4 `userRole`: added DELETE /id, GET /id, PATCH /id.
- **TMF672** v4 `userRole`: removed DELETE/id, GET/id, PATCH/id.

### Published events

- Removed published event **userRole**.
- Added published event **User Roles And Permissions**.
