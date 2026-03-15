@echo off
pip install pyinstaller
pip install pillow

pyinstaller ^
--distpath %CD%\.. ^
--onefile ^
--add-data "%CD%\..\content;content" ^
--windowed ^
--clean ^
--optimize 2 ^
--icon %CD%\..\content\icon.png ^
--version-file version.txt ^
%CD%\..\main.py

del %CD%\..\tilemap.exe
ren %CD%\..\main.exe tilemap.exe
rmdir /s /q build

pause