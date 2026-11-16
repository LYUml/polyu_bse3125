"""Check all source-linked native column footprints through their prototype graph."""
from pathlib import Path
import ast,json,re,sys
from shapely.geometry import Polygon,box
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'06_Tools'))
from read_native_archive import read
d=read(root/'05_Calculations/models/office-powerbalance-grid-native-v4.evo');o=d['objects']
expected=json.loads((root/'05_Calculations/data/room-v1.json').read_text())['obstacles']
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',v)]
def obj(v):return o[int(v[1:])]
def coord(v):
 c=obj(v)['fields'];assert ast.literal_eval(c['XAxis'])==(1.,0.,0.) and ast.literal_eval(c['YAxis'])==(0.,1.,0.) and ast.literal_eval(c['ZAxis'])==(0.,0.,1.)
 return ast.literal_eval(c['Origin'])
observed=[]
for column in expected:
 s=next(s for s in o.values() if s['type']=='FurnitureElement' and any(o[n]['fields'].get('ObjectName')=="'"+column['name']+"'" for n in refs(s['fields']['PropertySets'])))
 origin=coord(s['fields']['LocalCoordSys'])
 container=next(v for v in o.values() if v['type']=='RelContainedInSpatialStructure' and s['step_id'] in refs(v['fields']['RelatedElements']))
 parent=obj(container['fields']['RelatingStructure']);assert parent['type']=='Storey'
 assert coord(parent['fields']['LocalCoordSys'])==(0.,0.,0.)
 relation=next(v for v in o.values() if v['type']=='RelDefinesByPrototype' and s['step_id'] in refs(v['fields']['RelatedObjects']))
 proto=obj(relation['fields']['RelatingPrototype']);rep=obj(obj(proto['fields']['Representation'])['fields']['RepresentationData'])
 assert ast.literal_eval(rep['fields']['OperandScale'])==(1.,1.,1.)
 parts=[o[n] for n in refs(rep['fields']['Parts'])];assert len(parts)==1
 part=parts[0];assert part['type']=='ExtrudedPolygonRepresentationDataPart'
 assert coord(part['fields']['LocalCoordSys'])==(0.,0.,0.) and part['fields']['Alignment']=='.Bottom.'
 points=[ast.literal_eval(o[n]['fields']['Position']) for n in refs(part['fields']['PolyPoints'])]
 actual=Polygon([(origin[0]+x,origin[1]+y) for x,y in points])
 x,y=column['center_m'];w,h,height=column['size_m'];wanted=box(x-w/2,y-h/2,x+w/2,y+h/2)
 error=actual.hausdorff_distance(wanted)
 coordinate_error=max(abs(a-b) for a,b in zip(actual.bounds,wanted.bounds))
 # STF stores millimetre-rounded X/Y independently; the 2D corner distance
 # may exceed 0.51 mm while each component remains within that tolerance.
 assert coordinate_error<=.00051 and error<=2**.5*.00051 and abs(float(part['fields']['Height'])-height)<1e-8 and origin[2]==0,(column['name'],error,origin,points,part['fields']['Height'],height)
 observed.append({'name':column['name'],'native_instance_step_id':s['step_id'],'native_parent_type':parent['type'],'native_origin_m':origin,'footprint_m':list(actual.exterior.coords),'height_m':float(part['fields']['Height']),'maximum_boundary_deviation_m':error,'maximum_coordinate_deviation_m':coordinate_error})
assert len(observed)==8
record={'status':'all eight source-linked columns verified in saved core native model','native_sha256':d['sha256'],'column_count':8,'maximum_boundary_deviation_m':max(v['maximum_boundary_deviation_m'] for v in observed),'coordinate_tolerance_m':.00051,'euclidean_tolerance_m':2**.5*.00051,'scope':'Column geometry and coordinate hierarchy; surface reflectance and calculation-region exclusions are separate checks.','columns':observed}
out=root/'05_Calculations/data/native-column-verification-v1.json';assert not out.exists()
out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='columns'},indent=2))
