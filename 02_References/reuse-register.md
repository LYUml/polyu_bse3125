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
# Assignment PDF resource pruning

The complete 112-task native report shares large resource dictionaries. A 14-page PDFium-only excerpt exceeded 10 MB. Reused pikepdf 10.5.0 (MPL-2.0, installed locally from PyPI, no source vendored) and its documented `Pdf.remove_unreferenced_resources()` to copy explicit pages and remove unused resources. The bounded excerpt is 844,601 bytes. Independent PDFium verification preserved page text, physical dimensions and exact rendered pixels at both 72 and 150 dpi. See `06_Tools/compact_pdf_excerpt.py` and the excerpt manifest. This is lossless resource pruning, not resampling or recreating native results. Documentation: https://pikepdf.readthedocs.io/en/stable/api/main.html and https://pikepdf.readthedocs.io/en/stable/topics/pages.html .
