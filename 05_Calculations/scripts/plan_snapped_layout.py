"""Map each native fixture to a source CAD full ceiling tile. Geometry only."""
from pathlib import Path
import sys,json,re,hashlib,math
from shapely.geometry import Polygon,box
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'06_Tools'))
from read_native_archive import read,split_fields
source=Path(sys.argv[1]);out=Path(sys.argv[2]);assert not out.exists()
d=read(source);objects=d['objects'];data=root/'05_Calculations/data'
tiles=json.loads((data/'ceiling-candidates-v1.json').read_text())
r=json.loads((data/'room-v1.json').read_text());room=Polygon(r['contour'])
columns=[box(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2,c['center_m'][0]+c['size_m'][0]/2,c['center_m'][1]+c['size_m'][1]/2) for c in r['obstacles']]
valid=[]
for t in tiles['tiles']:
 x,y=t['center_m'];envelope=box(x-.3,y-.3,x+.3,y+.3)
 if room.buffer(-.3).covers(envelope) and all(envelope.distance(c)>=.3 for c in columns):valid.append(t)
groups=[o for o in objects.values() if o['type']=='LuminaireArrangement'];assert len(groups)==1
g=groups[0];coord=objects[int(g['fields']['LocalCoordSys'][1:])]['fields']
assert coord['XAxis']=='(1., 0., 0.)' and coord['YAxis']=='(0., 1., 0.)'
origin=[float(x) for x in split_fields(coord['Origin'][1:-1])]
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',v)]
aggregates=[o for o in objects.values() if o['type']=='RelAggregates' and o['fields'].get('RelatingObject')=='#'+str(g['step_id'])]
assert len(aggregates)==1
related=refs(aggregates[0]['fields']['RelatedObjects'])
fixture_ids=[n for n in related if objects[n]['type']=='LuminaireElement']
assert len(fixture_ids)==sum(o['type']=='LuminaireElement' for o in objects.values())==186
used=set();fixtures=[]
for n in fixture_ids:
 f=objects[n];c=objects[int(f['fields']['LocalCoordSys'][1:])]
 local=[float(x) for x in split_fields(c['fields']['Origin'][1:-1])]
 old=[a+b for a,b in zip(origin,local)]
 choices=[t for t in valid if t['handle'] not in used]
 tile=min(choices,key=lambda t:math.dist(old[:2],t['center_m']))
 distance=math.dist(old[:2],tile['center_m']);assert distance<1.,f'Unexpected displacement {distance}'
 used.add(tile['handle']);new=[*tile['center_m'],old[2]]
 fixtures.append({'id':f'L{len(fixtures)+1:03}','native_object_guid':f['fields']['ObjectGuid'][1:-1],'native_object_id':int(f['fields']['ObjectId']),'source_tile_handle':tile['handle'],'product_order_code':'910505103630','position_m':new,'original_position_m':old,'displacement_m':distance,'local_coord_step_id':c['step_id'],'local_origin_m':[a-b for a,b in zip(new,origin)],'envelope_m':[.6,.6]})
out.write_text(json.dumps({'status':'proposed snapped geometry; native installation and calculation pending','source_native_sha256':d['sha256'],'source_native_path':str(source.resolve()),'source_dxf_sha256':tiles['source_dxf_sha256'],'coordinate_frame':'design/storey coordinates in metres, drawing origin subtracted','ceiling_elevation_m':2.8,'native_reference_height_m':origin[2],'height_note':'Native mounting reference is above the ceiling plane because recessed product geometry extends into the plenum. Verify emitting surface against native section before final acceptance.','fixture_count':len(fixtures),'rated_input_W_each':20,'native_photometry_input_W_each':19.8,'conservative_connected_input_W':len(fixtures)*20,'conservative_lpd_using_1022_m2_W_m2':len(fixtures)*20/1022,'fixture_footprint_clearance_m':.3,'fixtures':fixtures},indent=2),encoding='utf-8')
print(json.dumps({'fixture_count':len(fixtures),'max_displacement_m':max(f['displacement_m'] for f in fixtures),'output':str(out)},indent=2))
