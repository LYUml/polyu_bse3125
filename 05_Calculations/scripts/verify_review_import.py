"""Verify the native product replacement preserves all physical fixture positions."""
from pathlib import Path
import ast,hashlib,json,re,sys
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'06_Tools'))
from read_native_archive import read
source=root/'05_Calculations/models/office-powerbalance-grid-native-v4.evo'
target=root/'05_Calculations/models/office-review-40s-import-v2.evo'
a,b=read(source),read(target);o=b['objects']
def refs(v):return [int(x) for x in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def fixtures(objects):
 return {v['fields']['ObjectGuid']:(v,objects[int(v['fields']['LocalCoordSys'][1:])]['fields']) for v in objects.values() if v['type']=='LuminaireElement'}
x,y=fixtures(a['objects']),fixtures(o);assert len(x)==len(y)==186 and set(x)==set(y)
for guid in x:
 assert x[guid][0]['fields']['ObjectId']==y[guid][0]['fields']['ObjectId']
 assert {k:ast.literal_eval(v) for k,v in x[guid][1].items()}=={k:ast.literal_eval(v) for k,v in y[guid][1].items()}
ids={v[0]['step_id'] for v in y.values()}
relations=[v for v in o.values() if v['type']=='RelDefinesByPrototype' and ids.intersection(refs(v['fields']['RelatedObjects']))]
assert len(relations)==1 and ids.issubset(refs(relations[0]['fields']['RelatedObjects']))
prototype=o[int(relations[0]['fields']['RelatingPrototype'][1:])];assert prototype['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'"
seen=set();pending=[prototype['step_id']]
while pending:
 n=pending.pop()
 if n in seen:continue
 seen.add(n);pending.extend(r for v in o[n]['fields'].values() for r in refs(v) if r not in seen)
assert any('910505103638' in v for n in seen for v in o[n]['fields'].values())
normalized=sorted(json.dumps({'type':o[n]['type'],'fields':{k:re.sub(r'#\d+','#REF',v) for k,v in o[n]['fields'].items()}},sort_keys=True) for n in seen)
maintenance=[v for v in o.values() if v['type']=='LuminaireMaintenancePropertySet' and int(v['fields']['DefinedObject'][1:]) in ids]
assert len(maintenance)==186 and all(abs(float(o[int(v['fields']['MaintenanceInfo'][1:])]['fields']['MaintenanceFactor'])-.8)<1e-8 for v in maintenance)
record={'status':'native replacement verified before calculation; result acceptance pending','original_native_sha256':a['sha256'],'imported_native_sha256':b['sha256'],'all_186_guids_object_ids_and_local_coordinate_systems_preserved':True,'all_186_maintenance_factors':.8,'all_186_use_new_manufacturer_prototype':True,'manufacturer_order_code':'910505103638','prototype_guid':prototype['fields']['ObjectGuid'][1:-1],'prototype_graph_record_count':len(seen),'prototype_graph_sha256':hashlib.sha256('\n'.join(normalized).encode()).hexdigest(),'native_ULD_import_evidence':'review-40s-import-v1.json','manufacturer_ULD_sha256':'ef4350f49fb80580ef6b3c6cbcafcedb15ef794fbc0d2aad67f8a218db21bcc5'}
out=root/'05_Calculations/data/review-40s-import-verification-v2.json';assert not out.exists();out.write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
