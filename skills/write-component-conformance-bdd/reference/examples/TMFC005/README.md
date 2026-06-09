# TMFC005 - Product Inventory

## Purpose

This example demonstrates dependency validation for a component with:

- One mandatory exposed API
- One mandatory dependent API
- One success scenario
- One failure scenario

## Component

TMFC005 - Product Inventory

## Mandatory Exposed APIs

| API ID | Resource | Operation |
|----------|----------|----------|
| TMF637 | product | createProduct |

## Mandatory Dependent APIs

| API ID | Resource |
|----------|----------|
| TMF620 | productSpecification |

## Generated Payloads

### Base Payloads

| File |
|----------|
| product-catalog-0001.json |

### Target Payloads

| File | Purpose |
|----------|----------|
| product-target-0001.json | Valid ProductSpecification reference |
| product-target-0002.json | Invalid ProductSpecification reference |

## Resource Mapping

| Dependent API | Resource | Field Path |
|----------|----------|----------|
| TMF620 | productSpecification | productSpecification |

## Generated Scenarios

### Scenario 1

Valid ProductSpecification reference

Expected Result:

success

### Scenario 2

Invalid ProductSpecification reference

Expected Result:

failure

## Operation Mapping

TMF637 product

→ createProduct

## Pattern Demonstrated

Single mandatory dependent API validation.