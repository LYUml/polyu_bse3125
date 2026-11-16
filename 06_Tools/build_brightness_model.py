"""Auxiliary native surfaces for surrounding/background and room brightness.

Preserves luminaires/materials; native calculation and geometry checks required.
Reuses the observed native Desk-001 cylindrical parameter and cloned surface graph.
UGR is retained in the separate verified design; removed from this auxiliary copy.
"""
from pathlib import Path
import sys,json,re,copy,uuid,zipfile,hashlib,math
from shapely.geometry import box,Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely.affinity import scale
from read_native_archive import read,split_fields
source,target=map(Path,sys.argv[1:3]);assert not target.exists()
exposed_mode='--exposed' in sys.argv[3:]
root=Path(__file__).resolve().parents[1];data=root/'05_Calculations/data'
d=read(source);objects=copy.deepcopy(d['objects']);original=d['objects']
def refs(v):return [int(n) for n in re.findall(r'#(\d+)',re.sub(r"'(?:[^']|'')*'",'',v))]
def serialize(o):return f"#{o['step_id']} = {o['type']} ("+', '.join(o['fields'].values())+');'
def real(v):
 s=format(v,'.16g');return s if '.' in s or 'e' in s.lower() else s+'.'
def vector(v):return '('+', '.join(real(n) for n in v)+')'
def loop(v):return '('+', '.join(vector(p) for p in list(v)[:-1])+')'
def listref(ids):return '('+', '.join('#'+str(n) for n in ids)+')'
def surface_name(s):return next(objects[n]['fields']['ObjectName'][1:-1] for n in refs(s['fields']['PropertySets']) if objects[n]['type']=='CommonInformationPropertySet')
def rep_of(s):return objects[int(objects[int(s['fields']['Representation'][1:])]['fields']['RepresentationData'][1:])]
surfaces=[s for s in objects.values() if s['type']=='CalculationGridSurface']
template=next(s for s in surfaces if surface_name(s)=='Desk-001');template_rep=rep_of(template)
cyl_id=next(n for n in refs(template_rep['fields']['Parts']) if objects[n]['fields'].get('ResultType')=='.CylIllum.')
cyl=copy.deepcopy(objects[cyl_id]);assert abs(float(cyl['fields']['HeightOffset'])-.4)<1e-8
grid_id=next(n for n in refs(template_rep['fields']['Parts']) if objects[n]['fields'].get('PartId')==template_rep['fields']['GridParamsPartId'])
cyl_connection=copy.deepcopy(next(objects[n] for n in refs(template_rep['fields']['PartConnections']) if objects[n]['fields']['RelatedPart']=='#'+str(cyl_id)))
next_step=max(objects)+1;added_cyl=0;removed_ugr=0
for surface in surfaces:
 rep=rep_of(surface);parts=refs(rep['fields']['Parts']);connections=refs(rep['fields']['PartConnections'])
 ugr={n for n in parts if objects[n]['fields'].get('ResultType')=='.Ugr.'}
 removed_ugr+=len(ugr);parts=[n for n in parts if n not in ugr]
 connections=[n for n in connections if int(objects[n]['fields']['RelatedPart'][1:]) not in ugr]
 if surface_name(surface).startswith('Desk-') and not any(objects[n]['fields'].get('ResultType')=='.CylIllum.' for n in parts):
  grid=next(n for n in parts if objects[n]['fields'].get('PartId')==rep['fields']['GridParamsPartId'])
  part=copy.deepcopy(cyl);part['step_id']=next_step;next_step+=1
  part['fields']['ContainingRepresentationData']='#'+str(rep['step_id']);part['fields']['PartId']=rep['fields']['NextPartId']
  connection=copy.deepcopy(cyl_connection);connection['step_id']=next_step;next_step+=1
  connection['fields'].update(ContainingRepresentationData='#'+str(rep['step_id']),PartId=str(int(rep['fields']['NextPartId'])+1),RelatingPart='#'+str(grid),RelatedPart='#'+str(part['step_id']))
  objects[part['step_id']]=part;objects[connection['step_id']]=connection
  parts.append(part['step_id']);connections.append(connection['step_id']);rep['fields']['NextPartId']=str(int(rep['fields']['NextPartId'])+2);added_cyl+=1
 rep['fields']['Parts']=listref(parts);rep['fields']['PartConnections']=listref(connections)
owned=set();todo=[template['step_id']]
while todo:
 n=todo.pop()
 if n in owned:continue
 owned.add(n);todo.extend(r for v in objects[n]['fields'].values() for r in refs(v) if r not in owned)
assert len(owned)<30
manager=objects[1];next_oid=int(manager['fields']['NextObjectId'])
oids=sorted({int(objects[n]['fields']['ObjectId']) for n in owned if 'ObjectId' in objects[n]['fields']})
name_id=next(n for n in refs(template['fields']['PropertySets']) if objects[n]['type']=='CommonInformationPropertySet')
coord_id=int(template['fields']['LocalCoordSys'][1:]);poly_id=int(template_rep['fields']['MultiPolygonSurface'][1:])
container=next(s for s in objects.values() if s['type']=='RelContainedInSpatialStructure' and template['step_id'] in refs(s['fields']['RelatedElements']))
f=json.loads((data/'furniture-proposal-v1.json').read_text());r=json.loads((data/'room-v1.json').read_text())
tasks=[];buffered=[]
for b in f['benches']:
 x,y=b['centre_m'];outer=box(-2.1,-1.3,2.1,1.3);inner=box(-1.6,-.8,1.6,.8)
 tasks.append({'name':'Surround-'+b['id'],'origin':[x,y,.8],'polygon':orient(outer.difference(inner),sign=1),'cylindrical':True,'expected_area_m2':outer.area-inner.area})
 buffered.append(box(x-2.1,y-1.3,x+2.1,y+1.3))
columns=[box(c['center_m'][0]-c['size_m'][0]/2,c['center_m'][1]-c['size_m'][1]/2,c['center_m'][0]+c['size_m'][0]/2,c['center_m'][1]+c['size_m'][1]/2) for c in r['obstacles']]
background=Polygon(r['contour']).difference(unary_union(buffered+columns));assert background.geom_type=='Polygon'
tasks.append({'name':'Background-floor','origin':[0.,0.,0.],'polygon':orient(background,sign=1),'cylindrical':False,'expected_area_m2':background.area})
if exposed_mode:
 tasks=[]
 # Match the native default 0.5 m evaluation edge zone. Remove only physical
 # column occlusion and luminaire apertures, with a stated 1 mm edge tolerance.
 panels=json.loads((data/'snapped-layout-proposal-v2.json').read_text())['fixtures']
 apertures=[box(p['position_m'][0]-.2985,p['position_m'][1]-.2985,p['position_m'][0]+.2985,p['position_m'][1]+.2985) for p in panels]
 ceiling=Polygon(r['contour']).buffer(-.5,join_style=2).difference(unary_union([c.buffer(.001,join_style=2) for c in columns]+apertures))
 ceiling_local=scale(ceiling,xfact=1,yfact=-1,origin=(0,0))
 tasks.append({'name':'Exposed-Ceiling','origin':[0.,0.,2.799],'axes':[[1.,0.,0.],[0.,-1.,0.],[0.,0.,-1.]],'polygon':ceiling_local,'cylindrical':False,'expected_area_m2':ceiling.area,'basis':'Native ceiling edge zone 0.5 m; exclude measured column footprints and 597 mm recessed fixture apertures. Evaluation plane 1 mm below ceiling.'})
 contour=r['contour']
 for i,(a,b) in enumerate(zip(contour,contour[1:]+contour[:1]),1):
  length=math.dist(a,b);tx,ty=(b[0]-a[0])/length,(b[1]-a[1])/length
  nx,ny=-ty,tx;mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
  # EN 12464-1:2021 5.4: excluded border <= min(15% of the
  # smallest surface dimension, 0.5 m). A 2.8 m wall gives 0.42 m.
  border=min(.15*min(length,r['height_m']),.5)
  half_height=r['height_m']/2
  surface=box(-length/2+border,-half_height+border,length/2-border,half_height-border);cuts=[]
  for c in columns:
   corners=list(c.exterior.coords)[:-1]
   depths=[nx*(x-mx)+ny*(y-my) for x,y in corners]
   if min(depths)<=.00101 and max(depths)>=-.00101:
    distances=[-tx*(x-mx)-ty*(y-my) for x,y in corners]
    cuts.append(box(min(distances)-.001,-1.5,max(distances)+.001,1.5))
  if cuts:surface=surface.difference(unary_union(cuts))
  tasks.append({'name':f'Exposed-Wall-{i:02}','origin':[mx+nx*.001,my+ny*.001,half_height],'axes':[[-tx,-ty,0.],[0.,0.,1.],[nx,ny,0.]],'polygon':surface,'cylindrical':False,'expected_area_m2':surface.area,'border_m':border,'basis':'EN 12464-1:2021 5.4 border min(15% of smallest surface dimension, 0.5 m); subtract wall portions physically behind measured columns, plus 1 mm numeric edge tolerance. Evaluation plane 1 mm into room.'})
new_roots=[];manifest=[]
for ordinal,task in enumerate(tasks,len(surfaces)+1):
 mapping={n:next_step+i for i,n in enumerate(sorted(owned))};next_step+=len(owned)
 oidmap={n:next_oid+i for i,n in enumerate(oids)};next_oid+=len(oids)
 for old in sorted(owned):
  s=copy.deepcopy(objects[old]);s['step_id']=mapping[old]
  for k,v in s['fields'].items():
   v=re.sub(r'#(\d+)',lambda m:'#'+str(mapping.get(int(m[1]),int(m[1]))),v)
   if k=='ObjectId':v=str(oidmap[int(v)])
   if k=='ObjectGuid':v="'"+str(uuid.uuid4())+"'"
   if old==name_id and k=='ObjectName':v="'"+task['name']+"'"
   if old==coord_id and k=='Origin':v=vector(task['origin'])
   if old==coord_id and k in ['XAxis','YAxis','ZAxis'] and 'axes' in task:v=vector(task['axes'][['XAxis','YAxis','ZAxis'].index(k)])
   components=list(task['polygon'].geoms) if task['polygon'].geom_type=='MultiPolygon' else [task['polygon']]
   components=[orient(p,sign=1) for p in components]
   if old==poly_id and k=='OuterLoops':v='('+', '.join(loop(p.exterior.coords) for p in components)+')'
   if old==poly_id and k=='InnerLoops':v='('+', '.join(loop(ring.coords) for p in components for ring in p.interiors)+')'
   s['fields'][k]=v
  objects[s['step_id']]=s
 new_rep=objects[mapping[template_rep['step_id']]]
 if not task['cylindrical']:
  unwanted={n for n in refs(new_rep['fields']['Parts']) if objects[n]['fields'].get('ResultType')=='.CylIllum.'}
  new_rep['fields']['Parts']=listref([n for n in refs(new_rep['fields']['Parts']) if n not in unwanted])
  new_rep['fields']['PartConnections']=listref([n for n in refs(new_rep['fields']['PartConnections']) if int(objects[n]['fields']['RelatedPart'][1:]) not in unwanted])
 new_roots.append(mapping[template['step_id']]);manifest.append({**{k:v for k,v in task.items() if k!='polygon'},'local_polygon_wkt':task['polygon'].wkt})
 manager['fields']['NameIndexMap']=manager['fields']['NameIndexMap'][:-1]+f", ({oidmap[int(template['fields']['ObjectId'])]}, {ordinal}))"
manager['fields']['NextObjectId']=str(next_oid)
collections=[]
for entry in split_fields(manager['fields']['ObjectCollections'][1:-1]):
 pair=split_fields(entry[1:-1])
 if pair[0]=="'InstanceObject'":pair[1]=pair[1][:-1]+''.join(', #'+str(n) for n in new_roots)+')'
 collections.append('('+', '.join(pair)+')')
manager['fields']['ObjectCollections']='('+', '.join(collections)+')'
indices=[]
for entry in split_fields(manager['fields']['ObjectIndices'][1:-1]):
 pair=split_fields(entry[1:-1]);counter=objects[int(pair[0][1:])]
 if "'CalculationGridSurface'" in counter['fields'].values():pair[1]=str(int(pair[1])+len(tasks))
 indices.append('('+', '.join(pair)+')')
manager['fields']['ObjectIndices']='('+', '.join(indices)+')'
container['fields']['RelatedElements']=container['fields']['RelatedElements'][:-1]+''.join(f', (#{n}, $)' for n in new_roots)+')'
with zipfile.ZipFile(source) as zi:
 text=zi.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
 for n,s in original.items():
  if objects[n]['fields']!=s['fields']:assert text.count(s['raw'])==1;text=text.replace(s['raw'],serialize(objects[n]))
 pos=text.index('ENDSEC;',text.index('DATA;'));text=text[:pos]+'\r\n'.join(serialize(s) for n,s in objects.items() if n not in original)+'\r\n'+text[pos:]
 with zipfile.ZipFile(target,'x') as zo:
  for item in zi.infolist():
   if item.filename.startswith('Project/Results/'):continue
   zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
check=read(target);assert all(n in check['objects'] for s in check['objects'].values() for v in s['fields'].values() for n in refs(v))
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256']
record={'status':'auxiliary native geometry proposed; fresh native calculation and persistence required','source_sha256':d['sha256'],'output_sha256':check['sha256'],'added_cylindrical_parameters':added_cyl,'removed_auxiliary_ugr_parameters':removed_ugr,'retained_ugr_evidence':'office-powerbalance-grid-native-v4.evo remains unchanged','added_surrounding_and_background_surfaces':len(tasks),'surfaces':manifest,'fixture_geometry_and_photometry_unchanged':True}
target.with_suffix('.brightness.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='surfaces'},indent=2))
