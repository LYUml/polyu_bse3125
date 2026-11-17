"""Plan full-tile lighting candidates from explicit source CAD cells.

No photometric performance is inferred. Candidates are not native placements.
"""
from pathlib import Path
import json,hashlib,collections
from shapely.geometry import Polygon,box
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'05_Calculations/data'
cad=json.loads((DATA/'cad_entities.json').read_text())
spec=json.loads((DATA/'room-v1.json').read_text()); room=Polygon(spec['contour'])
column_shapes=[box(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2,c['center_m'][0]+c['size_m'][0]/2,c['center_m'][1]+c['size_m'][1]/2) for c in spec['obstacles']]
tiles=[]
for e in cad['entities']:
 if e['type']!='LWPOLYLINE' or e['layer']!='Ceiling Grid' or not e['closed'] or len(e['points'])!=4:continue
 p=Polygon(e['points']); x0,y0,x1,y1=p.bounds
 if abs(x1-x0-.6)>1e-5 or abs(y1-y0-.6)>1e-5 or abs(p.area-.36)>1e-5:continue
 tiles.append({'handle':e['handle'],'center_m':[(x0+x1)/2,(y0+y1)/2],'polygon_m':e['points']})
origin=[min(t['center_m'][0] for t in tiles),min(t['center_m'][1] for t in tiles)]
for t in tiles:
 t['cell']=[round((t['center_m'][k]-origin[k])/.6) for k in (0,1)]
 assert all(abs(origin[k]+.6*t['cell'][k]-t['center_m'][k])<1e-5 for k in (0,1))
assert len({tuple(t['cell']) for t in tiles})==len(tiles)
candidates=[]
for ox in range(4):
 for oy in range(4):
  chosen=[]
  for t in tiles:
   if t['cell'][0]%4!=ox or t['cell'][1]%4!=oy:continue
   x,y=t['center_m']; footprint=box(x-.3,y-.3,x+.3,y+.3)
   if not room.buffer(-.3).covers(footprint):continue
   if any(footprint.distance(c)<.3 for c in column_shapes):continue
   chosen.append(t)
  candidates.append({'id':f'TILE24-{ox}{oy}','offset_cell':[ox,oy],'spacing_m':[2.4,2.4],'fixture_count':len(chosen),'input_power_if_32W_W':32*len(chosen),'lpd_using_annotated_1022_m2_W_m2':32*len(chosen)/1022,'fixtures':[{'id':f'L{i+1:03d}','source_tile_handle':t['handle'],'position_m':[*t['center_m'],2.8],'envelope_m':[.6,.6]} for i,t in enumerate(sorted(chosen,key=lambda t:(t['center_m'][1],t['center_m'][0])))],'native_placement_verified':False,'simulation_verified':False})
result={'status':'source-linked candidate geometry only','grid_origin_m':origin,'tile_size_m':[.6,.6],'selected_full_tile_count':len(tiles),'excluded_source_entities':'All non-full-square Ceiling Grid entities (cut fragments and boundary lines) are explicitly excluded; no room boundary inferred from grid.','source_dxf_sha256':json.loads((DATA/'source_manifest.json').read_text())['converted_dxf_sha256'],'tiles':tiles,'candidates':candidates}
(DATA/'ceiling-candidates-v1.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
im=Image.new('RGB',(1600,1100),'white');d=ImageDraw.Draw(im)
def px(p):return (round(70+p[0]*32),round(1010-p[1]*32))
for t in tiles:d.polygon([px(p) for p in t['polygon_m']],outline='#dce3ea')
d.line([px(p) for p in spec['contour']+[spec['contour'][0]]],fill='black',width=3)
candidate=next(c for c in candidates if c['id']=='TILE24-21')
for c in column_shapes:d.polygon([px(p) for p in c.exterior.coords],fill='#777777')
for f in candidate['fixtures']:
 x,y,_=f['position_m'];d.rectangle([px([x-.3,y+.3]),px([x+.3,y-.3])],fill='#227bb0')
d.text((70,20),f"{candidate['id']} - {candidate['fixture_count']} candidate luminaires; geometry only, not simulated or accepted",fill='black')
im.save(DATA/'ceiling-candidate-preview.png')
print(json.dumps({'selected_full_tiles':len(tiles),'grid_origin_m':origin,'candidates':[{k:v for k,v in c.items() if k!='fixtures'} for c in candidates]},indent=2))
