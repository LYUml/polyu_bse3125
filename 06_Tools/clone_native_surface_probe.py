"""Experimental clone of a native-created calculation surface in a NEW evo copy.

Geometry only. No cached results accepted. Must open, inspect, recalculate and
save with DIALux before any design use. Original and manufacturer pool unchanged.
"""
from pathlib import Path
import sys,re,json,zipfile,uuid,hashlib,copy
from read_native_archive import read,split_fields
source=Path(sys.argv[1]);target=Path(sys.argv[2]);d=read(source);objects=d['objects']
if target.exists():raise ValueError('Fresh output only')
sha=d['sha256']
with zipfile.ZipFile(source) as z:
 removed_results=[i.filename for i in z.infolist() if i.filename.startswith('Project/Results/')]
 text=z.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
name_record=next(o for o in objects.values() if o['type']=='CommonInformationPropertySet' and o['fields'].get('ObjectName')=="'Desk-01'")
rootid=int(name_record['fields']['DefinedObject'][1:])
assert objects[rootid]['type']=='CalculationGridSurface'
def refs(raw):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',raw))]
owned=set();todo=[rootid]
while todo:
 n=todo.pop()
 if n in owned:continue
 owned.add(n)
 todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in owned)
assert len(owned)<40,'Unexpectedly broad surface ownership graph'
manager=copy.deepcopy(objects[1]);next_object=int(manager['fields']['NextObjectId']);next_step=max(objects)+1
mapping={old:next_step+i for i,old in enumerate(sorted(owned))}
object_ids=sorted({int(objects[n]['fields']['ObjectId']) for n in owned if 'ObjectId' in objects[n]['fields']})
oid_map={old:next_object+i for i,old in enumerate(object_ids)}
new={}
for old in sorted(owned):
 o=copy.deepcopy(objects[old]);o['step_id']=mapping[old]
 for k,v in o['fields'].items():
  v=re.sub(r'#(\d+)',lambda m:'#'+str(mapping.get(int(m[1]),int(m[1]))),v)
  if k=='ObjectId':v=str(oid_map[int(v)])
  if k=='ObjectGuid':v="'"+str(uuid.uuid4())+"'"
  if old==name_record['step_id'] and k=='ObjectName':v="'Desk-02-probe'"
  # CoordSys origin is in the parent storey, confirmed against UI room offset.
  if old==int(objects[rootid]['fields']['LocalCoordSys'][1:]) and k=='Origin':v='(5.58, 2.58, 0.8)'
  o['fields'][k]=v
 new[o['step_id']]=o
manager['fields']['NextObjectId']=str(next_object+len(oid_map))
collections=split_fields(manager['fields']['ObjectCollections'][1:-1]);updated=[]
for c in collections:
 pair=split_fields(c[1:-1])
 if pair[0]=="'InstanceObject'":pair[1]=pair[1][:-1]+', #'+str(mapping[rootid])+')'
 updated.append('('+', '.join(pair)+')')
manager['fields']['ObjectCollections']='('+', '.join(updated)+')'
indices=split_fields(manager['fields']['ObjectIndices'][1:-1]);updated=[]
for c in indices:
 pair=split_fields(c[1:-1]);counter=objects[int(pair[0][1:])]
 if counter['fields'].get('ObjectTypeName')=="'CalculationGridSurface'" or "'CalculationGridSurface'" in counter['fields'].values():pair[1]=str(int(pair[1])+1)
 updated.append('('+', '.join(pair)+')')
manager['fields']['ObjectIndices']='('+', '.join(updated)+')'
manager['fields']['NameIndexMap']=manager['fields']['NameIndexMap'][:-1]+', ('+str(oid_map[int(objects[rootid]['fields']['ObjectId'])])+', 2))'
containers=[o for o in objects.values() if o['type']=='RelContainedInSpatialStructure' and rootid in refs(o['fields']['RelatedElements'])]
assert len(containers)==1
container=copy.deepcopy(containers[0]);container['fields']['RelatedElements']=container['fields']['RelatedElements'][:-1]+', (#'+str(mapping[rootid])+', $))'
def serialize(o):return '#'+str(o['step_id'])+' = '+o['type']+' ('+', '.join(o['fields'].values())+');'
for changed in [manager,container]:text=text.replace(changed['raw'],serialize(changed))
insert='\r\n'.join(serialize(o) for o in new.values())+'\r\n'
pos=text.index('ENDSEC;',text.index('DATA;'));text=text[:pos]+insert+text[pos:]
target.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(target,'x') as zo:
 for item in zi.infolist():
  if item.filename.startswith('Project/Results/'):continue
  zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
parsed=read(target); assert len(parsed['objects'])==len(objects)+len(new)
record={'status':'experimental geometry clone; native verification pending','source_sha256':sha,'output_sha256':parsed['sha256'],'owned_records':len(owned),'cloned_surface_step_id':mapping[rootid],'new_object_ids':oid_map,'source_unchanged':True,'removed_result_entries':removed_results,'results_present':False}
target.with_suffix('.probe.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
