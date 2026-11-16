# Open-plan Office Lighting Design

BSE3125: Optics and Lighting

Group 4

HUANG Celine 24034414D       LUO Qianyu 24114977D       LYU Mingliang 24099296D

RIOBA Ann Muniko 24114901D       XIE Jingxuan 24110957D

## 1. Introduction and design basis

### 1.1 Design objective

This project considers the lighting of an open-plan office used for reading, paperwork and computer work. A maintained average illuminance of 500 lx is required on each desk, with a uniformity of at least 0.60 and a maximum UGR of 19 [1]. The aim is to provide enough light for these activities without large differences across the working area or excessive glare from the fittings.

### 1.2 Office geometry and proposed use

The office is L-shaped and extends around the central service core. The area enclosed by the traced internal wall boundaries is 1042.10 m^2. Deducting the parts occupied by the eight columns gives 1032.57 m^2. This differs from the 1022 m^2 annotation on the drawing. The traced boundary is used to construct the model, while the smaller annotated area is used for the power density calculation, giving a slightly higher and more conservative value.

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

The manufacturer ULD file provides the light distribution used in the calculation [2]. DIALux accounts for reflected light using the surface reflectances in Table 1. The fittings occupy complete 600 mm ceiling tiles, with their emitting faces approximately level with the 2.8 m ceiling. Figure 1 shows the model and evaluation heights.

*Figure 1. Native room view (left) and adopted calculation heights (right).*

### 2.2 Task-area calculation

A calculation surface was placed on each desk at 0.8 m above the floor. Each surface measures 1.6 by 0.8 m and uses a 10 by 5 grid, giving a nominal spacing of 0.16 m. The selected calculation parameters follow the DIALux definitions [3]. Uniformity is calculated by dividing the minimum illuminance by the average illuminance on that surface. Checking individual desks is useful because a satisfactory average for the whole room could still leave some workstations poorly lit.

### 2.3 Maintenance factor and glare

A maintenance factor of 0.80 was applied to allow for the reduction in illumination during use [4]. Glare was calculated at a seated eye height of 1.2 m, with viewing directions at 15-degree intervals [5]. The manufacturer lists a catalogue UGR value for the fitting, but the glare experienced in the office also depends on its position and surroundings. The calculated room values are therefore used for the comparison with the UGR limit.

Further calculations were made for the 0.5 m bands around the bench groups, the remaining background floor, cylindrical illuminance at seated head height, and the exposed walls and ceiling. These use the same fittings and positions as the desk calculation. The desks are calculation surfaces; solid furniture, monitor screens and high partitions are not included. Separate copies were used for the output and reflectance comparisons, with all other inputs held constant.

## 3. Luminaire selection and lighting layout

### 3.1 Selected luminaire

The selected fitting is the Philips PowerBalance gen2 RC461B 40S/840, order code 910505103638. The design uses 186 fittings, each rated at 4000 lm and 23 W. A colour temperature of 4000 K and a colour rendering index above 80 are appropriate for the office activities considered here [2]. The low-glare optic was also an important consideration because occupants will be using computer screens as well as reading printed material.

### 3.2 Ceiling coordination and light distribution

The 597 by 597 mm fitting fits within a 600 mm ceiling tile. Following the grid avoids fittings crossing tile joints. Spacing is generally about 2.4 m, with adjustments near columns and room edges. Figure 2 shows the layout and the two principal photometric planes. Their similar downward distributions support overlapping light at desk height. The curves help explain the choice of optic; the actual spacing and glare are assessed using the room calculation.

*Figure 2. Ceiling layout (a) and principal light distributions from the manufacturer LDT (b) [2].*

### 3.3 Output selection and installation

An earlier arrangement using the 3400 lm PowerBalance fitting gave a minimum desk average of 504 lx. Although this exceeded 500 lx, the margin was small. The 4000 lm version at the same positions increased the minimum to 593 lx, while the maximum calculated UGR remained below 19. Section 7 compares this design with a reduced-output scene and a separate change in room reflectance.

The ceiling void must accommodate the fitting, driver and maintenance access. The manufacturer gives a height of 82 mm in the specification table and 86 mm on the dimension drawing, so at least the larger dimension should be allowed, with additional service clearance. The lighting layout on page 9 includes the ceiling grid, fitting numbers, legend and luminaire schedule.

## 4. Simulation results and interpretation

### 4.1 Distribution of task illumination

All 112 desks meet the selected illuminance, uniformity and glare criteria. The lowest desk average is 593 lx, the lowest uniformity is 0.80 and the highest calculated UGR is 18.1. These values occur at different desks. Figure 3 shows the variation in desk-average illuminance across the office, with the three desks giving the limiting results identified.

*Figure 3. Desk-average illuminance; A, B and C identify the three controlling desks.*

### 4.2 Desks with the lowest lighting levels and highest glare

Desk-021 has the lowest average illuminance: 593 lx, with a minimum of 525 lx, giving Uo = 525/593 = 0.89. Desk-084 has the lowest uniformity, at 0.80. Desk-018 gives the highest UGR when looking in the 180-degree direction. Figure 4 compares these three desks. The original isolux and glare outputs are retained in Appendix A.

*Figure 4. Different desks control mean illuminance, uniformity and glare.*

## 5. Comparison with lighting requirements

Table 2 compares the DIALux results with EN 12464-1:2021 and the lighting power limit in BEC 2024. The office activity and room assumptions are described in Section 1.

Table 2. Adopted requirements and calculated performance.

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
| Lighting power density | ≤7.2 W/m^2 | 4.235 W/m^2 |

Sources: [1, Table 34 and Secs. 5.3.4-5.3.5, 5.6.2]; [2] for colour rendering; [6, Table 5.4] for power density. Illuminance results are the lowest surface means. *Conservative uniformity bound across a group of surfaces.

### 5.1 Illuminance and uniformity

The desks meet the average illuminance and uniformity targets. The surrounding and background areas also meet their lower illuminance requirements, so the change in lighting level outside the desks is considered as well. Walls and ceiling are checked because their brightness affects the appearance of the room. For groups of calculation surfaces, the uniformity bound in Table 2 is the lowest point illuminance divided by the highest surface average, rounded down. This gives a conservative value for the group.

### 5.2 Glare and colour rendering

The maximum calculated UGR is below 19 for the seated positions and viewing directions tested. Colour rendering is taken from the manufacturer data. These results apply to the office tasks and arrangement described here; a different activity, such as unusually fine or low-contrast work, could require a higher lighting level.

## 6. Lighting controls and energy use

### 6.1 Local and automatic control

The office has 32 independent control zones: 28 for bench groups and four for circulation. Each has local manual switching and dimming. The largest zone is 46.67 m^2, below the 250 m^2 automatic-control limit. The number of manual points follows BEC Table 5.5 without claiming a reduction for low power density [6]. Figure 5 shows their boundaries.

Each zone switches off after 10 minutes without occupancy, within the BEC limit of 15 minutes. A schedule switches lighting off outside working hours, with local overrides limited to 120 minutes. Commissioning must confirm at least 50% power reduction, including sensor and driver standby consumption [6, Sec. 5.6.1].

*Figure 5. Proposed independent lighting control zones.*

### 6.2 Daylight response

Provide daylight dimming where the glazing arrangement triggers BEC clause 5.6.2. The sensor reduces electric light while maintaining desk illumination. Window dimensions are unavailable, so daylight is excluded from the simulation and no annual saving is claimed.

### 6.3 Connected power

The fittings draw 186 x 23 = 4278 W. Including a 50 W control allowance gives 4328 W, or 4328/1022 = 4.235 W/m^2 using the smaller annotated area. This is below the BEC limit of 7.2 W/m^2. Occupancy control and scheduling reduce operating time; actual energy use depends on working hours and occupancy.

## 7. Design comparison and conclusion

### 7.1 Comparison of calculation conditions

Two further DIALux calculations were made with the same layout and maintenance factor. One reduced all luminaire outputs to 90%. The other retained full output and changed ceiling/wall/floor reflectances from 80/70/20% to 70/50/20%. Table 3 shows the workstation results; Appendix C gives the auxiliary results and selected outputs.

Table 3. Workstation results for the three calculation conditions.

| Case | Lowest desk mean | Lowest Uo | Highest UGR |
| --- | --- | --- | --- |
| Requirement | ≥500 lx | ≥0.60 | ≤19 |
| Baseline | 593 lx | 0.80 | 18.1 |
| 90% output | 534 lx | 0.80 | 17.7 |
| Lower reflectance | 566 lx | 0.79 | 18.6 |

### 7.2 Design choice

At 90% output, the lowest desk average falls to 534 lx, only 6.8% above the requirement. Uniformity remains 0.80 and the maximum UGR falls to 17.7. This supports using dimming during commissioning, but full output is retained as the design condition to provide more allowance for differences between the assumed and actual office.

With the lower reflectances, the lowest desk average is 566 lx and the highest UGR rises to 18.6. Less light is reflected towards the desks, while a darker background can increase the contrast with the luminaires. The desk criteria are still met, although the glare margin is smaller. These are separate tests, so their results do not establish performance when both changes occur together. Both cases also meet the auxiliary criteria in Appendix C.

### 7.3 Maintenance and conclusion

The maintenance factor is based on 0.90 x 1.00 x 0.95 x 0.94 = 0.8037, rounded down to 0.80 [4]. The first factor follows the manufacturer L90 declaration [2]; the others are assumptions. Annual cleaning and prompt replacement of failed fittings are proposed. Screen reflections should be checked after fit-out, since room UGR does not assess reflected images of fittings on displays [1, Sec. 5.9].

The full-output arrangement is retained, with local dimming available after the finishes and workstation positions are confirmed. Lighting power density remains 4.235 W/m^2; a 10% reduction in light output does not establish a 10% reduction in electrical power. Screens and controls should be checked during commissioning.

## References

[1] Light and lighting - Lighting of work places - Part 1: Indoor work places, BS EN 12464-1:2021, British Standards Institution, London, U.K., 2021, doi: 10.3403/30385601.

[2] Signify, "Philips PowerBalance gen2, RC461B 40S/840 SEIA W60L60 VPC U4 WH SC UE," product 910505103638. Accessed: Nov. 16, 2026. [Online]. Available: https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-powerbalance-gen2/ 910505103638_EU/product

[3] DIAL GmbH, "Parameters of a calculation object," Knowledge Base DIALux evo, Sep. 19, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000075351-parameters-of-a-calculation -object

[4] DIAL GmbH, "Maintenance factors," Knowledge Base DIALux evo, Feb. 17, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000122341-maintenance-factors

[5] DIAL GmbH, "UGR method - Unified Glare Rating," Knowledge Base DIALux evo, May 21, 2026. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000073310-ugr-method-unified-glare -rating

[6] Electrical and Mechanical Services Department, Code of Practice for Energy Efficiency of Building Services Installation, 2024 ed. Hong Kong: Government of the Hong Kong Special Administrative Region, 2024, sec. 5, pp. 16-21. Accessed: Nov. 16, 2026. [Online]. Available: https://www.emsd.gov.hk/beeo/en/pee/BEC_2024_ENG.pdf
