"""Read-only UI inventory through the toolkit's native project guard and lease."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'dialux-agent-toolkit'))
from src.windows_worker import connect,prepare_project
from src.desktop_lock import desktop_lease
with desktop_lease():
 app,main,process=connect()
 prepare_project(app,main,process,sys.argv[1])
 items=[]
 for c in main.descendants():
  info=c.element_info
  if info.control_type not in {'TabItem','Button','Edit','CheckBox','RadioButton','ComboBox','MenuItem','ListItem','Text'}:continue
  try:
   if not c.is_visible():continue
   rec={'type':info.control_type,'id':info.automation_id,'text':c.window_text(),'enabled':c.is_enabled()}
   if info.control_type=='Edit':rec['value']=c.get_value()
   if info.control_type=='CheckBox':rec['checked']=c.get_toggle_state()
   items.append(rec)
  except Exception as e:items.append({'id':info.automation_id,'error':str(e)})
 result={'project':sys.argv[1],'title':main.window_text(),'controls':items}
 target=Path(sys.argv[2]); target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():raise ValueError('Use new output path')
 target.write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps([r for r in items if r['type']!='Text'],indent=2))
