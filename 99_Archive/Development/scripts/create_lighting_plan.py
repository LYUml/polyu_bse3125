"""Independent assignment CAD sheet using shared, report-verified fixture data.

Reuses toolkit label placement and dimension geometry. The toolkit's synthetic
sheet authoring is deliberately not used for a production coursework drawing.
Native DWG reopening and PDF plotting remain separate acceptance gates.
"""
from pathlib import Path
import sys,json,hashlib,textwrap
import ezdxf
from ezdxf.math import Matrix44
from ezdxf import bbox
from shapely.geometry import box,Polygon
root=Path(__file__).resolve().parents[2];toolkit=root.parent/'dialux-agent-toolkit'
sys.path.insert(0,str(toolkit))
from src.cad_labels import place_fixture_labels
from src.cad_dimensions import add_dimensions
data=root/'05_Calculations/data'
target=Path(sys.argv[4]) if len(sys.argv)>4 else root/'05_Calculations/Final_v01/BSE3125-L01-lighting-plan-v3.dxf'
destination=target.parent;destination.mkdir(parents=True,exist_ok=True);assert not target.exists()
revision=sys.argv[5] if len(sys.argv)>5 else 'P01'
source=toolkit/'local/bse3125-native-v2/source-copy.dxf'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='d8cea3af6c404161b7962567412832ff8343c1149327e8eed0f9f5d2597bbfb2'
plan_path=Path(sys.argv[1]) if len(sys.argv)>1 else data/'snapped-layout-proposal-v2.json';p=json.loads(plan_path.read_text())
verified=json.loads((Path(sys.argv[2]) if len(sys.argv)>2 else data/'grid-report-position-verification-v3.json').read_text())
assert verified['plan_sha256']==hashlib.sha256(plan_path.read_bytes()).hexdigest() and verified['fixture_count']==186
results=json.loads((Path(sys.argv[3]) if len(sys.argv)>3 else data/'grid-tasks-results-v3.json').read_text());assert results['all_tasks_pass_course_metrics']
products={f['product_order_code'] for f in p['fixtures']};assert len(products)==1
product=next(iter(products));flux=p.get('nominal_luminaire_flux_lm',3400);rated=p['rated_input_W_each'];native=p['native_photometry_input_W_each'];luminaire_load=186*rated;budget=luminaire_load+50
r=json.loads((data/'room-v1.json').read_text());furniture=json.loads((data/'furniture-proposal-v1.json').read_text())
doc=ezdxf.readfile(source);model=doc.modelspace();doc.units=6
doc.styles.get('Standard').dxf.font='arial.ttf'
# Flatten source dynamic blocks before unit conversion. AutoCAD otherwise
# regenerated the one source ceiling block using its old millimetre parameters.
exploded_source_blocks=[e.dxf.handle for e in list(model.query('INSERT'))]
for insert in list(model.query('INSERT')):insert.explode(target_layout=model)
transform=Matrix44.chain(Matrix44.scale(.001),Matrix44.translate(-64.34593225182503,-15.92558365525945,0))
removed=[];source_count=0
for entity in list(model):
 if entity.dxf.handle in ['8D06','8D08','8D09']:
  removed.append(entity.dxf.handle);model.delete_entity(entity);continue
 entity.transform(transform);source_count+=1
 original=entity.dxf.layer;layer='SRC_'+original
 if layer not in doc.layers:
  attrs={'color':8,'lineweight':13}
  if original=='Ceiling Grid':attrs.update(true_color=ezdxf.colors.rgb2int((210,210,210)),lineweight=5)
  doc.layers.new(layer,dxfattribs=attrs)
 entity.dxf.layer=layer;entity.dxf.color=256
for name,color,weight in [('ROOM',7,25),('LUMINAIRES',7,35),('FURNITURE',8,9),('BENCH_IDS',7,13),('SCHEDULE',7,18),('SHEET',7,25),('PLAN_NOTES',7,18),('LABEL_MASK',7,0)]:
 if name not in doc.layers:doc.layers.new(name)
 doc.layers.get(name).dxf.color=color;doc.layers.get(name).dxf.lineweight=weight
doc.layers.get('FURNITURE').dxf.true_color=ezdxf.colors.rgb2int((160,160,160))
model.add_lwpolyline(r['contour'],close=True,dxfattribs={'layer':'ROOM'})
exclusions=[]
for c in r['obstacles']:
 x,y=c['center_m'][:2];w,h=c['size_m'][:2];exclusions.append(list(box(x-w/2,y-h/2,x+w/2,y+h/2).exterior.coords)[:-1])
spec={'contour':r['contour'],'exclusions':exclusions,'fixture':{'width_m':.597,'depth_m':.597}}
layout={'fixtures':[{'id':f['id'],'position_m':f['position_m'],'rotation_deg':0} for f in p['fixtures']]}
body_boxes=[box(f['position_m'][0]-.30,f['position_m'][1]-.30,f['position_m'][0]+.30,f['position_m'][1]+.30) for f in p['fixtures']]
bench_labels={}
for bench in furniture['benches']:
 x,y=bench['centre_m']
 for cx,cy in [(x,y),(x,y-1.12),(x,y+1.12),(x+1.95,y),(x-1.95,y)]:
  envelope=box(cx-.33,cy-.15,cx+.33,cy+.15)
  if Polygon(r['contour']).contains(envelope) and not any(envelope.intersects(b) for b in body_boxes):break
 else:raise ValueError('No clear bench label '+bench['id'])
 bench_labels[bench['id']]=(cx,cy)
 spec['exclusions'].append(list(envelope.exterior.coords)[:-1])
labels=place_fixture_labels(spec,layout,.23)
symbol=doc.blocks.new('BSE3125_PANEL_TYPE_A')
symbol.add_lwpolyline([(-.2985,-.2985),(.2985,-.2985),(.2985,.2985),(-.2985,.2985)],close=True)
symbol.add_line((-.2985,-.2985),(.2985,.2985))
symbol.add_attdef('FIXTURE_ID',(0,-.6),height=.23)
for desk in furniture['desks']:
 model.add_lwpolyline(desk['polygon_m'],close=True,dxfattribs={'layer':'FURNITURE'})
def mask(cx,cy,half_width,half_height):
 model.add_solid([(cx-half_width,cy-half_height),(cx+half_width,cy-half_height),(cx-half_width,cy+half_height),(cx+half_width,cy+half_height)],dxfattribs={'layer':'LABEL_MASK','true_color':ezdxf.colors.rgb2int((255,255,255))})
for bench in furniture['benches']:
 x,y=bench_labels[bench['id']];mask(x,y,.33,.15)
 model.add_text(bench['id'],dxfattribs={'layer':'BENCH_IDS','height':.20}).set_placement((x,y),align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
for f in layout['fixtures']:
 cx,cy=labels[f['id']]['center_m'];mask(cx,cy,.36,.17)
 x,y,z=f['position_m'];insert=model.add_blockref(symbol.name,(x,y,0),dxfattribs={'layer':'LUMINAIRES'})
 insert.add_auto_attribs({'FIXTURE_ID':f['id']})
 insert.get_attrib('FIXTURE_ID').set_placement((cx,cy),align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
dimensions=[{'id':'D1','p1_m':[0,0],'p2_m':[45,0],'base_m':[0,-1.25],'angle_deg':0},{'id':'D2','p1_m':[0,0],'p2_m':[0,30],'base_m':[-1.25,0],'angle_deg':90}]
add_dimensions(doc,dimensions,.25)
def text(value,x,y,height=.23,layer='PLAN_NOTES'):
 return model.add_text(value,dxfattribs={'insert':(x,y),'height':height,'layer':layer})
def lines(items,x,y,height=.23,gap=.47,layer='PLAN_NOTES'):
 for i,value in enumerate(items):text(value,x,y-i*gap,height,layer)
 return y-len(items)*gap
x=46.;y=29.5
y=lines(['LUMINAIRE SCHEDULE - TYPE A','Philips PowerBalance gen2','Order: '+product,f'RC461B {int(flux/100)}S/840 SEIA W60L60','VPC U4 SC UE','Quantity: 186 recessed modules','Size: 597 x 597 mm; 600 module',f'4000 K; CRI >80; {flux:g} lm',f'Input: {rated:g} W rated ({native:g} W ULD)',f'Connected luminaire load: {luminaire_load:g} W','Controls allowance: 50 W',f'Design lighting budget: {budget:g} W'],x,y,layer='SCHEDULE')
y-=.45
y=lines(['LEGEND','Square + diagonal: Type A panel','L001-L186: unique luminaire IDs','Grey lines: source ceiling grid','Desk outlines: proposed furniture','B01-B28: four-person benches','Desk IDs: 4n-3..4n at bench Bn;','SW, SE, NW, NE in that order.'],x,y)
y-=.45
y=lines(['DESIGN NOTES','1. Drawing dimensions are in mm.','2. Ceiling: 2800 mm above FFL.','   Recessed emitting face flush.','   Body: 82 mm table; allow 86 mm','   supplier drawing envelope plus','   plenum/service clearance.','3. Source tiles are 600 x 600 mm.','   Every panel uses a full tile.','4. Desks are assumed at 800 mm.','   Layout: 112 seats, 28 benches.','5. Controls: 32 independent zones.','   Vacancy off after 10 minutes;','   driver/sensor standby retained.','   Manual override <=120 minutes.','   Daylight dimming to be enabled.','6. Core lighting excluded from','   this open-plan office design.','7. Academic design. Coordinate','   dimensions and services on site.'],x,y)
assert y>1.,'Notes exceed right-hand column'
# A2 landscape frame: 20 mm paper margins, 30 mm title block at 1:100.
left,bottom,right,top=-2.,-5.2,53.4,32.8
for a,b in [((left,bottom),(right,bottom)),((right,bottom),(right,top)),((right,top),(left,top)),((left,top),(left,bottom)),((left,-2.2),(right,-2.2)),((left,-3.7),(right,-3.7))]:model.add_line(a,b,dxfattribs={'layer':'SHEET'})
text('BSE3125  |  OPEN-PLAN OFFICE LIGHTING LAYOUT',-1.5,-3.15,.36,'SHEET')
text(f'Drawing: BSE3125-L01     Revision: {revision}     Academic design',-1.5,-4.65,.25,'SHEET')
text('A2 LANDSCAPE  |  1:100 AT 100% PRINT  |  DIMENSIONS: mm',25.,-4.65,.25,'SHEET')
content=bbox.extents([e for e in model if e.dxf.layer!='SHEET'],fast=False)
assert content.extmin.x>left and content.extmax.x<right and content.extmin.y>-2.2 and content.extmax.y<top
doc.saveas(target)
reopened=ezdxf.readfile(target);observed={e.get_attrib_text('FIXTURE_ID'):list(e.dxf.insert) for e in reopened.modelspace().query('INSERT[layer=="LUMINAIRES"]')}
assert len(observed)==186
for f in p['fixtures']:assert all(abs(a-b)<1e-9 for a,b in zip(observed[f['id']][:2],f['position_m'][:2]))
record={'status':'editable independent CAD sheet; native DWG/plot QA pending','path':str(target.resolve()),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_dxf_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'layout_sha256':hashlib.sha256(plan_path.read_bytes()).hexdigest(),'fixture_count':186,'desk_count':112,'source_entities_transformed':source_count,'exploded_source_block_handles':exploded_source_blocks,'source_annotation_handles_removed_in_copy':removed,'source_original_unchanged':True,'paper':'A2','scale_denominator':100,'frame_m':[left,bottom,right,top],'label_positions':labels}
target.with_suffix('.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='label_positions'},indent=2))
