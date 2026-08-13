# TMFC000 eTOM–SID Links

Source: transcribed from the original PDF's "2.3 eTOM L2 - SID ABEs links" diagram (page <N> of <M>),
verified by tracing every line and arrowhead in the rendered page image at up to 600 dpi, cropped tightly
around each connector to confirm which cylinder/box every curve actually terminates at.

<Provenance / discrepancy notes, if any. Record here anything a later reader would otherwise have to
re-derive, e.g.: which commit the true original was recovered from if the component-root PDF had been
overwritten by generated output; how many links the diagram actually contains versus how many the existing
`TMFC000_eTOM_SID.svg` encodes; and whether that SVG therefore needs regenerating from this link set.>

| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |
|---|---|---|---|---|
| Business Activity Name With Underscores | ABE Name ABE | <bidirectional \| eTOM-to-SID \| SID-to-eTOM> | <1.2.7\|Business_Activity_Name_With_Underscores\|v24.0> | <Domain_Name\|ABE_Name_ABE\|v25.0> |
| Business Activity Name With Underscores | BE Name BE | <bidirectional> | <1.2.7\|Business_Activity_Name_With_Underscores\|v24.0> | <Domain_Name\|ABE_Name_ABE\|BE_Name_BE\|v25.0> |

<!-- YAML key format:
     eTOM -> <identifier>|<Business_Activity_Name>|<eTOM version>       (spaces become underscores)
     SID  -> <Domain>|<Level1_ABE>|[<Level2_ABE_or_BE>|]<SID version>
     Pipes inside table cells must be escaped as \| -->
