"""Read all proposed task results from exact room-scoped native PDF tables."""
from pathlib import Path
import sys,re,json,hashlib
import pdfplumber
pdf,out=map(Path,sys.argv[1:3]);assert not out.exists()
illuminance={};glare={};scoped_pages=[]
pattern=re.compile(r'(Desk-\d{3})\s+([\d.]+) lx\s+([\d.]+) lx\s+([\d.]+) lx\s+([\d.]+)\s+([\d.]+)\s+CG\d+')
with pdfplumber.open(pdf) as document:
 count=len(document.pages)
 for i,page in enumerate(document.pages):
  text=page.extract_text() or ''
  if '· Open plan office (Light scene 1)' not in text or 'Calculation objects' not in text:continue
  rows=pattern.findall(text)
  for name,avg,lo,hi,u0,g2 in rows:
   assert name not in illuminance,f'Duplicate scoped row {name}'
   illuminance[name]={'average_lx':float(avg),'minimum_lx':float(lo),'maximum_lx':float(hi),'u0':float(u0),'g2':float(g2),'illuminance_page':i+1}
  names=re.findall(r'(Desk-\d{3}) \(RUG\)',text)
  if names and re.search(r'\bmax\s+[\d.]+',text):
   assert len(names)==1
   name=names[0];assert name not in glare
   value=re.search(r'\bmax\s+([\d.]+)',text);direction=re.search(r'Strongest glare at\s+([\d.]+)°',text)
   assert value and direction and 'Height 1.200 m' in text and 'Step width 15°' in text
   glare[name]={'max_directional_ugr':float(value[1]),'worst_direction_deg':float(direction[1]),'ugr_page':i+1}
  if rows or names:scoped_pages.append(i+1)
expected={f'Desk-{n:03}' for n in range(1,113)}
assert set(illuminance)==set(glare)==expected,(len(illuminance),len(glare))
results=[{'name':n,**illuminance[n],**glare[n]} for n in sorted(expected)]
for r in results:r['course_metric_pass']=r['average_lx']>=500 and r['u0']>=.6 and r['max_directional_ugr']<=19
record={'status':'actual native PDF task metrics; native geometry/persistence and whole-report acceptance separate','pdf':str(pdf.resolve()),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pdf_page_count':count,'task_count':len(results),'all_tasks_pass_course_metrics':all(r['course_metric_pass'] for r in results),'minimum_task_average_lx':min(r['average_lx'] for r in results),'minimum_task_u0':min(r['u0'] for r in results),'maximum_directional_ugr':max(r['max_directional_ugr'] for r in results),'failing_tasks':[r for r in results if not r['course_metric_pass']],'source_pages':scoped_pages,'tasks':results}
out.write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ['tasks','source_pages']},indent=2))
