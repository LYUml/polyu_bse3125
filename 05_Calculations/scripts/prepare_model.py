"""Construct source-linked first model; explicitly record unresolved area discrepancy."""
from pathlib import Path
import json,sys,hashlib
from shapely.geometry import Polygon,box
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'05_Calculations/data'
cad=json.loads((DATA/'cad_entities.json').read_text())
contour=[[.18,.18],[44.82,.18],[44.82,29.8],[30.863333,29.8],[30.863333,20.67],[.18,20.67]]
room=Polygon(contour)
handles=['3A66','4085','4086','4087','408A','408F','4091','4093']
columns=[]; evidence=[]
for h in handles:
 e=next(e for e in cad['entities'] if e['handle']==h)
 p=Polygon(e['points']).intersection(room)
 if p.is_empty or p.area<1e-6:continue
 x0,y0,x1,y1=p.bounds
 assert abs(p.area-(x1-x0)*(y1-y0))<1e-5
 # 0.1 micrometre inset prevents floating-point box reconstruction crossing walls.
 columns.append({'name':'Column-'+h,'center_m':[(x0+x1)/2,(y0+y1)/2],'size_m':[x1-x0-2e-7,y1-y0-2e-7,2.8],'reflectance_pct':40})
 evidence.append({'source_handle':h,'source_polygon_m':e['points'],'model_clipped_polygon_m':list(p.exterior.coords),'area_m2':p.area})
spec={'name':'Open plan office','units':'m','contour':contour,'height_m':2.8,'workplane_m':.8,'maintenance_factor':.8,'ceiling_reflectance_pct':70,'wall_reflectance_pct':50,'floor_reflectance_pct':20,'obstacles':columns,'assumptions':[
'Interior L-shaped boundary interpreted from supplied ARCH lines 3E42,3E43,3D31,4053,4054,4097,4098,4052,4099,409A. Door opening to core closed at office boundary for electric-light-only model.',
'Coordinates transformed from native DXF INSUNITS=4 with WCS metre origin [64.34593225182503,15.92558365525945].',
'Ceiling height 2.8 m, workplane 0.8 m, MF 0.80 and reflectances 70/50/20 percent are adopted design assumptions, not surveyed data.',
'Column footprints follow source handles with edge columns clipped to office interior. Column reflectance fixed at 40 percent by supported STF box adapter.',
'No office furniture or facade opening dimensions supplied. Initial electric-light-only calculation; no daylight credit. Task-area and glare evaluation remain pending.',
'Boundary area 1042.098 m2 differs from source annotation 1022 m2. Retain both; investigate before final area/LPD adoption.']}
(DATA/'room-v1.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
(DATA/'geometry-review.json').write_text(json.dumps({'status':'initial interpretation; native check pending','drawing_origin_wcs_m':cad['drawing_origin_wcs_m'],'room_area_before_columns_m2':room.area,'column_area_m2':sum(e['area_m2'] for e in evidence),'net_area_m2':room.area-sum(e['area_m2'] for e in evidence),'annotated_area_m2':1022,'boundary_source_handles':['3E42','3E43','3D31','4053','4054','4097','4098','4052','4099','409A'],'columns':evidence,'unresolved':['Source annotated area differs from interpreted interior area.','Furniture arrangement and facade/window details absent.','Working plane exclusion and glare calculation regions require explicit native setup.']},indent=2),encoding='utf-8')
print(json.dumps({'room_area_m2':room.area,'column_count':len(columns),'net_area_m2':room.area-sum(e['area_m2'] for e in evidence)},indent=2))
