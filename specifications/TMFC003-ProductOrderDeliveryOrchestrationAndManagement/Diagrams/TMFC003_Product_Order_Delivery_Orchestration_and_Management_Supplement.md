### 5.2. Jira References

**eTOM**
- ISA-389 - Improve Manage Order Fallout (1.3.3.8) description and decomposition (DONE): 1.3.3.8 - Manage
  Order Fallout, as this L3 is shared by POCV and POOM components (to be consistent with Functional
  Framework mapping), clarify which type of fallout needs to be managed during the order delivery
  orchestration (at POOM level) and which needs to be managed at Product Order Capture and Follow-Up
  level (by POCV)

**SID**
- ISA-399 - New BEs to describe Orchestration Plan and Delivery Process (BACKLOG): describe Orchestration
  Plan and delivery process at Product Order level. This could be added at least as a specialization from
  Project ABE.

**Functional Framework**
Already integrated in Functional Framework R22.0:
- Function 174 - Customer Order Error Resolution Support: review the definition of this function, may
  split it in 2 as it is proposed to be mapped to POCV and to POOM
- Function 723 - Customer Order Item Decomposition: the term "decomposition" in the function name or
  definition doesn't seem appropriate, since by definition a product order is built up of order items
  according to the catalog structure of product offerings and products

Need to be studied for R22.0 or R22.5:
- ISA-397 - Split Function 342 - Mass Service/product pre-activation (SME REVIEW): need to split this
  function in 2, one at product level, the other at service level
- ISA-398 - Review Function 743 - Number Portability Orchestration (DONE): review functions related to
  Number Portability and clarify which level (product/service/resource) each concerns, split if necessary

**API**
- AP-3664 - Manage Amend Order (DONE): does POOM need to issue TMF641 PATCH /serviceOrder and TMF652 PATCH
  /resourceOrder? No scenario identified where POOM would need to PATCH a service or resource order; order
  updates due to a change in intent should go through amendments, preferably using a task-based mechanism
  similar to cancellation requests (e.g. an amendment of a product order would result in a new
  orchestration plan, with changes trickling down to POOM, SOM and ROM as amendment and/or cancellation
  requests). Amend task operations are needed for all P/S/R order APIs.

### 5.3. Further resources

This component is involved in use cases described in IG1228 How to use ODA - Using Open APIs to realize
Use Cases.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 29-Mar-2022 | Gaetano Biancardi, Anastasios Sarantis, Sylvie Demarest, Dimitrios Lagkouvardos | Final edits prior to publication |
| 1.0.1 | 25-Jul-2023 | Ian Turkington | No content changed, simply a layout change to match template 3. |
| 1.0.1 | 15-Aug-2023 | Amaia White | Final edits prior to publication |
| 1.1.1 | 25-Jun-2024 | Sylvie Demarest | Aligned to Frameworks 23.5; aligned to latest template |
| 2.0.0 | 21-Oct-2024 | Gaetano Biancardi | Dependent API: corrected typo and set the following APIs mandatory: TMF620, TMF737 |
| 2.0.0 | 13-Mar-2025 | Rosie Wilson | Final administrative updates |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 29-Mar-2022 | Goutham Babu | Initial release |
| Production | 20-May-2022 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 15-Aug-2023 | Amaia White | New version 1.0.1 |
| Production | 06-Oct-2023 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 12-Jul-2024 | Amaia White | New version 1.1.1 |
| Production | 30-Aug-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 13-Mar-2025 | Rosie Wilson | New version 2.0.0 |
| Production | 09-May-2025 | Adrienne Walcott | Updated to reflect TM Forum Approved status |

### 6.2. Acknowledgements

| Team Member | Company | Role |
|---|---|---|
| Anastasios Sarantis | Vodafone | Editor |
| Ian Turkington | TM Forum | Additional Input |
| Hugo Vaughan (TM Forum) | TM Forum | Additional Input |
| Gaetano Biancardi | Accenture | Reviewer |
| Sylvie Demarest | Orange | Editor |
| Dimitrios Lagkouvardos | Oracle | Reviewer |

