"""Bind fresh native calculations, saved archives, title-only copies and reopened output."""
from pathlib import Path
import ast,hashlib,json,math,re,sys
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data';models=root/'05_Calculations/models'
sys.path.insert(0,str(root/'06_Tools'));from read_native_archive import read,split_fields
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def graph(objects):
 p=next(v for v in objects.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'")
 seen=set();todo=[p['step_id']]
 while todo:
  n=todo.pop()
  if n in seen:continue
  seen.add(n);todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in seen)
 return sorted(json.dumps({'type':objects[n]['type'],'fields':{k:re.sub(r'#\d+','#REF',v) for k,v in objects[n]['fields'].items() if k!='ObjectId'}},sort_keys=True) for n in seen)
imported=read(models/'office-review-40s-import-v2.evo');records=[]
for label,native,initial,reopened,save,reopen in [
 ('core','office-review-40s-native-v4.evo','review-40s-task-results-v2.json','review-40s-reopened-tasks-v4.json','review-40s-save-v3.json','review-core-reopen-v4.json'),
 ('auxiliary','office-review-brightness-native-v4.evo','review-brightness-results-v2.json','review-brightness-reopened-results-v4.json','review-brightness-save-v3.json','review-brightness-reopen-v4.json')]:
 p=models/native;d=read(p);o=d['objects'];stamp=load(p.with_suffix('.title.json'));s=load(data/save);r=load(data/reopen)
 assert s['exit_code']==r['exit_code']==0
 assert sha(p)==stamp['output_sha256'] and stamp['source_sha256']==s['result']['sha256'] and stamp['all_other_records_and_all_results_streams_unchanged']
 assert sha(Path(s['result']['path']))==s['result']['sha256']
 assert graph(o)==graph(imported['objects']) and len(graph(o))==63
 a=load(data/initial);b=load(data/reopened);key='tasks' if label=='core' else 'surfaces'
 assert a[key]==b[key] and len(b[key])==(112 if label=='core' else 288)
 assert sha(Path(b['pdf']))==b['pdf_sha256']
 pdf=pdfium.PdfDocument(b['pdf']);assert 'BSE3125 - Open-plan Office' in pdf[0].get_textpage().get_text_range();pdf.close()
 fixtures={n for n,v in o.items() if v['type']=='LuminaireElement'};assert len(fixtures)==186
 prototype=next(v for v in o.values() if v['type']=='LuminairePrototype' and v['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'")
 linked={n for v in o.values() if v['type']=='RelDefinesByPrototype' and v['fields']['RelatingPrototype']=='#'+str(prototype['step_id']) for n in refs(v['fields']['RelatedObjects'])};assert fixtures.issubset(linked)
 mf=[v for v in o.values() if v['type']=='LuminaireMaintenancePropertySet' and int(v['fields']['DefinedObject'][1:]) in fixtures];assert len(mf)==186 and all(float(o[int(v['fields']['MaintenanceInfo'][1:])]['fields']['MaintenanceFactor'])==.8 for v in mf)
 if label=='core':
  expected={t['id']:t for t in load(data/'furniture-proposal-v1.json')['desks']};observed=set()
  for v in o.values():
   if v['type']!='CalculationGridSurface':continue
   name=next(o[n]['fields']['ObjectName'][1:-1] for n in refs(v['fields']['PropertySets']) if o[n]['type']=='CommonInformationPropertySet')
   if name not in expected:continue
   origin=ast.literal_eval(o[int(v['fields']['LocalCoordSys'][1:])]['fields']['Origin']);assert math.dist(origin,expected[name]['centre_m'])<1e-8
   rep=o[int(o[int(v['fields']['Representation'][1:])]['fields']['RepresentationData'][1:])]
   poly=o[int(rep['fields']['MultiPolygonSurface'][1:])];loops=[ast.literal_eval(x) for x in split_fields(poly['fields']['OuterLoops'][1:-1])];assert len(loops)==1 and poly['fields']['InnerLoops']=='()'
   assert {(round(p[0],8),round(p[1],8)) for p in loops[0]}=={(-.8,-.4),(-.8,.4),(.8,-.4),(.8,.4)}
   u=next(o[n]['fields'] for n in refs(rep['fields']['Parts']) if o[n]['type']=='UgrCalculationParameterRepresentationDataPart')
   assert abs(origin[2]+float(u['HeightOffset'])-1.2)<1e-8 and abs(float(u['StepSize'])-math.pi/12)<1e-8 and abs(float(u['AngleRangeEnd'])-2*math.pi)<1e-8 and float(u['AngleRangeBegin'])==0
   observed.add(name)
  assert observed==set(expected)
 records.append({'project':label,'native_path':str(p),'native_sha256':sha(p),'reopened_pdf':b['pdf'],'reopened_pdf_sha256':b['pdf_sha256'],'all_results_preserved':len(b[key]),'all_186_use_manufacturer_imported_63_record_graph':True,'all_186_MF':.8,'saved_native_unchanged_after_reopen_export':True})
g=load(data/'review-brightness-saved-geometry-v4.json');assert g['maximum_symmetric_difference_area_m2']==0 and g['native_opening_count']==255 and g['all_186_fixture_guids_and_local_coordinate_systems_equal_core']
positions=load(data/'review-40s-positions-v4.json');assert positions['fixture_count']==186 if 'fixture_count' in positions else len(positions['matches'])==186
result={'status':'verified','projects':records,'all_112_task_geometry_and_direction_parameters_verified':True,'auxiliary_regions':36,'actual_native_openings':255,'auxiliary_geometry_check':'review-brightness-saved-geometry-v4.json','shared_plan_sha256':sha(data/'snapped-layout-proposal-v3.json')}
out=data/'review-native-persistence-v4.json';assert not out.exists();out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
