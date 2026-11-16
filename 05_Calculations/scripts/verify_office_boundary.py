"""Verify measured office-side source wall faces against the saved native contour."""
from pathlib import Path
import ast, hashlib, json, sys
import ezdxf
from shapely.geometry import Polygon
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '06_Tools'))
from read_native_archive import read

root=Path(__file__).resolve().parents[2]
source=root.parent/'dialux-agent-toolkit/local/bse3125-native-v2/source-copy.dxf'
native=root/'05_Calculations/models/office-powerbalance-grid-native-v4.evo'
review=json.loads((root/'05_Calculations/data/geometry-review.json').read_text())
room=json.loads((root/'05_Calculations/data/room-v1.json').read_text())
doc=ezdxf.readfile(source)
origin=review['drawing_origin_wcs_m']
faces=[]
for handle in ['3E42','3E43','3D31','3E3E','3E3F','3E23']:
 e=doc.entitydb[handle]
 assert e.dxftype()=='LINE'
 points=[[p.x/1000-origin[0],p.y/1000-origin[1]] for p in [e.dxf.start,e.dxf.end]]
 faces.append({'source_handle':handle,'endpoints_design_m':points})
for face in faces:
 axis=0 if face['source_handle'] in ['3D31','3E23'] else 1
 expected={'3D31':30.863333,'3E23':30.713333}.get(face['source_handle'],20.67 if face['source_handle'] in ['3E42','3E43'] else 20.85)
 assert max(abs(p[axis]-expected) for p in face['endpoints_design_m'])<.000001
d=read(native)
contours=[o for o in d['objects'].values() if o['type']=='StoreyContourRepresentationData' and o['fields']['ContourType']=='.Inner.']
assert len(contours)==1
points=ast.literal_eval(contours[0]['fields']['Points'])
measured=Polygon(room['contour']); model=Polygon(points)
distance=measured.hausdorff_distance(model)
assert distance<=.00051
result={'status':'source office-side wall faces and saved native inner contour verified; columns audited separately',
 'source_dxf_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_sha256':d['sha256'],
 'source_faces':faces,'native_contour_m':points,'maximum_boundary_deviation_m':distance,
 'measured_gross_area_m2':measured.area,'native_gross_area_m2':model.area,
 'annotated_area_m2':1022,'annotation_is_not_boundary_measurement':True,
 'interpretation':'Office lies south of the core north wall and east of the core east wall. Use y=20.67 and x=30.863333 office-facing surfaces; opposite core faces are y=20.85 and x=30.713333. Bridge door openings at the office boundary; core excluded.'}
out=root/'05_Calculations/data/office-boundary-verification-v1.json'
assert not out.exists()
out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
