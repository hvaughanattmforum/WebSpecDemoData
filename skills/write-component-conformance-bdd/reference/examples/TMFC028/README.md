# TMFC028 - Party

## Purpose

This example demonstrates dependency validation where the dependent API itself requires another resource to be created first.

This is a multi-stage dependency setup pattern.

## Component

TMFC028 - Party

## Mandatory Exposed APIs

| API ID | Resource | Operation |
|----------|----------|----------|
| TMF632 | organization | createOrganization |

## Mandatory Dependent APIs

| API ID | Resource |
|----------|----------|
| TMF669 | partyRole |

## Generated Payloads

### Dependency Setup Payloads

| File | Purpose |
|----------|----------|
| supplier-party-0001.json | Create engaged party |
| supplier-party-role-0001.json | Create partyRole referencing engaged party |

### Target Payloads

| File | Purpose |
|----------|----------|
| party-target-0001.json | Valid partyRole reference |
| party-target-0002.json | Invalid partyRole reference |

## Resource Mapping

### TMF669 Party Role

Resource:

partyRole

Field Path:

relatedParty[0]

## Dependency Setup Flow

Step 1

Create Party

supplier-party-0001.json

↓

returns

party.id
party.href

Step 2

Create Party Role

supplier-party-role-0001.json

↓

inject

VALID_PARTY_ID
VALID_PARTY_HREF

↓

returns

partyRole.id
partyRole.href

Step 3

Create Organization

party-target-0001.json

↓

inject

VALID_ID
VALID_HREF

## Generated Scenarios

### Scenario 1

Valid PartyRole reference

Expected Result:

success

### Scenario 2

Invalid PartyRole reference

Expected Result:

failure

## Operation Mapping

TMF632 organization

→ createOrganization

## Pattern Demonstrated

Multi-stage dependency initialization.

This example should be used whenever a dependent API resource requires another resource to be created before the dependency itself can be initialized.