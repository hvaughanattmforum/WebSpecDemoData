# TMFC055 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram. The diagram image is
embedded on the page *following* the section heading (page 9 of 19 — the heading sits at the bottom of page
8, and the diagram picture itself is on page 9, above that page's own "2.4. Functional Framework Functions"
heading), the same page-boundary issue found and corrected on TMFC031/043/054 in this same sweep.

**This supersedes a prior "confirmed empty" version of this file**, which was itself already known to be a
correction of an earlier *fabricated* link (per that version's own text). The actual diagram is real and
non-trivial — 4 eTOM activity boxes, 2 SID entities, 6 links.

**2026-07-21 correction**: this file's table had degraded to only 4 rows, one with blank eTOM
activity/SID ABE cells, even though these notes already claimed "6 links" — rows 5 and 6 (both touching
"Manage Service Test") had been lost. The component-root `TMFC055_Service_Test_Management.pdf` has since
been overwritten by this skill's own regenerated PDF, so re-verification used the archived original,
`TMFC055 Service Test Management v1.1.0.pdf` in the OneDrive `20260716 Completed Component Docs` folder.
Rows 1, 2, and 4 (below) were unchanged by this pass; row 3's blank cells were filled in and rows 5–6 were
restored, all per a fresh trace of that archived diagram.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| L2 - Service Strategy Management / L3 - Service Test Strategy | ServiceTestSpec BE | bidirectional | 1.4.1\|Service_Strategy_Management\|v24.5; 1.4.1.8\|Service_Test_Strategy\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTestSpec_BE\|v25.0 |
| L2 - Service Specification Lifecycle Management / L3 - Service Specification Test Development & Retirement | ServiceTestSpec BE | bidirectional | 1.4.3.8\|Service_Specification_Test_Development_&_Retirement\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTestSpec_BE\|v25.0 |
| L2 - Service Strategy Management / L3 - Analyse Service Test Quality | ServiceTest BE | activity consumes | 1.4.1\|Service_Strategy_Management\|v24.5; 1.4.1.9\|Analyze_Service_Test_Quality\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTest_BE\|v25.0 |
| L2 - Service Strategy Management / L3 - Analyse Service Test Quality | ServiceTestSpec BE | activity consumes | 1.4.1\|Service_Strategy_Management\|v24.5; 1.4.1.9\|Analyze_Service_Test_Quality\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTestSpec_BE\|v25.0 |
| Manage Service Test | ServiceTestSpec BE | activity consumes | 1.4.4.6\|Manage_Service_Test\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTestSpec_BE\|v25.0 |
| Manage Service Test | ServiceTest BE | bidirectional | 1.4.4.6\|Manage_Service_Test\|v24.5 | Service_Domain\|Service_Test_ABE\|ServiceTest_BE\|v25.0 |
