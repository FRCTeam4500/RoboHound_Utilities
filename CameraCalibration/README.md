# Camera Calibration
This software assists in identifying the intrinsic and extrinsic parameter of a camera as well as it's horizontal and vertical FOV. 

## Instillation
1) Navigate to this repo's [releases](https://github.com/FRCTeam4500/RoboHound_Utilities/releases) and download the version for your system.
2) Extract the contents to a desired directory.
3) Run the executable

## Building from source

### Dependencies
If you wish to make changes to the project, the following are needed:
```sh
# 1) Make sure Python 3, pip3, and the Python3-dev are installed on your OS
# 2) Execute the following command:
pip3 install numpy==1.15.4 opencv-python==3.4.5.20 PyQt5 pyqt5-tools pyinstaller
```

### Building
Pyinstaller is used to build the executable files. To generate an executable for Windows, run *build_windows.bat*. To generate an executable for Linux, run *build_linux.sh*. The executable is stored in *output/dist/*

## Authors

* **Nicolas Newman** - *Initial work* - [NicolasNewman](https://github.com/NicolasNewman)

## Usage
1) Follow [this](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html) guide for a general overview of how to gather your dataset of images

## License

This project is licensed under the MIT License - see the [LICENSE.md](../LICENSE) file for details