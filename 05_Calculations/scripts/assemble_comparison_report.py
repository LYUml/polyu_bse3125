"""Assemble the final concise report and modular original simulation evidence."""
from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'06_Tools/.runtime'))
import pikepdf,pypdfium2 as pdfium
f=r/'05_Calculations/Final_v04';models=r/'05_Calculations/models'
main,target=[Path(x).resolve() for x in sys.argv[1:3]];assert not target.exists()
components=[('Main report',main,None),('L01 lighting layout',f/'cad-plot-v7/BSE3125-L01-lighting-plan.pdf',[1]),('Appendix A - baseline workstation results',models/'office-review-40s-probe-reopened-v4.pdf',[254,316,529,592]),('Appendix B - baseline background',models/'office-review-brightness-probe-reopened-v4.pdf',[378]),('Appendix C - comparison calculations',f/'comparison-appendix-v3.pdf',[1]),('C: 90% output - Desk-021',models/'office-comparison-output90-core-reopened-v1.pdf',[529]),('C: lower reflectance - room settings and glare',models/'office-comparison-reflectance-core-reopened-v1.pdf',[254,316]),('C: 90% output - ceiling',models/'office-comparison-output90-aux-reopened-v2.pdf',[379]),('C: lower reflectance - ceiling',models/'office-comparison-reflectance-aux-reopened-v1.pdf',[379])]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
with pikepdf.Pdf.new() as out:
    starts=[]
    for title,path,pages in components:
        starts.append(len(out.pages))
        with pikepdf.open(path) as src:
            for n in (pages if pages else range(1,len(src.pages)+1)):out.pages.append(src.pages[n-1])
    with out.open_outline() as outline:
        for (title,_,_),n in zip(components,starts):outline.root.append(pikepdf.OutlineItem(title,n))
        for n,title in enumerate(['1 Introduction and design basis','2 DIALux modelling','3 Luminaire selection','4 Simulation results','5 Lighting requirements','6 Controls and energy','7 Design comparison and conclusion','References']):outline.root[0].children.append(pikepdf.OutlineItem(title,n))
    out.docinfo['/Title']='BSE3125 - Group 4 Lighting Design Report'
    out.remove_unreferenced_resources();out.save(target,compress_streams=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)
p=pdfium.PdfDocument(target);assert len(p)==20 and target.stat().st_size<10000000
checks=[];idx=0
for title,path,pages in components:
    src=pdfium.PdfDocument(path)
    for n in (pages if pages else range(1,len(src)+1)):
        a,b=src[n-1],p[idx]
        assert a.get_size()==b.get_size() and a.get_textpage().get_text_range()==b.get_textpage().get_text_range()
        for scale in [1,150/72]:assert a.render(scale=scale).to_pil().tobytes()==b.render(scale=scale).to_pil().tobytes()
        checks.append({'combined_page':idx+1,'source':str(path.relative_to(r)),'source_page':n,'source_sha256':sha(path)});idx+=1
    src.close()
for i in range(len(p)):p[i].render(scale=1.5).to_pil().save(f/f'final-page-{i+1}.png')
p.close()
record={'status':'Assembled and component-preservation verified; final acceptance separate','pdf':str(target.relative_to(r)),'sha256':sha(target),'bytes':target.stat().st_size,'main_including_CAD':9,'total_pages':20,'appendix_pages':11,'all_pages_preserve_source_text_dimensions_and_72_150dpi_pixels':True,'component_pages':checks}
(f/'assembly-manifest.json').write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k!='component_pages'},indent=2))
