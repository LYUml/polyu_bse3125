"""Prepare a new native copy for product/robustness review; no results invented."""
from pathlib import Path
import sys,zipfile,json,hashlib
from read_native_archive import read
source,target=map(Path,sys.argv[1:3]);assert not target.exists()
d=read(source)
name=next(o for o in d['objects'].values() if o['type']=='CommonInformationPropertySet' and o['fields']['ObjectName']=="'DIALux Agent Toolkit'")
fields=dict(name['fields']);fields['ObjectName']="'BSE3125 - Open-plan Office'"
row=f"#{name['step_id']} = CommonInformationPropertySet ("+', '.join(fields.values())+');'
with zipfile.ZipFile(source) as zi:
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig');assert text.count(name['raw'])==1;text=text.replace(name['raw'],row)
 with zipfile.ZipFile(target,'x') as zo:
  for item in zi.infolist():
   if item.filename=='Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):continue
   zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
record={'status':'new review copy, native product import and recalculation pending','source_sha256':d['sha256'],'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'changes':['Project display name','Cached scene/results omitted'],'physical_design_and_existing_photometry_unchanged':True}
target.with_suffix('.source.json').write_text(json.dumps(record,indent=2));print(json.dumps(record))
