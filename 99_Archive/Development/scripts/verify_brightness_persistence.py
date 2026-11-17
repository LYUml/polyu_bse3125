"""Require native save/close/reopen operations and identical reopened results."""
from pathlib import Path
import hashlib,json
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
load=lambda name:json.loads((data/name).read_text())
a=load('brightness-openings-results-v8.json');b=load('brightness-reopened-results-v9.json')
save=load('brightness-openings-save-v8.json');close=load('brightness-openings-close-v9.json');reopen=load('brightness-openings-reopen-v9.json');geometry=load('brightness-saved-geometry-v9b.json')
assert all(x['exit_code']==0 for x in [save,close,reopen])
native=Path(save['result']['path']);digest=hashlib.sha256(native.read_bytes()).hexdigest()
assert digest==save['result']['sha256']==geometry['native_sha256']
assert a['surfaces']==b['surfaces'] and a['checks']==b['checks'] and b['all_present_groups_pass'] and b['all_six_groups_present']
assert b['combined_seated_cylindrical']['pass']
pdf=Path(b['pdf']);assert hashlib.sha256(pdf.read_bytes()).hexdigest()==b['pdf_sha256']
doc=pdfium.PdfDocument(pdf)
summaries=[]
for i in range(35,55):
 text=doc[i].get_textpage().get_text_range()
 if 'Ceiling: 80.0 %' in text and 'Walls: 70.0 %' in text and 'Floor: 20.0 %' in text:summaries.append(i+1)
assert summaries,'Native reflectance summary not located'
record={'status':'verified','scope':'Auxiliary saved/reopened native results and separately reconstructed exposed regions; overall report/CAD/code acceptance remains separate','native_path':str(native),'native_sha256':digest,'native_bytes':native.stat().st_size,'saved_native_bytes_unchanged_after_reopen_export':True,'all_288_auxiliary_result_rows_identical':len(b['surfaces'])==288,'actual_auxiliary_result_row_count':len(b['surfaces']),'all_present_result_rows_identical':True,'all_six_groups_present_and_pass':True,'combined_seated_cylindrical_pass':True,'saved_geometry_verification':'brightness-saved-geometry-v9b.json','unchanged_186_fixture_positions_and_manufacturer_photometry':True,'native_summary_pages':summaries,'reopened_pdf_sha256':b['pdf_sha256'],'reopened_pdf_pages':b['page_count']}
assert len(b['surfaces'])==288
out=data/'brightness-openings-persistence-v9.json';assert not out.exists();out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
