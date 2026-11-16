"""Summarize verified native comparisons for report authoring, without synthetic results."""
from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[2];d=r/'05_Calculations/data'
load=lambda p:json.loads(p.read_text())
cases=[]
for name,core,aux in [('Baseline','review-40s-reopened-tasks-v4.json','review-brightness-reopened-results-v4.json'),('90% output','comparison-output90-core-reopened-results-v1.json','comparison-output90-aux-reopened-results-v2.json'),('Lower reflectance','comparison-reflectance-core-reopened-results-v1.json','comparison-reflectance-aux-reopened-results-v1.json')]:
    t,a=load(d/core),load(d/aux)
    assert len(t['tasks'])==112 and len(a['surfaces'])==288
    assert a['all_six_groups_present']
    for item in [t,a]:assert hashlib.sha256(Path(item['pdf']).read_bytes()).hexdigest()==item['pdf_sha256']
    checks={c['group']:c for c in a['checks']}
    cases.append({'name':name,'core_source':core,'aux_source':aux,'minimum_task_average_lx':t['minimum_task_average_lx'],'minimum_task_u0':t['minimum_task_u0'],'maximum_directional_ugr':t['maximum_directional_ugr'],'mean_of_desk_averages_lx':sum(x['average_lx'] for x in t['tasks'])/112,'critical_average_desks':[x['name'] for x in t['tasks'] if x['average_lx']==t['minimum_task_average_lx']],'critical_uniformity_desks':[x['name'] for x in t['tasks'] if x['u0']==t['minimum_task_u0']],'critical_glare_desks':[{'name':x['name'],'direction_deg':x['worst_direction_deg']} for x in t['tasks'] if x['max_directional_ugr']==t['maximum_directional_ugr']],'task_metrics_pass':t['all_tasks_pass_course_metrics'],'auxiliary_checks':checks,'combined_seated_cylindrical':a['combined_seated_cylindrical'],'all_selected_metrics_pass':t['all_tasks_pass_course_metrics'] and a['all_present_groups_pass']})
out=r/'05_Calculations/Final_v04/comparison-summary.json';assert not out.exists()
out.write_text(json.dumps({'status':'Native result summary; acceptance includes separate persistence checks','cases':cases,'common_connected_power_W':4328,'common_conservative_LPD_W_m2':4328/1022,'power_scope':'90% luminous output does not establish90%electric input; connected load unchanged','isolation':'Two separate single-factor scenarios, not a combined90%output+lower-reflectance test'},indent=2))
print(json.dumps(cases,indent=2))
