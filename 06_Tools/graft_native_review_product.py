"""Graft the actual imported product graph into an auxiliary new-copy model.

Photometry is copied verbatim except STEP references and object identifiers.
Native open/recalculate/save/reopen verification is mandatory afterwards.
"""
from pathlib import Path
import copy,hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
from read_native_archive import read,split_fields
base,imported,target=map(Path,sys.argv[1:4]);assert not target.exists()
a,b=read(base),read(imported);o=copy.deepcopy(a['objects']);source=b['objects']
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def row(item):return f"#{item['step_id']} = {item['type']} ("+', '.join(item['fields'].values())+');'
prototype=next(v for v in source.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'")
seen=set();todo=[prototype['step_id']]
while todo:
 n=todo.pop()
 if n in seen:continue
 seen.add(n);todo.extend(r for v in source[n]['fields'].values() for r in refs(v) if r not in seen)
assert len(seen)==63
start=max(o)+1;mapping={n:start+i for i,n in enumerate(sorted(seen))}
manager=o[1];first_oid=int(manager['fields']['NextObjectId'])
old_ids=sorted({int(source[n]['fields']['ObjectId']) for n in seen if 'ObjectId' in source[n]['fields']});oid_map={n:first_oid+i for i,n in enumerate(old_ids)}
for n in sorted(seen):
 item=copy.deepcopy(source[n]);item['step_id']=mapping[n]
 for k,v in item['fields'].items():
  if k=='ObjectId':v=str(oid_map[int(v)])
  else:v=re.sub(r'#(\d+)',lambda m:'#'+str(mapping[int(m[1])]),v)
  item['fields'][k]=v
 o[item['step_id']]=item
fixture_ids={n for n,v in o.items() if v['type']=='LuminaireElement'};assert len(fixture_ids)==186
relations=[v for v in o.values() if v['type']=='RelDefinesByPrototype' and fixture_ids.intersection(refs(v['fields']['RelatedObjects']))]
assert len(relations)==1 and fixture_ids.issubset(refs(relations[0]['fields']['RelatedObjects']))
relations[0]['fields']['RelatingPrototype']='#'+str(mapping[prototype['step_id']])
collections=[]
for entry in split_fields(manager['fields']['ObjectCollections'][1:-1]):
 pair=split_fields(entry[1:-1])
 if pair[0]=="'ProductPrototype'":pair[1]=pair[1][:-1]+', #'+str(mapping[prototype['step_id']])+')'
 collections.append('('+', '.join(pair)+')')
manager['fields']['ObjectCollections']='('+', '.join(collections)+')';manager['fields']['NextObjectId']=str(first_oid+len(old_ids))
name=next(v for v in o.values() if v['type']=='CommonInformationPropertySet' and v['fields']['ObjectName']=="'DIALux Agent Toolkit'");name['fields']['ObjectName']="'BSE3125 - Open-plan Office'"
def canonical(objects,ids):
 return sorted(json.dumps({'type':objects[n]['type'],'fields':{k:re.sub(r'#\d+','#REF',v) for k,v in objects[n]['fields'].items() if k!='ObjectId'}},sort_keys=True) for n in ids)
assert canonical(source,seen)==canonical(o,set(mapping.values()))
with zipfile.ZipFile(base) as zi,zipfile.ZipFile(imported) as si:
 schema=ET.fromstring(zi.read('Project/ProjectData/ProjectData.xml'));known={e.attrib['Name'] for e in schema}
 assert all(source[n]['type'] in known for n in seen)
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
 for n,item in a['objects'].items():
  if item['fields']!=o[n]['fields']:assert text.count(item['raw'])==1;text=text.replace(item['raw'],row(o[n]))
 pos=text.index('ENDSEC;',text.index('DATA;'));text=text[:pos]+'\r\n'.join(row(o[n]) for n in mapping.values())+'\r\n'+text[pos:]
 with zipfile.ZipFile(target,'x') as zo:
  for item in zi.infolist():
   if item.filename=='Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):continue
   zo.writestr(copy.copy(item),text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
  for item in si.infolist():
   if item.filename.startswith('Project/ProductImage/') and item.file_size:
    if item.filename in zi.namelist():assert zi.read(item.filename)==si.read(item.filename)
    else:zo.writestr(copy.copy(item),si.read(item.filename))
check=read(target);assert all(n in check['objects'] for v in check['objects'].values() for value in v['fields'].values() for n in refs(value))
record={'status':'actual imported product graph grafted; native validation pending','base_sha256':a['sha256'],'imported_native_sha256':b['sha256'],'output_sha256':check['sha256'],'copied_graph_record_count':63,'semantic_graph_sha256':hashlib.sha256('\n'.join(canonical(source,seen)).encode()).hexdigest(),'all_186_fixtures_relinked':True,'fixture_and_calculation_region_geometry_unchanged':True,'manufacturer_order_code':'910505103638','native_imported_prototype_guid':prototype['fields']['ObjectGuid'][1:-1]}
target.with_suffix('.product.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
