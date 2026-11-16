# BSE3125 - Optics and Lighting

Revised after strict rubric and engineering review on 2026-11-16.

**Final PDF:** [BSE3125_Lighting_Design_Report.pdf](00_Submit/BSE3125_Lighting_Design_Report.pdf) — 9 main pages including the independent A2 CAD plan; 192 pages with original native simulation appendices; 5,978,804 bytes. No course-platform submission has been made.

The revised 186-unit Philips PowerBalance 40S design (910505103638, 4000 lm/23 W) has a minimum desk mean of 593 lx, minimum desk Uo 0.80 and maximum tested directional UGR 18.1. Conservative power including controls is 4328 W / 1022 m2 = 4.235 W/m2. Both actual native calculations were saved and reopened; all 112 core desk rows and 288 supplemental rows were preserved.

Acceptance and rubric evidence: [assignment-acceptance-v3.json](05_Calculations/Final_v03/assignment-acceptance-v3.json). Shared design binding: [final-design-v2.json](05_Calculations/data/final-design-v2.json). Editable report: Final_v03/report-content-v3.json; generator: scripts/build_review_report.py; assembly: scripts/assemble_review_submission.py. Native CAD: Final_v03/cad-native-v5/layout.dwg.

Native projects retained locally: models/office-review-40s-native-v4.evo and models/office-review-brightness-native-v4.evo. Large full evo/result caches stay local; hashes and compact original-page evidence are tracked in Git. Original assignment PDF and DWG are unchanged. Final_v01/Final_v02 remain historical checkpoints; their earlier accepted values are superseded by Final_v03.

The report states furniture, finish, facade and maintenance assumptions, commissioning requirements and the limited scope of sampled display-luminance screening. These academic results are not an installed-system certificate. See PROJECT_SPEC.md for requirements and history.

Automation uses the separately maintained [DIALux Agent Toolkit](https://github.com/LYUml/dialux-agent-toolkit). Its synthetic test outputs are not coursework results.
