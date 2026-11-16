"""First student-facing editorial draft; reuse verified diagrams and native result data."""
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parents[2]
# Reuse existing ReportLab helpers only; do not execute its report-building section.
source=(root/'05_Calculations/scripts/build_review_report.py').read_text()
exec(compile(source.split('story=[]')[0],str(root/'05_Calculations/scripts/build_review_report.py'),'exec'))
folder=root/'05_Calculations/Report_Draft_v01';content=load(folder/'content.json');story=[]
body.fontSize=10.5;body.leading=15;body.spaceAfter=10
heading.fontSize=18;heading.leading=23
def footer(c,doc):
 c.setStrokeColor(teal);c.line(44,40,A4[0]-44,40);c.setFont('Body',7);c.setFillColor(grey)
 c.drawString(44,27,'BSE3125 | First report draft - for discussion');c.drawRightString(A4[0]-44,27,str(doc.page))
def image(name,width):
 from PIL import Image as PILImage
 p=root/'05_Calculations/Final_v03/figures'/name
 with PILImage.open(p) as im:w,h=im.size
 return Image(str(p),width=width,height=width*h/w)
def paragraphs(index):
 for s in content['pages'][index]['paragraphs']:story.append(P(s))
for i,page in enumerate(content['pages']):
 if i:story.append(PageBreak())
 if i==0:story.extend([P(content['title'],heading),P(content['subtitle'],caption)])
 story.append(P(page['title'],heading))
 if i==0:story.extend([map_figure('basis'),P('Figure 1. Proposed desk and luminaire arrangement; grey blocks indicate columns.',caption)])
 if i==1:
  paragraphs(i);story.extend([image('native-room-view.png',300),P('Figure 2. DIALux room model showing the recessed luminaires and full-height columns.',caption)]);continue
 if i==2:
  paragraphs(i);story.extend([image('manufacturer-polar.png',150),P('Figure 3. Manufacturer polar intensity distribution for the selected luminaire [4].',caption)]);continue
 if i==3:
  figure=map_figure('tasks');figure.scale(.80,.80);figure.height*=.80
  story.extend([figure,P('Figure 4. Maintained desk-average illuminance (lx), with the three controlling desks identified.',caption)]);paragraphs(i)
  rows=[['Quantity / reference','Adopted criterion','Calculated result'],['Desk average [2], Table 34','>=500 lx','Minimum 593 lx'],['Desk uniformity [2], Table 34','Uo >=0.60','Minimum 0.80'],['Directional glare [2], Table 34','UGR <=19','Maximum 18.1'],['Colour rendering [2,4]','Ra >=80','Manufacturer Ra >80'],['Seated cylindrical [2], 5.6.2','150 lx; Uo >=0.10','Minimum mean 224 lx; Uo bound >=0.59'],['Surroundings [2], 5.3.4','300 lx; Uo >=0.40','Minimum mean 595 lx; Uo bound >=0.64'],['Background [2], 5.3.5','100 lx; Uo >=0.10','Mean 617 lx; Uo 0.69'],['Walls / ceiling [2], Table 34','150 / 100 lx; Uo >=0.10','Minimum means 216 / 137 lx; bounds >=0.24 / 0.89'],['Office LPD [5], Table 5.4','<=7.2 W/m2','4.235 W/m2']]
  story.append(table(rows,[W*.34,W*.28,W*.38]));story.append(P('For grouped surfaces, the Uo bound is the smallest point minimum divided by the largest region mean, rounded down. EN 12464-1:2021 is applied to the stated ordinary office task assumptions; colour rendering is manufacturer-declared.',small));continue
 if i==4:
  story.extend([map_figure('zones'),P('Figure 5. Proposed independently controlled bench and circulation zones.',caption)]);paragraphs(i)
  story.append(P('BEC 2024 basis: Table 5.5 manual points; 5.6.1.1 automatic power reduction; 5.6.1.3 zone area <=250 m2; 5.6.1.4 override <=2 h; 5.6.1.5 vacancy <=15 min. Proposed values are 32 points, >=50% reduction, 46.67 m2, 120 min and 10 min respectively. Daylight controls remain subject to facade review.',small));continue
 paragraphs(i)
 if i==5:
  story.append(P('References',heading))
  refs=load(root/'05_Calculations/Final_v03/report-content-v3.json')['references']
  for ref in refs:
   story.append(P(f"[{ref['id']}] {ref['title']}. "+ref.get('scope',''),small))
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=52,title=content['title']+' - first draft',author='BSE3125 design group')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
p=pdfium.PdfDocument(out);assert len(p)==6,f'Unexpected narrative overflow: {len(p)}';p.close()
print('Six-page narrative draft built:',out)
