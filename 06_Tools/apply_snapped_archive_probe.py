"""Experimental new-copy fixture coordinate update; actual native verification required."""
from pathlib import Path
import sys,json,zipfile,hashlib
from read_native_archive import read
source,plan,target=map(Path,sys.argv[1:4]);assert not target.exists()
d=read(source);p=json.loads(plan.read_text());objects=d['objects']
fixtures={o['fields']['ObjectGuid'][1:-1]:o for o in objects.values() if o['type']=='LuminaireElement'}
assert len(fixtures)==p['fixture_count']==186
def real(v):
 s=format(v,'.16g')
 return s if '.' in s or 'e' in s.lower() else s+'.'
with zipfile.ZipFile(source) as z:text=z.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
for f in p['fixtures']:
 o=fixtures[f['native_object_guid']];assert int(o['fields']['ObjectId'])==f['native_object_id']
 c=objects[int(o['fields']['LocalCoordSys'][1:])];assert c['type']=='CoordSys3D'
 fields=dict(c['fields']);fields['Origin']='('+', '.join(real(v) for v in f['local_origin_m'])+')'
 row=f"#{c['step_id']} = CoordSys3D ("+', '.join(fields.values())+');'
 assert text.count(c['raw'])==1;text=text.replace(c['raw'],row)
omitted=[]
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(target,'x') as zo:
 for item in zi.infolist():
  if item.filename=='Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):
   omitted.append(item.filename);continue
  zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
check=read(target);assert len(check['objects'])==len(objects)
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256']
record={'status':'experimental fixture geometry; native report and persistence verification pending','source_sha256':d['sha256'],'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'output_sha256':check['sha256'],'modified_fixture_count':len(fixtures),'omitted_cache_entries':omitted,'source_unchanged':True,'photometry_unchanged':True,'synthetic_results':False}
target.with_suffix('.layout-probe.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
