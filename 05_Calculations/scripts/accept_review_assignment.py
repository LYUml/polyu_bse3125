"""Final strict-review acceptance: assertions against actual artifacts, not synthetic results."""
from pathlib import Path
import hashlib,json,math,re,shutil,sys
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[2];data=root/'05_Calculations/data';folder=root/'05_Calculations/Final_v03'
sys.path.insert(0,str(root/'06_Tools/.runtime'));import pikepdf
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=folder/'BSE3125-report-review-v3.pdf';assembly=load(review.with_suffix('.manifest.json'))
assert sha(review)==assembly['sha256'] and review.stat().st_size==assembly['bytes']<=10000000
assert assembly['main_report_pages_including_CAD']==9<=10 and assembly['total_pages']==192
assert len(assembly['page_preservation'])==192 and all(p['unchanged_text_size_and_72_150dpi_pixels'] for p in assembly['page_preservation'])
inputs=[(root/'01_Assignment_Brief/BSE3125 DIALux Assignment 2627.pdf','1774438e251086dd20f93e571f7021b7eb612b0ed8edcef19a4d73cc443edcfc'),(root/'01_Assignment_Brief/Building_Drawings/Project layout.dwg','5c5f0360987784171dc3b798132b25046cbd8253cf5566ba8eb2d110d1315c20')]
for p,h in inputs:assert sha(p)==h
persistence=load(data/'review-native-persistence-v4.json');assert persistence['status']=='verified'
for p in persistence['projects']:assert sha(Path(p['native_path']))==p['native_sha256'] and sha(Path(p['reopened_pdf']))==p['reopened_pdf_sha256']
tasks=load(data/'review-40s-reopened-tasks-v4.json');aux=load(data/'review-brightness-reopened-results-v4.json');geometry=load(data/'review-brightness-saved-geometry-v4.json')
assert tasks['task_count']==112 and tasks['all_tasks_pass_course_metrics'] and aux['all_six_groups_present'] and aux['all_present_groups_pass'] and len(aux['surfaces'])==288
assert geometry['effective_region_count']==36 and geometry['native_opening_count']==255 and geometry['maximum_symmetric_difference_area_m2']==0
shared=data/'snapped-layout-proposal-v3.json';plan=load(shared);control=load(data/'controls-proposal-v2.json');assert control['layout_sha256']==sha(shared) and control['zone_count']==control['manual_control_points']==32
assert control['maximum_zone_area_m2']<250 and len(plan['fixtures'])==186 and {x['product_order_code'] for x in plan['fixtures']}=={'910505103638'}
positions=load(data/'review-40s-positions-v4.json');assert positions['plan_sha256']==sha(shared) and positions['fixture_count']==186 and positions['maximum_coordinate_error_m']<1e-6
cad=load(folder/'cad-native-v5/manifest.json');plot=load(folder/'cad-plot-v5/manifest.json')
assert cad['fixture_count']==186 and cad['native_reopen_verified'] and cad['fixture_records_verified'] and cad['block_shapes_verified'] and cad['schedule_records_verified']
assert sha(Path(cad['dwg']))==cad['dwg_sha256'] and sha(Path(plot['pdf']))==plot['pdf_sha256'] and plot['visual_review_verified'] and plot['physical_scale']['verified']
doc=pdfium.PdfDocument(review);texts=[doc[i].get_textpage().get_text_range() for i in range(len(doc))];main='\n'.join(texts[:8]);assert len(doc)==192
for text in ['593','0.80','18.1','910505103638','4328','4.235','533.7','4755.8','1334','1468','82 mm','86 mm','standby','0.16 m','525/593','1022','1032.57','1042.10','32 independent','500 lx','15-degree']:
 assert text in main,text
for page,text in [(0,'Design basis'),(1,'DIALux functions'),(2,'Luminaire selection'),(3,'Iteration'),(4,'Criteria'),(5,'Controls'),(6,'Robustness'),(7,'References'),(8,'BSE3125-L01'),(9,'combined pages 1-9'),(10,'4000 lm'),(153,'Background-floor')]:assert text in texts[page],(page,text)
for prohibited in ['Vacancy operation reduces power to zero','very low minimum on the original automatic whole-room workplane occurs','1134.23']:
 assert prohibited not in main
assert not any('WORKING DRAFT' in t for t in texts[:10])
assert abs((186*23+50)/1022-4.234833659)<1e-8
assert abs((186*23*1.1+50)/1022-4.653424658)<1e-8
assert abs(593*.9-533.7)<1e-8 and 18.1+8*math.log10(1.1)<19
assert abs(.9*1*.95*.94-.8037)<1e-8
with pikepdf.open(review) as p:
 with p.open_outline() as outline:
  assert len(outline.root)==5 and len(outline.root[0].children)==8 and len(outline.root[3].children)==8
  for item in [*outline.root,*outline.root[0].children,*outline.root[3].children,*outline.root[4].children]:assert item.destination is not None
review_notes={
 'R01':'Actual 4000 lm native replacement/recalculation; minimum 593 lx, common -10% analytical sensitivity 533.7 lx.',
 'R02':'0% light output distinguished from standby; >=50% standby-inclusive power reduction is a commissioning requirement.',
 'R03':'Controls criteria table on p6 covers manual count, power reduction, zone area, override, vacancy and conditional daylight.',
 'R04':'Explicit combined/native page distinction, appendix navigation and bookmarks; project figures cite actual appendix sources.',
 'R05':'P2 explains geometry, photometry, interreflection, maintained illuminance, 0.16 m grid, Uo and directional UGR; native model view and p7 worked isolux.',
 'R06':'Quantitative 500-750 lx colour bar, iteration table, manufacturer polar plot and project-specific optical interpretation.',
 'R07':'Manufacturer 82 mm table/86 mm drawing discrepancy disclosed; larger envelope plus service clearance specified in report and CAD.',
 'R08':'Actual ProjectInfoPropertySet title corrected in new copies; all result streams preserved; reopened native PDFs verified.',
 'R09':'Unsupported assertion locating the automatic-plane minimum removed; fixed task and supplemental regional scopes explained.'}
rubric=[
 {'item':'DIALux key functions and procedure','weight_percent':20,'evidence':'Main p2; model view; native isolux p7; actual reopened appendix tables and directional UGR plots.'},
 {'item':'Luminaire/system selection and controls','weight_percent':20,'evidence':'Main p3 manufacturer optics, efficiency, colour, mounting; p4 iterations; p6 functional controls and clause comparison.'},
 {'item':'Summary comparison table','weight_percent':15,'evidence':'Main p5 selected EN/BEC lighting criteria/results; p6 control criteria/results; p1 explicit measured geometry and assumptions.'},
 {'item':'Coherent performance discussion','weight_percent':25,'evidence':'Main pp4,7 distinguish controlling desks, nominal/tolerance sensitivity, UGR, uniformity, maintenance, display scope and limitations.'},
 {'item':'Formal grid-aligned lighting layout','weight_percent':20,'evidence':'Combined p9 independent native AutoCAD A2 1:100 plot, 186 verified fixture IDs, ceiling grid, legend and product schedule.'}]
destination=root/'00_Submit/BSE3125_Lighting_Design_Report.pdf';shutil.copy2(review,destination);assert sha(destination)==sha(review)
record={'status':'accepted revised coursework artifact under stated model assumptions; no course-platform submission','review_date':'2026-11-16','final_pdf':str(destination),'sha256':sha(destination),'bytes':destination.stat().st_size,'main_pages_including_CAD':9,'total_pages':192,'all_192_assembled_pages_preserved_at_text_size_72_150dpi_pixels':True,'original_inputs':[{'path':str(p),'sha256':h} for p,h in inputs],'resolved_teacher_review_findings':review_notes,'rubric_evidence':rubric,'native_persistence':'05_Calculations/data/review-native-persistence-v4.json','native_projects':persistence['projects'],'shared_design_dataset':str(shared),'shared_design_sha256':sha(shared),'editable_report_source':str(folder/'report-content-v3.json'),'report_generator':'05_Calculations/scripts/build_review_report.py','native_cad':cad['dwg'],'native_cad_sha256':cad['dwg_sha256'],'visual_review':{'all_eight_narrative_pages':True,'A2_CAD_full_sheet':True,'appendix_guide':True,'representative_original_native_tables_and_plots':True,'notes':'Readable headings, captions and tables; no clipping or overlapping text. Original native pages preserve original typography.'},'remaining_scope_limits':['Specified rather than measured reflectances, glazing and furniture assumptions; recalculate on actual fit-out.','Analytical tolerance scenarios are not independent native scenario simulations.','DSE luminance is qualified sampled screening; complete angular conformity not established.','Installed controls and statutory applicability require project-specific commissioning/review.'],'no_submission_or_public_coursework_publication_performed':True}
out=folder/'assignment-acceptance-v3.json';out.write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k in ['status','final_pdf','sha256','bytes','main_pages_including_CAD','total_pages']},indent=2))
