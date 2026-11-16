"""Modular undergraduate report: TNR12, numbered hierarchy, consistent figure/table styles."""
from pathlib import Path
import sys,json,hashlib,html
root=Path(__file__).resolve().parents[2]
helpers=(root/'05_Calculations/scripts/build_review_report.py').read_text().split('story=[]')[0]
helpers=helpers.replace("'arial.ttf'","'times.ttf'").replace("'arialbd.ttf'","'timesbd.ttf'")
exec(compile(helpers,'shared_report_helpers','exec'))
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.platypus import KeepTogether
folder=root/'05_Calculations/Report_Draft_v02';folder.mkdir(exist_ok=True)
content=load(root/'05_Calculations/Report_Draft_v01/content.json')
for alias,file in [('Body','times.ttf'),('Bold','timesbd.ttf'),('Italic','timesi.ttf')]:pdfmetrics.registerFont(TTFont(alias,'C:/Windows/Fonts/'+file))
navy=colors.black;grey=colors.HexColor('#444444');teal=colors.black;light=colors.HexColor('#F1F1F1');W=A4[0]-144
body=ParagraphStyle('classicbody',fontName='Body',fontSize=12,leading=15,spaceAfter=8,alignment=TA_JUSTIFY,textColor=colors.black)
small=ParagraphStyle('classicsmall',parent=body,fontSize=10,leading=12,spaceAfter=5,alignment=0)
heading=ParagraphStyle('classicH1',parent=body,fontName='Bold',fontSize=15,leading=19,spaceBefore=0,spaceAfter=13,keepWithNext=True,alignment=0)
h2=ParagraphStyle('classicH2',parent=body,fontName='Bold',fontSize=12,leading=15,spaceBefore=8,spaceAfter=6,keepWithNext=True,alignment=0)
caption=ParagraphStyle('classiccaption',parent=small,fontName='Italic',alignment=TA_CENTER,spaceBefore=5,spaceAfter=10)
P=lambda s,style=body:Paragraph(html.escape(str(s)),style)
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
story.extend([P('Lighting Design for an Open-plan Office',ParagraphStyle('title',parent=heading,fontSize=19,leading=23,alignment=TA_CENTER)),Spacer(1,18)])
story.append(P('1. Introduction and design basis',heading));sub('1.1 Design objective');para(0,0)
sub('1.2 Office geometry and proposed use');para(0,1);para(0,2)
sub('1.3 Calculation assumptions');story.append(P('Table 1 summarises the principal model assumptions. Light ceiling and wall finishes support reflected illumination; darker finishes would require the design to be recalculated. No daylight contribution is credited because the glazing dimensions are unavailable.'))
classic_table('Table 1. Principal room and calculation assumptions.',[['Parameter','Adopted value'],['Ceiling / desk / seated eye height','2.8 / 0.8 / 1.2 m'],['Ceiling / wall / floor reflectance','80 / 70 / 20%'],['Column reflectance / maintenance factor','40% / 0.80'],['Furniture and daylight','Proposed desks; no high partitions or simulated daylight']],[W*.50,W*.50])
page('2. DIALux modelling and simulation');sub('2.1 Geometry and manufacturer photometry');para(1,0);para(1,1)
story.extend([image('native-room-view.png',165),P('Figure 1. DIALux model with recessed luminaires and full-height columns.',caption)])
sub('2.2 Task-area calculation');para(1,2)
sub('2.3 Maintenance, glare and additional checks');para(1,3);para(1,4)
page('3. Luminaire selection and lighting layout');sub('3.1 Selected luminaire');para(2,0)
sub('3.2 Ceiling coordination and light distribution');para(2,1)
figure('basis','Figure 2. Proposed workstations and ceiling-grid luminaire arrangement.',.85)
sub('3.3 Output selection and installation');para(2,2);para(2,3)
page('4. Simulation results and interpretation');sub('4.1 Distribution of task illumination');para(3,0)
figure('tasks','Figure 3. Maintained desk-average illuminance, with the controlling desks identified.',.90)
sub('4.2 Limiting workstations');para(3,1)
story.extend([image('native-desk021-isolux.png',265),P('Figure 4. Desk-021 native isolux output: 593 lx mean, 525 lx minimum, Uo 0.89.',caption)])
story.append(P('Appendix A contains the native room summary and the controlling glare, illuminance and uniformity outputs. Their original DIALux page numbers are retained.'))
page('5. Comparison with lighting criteria');story.append(P('Table 2 compares the selected international lighting criteria and local energy criterion with the simulation results. The assessment applies to ordinary office tasks and the assumptions in Table 1.'))
classic_table('Table 2. Design criteria and assessed performance.',[['Quantity / source','Adopted criterion','Result'],['Desk mean [2], Table 34','>=500 lx','Minimum 593 lx'],['Task uniformity [2], Table 34','Uo >=0.60','Minimum 0.80'],['Directional glare [2], Table 34','UGR <=19','Maximum 18.1'],['Colour rendering [2,4]','Ra >=80','Ra >80, manufacturer'],['Seated cylindrical [2], 5.6.2','150 lx; Uo >=0.10','Minimum mean 224 lx; Uo bound >=0.59'],['Immediate surroundings [2], 5.3.4','300 lx; Uo >=0.40','Minimum mean 595 lx; bound >=0.64'],['Background floor [2], 5.3.5','100 lx; Uo >=0.10','Mean 617 lx; Uo 0.69'],['Exposed walls [2], Table 34','150 lx; Uo >=0.10','Minimum mean 216 lx; bound >=0.24'],['Exposed ceiling [2], Table 34','100 lx; Uo >=0.10','Mean 137 lx; Uo 0.89'],['Office LPD [5], Table 5.4','<=7.2 W/m2','4.235 W/m2']],[W*.36,W*.27,W*.37])
sub('5.1 Interpretation of the comparison');story.append(P('The task results meet all three adopted illuminance, uniformity and directional glare criteria. The supplementary surface checks also satisfy their selected limits. For a group of regions, the reported uniformity bound is the smallest point minimum divided by the largest individual region mean, rounded down. This provides a conservative combined bound without averaging regional uniformities.'))
sub('5.2 Assessment scope');story.append(P('The manufacturer declares colour rendering, whereas illuminance and room UGR are calculated in DIALux. The selected 500 lx target applies to the stated ordinary office activity; more demanding tasks or different occupant needs would require the design basis to be reviewed. The comparison represents modelled performance rather than an installed-system certificate.'))
page('6. Lighting controls and energy use');sub('6.1 Local and automatic control');para(4,0);para(4,1)
figure('zones','Figure 5. Independent bench and circulation control zones.',.80)
sub('6.2 Daylight response');para(4,2)
sub('6.3 Connected power');para(4,3)
story.append(P('The proposed 46.67 m2 maximum zone is below 250 m2; the 10-minute vacancy delay and 120-minute override meet the adopted 15-minute and two-hour limits respectively (BEC 5.6.1.3-5). The required standby-inclusive automatic power reduction is at least 50% (5.6.1.1).',small))
page('7. Discussion and conclusion');sub('7.1 Adequacy and opportunity for optimisation');para(5,0)
sub('7.2 Sensitivity to output and fit-out');para(5,1)
sub('7.3 Maintenance and visual comfort');para(5,2)
sub('7.4 Conclusion');para(5,3)
page('References and supporting information')
refs=load(root/'05_Calculations/Final_v03/report-content-v3.json')['references']
for ref in refs:
 story.append(P(f"[{ref['id']}] {ref['title']}. "+ref.get('scope',''),small))
 if 'url' in ref:story.append(Paragraph('<link href="'+html.escape(ref['url'],quote=True)+'">'+html.escape(ref['url'])+'</link>',ParagraphStyle('url',parent=small,fontSize=9,leading=11,wordWrap='CJK')))
story.extend([Spacer(1,10),image('manufacturer-polar.png',155),P('Figure 6. Manufacturer polar intensity distribution for the selected fitting [4]. The curve describes how light output varies with direction.',caption)])
classic_table('Table 3. Drawing and appendix navigation.',[['Item','Combined PDF page'],['L01: Independent A2 lighting layout','9'],['Appendix A: Room summary','10'],['Appendix A: Desk-018 maximum directional glare','11'],['Appendix A: Desk-021 minimum average illuminance','12'],['Appendix A: Desk-084 minimum uniformity','13'],['Appendix B: Background floor','14']],[W*.78,W*.22])
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=72,rightMargin=72,topMargin=62,bottomMargin=62,title='BSE3125 - Modular report draft',author='BSE3125 design group')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
p=pdfium.PdfDocument(out);assert len(p)==8,f'Unexpected narrative pagination: {len(p)}';p.close()
(folder/'format-specification.json').write_text(json.dumps({'font':'Times New Roman','body_pt':12,'leading_pt':15,'margins_mm':25.4,'numbered_section_and_subsection_hierarchy':True,'table_font_pt':10,'figure_captions':'10pt Times New Roman Italic below figure','table_titles':'10pt Times New Roman Bold above table','narrative_pages':8,'status':'draft for user evaluation; engineering unchanged','guidance':['https://students.unimelb.edu.au/academic-skills/reading-writing-and-referencing/reports/technical-report-writing','https://www.sussex.ac.uk/webteam/gateway/file.php?name=technical-writing&site=23']},indent=2))
print('Eight-page modular Times New Roman narrative generated')
