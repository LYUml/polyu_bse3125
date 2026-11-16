"""Native academic CAD plotting with toolkit outline/fixture verification.

Separate from the toolkit's synthetic-only plot wrapper; retains source copies,
explicit fixed scale, exact fixture coverage and independent PDF checks.
"""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess
import pdfplumber,pypdfium2 as pdfium
root=Path(__file__).resolve().parents[1];toolkit=root.parent/'dialux-agent-toolkit'
sys.path.insert(0,str(toolkit))
from src.cad import verify_pdf_outline_scale
from src.cad_plot import plotted_fixture_ids
source,directory=map(lambda x:Path(x).resolve(),sys.argv[1:3])
assert source.suffix=='.dwg' and not directory.exists()
digest=hashlib.sha256(source.read_bytes()).hexdigest();directory.mkdir()
copied=directory/'plot-input.dwg';shutil.copy2(source,copied)
pdf=directory/'BSE3125-L01-lighting-plan.pdf';script=directory/'plot.scr'
args=['_.-PLOT','_Y','Model','DWG To PDF.pc3','ISO A2 (594.00 x 420.00 MM)','_M','_L','_N','_E','1000=100','_C','_Y','monochrome.ctb','_Y','_A',str(pdf).replace('\\','/'),'_N','_Y']
script.write_text('(setvar "FILEDIA" 0)\n(setvar "CMDDIA" 0)\n(setvar "BACKGROUNDPLOT" 0)\n(if (/= (getvar "INSUNITS") 6) (error "Expected metre CAD drawing"))\n(command '+ ' '.join(json.dumps(x) for x in args)+')\n(princ "ASSIGNMENT_PLOT_COMPLETE")\n(princ)\n',encoding='ascii')
core=Path('C:/Program Files/Autodesk/AutoCAD 2027/accoreconsole.exe')
try:
 result=subprocess.run([str(core),'/i',str(copied),'/s',str(script),'/product','ACAD','/l','en-US'],capture_output=True,timeout=90,cwd=directory)
except subprocess.TimeoutExpired as exc:
 (directory/'console.log').write_text((exc.stdout or b'').decode('utf-16le',errors='replace'),encoding='utf-8');raise
log=result.stdout.decode('utf-16le',errors='replace');(directory/'console.log').write_text(log,encoding='utf-8')
assert result.returncode==0 and 'ASSIGNMENT_PLOT_COMPLETE' in log and '; error:' not in log.lower() and pdf.exists()
plan_path=Path(sys.argv[3]) if len(sys.argv)>3 else root/'05_Calculations/data/snapped-layout-proposal-v2.json'
plan=json.loads(plan_path.read_text());room=json.loads((root/'05_Calculations/data/room-v1.json').read_text())
with pdfplumber.open(pdf) as doc:
 assert len(doc.pages)==1;page=doc.pages[0]
 assert abs(page.width-594*72/25.4)<2 and abs(page.height-420*72/25.4)<2
 scale=verify_pdf_outline_scale(page.curves+page.rects,room['contour'],100)
 ids,scope=plotted_fixture_ids(page,[f['id'] for f in plan['fixtures']],scale)
 text=page.extract_text() or ''
 products={f['product_order_code'] for f in plan['fixtures']};assert len(products)==1
 for required in [next(iter(products)),'186',str(186*plan['rated_input_W_each']),str(186*plan['rated_input_W_each']+50),'1:100','BSE3125-L01']:assert required in text,required
doc=pdfium.PdfDocument(pdf);doc[0].render(scale=150/72).to_pil().save(directory/'preview-150dpi.png');doc.close()
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
record={'status':'native A2 1:100 PDF plotted; visual review pending','source_dwg':str(source),'source_dwg_sha256':digest,'pdf':str(pdf),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'bytes':pdf.stat().st_size,'paper':'A2','scale_denominator':100,'fixture_count':len(ids),'all_fixture_labels_verified':True,'fixture_label_scope':scope,'physical_scale':scale,'original_dwg_unchanged':True,'visual_review_verified':False}
(directory/'manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
