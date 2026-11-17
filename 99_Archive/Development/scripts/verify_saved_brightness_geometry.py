"""Independently reconstruct saved native opening regions and protect core design."""
from pathlib import Path
import ast,hashlib,json,math,re,sys
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import wkt
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
sys.path.insert(0,str(root/'06_Tools'))
from read_native_archive import read,split_fields
native=Path(sys.argv[2]) if len(sys.argv)>2 else root/'05_Calculations/models/office-brightness-openings-native-v9.evo'
d=read(native);o=d['objects'];core=read(Path(sys.argv[3]) if len(sys.argv)>3 else root/'05_Calculations/models/office-powerbalance-grid-native-v4.evo')
spec=json.loads((root/'05_Calculations/models/office-brightness-openings-probe-v8.openings.json').read_text())
proposal=read(root/'05_Calculations/models/office-brightness-openings-probe-v8.evo')['objects']
save=json.loads((data/'brightness-openings-save-v8.json').read_text())
if len(sys.argv)<=2:assert d['sha256']==save['result']['sha256']
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def obj(v):return o[int(v[1:])]
def name(s):return next(o[n]['fields']['ObjectName'][1:-1] for n in refs(s['fields']['PropertySets']) if o[n]['type']=='CommonInformationPropertySet')
def rep(s):return obj(obj(s['fields']['Representation'])['fields']['RepresentationData'])
def identity(v):
 c=obj(v)['fields']
 assert ast.literal_eval(c['Origin'])==(0.,0.,0.)
 assert [ast.literal_eval(c[a]) for a in ['XAxis','YAxis','ZAxis']]==[(1.,0.,0.),(0.,1.,0.),(0.,0.,1.)]
surfaces={name(s):s for s in o.values() if s['type']=='CalculationGridSurface'}
proposed_surfaces={next(proposal[n]['fields']['ObjectName'][1:-1] for n in refs(s['fields']['PropertySets']) if proposal[n]['type']=='CommonInformationPropertySet'):s for s in proposal.values() if s['type']=='CalculationGridSurface'}
checks=[];opening_ids=set()
for expected in spec['surfaces']:
 s=surfaces[expected['name']];r=rep(s);p=obj(r['fields']['MultiPolygonSurface'])
 original_surface=proposed_surfaces[expected['name']]
 proposed_coord=proposal[int(original_surface['fields']['LocalCoordSys'][1:])]['fields']
 native_coord=obj(s['fields']['LocalCoordSys'])['fields']
 assert {k:ast.literal_eval(v) for k,v in native_coord.items()}=={k:ast.literal_eval(v) for k,v in proposed_coord.items()}
 outers=[ast.literal_eval(v) for v in split_fields(p['fields']['OuterLoops'][1:-1]) if v]
 holes=[ast.literal_eval(v) for v in split_fields(p['fields']['InnerLoops'][1:-1]) if v]
 region=unary_union([Polygon(a,[h for h in holes if Polygon(a).covers(Polygon(h).representative_point())]) for a in outers])
 relations=[v for v in o.values() if v['type']=='RelAggregates' and v['fields']['RelatingObject']=='#'+str(s['step_id'])]
 openings=[o[n] for relation in relations for n in refs(relation['fields']['RelatedObjects']) if o[n]['type']=='CalculationSurfaceOpening']
 cuts=[]
 for opening in openings:
  opening_ids.add(opening['step_id']);identity(opening['fields']['LocalCoordSys'])
  opening_rep=rep(opening);assert opening_rep['type']=='CalculationSurfaceOpeningRepresentationData'
  assert opening_rep['fields']['HasMargin']=='False'
  cuts.append(Polygon(ast.literal_eval(opening_rep['fields']['Points'])))
 assert len(cuts)==expected['opening_count']
 effective=region.difference(unary_union(cuts));wanted=wkt.loads(expected['region_wkt'])
 error=effective.symmetric_difference(wanted).area;assert error<1e-6,(expected['name'],error)
 checks.append({'name':expected['name'],'native_opening_count':len(cuts),'parent_coordinate_system_preserved':True,'effective_area_m2':effective.area,'symmetric_difference_area_m2':error})
assert len(checks)==36 and len(opening_ids)==255

def fixtures(objects):
 result={}
 for s in objects.values():
  if s['type']=='LuminaireElement':
   c=objects[int(s['fields']['LocalCoordSys'][1:])]['fields']
   result[s['fields']['ObjectGuid']]={k:ast.literal_eval(v) for k,v in c.items()}
 return result
a,b=fixtures(core['objects']),fixtures(o);assert len(a)==len(b)==186 and a==b
fixture_steps={n for n,v in o.items() if v['type']=='LuminaireElement'}
maintenance=[v for v in o.values() if v['type']=='LuminaireMaintenancePropertySet' and int(v['fields']['DefinedObject'][1:]) in fixture_steps]
assert len(maintenance)==186 and all(abs(float(obj(v['fields']['MaintenanceInfo'])['fields']['MaintenanceFactor'])-.8)<1e-8 for v in maintenance)
physical_types={'FurnitureElement','FurniturePrototype','StoreyContourRepresentationData','ExtrudedPolygonRepresentationDataPart','PolyPoint2D','Space','Storey'}
def physical_records(objects):
 return sorted(json.dumps({'type':v['type'],'fields':{k:re.sub(r'#\d+','#REF',value) for k,value in v['fields'].items()}},sort_keys=True) for v in objects.values() if v['type'] in physical_types)
assert physical_records(core['objects'])==physical_records(o)
def photometry(objects):
 guid="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'" if len(sys.argv)>3 else "'74b47d1c-9d32-40c3-9537-d2ba85948fe1'"
 prototype=next(v for v in objects.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']==guid)
 seen=set();todo=[prototype['step_id']]
 while todo:
  n=todo.pop()
  if n in seen:continue
  seen.add(n);todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in seen)
 normalized=sorted(json.dumps({'type':objects[n]['type'],'fields':{k:re.sub(r'#\d+','#REF',v) for k,v in objects[n]['fields'].items() if k!='ObjectId'}},sort_keys=True) for n in seen)
 return len(seen),hashlib.sha256('\n'.join(normalized).encode()).hexdigest()
assert photometry(core['objects'])==photometry(o)
for i in range(1,113):
 s=surfaces[f'Desk-{i:03}'];r=rep(s)
 parts=[o[n] for n in refs(r['fields']['Parts'])]
 cylinder=next(p for p in parts if p['fields'].get('ResultType')=='.CylIllum.')
 assert abs(ast.literal_eval(obj(s['fields']['LocalCoordSys'])['fields']['Origin'])[2]+float(cylinder['fields']['HeightOffset'])-1.2)<1e-8
record={'status':'saved native geometry verified; reopened result comparison separate','native_sha256':d['sha256'],'native_path':str(native),'effective_region_count':len(checks),'native_opening_count':len(opening_ids),'maximum_symmetric_difference_area_m2':max(c['symmetric_difference_area_m2'] for c in checks),'all_186_fixture_guids_and_local_coordinate_systems_equal_core':True,'all_186_fixture_maintenance_factors':.8,'room_storey_contours_column_instances_and_prototype_geometry_match_core':True,'photometry_graph_record_count':photometry(o)[0],'photometry_graph_sha256':photometry(o)[1],'photometry_graph_matches_core':True,'all_112_cylindrical_task_heights_m':1.2,'regions':checks}
out=Path(sys.argv[1]) if len(sys.argv)>1 else data/'brightness-saved-geometry-v9.json';assert not out.exists();out.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='regions'},indent=2))
