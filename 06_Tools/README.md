# Tools

Backend: C:/Users/lyuml-win/Desktop/dialux-agent-toolkit, inspected commit ade128b7ae446c6ea253776a5ead866280d6bf4a.
Python: that checkout's .venv/Scripts/python.exe. Run CLI from toolkit root with `-m src.dialux_agent`; use absolute assignment paths.
Only one live DIALux desktop operation at a time. Inspect status and journals after timeout; never blindly repeat a mutation.

Assignment scripts live in 05_Calculations/scripts. Source survey reads original files and reused native-converted DXF, verifies hashes and generates inspection evidence. prepare_model.py generates the initial source-linked room specification, not final simulation or compliance evidence.

Final report authoring uses `05_Calculations/scripts/build_main_report.py AUXILIARY_RESULTS_JSON NEW_MAIN_PDF`; pass `--draft` for visible draft marks. It reads the shared coordinate/result datasets and editable `Final_v02/report-content-v1.json`. The native full core PDF remains local and provides the actual Desk-021 figure. Use new output paths.

`05_Calculations/scripts/assemble_submission.py NEW_COMBINED_PDF OPTIONAL_MAIN_PDF` combines the seven-page narrative with the verified CAD plan, a new appendix guide and the preserved native excerpts. It checks all 191 pages against their component sources at text, physical size and 72/150-dpi pixel levels. A fresh reproduction was verified in sessions/reproduction-v1.pdf. The accepted handover is the separate PDF in 00_Submit, bound by Final_v02/assignment-acceptance-v1.json.

`apply_native_surface_openings.py` is the adopted assignment-specific native cutout adapter. `flatten_auxiliary_holes.py` is a rejected experiment; do not use its partial native output as evidence. Native geometry, result and persistence verification remain mandatory for any modified design.

## Current revised handover (supersedes earlier authoring paths above)

Run scripts/build_review_report.py NEW_MAIN_PDF from assignment root. It uses Final_v03/report-content-v3.json, shared plan v3 and reopened v4 native result datasets. Run scripts/assemble_review_submission.py NEW_COMBINED_PDF OPTIONAL_MAIN_PDF to combine 8 A4 pages, current A2 CAD, guide and 182 preserved native pages. scripts/verify_review_persistence.py checks current native archives/reopened rows; scripts/accept_review_assignment.py checks final constraints and copies the accepted PDF to 00_Submit. Use fresh build/output paths. Do not use historical nominal 3400 lm scripts for the current 4000 lm design.
