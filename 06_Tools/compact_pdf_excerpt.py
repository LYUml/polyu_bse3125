"""Copy selected native pages, prune unused resources, verify text and pixels.

Uses pikepdf's documented resource pruning, with independent PDFium checks.
Source PDFs remain unchanged; images/text are not resampled or recreated.
"""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).parent/'.runtime'))
import pikepdf
import pypdfium2 as pdfium
request,target=map(Path,sys.argv[1:3]);assert not target.exists()
r=json.loads(request.read_text());assert len(r['sections'])==1
s=r['sections'][0];source=Path(s['path']);raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()==s['sha256']
pages=s['pages'];assert len(pages)==len(set(pages)) and all(isinstance(n,int) and n>0 for n in pages)
pending=target.with_suffix('.pending.pdf');assert not pending.exists()
with pikepdf.open(source) as original:
 assert not original.is_encrypted and '/AcroForm' not in original.Root
 with pikepdf.Pdf.new() as compact:
  for n in pages:compact.pages.append(original.pages[n-1])
  compact.remove_unreferenced_resources()
  compact.save(pending,compress_streams=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)
a=pdfium.PdfDocument(source);b=pdfium.PdfDocument(pending);checks=[]
assert len(b)==len(pages)
for i,n in enumerate(pages):
 ap,bp=a[n-1],b[i];assert ap.get_size()==bp.get_size()
 at=ap.get_textpage().get_text_range();bt=bp.get_textpage().get_text_range();assert at==bt
 rendered={}
 for dpi in [72,150]:
  ai=ap.render(scale=dpi/72).to_pil();bi=bp.render(scale=dpi/72).to_pil()
  ah=hashlib.sha256(ai.tobytes()).hexdigest();bh=hashlib.sha256(bi.tobytes()).hexdigest()
  assert ai.size==bi.size and ah==bh,f'Changed page {n} at {dpi} dpi'
  rendered[str(dpi)]=ah
 checks.append({'output_page':i+1,'source_page':n,'size_pt':ap.get_size(),'text_sha256':hashlib.sha256(at.encode()).hexdigest(),'render_sha256_by_dpi':rendered})
 ap.close();bp.close()
a.close();b.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==s['sha256']
assert pending.stat().st_size<=r['max_bytes']
pending.rename(target)
record={'status':'selected native pages preserved at text, size, 72 and 150 dpi rendering','source':str(source.resolve()),'source_sha256':s['sha256'],'output':str(target.resolve()),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'pikepdf_version':pikepdf.__version__,'pages':checks,'scope':'Static selected-page content preservation only; no engineering acceptance or full-document interactive-feature claim'}
target.with_suffix('.manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='pages'},indent=2))
