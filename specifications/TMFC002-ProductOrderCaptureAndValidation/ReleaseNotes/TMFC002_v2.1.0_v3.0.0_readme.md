# Release note between TMFC002_v2.1.0_v3.0.0

**File:** `specifications/TMFC002-ProductOrderCaptureAndValidation/TMFC002-ProductOrderCaptureAndValidation.yaml`
**Base branch:** `v1.0.0` (component version `2.1.0`)  **Target branch:** `v1.1.0` (component version `3.0.0`)

### Component metadata

- Status changed from **specified** to **preview**.
- Publication date changed from **2024-11-12** to **2026-05-21**.
- Description text updated.

### Dependent APIs

- **TMF620**: added support for API v5.
- **TMF632**: added support for API v5.
- **TMF637**: added support for API v5.
- **TMF638**: added support for API v5.
- **TMF638** v4 `service`: added GET /id.
- **TMF638** v4 `service`: removed GET / id.
- **TMF639** v4 `resource`: added GET /id.
- **TMF639** v4 `resource`: removed GET / id.
- **TMF666**: added support for API v5.
- **TMF669**: added support for API v5.
- **TMF676** v4 `payment`: added GET /id.
- **TMF676** v4 `payment`: removed GET / id.
- **TMF683**: added support for API v5.
- **TMF683** v4 `partyInteraction`: added GET /id.
- **TMF683** v4 `partyInteraction`: removed GET / id.
- **TMF687** v4 `checkProductStock`: removed PATCH.
- **TMF687** v4 `queryProductStock`: removed PATCH.
- **TMF687** v4 `reserveProductStock`: removed PATCH.

### Exposed APIs

- **TMF663**: added support for API v5.
- **TMF663**: requirement changed from **false** to **true**.

### Published events

- Removed published event **ProcessFlowManagement**.
- Removed published event **Quote**.
- Removed published event **ShoppingCart**.
- Added published event **TMF648**.
- Added published event **TMF663**.
- Added published event **TMF701**.

### Subscribed events

- Removed subscribed event **GeographicAddressManagement**.
- Removed subscribed event **PaymentManagement**.
- Removed subscribed event **ProductOfferingQualification**.
- Removed subscribed event **ResourceReservation**.
- Added subscribed event **TMF673**.
- Added subscribed event **TMF676**.
- Added subscribed event **TMF679**.
- Added subscribed event **TMF716**.
