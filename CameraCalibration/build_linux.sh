#!/bin/sh
pyinstaller --onefile --name="Camera Calibrator" --noconfirm \
    --distpath=output/dist --workpath=output/build --specpath=output/spec \
    src/CameraCalibrator.py
rm -rf src/__pycache__
cp src/CameraCalibrator.ui output/dist/CameraCalibrator.ui