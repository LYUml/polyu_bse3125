# Design data and verification

`data/final-design.json` is the current shared binding. Other files in `data` contain measured geometry, assumptions, fixture/desks/control positions, actual native result tables, calculation logs and historical verification checkpoints. Do not infer the latest state from filename sorting; use the current binding and handover record.

`workspace-verification.json` verifies the reorganized handover and exact report reproduction. `workspace-migration.json` records every moved file, its hash and old-to-current path lookup. Historical JSON evidence retains original path strings to avoid rewriting hash-bound evidence. Resolve a former path with `06_Tools/resolve_evidence_path.py`.

Final editable engineering lives in `03_Engineering`; report sources in `04_Report`; historical models and drafts in `99_Archive`.
