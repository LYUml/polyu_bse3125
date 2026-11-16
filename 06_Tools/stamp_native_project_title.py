"""Change project title only in a new copy; preserve every result stream exactly."""
from pathlib import Path
import copy,hashlib,json,sys,zipfile
from read_native_archive import read
source,target=map(Path,sys.argv[1:3]);assert not target.exists();d=read(source)
item=next(o for o in d['objects'].values() if o['type']=='ProjectInfoPropertySet')
assert item['fields']['ProjectName']=="'DIALux Agent Toolkit'"
fields=dict(item['fields']);fields['ProjectName']="'BSE3125 - Open-plan Office'"
row=f"#{item['step_id']} = {item['type']} ("+', '.join(fields.values())+');'
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(target,'x') as zo:
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig');assert text.count(item['raw'])==1;text=text.replace(item['raw'],row)
 for entry in zi.infolist():zo.writestr(copy.copy(entry),text.encode('utf-8-sig') if entry.filename=='Project/ProjectData/ProjectData.dat' else zi.read(entry.filename))
with zipfile.ZipFile(source) as a,zipfile.ZipFile(target) as b:
 assert a.namelist()==b.namelist()
 changed=[n for n in a.namelist() if hashlib.sha256(a.read(n)).digest()!=hashlib.sha256(b.read(n)).digest()]
 assert changed==['Project/ProjectData/ProjectData.dat']
actual=read(target);assert len(actual['objects'])==len(d['objects'])
assert [n for n in d['objects'] if d['objects'][n]['fields']!=actual['objects'][n]['fields']]==[item['step_id']]
record={'status':'title-only new copy; native reopen/export required','source_sha256':d['sha256'],'output_sha256':actual['sha256'],'changed_record_type':'ProjectInfoPropertySet','changed_field':'ProjectName','all_other_records_and_all_results_streams_unchanged':True}
target.with_suffix('.title.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
