### 5.2. Jira References

**SID**
- ISA-894 - Formalize association between ProductUsage and AppliedCustomerBillingProductUsageRate (Done):
  in SID, rated ProductUsage represents AppliedCustomerBillingProductUsageRate. See ticket for more
  details.

**eTOM**
n/a

**Functional Framework**
- ISA-1032 - Clarification of Bill-time fee and what types it refers to in function 58 (BACKLOG):
  clarification of Function 58 to understand the types of fees that are underpinned by this function -
  bill-time fee.
- ISA-1033 - FF 73 - what type of reporting does this function cover? (BACKLOG): clarification of
  Function 73 to understand what type of reporting is meant by the function to determine the component
  to map to.
- ISA-996 - Master Data Management has repurposed catalog related functions (BACKLOG): Function 6
  re-purposed by Data Repository Management.

**OpenAPI**
- AP-4740 - Formalize association between ProductUsage and AppliedCustomerBillingProductUsageRate (OPEN)
- AP-5471 - TMF767 - updates for consistency with other 2 Usage APIs: 767 Product Usage (DONE): the
  future of Usage Management APIs moving to Product, Service & Resource from version 5.
- AP-6883 - TMF678 - add POST, PATCH, DELETE operations on appliedCustomerBillingRate (BACKLOG):
  currently only GET operations are available for Applied Customer Billing Rate; this is a request to
  add POST and PATCH.

**ODA Component**
n/a

### 5.3. Further resources

1. IG1228: please refer to IG1228 for defined use cases with ODA components interactions.

## 6. Administrative Appendix

### 6.1. Document History

#### 6.1.1. Version History

| Version Number | Date | Modified by | Description of changes |
|---|---|---|---|
| 1.0.0 | 27-Sep-2023 | Gaetano Biancardi | First version of document |
| 1.0.0 | 19-Dec-2023 | Amaia White | Final administrative edits |
| 1.1.0 | 29-Jan-2024 | Elisabeth Andersson | Functional Framework added: 6 Unbilled Invoice Items Listing, 68 Charges to Billing Statement Identification, 69 Charge To Billing Account Identification, 70 Charge To Billing Account Distribution, 158 Commitment Tracking Result Determining, 159 Commitment Tracking Terms & Conditions Evaluation, 160 Commitment Tracking Data Collection, 256 Customer Bill Usage and Charges Viewing |
| 1.1.0 | 01-Mar-2024 | Amaia White | Final administrative edits prior to release |
| 2.0.0 | 29-May-2024 | Elisabeth Andersson, Gaetano Biancardi | Updated to the latest template; added TMF620 Product Catalog as dependent API; modified API optionality (Optional to Mandatory: TMF637, TMF669, 635; removed TMF672 and TMF688 as they will be part of Canvas Services; removed TMF669; removed the need to access billingFormat and billingPresentationMedia from TMF666; updated TMF666 billingAccount and billingCycleSpecification to only have GET and GET/id); updated to 23.5 version of frameworks; eTOM updates: removed 1.3.9.3, added 1.6.15.3.1, added higher-level descriptions for already-included lower levels for 1.6.15; FF updates: changed aggregate action levels for 158, 159, 160, 258, added 60, 61, 89, 90, 183, 184 |
| 2.0.0 | 06-Sep-2024 | Amaia White | Final administrative edits prior to publication |
| 3.0.0 | 27-Oct-2025 | Elisabeth Andersson | Removed dependency on TMF666 for the Bill Cycle Specification and instead added TMF678 Bill Cycle operations, providing the instantiated Bill Cycle for a given period required by Bill Calculation; updated ISA-894 as resolved (in SID, rated ProductUsage represents AppliedCustomerBillingProductUsageRate); added Jira ticket dependency to TMF678 - add POST, PATCH, DELETE operations on appliedCustomerBillingRate (BACKLOG) |
| 3.0.0 | 19-Nov-2025 | Rosie Wilson | Updated description; final administrative edits prior to publication |
| 3.1.0 | 25-May-2026 | Hugo Vaughan | Gen 5 API updates |
| 3.1.0 | 25-Jun-2026 | Sannah Sibaya | Final edits prior to publication |

#### 6.1.2. Release History

| Release Status | Date Modified | Modified by | Description of changes |
|---|---|---|---|
| Pre-production | 19-Dec-2023 | Amaia White | Initial release |
| Pre-production | 22-Jan-2024 | Adrienne Walcott | Updated to Member Evaluated status |
| Pre-production | 01-Mar-2024 | Amaia White | Release of v1.1.0 |
| Production | 26-Apr-2024 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 06-Sep-2024 | Amaia White | Release of v2.0.0 |
| Pre-production | 19-Nov-2025 | Rosie Wilson | Release of v3.0.0 |
| Production | 16-Jan-2026 | Adrienne Walcott | Updated to reflect TM Forum Approved status |
| Pre-production | 25-Jun-2026 | Sannah Sibaya | Release of v3.1.0 |

### 6.2. Acknowledgements

This document was prepared by the members of the TM Forum ODA Components & Canvas team.

| Team Member | Company | Role |
|---|---|---|
| Gaetano Biancardi | Accenture | Author |
| Sylvie Demarest | Orange | Reviewer |
| Elisabeth Andersson | MATRIXX | Key Contributor |
| Rosie Wilson | TM Forum | Editor |
| Julien Rouland | Orange | Key Contributor / Reviewer |
| Muhammad Salman Sami | Whalecloud | Reviewer |
| Milind Bhagwat | BT | Reviewer |
| Abinash Vishwakarma | Netcracker | Reviewer |
| Luca Icardi | Accenture | Reviewer |
| Kamal Maghsoudlou | Ericsson | Reviewer |

