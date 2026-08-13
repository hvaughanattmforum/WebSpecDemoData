# TMFC038 eTOM–SID Links

Source: transcribed from the original PDF's "2.3. eTOM L2 - SID ABEs links" diagram (page 4 of 12),
recovered from git history (this component's original `TMFC038_Resource_Performance_Management.pdf` had
already been overwritten by this skill's own generated output before this file existed — the true
original was retrieved via `git show HEAD:...` on the branch's starting commit). Verified by tracing every
line and arrowhead at up to 1200 dpi, cropped tightly around each connector.

All ten eTOM–SID links in the diagram are bidirectional. There is also one direct SID-to-SID link (see the
second table below) with no eTOM side at all — a schema deviation from the standard table, same precedent
as TMFC039's SID-to-SID cycle.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Resource Performance Management / Report Resource Performance | Resource Performance ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5; 1.5.9.4\|Report_Resource_Performance\|v24.5 | Resource_Domain\|Resource_Performance_ABE\|v25.0 |
| Resource Performance Management / Create Resource Performance Degradation Report / Close Resource Performance Degradation Report | Resource Performance ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5; 1.5.9.5\|Create_Resource_Performance_Degradation_Report\|v24.5; 1.5.9.7\|Close_Resource_Performance_Degradation_Report\|v24.5 | Resource_Domain\|Resource_Performance_ABE\|v25.0 |
| Resource Performance Management / Monitor Resource Performance | Resource Performance ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5; 1.5.9.1\|Monitor_Resource_Performance\|v24.5 | Resource_Domain\|Resource_Performance_ABE\|v25.0 |
| Resource Performance Management | Resource Performance ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5 | Resource_Domain\|Resource_Performance_ABE\|v25.0 |
| Resource Readiness and Support / Enable Resource Performance Management | MeasurementCollectionJob BE | bidirectional | 1.5.4\|Resource_Readiness_and_Support\|v24.5; 1.5.4.2\|Enable_Resource_Performance_Management\|v24.5 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Collection_ABE\|MeasurementCollectionJob_BE\|v25.0 |
| Resource Readiness and Support / Enable Resource Performance Management | AdhocCollection BE | bidirectional | 1.5.4\|Resource_Readiness_and_Support\|v24.5; 1.5.4.2\|Enable_Resource_Performance_Management\|v24.5 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Collection_ABE\|AdhocCollection_BE\|v25.0 |
| Resource Readiness and Support / Enable Resource Performance Management | MeasurementProductionJob BE | bidirectional | 1.5.4\|Resource_Readiness_and_Support\|v24.5; 1.5.4.2\|Enable_Resource_Performance_Management\|v24.5 | Patterns_Domain\|Performance_ABE\|Performance_Monitoring_ABE\|Performance_Production_ABE\|MeasurementProductionJob_BE\|v25.0 |
| Resource Readiness and Support / Enable Resource Performance Management | Performance Threshold ABE | bidirectional | 1.5.4\|Resource_Readiness_and_Support\|v24.5; 1.5.4.2\|Enable_Resource_Performance_Management\|v24.5 | Patterns_Domain\|Performance_ABE\|Performance_Threshold_ABE\|v25.0 |
| Resource Performance Management | Alarm ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5 | Resource_Domain\|Resource_Trouble_ABE\|Alarm_ABE\|v25.0 |
| Resource Performance Management / Monitor Resource Performance | Performance Threshold ABE | bidirectional | 1.5.9\|Resource_Performance_Management\|v24.5; 1.5.9.1\|Monitor_Resource_Performance\|v24.5 | Patterns_Domain\|Performance_ABE\|Performance_Threshold_ABE\|v25.0 |

**Additional SID-to-SID link (no eTOM side)** — one connector in the diagram runs directly between two SID
entities, not between an eTOM activity and a SID ABE:

| Source SID ABE | Target SID ABE | Direction | YAML source | YAML target |
|---|---|---|---|---|
| Performance Threshold ABE | Alarm ABE | Performance Threshold ABE produces Alarm ABE | Patterns_Domain\|Performance_ABE\|Performance_Threshold_ABE\|v25.0 | Resource_Domain\|Resource_Trouble_ABE\|Alarm_ABE\|v25.0 |

Naming note: the diagram's cylinder labels (`ResourcePerformance`, `AdhocCollection`, etc.) are concatenated
camelCase while the current YAML's cleaned SID names are space-separated (`Resource Performance`,
`Adhoc Collection`) — a labeling-convention difference between the hand-drawn diagram and the current YAML
parsing rule, not a data mismatch; the `YAML SID` column above still resolves correctly by underlying token
match.
