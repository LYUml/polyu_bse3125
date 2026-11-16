"""Verify exact fresh/reopened native result rows and the reopened disk checkpoint."""
from pathlib import Path
import sys,json,hashlib
fresh,reopened,checkpoint,out=map(Path,sys.argv[1:5]);assert not out.exists()
a,b,c=[json.loads(p.read_text()) for p in [fresh,reopened,checkpoint]]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
key='tasks' if 'tasks' in a else 'surfaces'
assert len(a[key])==(112 if key=='tasks' else 288)
assert a[key]==b[key], 'Fresh and reopened rows differ'
assert sha(a['pdf'])==a['pdf_sha256'] and sha(b['pdf'])==b['pdf_sha256']
assert sha(c['path'])==c['sha256'], 'Disk checkpoint changed after reopen'
record={'status':'verified','native_path':c['path'],'native_sha256':c['sha256'],'fresh_result_file':str(fresh),'reopened_result_file':str(reopened),'fresh_pdf_sha256':a['pdf_sha256'],'reopened_pdf_sha256':b['pdf_sha256'],'exact_preserved_rows':len(a[key]),'saved_bytes_unchanged_after_reopen_export':True}
out.write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
