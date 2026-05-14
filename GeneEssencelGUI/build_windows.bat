@echo off
setlocal

rmdir /s /q build dist 2>nul
del /f GeneEssenceGUI.spec 2>nul

pyinstaller ^
  --name GeneEssenceGUI ^
  --windowed ^
  --icon assets\genne_essence.png ^
  --add-data "assets;assets" ^
  --add-data "prepareDataset2RNA.jar;." ^
  --add-data ".env;." ^
  --collect-submodules sklearn ^
  --collect-submodules matplotlib ^
  GeneEssenceGUI.py

echo Build complete: dist\GeneEssenceGUI\