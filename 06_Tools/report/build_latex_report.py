"""Render the report's engineering figures and compile its nine narrative pages."""
from pathlib import Path
import os
import subprocess
import sys

import pypdfium2 as pdfium
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from report_figures import calculation_heights, layout_polar, task_map, zone_map

root = Path(__file__).resolve().parents[2]
output = Path(sys.argv[1]).resolve()
if output.exists():
    raise FileExistsError(output)
for alias, filename in [("Body", "times.ttf"), ("Bold", "timesbd.ttf")]:
    pdfmetrics.registerFont(TTFont(alias, str(Path(os.environ["WINDIR"]) / "Fonts" / filename)))
for name, draw in [("heights", calculation_heights), ("layout", layout_polar),
                   ("tasks", task_map), ("zones", zone_map)]:
    renderPDF.drawToFile(draw(), str(output.parent / (name + ".pdf")))

with pdfium.PdfDocument(root / "03_Engineering/Native_Reports/Final_Workstations.pdf") as native:
    # Bounds are fractions of each native page measured from its top left.
    panels = [
        ("workplane", 254, (.12, .21, .90, .59)),
        ("placement", 256, (.12, .20, .90, .59)),
        ("desk", 529, (.14, .31, .95, .63)),
        ("observer", 316, (.09, .195, .405, .43)),
    ]
    for name, number, (left, top, right, bottom) in panels:
        page = native[number - 1]
        width, height = page.get_size()
        crop = (width * left, height * (1 - bottom), width * (1 - right), height * top)
        page.render(scale=3, crop=crop).to_pil().save(output.parent / (name + ".png"))

env = os.environ.copy()
env["TEXINPUTS"] = str(output.parent) + os.pathsep + env.get("TEXINPUTS", "") + os.pathsep
for source, job in [("main.tex", output.stem), ("appendix-d.tex", "native-views")]:
    subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                "-output-directory=" + str(output.parent), "-jobname=" + job, source],
               cwd=root / "04_Report/LaTeX", env=env, check=True)
with pdfium.PdfDocument(output) as report:
    if len(report) != 9:
        raise ValueError(f"Expected nine narrative pages, found {len(report)}")
