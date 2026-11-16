"""Instantiate proposed desks from an already native-validated surface template.

Always creates a new experimental copy, removes cached results and requires
native calculation/save/reopen verification. No illumination is synthesized.
"""
from pathlib import Path
import sys,re,json,zipfile,uuid,hashlib,copy
from read_native_archive import read,split_fields
source,furniture,target=map(Path,sys.argv[1:4])
assert not target.exists()
d=read(source);objects=d['objects'];proposal=json.loads(furniture.read_text())
desks=proposal['desks']
assert len(desks)==112 and len({x['id'] for x in desks})==112
def refs(s):return [int(x) for x in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',s))]
def serialize(o):return f"#{o['step_id']} = {o['type']} ("+', '.join(o['fields'].values())+');'
name=next(o for o in objects.values() if o['type']=='CommonInformationPropertySet' and o['fields'].get('ObjectName')=="'Desk-01'")
rootid=int(name['fields']['DefinedObject'][1:]);template=objects[rootid]
assert template['type']=='CalculationGridSurface'
coordid=int(template['fields']['LocalCoordSys'][1:])
owned=set();todo=[rootid]
while todo:
 n=todo.pop()
 if n in owned:continue
 owned.add(n);todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in owned)
assert len(owned)==17
manager=copy.deepcopy(objects[1]);assert manager['type']=='ObjectManager'
next_oid=int(manager['fields']['NextObjectId']);next_step=max(objects)+1
containers=[o for o in objects.values() if o['type']=='RelContainedInSpatialStructure' and rootid in refs(o['fields']['RelatedElements'])]
assert len(containers)==1
container=copy.deepcopy(containers[0]);new=[];roots=[];name_indices=[];manifest=[]
object_ids=sorted({int(objects[n]['fields']['ObjectId']) for n in owned if 'ObjectId' in objects[n]['fields']})
for i,desk in enumerate(desks):
 assert desk['size_m']==[1.6,.8] and desk['centre_m'][2]==.8
 mapping={n:next_step+j for j,n in enumerate(sorted(owned))};next_step+=len(owned)
 oidmap={n:next_oid+j for j,n in enumerate(object_ids)};next_oid+=len(object_ids)
 for old in sorted(owned):
  o=copy.deepcopy(objects[old]);o['step_id']=mapping[old]
  for k,v in o['fields'].items():
   v=re.sub(r'#(\d+)',lambda m:'#'+str(mapping.get(int(m[1]),int(m[1]))),v)
   if k=='ObjectId':v=str(oidmap[int(v)])
   if k=='ObjectGuid':v="'"+str(uuid.uuid4())+"'"
   if old==name['step_id'] and k=='ObjectName':v="'"+desk['id']+"'"
   if old==coordid and k=='Origin':v='('+', '.join(format(x,'.12g') for x in desk['centre_m'])+')'
   o['fields'][k]=v
  new.append(o)
 roots.append(mapping[rootid]);name_indices.append((oidmap[int(template['fields']['ObjectId'])],i+3))
 manifest.append({'name':desk['id'],'surface_step_id':mapping[rootid],'parent_storey_origin_m':desk['centre_m'],'ugr_eye_height_m':1.2})
manager['fields']['NextObjectId']=str(next_oid)
collections=[]
for c in split_fields(manager['fields']['ObjectCollections'][1:-1]):
 pair=split_fields(c[1:-1])
 if pair[0]=="'InstanceObject'":pair[1]=pair[1][:-1]+''.join(', #'+str(n) for n in roots)+')'
 collections.append('('+', '.join(pair)+')')
manager['fields']['ObjectCollections']='('+', '.join(collections)+')'
indices=[];updated_counter=0
for c in split_fields(manager['fields']['ObjectIndices'][1:-1]):
 pair=split_fields(c[1:-1]);counter=objects[int(pair[0][1:])]
 if "'CalculationGridSurface'" in counter['fields'].values():pair[1]=str(int(pair[1])+len(desks));updated_counter+=1
 indices.append('('+', '.join(pair)+')')
assert updated_counter==1
manager['fields']['ObjectIndices']='('+', '.join(indices)+')'
manager['fields']['NameIndexMap']=manager['fields']['NameIndexMap'][:-1]+''.join(f', ({oid}, {idx})' for oid,idx in name_indices)+')'
container['fields']['RelatedElements']=container['fields']['RelatedElements'][:-1]+''.join(f', (#{n}, $)' for n in roots)+')'
with zipfile.ZipFile(source) as zi:
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
 for changed in [manager,container]:assert text.count(changed['raw'])==1;text=text.replace(changed['raw'],serialize(changed))
 pos=text.index('ENDSEC;',text.index('DATA;'));text=text[:pos]+'\r\n'.join(map(serialize,new))+'\r\n'+text[pos:]
 with zipfile.ZipFile(target,'x') as zo:
  for item in zi.infolist():
   if item.filename.startswith('Project/Results/'):continue
   zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
check=read(target);allobjects=check['objects'];guids=[]
for o in allobjects.values():
 for v in o['fields'].values():assert all(n in allobjects for n in refs(v))
 if 'ObjectGuid' in o['fields']:guids.append(o['fields']['ObjectGuid'])
assert len(guids)==len(set(guids))
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256']
record={'status':'experimental task geometry; native acceptance pending','source_sha256':d['sha256'],'proposal_sha256':hashlib.sha256(furniture.read_bytes()).hexdigest(),'output_sha256':check['sha256'],'cloned_record_count':len(new),'added_task_count':len(desks),'diagnostic_surfaces_retained':['Desk-01','Desk-02-probe'],'cached_results_removed':True,'source_unchanged':True,'surfaces':manifest}
target.with_suffix('.tasks.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='surfaces'},indent=2))
