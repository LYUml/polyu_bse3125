# BSE3125 current project specification

Assignment production and repository synchronization are authorized. User authorized adding native DIALux projects to `00_Submit` and reorganizing the workspace on 2026-11-16. No Blackboard submission is authorized by this task.

## Deliverable

One final PDF: 10 main pages including the independent A2 lighting layout, 15 appendix pages, 25 total pages, 5,036,266 bytes. Native final/comparison evo copies are additional local handover files under `00_Submit/DIALux`, organized separately from the PDF.

## Engineering basis

186 Philips PowerBalance gen2 910505103638 units, 4000 lm/23 W each; ceiling 2.8 m, task plane 0.8 m, UGR observer 1.2 m; MF 0.80. Baseline ceiling/wall/floor reflectances 80/70/20%, columns 40%. Measured gross/net areas 1042.097970/1032.573045 m2; the traced 1042.10 m2 internal floor area is used for LPD; the 1022 m2 drawing annotation is recorded separately. Shared positions, CAD and model remain consistent.

Baseline minimum desk mean/Uo and maximum directional UGR: 593 lx/0.80/18.1. Output90 comparison: 534 lx/0.80/17.7. Lower-reflectance comparison: 566 lx/0.79/18.6. The combined comparison gives 509 lx/0.79/18.2. Each scenario has separate core and auxiliary native projects with 112 and 288 reported result rows.

## Rubric and format

DIALux procedure/functions and figures (20%); luminaire/system selection (20%); criteria summary (15%); results discussion (25%); independent CAD layout with grid, legend and schedule (20%). Main report <=10 pages, combined PDF <=10 MB. Current body is Times New Roman 12 pt, numbered sections, IEEE references, Group 4 names in two alphabetical lines. No PolyU reference entry. CAD P05 has tabulated luminaire information and actual spacing dimensions; all 186 fixture records match the accepted design.

## Current sources and evidence

- Editable report: `04_Report/content.json`; assets: `04_Report/Assets`; private group metadata: `04_Report/Private`.
- Build: `06_Tools/rebuild_report.py`; authoring modules: `06_Tools/report`.
- Native engineering: `03_Engineering/project-index.json`; current CAD: `03_Engineering/CAD/manifest.json`.
- Shared design: `05_Calculations/data/final-design.json`.
- Directory/rebuild handover: `05_Calculations/workspace-verification.json`.
- Historical engineering acceptance: `99_Archive/Development/Final_v04/assignment-acceptance-v4.json`; presentation checks: `99_Archive/Development/Final_v04/figure-layout-review.json`. Historical path references resolve through `05_Calculations/workspace-migration.json`.

The original assignment PDF and DWG retain their fingerprints. All relocated files were hash-checked. The current build verifies component text, dimensions and 72/150 dpi rendering outside the case labels. Historical pending/rejected experiments are archived, not current deliverables. The former detailed development specification is preserved under `99_Archive/Documentation`.
