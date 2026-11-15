"""Preserve and inspect the supplied native-converted CAD, without adopting geometry."""
from pathlib import Path
import hashlib,json,collections,math
import ezdxf
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
TOOLKIT=ROOT.parent/'dialux-agent-toolkit'
OUT=ROOT/'05_Calculations/data'
OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
originals=[ROOT/'01_Assignment_Brief/BSE3125 DIALux Assignment 2627.pdf',ROOT/'01_Assignment_Brief/Building_Drawings/Project layout.dwg']
native=TOOLKIT/'local/bse3125-native-v2'
assert sha(originals[1])==sha(native/'source-copy.dwg')
import subprocess
record={'originals':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in originals],
 'toolkit_commit':subprocess.check_output(['git','-C',str(TOOLKIT),'rev-parse','HEAD'],text=True).strip(),'native_conversion_manifest':json.loads((native/'manifest.json').read_text()),
 'converted_dxf':str(native/'source-copy.dxf'),'converted_dxf_sha256':sha(native/'source-copy.dxf')}
(OUT/'source_manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
d=ezdxf.readfile(native/'source-copy.dxf'); m=d.modelspace()
assert d.header['$INSUNITS']==4
scale=0.001; origin=(64.34593225182503,15.92558365525945)
def xy(v):return [round(float(v[0])*scale-origin[0],6),round(float(v[1])*scale-origin[1],6)]
entities=[]
for e in m:
 t=e.dxftype(); item={'handle':e.dxf.handle,'type':t,'layer':e.dxf.layer}
 if t=='LINE':item.update(points=[xy(e.dxf.start),xy(e.dxf.end)])
 elif t=='LWPOLYLINE':item.update(points=[xy(p) for p in e.get_points('xy')],closed=e.closed)
 elif t in ('TEXT','MTEXT'):item.update(text=e.dxf.text if t=='TEXT' else e.text,position=xy(e.dxf.insert))
 else:continue
 entities.append(item)
(OUT/'cad_entities.json').write_text(json.dumps({'units':'m','drawing_origin_wcs_m':origin,'entities':entities},indent=2),encoding='utf-8')
im=Image.new('RGB',(2000,1500),'white'); draw=ImageDraw.Draw(im)
def px(p):return (round(70+p[0]*40),round(1370-p[1]*40))
for item in entities:
 if 'points' not in item:continue
 pts=[px(p) for p in item['points']]
 if item.get('closed'):pts.append(pts[0])
 if len(pts)>1:draw.line(pts,fill='#c9d3df' if item['layer']=='Ceiling Grid' else '#222222',width=1 if item['layer']=='Ceiling Grid' else 2)
for item in entities:
 if 'text' in item:draw.text(px(item['position']),item['text'].replace('%%U',''),fill='navy')
draw.text((50,25),'Source CAD inspection - metres from southwest column corner; no design adopted',fill='black')
im.save(OUT/'source_plan_preview.png')
print(json.dumps({'source_unchanged':True,'units':'mm','entity_counts':dict(collections.Counter(e.dxftype() for e in m)),'preview':str(OUT/'source_plan_preview.png')},indent=2))
