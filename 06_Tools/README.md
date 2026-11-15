# Tools

Backend: C:/Users/lyuml-win/Desktop/dialux-agent-toolkit, inspected commit ade128b7ae446c6ea253776a5ead866280d6bf4a.
Python: that checkout's .venv/Scripts/python.exe. Run CLI from toolkit root with `-m src.dialux_agent`; use absolute assignment paths.
Only one live DIALux desktop operation at a time. Inspect status and journals after timeout; never blindly repeat a mutation.

Assignment scripts live in 05_Calculations/scripts. Source survey reads original files and reused native-converted DXF, verifies hashes and generates inspection evidence. prepare_model.py generates the initial source-linked room specification, not final simulation or compliance evidence.
