"""Build the editable report's seven A4 pages; formal CAD and appendix are separate.

Drafts are visibly marked. Final assembly additionally requires persistence,
content/layout inspection, native CAD and overall submission acceptance.
"""
from pathlib import Path
import json,sys,html,hashlib,math
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
from reportlab.graphics.shapes import Drawing,Polygon,Rect,Circle,String,Line
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
aux_path,out=map(Path,sys.argv[1:3]);draft='--draft' in sys.argv[3:];assert not out.exists()
out.parent.mkdir(parents=True,exist_ok=True)
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
content=load(root/'05_Calculations/Final_v02/report-content-v1.json');aux=load(aux_path)
assert aux['all_present_groups_pass'] and aux['all_six_groups_present']
if not draft:
 persistence=load(data/'brightness-openings-persistence-v9.json');assert persistence['status']=='verified'
tasks=load(data/'grid-reopened-tasks-v4.json');assert tasks['all_tasks_pass_course_metrics']
room=load(data/'room-v1.json');furniture=load(data/'furniture-proposal-v1.json')
fixtures=load(data/'snapped-layout-proposal-v2.json')['fixtures'];controls=load(data/'controls-proposal-v1.json')
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
navy=colors.HexColor('#15364F');teal=colors.HexColor('#008995');grey=colors.HexColor('#506572');light=colors.HexColor('#E9F0F3')
body=ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=14.2,textColor=navy,spaceAfter=8)
small=ParagraphStyle('small',parent=body,fontSize=8.3,leading=11.2,spaceAfter=5)
heading=ParagraphStyle('heading',fontName='Bold',fontSize=18,leading=23,textColor=navy,spaceAfter=13)
caption=ParagraphStyle('caption',parent=small,textColor=grey,spaceBefore=5,spaceAfter=10)
P=lambda text,style=body:Paragraph(html.escape(text),style)
W=A4[0]-88
def map_figure(mode):
 d=Drawing(W,210);scale=6.1;ox,oy=6,17
 def xy(x,y):return ox+x*scale,oy+y*scale
 def polygon(coords,fill,stroke=grey,width=.4):
  d.add(Polygon([v for p in coords for v in xy(*p[:2])],fillColor=fill,strokeColor=stroke,strokeWidth=width))
 polygon(room['contour'],colors.HexColor('#F4F7F8'))
 if mode=='zones':
  palette=['#D2E8EC','#E6EDD4','#F1DECC','#D9DDF0','#EBD7E7','#D5E5D8']
  for i,z in enumerate(controls['zones']):
   geom=z['polygon'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
   for poly in polys:polygon(poly[0],colors.HexColor(palette[i%len(palette)]),colors.white,.5)
   x,y=xy(*z['seed_m']);d.add(String(x,y,z['id'],fontName='Bold',fontSize=5.5,textAnchor='middle',fillColor=navy))
 for c in room['obstacles']:
  x,y=xy(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2)
  d.add(Rect(x,y,c['size_m'][0]*scale,c['size_m'][1]*scale,fillColor=grey,strokeColor=None))
 if mode=='tasks':
  metrics={t['name']:t for t in tasks['tasks']}
  for task in furniture['desks']:
   val=metrics[task['id']]['average_lx'];t=max(0,min(1,(val-500)/110))
   polygon(task['polygon_m'],colors.Color(.98-.72*t,.73+.11*t,.26+.50*t),navy,.2)
  for name,dy in [('Desk-018',8),('Desk-021',-12),('Desk-084',8)]:
   task=next(v for v in furniture['desks'] if v['id']==name);x,y=xy(*task['centre_m'][:2]);d.add(Circle(x,y,4,fillColor=None,strokeColor=navy,strokeWidth=.7));d.add(String(x+5,y+dy,name,fontName='Bold',fontSize=5.5,fillColor=navy))
 else:
  for bench in furniture['benches']:
   x,y=bench['centre_m'];x,y=xy(x-1.6,y-.8);d.add(Rect(x,y,3.2*scale,1.6*scale,fillColor=None,strokeColor=grey,strokeWidth=.4))
 if mode!='tasks':
  for f in fixtures:
   x,y=xy(*f['position_m'][:2]);d.add(Rect(x-1.6,y-1.6,3.2,3.2,fillColor=navy,strokeColor=None))
 legend_x=310
 lines={'basis':['45 x 30 m source footprint','L-shaped office around core','28 benches / 112 desks','186 recessed luminaires','Grey: full-height columns','Furniture: proposed design'],
 'tasks':['Maintained desk averages','Each coloured cell: one desk','No spatial interpolation','Amber: near 500 lx','Teal: approximately 610 lx','Rings: distinct critical desks'],
 'zones':['32 independently controlled zones','28 benches + 4 circulation zones','Maximum zone: 46.67 m2','Local manual on/off/dim','10 min vacancy switch-off','Override expires within 120 min']}[mode]
 for i,line in enumerate(lines):d.add(String(legend_x,175-i*18,line,fontName='Body',fontSize=7,fillColor=navy))
 d.add(Line(ox,7,ox+10*scale,7,strokeColor=navy,strokeWidth=1));d.add(String(ox,0,'0',fontName='Body',fontSize=6));d.add(String(ox+10*scale,0,'10 m',fontName='Body',fontSize=6,textAnchor='end'))
 return d
def workflow():
 d=Drawing(W,115)
 labels=[('MODEL','Contour, columns and finishes'),('SPECIFY','Manufacturer photometry + MF'),('EVALUATE','Tasks, directions and surroundings'),('VERIFY','Save, reopen, compare and document')]
 for i,(title,text) in enumerate(labels):
  x=(i%2)*(W/2+5);y=64-(i//2)*57;d.add(Rect(x,y,W/2-8,46,fillColor=light,strokeColor=None));d.add(String(x+10,y+29,title,fontName='Bold',fontSize=9,fillColor=teal));d.add(String(x+10,y+12,text,fontName='Body',fontSize=7,fillColor=navy))
 return d
def table(rows,widths):
 rows=[[str(cell).replace('Table 34.2','Table 34, row 34.2') for cell in row] for row in rows]
 header_style=ParagraphStyle('headercell',parent=small,textColor=colors.white,fontName='Bold')
 values=[[P(str(c),header_style if i==0 else small) for c in row] for i,row in enumerate(rows)]
 t=Table(values,colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('TEXTCOLOR',(0,0),(-1,0),colors.white),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,light]),('LINEBELOW',(0,0),(-1,0),.6,teal)]))
 return t
def footer(canvas,doc):
 canvas.setStrokeColor(teal);canvas.line(44,40,A4[0]-44,40);canvas.setFont('Body',7);canvas.setFillColor(grey)
 canvas.drawString(44,27,'BSE3125 | Open-plan office lighting');canvas.drawRightString(A4[0]-44,27,str(doc.page))
 if draft:canvas.setFillColor(colors.HexColor('#A85E19'));canvas.drawCentredString(A4[0]/2,15,'WORKING DRAFT - final acceptance pending')
story=[]
def section(index,figure=None):
 s=content['sections'][index];story.append(P(s['title'],heading))
 if figure:story.extend([figure,P({'basis':'Figure 1. Shared geometry and proposed workstation arrangement. Source: original drawing and design dataset.','tasks':'Figure 4. Actual DIALux desk averages mapped to the proposed task areas. Source: reopened native report, pp268-277.','zones':'Figure 5. Functional control zoning. Zone interfaces and operation require commissioning.'}[{'0':'basis','3':'tasks','4':'zones'}[str(index)]],caption)])
 for text in s['paragraphs']:story.append(P(text))
story.extend([P(content['title'],ParagraphStyle('title',parent=heading,fontSize=25,leading=30)),P(content['subtitle'],caption)])
section(0,map_figure('basis'));story.append(PageBreak())
story.append(P(content['sections'][1]['title'],heading));story.extend([workflow(),P('Figure 2. Project-specific simulation and verification sequence. Calculation results are generated in native DIALux evo.',caption)])
for text in content['sections'][1]['paragraphs']:story.append(P(text))
import pypdfium2 as pdfium
native_plot=root/'05_Calculations/models/office-powerbalance-grid-probe-reopened-v4.pdf'
assert hashlib.sha256(native_plot.read_bytes()).hexdigest()==tasks['pdf_sha256']
native_document=pdfium.PdfDocument(native_plot);plot=native_document[528]
assert 'Desk-021' in plot.get_textpage().get_text_range()
figure_dir=out.parent/'figures';figure_dir.mkdir(exist_ok=True)
figure_path=figure_dir/'native-desk021-isolux.png'
plot.render(scale=2).to_pil().crop((196,590,1100,1038)).save(figure_path)
story.append(Image(str(figure_path),width=390,height=390*448/904))
story.append(P('Figure 3. Native Desk-021 isolux and 10 x 5 calculation grid: 504 lx mean, 446 lx minimum, Uo 0.88. [3]',ParagraphStyle('nativecaption',parent=small,fontSize=7.3,leading=9,spaceBefore=3,spaceAfter=0)))
story.append(PageBreak());section(2)
story.append(table([['Selected installation','Design value'],['Product / count','910505103630 / 186 units'],['Imported output / power','3400 lm / 19.8 W per unit'],['Budget / light colour','20 W per unit / 4000 K / Ra > 80'],['Ceiling module / physical body','600 mm / 597 x 597 x 82 mm'],['Maintained calculation basis','MF 0.80; ceiling/wall/floor 80/70/20%']],[W*.36,W*.64]));story.append(PageBreak())
section(3,map_figure('tasks'));story.append(PageBreak())
story.extend([P('Criteria and calculated performance',heading),P('Selected design criteria are compared with actual native calculations. Passing these rows is not an unconditional whole-standard or installed-system certification. Numerical values are maintained electric-light results unless stated otherwise.')])
rows=[['Quantity / basis','Adopted criterion','Actual design / scope'],['Desk average [2], Table 34.2','>= 500 lx','Minimum 504 lx across 112 desks'],['Desk uniformity [2], Table 34.2','Uo >= 0.60','Minimum 0.80 across 112 desks'],['Directional glare [2], Table 34.2','UGR <= 19','Maximum 17.5; 1.2 m height; 15-degree steps'],['Colour rendering [2,4]','Ra >= 80','Manufacturer Ra > 80']]
labels={'immediate surrounding':('0.5 m surrounding band [2], 5.3.4','>= 300 lx; Uo >= 0.40'),'background floor':('Background floor [2], 5.3.5','>= 100 lx; Uo >= 0.10'),'exposed walls':('Exposed walls [2], Table 34.2','>= 150 lx; Uo >= 0.10'),'exposed ceiling':('Exposed ceiling [2], Table 34.2','>= 100 lx; Uo >= 0.10')}
for check in aux['checks']:
 if check['group'] not in labels:continue
 title,criterion=labels[check['group']];lower=math.floor(check['conservative_combined_u0_lower_bound']*100)/100;rows.append([title,criterion,f"Minimum surface mean {check['minimum_surface_average_lx']:g} lx; combined Uo >= {lower:.2f}"])
seated=[s for s in aux['surfaces'] if s['parameter']=='Cylindrical illuminance'];bound=min(s['minimum_lx'] for s in seated)/max(s['average_lx'] for s in seated)
rows.insert(5,['Seated cylindrical [2], 5.6.2','>= 150 lx; Uo >= 0.10',f'Minimum mean 190 lx; combined Uo >= {math.floor(bound*100)/100:.2f}; 140 task/surround surfaces at 1.2 m'])
rows.extend([['Office LPD [5], Table 5.4','<= 7.2 W/m2','3.689 W/m2, conservative 3770 W / 1022 m2'],['DSE luminance screening [2], 5.9.2','1500 cd/m2 adopted category','1134.23 cd/m2 sampled maximum, gamma 65-89 degrees; full angular conformity not established']])
story.append(table(rows,[W*.29,W*.25,W*.46]));story.extend([Spacer(1,10),P('For unions of calculation regions, the reported uniformity lower bound is the smallest native point minimum divided by the largest individual region average. This conservative bound is no greater than the true combined minimum-to-average ratio; it is not an arithmetic mean of region uniformities.',small),P('Context: ordinary paperwork/data processing with fixed proposed task locations. Higher illuminance modifiers must be reconsidered for low contrast, unusually demanding or prolonged work, impaired vision or inadequate daylight provision. Physical exposed-surface masks exclude obstructions; wall borders follow clause 5.4 (0.42 m for 2.8 m-high walls).',small)]);story.append(PageBreak())
section(4,map_figure('zones'));story.append(PageBreak());section(5)
story.append(P('References',ParagraphStyle('refs',parent=heading,fontSize=12,leading=16,spaceBefore=6,spaceAfter=7)))
for ref in content['references']:
 text=f"[{ref['id']}] {ref['title']}. "+ref.get('scope','')
 story.append(P(text,small))
 if 'url' in ref:story.append(Paragraph('<link href="'+html.escape(ref['url'],quote=True)+'" color="#008995">Official source</link>',small))
out.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=43,bottomMargin=52,title=content['title'],author='BSE3125 design group',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
import pypdfium2 as pdfium
pdf=pdfium.PdfDocument(out);count=len(pdf);assert count==7,f'Unexpected pagination: {count} A4 pages, expected 7. Inspect overflow.'
record={'status':'draft requires visual review and final assembly' if draft else 'main narrative generated; final assembly and visual review required','page_count':count,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'auxiliary_result_sha256':hashlib.sha256(aux_path.read_bytes()).hexdigest(),'formal_CAD_not_yet_appended':True}
out.with_suffix('.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
