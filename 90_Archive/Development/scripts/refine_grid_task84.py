"""One source-tile correction prompted by the actual Desk-084 result of 497 lx."""
from pathlib import Path
import json,hashlib,math
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data'
source=data/'snapped-layout-proposal-v1.json';out=data/'snapped-layout-proposal-v2.json';assert not out.exists()
p=json.loads(source.read_text());f=next(x for x in p['fixtures'] if x['id']=='L120')
assert all(abs(a-b)<1e-8 for a,b in zip(f['position_m'][:2],[18.48,19.77]))
tiles=json.loads((data/'ceiling-candidates-v1.json').read_text())['tiles']
t=[t for t in tiles if math.dist(t['center_m'],[18.48,19.17])<1e-6];assert len(t)==1
assert t[0]['handle'] not in {x['source_tile_handle'] for x in p['fixtures']}
old=f['position_m'][:];f['position_m'][1]-=.6;f['local_origin_m'][1]-=.6
f['source_tile_handle']=t[0]['handle'];f['displacement_m']=math.dist(f['position_m'][:2],f['original_position_m'][:2])
p['previous_plan_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
p['refinement']={'fixture_id':'L120','from_m':old,'to_m':f['position_m'],'source_tile_handle':t[0]['handle'],'trigger_report_sha256':json.loads((data/'grid-tasks-results-v2.json').read_text())['pdf_sha256'],'reason':'Desk-084 average 497 lx; move one tile (0.6 m) south toward bench B21. Retain all 186 luminaires and photometry; re-evaluate every task, not only this desk.'}
out.write_text(json.dumps(p,indent=2),encoding='utf-8');print(json.dumps(p['refinement'],indent=2))
