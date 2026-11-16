"""Validate and promote the reviewed presentation revision without recalculating design."""
from pathlib import Path
import json,hashlib,sys,re,shutil
import pdfplumber,pypdfium2 as pdfium,ezdxf
from ezdxf.lldxf.tagwriter import TagCollector
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r.parent/'dialux-agent-toolkit'))
from src.cad import _fixture_records
f=r/'05_Calculations/Final_v04';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=load(f/'assembly-manifest.json');new=r/manifest['pdf'];old=r/'05_Calculations/local/report-before-figure-revision.pdf'
assert sha(new)==manifest['sha256'] and manifest['total_pages']==20 and manifest['main_including_CAD']==9 and new.stat().st_size<10000000
assert sha(old)=='b9c3c35d2f94aad171bca81934440754221552adc8b4f044c3225cb1b52425ec'
for name,h in load(r/'05_Calculations/data/comparison-plan-v1.json')['original_inputs'].items():assert sha(r/name)==h
binding=load(r/'05_Calculations/data/final-design-v4.json')
for item in binding['bindings'].values():assert sha(r/item['path'])==item['sha256']
source=r/'05_Calculations/Final_v03/BSE3125-L01-lighting-plan-v5.dxf';cad=f/'BSE3125-L01-lighting-plan-v7.dxf'
assert _fixture_records(source)==_fixture_records(cad)
a=ezdxf.readfile(source);b=ezdxf.readfile(cad);unchanged_entities=0
for e in a.modelspace():
 if e.dxf.layer in ['SCHEDULE','PLAN_NOTES','SHEET']:continue
 other=b.entitydb[e.dxf.handle];assert TagCollector.dxftags(e)==TagCollector.dxftags(other);unchanged_entities+=1
native=load(f/'cad-native-v7/manifest.json');plot=load(f/'cad-plot-v7/manifest.json')
assert native['native_reopen_verified'] and native['fixture_count']==186 and native['dimension_count']==5
assert sha(Path(native['dwg']))==native['dwg_sha256'] and sha(Path(plot['pdf']))==plot['pdf_sha256']
assert plot['physical_scale']['verified'] and plot['all_fixture_labels_verified']
with pdfplumber.open(new) as p:
 texts=[x.extract_text() or '' for x in p.pages];body='\n'.join(texts[:8]);assert 'PolyU' not in body
 assert all('TimesNewRoman' in ch['fontname'] for pg in p.pages[:8] for ch in pg.chars)
 for pg in p.pages[:8]:assert all(60<=ch['x0'] and ch['x1']<=pg.width-50 for ch in pg.chars)
 for i in range(1,6):assert f'Figure {i}.' in body
 for i in range(1,4):assert f'Table {i}.' in body
 assert 'Mean (lx)' in texts[14] and 'Uo bound' in texts[14]
 for z in range(1,33):assert f'Z{z:02}' in texts[5]
 for val in ['593','534','566','18.1','17.7','18.6','4328','4.235']:assert val in body
 group=load(r/'05_Calculations/local/group-details.json')
 for m in group['members']:assert m['name'] in texts[0] and m['student_id'] in texts[0]
 refs=[int(n) for n in re.findall(r'\[(\d+)(?:\]|,)', '\n'.join(texts[:7]))];assert list(dict.fromkeys(refs))==list(range(1,7))
 a=pdfium.PdfDocument(old);b=pdfium.PdfDocument(new)
 for i in [0,7,9,10,11,12,13,15,16,17,18,19]:assert a[i].render(scale=1).to_pil().tobytes()==b[i].render(scale=1).to_pil().tobytes()
 a.close();b.close()
source_ldt=r/'02_References/Manufacturer/910505103638.ldt';rows=source_ldt.read_text().splitlines();assert float(rows[23])==1 and int(rows[2])==4
vals=list(map(float,rows[42+180+91:]));assert len(vals)==46*91
record={'status':'accepted after visual review and data checks','pdf_sha256':sha(new),'bytes':new.stat().st_size,'main_pages_including_CAD':9,'total_pages':20,'original_inputs_unchanged':True,'all_five_shared_dataset_bindings_unchanged':True,'all_186_CAD_fixture_records_identical':True,'unchanged_CAD_geometry_entity_count':unchanged_entities,'native_CAD_saved_reopened_verified':True,'native_CAD':native['dwg'],'native_CAD_sha256':native['dwg_sha256'],'CAD_plot':plot['pdf'],'CAD_plot_sha256':plot['pdf_sha256'],'CAD_plot_1_to_100_verified':True,'figure_data_sources':{'2':'Shared room/furniture/fixture datasets; original manufacturer EULUMDAT C0 and C90 planes, cd/klm','3':'112 reopened native desk means; markers identify controlling desks','4':'Desk-021,084,018 values read directly from reopened native task JSON','5':'All 32 unchanged shared control-zone polygons; representative-point labels'},'manufacturer_LDT_sha256':sha(source_ldt),'C0_91_samples_cd_per_klm':vals[:91],'C90_91_samples_cd_per_klm':vals[45*91:46*91],'all_ten_original_native_appendix_pages_unchanged':True,'visual_review':{'pages':[2,3,4,5,6,7,9,15],'pages_1_and_8_pixel_identical_to_previous_reviewed_final':True,'findings':['Readable unscaled vector labels','Clear curve axes and legend','Distinct critical-desk markers and zero-based illuminance bars','Every control zone labelled','Criteria sources moved to table note','Auxiliary illuminance and uniformity in separate rows','Native CAD schedule and dimension chain readable','No clipping or overlaps observed']}}
(f/'figure-layout-review.json').write_text(json.dumps(record,indent=2))
plot.update(status='Accepted native A2 1:100 plot after visual review',visual_review_verified=True);(f/'cad-plot-v7/manifest.json').write_text(json.dumps(plot,indent=2))
target=r/'00_Submit/BSE3125_Lighting_Design_Report.pdf';assert sha(target)==sha(old);shutil.copy2(new,target)
accept=load(f/'assignment-acceptance-v4.json');accept.update(sha256=sha(new),bytes=new.stat().st_size,report_source_sha256=sha(f/'content.json'),baseline_design_and_CAD_unchanged=False,baseline_engineering_geometry_and_results_unchanged=True,CAD_presentation_revised=True,presentation_acceptance='05_Calculations/Final_v04/figure-layout-review.json',current_CAD='05_Calculations/Final_v04/cad-native-v7/layout.dwg')
accept['rubric_coverage']['lighting_layout_20']='Revised independent A2 CAD P04, ceiling grid, tabulated schedule, legend, dimension chain and 186 unchanged matching fixtures'
# Prior revision checks are historical, not claims about the current CAD or plots.
for key in ['name_layout_revision','title_reference_revision']:
 if key in accept:accept[key]['scope']='Historical revision; current presentation checks are in figure-layout-review.json'
(f/'assignment-acceptance-v4.json').write_text(json.dumps(accept,indent=2))
visual={'accepted':True,'pdf_sha256':sha(new),'review_date':'2026-11-16','review_record':'05_Calculations/Final_v04/figure-layout-review.json','method':'Changed pages reviewed as rendered; unchanged native appendices and pages 1/8 verified pixel-identical to reviewed prior final. Assembly checks all source pages at 72/150 dpi.','main_pages_including_CAD':9,'total_pages':20};(f/'visual-review.json').write_text(json.dumps(visual,indent=2))
binding.update(final_pdf_sha256=sha(new),report_source_sha256=sha(f/'content.json'),current_CAD={'native':'05_Calculations/Final_v04/cad-native-v7/layout.dwg','native_sha256':native['dwg_sha256'],'plot':'05_Calculations/Final_v04/cad-plot-v7/BSE3125-L01-lighting-plan.pdf','plot_sha256':plot['pdf_sha256']});(r/'05_Calculations/data/final-design-v4.json').write_text(json.dumps(binding,indent=2))
fmt=load(f/'format-specification.json');fmt.update(status='accepted; revised figures, tables and CAD reviewed',figure_label_font_pt_range=[8,10]);(f/'format-specification.json').write_text(json.dumps(fmt,indent=2))
print(json.dumps({k:v for k,v in record.items() if k not in ['C0_91_samples_cd_per_klm','C90_91_samples_cd_per_klm','visual_review','figure_data_sources']},indent=2))
