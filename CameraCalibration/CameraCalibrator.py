from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QWidget
import sys

class CameraCalibrator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = None
        self.load_ui()
    
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
        self.show()
    
    def loadDir(self, editPath):
        editPath.setText(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def startClicked(self):
        self.width = self.editWidth.text()
        self.height = self.editHeight.text()

        self.inputPath = self.editInputDir.text()
        self.outputPath = self.editOutputDir.text()
    

app = QApplication(sys.argv)
cameraCalibrator = CameraCalibrator()
sys.exit(app.exec_())