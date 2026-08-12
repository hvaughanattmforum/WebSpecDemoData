# Release note between TMFC028_v2.1.0_v2.2.0

**File:** `specifications/TMFC028-PartyManagement/TMFC028-PartyManagement.yaml`
**Base branch:** `v1.0.0` (component version `2.1.0`)  **Target branch:** `v1.1.0` (component version `2.2.0`)

### Component metadata

- Status changed from **specified** to **preview**.
- Publication date changed from **2024-10-14** to **2026-05-21**.
- Added eTOM mapping: Collect Party data (eTOM 1.6.3.1.5, v26.0).
- Added eTOM mapping: Party Relationship Management (eTOM 1.6.3.1, v26.0).
- Removed eTOM mapping: Collect Party data (eTOM 1.6.3.1.5, v23.0).
- Removed eTOM mapping: Party Relationship Management (eTOM 1.6.3.1, v23.0).

### Dependent APIs

- Removed dependent API **TMF688**.
- **TMF669**: added support for API v5.

### Exposed APIs

- **TMF632**: added support for API v5.
- **TMF632** v4 `individual`: added DELETE /id, GET /id, PATCH /id.
- **TMF632** v4 `individual`: removed DELETE/id, GET/id, PATCH/id.
- **TMF632** v4 `organization`: added DELETE /id, GET /id, PATCH /id.
- **TMF632** v4 `organization`: removed DELETE/id, GET/id, PATCH/id.
- **TMF701** v4 `processFlow`: added DELETE /id, GET /id.
- **TMF701** v4 `processFlow`: removed DELETE/id, GET/id.
- **TMF701** v4 `taskFlow`: added GET /id, PATCH /id.
- **TMF701** v4 `taskFlow`: removed GET/id, PATCH/id.
