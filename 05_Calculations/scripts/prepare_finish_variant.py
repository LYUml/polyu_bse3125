"""New native copy with an explicit white-finish design option; fresh calc required."""
from pathlib import Path
import sys,zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'06_Tools'))
from read_native_archive import read
source=Path(sys.argv[1]);target=Path(sys.argv[2]);d=read(source)
if target.exists():raise ValueError('New output required')
changes=[]
with zipfile.ZipFile(source) as z:text=z.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
for o in d['objects'].values():
 if o['type']!='MaterialParams':continue
 f=o['fields']
 if not f['InternalName'].startswith("'STF "):continue
 rho=float(f['ColorLuminance']);new=.8 if abs(rho-.7)<1e-5 else .7 if abs(rho-.5)<1e-5 else None
 if new is None:continue
 f['ColorLuminance']=str(new);f['ColorBase']=f'({new}, {new}, {new})'
 f['DisplayName']=f"'Design white finish reflectance {new}'";f['InternalName']=f['DisplayName']
 newrow=f"#{o['step_id']} = {o['type']} ("+', '.join(f.values())+');'
 assert text.count(o['raw'])==1;text=text.replace(o['raw'],newrow)
 changes.append({'material_step_id':o['step_id'],'old_reflectance':rho,'new_reflectance':new,'use':'ceiling' if new==.8 else 'walls'})
assert len(changes)==2
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(target,'x') as zo:
 for item in zi.infolist():
  if item.filename.startswith('Project/Results/'):continue
  zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
result=read(target)
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256']
record={'status':'white-finish option, native verification/calculation pending','source':str(source.resolve()),'source_sha256':d['sha256'],'output':str(target.resolve()),'output_sha256':result['sha256'],'changes':changes,'assumption':'Matte white ceiling rho=0.80 and light walls rho=0.70 specified as design finishes, floor rho=0.20 and columns rho=0.40 retained. No fixture geometry/photometry changed.','cached_results_removed':True,'source_unchanged':True}
target.with_suffix('.design.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
