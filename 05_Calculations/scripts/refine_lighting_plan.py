"""Presentation-only CAD revision; fixture and room geometry remain unchanged."""
from pathlib import Path
import sys,json,hashlib
import ezdxf
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r.parent/'dialux-agent-toolkit'))
from src.cad import _fixture_records,verify_layout_native
source=r/'05_Calculations/Final_v03/BSE3125-L01-lighting-plan-v5.dxf';version=sys.argv[1] if len(sys.argv)>1 else 'v6';target=r/f'05_Calculations/Final_v04/BSE3125-L01-lighting-plan-{version}.dxf';assert not target.exists()
doc=ezdxf.readfile(source);m=doc.modelspace();original=_fixture_records(source)
for layer in doc.layers:
 if layer.dxf.name.startswith('SRC_'):
  value=210 if 'Ceiling' in layer.dxf.name else 170;layer.dxf.true_color=ezdxf.colors.rgb2int((value,value,value));layer.dxf.lineweight=5 if 'Ceiling' in layer.dxf.name else 9
for e in list(m):
 if e.dxf.layer in ['SCHEDULE','PLAN_NOTES']:
  m.delete_entity(e);continue
 if e.dxftype()=='TEXT' and e.dxf.layer=='SHEET':e.dxf.text=e.dxf.text.replace('Revision: P03','Revision: P04')
def text(t,x,y,h=.22,layer='PLAN_NOTES'):m.add_text(t,dxfattribs={'insert':(x,y),'height':h,'layer':layer})
def line(x1,y1,x2,y2,layer='SCHEDULE'):m.add_line((x1,y1),(x2,y2),dxfattribs={'layer':layer})
text('LUMINAIRE SCHEDULE',46,29.65,.26,'SCHEDULE')
rows=[('Type / quantity',['A / 186']),('Manufacturer',['Philips']),('Range',['PowerBalance gen2']),('Order code',['910505103638']),('Model',['RC461B 40S/840','SEIA W60L60','VPC U4 WH SC UE']),('Mounting',['Recessed; 600 mm grid']),('Size (mm)',['597 x 597']),('Flux / input',['4000 lm / 23 W']),('CCT / CRI',['4000 K / >80']),('Luminaire load',['4278 W']),('Controls',['50 W']),('Total design load',['4328 W'])]
x0,x1,x2=46,48.75,53.0;y=29.3;top=y
line(x0,y,x2,y)
for label,values in rows:
 height=max(.65,.27+len(values)*.32);text(label,x0+.12,y-.40,.21,'SCHEDULE')
 for i,v in enumerate(values):text(v,x1+.12,y-.40-i*.32,.21,'SCHEDULE')
 y-=height;line(x0,y,x2,y)
for x in [x0,x1,x2]:line(x,top,x,y)
y-=.7;text('LEGEND',46,y,.26);y-=.55
for t in ['Square + diagonal: Type A panel','L001-L186: luminaire identifiers','Light grey: existing ceiling grid','Thin outlines: proposed desks','B01-B28: four-person benches']:
 text(t,46,y);y-=.45
y-=.35;text('DESIGN NOTES',46,y,.26);y-=.55
for t in ['1. Dimensions in mm; ceiling at 2800.','   Emitting faces flush with ceiling.','2. Each panel occupies a full tile.','   Lower chain dimensions: L001-L004.','   Local spacing varies around columns.','   L120 has a 600 mm local grid shift.','3. Allow 86 mm fitting envelope plus','   driver and maintenance clearance.','4. Furniture is proposed: 112 desks','   at 800 mm above finished floor.','5. Core lighting is outside this scope.','6. Control strategy: report Section 6.','7. Coordinate services before installation.']:
 text(t,46,y);y-=.43
assert y>1
fixtures={f['id']:f for f in json.loads((r/'05_Calculations/data/snapped-layout-proposal-v3.json').read_text())['fixtures']}
for i,(a,b) in enumerate([('L001','L002'),('L002','L003'),('L003','L004')],3):
 p1,p2=fixtures[a]['position_m'][:2],fixtures[b]['position_m'][:2]
 dim=m.add_linear_dim(base=(p1[0],-.5),p1=p1,p2=p2,angle=0,dxfattribs={'layer':'DIMENSIONS'},override={'dimlfac':1000,'dimpost':'<> mm','dimdec':0,'dimtxt':.20,'dimasz':.14,'dimgap':.08,'dimexo':1.05,'dimexe':.10})
 dim.dimension.set_xdata('DIALUX_AGENT_DIMENSION',[(1000,f'D{i}')]);dim.render()
doc.saveas(target);assert _fixture_records(target)==original
record={'source':str(source.relative_to(r)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'revised_dxf':str(target.relative_to(r)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'all_186_fixture_records_identical':True,'changes':['Lighter architectural underlay','Tabulated luminaire schedule','Shorter installation notes','Three actual spacing dimensions L001-L004','Revision P04']}
target.with_suffix('.json').write_text(json.dumps(record,indent=2))
result=verify_layout_native(str(target),str(r/f'05_Calculations/Final_v04/cad-native-{version}'));print(json.dumps({k:result[k] for k in ['native_reopen_verified','fixture_count','dimension_count','schedule_entity_count','dwg_sha256']},indent=2))
