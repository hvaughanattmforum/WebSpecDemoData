# TMForum ODA Component Factory
## ODA Teams
- Components
- Technical Architecture
- Canvas 
- Conformance

## Repositories
- Component Specs: [https://github.com/tmforum-rand/TMForum-ODA-Component-Specification](https://github.com/tmforum-rand/TMForum-ODA-Component-Specification)
- Canvas Spec: [https://github.com/tmforum-rand/TMForum-ODA-Canvas-Specification](https://github.com/tmforum-rand/TMForum-ODA-Canvas-Specification)
- Conformance: [https://github.com/tmforum-rand/TMForum-ODA-Component-Conformance](https://github.com/tmforum-rand/TMForum-ODA-Component-Conformance)
- Releases: [https://github.com/tmforum-rand/TMForum-ODA-Ready-for-publication](https://github.com/tmforum-rand/TMForum-ODA-Ready-for-publication)


## Introduction
The component factory is the name given to the processes that implement the CI/CD development lifecycle of component assets. 

The releasable assets are:
- Golden component definitions, 
- CTK's (Conformance Tests)
- Deployable reference implementation. (Component envelopes)

There are three main phases each one is responsible in producing a complete asset which will be used an input for the next phase. Each phase will publish progress status reports that will inform the status of each component. 

Workflow steps are described in more detail in the workflow definition below. 

## Dependencies
There are two file dependencies in order to publish a **golden component**.
- **Component spec:** This file contains the metadata and core functions of a component. This is maintained by the components team.
- **supporting functions:** This file contains the security and management functions which are shared across all components 

Golden components are used to auto generate **component CTK's** and **reference implementations**.

## Usage
To build a component users only need to interact with two repositories which are managed by different teams. Contributions are made by opening pull requests which will be validated by their respective teams before merging. 

First the **component spec** has to be produced and can be contributed to the **canvas spec** repository via pull requests. 
Contributions to the **Supporting functions** must be done in the file `supportingFunctions.yaml` under `src/supporting-functions`

Apart from the pull requests to contribute to the component spec or supporting functions there are a set of validation jobs which will validate the spec before merging into the correct branch which will depend on the version of the asset.

The versioning approach is a combination between semantic versioning and grouping based on api stability.

For example each version v1, v2, may have different branches depending on stability. 
This will be refered too as v1alphaX, v1BetaX etc.

Contributions for each of the versions available will be done in the branches named with the same versions as the asset.
For example a **v1beta1** asset will go to the branch **v1beta2** in the **components spec** repository


## Workflow Definition
### Step 1 
This step is responsible of producing a **component spec**. This is a two step process. First a pull requests must be reaised which triggers a validation job. Once the validation has succeeded and the spec has been approved it will be merged. Second process is triggered by merging a validated spec to a branch in the **component spec** repository. This will trigger the following jobs:
1. **Spec build:** This merges the spec and supporting functions to create a golden component which will be used for generation of **conformance** assets.
2. **Report:** This job is responsible for reporting the result of the merging. The job will create a hierarchy of issues in Jira to track each of the components to be published and its assets.   

[<img src="ComponentFactoryS1.drawio.png">](https://link-to-your-URL/)

### Step 2
In this step component assets are generated and tested. Once a spec has been approved the following assets will generated:
- **Golden component**: This is the complete build of the component with the core and supporting functions.
- **CTK**: Conformance testing software to validate implementations of a component spec.
- **RI**: This is an example implementation of the spec which has been validated by the previous ctk.
The output gathered through this pipeline will be used to automatically update Jira for development reporting.

[<img src="ComponentFactoryS2.drawio.png">](https://link-to-your-URL/)


## Contact
For any issues with the pipeline contanct this email for support: vmarirodriguez@tmforum.org