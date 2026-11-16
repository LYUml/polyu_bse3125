"""Explicit 32-zone control design tied to the current shared fixture proposal."""
from pathlib import Path
import json,hashlib,sys
from shapely.geometry import Polygon,box,MultiPoint,mapping
from shapely.ops import voronoi_diagram,unary_union
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
layout_path=Path(sys.argv[1]) if len(sys.argv)>1 else data/'snapped-layout-proposal-v2.json';layout=json.loads(layout_path.read_text())
furniture=json.loads((data/'furniture-proposal-v1.json').read_text());r=json.loads((data/'room-v1.json').read_text())
room=Polygon(r['contour']);columns=unary_union([box(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2,c['center_m'][0]+c['size_m'][0]/2,c['center_m'][1]+c['size_m'][1]/2) for c in r['obstacles']]);usable=room.difference(columns)
seeds=[{'id':f'Z{i:02}','seed_m':b['centre_m'],'activity':b['id']+' paperwork bench','manual_interface':'One independent local manual on/off/dim control at the bench'} for i,b in enumerate(furniture['benches'],1)]
seeds += [{'id':f'Z{i}','seed_m':p,'activity':'Circulation','manual_interface':'One independent local manual on/off/dim control, location to be coordinated with final access layout'} for i,p in enumerate([[14.38,15.8],[25.18,15.8],[10.78,5.38],[37.58,20.98]],29)]
points=MultiPoint([s['seed_m'] for s in seeds]);cells=list(voronoi_diagram(points,envelope=room.envelope.buffer(10)).geoms)
for s in seeds:
 from shapely.geometry import Point
 point=Point(s['seed_m']);cell=[c for c in cells if c.covers(point)];assert len(cell)==1
 poly=cell[0].intersection(usable);assert 0<poly.area<=250
 s.update(area_m2=poly.area,polygon=mapping(poly),fixture_ids=[])
for f in layout['fixtures']:
 distances=[sum((a-b)**2 for a,b in zip(f['position_m'][:2],s['seed_m'])) for s in seeds]
 i=min(range(len(seeds)),key=lambda i:distances[i]);seeds[i]['fixture_ids'].append(f['id'])
assert all(s['fixture_ids'] for s in seeds)
assert abs(sum(s['area_m2'] for s in seeds)-usable.area)<1e-6
out=Path(sys.argv[2]) if len(sys.argv)>2 else data/'controls-proposal-v1.json';assert not out.exists()
budget=186*layout['rated_input_W_each']+50
record={'status':'proposed control zoning and commissioning requirements; not installed controls or an electrical circuit design','layout_sha256':hashlib.sha256(layout_path.read_bytes()).hexdigest(),'manual_control_points':32,'base_BEC_table_5_5_points':32,'LPD_reduction_claimed':False,'zone_count':len(seeds),'maximum_zone_area_m2':max(s['area_m2'] for s in seeds),'net_zoned_area_m2':usable.area,'automatic_operation':{'each_zone_independent':True,'vacancy_off_delay_minutes':10,'light_output_after_vacancy_percent':0,'off_state_power':'Driver/sensor standby remains; zero electrical consumption is not assumed.','minimum_automatic_power_reduction_pct':50,'maximum_manual_override_minutes':120,'weekend_holidays':'Calendar-controlled shutdown with local timed override; recommission with occupier schedule.','daylight':'Daylight-responsive control provided as a design requirement where exterior fenestration triggers BEC 5.6.2. Confirm actual glazing, required zone extent and a separate daylight control device. Calibrate to maintain >=500 lx at the worst desk in each occupied zone; no simulated daylight or annual savings credited.','commissioning':'Confirm sensor coverage at 2.8 m, occupancy timing, automatic power reduction >=50% including standby, override expiry, independent manual switching and calibrated daylight response.'},'power_budget':{'luminaire_count':186,'datasheet_rated_input_W_each':layout['rated_input_W_each'],'native_photometry_W_each':layout['native_photometry_input_W_each'],'external_control_allowance_W':50,'design_connected_budget_W':budget,'LPD_using_conservative_1022_m2_W_m2':budget/1022,'BEC_office_limit_W_m2':7.2,'scope':'Rated full-load design plus external control allowance; standby must be measured for off-state power reduction. Actual controller/accessory loads remain a procurement check.'},'zones':seeds}
out.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ['zones','automatic_operation']},indent=2))
