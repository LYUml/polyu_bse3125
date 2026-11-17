"""Requirement-by-requirement handover audit after recorded visual inspection."""
from pathlib import Path
import hashlib,json,re,shutil
import pdfplumber,pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data';folder=root/'05_Calculations/Final_v02'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=folder/'BSE3125-report-review-v2.pdf';assembly=load(review.with_suffix('.manifest.json'))
assert sha(review)==assembly['sha256'] and assembly['bytes']==review.stat().st_size<=10000000
assert assembly['main_report_pages_including_CAD']==8 and assembly['total_pages']==191
assert len(assembly['page_preservation'])==191 and all(x['unchanged_text_size_and_72_150dpi_pixels'] for x in assembly['page_preservation'])
inputs=[(root/'01_Assignment_Brief/BSE3125 DIALux Assignment 2627.pdf','1774438e251086dd20f93e571f7021b7eb612b0ed8edcef19a4d73cc443edcfc'),(root/'01_Assignment_Brief/Building_Drawings/Project layout.dwg','5c5f0360987784171dc3b798132b25046cbd8253cf5566ba8eb2d110d1315c20')]
for p,h in inputs:assert sha(p)==h
core=load(data/'refined-native-persistence-v1.json');aux=load(data/'brightness-openings-persistence-v9.json');geometry=load(data/'brightness-saved-geometry-v9c.json')
for p,h in [(Path(core['native_path']),core['native_sha256']),(Path(aux['native_path']),aux['native_sha256'])]:assert sha(p)==h
assert aux['status']=='verified' and aux['all_288_auxiliary_result_rows_identical'] and geometry['maximum_symmetric_difference_area_m2']==0
assert geometry['all_186_fixture_maintenance_factors']==.8 and geometry['room_storey_contours_column_instances_and_prototype_geometry_match_core']
assert core['all_112_task_results_preserved'] and core['all_186_report_positions_preserved'] and core['all_112_task_geometry_and_ugr_parameters_verified']
task_results=load(data/'grid-reopened-tasks-v4.json');brightness=load(data/'brightness-reopened-results-v9.json')
assert task_results['all_tasks_pass_course_metrics'] and len(task_results['tasks'])==112
assert brightness['all_present_groups_pass'] and brightness['all_six_groups_present'] and brightness['combined_seated_cylindrical']['pass']
cad=load(root/'05_Calculations/Final_v01/cad-native-v3/manifest.json');plot=load(root/'05_Calculations/Final_v01/cad-plot-v3/manifest.json');visual=load(data/'cad-visual-review-v3.json')
assert sha(Path(cad['dwg']))==cad['dwg_sha256'] and cad['native_reopen_verified'] and cad['fixture_records_verified'] and cad['fixture_count']==186
assert sha(Path(plot['pdf']))==plot['pdf_sha256']==visual['pdf_sha256'] and plot['all_fixture_labels_verified'] and plot['physical_scale']['verified'] and all(visual['checks'].values())
shared=data/'snapped-layout-proposal-v2.json';assert sha(shared)=='a141f488b1055afd98aae9ee7ade9111f39ac0d8cbf4bfc3d41b8b6ab2383789'
controls=load(data/'controls-proposal-v1.json');assert controls['layout_sha256']==sha(shared) and controls['zone_count']==controls['manual_control_points']==32 and controls['maximum_zone_area_m2']<250
pdf=pdfium.PdfDocument(review);assert len(pdf)==191
text='\n'.join(pdf[i].get_textpage().get_text_range() for i in range(7))
for value in ['DIALux workflow','Luminaire selection','Criteria and calculated performance','Controls, power','References','504 lx','17.5','116 lx','3.689','0.8037']:assert value in text,value
assert 'WORKING DRAFT' not in text
cad_text=pdf[7].get_textpage().get_text_range();ids=set(re.findall(r'\bL\d{3}\b',cad_text));assert ids=={f'L{i:03}' for i in range(1,187)}
assert 'LUMINAIRE SCHEDULE' in cad_text and 'LEGEND' in cad_text and '1:100' in cad_text
with pdfplumber.open(review) as document:
 for page in document.pages[:7]:
  content=[c for c in page.chars if c['top']<790]
  assert content and min(c['x0'] for c in content)>=40 and max(c['x1'] for c in content)<=page.width-40
  assert min(c['top'] for c in content)>=40 and max(c['bottom'] for c in content)<790
requirements=[
 ('Original brief/DWG preservation','Verified exact input hashes.'),
 ('DIALux functions and procedure, 20%','Main p2: native calculation figure, modelling, manufacturer data, calculation objects, maintenance and persistence.'),
 ('Luminaire/system justification, 20%','Main pp3,6: product selection, grid coordination, mounting reference, 32-zone control and power budget.'),
 ('Criteria summary, 15%','Main p5; exact EN edition/clauses and BEC 2024 review in reference register. All adopted native numerical criteria pass.'),
 ('Performance discussion, 25%','Main pp4,6,7: failed iterations, distinct critical desks, 4 lx margin, maintenance, controls and stated limits.'),
 ('Independent lighting plan, 20%','Main p8: native-reopened independent A2 1:100 CAD plot, 186 tile-linked fixtures, legend, schedule and dimensions.'),
 ('Shared design and manufacturer photometry','186 fixture coordinates/GUIDs, all maintenance factors and 63-record photometry graph match verified core model. CAD shares the same dataset.'),
 ('Measured geometry versus assumptions','Office-facing wall survey and eight-column native checks; measured gross/net versus annotation discrepancy retained. Furniture, finishes and controls explicitly assumed.'),
 ('All tasks and supplemental metrics','112 desks; actual directional UGR; 140 seated cylindrical surfaces; surrounding/background and exposed walls/ceiling. 255 native openings independently reconstructed.'),
 ('Save/reopen evidence','Core and supplemental native projects saved, closed and reopened; results retained and saved bytes unchanged.'),
 ('One PDF and size/page limits','8 main pages including CAD; 191 total pages including appendix; 5,859,608 bytes, below 10,000,000.'),
 ('Authentic simulation appendix','182 original native pages; text, page dimensions and exact 72/150-dpi rendered pixels preserved during extraction and assembly.'),
 ('Visual inspection','All main pages reviewed as rendered contact sheets; detailed review of native plot, criterion table, references, independent CAD and appendix guide; representative native tables/plots reviewed.'),
 ('Editable sources and native files','Report JSON/Python and figure in Final_v02; native evo files in models; editable DXF/native DWG under Final_v01, listed in handover manifest.'),
 ('Repository reuse','Pinned toolkit CLI/backend, MIT upstream STF implementation, Shapely, ezdxf, PDFium and pikepdf documented in reuse register. Failed geometry experiments rejected, not used as performance evidence.'),
 ('No course submission','Local deliverable preparation and authorized GitHub synchronization only; no Blackboard/Canvas submission.')]
handover={'status':'assignment deliverable accepted for handover under documented academic assumptions','review_pdf_sha256':sha(review),'main_pages':8,'total_pages':191,'bytes':review.stat().st_size,'requirements':[{'requirement':name,'status':'verified','evidence':evidence} for name,evidence in requirements],
 'qualified_scope':['DSE luminance is a bounded sampled screening, not complete 65-90-degree certification.','Controls are specified design/commissioning provisions, not installed/tested-system evidence.','No unconditional whole-standard or statutory certification is claimed; actual glazing, occupancy and maintenance assumptions are documented.'],
 'visual_review_artifacts':'05_Calculations/sessions/final-review-v2',
 'core_native':{'path':core['native_path'],'sha256':core['native_sha256']},'supplemental_native':{'path':aux['native_path'],'sha256':aux['native_sha256']},'editable_CAD':{'path':cad['dwg'],'sha256':cad['dwg_sha256']},'editable_report':['05_Calculations/Final_v02/report-content-v1.json','05_Calculations/scripts/build_main_report.py','05_Calculations/scripts/assemble_submission.py'],'shared_fixture_dataset':str(shared)}
final=root/'00_Submit/BSE3125_Lighting_Design_Report.pdf';assert not final.exists();final.parent.mkdir(exist_ok=True);shutil.copyfile(review,final);assert sha(final)==sha(review)
handover['final_pdf']=str(final);handover['final_pdf_sha256']=sha(final)
out=folder/'assignment-acceptance-v1.json';assert not out.exists();out.write_text(json.dumps(handover,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in handover.items() if k not in ['requirements']},indent=2))
