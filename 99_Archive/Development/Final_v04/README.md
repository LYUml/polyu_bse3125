# Final comparison report

Accepted on 2026-11-16 under the report's declared academic assumptions. Local final: `../../00_Submit/BSE3125_Lighting_Design_Report.pdf` (9 main pages including CAD, 11 appendix pages, 20 total; 3,714,013 bytes). SHA-256: 62036e4b3957cbde931a18bb23ed0d3a43d3e7c6604944774d3132315fa66a50. `assignment-acceptance-v4.json`, `assembly-manifest.json` and `visual-review.json` record the checks. Personalized PDFs and private group details remain local.

## Editable sources and reproduction

Run from the assignment root with the sibling toolkit's `.venv/Scripts/python.exe`. `content.json` holds the revised narrative; `../local/group-details.json` supplies private cover information. `format-specification.json` documents Times New Roman 12 pt body, 15 pt leading and modular heading/table conventions. The main report is eight A4 pages plus the revised A2 CAD sheet.

1. `05_Calculations/scripts/build_comparison_report.py NEW_MAIN_PDF` creates the eight narrative pages (accepted local source: `main-report-v8.pdf`).
2. `summarize_comparisons.py` verifies the three reopened result sets and creates `comparison-summary.json`. It refuses to overwrite existing evidence.
3. `build_comparison_appendix.py NEW_APPENDIX_PDF` creates the one-page modular comparison. Assembly uses the accepted `comparison-appendix-v3.pdf`.
4. `assemble_comparison_report.py MAIN_PDF NEW_COMBINED_PDF` preserves the CAD and ten selected original DIALux pages, checks exact text/dimensions/pixels at 72 and 150 dpi, and renders every assembled page. Accepted local combined source: `final-report-v9.pdf`.
5. Current presentation promotion uses `accept_figure_revision.py`, which checks original/shared-data hashes, unchanged CAD geometry, native save/reopen/plot evidence, references, group metadata, font/margins, original native appendix pixels and the exact previous final hash. It is a one-time promotion, not a reusable overwrite command. `accept_comparison_report.py` documents the earlier comparison handover.

The first assembly attempt stopped on relative-path manifest handling after writing an intermediate PDF. `BSE3125_Lighting_Design_Report.pdf` in this working directory is not the accepted assembled artifact; use `final-report-v9.pdf` or the sole deliverable in `00_Submit`.

## Native projects retained locally

Under `../models`:

- Baseline core: `office-review-40s-native-v4.evo`.
- Baseline auxiliary: `office-review-brightness-native-v4.evo`.
- 90% core: `office-comparison-output90-core-verified-v2.evo`.
- 90% auxiliary: `office-comparison-output90-aux-verified-v3.evo`.
- Lower-reflectance core: `office-comparison-reflectance-core-verified-v2.evo`.
- Lower-reflectance auxiliary: `office-comparison-reflectance-aux-verified-v2.evo`.

Exact hashes, fresh/reopened native PDF hashes and row persistence are linked in `assignment-acceptance-v4.json`. The first 90% auxiliary attempt had an inactive prototype dimming key and is explicitly rejected in `comparison-output90-aux-rejection-v1.json`. Only the corrected v2 result dataset is used. Geometry, 186 positions, maintenance factors, manufacturer photometry and calculation surfaces remain source-verified.

Current native CAD is `cad-native-v7/layout.dwg` (P04); its matching A2 native plot is `cad-plot-v7/BSE3125-L01-lighting-plan.pdf`. The previous P03 remains in Final_v03. The original assignment and drawing hashes are unchanged. The prior anonymous 14-page final is in `../Archive/2026-11-16_Pre_Comparisons`.

These are two independent scenarios, not a combined adverse-condition test. All adopted metrics pass, but no measured dimming power curve, annual savings or unconditional statutory certification is claimed. No Blackboard submission has been made.

The current heading is "Open-plan Office Lighting Design", with subtitle "BSE3125: Optics and Lighting". Six IEEE-style references are authored in `content.json`, in first-citation order. The PolyU/course reference is removed; calculation-object and maintenance-factor guidance are added. `reference-review.json` records sources and formatting guidance. Previous personalized PDFs remain local under `../local`; archived acceptance/source records are in `../Archive/2026-11-16_Pre_References`.

## Figure and CAD presentation revision

`report_figures.py` creates editable vector diagrams from the unchanged shared datasets. Figure 1 now pairs the native room view with calculation heights; Figure 2 shows larger layout and manufacturer LDT curves; Figure 3 uses clear controlling-desk markers; Figure 4 compares the three critical desks directly; Figure 5 shows all 32 control boundaries without luminaire clutter. Table 2 separates source clauses into a note, Table 3 includes criteria, and Table C1 separates illuminance and uniformity rows. No new simulated result is invented or claimed.

`refine_lighting_plan.py v7` generated the P04 CAD source and verified native round-trip using the existing toolkit backend. `06_Tools/plot_assignment_plan.py` verified the actual AutoCAD A2 plot and scale. `figure-layout-review.json` records all 186 identical fixture records, 4448 unchanged geometry entities, full input fingerprints and visual review. The former personalized final remains local as `../local/report-before-figure-revision.pdf`; source/evidence records are in `../Archive/2026-11-16_Pre_Figure_Revision`. Intermediate main/final v7 PDFs failed the page-count gate and are not deliverables.
