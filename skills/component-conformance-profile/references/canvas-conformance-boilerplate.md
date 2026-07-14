## Canvas Conformance

### Deployment Conformance
Canvas should be Kubernetes based and it is required to have the component deployment in a Kubernetes based environment. Cluster should be running on a supported Kubernetes version. Ensure that the Kubernetes manifests, deployment configurations, and custom resources are compatible with the targeted Kubernetes API version. Compatibility with 3 previous Kubernetes versions must also be considered for backward compatibility. Only trusted container images from reputable sources must be used.

The component deployment and the Kubernetes cluster must pass the following tests:

#### Step 0: Basic environment connectivity tests
- Kubectl configured correctly
- The configuration must be available and the context must be set to the correct cluster
- Kubectl should return pods in `<namespace of components>` namespace

#### Step 1: Deployment component tests
- Component must be found in the established namespace
- Component must have deployed successfully (status: Complete)
- All exposed APIs must be accessible and return HTTP 200
- All exposed APIs must provide valid URLs
- Security API must return at least one party role with canvas system role defined, unless only `canvasSystemRole` is used
- CTKs for all exposed APIs must execute successfully without errors


### Configuration Conformance

- Helm chart MUST be used for deployment
- Configuration file MUST be in YAML
- Namespace MUST exist for Canvas and Components
- CRDs MUST exist for Components and API definitions
- Canvas operator and versioning webhook MUST be running

#### Step 0: Component file checks
- Helm manifest file must exist at the configured path
- File must contain valid YAML

#### Step 1: Component manifest checks
- Must contain a document of kind `Component`
- API version must be supported (`oda.tmforum.org/v1`)
- Must include `metadata` with name and labels
- Must include `spec`
- `coreFunction` must include exposed and dependent APIs
- Must include a `security` function
- Must include either `canvasSystemRole` or a partyRole API
- All resources must be labelled with the component name
- Component ID must match the standard specification
- All mandatory exposed and dependent APIs must match the standard specification versions
- All swagger URLs must be valid and accessible
