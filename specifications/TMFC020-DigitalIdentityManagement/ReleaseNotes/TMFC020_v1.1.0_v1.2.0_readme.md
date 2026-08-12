# Release note between TMFC020_v1.1.0_v1.2.0

**File:** `specifications/TMFC020-DigitalIdentityManagement/TMFC020-DigitalIdentityManagement.yaml`
**Base branch:** `v1.0.0` (component version `1.1.0`)  **Target branch:** `v1.1.0` (component version `1.2.0`)

### Component metadata

- Status changed from **specified** to **roadmap**.
- Publication date changed from **2023-08-18** to **2026-06-08**.
- Added FF mapping: Application Access (Functional Framework 1025, v23.5).
- Added FF mapping: Identity Verification (Functional Framework 1240, v23.5).
- Added FF mapping: Credentials Establishment (Functional Framework 1247, v23.5).
- Added FF mapping: Credentials Query (Functional Framework 1248, v23.5).
- Added FF mapping: Single Sign-On Access Control (Functional Framework 899, v23.5).
- Added FF mapping: PKI and Digital Certificates Systems Integration (Functional Framework 906, v23.5).

### Dependent APIs

- **TMF632**: added support for API v5.
- **TMF632** v4 `individual`: added GET /id.
- **TMF632** v4 `individual`: removed GET/id.
- **TMF632** v4 `organization`: added GET /id.
- **TMF632** v4 `organization`: removed GET/id.
- **TMF669**: added support for API v5.

### Exposed APIs

- **TMF701** v4 `processFlow`: added DELETE /id, GET /id.
- **TMF701** v4 `processFlow`: removed DELETE/id, GET/id.
- **TMF701** v4 `taskFlow`: added GET /id, PATCH /id.
- **TMF701** v4 `taskFlow`: removed GET/id, PATCH/id.
- **TMF720** v4 `digitalIdentity`: added DELETE /id, GET /id, PATCH /id.
- **TMF720** v4 `digitalIdentity`: removed DELETE/id, GET/id, PATCH/id.
- **TMF720** v4 `roles`: added DELETE /id, GET /id, PATCH /id.
- **TMF720** v4 `roles`: removed DELETE/id, GET/id, PATCH/id.

### Subscribed events

- Subscribed event **PartyRoleManagement**: added `partyRoleAttributeValueChangeEvent` event.
- Subscribed event **PartyRoleManagement**: added `partyRoleCreateEvent` event.
- Subscribed event **PartyRoleManagement**: removed `UserRoleChangeNotification` event.
- Subscribed event **PartyRoleManagement**: removed `UserRoleCreationNotification` event.
