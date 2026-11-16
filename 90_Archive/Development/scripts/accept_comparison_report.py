"""Final coursework checks and local promotion after a recorded visual review."""
from pathlib import Path
import json,hashlib,sys,re,shutil
import pypdfium2 as pdfium
import pdfplumber
r=Path(__file__).resolve().parents[2];d=r/'05_Calculations/data';f=r/'05_Calculations/Final_v04'
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=load(f/'assembly-manifest.json');pdf=r/manifest['pdf'];assert sha(pdf)==manifest['sha256']
assert manifest['main_including_CAD']==9 and manifest['total_pages']==20 and pdf.stat().st_size<10000000
assert manifest['all_pages_preserve_source_text_dimensions_and_72_150dpi_pixels']
visual=load(f/'visual-review.json');assert visual['pdf_sha256']==sha(pdf) and visual['accepted']
plan=load(d/'comparison-plan-v1.json')
for path,h in plan['original_inputs'].items():assert sha(r/path)==h
binding=load(d/'final-design-v3.json')
for item in binding['bindings'].values():assert sha(r/item['path'])==item['sha256']
assert sha(r/'05_Calculations/Final_v03/cad-native-v5/layout.dwg')=='719501e0e81919cd5671f2056ff4be4009eeb5658354b85d3067ec2e2b207252'
assert sha(r/'05_Calculations/Final_v03/cad-plot-v5/BSE3125-L01-lighting-plan.pdf')=='14716ab93e661d495752f76aa6c8d2fb07477e46c3e3efc93939bcf5d5c7bf88'
persistence=[]
for stem,version in [('output90-core',2),('reflectance-core',2),('output90-aux',3),('reflectance-aux',2)]:
    p=load(d/f'comparison-{stem}-persistence-v{version}.json');assert p['status']=='verified' and sha(Path(p['native_path']))==p['native_sha256']
    assert p['exact_preserved_rows']==(112 if stem.endswith('core') else 288)
    for key in ['fresh_result_file','reopened_result_file']:
        result=load(r/p[key]);assert sha(Path(result['pdf']))==result['pdf_sha256']
    persistence.append(p)
summary=load(f/'comparison-summary.json');assert all(c['all_selected_metrics_pass'] for c in summary['cases'])
assert [c['minimum_task_average_lx'] for c in summary['cases']]==[593,534,566]
assert [c['maximum_directional_ugr'] for c in summary['cases']]==[18.1,17.7,18.6]
# Reject ineffective dimming evidence even if its original parser marked full-output values passing.
b=summary['cases'][0];dim=summary['cases'][1]
assert dim['combined_seated_cylindrical']['minimum_surface_average_lx']<b['combined_seated_cylindrical']['minimum_surface_average_lx']
with pdfplumber.open(pdf) as document:
    main_text='\n'.join(p.extract_text() or '' for p in document.pages[:8])
    fonts={c['fontname'] for p in document.pages[:8] for c in p.chars}
    assert all('TimesNewRoman' in font for font in fonts),fonts
group=load(r/'05_Calculations/local/group-details.json');assert group['group']=='Group 4' and len(group['members'])==5
normalized=re.sub(r'\s+','',main_text)
for member in group['members']:
    assert re.sub(r'\s+','',member['name']) in normalized and member['student_id'] in normalized
for forbidden in ['For review','Report draft','native results; no interpolation']:
    assert forbidden.lower() not in main_text.lower()
for value in ['593','534','566','17.7','18.6','4.235','4328','0.8037','Appendix C']:
    assert value in main_text,value
target=r/'00_Submit/BSE3125_Lighting_Design_Report.pdf'
archive=r/'05_Calculations/Archive/2026-11-16_Pre_Comparisons/BSE3125_Lighting_Design_Report.pdf'
assert sha(target)=='160c3bb9cf17e3c8691913287ba4a4a0b8d0aa2faf647ab32ba3fd2cbc2ce9b0'
archive.parent.mkdir(parents=True,exist_ok=True)
if archive.exists():assert sha(archive)==sha(target)
else:shutil.copy2(target,archive)
shutil.copy2(pdf,target);assert sha(target)==sha(pdf)
record={'status':'Accepted academic deliverable under declared assumptions','final_pdf':str(target.relative_to(r)),'sha256':sha(target),'bytes':target.stat().st_size,'main_pages_including_CAD':9,'appendix_pages':11,'total_pages':20,'group_member_count_verified':5,'personal_metadata_in_local_files_only':True,'font_names_used_in_main':sorted(fonts),'original_inputs_unchanged':True,'baseline_design_and_CAD_unchanged':True,'all_four_native_comparison_projects_saved_reopened_verified':True,'native_persistence':persistence,'report_source_sha256':sha(f/'content.json'),'assembly_manifest':'05_Calculations/Final_v04/assembly-manifest.json','visual_review':'05_Calculations/Final_v04/visual-review.json','rubric_coverage':{'DIALux_functions_20':'Section2 and model/isolux figures; controlled calculation comparisons','luminaire_system_selection_20':'Sections3,6,7; output selection and control explanation','criteria_summary_15':'Tables1,2,3,C1; explicit assumptions','performance_discussion_25':'Sections4,5,7 and AppendixC; actual independent sensitivity results','lighting_layout_20':'Unchanged independent A2 CAD, ceiling grid,legend,schedule and186matchingfixtures'},'limitations':['Two independent scenarios, not combined lower-output and lower-reflectance test','No measured dimming power curve or annual savings claimed','Furniture, facade and commissioning assumptions retained; not statutory or installed-system certification'],'archive':str(archive.relative_to(r)),'course_platform_submission':False}
(f/'assignment-acceptance-v4.json').write_text(json.dumps(record,indent=2))
binding.update(status='Accepted baseline design with native comparison studies and concise final report',acceptance='05_Calculations/Final_v04/assignment-acceptance-v4.json',revised_acceptance='05_Calculations/Final_v04/assignment-acceptance-v4.json',report_source_sha256=sha(f/'content.json'),final_pdf_sha256=sha(target),comparison_summary='05_Calculations/Final_v04/comparison-summary.json')
(d/'final-design-v4.json').write_text(json.dumps(binding,indent=2));print(json.dumps({k:v for k,v in record.items() if k not in ['native_persistence','rubric_coverage']},indent=2))
