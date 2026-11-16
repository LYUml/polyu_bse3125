"""Author revised eight-page narrative from shared/native evidence; append CAD separately."""
from pathlib import Path
import json,sys,html,math,hashlib
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
from reportlab.graphics.shapes import Drawing,Polygon,Rect,Circle,String,Line
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2];folder=root/'05_Calculations/Final_v03';data=root/'05_Calculations/data'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
out=Path(sys.argv[1]);assert not out.exists()
content=load(folder/'report-content-v3.json');tasks=load(data/'review-40s-reopened-tasks-v4.json');aux=load(data/'review-brightness-reopened-results-v4.json')
assert tasks['all_tasks_pass_course_metrics'] and aux['all_present_groups_pass'] and aux['all_six_groups_present']
room=load(data/'room-v1.json');furniture=load(data/'furniture-proposal-v1.json');plan=load(data/'snapped-layout-proposal-v3.json');controls=load(data/'controls-proposal-v2.json')
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
navy=colors.HexColor('#15364F');teal=colors.HexColor('#008995');grey=colors.HexColor('#506572');light=colors.HexColor('#E9F0F3');W=A4[0]-88
body=ParagraphStyle('body',fontName='Body',fontSize=10,leading=14,spaceAfter=9,textColor=navy)
small=ParagraphStyle('small',parent=body,fontSize=8.2,leading=11,spaceAfter=5)
heading=ParagraphStyle('heading',fontName='Bold',fontSize=19,leading=24,textColor=navy,spaceAfter=12)
caption=ParagraphStyle('caption',parent=small,textColor=grey,spaceBefore=4,spaceAfter=10)
P=lambda s,style=body:Paragraph(html.escape(str(s)),style)
def table(rows,widths):
 hs=ParagraphStyle('header',parent=small,fontName='Bold',textColor=colors.white)
 t=Table([[P(c,hs if i==0 else small) for c in row] for i,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,light])]))
 return t
def map_figure(mode):
 d=Drawing(W,205);scale=6.1;ox,oy=5,16
 def xy(x,y):return ox+x*scale,oy+y*scale
 def poly(coords,fill,stroke=grey,width=.4):d.add(Polygon([v for p in coords for v in xy(*p[:2])],fillColor=fill,strokeColor=stroke,strokeWidth=width))
 poly(room['contour'],colors.HexColor('#F4F7F8'))
 if mode=='zones':
  palette=['#D2E8EC','#E6EDD4','#F1DECC','#D9DDF0','#EBD7E7','#D5E5D8']
  for i,z in enumerate(controls['zones']):
   geom=z['polygon'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
   for p in polys:poly(p[0],colors.HexColor(palette[i%6]),colors.white,.5)
   x,y=xy(*z['seed_m']);d.add(String(x,y,z['id'],fontName='Bold',fontSize=5.5,textAnchor='middle',fillColor=navy))
 for c in room['obstacles']:
  x,y=xy(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2);d.add(Rect(x,y,c['size_m'][0]*scale,c['size_m'][1]*scale,fillColor=grey,strokeColor=None))
 def colour(value):
  t=max(0,min(1,(value-500)/250));return colors.Color(.98-.72*t,.73+.11*t,.26+.50*t)
 if mode=='tasks':
  metrics={t['name']:t for t in tasks['tasks']}
  for desk in furniture['desks']:poly(desk['polygon_m'],colour(metrics[desk['id']]['average_lx']),navy,.2)
  for name,dy in [('Desk-018',8),('Desk-021',-12),('Desk-084',8)]:
   desk=next(x for x in furniture['desks'] if x['id']==name);x,y=xy(*desk['centre_m'][:2]);d.add(Circle(x,y,4,strokeColor=navy,fillColor=None));d.add(String(x+5,y+dy,name,fontName='Bold',fontSize=5.5,fillColor=navy))
  for i in range(50):d.add(Rect(315+i*3.4,105,3.5,12,fillColor=colour(500+i/49*250),strokeColor=None))
  for v in [500,600,700,750]:d.add(String(315+(v-500)/250*170,94,str(v),fontName='Body',fontSize=6,textAnchor='middle',fillColor=navy))
  lines=['Maintained desk mean / lx','One coloured cell per desk','Native results; no interpolation']
 else:
  for b in furniture['benches']:
   x,y=xy(b['centre_m'][0]-1.6,b['centre_m'][1]-.8);d.add(Rect(x,y,3.2*scale,1.6*scale,fillColor=None,strokeColor=grey,strokeWidth=.4))
  for f in plan['fixtures']:
   x,y=xy(*f['position_m'][:2]);d.add(Rect(x-1.6,y-1.6,3.2,3.2,fillColor=navy,strokeColor=None))
  lines=['186 recessed luminaires','28 benches / 112 desks','Grey: full-height columns','Furniture: proposed design'] if mode=='basis' else ['32 independent control zones','28 bench + 4 circulation zones','Maximum zone: 46.67 m2','Manual on/off/dim per zone']
 for i,s in enumerate(lines):d.add(String(315,177-i*17,s,fontName='Body',fontSize=7,fillColor=navy))
 d.add(Line(ox,7,ox+61,7,strokeColor=navy));d.add(String(ox,0,'0',fontName='Body',fontSize=6));d.add(String(ox+61,0,'10 m',fontName='Body',fontSize=6,textAnchor='end'))
 return d
def footer(c,doc):
 c.setStrokeColor(teal);c.line(44,40,A4[0]-44,40);c.setFillColor(grey);c.setFont('Body',7);c.drawString(44,27,'BSE3125 | Open-plan office lighting');c.drawRightString(A4[0]-44,27,str(doc.page))
story=[]
def section(i,figure=None,cap=None):
 s=content['sections'][i];story.append(P(s['title'],heading))
 if figure:story.extend([figure,P(cap,caption)])
 for text in s['paragraphs']:story.append(P(text))
def image_crop(source,page,box,name,width):
 doc=pdfium.PdfDocument(source);im=doc[page-1].render(scale=2).to_pil();im.crop(box).save(folder/'figures'/name);doc.close();p=folder/'figures'/name
 return Image(str(p),width=width,height=width*(box[3]-box[1])/(box[2]-box[0]))
(folder/'figures').mkdir(exist_ok=True)
story.extend([P(content['title'],ParagraphStyle('title',parent=heading,fontSize=25,leading=30)),P(content['subtitle'],caption)])
section(0,map_figure('basis'),'Figure 1. Measured office boundary and proposed lighting/workstation arrangement; shared design dataset.')
story.append(PageBreak());section(1)
story.append(table([['Calculation object','Project setting and interpretation'],['112 desk planes','1.6 x 0.8 m at z = 0.8 m; 10 x 5 regular grid, nominal 0.16 m spacing'],['112 directional UGR objects','Seated z = 1.2 m; directions in 15-degree steps; actual maximum over all desks'],['Surrounding / background','0.5 m band outside each four-desk bench; remaining usable background floor'],['Cylindrical / exposed surfaces','140 task/surround regions at z = 1.2 m; six wall regions and exposed ceiling']],[W*.29,W*.71]))
story.append(PageBreak());section(2)
story.append(image_crop(root/'02_References/Manufacturer/910505103638.pdf',3,(60,640,610,1120),'manufacturer-polar.png',240))
story.append(P('Figure 2. Manufacturer polar intensity distribution, C0-C180 and C90-C270 planes (leaflet p3) [4]. High-angle intensity affects glare and display reflections; actual room UGR is checked separately.',caption))
story.append(PageBreak());section(3,map_figure('tasks'),'Figure 3. All 112 maintained desk means from the reopened core project (Appendix A, original native pp268-277). Different desks control illuminance, uniformity and glare.')
story.append(table(content['iteration_table'],[W*.27,W*.24,W*.24,W*.25]));story.append(PageBreak())
story.append(P('Criteria and calculated performance',heading));story.append(P('Ordinary office paperwork, typing and data processing: course criteria [1] and EN 12464-1:2021 Table 34, row 34.2 [2]. Values below are maintained electric-light calculations unless identified as manufacturer data or a bounded screening check.'))
rows=[['Quantity / source','Adopted criterion','Actual result / assessment'],['Desk mean [2], Table 34','>= 500 lx','Minimum 593 lx; all 112 pass'],['Desk uniformity [2], Table 34','Uo >= 0.60','Minimum 0.80; all 112 pass'],['Directional glare [2], Table 34','UGR <= 19','Maximum 18.1, Desk-018 at 180 degrees; all 112 pass'],['Colour rendering [2,4]','Ra >= 80','Ra > 80, manufacturer declaration']]
labels={'immediate surrounding':('Surrounds [2], 5.3.4','300 lx / Uo 0.40'),'background floor':('Background [2], 5.3.5','100 lx / Uo 0.10'),'exposed walls':('Walls [2], Table 34','150 lx / Uo 0.10'),'exposed ceiling':('Ceiling [2], Table 34','100 lx / Uo 0.10')}
cy=aux['combined_seated_cylindrical'];rows.append(['Seated cylindrical [2], 5.6.2','150 lx / Uo 0.10',f"Minimum mean {cy['minimum_surface_average_lx']:g} lx; combined Uo >= {math.floor(cy['conservative_combined_u0_lower_bound']*100)/100:.2f}; pass"])
for c in aux['checks']:
 if c['group'] in labels:
  label,criterion=labels[c['group']];rows.append([label,criterion,f"Minimum mean {c['minimum_surface_average_lx']:g} lx; combined Uo >= {math.floor(c['conservative_combined_u0_lower_bound']*100)/100:.2f}; pass"])
rows.extend([['Office LPD [5], Table 5.4','<= 7.2 W/m2','4.235 W/m2; conservative 4328 W / 1022 m2; pass'],['Display screening [2], 5.9.2','1500 cd/m2, adopted case','1334 cd/m2 sampled maximum, gamma 65-89 degrees; qualified screening only']])
story.append(table(rows,[W*.28,W*.24,W*.48]));story.append(P('For a union of regions, Uo is bounded conservatively by the smallest native point minimum divided by the largest region average; displayed bounds are rounded down. This avoids averaging regional uniformities. Walls use 0.42 m edge borders (clause 5.4); physical column and luminaire openings are excluded from exposed regions. The 36 supplemental regions contain 255 actual native openings.',small));story.append(P('The selected 500 lx basis applies to ordinary taught office tasks. Reassess context modifiers (clause 5.3.3) for demanding/low-contrast work, impaired vision, prolonged tasks or inadequate daylight provision. This comparison does not establish full standard or statutory certification.',small))
story.append(PageBreak());section(4,map_figure('zones'),'Figure 4. Functional control zones from the shared fixture dataset. All 186 fixtures belong to one zone each; interfaces and sensor coverage require commissioning.')
story.append(table(content['control_table'],[W*.34,W*.29,W*.37]));story.append(PageBreak());section(5)
story.append(image_crop(Path(tasks['pdf']),529,(196,590,1100,1038),'native-desk021-isolux.png',350))
story.append(P('Figure 5. Native Desk-021 isolux/grid output: mean 593 lx, minimum 525 lx, maximum 637 lx; Uo = 525/593 = 0.89. Source: reopened project, Appendix A original native p529. This is the controlling desk average, not the controlling Uo or UGR.',caption))
story.append(PageBreak());section(6)
story.append(P('References',ParagraphStyle('refs',parent=heading,fontSize=12,leading=16,spaceAfter=7)))
for ref in content['references']:
 story.append(P(f"[{ref['id']}] {ref['title']}. "+ref.get('scope',''),small))
 if 'url' in ref:story.append(Paragraph('<link href="'+html.escape(ref['url'],quote=True)+'" color="#008995">Official source</link>',small))
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=43,bottomMargin=52,title=content['title'],author='BSE3125 design group',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
d=pdfium.PdfDocument(out);assert len(d)==8,f'Unexpected pagination {len(d)}';d.close()
out.with_suffix('.json').write_text(json.dumps({'page_count':8,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'status':'narrative generated; visual and final assembly acceptance pending'},indent=2))
