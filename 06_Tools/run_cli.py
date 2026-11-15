"""Run the external toolkit and retain exact JSON/stdout evidence per operation.

Usage: toolkit_python run_cli.py evidence.json desktop-status
One operation at a time; this wrapper never retries desktop mutations.
"""
from pathlib import Path
import sys,subprocess,json,datetime,hashlib
ROOT=Path(__file__).resolve().parents[1]
TOOLKIT=ROOT.parent/'dialux-agent-toolkit'
out=Path(sys.argv[1]).resolve()
if out.exists():raise SystemExit('Choose a new evidence file; existing evidence is immutable.')
out.parent.mkdir(parents=True,exist_ok=True)
args=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run([str(TOOLKIT/'.venv/Scripts/python.exe'),'-m','src.dialux_agent',*args],cwd=TOOLKIT,capture_output=True,text=True,encoding='utf-8',errors='replace')
record={'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolkit_commit':subprocess.check_output(['git','-C',str(TOOLKIT),'rev-parse','HEAD'],text=True).strip(),'arguments':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
try:record['result']=json.loads(p.stdout)
except json.JSONDecodeError:pass
with out.open('x',encoding='utf-8') as f:json.dump(record,f,indent=2,ensure_ascii=False)
print(p.stdout,end=''); print(p.stderr,end='',file=sys.stderr)
raise SystemExit(p.returncode)
