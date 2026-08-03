# TMFC009 eTOM–SID Links

Source: transcribed from the original PDF's "2.3. eTOM L2 - SID ABEs links" diagram (page 7 of 15).

The diagram itself draws exactly one eTOM Business Activity box and one SID Data Entity cylinder. The
original PDF literally labels both "to be determined" rather than naming a real activity or ABE — a
placeholder, not a missing render. The single connecting line has an arrowhead at both ends (a small
open/hollow triangle into the eTOM box, a filled triangle into the SID cylinder), i.e. bidirectional.

**2026-07-23 update**: the YAML has since been given a real `SIDs` entry, and the eTOM entry's version
was corrected from `v23.0` to `v23.0.1`. The row below now names the resolved activity/ABE
(`Service Configuration and Activation` / `Service Configuration`) rather than the PDF's literal
placeholder text, since both a real eTOM and a real SID now exist for this component to point to.

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Service Configuration and Activation | Service Configuration | bidirectional | 1.4.5\|Service_Configuration_&_Activation\|v23.0.1 | Service_Domain\|Service_Configuration_ABE\|v23.5.0 |
