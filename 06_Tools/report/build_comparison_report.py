"""Modular undergraduate report: TNR12, numbered hierarchy, consistent figure/table styles."""
from pathlib import Path
import sys,json,hashlib,html
from io import BytesIO
root=Path(__file__).resolve().parents[2]
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
import pypdfium2 as pdfium
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
out=Path(sys.argv[1]);assert not out.exists()
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.platypus import KeepTogether
folder=root/'04_Report';folder.mkdir(exist_ok=True)
content=load(folder/'content.json')
for alias,file in [('Body','times.ttf'),('Bold','timesbd.ttf'),('Italic','timesi.ttf')]:pdfmetrics.registerFont(TTFont(alias,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
navy=colors.black;grey=colors.HexColor('#444444');teal=colors.black;light=colors.HexColor('#F1F1F1');W=A4[0]-144
body=ParagraphStyle('classicbody',fontName='Body',fontSize=12,leading=15,spaceAfter=8,alignment=TA_JUSTIFY,textColor=colors.black)
small=ParagraphStyle('classicsmall',parent=body,fontSize=10,leading=12,spaceAfter=5,alignment=0)
heading=ParagraphStyle('classicH1',parent=body,fontName='Bold',fontSize=15,leading=19,spaceBefore=0,spaceAfter=13,keepWithNext=True,alignment=0)
h2=ParagraphStyle('classicH2',parent=body,fontName='Bold',fontSize=12,leading=15,spaceBefore=8,spaceAfter=6,keepWithNext=True,alignment=0)
caption=ParagraphStyle('classiccaption',parent=small,fontName='Italic',alignment=TA_CENTER,spaceBefore=5,spaceAfter=10)
P=lambda s,style=body:Paragraph(html.escape(str(s)).replace('m2','m<super>2</super>').replace('&gt;=','&#8805;').replace('&lt;=','&#8804;'),style)
from report_figures import layout_polar,task_map,zone_map,calculation_heights
story=[]
def para(i,j):story.append(P(content['pages'][i]['paragraphs'][j]))
def sub(title):story.append(P(title,h2))
def page(title):
 if story:story.append(PageBreak())
 story.append(P(title,heading))
def image(name,width):
 from PIL import Image as PILImage
 p=root/'04_Report/Assets'/name
 with PILImage.open(p) as im:w,h=im.size
 return Image(str(p),width=width,height=width*h/w)
def native_crop(source, number, bounds, width):
 page=source[number-1]
 w,h=page.get_size()
 x0,y0,x1,y1=bounds
 img=page.render(scale=2,crop=(w*x0,h*(1-y1),w*(1-x1),h*y0)).to_pil()
 buffer=BytesIO()
 img.save(buffer,format='PNG')
 return Image(buffer,width=width,height=width*img.height/img.width)
def classic_table(title,rows,widths):
 values=[[P(c,ParagraphStyle('cellhead',parent=small,fontName='Bold') if i==0 else small) for c in row] for i,row in enumerate(rows)]
 t=Table(values,colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),light),('LINEABOVE',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,0),(-1,0),.5,colors.black),('LINEBELOW',(0,-1),(-1,-1),.7,colors.black),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 story.extend([P(title,ParagraphStyle('tablecaption',parent=small,fontName='Bold',keepWithNext=True,spaceAfter=6)),t,Spacer(1,8)])
def footer(c,doc):
 c.setFont('Body',9);c.setFillColor(colors.black);c.drawCentredString(A4[0]/2,34,str(doc.page))
story.extend([P(content['title'],ParagraphStyle('title',parent=heading,fontSize=22,leading=26,alignment=TA_CENTER,spaceAfter=5)),P(content['subtitle'],ParagraphStyle('subtitle',parent=small,fontSize=12,leading=15,alignment=TA_CENTER,spaceAfter=8))])
group=load(root/'04_Report/Private/group-details.json')
story.append(P(group['group'],ParagraphStyle('group',parent=small,fontName='Bold',alignment=TA_CENTER)))
members=sorted(group['members'],key=lambda m:m['name'].casefold())
member_style=ParagraphStyle('members',parent=small,alignment=TA_CENTER,spaceAfter=1)
for row in [members[:3],members[3:]]:
 labels=[m['name']+' '+m['student_id'] for m in row]
 assert sum(pdfmetrics.stringWidth(s,'Body',10) for s in labels)+18*(len(labels)-1)<=W
 story.append(Paragraph(('&#160;'*7).join(html.escape(s) for s in labels),member_style))
story.append(Spacer(1,8))
story.append(P('1. Introduction and design basis',heading));sub('1.1 Design objective');para(0,0)
sub('1.2 Office geometry and proposed use');para(0,1);para(0,2)
sub('1.3 Room conditions');story.append(P('Table 1 gives the main assumptions used in DIALux. The relatively light ceiling and walls contribute reflected light to the desks. Daylight is excluded because the window dimensions are not given. Section 7 considers changes to these conditions.'))
classic_table('Table 1. Principal room and calculation assumptions.',[['Parameter','Adopted value'],['Ceiling / desk / seated eye height','2.8 / 0.8 / 1.2 m'],['Ceiling / wall / floor reflectance','80 / 70 / 20%'],['Column reflectance / maintenance factor','40% / 0.80'],['Furniture and daylight','Proposed desks; no high partitions or simulated daylight']],[W*.50,W*.50])
page('2. DIALux modelling and simulation');sub('2.1 Geometry and manufacturer photometry');para(1,0);para(1,1)
model_views=Table([[image('native-room-view.png',200),calculation_heights()]],colWidths=[W*.5,W*.5],hAlign='LEFT')
model_views.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
story.extend([model_views,P('Figure 1. Native room view (left) and adopted calculation heights (right).',caption)])
sub('2.2 Task-area calculation');para(1,2)
sub('2.3 Maintenance factor and glare');para(1,3);para(1,4)
page('2.4 Native DIALux documentation')
story.append(P('The automatic whole-room plane reports 640 lx and Uo = 0.002 with a zero wall offset. This low uniformity rules out a claim of uniform task lighting everywhere. The adopted assessment covers the proposed desk positions, their surroundings and the accessible background. A revised seating plan requires a new desk assessment.'))
native=pdfium.PdfDocument(root/'03_Engineering/Native_Reports/Final_Workstations.pdf')
story.append(native_crop(native,529,(.14,.31,.95,.63),W*.83))
native.close()
story.append(P('Figure 2. Desk-021 calculation grid and isolux contours. Native workstation report, page 529.',caption))
sub('Reading the local result')
story.append(P('Each point samples the same horizontal task surface. With a mean of 593 lx and a minimum of 525 lx, Desk-021 has Uo = 525/593 = 0.89. Its low mean governs the illuminance margin. Desk-084 governs uniformity. This distinction would be lost in a room-wide average.'))
sub('Spacing and lumen-method checks')
story.append(P('For a typical 2.4 m spacing and a nominal 2.0 m height above the desk plane, SHR is about 1.20. Local spacings vary at columns and edges. The desk grids directly check uniformity at those locations. Using N = E x A / (flux x UF x MF), 186 fittings would require UF = 0.875 to average 500 lx over the whole 1042.10 m2 at MF 0.80. This is a threshold calculation. The L-shaped room and the individual desk criteria are assessed with the native model.'))
page('3. Luminaire selection and lighting layout');sub('3.1 Selected luminaire');para(2,0)
sub('3.2 Ceiling coordination and light distribution')
story.append(P('The 597 x 597 mm fitting occupies one 600 mm ceiling tile. Typical spacing is 2.4 m, with adjustments at columns and edges. The broad downward distributions in Figure 3 support overlap at desk height.'))
story.extend([layout_polar(W),P('Figure 3. Ceiling layout (a) and principal light distributions from the manufacturer LDT (b) [2].',caption)])
sub('3.3 Output selection and installation')
classic_table('Table 2. Manufacturer ratings and modelled layout choices.',[
 ['Luminaire','Count','lm / W per fitting','Catalogue UGR','Connected kW*'],
 ['CoreLine [7]','142','4300 / 32','19','4.54'],
 ['PowerBalance 34S [8]','186','3400 / 20','16','3.72'],
 ['PowerBalance 40S [2]','186','4000 / 23','16','4.28'],
], [W*.33,W*.10,W*.20,W*.18,W*.19])
story.append(P('*Luminaire input only. The CoreLine trial used the automatic working plane and a different layout. At the same 186 positions, 34S and 40S gave 504 lx and 593 lx as their lowest desk means, respectively.',small))
story.append(P(content['pages'][2]['paragraphs'][3],small))
page('4. Simulation results and interpretation');sub('4.1 Distribution of task illumination');para(3,0)
story.extend([task_map(W),P('Figure 4. Desk-average illuminance; A, B and C identify the three controlling desks.',caption)])
sub('4.2 Desks with the lowest lighting levels and highest glare');para(3,1)
for explanation in content['critical_desks']:
 story.append(P(explanation))
story.append(P('Appendix A includes the native task contours and directional glare result. The automatic WP1 surface samples the wider room, including column footprints. The 112 explicit desk surfaces define the task-area check for the proposed furniture plan.',small))
page('5. Comparison with lighting requirements');story.append(P('Table 3 compares the DIALux results with EN 12464-1:2021 and the lighting power limit in BEC 2024. The office activity and room assumptions are described in Section 1.'))
classic_table('Table 3. Adopted requirements and calculated performance.',[
 ['Quantity','Requirement','Calculated result'],
 ['Desk mean','>=500 lx','Lowest mean: 593 lx'],
 ['Desk uniformity','Uo >=0.60','Lowest Uo: 0.80'],
 ['Directional glare','UGR <=19','Highest UGR: 18.1'],
 ['Colour rendering','Ra >=80','Ra >80 (manufacturer)'],
 ['Seated cylindrical','>=150 lx; Uo >=0.10','224 lx; Uo >=0.59*'],
 ['Immediate surround','>=300 lx; Uo >=0.40','595 lx; Uo >=0.64*'],
 ['Background floor','>=100 lx; Uo >=0.10','617 lx; Uo =0.69'],
 ['Exposed walls','>=150 lx; Uo >=0.10','216 lx; Uo >=0.24*'],
 ['Exposed ceiling','>=100 lx; Uo >=0.10','137 lx; Uo =0.89'],
 ['Lighting power density','<=7.2 W/m2','4.153 W/m2 including allowance'],
 ['Manual control points','>=32 for 1042.10 m2','32 proposed'],
 ['Occupancy shutoff','<=15 min','10 min specified'],
 ['Daylight response','Conditional on glazing and load','Pending glazing survey']], [W*.30,W*.34,W*.36])
story.append(P('Sources: [1, Table 34, row 34.2 and clauses 5.3.4-5.3.5, 5.6.2]; [2] for colour rendering; [6, Tables 5.4-5.5 and clauses 5.6.1-5.6.2] for energy and controls. *Conservative uniformity bound across a group.',small))
sub('5.1 Illuminance and uniformity');story.append(P('The background floor receives 617 lx against a 100 lx target. The regular ceiling grid delivers more light than required in circulation. The four circulation zones allow reduced output to be tested against the background and nearby task criteria. Group uniformity bounds use the lowest point divided by the highest surface mean, rounded down.'))
sub('5.2 Glare and screen reflections');story.append(P('The highest directional UGR is 18.1 in the baseline. The LDT check scales intensity to 4000 lm and divides by the projected area of the 510 x 510 mm aperture. The highest sampled luminance is 1334 cd/m2 (C44, gamma 65 degrees). EN clause 5.9.2 and Table 7 set 1500 cd/m2 for Case A medium-luminance screens (high state up to 200 cd/m2) tilted up to 15 degrees from vertical [1]. The check covers sampled angles from 65 to 89 degrees. Projection is undefined at 90 degrees. Confirm screen type, tilt and orientation at fit-out.'))
page('6. Lighting controls and energy use');sub('6.1 Local and automatic control');para(4,0);para(4,1)
story.extend([zone_map(W),P('Figure 5. Proposed independent lighting control zones.',caption)])
sub('6.2 Daylight response');para(4,2)
sub('6.3 Connected power');para(4,3)
page('7. Design comparison and conclusion')
sub('7.1 Comparison of calculation conditions')
story.append(P(content['comparison']['method']))
comparison=load(folder/'comparison-summary.json')
rows=[['Case','Lowest desk mean','Lowest Uo','Highest UGR'],['Requirement','>=500 lx','>=0.60','<=19']]
for c in comparison['cases']:
 rows.append([c['name'],f"{c['minimum_task_average_lx']:.0f} lx",f"{c['minimum_task_u0']:.2f}",f"{c['maximum_directional_ugr']:.1f}"])
classic_table('Table 4. Workstation results by calculation condition.',rows,[W*.34,W*.25,W*.20,W*.21])
sub('7.2 Design choice')
for text in content['comparison']['interpretation']:story.append(P(text))
sub('7.3 Maintenance and conclusion')
for text in content['comparison']['conclusion']:story.append(P(text))
page('References')
refs=content['references']
reference_style=ParagraphStyle('reference',parent=body,fontSize=11,leading=14,alignment=0,spaceAfter=0,splitLongWords=False)
for ref in refs:
 text=ref['html']
 if ref['id']!=1:
  url=html.escape(ref['url'],quote=True)
  import re
  raw=ref['url'];parts=[]
  while pdfmetrics.stringWidth(raw,'Body',11)>W-25:
   breaks=[i for i in range(1,len(raw)) if raw[i-1]=='/' or raw[i] in '-_?&=']
   valid=[i for i in breaks if pdfmetrics.stringWidth(raw[:i],'Body',11)<=W-25]
   assert valid,'URL has no safe line break'
   stop=max(valid);parts.append(raw[:stop]);raw=raw[stop:]
  parts.append(raw)
  display='<br/>'.join(html.escape(part) for part in parts)
  text+='<br/><link href="'+url+'">'+display+'</link>'
 entry=Table([[P('['+str(ref['id'])+']',reference_style),Paragraph(text,reference_style)]],colWidths=[25,W-25],hAlign='LEFT')
 entry.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
 story.extend([entry,Spacer(1,13)])

doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=72,rightMargin=72,topMargin=62,bottomMargin=62,title='BSE3125 - Lighting Design Report',author='BSE3125 design group')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
p=pdfium.PdfDocument(out);assert len(p)==9,f'Unexpected narrative pagination: {len(p)}';p.close()
print('Nine-page modular Times New Roman narrative generated')
