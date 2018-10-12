if not exist .\Port_Python (
.\automationConfig_files\7z.exe x ..\tools\Port_Python.zip )

set path=.\Port_Python;%path%
Python-Portable Run_2DOverlay_Suite.py