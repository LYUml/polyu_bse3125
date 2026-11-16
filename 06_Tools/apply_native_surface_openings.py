"""Use a native-created CalculationSurfaceOpening graph for physical cutouts.

Creates a new experimental copy. Geometric equivalence is checked independently;
native calculation and saved/reopened coverage must still be verified.
"""
from pathlib import Path
import ast,copy,hashlib,json,re,sys,uuid,zipfile
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from read_native_archive import read,split_fields

source,template,target=map(Path,sys.argv[1:4]);assert not target.exists()
d=read(source);t=read(template);objects=copy.deepcopy(d['objects']);original=d['objects']
def refs(v):return [int(x) for x in re.findall(r'#(\d+)',v)]
def ref(v):return int(v[1:])
def real(v):
 s=format(v,'.16g');return s if '.' in s or 'e' in s.lower() else s+'.'
def loop(points):return '('+', '.join('('+', '.join(real(v) for v in p)+')' for p in points)+')'
def serialize(o):return f"#{o['step_id']} = {o['type']} ("+', '.join(o['fields'].values())+');'
def name(s):return next(objects[n]['fields']['ObjectName'][1:-1] for n in refs(s['fields']['PropertySets']) if objects[n]['type']=='CommonInformationPropertySet')
opening=next(o for o in t['objects'].values() if o['type']=='CalculationSurfaceOpening')
owned=set();pending=[opening['step_id']]
while pending:
 n=pending.pop()
 if n in owned:continue
 owned.add(n)
 for k,v in t['objects'][n]['fields'].items():
  if k not in ['RepresentedObject','DefinedObject']:pending.extend(refs(v))
assert len(owned)==8,owned
rep_id=ref(t['objects'][ref(opening['fields']['Representation'])]['fields']['RepresentationData'])
native_cutout_sign=1 if Polygon(ast.literal_eval(t['objects'][rep_id]['fields']['Points'])).exterior.is_ccw else -1
rel_template=next(o for o in t['objects'].values() if o['type']=='RelAggregates' and opening['step_id'] in refs(o['fields']['RelatedObjects']))
manager=objects[1];next_step=max(objects)+1;next_oid=int(manager['fields']['NextObjectId'])
new_instances=[];new_relations=[];manifest=[];name_entries=[]
for surface in list(objects.values()):
 if surface['type']!='CalculationGridSurface':continue
 label=name(surface)
 if not label.startswith(('Surround-','Background-','Exposed-')):continue
 rep=objects[ref(objects[ref(surface['fields']['Representation'])]['fields']['RepresentationData'])]
 poly=objects[ref(rep['fields']['MultiPolygonSurface'])]
 outers=[ast.literal_eval(v) for v in split_fields(poly['fields']['OuterLoops'][1:-1])]
 holes=[ast.literal_eval(v) for v in split_fields(poly['fields']['InnerLoops'][1:-1]) if v]
 region=unary_union([Polygon(p,[h for h in holes if Polygon(p).covers(Polygon(h).representative_point())]) for p in outers])
 assert region.is_valid
 if region.geom_type=='Polygon':
  envelope=Polygon(region.exterior);cuts=[Polygon(h) for h in region.interiors]
 else:
  envelope=box(*region.bounds);difference=envelope.difference(region)
  cuts=list(difference.geoms) if difference.geom_type=='MultiPolygon' else [difference]
  assert all(not c.interiors for c in cuts)
 rebuilt=envelope.difference(unary_union(cuts))
 error=rebuilt.symmetric_difference(region).area
 assert error<1e-7
 exterior=list(orient(envelope,sign=1).exterior.coords)[:-1]
 poly['fields']['OuterLoops']='('+loop(exterior)+')';poly['fields']['InnerLoops']='()'
 children=[];cut_records=[]
 for cut in cuts:
  # Match the orientation observed in the native-created opening.
  points=list(orient(cut,sign=native_cutout_sign).exterior.coords)[:-1]
  mapping={old:next_step+i for i,old in enumerate(sorted(owned))};next_step+=len(owned)
  oidmap={old:next_oid+i for i,old in enumerate(sorted({int(t['objects'][n]['fields']['ObjectId']) for n in owned if 'ObjectId' in t['objects'][n]['fields']}))};next_oid+=len(oidmap)
  for old in sorted(owned):
   item=copy.deepcopy(t['objects'][old]);item['step_id']=mapping[old]
   for k,v in item['fields'].items():
    v=re.sub(r'#(\d+)',lambda m:'#'+str(mapping.get(int(m[1]),int(m[1]))),v)
    if k=='ObjectId':v=str(oidmap[int(v)])
    if k=='ObjectGuid':v="'"+str(uuid.uuid4())+"'"
    if old==rep_id and k=='Points':v=loop(points)
    item['fields'][k]=v
   objects[item['step_id']]=item
  child=mapping[opening['step_id']];children.append(child);new_instances.append(child)
  name_entries.append((oidmap[int(opening['fields']['ObjectId'])],len(new_instances)))
  cut_records.append({'opening_step_id':child,'local_points_m':points,'area_m2':cut.area})
 if children:
  relation=copy.deepcopy(rel_template);relation['step_id']=next_step;next_step+=1
  relation['fields'].update(ObjectId=str(next_oid),ObjectGuid="'"+str(uuid.uuid4())+"'",RelatingObject='#'+str(surface['step_id']),RelatedObjects='('+', '.join(f'(#{n}, $)' for n in children)+')');next_oid+=1
  objects[relation['step_id']]=relation;new_relations.append(relation['step_id'])
 manifest.append({'name':label,'surface_step_id':surface['step_id'],'original_region_area_m2':region.area,'region_wkt':region.wkt,'opening_count':len(cuts),'symmetric_difference_area_m2':error,'openings':cut_records})
assert len(manifest)==36 and len(new_instances)>200
counter={'step_id':next_step,'type':'ObjectCounterIndex','fields':{'ParentId':'-1','PersistenceName':"'CalculationSurfaceOpening'"}};objects[next_step]=counter;next_step+=1
manager['fields']['ObjectIndices']=manager['fields']['ObjectIndices'][:-1]+f", (#{counter['step_id']}, {len(new_instances)}))"
manager['fields']['NameIndexMap']=manager['fields']['NameIndexMap'][:-1]+''.join(f', ({oid}, {idx})' for oid,idx in name_entries)+')'
manager['fields']['NextObjectId']=str(next_oid)
collections=[]
for entry in split_fields(manager['fields']['ObjectCollections'][1:-1]):
 pair=split_fields(entry[1:-1]);add=new_instances if pair[0]=="'InstanceObject'" else new_relations if pair[0]=="'RelAggregates'" else []
 if add:pair[1]=pair[1][:-1]+''.join(', #'+str(n) for n in add)+')'
 collections.append('('+', '.join(pair)+')')
manager['fields']['ObjectCollections']='('+', '.join(collections)+')'
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(template) as ti:
 schema=ET.fromstring(zi.read('Project/ProjectData/ProjectData.xml'));extra=ET.fromstring(ti.read('Project/ProjectData/ProjectData.xml'))
 known={e.attrib['Name']:e for e in schema}
 for e in extra:
  if e.attrib['Name'] not in known:schema.append(copy.deepcopy(e))
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
 for n,o in original.items():
  if objects[n]['fields']!=o['fields']:assert text.count(o['raw'])==1;text=text.replace(o['raw'],serialize(objects[n]))
 pos=text.index('ENDSEC;',text.index('DATA;'));text=text[:pos]+'\r\n'.join(serialize(o) for n,o in objects.items() if n not in original)+'\r\n'+text[pos:]
 with zipfile.ZipFile(target,'x') as zo:
  for item in zi.infolist():
   if item.filename=='Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):continue
   content=text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else ET.tostring(schema,encoding='utf-8',xml_declaration=True) if item.filename=='Project/ProjectData/ProjectData.xml' else zi.read(item)
   zo.writestr(item,content)
check=read(target)
assert all(n in check['objects'] for o in check['objects'].values() for v in o['fields'].values() for n in refs(re.sub(r"'(?:[^']|'')*'",'',v)))
record={'status':'native opening graph reused; calculation and persistence pending','source_sha256':d['sha256'],'native_template_sha256':t['sha256'],'output_sha256':check['sha256'],'surface_count':len(manifest),'opening_count':len(new_instances),'fixtures_and_photometry_unchanged':True,'surfaces':manifest}
target.with_suffix('.openings.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='surfaces'},indent=2))
