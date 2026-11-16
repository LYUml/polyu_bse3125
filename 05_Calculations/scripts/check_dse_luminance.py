"""Bounded flat-aperture luminance check using original manufacturer EULUMDAT.

Follows the Lighting Analysts/DIAL EULUMDAT field layout. Not a room simulation.
"""
from pathlib import Path
import math,json,hashlib,sys
root=Path(__file__).resolve().parents[2];code=sys.argv[1] if len(sys.argv)>1 else '910505103630';nominal_flux=float(sys.argv[2]) if len(sys.argv)>2 else 3400
source=root/'02_References/Manufacturer'/f'{code}.ldt'
rows=source.read_text().splitlines();assert int(rows[2])==4 and int(rows[25])==1
mc,ng=int(rows[3]),int(rows[5]);assert mc==180 and ng==91
assert [float(x) for x in rows[17:21]]==[0.,0.,0.,0.],'Only the supplied flat aperture supported'
length,width=float(rows[15])/1000,float(rows[16])/1000;assert length==width==.510
lamp_flux=float(rows[28]);conversion=float(rows[23]);assert conversion==1.0
start=32+10
angles_c=list(map(float,rows[start:start+mc]));start+=mc
angles_g=list(map(float,rows[start:start+ng]));start+=ng
intensity=list(map(float,rows[start:]));stored_planes=mc//4+1;assert len(intensity)==stored_planes*ng
assert angles_c[:stored_planes]==[2.*i for i in range(stored_planes)] and angles_g==[float(i) for i in range(91)]
samples=[]
for ci in range(stored_planes):
 for gi,gamma in enumerate(angles_g):
  if not 65<=gamma<90:continue
  # Native ULD reports 3400 lm vs 3399 lm in LDT; use the larger flux.
  candela=intensity[ci*ng+gi]*nominal_flux/1000
  projected_area=length*width*math.cos(math.radians(gamma))
  samples.append({'C_deg':angles_c[ci],'gamma_deg':gamma,'intensity_cd_klm':intensity[ci*ng+gi],'luminance_cd_m2':candela/projected_area})
horizontal_intensity_max=max(intensity[ci*ng+90] for ci in range(stored_planes))
worst=max(samples,key=lambda s:s['luminance_cd_m2'])
out=Path(sys.argv[3]) if len(sys.argv)>3 else root/'05_Calculations/data/dse-luminance-check-v1.json';assert not out.exists()
record={'status':'bounded analytic check of sampled manufacturer high-angle average luminance','manufacturer_order_code':code,'nominal_flux_lm':nominal_flux,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_format':'EULUMDAT quadrant symmetry, flat 510 x 510 mm emitting aperture, cd/klm intensities','format_reference':'https://www.agi32.com/Downloads/TechnicalDocs/Thinking%20Photometrically%20II.pdf Appendix B; manufacturer-authored file','equation':f'L=I_normalized*({nominal_flux:g}/1000)/(0.510*0.510*cos(gamma))','angular_sampling':'C=0..90 by 2 degrees, gamma=65..89 by 1 degree; quadrant symmetry extends remaining azimuths. No between-sample maxima claim.','horizontal_90deg_intensity_max_cd_klm':horizontal_intensity_max,'horizontal_endpoint_limitation':'Declared flat aperture has zero projected area at 90 degrees while measured file intensities are slightly nonzero. No finite luminance or complete 65..90-degree conformity claim is inferred for this endpoint.','worst_sample':worst,'plus_10pct_flux_luminance_cd_m2':worst['luminance_cd_m2']*1.1,'DSE_design_basis':'EN 12464-1:2021 5.9.2 Table 7 Case A, positive-polarity ordinary office screens. Adopt 1500 cd/m2 for medium-luminance screens; screens vertical or tilted <=15 degrees. Matte worktops and screen orientation still required to reduce reflections.','adopted_limit_cd_m2':1500,'sampled_data_pass':worst['luminance_cd_m2']<=1500,'scope':'Independent sampled photometric check, not measured luminaire luminance or a substitute for room UGR calculation. Native UGR remains separately verified.'}
out.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
