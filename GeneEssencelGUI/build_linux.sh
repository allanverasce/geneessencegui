#!/bin/bash
set -e

# python3-tk must be installed on the target system: sudo apt install python3-tk
rm -rf build dist GeneEssenceGUI.spec

pyinstaller \
  --name GeneEssenceGUI \
  --windowed \
  --icon assets/genne_essence.png \
  --add-data "assets:assets" \
  --add-data "prepareDataset2RNA.jar:." \
  --add-data ".env:." \
  --collect-submodules sklearn \
  --collect-submodules matplotlib \
  GeneEssenceGUI.py

echo "Build complete: dist/GeneEssenceGUI/"