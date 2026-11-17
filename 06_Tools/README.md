# Current tools

Use the sibling `dialux-agent-toolkit/.venv/Scripts/python.exe` from the workspace root.

- `rebuild_report.py NEW_OUTPUT_DIRECTORY`: regenerate the current report from `04_Report`, `03_Engineering` and shared data. Requires a new output directory and preserves the final delivery PDF.
- `report/`: current narrative/appendix assembly and vector figures. The pipeline no longer imports historical report scripts.
- `resolve_evidence_path.py OLD_PATH`: locate a moved file referenced by a historical evidence record.
- `plot_assignment_plan.py DWG NEW_OUTPUT_DIRECTORY PLAN_JSON`: native AutoCAD plot and scale/fixture verification; supply current paths explicitly.
- `run_cli.py`, native archive/calculation helpers: retained engineering automation using the sibling toolkit backend. Inspect capabilities and use explicit paths before mutations. One live DIALux desktop operation at a time; inspect actual output after timeouts.
- `.runtime`: local PDF assembly dependencies; excluded from Git.
- `restructure_workspace.py`: one-time completed migration record generator; do not rerun over the reorganized workspace.

Historical authoring/one-time acceptance scripts are preserved under `99_Archive/Development/scripts`; their old relative paths are archival context, not current entry points. Synthetic toolkit outputs are never assignment results.
