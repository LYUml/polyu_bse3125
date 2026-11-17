# Working design evidence — report not yet accepted

This folder holds the current validated CAD candidate and selected actual simulation output. It is not the complete assignment submission. `00_Submit` remains empty.

- Current CAD: `BSE3125-L01-lighting-plan-v3.dxf`, native `cad-native-v3/layout.dwg`, and `cad-plot-v3/BSE3125-L01-lighting-plan.pdf`. A2 landscape, 1:100; 186 unique fixture IDs, 112 desk outlines, source architectural background, ceiling grid, schedule and legend.
- `DIALux-selected-native-output-v1.pdf`: original selected pages from the saved/reopened refined model. Its manifest maps every page to the complete native PDF and verifies identical text, dimensions and rendered pixels at 72/150 dpi. It includes all 112 task illuminance rows and critical glare/isolux pages; no result is redrawn or replaced.
- The complete calculated project is retained locally at `../models/office-powerbalance-grid-native-v4.evo` (192,962,019 bytes; SHA-256 `f0819433f90081f1802c75065ff7ea92756ec0baccfbd313d4a28f7552b3d33a`). The complete native PDF is also local. Large result caches are excluded from Git; geometry-generating copies, shared datasets, selected native pages and verification records are tracked.
- Earlier CAD v1 is rejected: a source dynamic ceiling block regenerated with millimetre parameters after conversion. v2 flattened that block before transformation. v3 also improves furniture contrast and annotation clearance. Earlier versions remain as development evidence, not alternative final drawings.

Pending: complete guideline review/discussion, report authoring, combined PDF packaging and final visual/content acceptance.
