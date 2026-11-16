"""Select the toolkit's supported lighting view before checking saved results."""
from pathlib import Path
import sys,json
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root.parent/'dialux-agent-toolkit'))
from src.windows_worker import connect,prepare_project,select_lighting_tool,snapshot
from src.desktop_lock import desktop_lease
out=Path(sys.argv[2]);assert not out.exists()
with desktop_lease():
    app,main,process=connect()
    prepare_project(app,main,process,sys.argv[1])
    select_lighting_tool(main,'LuminaireArrangementTool')
    state=snapshot(app,main,process)
out.write_text(json.dumps(state,indent=2));print(json.dumps(state,indent=2))
