"""Inspect native surface geometry/UGR settings and scoped PDF result evidence."""
from pathlib import Path
import sys,json,re,hashlib
import pdfplumber
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'06_Tools'))
from read_native_archive import read,split_fields
assert split_fields("1, 'a,b', (2,3), .Normal, Daylight., 0.4")==['1',"'a,b'",'(2,3)','.Normal, Daylight.','0.4']
native=Path(sys.argv[1]);pdf=Path(sys.argv[2]);out=Path(sys.argv[3])
if out.exists():raise ValueError('Fresh evidence path required')
data=read(native);objects=data['objects']
def ref(v):return objects[int(v[1:])]
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
missing=[n for o in objects.values() for v in o['fields'].values() for n in refs(v) if n not in objects]
assert not missing,'Dangling native object reference'
ids={}
for o in objects.values():
 if 'ObjectGuid' in o['fields']:
  guid=o['fields']['ObjectGuid'];assert guid not in ids;ids[guid]=o['step_id']
surfaces=[]
for o in objects.values():
 if o['type']!='CalculationGridSurface':continue
 props=[objects[n] for n in refs(o['fields']['PropertySets'])]
 name=next(p['fields']['ObjectName'][1:-1] for p in props if p['type']=='CommonInformationPropertySet')
 coord=ref(o['fields']['LocalCoordSys']);origin=[float(x) for x in split_fields(coord['fields']['Origin'][1:-1])]
 rep=ref(ref(o['fields']['Representation'])['fields']['RepresentationData'])
 poly=ref(rep['fields']['MultiPolygonSurface'])
 ugr=[objects[n] for n in refs(rep['fields']['Parts']) if objects[n]['type']=='UgrCalculationParameterRepresentationDataPart']
 assert len(ugr)==1
 f=ugr[0]['fields'];height=origin[2]+float(f['HeightOffset'])
 assert abs(height-1.2)<1e-9
 surfaces.append({'name':name,'native_step_id':o['step_id'],'parent_frame_origin_m':origin,'outer_loops_raw':poly['fields']['OuterLoops'],'inner_loops_raw':poly['fields']['InnerLoops'],'ugr_eye_height_m':height,'ugr_step_radians':float(f['StepSize']),'ugr_range_radians':[float(f['AngleRangeBegin']),float(f['AngleRangeEnd'])]})
pages=[]
with pdfplumber.open(pdf) as document:
 for i,p in enumerate(document.pages):
  t=p.extract_text() or ''
  if i<10 or not any(s['name'] in t for s in surfaces):continue
  if '· Open plan office (Light scene 1)' not in t:continue
  if 'Calculation objects' not in t:continue
  pages.append({'page':i+1,'text':t})
assert pages,'No room-scoped task calculation pages found'
result={'status':'archive structure plus actual report evidence; native save/reopen check separate','native_path':str(native.resolve()),'native_sha256':data['sha256'],'schema_checked_object_count':len(objects),'unique_guid_count':len(ids),'dangling_references':missing,'surfaces':surfaces,'report_path':str(pdf.resolve()),'report_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'scoped_report_pages':pages}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'surface_count':len(surfaces),'native_records':len(objects),'report_pages':[p['page'] for p in pages]},indent=2))
