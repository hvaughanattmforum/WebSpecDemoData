# Release note between TMFC039_v1.1.0_v1.2.0

**File:** `specifications/TMFC039-AgreementManagement/TMFC039-AgreementManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.1.0`)  **Target branch:** `v1.1.0` (component version `1.2.0`)

### Component metadata

- Status changed from **specified** to **roadmap**.
- Publication date changed from **2024-08-19** to **2026-05-21**.

### Dependent APIs

- **TMF620**: added support for API v5.
- **TMF620** v4 `productOffering`: added GET /id.
- **TMF620** v4 `productOffering`: removed GET/id.
- **TMF620** v4 `productOfferingPrice`: added GET /id.
- **TMF620** v4 `productOfferingPrice`: removed GET/id.
- **TMF632**: added support for API v5.
- **TMF632** v4 `individual`: added GET /id.
- **TMF632** v4 `individual`: removed GET/id.
- **TMF632** v4 `organization`: added GET /id.
- **TMF632** v4 `organization`: removed GET/id.
- **TMF637**: added support for API v5.
- **TMF637** v4 `product`: added GET /id.
- **TMF637** v4 `product`: removed GET/id.
- **TMF667** v4 `document`: added GET /id.
- **TMF667** v4 `document`: removed GET/id.
- **TMF669**: added support for API v5.
- **TMF669** v4 `partyRole`: added GET /id.
- **TMF669** v4 `partyRole`: removed GET/id.

### Exposed APIs

- **TMF651** v4 `agreement`: added DELETE /id, GET /id, PATCH /id.
- **TMF651** v4 `agreement`: removed DELETE/id, GET/id, PATCH/id.
- **TMF651** v4 `agreementSpecification`: added DELETE /id, GET /id, PATCH /id.
- **TMF651** v4 `agreementSpecification`: removed DELETE/id, GET/id, PATCH/id.

### Published events

- Removed published event **userRole**.
- Added published event **AgreementManagement**.
