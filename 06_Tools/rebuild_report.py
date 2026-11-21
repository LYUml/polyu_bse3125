"""Rebuild the current report from the organised workspace into a fresh directory."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[1];out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else r/'04_Report/Build'
assert r in out.parents and not out.exists(),'Choose a fresh output directory inside the workspace'
out.mkdir(parents=True)
scripts=r/'06_Tools/report';main=out/'main-report.pdf';appendix=out/'comparison-appendix.pdf';final=out/'BSE3125_Lighting_Design_Report.pdf'
for script,args in [('build_latex_report.py',[main]),('build_comparison_appendix.py',[appendix]),('assemble_comparison_report.py',[main,final,appendix])]:
 subprocess.run([sys.executable,'-X','utf8',str(scripts/script),*map(str,args)],cwd=r,check=True)
print('Rebuilt report: '+str(final))
