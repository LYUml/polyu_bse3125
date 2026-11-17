"""Reuse toolkit table reader, verify all fixture positions against shared CAD plan."""
from pathlib import Path
import sys,json,re,math,hashlib
import pdfplumber
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root.parent/'dialux-agent-toolkit'))
from src.report_layout import parse_coordinate_page
pdf,plan,out=map(Path,sys.argv[1:4]);assert not out.exists()
p=json.loads(plan.read_text());rows=[];header='Building Open plan office · Storey Open plan office · Open plan office'
products={f['product_order_code'] for f in p['fixtures']};assert len(products)==1
product=next(iter(products));power=p['native_photometry_input_W_each'];flux=p.get('nominal_luminaire_flux_lm',3400)
with pdfplumber.open(pdf) as d:
 for n in range(257,266):
  page=d.pages[n-1];text=page.extract_text() or ''
  assert text.splitlines()[1]==header and '\nLuminaire layout plan\n' in text
  if n==257:
   observed_power=re.search(r'^Manufacturer Philips P ([\d.]+) W$',text,re.M)
   observed_product=re.search(r'^Article No\. (\d+) ΦLuminaire ([\d.]+) lm$',text,re.M)
   assert observed_power and abs(float(observed_power[1])-power)<1e-8
   assert observed_product and observed_product[1]==product and abs(float(observed_product[2])-flux)<1e-8
  rows.extend(parse_coordinate_page(page,n))
assert [x['report_luminaire_number'] for x in rows]==list(range(1,187))
remaining={f['id']:f for f in p['fixtures']};matches=[]
for row in rows:
 pos=[row['position_m'][0]+.18,row['position_m'][1]+.18,row['position_m'][2]]
 found=[f for f in remaining.values() if math.dist(pos,f['position_m'])<=.001]
 assert len(found)==1,f'Unmatched or ambiguous reported fixture {row}'
 f=found[0];del remaining[f['id']]
 matches.append({'id':f['id'],'native_object_guid':f['native_object_guid'],'source_tile_handle':f['source_tile_handle'],'planned_position_m':f['position_m'],'reported_room_position_m':row['position_m'],'transformed_report_position_m':pos,'coordinate_error_m':math.dist(pos,f['position_m']),'report_number':row['report_luminaire_number'],'report_page':row['page']})
assert not remaining
record={'status':'all 186 native report positions match source-linked ceiling tiles','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'fixture_count':len(matches),'product_order_code':product,'reported_power_W_each':power,'reported_flux_lm_each':flux,'translation_report_to_design_m':[.18,.18,0],'translation_evidence':'Measured room starts at design/storey (0.18,0.18); native room-scoped report coordinates subtract this room origin. Native reference mounting height is unchanged.','maximum_coordinate_error_m':max(m['coordinate_error_m'] for m in matches),'matches':matches,'scope':'Actual exported coordinates matched one-to-one; save/reopen persistence and photometry asset checks remain separate.'}
out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='matches'},indent=2))
