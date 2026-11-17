"""Combine first editorial draft with unchanged CAD and five original native pages."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'06_Tools/.runtime'))
import pikepdf,pypdfium2 as pdfium
r=root/'05_Calculations/Report_Draft_v01';target=r/'BSE3125_Report_First_Draft.pdf'
components=[('Draft report',r/'main-draft.pdf',None),('L01 - independent lighting layout',root/'05_Calculations/Final_v03/cad-plot-v5/BSE3125-L01-lighting-plan.pdf',None),('Selected DIALux evidence',root/'05_Calculations/models/office-review-40s-probe-reopened-v4.pdf',[254,316,529,592]),('Background floor',root/'05_Calculations/models/office-review-brightness-probe-reopened-v4.pdf',[378])]
with pikepdf.Pdf.new() as out:
 starts=[]
 for title,path,pages in components:
  starts.append(len(out.pages))
  with pikepdf.open(path) as p:
   for n in (pages if pages else range(1,len(p.pages)+1)):out.pages.append(p.pages[n-1])
 with out.open_outline() as outline:
  for (title,_,_),n in zip(components,starts):outline.root.append(pikepdf.OutlineItem(title,n))
  for n,title in enumerate(['Basis','DIALux procedure','Luminaire selection','Results comparison','Controls and power','Discussion and references']):outline.root[0].children.append(pikepdf.OutlineItem(title,n))
  for n,title in enumerate(['Room summary','Desk-018 maximum glare','Desk-021 minimum average','Desk-084 minimum uniformity']):outline.root[2].children.append(pikepdf.OutlineItem(title,7+n))
 out.docinfo['/Title']='BSE3125 - First student report draft';out.remove_unreferenced_resources();out.save(target,compress_streams=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)
p=pdfium.PdfDocument(target);assert len(p)==12 and target.stat().st_size<10000000
checks=[];idx=0
for title,path,pages in components:
 s=pdfium.PdfDocument(path)
 for n in (pages if pages else range(1,len(s)+1)):
  a,b=s[n-1],p[idx];assert a.get_size()==b.get_size() and a.get_textpage().get_text_range()==b.get_textpage().get_text_range()
  for scale in [1,150/72]:assert a.render(scale=scale).to_pil().tobytes()==b.render(scale=scale).to_pil().tobytes()
  checks.append({'combined_page':idx+1,'source':str(path),'source_page':n});idx+=1
for n in range(6):p[n].render(scale=1.3).to_pil().save(r/f'page-{n+1}.png')
(r/'draft-manifest.json').write_text(json.dumps({'status':'first editorial draft for user evaluation; current final submission remains unchanged','pages':12,'main_including_CAD':7,'selected_native_appendix_pages':5,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'all_pages_preserve_component_text_size_72_150dpi_pixels':True,'component_page_preservation':checks},indent=2))
print('First draft:',len(p),'pages;',target.stat().st_size,'bytes')
