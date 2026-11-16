"""Assignment adapter: configure one already-created native calculation surface.

Reuses toolkit exact-project/dialog/desktop guards. Does not create surfaces or
retry partial edits. The operator must select and inspect the intended surface.
"""
from pathlib import Path
import sys,json,time,math,datetime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'dialux-agent-toolkit'))
from src.windows_worker import connect,prepare_project,snapshot,unique_control
from src.desktop_lock import desktop_lease
request=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
out=Path(request['evidence']); out.parent.mkdir(parents=True,exist_ok=True)
if out.exists():raise ValueError('Use fresh evidence path; inspect after failure')
journal={'request':request,'state':'starting','steps':[]}
def persist():out.write_text(json.dumps(journal,indent=2),encoding='utf-8')
persist()
try:
 with desktop_lease():
  app,main,process=connect(); prepare_project(app,main,process,request['expected_project'])
  edits={}
  for c in main.descendants(control_type='Edit'):
   if c.is_visible():edits.setdefault(c.element_info.automation_id,[]).append(c)
  def edit(k):
   a=edits.get(k,[])
   if len(a)!=1:raise ValueError('Missing/ambiguous field '+k)
   return a[0]
  assert edit('ObjectName').get_value()==request['expected_name'],'Unexpected selected surface'
  allowed={'Positioning_X','Positioning_Y','Positioning_Z','Size_X','Size_Y','HeightOffset_Ugr','StepSize_Ugr','AngleRangeBegin_Ugr','AngleRangeEnd_Ugr'}
  assert set(request['values'])<=allowed
  assert all(type(v) in (int,float) and math.isfinite(v) for v in request['values'].values())
  assert not snapshot(app,main,process)['controls']['DiscardResultsButton']['enabled'],'Clear results explicitly before configuration'
  journal['before']={k:edit(k).get_value() for k in request['values']};persist()
  for key,value in request['values'].items():
   journal['state']='pending_edit';journal['pending_field']=key;persist()
   c=edit(key); c.set_focus();c.iface_value.SetValue(str(value));c.type_keys('{TAB}',set_foreground=False)
   time.sleep(.3)
   actual=c.get_value()
   if abs(float(actual)-value)>.00051:raise ValueError('Readback mismatch '+key)
   journal['steps'].append({'field':key,'value':actual});persist()
  journal['after']={k:edit(k).get_value() for k in request['values']}
  if request.get('enable_ugr'):
   buttons=[c for c in main.descendants(control_type='Button') if c.element_info.automation_id=='Ugr' and c.is_visible()]
   assert len(buttons)==1
   journal['state']='pending_enable_ugr';persist()
   toggle=buttons[0].iface_toggle
   journal['ugr_before']=toggle.CurrentToggleState
   if toggle.CurrentToggleState==0:toggle.Toggle()
   time.sleep(.4)
   journal['ugr_after']=toggle.CurrentToggleState
   if toggle.CurrentToggleState!=1:raise ValueError('UGR toggle not enabled')
  journal['final_state']=snapshot(app,main,process)
  if journal['final_state']['dialogs']:raise ValueError('Dialog after surface configuration')
  journal['state']='configured_unsaved';persist();print(json.dumps(journal,indent=2))
except BaseException as e:
 journal['state']='failed_inspect_before_retry';journal['error']=str(e);persist();raise
