# Release note between TMFC062_v1.0.0_v1.1.0

**File:** `specifications/TMFC062-ResourceConfigurationandActivation/TMFC062-ResourceConfigurationandActivation.yaml`
**Base branch:** `v1.0.0` (component version `1.0.0`)  **Target branch:** `v1.1.0` (component version `1.1.0`)

### Component metadata

- Status changed from **specified** to **preview**.
- Publication date changed from **2024-11-18** to **2026-06-02**.
- Added eTOM mapping: Verify Resource Configuration (eTOM 1.5.8.2.1, v25.0).

### Dependent APIs

- **TMF634**: added support for API v5.
- **TMF634** v4 `resourceSpecification`: added GET /id.
- **TMF634** v4 `resourceSpecification`: removed GET/id.
- **TMF634**: requirement changed from **false** to **true**.
- **TMF639** v4 `resource`: added GET /id.
- **TMF639** v4 `resource`: removed GET/id.
- **TMF639**: requirement changed from **false** to **true**.

### Published events

- Removed published event **ResourceActivationManagement**.
- Removed published event **ResourceFunctionActivationManagement**.
- Added published event **API Resource Activation and Configuration**.
- Added published event **Resource Function Activation and Configuration**.
