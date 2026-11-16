"""Proposed desks: explicit design assumptions, clipped against measured geometry."""
from pathlib import Path
import json,hashlib
from shapely.geometry import Polygon,box
root=Path(__file__).resolve().parents[2];p=root/'05_Calculations/data/room-v1.json'
room=json.loads(p.read_text());office=Polygon(room['contour'])
columns=[box(o['center_m'][0]-o['size_m'][0]/2,o['center_m'][1]-o['size_m'][1]/2,o['center_m'][0]+o['size_m'][0]/2,o['center_m'][1]+o['size_m'][1]/2) for o in room['obstacles']]
centres=[(3.58+7.2*i,y) for y in [2.98,7.78,12.58,18.58] for i in range(6)]
centres += [(x,y) for y in [23.38,27.58] for x in [34.58,40.58]]
benches=[];desks=[]
for n,(x,y) in enumerate(centres,1):
 poly=box(x-1.6,y-.8,x+1.6,y+.8)
 assert office.covers(poly.buffer(.9,join_style=2)),f'Wall clearance bench {n}'
 assert all(poly.distance(c)>=.9 for c in columns),f'Column clearance bench {n}'
 benches.append({'id':f'B{n:02}','centre_m':[round(x,6),round(y,6)],'size_m':[3.2,1.6],'wall_clearance_m':poly.distance(office.boundary),'minimum_column_clearance_m':min(poly.distance(c) for c in columns)})
 for dx,dy in [(-.8,-.4),(.8,-.4),(-.8,.4),(.8,.4)]:
  cx,cy=round(x+dx,6),round(y+dy,6)
  desks.append({'id':f'Desk-{len(desks)+1:03}','bench_id':f'B{n:02}','centre_m':[cx,cy,.8],'size_m':[1.6,.8],'polygon_m':[[cx-.8,cy-.4],[cx+.8,cy-.4],[cx+.8,cy+.4],[cx-.8,cy+.4]],'ugr_eye_height_m':1.2})
polys=[box(x-1.6,y-.8,x+1.6,y+.8) for x,y in centres]
assert all(a.distance(b)>=1.8 for i,a in enumerate(polys) for b in polys[i+1:])
out=root/'05_Calculations/data/furniture-proposal-v1.json'
assert not out.exists()
out.write_text(json.dumps({'status':'proposed furniture design; not a supplied architectural arrangement or simulated result','basis':'28 four-person back-to-back benches; 112 desks of 1.6 x 0.8 m at 0.8 m height. Reserve >=0.9 m around bench footprints to walls/columns and >=1.8 m between benches. These are explicit planning assumptions, not a certified accessibility/fire escape review. Seats face toward opposite bench rows. Desk surfaces are the intended paperwork task areas.','coordinate_frame':'drawing-origin-subtracted design metres; native room-frame conversion must be verified separately','geometry_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'benches':benches,'desks':desks,'desk_count':len(desks),'task_area_m2':len(desks)*1.6*.8},indent=2),encoding='utf-8')
print(json.dumps({'benches':len(benches),'desks':len(desks),'task_area_m2':len(desks)*1.6*.8,'output':str(out)},indent=2))
