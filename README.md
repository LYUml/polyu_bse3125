# BSE3125 - Optics and Lighting

[中文文件导航](README.zh-CN.md)

Current handover: `00_Submit/BSE3125_Lighting_Design_Report.pdf` (9 main pages including CAD, 20 pages total, 3,714,013 bytes). `00_Submit/DIALux/Final` contains the two final-scheme native models; `Comparisons` contains four native comparison models. All six are byte-identical to the saved/reopened verified originals. No course-platform submission has been made.

| Directory | Purpose |
|---|---|
| 00_Submit | Final PDF and clearly separated native DIALux delivery copies |
| 01_Assignment_Brief | Immutable assignment PDF and source DWG |
| 02_References | Standards, manufacturer documentation and photometry |
| 03_Engineering | Current DIALux, CAD and full native calculation reports |
| 04_Report | Current editable narrative, assets, private metadata and build output |
| 05_Calculations | Shared design/result data and verification records |
| 06_Tools | Current report build pipeline and engineering utilities |
| 90_Archive | Historical drafts, trials, models and documentation |

The baseline retains 186 Philips PowerBalance 40S luminaires, minimum desk mean 593 lx, minimum Uo 0.80, maximum tested UGR 18.1 and connected input 4328 W. The 90% output and lower-reflectance scenarios remain independent; no global optimum or measured dimming-energy saving is claimed.

Use `06_Tools/rebuild_report.py NEW_OUTPUT_DIRECTORY` with the sibling toolkit Python. The current pipeline has no archive dependency. All 20 rebuilt pages match the delivered PDF in text, dimensions and 72/150 dpi pixels. Current binding: `05_Calculations/data/final-design.json`; handover verification: `05_Calculations/workspace-verification.json`; file relocation index: `05_Calculations/workspace-migration.json`.

Personalized PDFs, private group metadata, large native models and full raw reports remain local. The original assignment and source drawing are unchanged. Historical evidence retains its original paths and hashes; resolve relocated paths using `06_Tools/resolve_evidence_path.py`.
