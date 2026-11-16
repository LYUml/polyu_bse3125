"""One-time workspace relocation with bounded paths, hashes and a tracked-file map."""
from pathlib import Path
import json,hashlib,shutil,subprocess
r=Path(__file__).resolve().parents[1];log=r/'05_Calculations/workspace-migration.json';assert not log.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=r).decode().split('\0'))
originals={str(p.relative_to(r)).replace('\\','/'):sha(p) for p in (r/'01_Assignment_Brief').rglob('*') if p.is_file()}
records=[]
def safe(rel):
 p=(r/rel).resolve();assert r in p.parents and p!=r;return p
def move(src,dst):
 a,b=safe(src),safe(dst);assert a.exists() and not b.exists(),(src,dst)
 items=[a] if a.is_file() else [p for p in a.rglob('*') if p.is_file()]
 batch=[{'old':p.relative_to(r).as_posix(),'new':(b if a.is_file() else b/p.relative_to(a)).relative_to(r).as_posix(),'sha256':sha(p),'tracked':p.relative_to(r).as_posix() in tracked} for p in items]
 b.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(a),str(b))
 for item in batch:assert sha(r/item['new'])==item['sha256']
 records.extend(batch)
for folder in ['Archive','Final_v01','Final_v02','Final_v03','Final_v04','Report_Draft_v01','Report_Draft_v02','local','models','scripts','sessions']:
 move('05_Calculations/'+folder,'90_Archive/Development/'+folder)
# Move each current asset out of the frozen development history.
f='90_Archive/Development/Final_v04/'
for n in ['content.json','comparison-summary.json','reference-review.json','format-specification.json']:
 move(f+n,'04_Report/'+n)
move('90_Archive/Development/local/group-details.json','04_Report/Private/group-details.json')
move('90_Archive/Development/Final_v03/figures/native-room-view.png','04_Report/Assets/native-room-view.png')
for name in ['build_comparison_report.py','build_comparison_appendix.py','assemble_comparison_report.py','report_figures.py']:
 move('90_Archive/Development/scripts/'+name,'06_Tools/report/'+name)
move(f+'BSE3125-L01-lighting-plan-v7.dxf','03_Engineering/CAD/Lighting_Layout.dxf')
move(f+'cad-native-v7/layout.dwg','03_Engineering/CAD/Lighting_Layout.dwg')
move(f+'cad-plot-v7/BSE3125-L01-lighting-plan.pdf','03_Engineering/CAD/Lighting_Layout.pdf')
for src,dst in [('BSE3125-L01-lighting-plan-v7.json','source-verification.json'),('cad-native-v7/manifest.json','native-verification.json'),('cad-plot-v7/manifest.json','plot-verification.json')]:move(f+src,'03_Engineering/CAD/Verification/'+dst)
models=[('office-review-40s-native-v4.evo','Final/Office_Workstations.evo','office-review-40s-probe-reopened-v4.pdf','Final_Workstations.pdf'),('office-review-brightness-native-v4.evo','Final/Office_Visual_Environment.evo','office-review-brightness-probe-reopened-v4.pdf','Final_Visual_Environment.pdf'),('office-comparison-output90-core-verified-v2.evo','Comparisons/Output90_Workstations.evo','office-comparison-output90-core-reopened-v1.pdf','Output90_Workstations.pdf'),('office-comparison-output90-aux-verified-v3.evo','Comparisons/Output90_Visual_Environment.evo','office-comparison-output90-aux-reopened-v2.pdf','Output90_Visual_Environment.pdf'),('office-comparison-reflectance-core-verified-v2.evo','Comparisons/Lower_Reflectance_Workstations.evo','office-comparison-reflectance-core-reopened-v1.pdf','Lower_Reflectance_Workstations.pdf'),('office-comparison-reflectance-aux-verified-v2.evo','Comparisons/Lower_Reflectance_Visual_Environment.evo','office-comparison-reflectance-aux-reopened-v1.pdf','Lower_Reflectance_Visual_Environment.pdf')]
project_index=[]
for src,dst,raw,rawnew in models:
 move('90_Archive/Development/models/'+src,'03_Engineering/DIALux/'+dst)
 move('90_Archive/Development/models/'+raw,'03_Engineering/Native_Reports/'+rawnew)
 source=r/'03_Engineering/DIALux'/dst;submit=r/'00_Submit/DIALux'/dst;submit.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,submit);assert sha(source)==sha(submit)
 project_index.append({'engineering':source.relative_to(r).as_posix(),'submission_copy':submit.relative_to(r).as_posix(),'sha256':sha(source),'bytes':source.stat().st_size,'native_report':'03_Engineering/Native_Reports/'+rawnew,'native_report_sha256':sha(r/'03_Engineering/Native_Reports'/rawnew)})
# Collapse multi-step movements into final destinations for old evidence paths.
lookup={item['old']:item['new'] for item in records}
for key in list(lookup):
 p=lookup[key]
 while p in lookup:p=lookup[p]
 lookup[key]=p
for path,h in originals.items():assert sha(r/path)==h
tracked_moves={p:lookup[p] for p in tracked if p in lookup}
record={'status':'files relocated; active report rebuild verification pending','original_inputs':originals,'moves':records,'path_lookup':lookup,'tracked_moves':tracked_moves,'DIALux_projects':project_index,'historical_evidence_policy':'Historical records remain byte-exact. Resolve their former paths through path_lookup; active scripts use the new directories.'}
log.write_text(json.dumps(record,indent=2));(r/'03_Engineering/project-index.json').write_text(json.dumps(project_index,indent=2));print(json.dumps({'moved_files':len(records),'tracked_moves':len(tracked_moves),'native_submission_copies':len(project_index),'original_inputs_unchanged':True}))
