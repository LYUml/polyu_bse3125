# Current report sources

- `content.json`: editable English narrative, title/subtitle and six references.
- `comparison-summary.json`: actual verified results for the three conditions.
- `Assets/native-room-view.png`: original native room view. Other figures are generated as vectors from the shared datasets by `06_Tools/report/report_figures.py`.
- `Private/group-details.json`: private group names/IDs, excluded from Git.
- `Build`: reproducible local main report, comparison appendix, combined PDF and page previews, excluded from Git.
- `format-specification.json` and `reference-review.json`: formatting/source decisions.

From the workspace root, use the sibling toolkit Python to run `06_Tools/rebuild_report.py NEW_OUTPUT_DIRECTORY`. The output directory must not already exist. This rebuild does not replace the delivery PDF automatically. Current authoring has no dependency on archived drafts. The initial organized build has been compared against all 20 pages of the final delivery at text, size and 72/150 dpi pixel levels.

Main report: eight A4 pages plus A2 CAD = nine pages; appendix: eleven pages; total: twenty. The final delivery is always the PDF in `00_Submit`.
