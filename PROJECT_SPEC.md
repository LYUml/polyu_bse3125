# BSE3125 lighting design

Assignment production authorized 2026-11-15; repository synchronization authorized 2026-11-16. Original files remain unchanged. This is work in progress, not an accepted submission.

## Deliverables and acceptance

- One combined PDF <=10 MB, main report including figures and formal lighting layout <=10 pages; actual DIALux simulation outputs in appendix.
- Explain DIALux modelling, assumptions, photometry, calculation objects, simulation and documentation with project-specific figures (20%).
- Justify luminaires and layout using office activity, furniture and 600 mm ceiling grid; explain controls (20%).
- Source-backed comparison table of criteria and actual results (15%).
- Interpret spatial results, glare, uniformity, energy and design iteration (25%).
- Independent formal CAD plan with simplified symbols, legend and luminaire schedule, aligned with ceiling grid (20%). No circuit/switch drawing required.
- Save/reopen native evo; verify source-to-model geometry, model parameters, all fixture coordinates/counts, product identity and exported results. Native DWG reopen/plot plus visual PDF review.

## Course evidence

Course directory: C:/Users/lyuml-win/iCloudDrive/Desktop/y3_s1/bse3125.
The course Layout.dwg matches the workspace DWG SHA-256. Brief content matches the supplied assignment.
P01 recording transcript (2026-10-20), 8:56-17:24 and 20:45-21:30: office paperwork design targets average 500 lx, Uo >=0.6, UGR <=19, with local BEC LPD check; lamp colour rendering also discussed. These are course targets, not independently authenticated international-standard quotations.
P02 transcript (2026-10-27), 11:15-24:18: distinguish whole working plane from desk task surfaces; justify critical desk selection using spatial distributions. 25:09-28:18: UGR at 1.2 m seated eye level, 0.4 m offset above 0.8 m desks, directional evaluation. Transcript is automated and may contain recognition errors; do not quote its misspellings as terminology.
Mini_Design_Submission.html: due 22 November 2026 23:59, one group representative, single PDF. No submission action authorized.

## Current design basis and open gates

- Native-converted drawing: millimetres, footprint 45 x 30 m; selected office is L-shaped around northern core.
- Initial interior polygon: 1042.097970 m2 before columns, 1032.573045 m2 after eight source-linked column intersections. Source text says 1022 m2. Discrepancy remains open; do not force a match or label annotation a measurement.
- Initial assumptions: ceiling 2.8 m, workplane 0.8 m, MF 0.80, ceiling/wall/floor 70/50/20%. These are adjustable design assumptions.
- Native geometry import completed; native readback, furniture arrangement, calculation objects and lighting design pending.
- Candidate RC132V G6 43S/840 SIA W60L60 OC IA4, 910505102802: source photometry cached by toolkit. Datasheet/photometry dimensions differ; reconcile nominal module versus physical envelope and power before final selection.
- International source row/edition and Hong Kong BEC applicability must be verified. Course's illustrative 8.5 W/m2 must not substitute for the correct >200 m2 category in BEC 2024.

## Reuse

Use sibling dialux-agent-toolkit (CLI and MCP share backend), its MIT-licensed MCP_Dialux STF serializer/reader, installed ezdxf/Shapely/PDFium and native AutoCAD Core Console workflow. See 02_References/reuse-register.md. Do not copy synthetic simulation results into this assignment.

## Repository checkpoints

Push meaningful milestones to https://github.com/LYUml/polyu_bse3125.git. Commit naming: YYYY-MM-DD English description. Preserve original sources and native design; exclude caches, personal course/group records and crash dumps.
