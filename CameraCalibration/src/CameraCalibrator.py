import numpy as np
import cv2
import sys
import os.path
import glob
import math
import json

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QWidget, QListWidget

class CameraCalibrator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = None
        self.load_ui()

        self.resultWindow = ResultWindow()
    
    def load_ui(self):
        self.ui = loadUi('CameraCalibrator.ui', self)

        self.editInputDir = self.ui.findChild(QLineEdit, 'editInputDir')
        self.btnInputDir = self.ui.findChild(QPushButton, 'btnInputDir')
        self.btnInputDir.clicked.connect(lambda: self.loadDir(self.editInputDir))
       
        self.btnOutputDir = self.ui.findChild(QPushButton, 'btnOutputDir')
        self.editOutputDir = self.ui.findChild(QLineEdit, 'editOutputDir')
        self.btnOutputDir.clicked.connect(lambda: self.loadDir(self.editOutputDir))
        
        self.editWidth = self.ui.findChild(QLineEdit, 'editWidth')
        self.editHeight = self.ui.findChild(QLineEdit, 'editHeight')

        self.btnStart = self.ui.findChild(QPushButton, 'btnStart')
        self.btnStart.clicked.connect(self.startClicked)

        self.checkAdaptive = self.ui.findChild(QCheckBox, 'checkAdaptive')
        self.checkNormalize = self.ui.findChild(QCheckBox, 'checkNormalize')
        self.checkFilter = self.ui.findChild(QCheckBox, 'checkFilter')
        self.checkFast = self.ui.findChild(QCheckBox, 'checkFast')

        self.flagDic = {
            "CALIB_CB_ADAPTIVE_THRESH": cv2.CALIB_CB_ADAPTIVE_THRESH,
            "CALIB_CB_NORMALIZE_IMAGE": cv2.CALIB_CB_NORMALIZE_IMAGE,
            "CALIB_CB_FILTER_QUADS": cv2.CALIB_CB_FILTER_QUADS,
            "CALIB_CB_FAST_CHECK": cv2.CALIB_CB_FAST_CHECK
        }
        self.selectedFlags = None
        
        self.show()
    
    def loadDir(self, editPath):
        editPath.setText(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def startClicked(self):
        try:
            self.width = int(self.editWidth.text())
            self.height = int(self.editHeight.text())

            self.inputPath = self.editInputDir.text()
            self.outputPath = self.editOutputDir.text()
            
            self.selectedFlags = []
            if self.checkAdaptive.isChecked():
                self.selectedFlags.append(self.checkAdaptive.text())
            if self.checkNormalize.isChecked():
                self.selectedFlags.append(self.checkNormalize.text())
            if self.checkFilter.isChecked():
                self.selectedFlags.append(self.checkFilter.text())
            if self.checkFast.isChecked():
                self.selectedFlags.append(self.checkFast.text())
            
            self.calibrate()
        except ValueError:
            print("ERROR: Please enter a valid number")
    
    # Method source:
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
    # https://github.com/ligerbots/VisionServer/blob/master/utils/camera_calibration.py
    def calibrate(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((self.width * self.height, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.width, 0:self.height].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        total = 0
        success = 0
        failed = 0
        failedList = []


        images = glob.glob(os.path.join(self.inputPath, '*.jpg'))

        for fname in images:
            print('Processing file', fname)
            img = cv2.imread(fname)

            if img is None:
                print('ERROR: Unable to read file', fname)
                continue
            self.shape = img.shape
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            if len(self.selectedFlags) == 0:
                ret, corners = cv2.findChessboardCorners(gray, (self.width, self.height), None)
            elif len(self.selectedFlags) == 1:
                ret, corners = cv2.findChessboardCorners(gray, (self.width, self.height), self.flagDic[self.selectedFlags[0]])
            elif len(self.selectedFlags) == 2:
                ret, corners = cv2.findChessboardCorners(gray, (self.width, self.height), self.flagDic[self.selectedFlags[0]] + self.flagDic[self.selectedFlags[1]])
            elif len(self.selectedFlags) == 3:
                ret, corners = cv2.findChessboardCorners(gray, (self.width, self.height), self.flagDic[self.selectedFlags[0]] + self.flagDic[self.selectedFlags[1]] + self.flagDic[self.selectedFlags[2]])
            elif len(self.selectedFlags) == 4:
                ret, corners = cv2.findChessboardCorners(gray, (self.width, self.height), self.flagDic[self.selectedFlags[0]] + self.flagDic[self.selectedFlags[1]] + self.flagDic[self.selectedFlags[2]] + self.flagDic[self.selectedFlags[3]])
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (self.width ,self.height), corners2,ret)
                cv2.imshow('img',img)

                if self.outputPath:
                    name = os.path.join(self.outputPath, os.path.basename(fname))
                    cv2.imwrite(name, img)

                cv2.waitKey(500)
                success += 1
            else:
                print(fname, 'failed')
                failed += 1
                failedList.append(fname)
            
            total += 1

        cv2.destroyAllWindows()

        if not objpoints:
            print("No useful images. Quitting...")
            return None
    
        print('Found {} useful images'.format(len(objpoints)))
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


        print('reprojection error = ', ret)
        print('image center = ({:.2f}, {:.2f})'.format(mtx[0][2], mtx[1][2]))

        fov_x = math.degrees(2.0 * math.atan(self.shape[1] / 2.0 / mtx[0][0]))
        fov_y = math.degrees(2.0 * math.atan(self.shape[0] / 2.0 / mtx[1][1]))
        print('FOV = ({:.2f}, {:.2f}) degrees'.format(fov_x, fov_y))

        self.resultWindow.setTotal(total)
        self.resultWindow.setSuccess(success)
        self.resultWindow.setFailed(failed)
        self.resultWindow.setFOV(fov_x, fov_y)
        self.resultWindow.setCenter(mtx[0][2], mtx[1][2])
        self.resultWindow.setList(failedList)
        self.resultWindow.show_ui()

        print('mtx = ', mtx)
        print('dist = ', dist)

        if self.outputPath:
            with open(os.path.join(self.outputPath, 'data.json'), 'w+') as f:
                json.dump({"camera_matrix": mtx.tolist(), "distorsion": dist.tolist()}, f)
    
class ResultWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = None
        self.load_ui()
    
    def load_ui(self):
        self.ui = loadUi('Result.ui', self)

        self.labelTotal = self.ui.findChild(QLabel, 'labelTotal')
        self.labelSuccess = self.ui.findChild(QLabel, 'labelSuccess')
        self.labelFailed = self.ui.findChild(QLabel, 'labelFailed')

        self.listFailed = self.ui.findChild(QListWidget, 'listFailed')

        self.labelFOV = self.ui.findChild(QLabel, 'labelFOV')
        self.labelCenter = self.ui.findChild(QLabel, 'labelCenter')
    
    def show_ui(self):
        self.show()


    def setTotal(self, total):
        self.labelTotal.setText('Total: {}'.format(total))
        
    def setSuccess(self, success):
        self.labelSuccess.setText('Success: {}'.format(success))

    def setFailed(self, failed):
        self.labelFailed.setText('Failed: {}'.format(failed))

    def setFOV(self, fovX, fovY):
        self.labelFOV.setText('FOV: ({:.2f}, {:.2f})'.format(fovX,  fovY))

    def setCenter(self, centerX, centerY):
        self.labelCenter.setText('Center: ({:.2f}, {:.2f})'.format(centerX,  centerY))
    
    def setList(self, list):
        self.listFailed.addItems(list)

app = QApplication(sys.argv)
cameraCalibrator = CameraCalibrator()
sys.exit(app.exec_())