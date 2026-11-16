"""Resolve a historical evidence path through the verified relocation index."""
from pathlib import Path
import json,sys
r=Path(__file__).resolve().parents[1]
def resolve(value):
 p=Path(value);p=p if p.is_absolute() else r/p
 if p.exists():return p.resolve()
 try:key=p.relative_to(r).as_posix()
 except ValueError:raise FileNotFoundError(value)
 lookup=json.loads((r/'05_Calculations/workspace-migration.json').read_text())['path_lookup']
 if key not in lookup:raise FileNotFoundError(value)
 result=r/lookup[key]
 if not result.exists():raise FileNotFoundError(result)
 return result.resolve()
if __name__=='__main__':print(resolve(sys.argv[1]))
