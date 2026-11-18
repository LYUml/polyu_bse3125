# Open-plan Office Lighting Design

BSE3125: Optics and Lighting

Group 4

HUANG Celine 24034414D LUO Qianyu 24114977D LYU Mingliang 24099296D

RIOBA Ann Muniko 24114901D XIE Jingxuan 24110957D

## 1. Introduction and design basis

### 1.1 Design objective

This project considers the lighting of an open-plan office used for reading, paperwork and computer work. A maintained average illuminance of 500 lx is required on each desk, with a uniformity of at least 0.60 and a maximum UGR of 19 [1]. The aim is to provide enough light for these activities without large differences across the working area or excessive glare from the fittings.

### 1.2 Office geometry and proposed use

The office is L-shaped and extends around the central service core. The area enclosed by the traced internal wall boundaries is 1042.10 m2. Deducting the parts occupied by the eight columns gives 1032.57 m2. This differs from the 1022 m2 annotation on the drawing. The traced boundary defines the model and the 1042.10 m2 internal floor area used for BEC calculations.

The supplied drawing does not show office furniture, so 28 four-person bench groups have been arranged within the space. This gives 112 desks, each 1.6 by 0.8 m. Their positions provide a basis for checking the lighting where people would be working. The calculation assumes this furniture arrangement and would need to be reviewed if the desks were moved significantly.

### 1.3 Room conditions

Table 1 gives the main assumptions used in DIALux. The relatively light ceiling and walls contribute reflected light to the desks. Daylight is excluded because the window dimensions are not given. Section 7 considers changes to these conditions.

Table 1. Principal room and calculation assumptions.

| Parameter | Adopted value |
| --- | --- |
| Ceiling / desk / seated eye height | 2.8 / 0.8 / 1.2 m |
| Ceiling / wall / floor reflectance | 80 / 70 / 20% |
| Column reflectance / maintenance factor | 40% / 0.80 |
| Furniture and daylight | Proposed desks; no high partitions or simulated daylight |

## 2. DIALux modelling and simulation

### 2.1 Geometry and manufacturer photometry

The architectural drawing was imported into DIALux evo and checked against the 45 m overall dimension. The office boundary and eight full-height columns were modelled so that their obstruction of light is included.

The manufacturer ULD file provides the light distribution used in the calculation [2]. DIALux accounts for reflected light using the surface reflectances in Table 1. The fittings occupy complete 600 mm ceiling tiles, with their emitting faces approximately level with the 2.8 m ceiling. The native report lists the luminaire reference position at 2.868 m, 68 mm above the adopted ceiling plane. Figure 1 shows the model and evaluation heights.

Figure 1. Native room view (left) and adopted calculation heights (right).

### 2.2 Task-area calculation

Each 1.6 by 0.8 m desk has a 10 by 5 calculation grid at 0.8 m. Under EN 12464-1 clause 5.4, a 2:1 area uses its short side, so the maximum spacing is 0.2 x 5^log10(0.8) = 0.171 m [1]. The 0.16 m grid meets this limit. DIALux reports Uo as minimum divided by mean illuminance [3]. Checking desks individually exposes local shortfalls that a room mean would hide.

### 2.3 Maintenance factor and glare

A maintenance factor of 0.80 was applied to allow for the reduction in illumination during use [4]. Glare was calculated at a seated eye height of 1.2 m, with viewing directions at 15-degree intervals [5]. The manufacturer lists a catalogue UGR value for the fitting, but the glare experienced in the office also depends on its position and surroundings. The calculated room values are therefore used for the comparison with the UGR limit.

Further calculations were made for the 0.5 m bands around the bench groups, the remaining background floor, cylindrical illuminance at seated head height, and the exposed walls and ceiling. These use the same fittings and positions as the desk calculation. The desks are calculation surfaces; solid furniture, monitor screens and high partitions are not included. Separate copies were used for the output and reflectance comparisons, with all other inputs held constant.

## 2.4 Native DIALux documentation

The automatic whole-room plane reports 640 lx and Uo = 0.002 with a zero wall offset. This low uniformity rules out a claim of uniform task lighting everywhere. The adopted assessment covers the proposed desk positions, their surroundings and the accessible background. A revised seating plan requires a new desk assessment.

Figure 2. Desk-021 calculation grid and isolux contours. Native workstation report, page 529.

### Reading the local result

Each point samples the same horizontal task surface. With a mean of 593 lx and a minimum of 525 lx, Desk-021 has Uo = 525/593 = 0.89. Its low mean governs the illuminance margin. Desk-084 governs uniformity. This distinction would be lost in a room-wide average.

### Spacing and lumen-method checks

For a typical 2.4 m spacing and a nominal 2.0 m height above the desk plane, SHR is about 1.20. Local spacings vary at columns and edges. The desk grids directly check uniformity at those locations. Using N = E x A / (flux x UF x MF), 186 fittings would require UF = 0.875 to average 500 lx over the whole 1042.10 m2 at MF 0.80. This is a threshold calculation. The L-shaped room and the individual desk criteria are assessed with the native model.

## 3. Luminaire selection and lighting layout

### 3.1 Selected luminaire

The selected fitting is the Philips PowerBalance gen2 RC461B 40S/840, order code 910505103638. The design uses 186 fittings, each rated at 4000 lm and 23 W (174 lm/W). A colour temperature of 4000 K and a colour rendering index above 80 are appropriate for the office activities considered here [2]. The catalogue UGR 16 optic was also an important consideration because occupants will be using computer screens as well as reading printed material.

### 3.2 Ceiling coordination and light distribution

The 597 x 597 mm fitting occupies one 600 mm ceiling tile. Typical spacing is 2.4 m, with adjustments at columns and edges. The broad downward distributions in Figure 3 support overlap at desk height.

Figure 3. Ceiling layout (a) and principal light distributions from the manufacturer LDT (b) [2].

### 3.3 Output selection and installation

Table 2. Manufacturer ratings and modelled layout choices.

| Luminaire | Count | lm / W per fitting | Catalogue UGR | Connected kW* |
| --- | --- | --- | --- | --- |
| CoreLine [6] | 142 | 4300 / 32 | 19 | 4.54 |
| PowerBalance 34S [7] | 186 | 3400 / 20 | 16 | 3.72 |
| PowerBalance 40S [2] | 186 | 4000 / 23 | 16 | 4.28 |

*Luminaire input only. The CoreLine trial used the automatic working plane and a different layout. At the same 186 positions, 34S and 40S gave 504 lx and 593 lx as their lowest desk means, respectively.

Allow at least 86 mm for the fitting body, plus driver and maintenance clearance [2]. Drawing L01 on page 10 identifies each fitting and gives the luminaire schedule.

## 4. Simulation results and interpretation

### 4.1 Distribution of task illumination

All 112 desks meet the selected illuminance, uniformity and glare criteria. The lowest desk average is 593 lx, the lowest uniformity is 0.80 and the highest calculated UGR is 18.1. These values occur at different desks. Figure 4 shows the variation in desk-average illuminance across the office, with the three desks giving the limiting results identified.

Figure 4. Desk-average illuminance; A, B and C identify the three controlling desks.

### 4.2 Desks with the lowest lighting levels and highest glare

Desk-021 averages 593 lx at the south perimeter. Its centre is 2.40 m from the boundary; L140 and L136 are about 1.0 and 1.4 m away, bracketing the desk north to south. The perimeter limits additional coverage from rows farther south. L013 is about 7.7 m away.

Desk-084 has the lowest Uo (0.80), with a range of 521-736 lx around a 654 lx mean. L120 is only 0.36 m from the desk centre and sits toward one side of the desk. The native isolux plot shows a gradient across the task area, consistent with uneven overlap from the adjacent fittings.

At Desk-018 the highest directional UGR is 18.1 at 180 degrees (Appendix A, PDF p. 12, DIALux p. 316). Several luminaires are close to the observer, with L028 and L014 within 1.5 m in plan. The directional result reflects the combined effect of source luminance, apparent position and background luminance. The export gives the total, so individual source contributions remain unquantified.

Appendix A includes the native task contours and directional glare result. The automatic WP1 surface samples the wider room, including column footprints. The 112 explicit desk surfaces define the task-area check for the proposed furniture plan.

## 5. Comparison with lighting requirements

Table 3 compares the DIALux results with EN 12464-1:2021 and the lighting power limit in BEC 2024. The office activity and room assumptions are described in Section 1.

Table 3. Adopted requirements and calculated performance.

| Quantity | Requirement | Calculated result |
| --- | --- | --- |
| Desk mean | ≥500 lx | Lowest mean: 593 lx |
| Desk uniformity | Uo ≥0.60 | Lowest Uo: 0.80 |
| Directional glare | UGR ≤19 | Highest UGR: 18.1 |
| Colour rendering | Ra ≥80 | Ra >80 (manufacturer) |
| Seated cylindrical | ≥150 lx; Uo ≥0.10 | 224 lx; Uo ≥0.59* |
| Immediate surround | ≥300 lx; Uo ≥0.40 | 595 lx; Uo ≥0.64* |
| Background floor | ≥100 lx; Uo ≥0.10 | 617 lx; Uo =0.69 |
| Exposed walls | ≥150 lx; Uo ≥0.10 | 216 lx; Uo ≥0.24* |
| Exposed ceiling | ≥100 lx; Uo ≥0.10 | 137 lx; Uo =0.89 |
| Lighting power density | ≤7.2 W/m2 | 4.153 W/m2 including allowance |
| Manual control points | ≥32 for 1042.10 m2 | 32 proposed |
| Occupancy shutoff | ≤15 min | 10 min specified |
| Daylight response | Conditional on glazing and load | Pending glazing survey |

Sources: [1, Table 34, row 34.2 and clauses 5.3.4-5.3.5, 5.6.2]; [2] for colour rendering; [8, Tables 5.4-5.5 and clauses 5.6.1-5.6.2] for energy and controls. *Conservative uniformity bound across a group.

### 5.1 Illuminance and uniformity

The background floor receives 617 lx against a 100 lx target. The regular ceiling grid delivers more light than required in circulation. The four circulation zones allow reduced output to be tested against the background and nearby task criteria. Group uniformity bounds use the lowest point divided by the highest surface mean, rounded down.

### 5.2 Glare and screen reflections

The highest directional UGR is 18.1 in the baseline. The LDT check scales intensity to 4000 lm and divides by the projected area of the 510 x 510 mm aperture. The highest sampled luminance is 1334 cd/m2 (C44, gamma 65 degrees). EN clause 5.9.2 and Table 7 set 1500 cd/m2 for Case A medium-luminance screens (high state up to 200 cd/m2) tilted up to 15 degrees from vertical [1]. The check covers sampled angles from 65 to 89 degrees. Projection is undefined at 90 degrees. Confirm screen type, tilt and orientation at fit-out.

## 6. Lighting controls and energy use

### 6.1 Local and automatic control

The office has 32 independent control zones: 28 for bench groups and four for circulation. Each has local manual switching and dimming. The largest zone is 46.67 m2, below the 250 m2 automatic-control limit. The 1042.10 m2 office requires 32 manual control points under BEC Table 5.5 without claiming a reduction for low power density [8]. Figure 5 shows their boundaries.

Each zone switches off after 10 minutes without occupancy, within the BEC limit of 15 minutes. A schedule switches lighting off outside working hours, with local overrides limited to 120 minutes. Commissioning must confirm at least 50% power reduction, including sensor and driver standby consumption [8, Sec. 5.6.1].

Figure 5. Proposed independent lighting control zones.

### 6.2 Daylight response

Daylight-responsive control is proposed where the actual external glazing and lighting load trigger BEC clause 5.6.2 [8]. The window dimensions and grouping are needed to define these zones and check the exceptions. Where applicable, the controller must be able to reduce lighting power to 50% or less, or switch off, in response to daylight.

### 6.3 Connected power

The fittings draw 186 x 23 = 4278 W. With a provisional 50 W allowance for sensors and shared control equipment, the design load is 4328 W, or 4.153 W/m2 over 1042.10 m2. The BEC limit is 7.2 W/m2. A full-load scenario of 2500 h/year gives approximately 10.82 MWh/year. A controlled estimate requires logged occupancy, driver power at dimmed output and standby loads.

## 7. Design comparison and conclusion

### 7.1 Comparison of calculation conditions

DIALux tested 90% output, lower ceiling/wall/floor reflectances (70/50/20%), and both together. The layout and MF were retained. Table 4 shows the workstation results.

Table 4. Workstation results by calculation condition.

| Case | Lowest desk mean | Lowest Uo | Highest UGR |
| --- | --- | --- | --- |
| Requirement | ≥500 lx | ≥0.60 | ≤19 |
| Baseline | 593 lx | 0.80 | 18.1 |
| 90% output | 534 lx | 0.80 | 17.7 |
| Lower reflectance | 566 lx | 0.79 | 18.6 |
| Combined | 509 lx | 0.79 | 18.2 |

### 7.2 Design choice

At 90% output, the lowest desk mean is 534 lx, 6.8% above the target. The worst directional UGR falls from 18.1 to 17.7. Lower reflectance at full output reduces the minimum desk mean to 566 lx while the UGR rises to 18.6, leaving 0.4 below the limit.

With both changes, the lowest desk mean is 509 lx and maximum directional UGR is 18.2. The 9 lx illuminance margin supports keeping full output as the design setting and tuning the installed system after completion.

### 7.3 Maintenance and conclusion

The maintenance factor uses LLMF x LSF x LMF x RSMF = 0.90 x 1.00 x 0.95 x 0.94 = 0.8037, rounded down to 0.80 [4]. The product declares L90 at 50,000 h [2]. The remaining factors assume prompt replacement, annual cleaning and retained room finishes.

Full output remains the design setting. The 593 lx minimum maintained desk mean is 19% above 500 lx and corresponds to about 741 lx initially under the adopted MF. Local dimming can be commissioned against the installed finishes, desks and screens. Actual dimmed power should be verified separately.

## References

[1] Light and lighting - Lighting of work places - Part 1: Indoor work places, BS EN 12464-1:2021, British Standards Institution, London, U.K., 2021, doi: 10.3403/30385601. https://doi.org/10.3403/30385601

[2] Signify, "Philips PowerBalance gen2, RC461B 40S/840 SEIA W60L60 VPC U4 WH SC UE," product 910505103638. Accessed: Nov. 16, 2026. [Online]. Available: https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-powerbalance-gen2/910505103638_EU/product

[3] DIAL GmbH, "Parameters of a calculation object," Knowledge Base DIALux evo, Sep. 19, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000075351-parameters-of-a-calculation-object

[4] DIAL GmbH, "Maintenance factors," Knowledge Base DIALux evo, Feb. 17, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000122341-maintenance-factors

[5] DIAL GmbH, "UGR method - Unified Glare Rating," Knowledge Base DIALux evo, May 21, 2026. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000073310-ugr-method-unified-glare-rating

[6] Signify, "Philips CoreLine Panel gen6, RC132V G6 43S/840, product 910505102802." Accessed: Nov. 18, 2026. [Online]. Available: https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-coreline-panel-gen6/910505102802_EU/product

[7] Signify, "Philips PowerBalance gen2, RC461B 34S/840, product 910505103630." Accessed: Nov. 18, 2026. [Online]. Available: https://www.signify.com/api/assets/v1/file/Signify/content/910505103630_EU.en_AA.PROF.FP/Localized_commercial_leaflet_910505103630_en_AA.pdf

[8] Electrical and Mechanical Services Department, Code of Practice for Energy Efficiency of Building Services Installation, 2024 ed. Hong Kong: Government of the Hong Kong Special Administrative Region, 2024, sec. 5, pp. 16-21. Accessed: Nov. 16, 2026. [Online]. Available: https://www.emsd.gov.hk/beeo/en/pee/BEC_2024_ENG.pdf
