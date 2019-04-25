pyinstaller --onefile --name="Camera Calibrator" --noconfirm --noconsole ^
    --distpath=output/dist --workpath=output/build --specpath=output/spec ^
    src/CameraCalibrator.py
rmdir /s /q "src/__pycache__/"
xcopy /y "src\CameraCalibrator.ui" "output\dist"