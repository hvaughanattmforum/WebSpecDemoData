# TMFC037 eTOM–SID Links

Source: transcribed from the original PDF's "2.3. eTOM L2 - SID ABEs links" diagram (page 8 of 19).

**Refreshed 2026-07-22**: `componentMetadata.eTOMs` was empty (`[]`) in the YAML when this file was first
written, even though the PDF's own section 2.1 listed real eTOM business activities and this diagram draws
six eTOM activity boxes — the note used to say every "YAML eTOM" cell below was `**NO MATCH**` for that
reason. The YAML has since been populated with all 7 eTOM entries (including the L2 parent), and every row
below now resolves cleanly.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Manage Service Performance Requirement | Service Performance ABE | bidirectional | 1.4.7.6\|Manage_Service_Performance_Requirement\|v25.0 | Service_Domain\|Service_Performance_ABE\|v25.0 |
| Manage Service Performance Reporting | Service Performance ABE | bidirectional | 1.4.7.11\|Manage_Service_Performance_Reporting\|v25.0 | Service_Domain\|Service_Performance_ABE\|v25.0 |
| Manage Service Performance Measure | MeasurementProductionJob BE | bidirectional | 1.4.7.8\|Manage_Service_Performance_Measure\|v25.0 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Production_ABE\|MeasurementProductionJob_BE\|v25.0 |
| Manage Service Performance Measure | Performance Threshold ABE | bidirectional | 1.4.7.8\|Manage_Service_Performance_Measure\|v25.0 | Patterns_Domain\|Performance_ABE\|Performance_Threshold_ABE\|v25.0 |
| Manage Service Performance Analysis | Service Performance ABE | bidirectional | 1.4.7.9\|Manage_Service_Performance_Analysis\|v25.0 | Service_Domain\|Service_Performance_ABE\|v25.0 |
| Manage Service Performance Control | Performance Threshold ABE | bidirectional | 1.4.7.10\|Manage_Service_Performance_Control\|v25.0 | Patterns_Domain\|Performance_ABE\|Performance_Threshold_ABE\|v25.0 |
| Manage Service Performance Control | Service Performance ABE | bidirectional | 1.4.7.10\|Manage_Service_Performance_Control\|v25.0 | Service_Domain\|Service_Performance_ABE\|v25.0 |
| Manage Service Performance Control | AdhocCollection BE | bidirectional | 1.4.7.10\|Manage_Service_Performance_Control\|v25.0 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Collection_ABE\|AdhocCollection_BE\|v25.0 |
| Manage Service Performance Control | MeasurementCollectionJob BE | bidirectional | 1.4.7.10\|Manage_Service_Performance_Control\|v25.0 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Collection_ABE\|MeasurementCollectionJob_BE\|v25.0 |
| Manage Service Performance Control | Alarm ABE | bidirectional | 1.4.7.10\|Manage_Service_Performance_Control\|v25.0 | Resource_Domain\|Resource_Trouble_ABE\|Alarm_ABE\|v25.0 |
