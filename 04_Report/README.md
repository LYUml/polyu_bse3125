# Current report sources

- `content.json`: editable English narrative, title/subtitle and manufacturer, standards and software references.
- `comparison-summary.json`: actual verified results for the four conditions.
- `Assets/native-room-view.png`: original native room view. Other figures use native PDF excerpts or vectors generated from the shared datasets by `06_Tools/report/report_figures.py`.
- `Private/group-details.json`: group names and IDs used on the title page.
- `Build`: reproducible local main report, comparison appendix, combined PDF and page previews, excluded from Git.
- `format-specification.json` and `reference-review.json`: formatting/source decisions.

From the workspace root, use the sibling toolkit Python to run `06_Tools/rebuild_report.py NEW_OUTPUT_DIRECTORY`. The output directory must not already exist. This rebuild does not replace the delivery PDF automatically. Current authoring has no dependency on archived drafts. The build verifies source text, dimensions and rendering, with case labels added to the top margin of comparison excerpts.

Main report: nine A4 pages plus A2 CAD = 10 pages; appendix: 15 pages; total: 25. The final delivery is always the PDF in `00_Submit`.
