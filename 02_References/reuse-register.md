# Reuse register

Reviewed 2026-11-16. Reuse existing implementations; add assignment-specific data and evidence rather than competing serializers or unverified calculation engines.

| Repository | Review and adopted use | Limits |
| --- | --- | --- |
| https://github.com/LYUml/dialux-agent-toolkit | Local README, skill, acceptance map and modules inspected; public repository confirmed. Use standalone desktop CLI, CAD interchange, report readers and evidence workflows. Record local commit at milestones. | Capability documentation is not assignment acceptance; native checks required. |
| https://github.com/MarcosCastanedaVentura/MCP_Dialux | Toolkit already vendors pinned commit 4489032e67cabe0d409819fad24f091128620a9d with MIT license. Reuse its STF serializer through toolkit room-create. | Import carries geometry, not verified photometry or calculation; no second copy needed. |
| https://github.com/HKUDS/CLI-Anything | Toolkit's upstream review records Apache-2.0 architecture research. Reuse existing CLI/JSON/evidence design through toolkit, no code copied here. | DIALux's live desktop backend remains necessary. |
| https://github.com/ZOdiaKTN/dwg2ifc | Earlier review identifies experimental orthogonal DWG-to-IFC route. Not adopted. | Existing native DXF plus STF is sufficient; IFC adds Pro dependency and unproven reconstruction. |
| https://github.com/BHoM/DIALux_Toolkit | Existing upstream STF lineage; no additional code copied. | Avoid redundant legacy DIALux 4 serializer. |
| https://github.com/luciodias/EvoParse | Rechecked public repository and STEP/schema inspection approach on 2026-11-16. No root license verified; no source copied or package installed. A small independent read-only record inspector uses the schema included in the user's own native project. | Native archive cloning is experimental and must pass actual DIALux reopen, calculation, report and persistence checks; syntax/schema checks alone prove no native validity. |

Official references rechecked: EMSD BEC index https://www.emsd.gov.hk/beeo/en/mibec_beeo_codtechguidelines.html and CIBSE LG7 2023 publication page https://www.cibse.org/knowledge-research/knowledge-portal/lg7-lighting-for-offices-2023. Publication discovery does not authenticate numerical clauses. Manufacturer candidate page https://www.signify.com/pt-pt/prof/luminarias-de-interior/encastradas/philips-painel-coreline-gen6/910505102802_EU/product and official family leaflet identified. Final source register will bind adopted facts to actual source bytes/pages.
