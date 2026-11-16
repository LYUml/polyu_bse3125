"""One-page comparison module using the actual native result summary."""
from pathlib import Path
import json,sys,html,math
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import pypdfium2 as pdfium
r=Path(__file__).resolve().parents[2];folder=r/'05_Calculations/Final_v04';out=Path(sys.argv[1]);assert not out.exists()
summary=json.loads((folder/'comparison-summary.json').read_text());content=json.loads((folder/'content.json').read_text())
for alias,file in [('Body','times.ttf'),('Bold','timesbd.ttf')]:pdfmetrics.registerFont(TTFont(alias,'C:/Windows/Fonts/'+file))
body=ParagraphStyle('body',fontName='Body',fontSize=12,leading=15,spaceAfter=8)
small=ParagraphStyle('small',parent=body,fontSize=10,leading=12,spaceAfter=5)
h=ParagraphStyle('h',parent=body,fontName='Bold',fontSize=15,leading=19,spaceAfter=12)
h2=ParagraphStyle('h2',parent=body,fontName='Bold',spaceBefore=8,spaceAfter=6)
P=lambda t,style=body:Paragraph(html.escape(str(t)),style)
story=[P('Appendix C. Comparison calculations',h),P('C.1 Calculation conditions',h2),P('The baseline uses full output and ceiling/wall/floor reflectances of 80/70/20%. Case B changes only the scene output to 90%. Case C keeps full output and changes reflectances to 70/50/20%. All cases retain 186 luminaires, the same positions, desk surfaces, glare directions, columns and maintenance factor of 0.80. Each comparison was calculated in DIALux, saved and reopened.'),P('C.2 Lighting outside the desk plane',h2),P('Table C1. Auxiliary illuminance and uniformity comparisons.',small)]
rows=[['Area / quantity','Criterion','Baseline','B: 90%','C: 70/50/20']]
for key,label in [('desk cylindrical','Seated cylindrical'),('immediate surrounding','Immediate surround'),('background floor','Background'),('exposed walls','Walls'),('exposed ceiling','Ceiling')]:
    cs=[c['combined_seated_cylindrical'] if key=='desk cylindrical' else c['auxiliary_checks'][key] for c in summary['cases']]
    rows.append([label,f"{cs[0]['average_target_lx']:.0f} / {cs[0]['u0_target']:.2f}"]+[f"{c['minimum_surface_average_lx']:.0f} / {math.floor(c['conservative_combined_u0_lower_bound']*100)/100:.2f}" for c in cs])
t=Table([[P(c,small) for c in row] for row in rows],colWidths=[119,82,82,82,A4[0]-144-365],repeatRows=1)
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#F1F1F1')),('LINEABOVE',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,0),(-1,0),.5,colors.black),('LINEBELOW',(0,-1),(-1,-1),.7,colors.black),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story.extend([t,Spacer(1,7),P('Values are minimum surface-average illuminance (lx) / conservative uniformity bound. The bound is the lowest point illuminance divided by the highest surface average in the group, rounded down. Seated cylindrical results cover the desks and surrounding bands. Each case includes all 288 auxiliary result rows.',small),P('C.3 Interpretation and limits',h2)])
for text in content['comparison']['appendix']:story.append(P(text))
story.extend([P('C.4 Selected DIALux outputs',h2),P(content['comparison']['evidence_note'],small)])
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=72,rightMargin=72,topMargin=62,bottomMargin=62,title='BSE3125 comparison calculations')
doc.build(story)
p=pdfium.PdfDocument(out);assert len(p)==1,len(p);p.close();print('One-page comparison appendix created')
