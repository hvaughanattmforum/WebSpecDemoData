# TMFC007 - Service Order

## Purpose

This example demonstrates dependency validation for a component with:

- One mandatory exposed API
- Multiple mandatory dependent APIs
- Multiple resource field paths
- Success and failure scenarios for each dependency

## Component

TMFC007 - Service Order

## Mandatory Exposed APIs

| API ID | Resource | Operation |
|----------|----------|----------|
| TMF641 | serviceOrder | createServiceOrder |

## Mandatory Dependent APIs

| API ID | Resource |
|----------|----------|
| TMF633 | serviceSpecification |
| TMF638 | service |

## Generated Payloads

### Base Payloads

| File |
|----------|
| service-catalog-0001.json |
| service-inventory-0001.json |

### Target Payloads

| File | Purpose |
|----------|----------|
| service-target-0001.json | Valid ServiceSpecification reference |
| service-target-0002.json | Invalid ServiceSpecification reference |
| service-target-0003.json | Valid Service reference |
| service-target-0004.json | Invalid Service reference |

## Resource Mapping

### TMF633 Service Catalog

Resource:

serviceSpecification

Field Path:

serviceOrderItem[0].service.serviceSpecification

### TMF638 Service Inventory

Resource:

service

Field Path:

serviceOrderItem[0].service

## Generated Scenarios

### Scenario 1

Valid ServiceSpecification reference

Expected Result:

success

### Scenario 2

Invalid ServiceSpecification reference

Expected Result:

failure

### Scenario 3

Valid Service reference

Expected Result:

success

### Scenario 4

Invalid Service reference

Expected Result:

failure

## Operation Mapping

TMF641 serviceOrder

→ createServiceOrder

## Pattern Demonstrated

Multiple mandatory dependent APIs within a single feature file.