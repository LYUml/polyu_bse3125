"""Extract exact room-scoped auxiliary native calculation table rows."""
from pathlib import Path
import sys,re,json,hashlib
import pdfplumber
pdf,out=map(Path,sys.argv[1:3]);assert not out.exists()
name=r'(?:Desk-\d{3}|Surround-B\d{2}|Background-floor|Exposed-Ceiling|Exposed-Wall-\d{2})'
row=re.compile(rf'^({name})\s+([\d.]+) lx\s+([\d.]+) lx\s+([\d.]+) lx\s+([\d.]+)\s+([\d.]+)\s+(CG\d+)$')
results=[];keys=set();pages=set()
with pdfplumber.open(pdf) as document:
 total=len(document.pages)
 for i,page in enumerate(document.pages):
  text=page.extract_text() or ''
  if '· Open plan office (Light scene 1)' not in text or '\nCalculation objects\n' not in text:continue
  lines=text.splitlines()
  for j,line in enumerate(lines):
   m=row.fullmatch(line)
   if not m:continue
   kind=lines[j+1].strip();assert kind in ['Perpendicular illuminance','Cylindrical illuminance']
   key=(m[1],kind);assert key not in keys,key;keys.add(key);pages.add(i+1)
   height_line=next((s for s in lines[j+2:j+5] if s.startswith('Height: ')),None);assert height_line
   height=float(re.search(r'([\d.]+) m',height_line)[1])
   results.append({'name':m[1],'parameter':kind,'average_lx':float(m[2]),'minimum_lx':float(m[3]),'maximum_lx':float(m[4]),'u0':float(m[5]),'g2':float(m[6]),'native_index':m[7],'height_m':height,'page':i+1})
def subset(prefix,kind):return [r for r in results if r['name'].startswith(prefix) and r['parameter']==kind]
desk_cyl=subset('Desk-','Cylindrical illuminance');ring_cyl=subset('Surround-','Cylindrical illuminance');rings=subset('Surround-','Perpendicular illuminance');background=subset('Background-','Perpendicular illuminance');walls=subset('Exposed-Wall-','Perpendicular illuminance');ceiling=subset('Exposed-Ceiling','Perpendicular illuminance')
assert len(desk_cyl)==112 and len(ring_cyl)==len(rings)==28 and len(background)==1
assert len(walls) in [0,6] and len(ceiling) in [0,1]
criteria={'Desk-':(150,.1),'Surround-':(150,.1)}
checks=[]
for group,label,avg,u0 in [(desk_cyl,'desk cylindrical',150,.1),(ring_cyl,'surrounding cylindrical',150,.1),(rings,'immediate surrounding',300,.4),(background,'background floor',100,.1),(walls,'exposed walls',150,.1),(ceiling,'exposed ceiling',100,.1)]:
 if not group:continue
 bound=min(r['minimum_lx'] for r in group)/max(r['average_lx'] for r in group)
 checks.append({'group':label,'surface_count':len(group),'average_target_lx':avg,'u0_target':u0,'minimum_surface_average_lx':min(r['average_lx'] for r in group),'minimum_surface_u0':min(r['u0'] for r in group),'conservative_combined_u0_lower_bound':bound,'pass':all(r['average_lx']>=avg and r['u0']>=u0 for r in group) and bound>=u0,'failing_surfaces':[r for r in group if r['average_lx']<avg or r['u0']<u0]})
record={'status':'actual room-scoped auxiliary native PDF results; geometry/persistence separate','pdf':str(pdf.resolve()),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':total,'checks':checks,'all_present_groups_pass':all(c['pass'] for c in checks),'all_six_groups_present':len(checks)==6,'table_pages':sorted(pages),'surfaces':results}
out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k not in ['surfaces','table_pages']},indent=2))
