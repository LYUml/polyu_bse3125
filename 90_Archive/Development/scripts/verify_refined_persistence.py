"""Verify saved/reopened refined native design, task geometry and photometry graph."""
from pathlib import Path
import sys,json,re,hashlib,math,ast
import pdfplumber
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
sys.path.insert(0,str(root/'06_Tools'));from read_native_archive import read,split_fields
native=root/'05_Calculations/models/office-powerbalance-grid-native-v4.evo'
d=read(native);o=d['objects'];save=json.loads((data/'grid-refined-save-v3.json').read_text())
assert d['sha256']==save['result']['sha256']
a=json.loads((data/'grid-tasks-results-v3.json').read_text());b=json.loads((data/'grid-reopened-tasks-v4.json').read_text())
assert a['tasks']==b['tasks'] and b['all_tasks_pass_course_metrics']
x=json.loads((data/'grid-report-position-verification-v3.json').read_text());y=json.loads((data/'grid-reopened-positions-v4.json').read_text());assert x['matches']==y['matches']
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def obj(v):return o[int(v[1:])]
proposal=json.loads((data/'furniture-proposal-v1.json').read_text());expected={t['id']:t for t in proposal['desks']};observed={}
for s in o.values():
 if s['type']!='CalculationGridSurface':continue
 props=[o[n] for n in refs(s['fields']['PropertySets'])];name=next(p['fields']['ObjectName'][1:-1] for p in props if p['type']=='CommonInformationPropertySet')
 if name not in expected:continue
 origin=ast.literal_eval(obj(s['fields']['LocalCoordSys'])['fields']['Origin']);assert math.dist(origin,expected[name]['centre_m'])<1e-8
 rep=obj(obj(s['fields']['Representation'])['fields']['RepresentationData']);poly=obj(rep['fields']['MultiPolygonSurface'])
 loops=[ast.literal_eval(v) for v in split_fields(poly['fields']['OuterLoops'][1:-1])];assert len(loops)==1 and len(loops[0])==4 and poly['fields']['InnerLoops']=='()'
 assert {(round(v[0],8),round(v[1],8)) for v in loops[0]}=={(-.8,-.4),(-.8,.4),(.8,-.4),(.8,.4)}
 ugr=[o[n] for n in refs(rep['fields']['Parts']) if o[n]['type']=='UgrCalculationParameterRepresentationDataPart'];assert len(ugr)==1
 f=ugr[0]['fields'];assert abs(origin[2]+float(f['HeightOffset'])-1.2)<1e-8
 assert abs(float(f['StepSize'])-math.pi/12)<1e-8 and abs(float(f['AngleRangeBegin']))<1e-8 and abs(float(f['AngleRangeEnd'])-2*math.pi)<1e-8
 observed[name]={'parent_origin_m':origin,'size_m':[1.6,.8],'ugr_eye_height_m':1.2,'ugr_step_degrees':15}
assert set(observed)==set(expected)
fixtures={n for n,v in o.items() if v['type']=='LuminaireElement'};assert len(fixtures)==186
prototype_guid="'74b47d1c-9d32-40c3-9537-d2ba85948fe1'"
prototype=next(v for v in o.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']==prototype_guid)
relations=[v for v in o.values() if v['type']=='RelDefinesByPrototype' and v['fields']['RelatingPrototype']=='#'+str(prototype['step_id'])];assert len(relations)==1
assert set(refs(relations[0]['fields']['RelatedObjects'])) & fixtures==fixtures
maintenance=[v for v in o.values() if v['type']=='LuminaireMaintenancePropertySet' and int(v['fields']['DefinedObject'][1:]) in fixtures];assert len(maintenance)==186
assert all(abs(float(obj(v['fields']['MaintenanceInfo'])['fields']['MaintenanceFactor'])-.8)<1e-8 for v in maintenance)
def canonical_graph(objects):
 proto=next(v for v in objects.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']==prototype_guid)
 seen=set();todo=[proto['step_id']]
 while todo:
  n=todo.pop()
  if n in seen:continue
  seen.add(n);todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in seen)
 normalized=sorted(json.dumps({'type':objects[n]['type'],'fields':{k:re.sub(r'#\d+','#REF',v) for k,v in objects[n]['fields'].items()}},sort_keys=True) for n in seen)
 return len(seen),hashlib.sha256('\n'.join(normalized).encode()).hexdigest()
original=read(root/'05_Calculations/models/office-powerbalance-development-v1.evo')
assert canonical_graph(original['objects'])==canonical_graph(o)
pdf=root/'05_Calculations/models/office-powerbalance-grid-probe-reopened-v4.pdf'
with pdfplumber.open(pdf) as doc:summary=doc.pages[253].extract_text()
for value in ['Ceiling: 80.0 %','Walls: 70.0 %','Floor: 20.0 %','2.800 m','2.868 m','0.80 (fixed)']:assert value in summary
out=data/'refined-native-persistence-v1.json';assert not out.exists()
record={'status':'refined native task/fixture design persistence verified; full assignment acceptance remains separate','native_path':str(native),'native_sha256':d['sha256'],'native_bytes_unchanged_after_reopen_export':True,'all_112_task_results_preserved':True,'all_186_report_positions_preserved':True,'all_112_task_geometry_and_ugr_parameters_verified':True,'all_186_fixture_maintenance_factors':.8,'all_186_fixtures_use_powerbalance_prototype':True,'prototype_graph_record_count':canonical_graph(o)[0],'prototype_graph_sha256':canonical_graph(o)[1],'photometry_graph_unchanged_from_native_imported_baseline':True,'manufacturer_uld_sha256':json.loads((data/'powerbalance-import-v1.json').read_text())['result']['sha256'],'reopened_report_sha256':b['pdf_sha256'],'native_summary_page':254,'native_summary_text':summary,'task_geometry':observed,'scope':'Verifies these native datasets and actual reported course task metrics. Does not itself verify all international clauses, installed controls, CAD visual quality or report packaging.'}
out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k not in ['task_geometry','native_summary_text']},indent=2))
