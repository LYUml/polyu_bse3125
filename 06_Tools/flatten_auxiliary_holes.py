"""Represent exact exposed regions as disjoint native outer-loop triangles.

The previous native ceiling result still sampled an occluded point despite inner
loops. Use equivalent explicit polygons and verify their union before native use.
"""
from pathlib import Path
import sys,json,ast,zipfile,hashlib
import shapely
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from read_native_archive import read,split_fields
source,target=map(Path,sys.argv[1:3]);assert not target.exists();d=read(source)
def real(v):
 s=format(v,'.16g');return s if '.' in s or 'e' in s.lower() else s+'.'
def encode(ring):return '('+', '.join('('+', '.join(real(v) for v in p)+')' for p in list(ring.coords)[:-1])+')'
with zipfile.ZipFile(source) as z:text=z.read('Project/ProjectData/ProjectData.dat').decode('utf-8-sig')
changes=[]
for o in d['objects'].values():
 if o['type']!='MultiPolygonSurface2D' or o['fields']['InnerLoops']=='()':continue
 f=dict(o['fields']);outers=[ast.literal_eval(x) for x in split_fields(f['OuterLoops'][1:-1])];inners=[ast.literal_eval(x) for x in split_fields(f['InnerLoops'][1:-1])]
 polygons=[Polygon(outer,[hole for hole in inners if Polygon(outer).covers(Polygon(hole).representative_point())]) for outer in outers]
 region=unary_union(polygons);assert region.is_valid
 triangles=list(shapely.constrained_delaunay_triangles(region).geoms)
 assert all(p.geom_type=='Polygon' and not p.interiors for p in triangles)
 rebuilt=unary_union(triangles);error=region.symmetric_difference(rebuilt).area
 assert error<1e-7 and abs(sum(p.area for p in triangles)-region.area)<1e-7
 f['OuterLoops']='('+', '.join(encode(orient(p,sign=1).exterior) for p in triangles)+')';f['InnerLoops']='()'
 row=f"#{o['step_id']} = MultiPolygonSurface2D ("+', '.join(f.values())+');'
 assert text.count(o['raw'])==1;text=text.replace(o['raw'],row)
 changes.append({'step_id':o['step_id'],'original_hole_count':len(inners),'triangle_count':len(triangles),'area_m2':region.area,'symmetric_difference_area_m2':error})
assert len(changes)==30
with zipfile.ZipFile(source) as zi,zipfile.ZipFile(target,'x') as zo:
 for item in zi.infolist():
  if item.filename=='Project/ScenegraphScene' or item.filename.startswith('Project/Results/'):continue
  zo.writestr(item,text.encode('utf-8-sig') if item.filename=='Project/ProjectData/ProjectData.dat' else zi.read(item))
check=read(target);assert len(check['objects'])==len(d['objects'])
record={'status':'equivalent explicit exposed polygons; native calculation/geometry verification pending','source_sha256':d['sha256'],'output_sha256':check['sha256'],'shapely_version':shapely.__version__,'fixture_and_photometry_records_unchanged':True,'cached_scene_and_results_omitted':True,'changed_regions':changes}
target.with_suffix('.regions.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps({'region_count':len(changes),'triangle_count':sum(c['triangle_count'] for c in changes),'maximum_area_error_m2':max(c['symmetric_difference_area_m2'] for c in changes),'output_sha256':check['sha256']},indent=2))
