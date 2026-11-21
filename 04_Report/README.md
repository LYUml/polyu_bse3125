# Current report sources

Edit the narrative and references in `LaTeX/sections/`. The document entry point is `LaTeX/main.tex`. The sections follow the nine narrative pages of the previous report. The title block, Times New Roman styles and table and caption definitions are in the entry point.

From the workspace root, run the following PowerShell command, choosing a fresh output directory for each review.

```powershell
& ../dialux-agent-toolkit/.venv/Scripts/python.exe -X utf8 06_Tools/rebuild_report.py 04_Report/Build/Review_New
```

The build uses XeLaTeX and the installed Times New Roman font. It generates the illustrations from the shared engineering data and native evidence, compiles the narrative, and assembles the original A2 lighting plan and simulation appendix. It writes the combined PDF, previews and assembly checks in the output directory. The reviewed delivery is in `00_Submit`.

`Editorial_Inputs/` preserves the two original group files. `LaTeX/appendix-d.tex` and the false-colour images in `Assets/` supply Appendix D.

`Report_Text_For_Editing.md` is the editorial snapshot for this revision. The previous ReportLab narrative and its `content.json` are retained for the earlier edition. The native comparison data is in `comparison-summary.json`.
