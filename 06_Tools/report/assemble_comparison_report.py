"""Assemble the final concise report and modular original simulation evidence."""
from pathlib import Path
from io import BytesIO
import sys,json,hashlib
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'06_Tools/.runtime'))
import pikepdf,pypdfium2 as pdfium
from reportlab.pdfgen.canvas import Canvas
f=r/'04_Report';models=r/'03_Engineering/Native_Reports'
main,target=[Path(x).resolve() for x in sys.argv[1:3]];assert not target.exists()
appendix=Path(sys.argv[3]).resolve() if len(sys.argv)>3 else f/'Build/comparison-appendix.pdf'
components=[('Main report',main,None),('L01 lighting layout',r/'03_Engineering/CAD/Lighting_Layout.pdf',[1]),('Appendix A - baseline workstation results',models/'Final_Workstations.pdf',[254,316,529,592]),('Appendix B - baseline background',models/'Final_Visual_Environment.pdf',[378]),('Appendix C - comparison calculations',appendix,[1]),('Case B - 90% output',models/'Output90_Workstations.pdf',[529]),('Case B - 90% output',models/'Output90_Visual_Environment.pdf',[379]),('Case C - lower reflectance',models/'Lower_Reflectance_Workstations.pdf',[254,316]),('Case C - lower reflectance',models/'Lower_Reflectance_Visual_Environment.pdf',[379])]
components.append(('Case D - 90% output and lower reflectance',models/'Combined_Workstations.pdf',[254,316,529]))
components.append(('Case D - 90% output and lower reflectance',models/'Combined_Visual_Environment.pdf',[379]))
def add_case_label(page,label):
    w,h=map(float,list(page.mediabox)[2:])
    buffer=BytesIO()
    canvas=Canvas(buffer,pagesize=(w,h))
    canvas.setFont('Helvetica-Bold',10)
    canvas.drawCentredString(w/2,h-13,label)
    canvas.save()
    buffer.seek(0)
    with pikepdf.open(buffer) as overlay:
        page.add_overlay(overlay.pages[0])

sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
with pikepdf.Pdf.new() as out:
    starts=[]
    for title,path,pages in components:
        starts.append(len(out.pages))
        with pikepdf.open(path) as src:
            for n in (pages if pages else range(1,len(src.pages)+1)):
                out.pages.append(src.pages[n-1])
                if title.startswith('Case '):
                    add_case_label(out.pages[-1],title)
    with out.open_outline() as outline:
        for (title,_,_),n in zip(components,starts):outline.root.append(pikepdf.OutlineItem(title,n))
        for n,title in enumerate(['1 Introduction and design basis','2 DIALux modelling','2.4 Native DIALux documentation','3 Luminaire selection','4 Simulation results','5 Lighting requirements','6 Controls and energy','7 Design comparison and conclusion','References']):outline.root[0].children.append(pikepdf.OutlineItem(title,n))
    out.docinfo['/Title']='BSE3125 - Group 4 Lighting Design Report'
    out.remove_unreferenced_resources();out.save(target,compress_streams=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)
p=pdfium.PdfDocument(target);assert starts[2]==10 and target.stat().st_size<=10000000
checks=[];idx=0
for title,path,pages in components:
    src=pdfium.PdfDocument(path)
    for n in (pages if pages else range(1,len(src)+1)):
        a,b=src[n-1],p[idx]
        assert a.get_size()==b.get_size()
        original=a.get_textpage().get_text_range()
        assembled=b.get_textpage().get_text_range()
        labelled=title.startswith('Case ')
        assert original.strip()==(assembled.replace(title,'',1) if labelled else assembled).strip()
        for scale in [1,150/72]:
            crop=(0,0,0,17) if labelled else (0,0,0,0)
            assert a.render(scale=scale,crop=crop).to_pil().tobytes()==b.render(scale=scale,crop=crop).to_pil().tobytes()
        checks.append({'combined_page':idx+1,'source':str(path.relative_to(r)),'source_page':n,'source_sha256':sha(path)});idx+=1
    src.close()
preview=target.parent/'Preview';preview.mkdir(exist_ok=True)
for i in range(len(p)):p[i].render(scale=1.5).to_pil().save(preview/f'page-{i+1}.png')
p.close()
record={'status':'Assembled and component-preservation verified','pdf':str(target.relative_to(r)),'sha256':sha(target),'bytes':target.stat().st_size,'main_including_CAD':starts[2],'total_pages':len(checks),'appendix_pages':len(checks)-starts[2],'all_pages_preserve_source_text_and_dimensions':True,'source_pixels_verified_at_72_150dpi_outside_case_label_margin':True,'component_pages':checks}
(target.parent/'assembly-manifest.json').write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k!='component_pages'},indent=2))
