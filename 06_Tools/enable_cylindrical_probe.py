"""Enable the observed native cylindrical parameter on selected Desk-001 only."""
from pathlib import Path
import sys,json,time
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root.parent/'dialux-agent-toolkit'))
from src.windows_worker import connect,prepare_project,unique_control,snapshot
from src.desktop_lock import desktop_lease
project,out=sys.argv[1],Path(sys.argv[2]);assert not out.exists()
with desktop_lease():
 app,main,process=connect();prepare_project(app,main,process,project)
 assert unique_control(main,'Edit','ObjectName').get_value()=='Desk-001'
 assert not snapshot(app,main,process)['controls']['DiscardResultsButton']['enabled']
 button=unique_control(main,'Button','CylIllum');before=button.iface_toggle.CurrentToggleState
 if before==0:button.iface_toggle.Toggle()
 time.sleep(.3);assert button.iface_toggle.CurrentToggleState==1
 edits=[]
 for c in main.descendants(control_type='Edit'):
  if 'HeightOffset' in c.element_info.automation_id:edits.append({'id':c.element_info.automation_id,'value':c.get_value()})
 result={'status':'cylindrical parameter enabled on native Desk-001; offset not yet configured','before':before,'after':button.iface_toggle.CurrentToggleState,'offset_fields':edits,'state':snapshot(app,main,process)}
 out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
