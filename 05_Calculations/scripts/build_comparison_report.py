"""Modular undergraduate report: TNR12, numbered hierarchy, consistent figure/table styles."""
from pathlib import Path
import sys,json,hashlib,html
root=Path(__file__).resolve().parents[2]
helpers=(root/'05_Calculations/scripts/build_review_report.py').read_text().split('story=[]')[0]
helpers=helpers.replace("'arial.ttf'","'times.ttf'").replace("'arialbd.ttf'","'timesbd.ttf'")
helpers=helpers.replace('Native results; no interpolation','').replace('One coloured cell per desk','').replace('Furniture: proposed design','')
exec(compile(helpers,'shared_report_helpers','exec'))
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.platypus import KeepTogether
folder=root/'05_Calculations/Final_v04';folder.mkdir(exist_ok=True)
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
story=[]
def para(i,j):story.append(P(content['pages'][i]['paragraphs'][j].replace('lighting layout on page 7','lighting layout on page 9').replace('Figure 4 maps','Figure 3 maps').replace('Figure 2 shows the resulting room model','Figure 1 shows the resulting room model')))
def sub(title):story.append(P(title,h2))
def page(title):
 if story:story.append(PageBreak())
 story.append(P(title,heading))
def image(name,width):
 from PIL import Image as PILImage
 p=root/'05_Calculations/Final_v03/figures'/name
 with PILImage.open(p) as im:w,h=im.size
 return Image(str(p),width=width,height=width*h/w)
def figure(mode,title,factor=.90):
 d=map_figure(mode);d.scale(factor,factor);d.height*=factor
 story.append(KeepTogether([d,P(title,caption)]))
def classic_table(title,rows,widths):
 values=[[P(c,ParagraphStyle('cellhead',parent=small,fontName='Bold') if i==0 else small) for c in row] for i,row in enumerate(rows)]
 t=Table(values,colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),light),('LINEABOVE',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,0),(-1,0),.5,colors.black),('LINEBELOW',(0,-1),(-1,-1),.7,colors.black),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 story.extend([P(title,ParagraphStyle('tablecaption',parent=small,fontName='Bold',keepWithNext=True,spaceAfter=6)),t,Spacer(1,8)])
def footer(c,doc):
 c.setFont('Body',9);c.setFillColor(colors.black);c.drawCentredString(A4[0]/2,34,str(doc.page))
story.extend([P(content['title'],ParagraphStyle('title',parent=heading,fontSize=22,leading=26,alignment=TA_CENTER,spaceAfter=5)),P(content['subtitle'],ParagraphStyle('subtitle',parent=small,fontSize=12,leading=15,alignment=TA_CENTER,spaceAfter=8))])
group=load(root/'05_Calculations/local/group-details.json')
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
story.extend([image('native-room-view.png',165),P('Figure 1. DIALux model with recessed luminaires and full-height columns.',caption)])
sub('2.2 Task-area calculation');para(1,2)
sub('2.3 Maintenance factor and glare');para(1,3);para(1,4)
page('3. Luminaire selection and lighting layout');sub('3.1 Selected luminaire');para(2,0)
sub('3.2 Ceiling coordination and light distribution');para(2,1)
d=map_figure('basis');d.scale(.58,.58);d.height*=.58
combined=Table([[d,image('manufacturer-polar.png',110)]],colWidths=[W*.73,W*.27],hAlign='LEFT')
combined.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
story.extend([combined,P('Figure 2. Proposed lighting layout (left) and manufacturer light distribution (right) [2].',caption)])
sub('3.3 Output selection and installation');para(2,2);para(2,3)
page('4. Simulation results and interpretation');sub('4.1 Distribution of task illumination');para(3,0)
figure('tasks','Figure 3. Maintained desk-average illuminance, with the controlling desks identified.',.90)
sub('4.2 Desks with the lowest lighting levels and highest glare');para(3,1)
story.extend([image('native-desk021-isolux.png',265),P('Figure 4. Illuminance at Desk-021: average 593 lx, minimum 525 lx, uniformity 0.89.',caption)])
page('5. Comparison with lighting requirements');story.append(P('Table 2 compares the DIALux results with EN 12464-1:2021 and the lighting power limit in BEC 2024. The office activity and room assumptions are described in Section 1.'))
classic_table('Table 2. Design criteria and assessed performance.',[['Quantity / source','Adopted criterion','Result'],['Desk mean [1, Table 34]','>=500 lx','Minimum 593 lx'],['Task uniformity [1, Table 34]','Uo >=0.60','Minimum 0.80'],['Directional glare [1, Table 34]','UGR <=19','Maximum 18.1'],['Colour rendering [1], [2]','Ra >=80','Ra >80, manufacturer'],['Seated cylindrical [1, Sec. 5.6.2]','150 lx; Uo >=0.10','Minimum mean 224 lx; Uo bound >=0.59'],['Immediate surroundings [1, Sec. 5.3.4]','300 lx; Uo >=0.40','Minimum mean 595 lx; bound >=0.64'],['Background floor [1, Sec. 5.3.5]','100 lx; Uo >=0.10','Mean 617 lx; Uo 0.69'],['Exposed walls [1, Table 34]','150 lx; Uo >=0.10','Minimum mean 216 lx; bound >=0.24'],['Exposed ceiling [1, Table 34]','100 lx; Uo >=0.10','Mean 137 lx; Uo 0.89'],['Office LPD [6, Table 5.4]','<=7.2 W/m2','4.235 W/m2']],[W*.36,W*.27,W*.37])
sub('5.1 Illuminance and uniformity');story.append(P('The desks meet the average illuminance and uniformity targets. The surrounding and background areas also meet their lower illuminance requirements, so the change in lighting level outside the desks is considered as well. Walls and ceiling are checked because their brightness affects the appearance of the room. For groups of calculation surfaces, the uniformity bound in Table 2 is the lowest point illuminance divided by the highest surface average, rounded down. This gives a conservative value for the group.'))
sub('5.2 Glare and colour rendering');story.append(P('The maximum calculated UGR is below 19 for the seated positions and viewing directions tested. Colour rendering is taken from the manufacturer data. These results apply to the office tasks and arrangement described here; a different activity, such as unusually fine or low-contrast work, could require a higher lighting level.'))
page('6. Lighting controls and energy use');sub('6.1 Local and automatic control');para(4,0);para(4,1)
figure('zones','Figure 5. Independent bench and circulation control zones.',.80)
sub('6.2 Daylight response');para(4,2)
sub('6.3 Connected power');para(4,3)
story.append(P('The proposed 46.67 m2 maximum zone is below 250 m2; the 10-minute vacancy delay and 120-minute override meet the adopted 15-minute and two-hour limits respectively (BEC 5.6.1.3-5). The required standby-inclusive automatic power reduction is at least 50% (5.6.1.1).',small))
page('7. Design comparison and conclusion')
sub('7.1 Comparison of calculation conditions')
story.append(P(content['comparison']['method']))
comparison={'cases':[dict(name=name,**load(root/'05_Calculations/data'/file)) for name,file in [('Baseline','review-40s-reopened-tasks-v4.json'),('90% output','comparison-output90-core-reopened-results-v1.json'),('Lower reflectance','comparison-reflectance-core-reopened-results-v1.json')]]}
rows=[['Case','Lowest desk mean','Lowest Uo','Highest UGR']]
for c in comparison['cases']:
 rows.append([c['name'],f"{c['minimum_task_average_lx']:.0f} lx",f"{c['minimum_task_u0']:.2f}",f"{c['maximum_directional_ugr']:.1f}"])
classic_table('Table 3. Workstation results for the three calculation conditions.',rows,[W*.34,W*.25,W*.20,W*.21])
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
p=pdfium.PdfDocument(out);assert len(p)==8,f'Unexpected narrative pagination: {len(p)}';p.close()
(folder/'format-specification.json').write_text(json.dumps({'font':'Times New Roman','body_pt':12,'leading_pt':15,'side_margins_mm':25.4,'top_bottom_margins_mm':62*25.4/72,'numbered_section_and_subsection_hierarchy':True,'table_font_pt':10,'figure_captions':'10pt Times New Roman Italic below figure','table_titles':'10pt Times New Roman Bold above table','narrative_pages':8,'status':'comparison revision; engineering results require acceptance','guidance':['https://students.unimelb.edu.au/academic-skills/reading-writing-and-referencing/reports/technical-report-writing','https://www.sussex.ac.uk/webteam/gateway/file.php?name=technical-writing&site=23']},indent=2))
print('Eight-page modular Times New Roman narrative generated')
