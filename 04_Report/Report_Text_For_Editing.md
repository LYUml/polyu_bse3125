# Open-plan Office Lighting Design

BSE3125: Optics and Lighting

Group 4

HUANG Celine 24034414D LUO Qianyu 24114977D LYU Mingliang 24099296D

RIOBA Ann Muniko 24114901D XIE Jingxuan 24110957D

## 1. Introduction and design basis

### 1.1 Design objective

This project addresses the lighting needs of an open-plan office used for reading, paperwork, and computer work. To support these tasks, a maintained average illuminance of 500 lx is required on each desk, with a uniformity of at least 0.60 and a maximum UGR of 19 [1]. Ultimately, the aim is to provide enough light for these activities without large differences across the working area while reducing excessive glare from the fittings.

### 1.2 Office geometry and proposed use

The L-shaped office wraps around the central service core. For the BEC lighting power density calculation, the internal floor area of 1042.10 m² is measured to the inner faces of the enclosing walls and includes the column footprints [2]. 

Within this layout, the office space is arranged with 28 four-person bench groups, totalling 112 desks, each 1.6 by 0.8 m. Their positions serve as reference points for evaluating lighting across the workplace. Accordingly, the calculations below assume a fixed furniture arrangement, meaning a revision would be necessary if the desks are moved significantly.

### 1.3 Room conditions

Table 1 indicates the key assumptions implemented in DIALux. The relatively light ceiling and walls contribute reflected light onto the desks, whereas daylight is excluded because the window dimensions are not taken into account. Section 7 further evaluates the impact of changing these conditions.

Table 1. Principal room and calculation assumptions.

| Parameter | Adopted value |
| --- | --- |
| Ceiling / desk / seated eye height | 2.8 / 0.8 / 1.2 m |
| Ceiling / wall / floor reflectance | 80 / 70 / 20% |
| Column reflectance / maintenance factor | 40% / 0.80 |
| Furniture and daylight | Proposed desks; no high partitions or simulated daylight |

## 2. DIALux modelling and simulation

### 2.1 Geometry and manufacturer photometry

The architectural drawing imported into DIALux evo was verified against the 45 m overall dimension to reduce scale mismatches. Following this, to account for light obstruction, the office boundary and eight full-height columns were modelled.

Moreover, the light distribution data from the manufacturer's ULD file is used in the calculation [3], while DIALux calculates reflected light using the surface reflectances listed in Table 1. The fittings sit within the 600 mm ceiling tiles and have their light-emitting faces aligned with the 2.8 m ceiling, whereas in the DIALux simulation report, the luminaire reference position is listed at 2.868 m, which is 68 mm above the ceiling plane. Figure 1 depicts the model alongside the evaluation heights.

Figure 1. Native room view (left) and adopted calculation heights (right).

### 2.2 Task-area calculation

Each 1.6 by 0.8 m desk has a 10 by 5 calculation grid at 0.8 m height. According to EN 12464-1 clause 5.4, a 2:1 area is governed by its short side, which limits the maximum spacing to 0.2 x 5^log10(0.8) = 0.171 m [1]. As a result, the selected 0.16 m grid meets this requirement. Meanwhile, DIALux defines the overall uniformity Uo as the ratio of minimum to mean illuminance [4]. Ultimately, individual desk checks are essential to prevent some poorly lit workstations from being overlooked due to a satisfactory room average. 

### 2.3 Maintenance factor and glare

By applying a maintenance factor of 0.80, the gradual reduction in illumination is accounted for over time [5]. In addition, glare was calculated at a seated eye height of 1.2 m across viewing directions at 15-degree intervals [6]. While the manufacturer gives a catalogue UGR value for the fitting, the glare experienced in the office also depends on luminaire positioning and office surroundings, therefore, the calculated room values are compared against the UGR limit.

Furthermore, calculations were applied to the 0.5 m bands around the bench groups, the remaining background floor, cylindrical illuminance at seated head height, and the exposed walls and ceiling. The same fittings and positions were maintained for the desk calculation, where the desks serve as calculation surfaces, whereas solid furniture, monitor screens, and high partitions are excluded. Finally, separate copies were used for the output and reflectance comparisons, with all other inputs held constant.

## 2.4 Native DIALux documentation

With a zero wall offset, the automatic whole-room plane reports 640 lx and Uo = 0.002, which rules out a claim of uniform task lighting everywhere. Instead, the adopted assessment evaluates the proposed desk positions, their surroundings, and the accessible background, meaning that a revised seating plan would require a new desk assessment.

Figure 2. Native DIALux workstation results, pp. 254, 256, 529 and 316, respectively.

### Reading the local result

Each point samples the same horizontal task surface to each point. With a mean of 593 lx and a minimum of 525 lx, Desk-021 has Uo = 525/593 = 0.89. Although its low mean governs the illuminance margin, Desk-084 governs uniformity, this distinction would be lost in a room-wide average.

### Spacing and lumen-method checks

For a typical 2.4 m spacing and a nominal 2.0 m height above the desk plane, the SHR is about 1.20. However, local spacings vary around columns and edges; thus, the individual desk grids are used to directly verify uniformity at those locations. Using N = E x A / (flux x UF x MF), 186 fittings would require a UF of 0.875 to reach an average of 500 lx across the entire 1042.10 m2 floor area at an MF of 0.80. Since this serves only as a threshold calculation, the L-shaped room and the individual desk criteria are assessed with the DIALux evo model.

## 3. Luminaire selection and lighting layout

### 3.1 Selected luminaire

The selected fitting is the Philips PowerBalance gen2 RC461B 40S/840, with 186 fittings in total. Each fitting is rated at 4000 lm and 23 W, achieving a high efficacy of approximately 174 lm/W [3] and delivering enough light to reach the office standard of 500 lx per desk surface [1], [7]. It also has a colour temperature of 4000 K and a colour rendering index above 80, which are appropriate for these office activities [3]. In particular,  the fitting is rated for a UGR of 16 rather than the UGR of 19 limit [1], [8], reducing perceived discomfort by preventing bright light from shining directly into the eyes of seated occupants using computer screens or reading printed materials.

### 3.2 Ceiling coordination and light distribution

Each 597 x 597 mm fitting occupies one 600 mm ceiling tile. While the typical spacing is 2.4 m, adjustments are made near columns and edges. As shown in Figure 3, the broad downward distribution ensures adequate beam overlap at desk height.

Figure 3. Ceiling layout (a) and principal light distributions from the manufacturer LDT (b) [3]. DIALux uses 1–186 and Drawing L01 uses L001–L186.

### 3.3 Output selection and installation

Table 2. Manufacturer ratings and modelled layout choices.

| Luminaire | Count | lm / W per fitting | Catalogue UGR | Connected kW* |
| --- | --- | --- | --- | --- |
| CoreLine [9] | 142 | 4300 / 32 | 19 | 4.54 |
| PowerBalance 34S [10] | 186 | 3400 / 20 | 16 | 3.72 |
| PowerBalance 40S [3] | 186 | 4000 / 23 | 16 | 4.28 |

*Luminaire input only. The CoreLine trial used the automatic working plane and a different layout. At the same 186 positions, 34S and 40S gave 504 lx and 593 lx as their lowest desk means, respectively.

At least 86 mm of ceiling void depth is required for the fitting body, in addition to space for external drivers and maintenance access [3]. Drawing L01 on page 10 identifies each fitting and provides the luminaire schedule.

## 4. Simulation results and interpretation

### 4.1 Distribution of task illumination

All 112 desks meet the selected illuminance, uniformity, and glare requirements, with the lowest desk average at 593 lx, the lowest uniformity at 0.80, and the highest calculated UGR at 18.1. Due to these values occurring at different desks, Figure 4 illustrates the variation in desk-average illuminance across the office and identifies the three desks giving the limiting results. 

Figure 4. Desk-average illuminance; A, B and C identify the three controlling desks. Appendix D shows the native false-colour views.

### 4.2 Desks with the lowest lighting levels and highest glare

Desk-021 averages 593 lx at the south perimeter, with its centre located 2.40 m from the boundary. While L140 and L136 are about 1.0 m and 1.4 m away, positioned on either side of the desk north to south, the perimeter limits additional coverage from rows farther south, leaving L013 about 7.7 m away.

Desk-084 has the lowest Uo (0.80), with a range of 521-736 lx around a 654 lx mean. L120 is only 0.36 m from the desk centre and sits toward one side of the desk, resulting in a gradient across the task area on the native isolux plot, consistent with uneven overlap from the adjacent fittings.

At Desk-018 the highest directional UGR is 18.1 at 180 degrees (Appendix A, PDF p. 12, DIALux p. 316), where several luminaires are close to the observer, with L028 and L014 within 1.5 m in plan. While the directional result reflects the combined effect of source luminance, apparent position, and background luminance, the export only gives the total, leaving individual contributions source unquantified.

Appendix A includes the native task contours and directional glare result. The automatic WP1 surface samples the wider room, including column footprints; in contrast, the 112 explicit desk surfaces define the task-area check for the proposed furniture plan.

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

Sources: [1, Table 34, row 34.2 and clauses 5.3.4-5.3.5, 5.6.2]; [3] for colour rendering; [11, Tables 5.4-5.5 and clauses 5.6.1-5.6.2] for energy and controls. *Conservative uniformity bound across a group.

### 5.1 Illuminance and uniformity

The background floor receives 617 lx, which is significantly higher than the 100 lx target, because the regular ceiling grid delivers more light than required in circulation areas. To address this, the four circulation zones provide a way to test reduced lighting outputs against the background and nearby task criteria, while group uniformity bounds are calculated using the lowest point divided by the highest surface mean, rounded down.

### 5.2 Glare and screen reflections

In the baseline, the highest directional UGR is 18.1. To verify luminance limits, the LDT check scales intensity to 4000 lm and divides it by the projected area of the 510 x 510 mm aperture, which gives a maximum sampled luminance of 1334 cd/m2 (C44, gamma 65 degrees). This is below the 1500 cd/m2 limit set by EN clause 5.9.2 and Table 7 for Case A medium-luminance screens (high state up to 200 cd/m2) tilted up to 15 degrees from vertical [1]. While the check covers sampled angles from 65 to 89 degrees, since projection is undefined at 90 degrees, screen type, tilt, and orientation must be confirm at fit-out.

## 6. Lighting controls and energy use

### 6.1 Local and automatic control

The office is divided into 32 independent control zones: 28 for bench groups and four for circulation, each with local manual switching and dimming. The largest zone measures 46.67 m2, which is below the 250 m2 automatic-control limit. According to BEC Table 5.5, the 1042.10 m2 office requires 32 manual control points without needing a reduction for low power density [11], and Figure 5 illustrates their boundaries.

Each zone switches off after 10 minutes without occupancy, which falls within the BEC limit of 15 minutes. In addition, a schedule switches lighting off outside working hours, with local overrides limited to 120 minutes. To verify compliance, commissioning must confirm at least 50% power reduction, including sensor and driver standby consumption [11, Sec. 5.6.1].

Figure 5. Proposed independent lighting control zones. The DIALux calculation uses one luminaire group.

### 6.2 Daylight response

In areas where the external glazing and lighting load meet BEC clause 5.6.2 criteria, daylight-responsive control is proposed [11]. However, window dimensions and grouping are still needed to define these zones and check the exceptions. Where it is required, the controller must also be able to reduce lighting power to 50% or less, or switch it off entirely, in response to daylight.

### 6.3 Connected power

The fittings draw 186 x 23 = 4278 W. With a 50 W allowance for sensors and shared control equipment, the design load reaches 4328 W, or 4.153 W/m2 across 1042.10 m2, which is below the BEC limit of 7.2 W/m2. At full load for 2500 h/year, the energy use is about 10.82 MWh/year. However, a controlled estimate requires logged occupancy, driver power at dimmed output, and standby loads.

## 7. Design comparison and conclusion

### 7.1 Comparison of calculation conditions

DIALux tested three sensitivity scenarios: 90% output, lower ceiling/wall/floor reflectances (70/50/20%), and both combined, while retaining the original layout and MF. Table 4 shows the workstation performance.  

Table 4. Workstation results by calculation condition.

| Case | Lowest desk mean | Lowest Uo | Highest UGR |
| --- | --- | --- | --- |
| Requirement | ≥500 lx | ≥0.60 | ≤19 |
| Baseline | 593 lx | 0.80 | 18.1 |
| 90% output | 534 lx | 0.80 | 17.7 |
| Lower reflectance | 566 lx | 0.79 | 18.6 |
| Combined | 509 lx | 0.79 | 18.2 |

### 7.2 Design choice

At 90% output, the lowest desk mean is 534 lx, 6.8% above the target, and the worst directional UGR falls from 18.1 to 17.7. In contrast, lower reflectance at full output reduces the minimum desk mean to 566 lx while the UGR rises to 18.6, leaving a 0.4 margin below the limit.

With both changes combined, the lowest desk mean is 509 lx and the maximum directional UGR is 18.2. This relatively narrow 9 lx illuminance margin supports keeping full output as the design setting and tuning the installed system after completion.

### 7.3 Maintenance and conclusion

The maintenance factor is calculated as LLMF x LSF x LMF x RSMF = 0.90 x 1.00 x 0.95 x 0.94 = 0.8037, which is rounded down to 0.80 [5]. Specifically, the product declares L90 at 50,000 h [3], while the remaining factors assume prompt replacement, annual cleaning, and retained room finishes.

Full output remains the design setting, as the 593 lx minimum maintained desk mean is 19% above the 500 lx target and corresponds to about 741 lx initially under the adopted MF. Accordingly, local dimming can be commissioned after installation against the actual finishes, desks, and screens, though dimmed power should be verified separately.

## References

[1] Light and lighting - Lighting of work places - Part 1: Indoor work places, BS EN 12464-1:2021, British Standards Institution, London, U.K., 2021, doi: 10.3403/30385601. https://doi.org/10.3403/30385601

[2] Electrical and Mechanical Services Department, Technical Guidelines on Code of Practice for Energy Efficiency of Building Services Installation, 2024 ed., sec. 5.4.1(c), “Internal Floor Area,” p. 51. https://www.emsd.gov.hk/beeo/en/pee/TG-BEC_2024.pdf

[3] Signify, "Philips PowerBalance gen2, RC461B 40S/840 SEIA W60L60 VPC U4 WH SC UE," product 910505103638. Accessed: Nov. 16, 2026. [Online]. Available: https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-powerbalance-gen2/910505103638_EU/product

[4] DIAL GmbH, "Parameters of a calculation object," Knowledge Base DIALux evo, Sep. 19, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000075351-parameters-of-a-calculation-object

[5] DIAL GmbH, "Maintenance factors," Knowledge Base DIALux evo, Feb. 17, 2023. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000122341-maintenance-factors

[6] DIAL GmbH, "UGR method - Unified Glare Rating," Knowledge Base DIALux evo, May 21, 2026. Accessed: Nov. 16, 2026. [Online]. Available: https://evo.support-en.dial.de/support/solutions/articles/9000073310-ugr-method-unified-glare-rating

[7] Electrical and Mechanical Services Department, Task Lighting Design, p. 4 (PDF). https://www.emsd.gov.hk/filemanager/en/content_2/Task_Lighting_Design.pdf

[8] BEAM Society Limited, BEAM Plus Interiors, Version 2.0, Non-Residential, 2023, Health and Wellbeing, Unified Glare Rating, item (b), p. 173 (PDF). https://www.beamsociety.org.hk/en/BEAM-Plus/-/media/7400264437D8466599EB31804B350988.ashx

[9] Signify, "Philips CoreLine Panel gen6, RC132V G6 43S/840, product 910505102802." Accessed: Nov. 18, 2026. [Online]. Available: https://www.signify.com/global/prof/indoor-luminaires/recessed/philips-coreline-panel-gen6/910505102802_EU/product

[10] Signify, "Philips PowerBalance gen2, RC461B 34S/840, product 910505103630." Accessed: Nov. 18, 2026. [Online]. Available: https://www.signify.com/api/assets/v1/file/Signify/content/910505103630_EU.en_AA.PROF.FP/Localized_commercial_leaflet_910505103630_en_AA.pdf

[11] Electrical and Mechanical Services Department, Code of Practice for Energy Efficiency of Building Services Installation, 2024 ed. Hong Kong: Government of the Hong Kong Special Administrative Region, 2024, sec. 5, pp. 16-21. Accessed: Nov. 16, 2026. [Online]. Available: https://www.emsd.gov.hk/beeo/en/pee/BEC_2024_ENG.pdf
