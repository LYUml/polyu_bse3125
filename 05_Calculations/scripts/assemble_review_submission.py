"""Assemble a review PDF without changing native appendix/CAD page content."""
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'06_Tools/.runtime'))
import pikepdf,pypdfium2 as pdfium
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
root=Path(__file__).resolve().parents[2];folder=root/'05_Calculations/Final_v03'
out=Path(sys.argv[1]);assert not out.exists()
out.parent.mkdir(parents=True,exist_ok=True)
guide=out.with_name(out.stem+'-appendix-guide.pdf');assert not guide.exists()
main=Path(sys.argv[2]) if len(sys.argv)>2 else folder/'BSE3125-main-v3.pdf'
sections=[('Main report',main),('L01 - formal lighting layout',root/'05_Calculations/Final_v03/cad-plot-v5/BSE3125-L01-lighting-plan.pdf'),('Appendix guide',guide),('Appendix A - task illuminance, directional glare and fixture coordinates',folder/'DIALux-core-native-output-v3.pdf'),('Appendix B - cylindrical, surrounding, background and exposed surfaces',folder/'DIALux-brightness-native-output-v3.pdf')]
c=Canvas(str(guide),pagesize=A4,pageCompression=1);c.setTitle('Native DIALux output appendix guide')
c.setFillColorRGB(.08,.21,.31);c.setFont('Helvetica-Bold',22);c.drawString(44,780,'Simulation appendix')
c.setFont('Helvetica',11)
lines=[
 'Main report: combined pages 1-9, including the formal CAD layout.',
 'Appendix A: combined pages 11-153 (143 original native pages).',
 'Appendix B: combined pages 154-192 (39 original native pages).',
 '',
 'A. Task lighting, glare and coordinate evidence',
 'Manufacturer data; room summary; all 186 luminaire coordinates;',
 'all 112 desk illuminance rows; all 112 directional UGR result tables;',
 'critical UGR diagrams and task isolux plots.',
 '',
 'B. Additional visual-environment evidence',
 'Complete selected room calculation-object tables (288 result rows),',
 'critical cylindrical and surrounding plots, background floor,',
 'exposed ceiling and all six exposed wall plots.',
 '',
 'How to read the evidence',
 'Original DIALux page numbers remain on the reproduced pages.',
 'PDF bookmarks identify the main sections and critical native outputs.',
 'The two native projects use identical fixture positions and manufacturer',
 'photometry. The supplemental project adds surrounding, cylindrical',
 'and exposed-surface checks; directional UGR remains in the core project.',
 'Both projects were calculated, saved, closed and reopened.',
 '',
 'The general adaptive workplane is not the fixed task-area criterion.',
 'Task-area uniformity is assessed on the documented usable desks.',
 'Exposed surface regions exclude physical column/luminaire openings;',
 'they do not discard occupied task locations.',
 '',
 'These are original native output pages, not reconstructed result tables.',
 'Unused PDF resources were removed without changing page text, size',
 'or rendered content. Full raw PDFs and editable native projects are',
 'retained separately with their file hashes.'
]
y=742
for line in lines:
 c.setFont('Helvetica-Bold' if line.startswith(('A.','B.','How')) else 'Helvetica',11);c.drawString(44,y,line);y-=19
c.setStrokeColorRGB(0,.54,.58);c.line(44,40,A4[0]-44,40);c.setFont('Helvetica',8);c.drawString(44,27,'BSE3125 | Native simulation appendix');c.drawRightString(A4[0]-44,27,'10');c.showPage();c.save()
offsets=[];records=[]
with pikepdf.Pdf.new() as combined:
 for title,path in sections:
  start=len(combined.pages);offsets.append(start)
  with pikepdf.open(path) as source:
   combined.pages.extend(source.pages)
   records.append({'title':title,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'first_combined_page':start+1,'page_count':len(source.pages)})
 assert offsets==[0,8,9,10,153] and len(combined.pages)==192
 with combined.open_outline() as outline:
  for (title,_),offset in zip(sections,offsets):outline.root.append(pikepdf.OutlineItem(title,offset))
  for page,title in enumerate(['Design basis','DIALux method','Luminaire selection','Iteration and spatial performance','Criteria table','Controls and power','Robustness and maintenance','Conclusion and references']):outline.root[0].children.append(pikepdf.OutlineItem(title,page))
  core_manifest=json.loads((folder/'DIALux-core-native-output-v3.manifest.json').read_text())
  aux_manifest=json.loads((folder/'DIALux-brightness-native-output-v3.manifest.json').read_text())
  for native,title in [(254,'Native room summary'),(257,'All fixture coordinates'),(268,'All 112 task illuminance rows'),(282,'All 112 directional UGR tables'),(316,'Desk-018 maximum glare'),(448,'Desk-084 glare'),(529,'Desk-021 critical illuminance'),(592,'Desk-084 critical uniformity')]:
   index=next(p['output_page']-1 for p in core_manifest['pages'] if p['source_page']==native);outline.root[3].children.append(pikepdf.OutlineItem(title,offsets[3]+index))
  for native,title in [(61,'Complete auxiliary calculation tables'),(350,'Critical surrounding region'),(378,'Background floor'),(379,'Exposed ceiling'),(380,'Exposed walls')]:
   index=next(p['output_page']-1 for p in aux_manifest['pages'] if p['source_page']==native);outline.root[4].children.append(pikepdf.OutlineItem(title,offsets[4]+index))
 combined.docinfo['/Title']='BSE3125 - Open-plan office lighting design';combined.docinfo['/Subject']='Lighting report, independent CAD layout and actual DIALux simulation appendix'
 combined.remove_unreferenced_resources();combined.save(out,compress_streams=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)
assert out.stat().st_size<=10000000
final=pdfium.PdfDocument(out);checks=[]
for record in records:
 source=pdfium.PdfDocument(record['path'])
 for i in range(len(source)):
  a,b=source[i],final[record['first_combined_page']-1+i]
  assert a.get_size()==b.get_size() and a.get_textpage().get_text_range()==b.get_textpage().get_text_range()
  for dpi in [72,150]:
   x,y=a.render(scale=dpi/72).to_pil(),b.render(scale=dpi/72).to_pil();assert x.size==y.size and hashlib.sha256(x.tobytes()).digest()==hashlib.sha256(y.tobytes()).digest()
  checks.append({'combined_page':record['first_combined_page']+i,'source_page':i+1,'unchanged_text_size_and_72_150dpi_pixels':True})
assert len(checks)==192
manifest={'status':'assembled review PDF; final engineering/content/visual acceptance required','output':str(out.resolve()),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'main_report_pages_including_CAD':9,'total_pages':192,'sections':records,'page_preservation':checks}
out.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in manifest.items() if k not in ['sections','page_preservation']},indent=2))
