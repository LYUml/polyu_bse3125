# BSE3125 lighting design

Assignment production authorized 2026-11-15; repository synchronization authorized 2026-11-16. Original files remain unchanged in 01_Assignment_Brief. Follow BSE3124's current layout: 00_Submit is the sole final entry; 05_Calculations holds shared data, working models and Final_vXX editable sources/evidence; 06_Tools holds automation. The final deliverable was accepted for handover on 2026-11-16; no course-platform submission has been made. Historical pending/rejected states below describe their own development checkpoints, not the final handover status.

## Current comparison revision, 2026-11-16

Final PDF: 00_Submit/BSE3125_Lighting_Design_Report.pdf; 9 main pages including CAD + 11 appendix pages = 20 total; 3,838,818 bytes; SHA-256 03c33583a0bfc768a2cacca6a1bd84758f7cabcb1604485efabd3404308b5366. Current acceptance: Final_v04/assignment-acceptance-v4.json; shared binding: data/final-design-v4.json. Editable source: Final_v04/content.json. The 14-page version below is archived in Archive/2026-11-16_Pre_Comparisons.

Native 90% output: minimum desk mean 534 lx, Uo 0.80, maximum UGR 17.7. Native lower reflectance (70/50/20%, full output): 566 lx, Uo 0.79, UGR 18.6. All auxiliary criteria pass. Each case has saved/reopened core and auxiliary verification (112 and 288 rows respectively). Full output remains the design condition; dimming is a commissioning option. No combined-case or measured electrical-saving claim. Original inputs, shared fixture positions, manufacturer photometry and final CAD are unchanged. Group metadata and personalized PDFs remain local and untracked. No platform submission.

## Historical concise handover before comparisons, 2026-11-16

User authorized replacement and archival. Current PDF: 00_Submit/BSE3125_Lighting_Design_Report.pdf; 9 main pages including CAD + 5 native appendix pages = 14 total; 1,883,123 bytes; SHA-256 160c3bb9cf17e3c8691913287ba4a4a0b8d0aa2faf647ab32ba3fd2cbc2ce9b0. Verification: Report_Draft_v02/final-promotion.json. Binding: data/final-design-v3.json. Editable source: Report_Draft_v02/content.json; build_classic_draft.py and assemble_classic_draft.py. Engineering unchanged. Old PDF retained in 05_Calculations/Archive/2026-11-16_Pre_Concise. No platform submission.

## Historical detailed handover after strict review, 2026-11-16

- Current PDF: 00_Submit/BSE3125_Lighting_Design_Report.pdf; 9 main pages including A2 CAD, 192 total pages, 5,978,804 bytes; SHA-256 c13386ab9773183073f2679e661a21cedc4675a4698facefeca50f681fee6c3b.
- Current acceptance: Final_v03/assignment-acceptance-v3.json; current shared binding: data/final-design-v2.json. Earlier handover below is historical and superseded.
- Actual native upgrade to 910505103638, 4000 lm/23 W, same 186 ceiling-tile positions. Minimum desk mean 593 lx, minimum Uo 0.80, maximum UGR 18.1. Conservative 4328 W / 1022 m2 = 4.235 W/m2.
- Reopened supplemental minima: seated cylindrical 224 lx; surrounds 595 lx; background 617 lx; exposed walls 216 lx; exposed ceiling 137 lx. Combined uniformity bounds pass. All 112 core desk and 288 auxiliary result rows persist.
- Core native v4 SHA-256 1c2421837b10cd910d405670c88715167acc3b14798ab374517357a03e804e82; supplemental native v4 102608c64a64a4d9838fb652a09d7a8322cc346da69aec9c563d6f6b101a2742. Title-only copies preserve calculated result streams and have actual native reopen/export evidence.
- Rewritten narrative explains grid/Uo/interreflection/UGR, quantitative iterations, manufacturer optics, standby-inclusive controls, tolerance sensitivity and 82/86 mm body discrepancy. Native CAD P03 is Final_v03/cad-native-v5/layout.dwg.
- All 192 assembled pages preserve source text, dimensions and exact pixels at 72/150 dpi. Main pages, CAD, appendix guide and representative native tables/plots visually reviewed. No course-platform submission.

## Historical earlier handover, 2026-11-16


- `00_Submit/BSE3125_Lighting_Design_Report.pdf`: 8 main pages including the independent A2 CAD layout, 191 total pages including actual native appendices, 5,859,608 bytes; SHA-256 b5ab0097513f67dea744bb01376eae68206cacbaef84ceb1495a28838b08a384.
- Requirement-by-requirement audit: `05_Calculations/Final_v02/assignment-acceptance-v1.json`. Editable English narrative is report-content-v1.json; build_main_report.py and assemble_submission.py reproduce the report/assembly from the retained sources.
- Native auxiliary cutouts are represented by 255 independently verified CalculationSurfaceOpening objects, observed from a native-created example. All 36 physical regions preserve their intended geometry and coordinate systems. The failed triangle experiment is not used.
- Supplementary saved/reopened results: seated cylindrical minimum mean 190 lx; surrounding mean >=506 lx; background 525 lx; exposed wall means >=183 lx; ceiling 116 lx/Uo 0.89. Conservative combined uniformity bounds also pass. All 288 table rows persist after reopening.
- Supplemental native file SHA-256 6548a5bb46c2c02f70fedb5dc0808efa433e6715fc063c017691856e3bba8293; core native file f0819433f90081f1802c75065ff7ea92756ec0baccfbd313d4a28f7552b3d33a. The 186 positions, maintenance factors, manufacturer photometry and physical room/column records match.
- All source inputs retain their original hashes. All 191 assembled pages preserve source text, physical page dimensions and exact rendered pixels at 72/150 dpi. Main report, native plots, criteria table, CAD and appendix guide were visually reviewed.
- Documented academic assumptions and qualifications remain intentional: actual facade/occupancy/maintenance must be confirmed; controls require commissioning; DSE luminance is bounded sampled screening, not full angular certification. No unconditional whole-standard/statutory certificate is claimed.

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
- Native geometry import and initial 142-fixture automatic arrangement calculated and saved. Baseline PDF pp14-15: 501 lx, Uo 0.005, 4.36 W/m2; rectangular-room glare estimate 20. **Not accepted**. Native readback, furniture/task surfaces, directional UGR, grid alignment and optimization pending. See data/baseline-calculation-observation-v1.json.
- Candidate RC132V G6 43S/840 SIA W60L60 OC IA4, 910505102802: source photometry cached by toolkit. Datasheet/photometry dimensions differ; reconcile nominal module versus physical envelope and power before final selection.
- International source row/edition and Hong Kong BEC applicability must be verified. Course's illustrative 8.5 W/m2 must not substitute for the correct >200 m2 category in BEC 2024.

## Native task-surface milestone, 2026-11-16

- Two 1.6 x 0.8 m desk surfaces at 0.8 m height have actual DIALux results. Desk-01: 479 lx average, 387 lx minimum, Uo 0.81, maximum directional UGR 20.3. Desk-02-probe: 516 lx average, 407 lx minimum, Uo 0.79, maximum directional UGR 20.2. UGR eye offset is 0.4 m, giving 1.2 m seated height; directions cover 0–360 degrees at 15-degree intervals. Neither desk establishes final design acceptance.
- An isolated native archive adapter cloned a surface created in DIALux. DIALux opened, freshly calculated, saved and reopened it. Both surface geometries and scoped report text persisted; see surface-clone-persistence-v1.json and office-surface-clone-native-v2.evo. This is bounded evidence for two surfaces, not a general project writer.
- Source-linked full ceiling tiles have been enumerated for candidate layouts. Candidate positions are geometric proposals only and are not calculated installation results.
- BEC 2024 Table 5.4 specifies 7.2 W/m2 for the office category above 200 m2, with automatic control requirements. Source clauses, control assumptions and limitations are recorded in 02_References/design-criteria.json. No comprehensive code compliance claim is made.
- The first isolated white-finish archive experiment produced unchanged illumination/glare after fresh calculation. Material propagation remains unverified. A separate cache-omission probe is experimental until native opening and changed physical parameters/results are evidenced.
- Subsequent cache rebuild succeeded: office-white-finish-native-v3.evo was calculated, saved, closed and reopened. Reopened PDF p18 confirms 80/70/20% reflection factors; pp30/31/33 give Desk-01 507 lx/Uo 0.82/UGR 19.7 and Desk-02 541 lx/Uo 0.80/UGR 19.6. Geometry, scoped report text and saved native bytes persist. Glare remains above 19. See white-finish-persistence-v1.json. This resolves propagation for this specific finish experiment, not final acceptance.
- PowerBalance 910505103630 is a new lower-glare candidate: official ULD, LDT and leaflet cached with URLs/hashes. Native import/calculation and installation layout are still pending; catalogue UGR16 is not a room result.

## Full task-area development milestone, 2026-11-16

- Native replacement with manufacturer PowerBalance 910505103630 gives 3400 lm / 19.8 W per luminaire (datasheet rounded input 20 W). At 142 luminaires two diagnostic desks give 420/439 lx, UGR 17.4/17.5. Increasing the native 18 x 13 clipped arrangement yields 186 luminaires.
- A proposed furniture arrangement defines 112 desks in 28 four-person benches. These are design assumptions, not supplied architectural furniture. Source-boundary/column checks reserve at least 0.9 m around benches and 1.8 m between them. All desk coordinates are shared in furniture-proposal-v1.json.
- The unaligned 186-luminaire model was actually calculated for all 112 desks: minimum desk average 530 lx, minimum Uo 0.94, maximum directional UGR 17.0. Full native PDF and 192.9 MB calculated evo are retained locally; compact original-page evidence and hashes are tracked. See alltasks-results-v1.json. This is not final acceptance because this arrangement is not ceiling-grid aligned.
- All 186 snapped fixture positions have subsequently matched the native report coordinate table one-to-one, tied to source tile handles. After snapping, Desk-084 gives 497 lx, so that variant fails the adopted average criterion despite maximum UGR 17.5 and minimum desk Uo 0.82. A one-tile local refinement of L120 is under actual recalculation; do not call it accepted before reviewing all tasks again.
- Grid probe v1 was rejected by DIALux because a zero coordinate was serialized as an integer. Probe v2 uses real-valued STEP coordinates (`0.`) and opened/calculated successfully; failure evidence is retained. No toolkit guard or source was modified.
- The native calculation/export worker observation windows are shorter than these full-task operations. Timeout records remain intact; actual GUI completion and stable parsed native reports provide subsequent evidence. Do not automatically repeat a calculation or export on an observation timeout.
- Control design proposal: 32 independent manual/automatic zones linked to the refined shared fixture dataset; maximum zone area 46.68 m2. Proposed vacancy off is 10 minutes and timed overrides expire within 120 minutes. Conservative input budget is 186 x 20 W + 50 W external control allowance = 3770 W (3.689 W/m2 using the smaller annotated 1022 m2). These are design provisions requiring commissioning, not installed-system evidence.
- Remaining gates include refined grid results, native save/reopen persistence, final height/geometry/asset checks, independent CAD drawing/native plot, standards discussion, <=10-page main report, selected actual-output appendix and <=10 MB combined PDF with visual QA. 00_Submit remains empty.

## Refined grid and CAD milestone, 2026-11-16

- Moving L120 one 600 mm tile south raises Desk-084 from 497 to 557 lx. All 112 proposed tasks now pass: minimum average 504 lx, minimum Uo 0.80, maximum directional UGR 17.5. The smallest average margin is 4 lx (Desk-021), which must be discussed rather than hidden.
- Refined native model was saved, closed and reopened. All task result rows and all 186 report positions persisted. The saved native bytes remained unchanged after reopening/export. Every proposed task's 1.6 x 0.8 m geometry, 0.8 m plane and 1.2 m/15-degree UGR parameters were checked. All fixtures retain MF 0.8 and the same manufacturer prototype; its 63-record photometry/geometry graph matches the imported native baseline. See refined-native-persistence-v1.json.
- Independent CAD v3 uses the same source-tile fixture data. Native AutoCAD save/reopen preserves 186 fixture blocks/IDs, two dimensions, schedule and sheet entities. Native A2 1:100 output has all fixture labels and a physical outline error below 0.037 pt. Whole-sheet and detail visual review confirms readable labels, lighter furniture/grid, complete frame, schedule and legend. See Final_v01 README and cad visual review record.
- Original selected DIALux appendix pages were resource-pruned to 2,617,951 bytes while retaining text, physical dimensions and exact 72/150-dpi rendering. Complete raw native outputs remain local with recorded hashes. Final main report and assignment-wide acceptance remain outstanding.
- International-guideline review must also resolve the additional surrounding-area, cylindrical, wall and ceiling criteria identified in design-criteria.json. The verified desk metrics alone do not prove these quantities. Do not silently omit them or claim comprehensive EN 12464-1:2021 conformity.

## Auxiliary brightness and geometry review, 2026-11-16

- The exact international office row and surrounding/background/cylindrical/wall/ceiling clauses were reviewed; see `02_References/international-clause-review.json`. Full copyrighted review copies remain local and untracked.
- Source office-facing core wall lines were checked against the saved native inner contour. Maximum boundary difference is 0.333 mm from source-coordinate rounding; measured gross area is 1042.097970 m2 and native gross area is 1042.101010 m2. The drawing's 1022 m2 annotation is not substituted for measured geometry. See office-boundary-verification-v1.json.
- Auxiliary v4 native results show all 112 seated cylindrical task averages >=190 lx, immediate surrounding averages >=518 lx, background floor 529 lx, and exposed wall averages >=181 lx. These remain provisional until actual evaluation-region coverage and saved/reopened persistence are verified. Exposed ceiling mean 115 lx has a near-zero minimum and fails the adopted uniformity criterion.
- The v5 equivalent-triangle experiment is rejected: native report omits background and ceiling calculation rows. Its geometric union precheck is insufficient for native coverage. The strict report reader failed on missing surfaces. See brightness-tessellated-rejection-v5.json; do not accept this partial output.
- Native wall default 0.5 m borders are being replaced with 0.42 m borders for 2.8 m-high walls, following EN 12464-1:2021 5.4's smaller-of-15%-or-0.5-m rule. Newly generated v6 geometry is uncalculated and is not accepted evidence.
- A bounded manufacturer LDT screening calculation gives sampled maximum 1134.23 cd/m2 for gamma 65–89 degrees, below the adopted 1500 cd/m2 DSE category. The 90-degree endpoint has zero projected flat aperture area and does not support a finite value; no complete 65–90-degree conformity or between-sample maximum claim is made. See dse-luminance-check-v1.json.

## Reused implementation details

Use sibling dialux-agent-toolkit (CLI and MCP share backend), its MIT-licensed MCP_Dialux STF serializer/reader, installed ezdxf/Shapely/PDFium and native AutoCAD Core Console workflow. See 02_References/reuse-register.md. Do not copy synthetic simulation results into this assignment.

## Repository checkpoints

Push meaningful milestones to https://github.com/LYUml/polyu_bse3125.git. Commit naming: YYYY-MM-DD English description. Preserve original sources and native design; exclude caches, personal course/group records and crash dumps.
