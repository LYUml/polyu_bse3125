# Final comparison report

Accepted on 2026-11-16 under the report's declared academic assumptions. Local final: `../../00_Submit/BSE3125_Lighting_Design_Report.pdf` (9 main pages including CAD, 11 appendix pages, 20 total; 3,839,238 bytes). SHA-256: b9c3c35d2f94aad171bca81934440754221552adc8b4f044c3225cb1b52425ec. `assignment-acceptance-v4.json`, `assembly-manifest.json` and `visual-review.json` record the checks. Personalized PDFs and private group details remain local.

## Editable sources and reproduction

Run from the assignment root with the sibling toolkit's `.venv/Scripts/python.exe`. `content.json` holds the revised narrative; `../local/group-details.json` supplies private cover information. `format-specification.json` documents Times New Roman 12 pt body, 15 pt leading and modular heading/table conventions. The main report is eight A4 pages plus the unchanged A2 CAD sheet.

1. `05_Calculations/scripts/build_comparison_report.py NEW_MAIN_PDF` creates the eight narrative pages (accepted local source: `main-report-v5.pdf`).
2. `summarize_comparisons.py` verifies the three reopened result sets and creates `comparison-summary.json`. It refuses to overwrite existing evidence.
3. `build_comparison_appendix.py NEW_APPENDIX_PDF` creates the one-page modular comparison. Assembly uses the accepted `comparison-appendix.pdf`.
4. `assemble_comparison_report.py MAIN_PDF NEW_COMBINED_PDF` preserves the CAD and ten selected original DIALux pages, checks exact text/dimensions/pixels at 72 and 150 dpi, and renders every assembled page. Accepted local combined source: `final-report-v5.pdf`.
5. Visual review precedes `accept_comparison_report.py`. That one-time promotion script validates the specific prior PDF hash, archives it, checks source/design/native/result/group/font/page constraints, then replaces the local final. Do not rerun promotion against a different current version.

The first assembly attempt stopped on relative-path manifest handling after writing an intermediate PDF. `BSE3125_Lighting_Design_Report.pdf` in this working directory is not the accepted assembled artifact; use `final-report-v5.pdf` or the sole deliverable in `00_Submit`.

## Native projects retained locally

Under `../models`:

- Baseline core: `office-review-40s-native-v4.evo`.
- Baseline auxiliary: `office-review-brightness-native-v4.evo`.
- 90% core: `office-comparison-output90-core-verified-v2.evo`.
- 90% auxiliary: `office-comparison-output90-aux-verified-v3.evo`.
- Lower-reflectance core: `office-comparison-reflectance-core-verified-v2.evo`.
- Lower-reflectance auxiliary: `office-comparison-reflectance-aux-verified-v2.evo`.

Exact hashes, fresh/reopened native PDF hashes and row persistence are linked in `assignment-acceptance-v4.json`. The first 90% auxiliary attempt had an inactive prototype dimming key and is explicitly rejected in `comparison-output90-aux-rejection-v1.json`. Only the corrected v2 result dataset is used. Geometry, 186 positions, maintenance factors, manufacturer photometry and calculation surfaces remain source-verified.

Native CAD remains `../Final_v03/cad-native-v5/layout.dwg`; its matching A2 native plot is `../Final_v03/cad-plot-v5/BSE3125-L01-lighting-plan.pdf`. The original assignment and drawing hashes are unchanged. The prior anonymous 14-page final is in `../Archive/2026-11-16_Pre_Comparisons`.

These are two independent scenarios, not a combined adverse-condition test. All adopted metrics pass, but no measured dimming power curve, annual savings or unconditional statutory certification is claimed. No Blackboard submission has been made.

The current heading is "Open-plan Office Lighting Design", with subtitle "BSE3125: Optics and Lighting". Six IEEE-style references are authored in `content.json`, in first-citation order. The PolyU/course reference is removed; calculation-object and maintenance-factor guidance are added. `reference-review.json` records sources and formatting guidance. Previous personalized PDFs remain local under `../local`; archived acceptance/source records are in `../Archive/2026-11-16_Pre_References`.
