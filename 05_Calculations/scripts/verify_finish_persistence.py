"""Compare the bounded native finish experiment before and after reopening."""
from pathlib import Path
import json,hashlib,pdfplumber
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
a=json.loads((data/'white-rebuild-audit-v1.json').read_text())
b=json.loads((data/'white-rebuild-reopened-audit-v1.json').read_text())
assert a['surfaces']==b['surfaces']
assert a['scoped_report_pages']==b['scoped_report_pages']
native=root/'05_Calculations/models/office-white-finish-native-v3.evo'
assert hashlib.sha256(native.read_bytes()).hexdigest()==a['native_sha256']
pdf=root/'05_Calculations/models/office-white-finish-reopened-v3.pdf'
with pdfplumber.open(pdf) as d:text=d.pages[17].extract_text()
assert 'Ceiling: 80.0 %' in text and 'Walls: 70.0 %' in text and 'Floor: 20.0 %' in text
out=data/'white-finish-persistence-v1.json'
assert not out.exists()
out.write_text(json.dumps({'status':'native finish change and two-surface persistence verified; design still fails glare target','native_sha256':a['native_sha256'],'geometry_preserved':True,'scoped_result_text_preserved':True,'native_bytes_preserved_after_reopen_export':True,'reflection_summary_page':18,'reflection_summary_text':text,'report_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'desk_results':[{'name':'Desk-01','average_lx':507,'minimum_lx':415,'maximum_lx':597,'u0':0.82,'max_directional_ugr':19.7},{'name':'Desk-02-probe','average_lx':541,'minimum_lx':433,'maximum_lx':621,'u0':0.80,'max_directional_ugr':19.6}],'result_pages':[30,31,33],'scope':'Two provisional task surfaces only; fixture alignment, furniture layout and final occupied-area validation remain pending'},indent=2),encoding='utf-8')
print(out)
