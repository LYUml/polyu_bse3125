"""Check saved comparison inputs against the accepted baseline, independently of results."""
from pathlib import Path
import sys,json,re,zipfile,hashlib
from read_native_archive import read
source,target=map(Path,sys.argv[1:3]);variant=sys.argv[3];out=Path(sys.argv[4]);assert not out.exists()
a,b=read(source),read(target);ao,bo=a['objects'],b['objects']
def refs(s): return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',s))]
def graph(o,n):
    seen=set();todo=[n]
    while todo:
        k=todo.pop()
        if k in seen:continue
        seen.add(k);todo.extend(refs(' '.join(o[k]['fields'].values())))
    return {k:o[k] for k in seen}
assert ao.keys()==bo.keys(), 'Native record mapping changed; inspect before acceptance'
physical_types=['LuminaireElement','LuminaireMaintenancePropertySet','GlobalLuminaireMaintenanceInfo','RelDefinesByPrototype','CalculationGridSurface','CalculationSurfaceOpening','MultiPolygonSurface2D','CoordSys3D','ExtrudedPolygonRepresentationDataPart','En12464CalculationGridSurfaceRepresentationData','CalculationSurfaceRepresentationDataPart','UgrCalculationParameterRepresentationDataPart']
counts={}
for typ in physical_types:
    selected={n:v for n,v in ao.items() if v['type']==typ}
    assert all(bo[n]==v for n,v in selected.items()),typ
    counts[typ]=len(selected)
assert counts['LuminaireElement']==186
for n,o in ao.items():
    if 'CoordSys' in o['type'] or 'Coordinate' in o['type']:
        assert bo[n]==o,o['type']
prototype=next(n for n,o in ao.items() if o['type']=='LuminairePrototype' and o['fields']['ObjectGuid']=="'76180ce0-f1c1-4543-860d-c8d94c1cf11b'")
assert graph(ao,prototype)==graph(bo,prototype)
dim=[o for o in bo.values() if o['type']=='LuminaireGroupRepresentationData'];assert len(dim)==1
dimval=float(re.search(r', ([\d.]+)\)',dim[0]['fields']['DimValues'])[1]);assert abs(dimval-(.9 if variant=='output90' else 1))<1e-7
if variant=='output90':
    dim_key=bo[int(re.search(r'#(\d+)',dim[0]['fields']['DimValues'])[1])]
    assert dim_key['fields']['LuminairePrototypeId']==bo[prototype]['fields']['ObjectId'], 'Dim setting does not target the installed product'
materials=[]
for n,o in ao.items():
    if o['type']!='MaterialParams':continue
    old=float(o['fields']['ColorLuminance']);new=float(bo[n]['fields']['ColorLuminance'])
    expected=(.7 if abs(old-.8)<1e-6 else .5) if variant=='reflectance' and 'Design white finish reflectance' in o['fields']['InternalName'] else old
    assert abs(new-expected)<1e-6
    materials.append({'name':bo[n]['fields']['InternalName'],'reflectance':new})
with zipfile.ZipFile(target) as z:
    streams=[i for i in z.infolist() if i.filename.startswith('Project/Results/') and i.file_size>0]
assert streams,'No saved native results'
record={'status':'Saved native input/result-stream checks passed; PDF reopen row comparison separate','source':str(source.resolve()),'source_sha256':a['sha256'],'saved_native':str(target.resolve()),'saved_native_sha256':b['sha256'],'variant':variant,'scene_output_fraction':dimval,'unchanged_physical_record_counts':counts,'all_coordinate_system_records_unchanged':True,'manufacturer_prototype_graph_records':len(graph(ao,prototype)),'manufacturer_graph_unchanged':True,'materials':materials,'saved_result_stream_count':len(streams)}
out.write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k!='materials'},indent=2))
