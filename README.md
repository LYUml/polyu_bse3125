# BSE3125 - Optics and Lighting

Final comparison revision, 2026-11-16. The local deliverable is `00_Submit/BSE3125_Lighting_Design_Report.pdf`: **9 main pages including the A2 CAD layout, 20 total pages, 3,839,238 bytes**. The five group members are included locally. Personalized PDFs and group metadata are excluded from Git. No course-platform submission has been made.

The retained design uses 186 Philips PowerBalance 40S luminaires (910505103638, 4000 lm/23 W). The minimum desk mean is 593 lx, minimum desk Uo 0.80 and maximum tested directional UGR 18.1. Conservative connected input including controls is 4328 W / 1022 m2 = 4.235 W/m2. The original assignment PDF and DWG remain unchanged.

Two independent native DIALux comparisons now support the design discussion:

| Condition | Lowest desk mean | Lowest desk Uo | Highest UGR |
|---|---:|---:|---:|
| Baseline, full output, 80/70/20% reflectance | 593 lx | 0.80 | 18.1 |
| 90% output, original reflectance | 534 lx | 0.80 | 17.7 |
| Full output, 70/50/20% reflectance | 566 lx | 0.79 | 18.6 |

All adopted auxiliary criteria also pass. Each comparison has separate core and auxiliary native models, calculated, saved and reopened; all 112 core rows and 288 auxiliary rows persist exactly. The ineffective first dimming auxiliary experiment is rejected and replaced by the verified active-prototype calculation. A 10% light-output reduction is not claimed as a 10% electrical saving. The two changes were not combined in one scenario.

Current acceptance: [assignment-acceptance-v4.json](05_Calculations/Final_v04/assignment-acceptance-v4.json). Shared design binding: [final-design-v4.json](05_Calculations/data/final-design-v4.json). Editable narrative, evidence index and reproduction instructions: [Final_v04](05_Calculations/Final_v04/README.md). The previous 14-page report is archived in `05_Calculations/Archive/2026-11-16_Pre_Comparisons`; the older detailed version remains in `2026-11-16_Pre_Concise`.

Native CAD remains `05_Calculations/Final_v03/cad-native-v5/layout.dwg`; native DIALux models and full raw reports are retained locally under `05_Calculations/models`. Large caches stay local; compact result datasets and verification records are tracked. Earlier versions and pending states in PROJECT_SPEC.md are historical.

Automation uses the separately maintained [DIALux Agent Toolkit](https://github.com/LYUml/dialux-agent-toolkit). Synthetic toolkit outputs are not coursework results. Furniture, finish, facade, maintenance and commissioning assumptions remain explicit in the report.
