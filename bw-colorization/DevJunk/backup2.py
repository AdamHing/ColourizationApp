import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import getcwd
import filetype
import psutil
import GPUtil
import wmi
import subprocess
import time


f = open("communicate.txt","w")
f.write('')
f.close()

qtCreatorFile = "D:\\coding\\python\\bw-colorization\\colourgui.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Ui(QtWidgets.QMainWindow, QtCore.QThread):


    custom_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('D:\\coding\\python\\bw-colorization\\colourgui.ui', self) # Load the .ui file

        self.thread = QtCore.QThread()
        #window settings
        self.setFixedSize(500, 310)#220
        self.setWindowTitle('Colourization GUI')
        self.setWindowIcon(QtGui.QIcon('Zealot_SC2_Art1.jpg'))

        #cpu/gpu ID
        self.cpuID = self.findChild(QtWidgets.QLabel, 'cpuID')
        self.gpuID = self.findChild(QtWidgets.QLabel, 'gpuID')
        computer = wmi.WMI()
        proc_info = computer.Win32_Processor()[0]
        gpu_info = computer.Win32_VideoController()[0]
        self.cpuID.setText('{0}'.format(proc_info.Name))
        self.gpuID.setText('{0}'.format(gpu_info.Name))
        #progress bar
        self.cpuBar = self.findChild(QtWidgets.QProgressBar, 'progressBar_1')
        self.gpuBar = self.findChild(QtWidgets.QProgressBar, 'progressBar_2')
        #clearbutton
        self.clearButton = self.findChild(QtWidgets.QPushButton, 'Clear')
        self.clearButton.clicked.connect(self.resetInputs)
        #gobutton
        self.button = self.findChild(QtWidgets.QPushButton, 'goButton')
        self.button.clicked.connect(self.GoWhenPressed)
        #processMode
        self.cpuButton = self.findChild(QtWidgets.QPushButton, 'cpuButton')
        self.cpuButton.clicked.connect(self.cpu)
        self.gpuButton = self.findChild(QtWidgets.QPushButton, 'gpuButton')
        self.gpuButton.clicked.connect(self.gpu)
        #file input
        self.fileInput = self.findChild(QtWidgets.QLineEdit, 'fileInput')
        self.browseFile = self.findChild(QtWidgets.QPushButton, 'get_file')
        self.browseFile.clicked.connect(self.open_fileBrowser)
        #radio Buttons
        self.radioButton = self.findChild(QtWidgets.QRadioButton, 'radioButton')
        self.radioButton.clicked.connect(self.radiobutton_checked)

        self.radioButton2 = self.findChild(QtWidgets.QRadioButton, 'radioButton_2')
        self.radioButton2.clicked.connect(self.radiobutton_checked)

        self.radioButton3 = self.findChild(QtWidgets.QRadioButton, 'radioButton_3')
        self.radioButton3.clicked.connect(self.radiobutton_checked)

        self.radioButton4 = self.findChild(QtWidgets.QRadioButton, 'radioButton_4')
        self.radioButton4.clicked.connect(self.radiobutton_checked)
        
        self.Cpu_gpu_Usage = cpu_gpu_Usage()
        self.Cpu_gpu_Usage.cpuUsageReading.connect(self.cpuReadings)
        self.Cpu_gpu_Usage.gpuUsageReading.connect(self.gpuReadings)
        self.Cpu_gpu_Usage.start()
        self.info_thread = Info_thread()
        
        self.fps_label = self.findChild(QtWidgets.QLabel, 'fps_label')
        # self.elapsedTime = self.findChild(QtWidgets.QLabel, 'elapsedTime')

        self.info_thread.vid_FPS.connect(self.vid_FPS_Readings)

        self.show()

    def vid_FPS_Readings(self, fpsval):
        self.fps_label.setText(fpsval)
        # self.elapsedTime.setText(fpsval)

    def cpuReadings(self, cpuval):
        self.cpuBar.setValue(cpuval)

    def gpuReadings(self, gpuval):
        self.gpuBar.setValue(gpuval)

    #cpu mode
    def cpu(self):
        print("cpu")
        global gc_toggle
        gc_toggle = "0"
        print(gc_toggle)
        self.gpuButton.setStyleSheet("none")
        self.cpuButton.setStyleSheet("background-color: grey")
    #gpu mode
    def gpu(self):
        print("gpu")
        global gc_toggle
        gc_toggle = "1"
        print(gc_toggle)
        self.cpuButton.setStyleSheet("none")
        self.gpuButton.setStyleSheet("background-color: grey")
    #reset inputs
    def resetInputs(self):
        self.fileInput.setText(None)
        global gc_toggle
        gc_toggle = None
        self.cpuButton.setStyleSheet("none")
        self.gpuButton.setStyleSheet("none")

    #open_fileBrower
    def open_fileBrowser(self):
        global isImageFormat, setmode, dovideo, doimage, isVideoFormat, sourcefile
        dovideo = False
        doimage = False
        filename = QFileDialog.getOpenFileName()
        sourcefile = filename[0]
        self.fileInput.setText(sourcefile)
        isImageFormat = filetype.is_image(sourcefile)
        isVideoFormat = filetype.is_video(sourcefile)
        self.radioButton.setChecked(isImageFormat)
        self.radioButton2.setChecked(isVideoFormat)
        
        if self.radioButton.isChecked(): #imagecolourize
            print("checked")
            setmode = "\\bw2color_image.py"
            doimage = True
        if self.radioButton2.isChecked():#videocolourize
            print("checked2")
            setmode = "\\bw2color_video.py"
            dovideo = True
    #radiobuttons
    def radiobutton_checked(self):
        global setmode,dovideo,doWebcam,doimage,dodecolourize
        dovideo = False
        doimage = False
        doWebcam = False
        dodecolourize = False
        self.fileInput.setDisabled(False)
        self.browseFile.setDisabled(False)
        self.cpuButton.setDisabled(False)
        self.gpuButton.setDisabled(False)
        
        if self.radioButton.isChecked(): #imagecolourize
            print("checked")
            setmode = "\\bw2color_image.py"
            doimage = True
            
        if self.radioButton2.isChecked():#videocolourize
            print("checked2")
            # setmode = "\\bw2color_video.py"
            setmode = "\\test.py"
            dovideo = True
            
        if self.radioButton3.isChecked():#decolourize
            print("checked3")
            setmode = "\\decolorization2.py"
            dodecolourize = True
            self.cpuButton.setDisabled(True)
            self.gpuButton.setDisabled(True)

        if self.radioButton4.isChecked():#Webcam
            print("checked4")
            setmode = "\\bw2color_video.py"
            doWebcam = True
            self.fileInput.setText(None)
            self.fileInput.setDisabled(True)
            self.browseFile.setDisabled(True)
        
    #gobutton
    def GoWhenPressed(self):
        self.info_thread.start()
        self.button.setStyleSheet("background-color: grey")
        #error fail safe
        mode = setmode
        print(setmode)
        if setmode == None:
            QMessageBox.about(self, "Warning", "Fill all stuffs")
         
        pythonpath = "python "
        folderlocation = getcwd()
        mediatype = folderlocation + mode
        modelpath = folderlocation + "\\model\\"
        sourcefile = self.fileInput.text()
        
        if doimage == True:
            startImageColourizing = pythonpath + mediatype + ' --image '+ sourcefile + ' --prototxt ' + modelpath + 'colorization_deploy_v2.prototxt' + ' --model ' + modelpath +'colorization_release_v2.caffemodel' + ' --points ' + modelpath +'pts_in_hull.npy' + ' --usegpu '+ gc_toggle
            print(startImageColourizing)
            subprocess.Popen(startImageColourizing)

        elif dovideo== True:
            startVideoColourizing = pythonpath + mediatype + ' --prototxt ' + modelpath + 'colorization_deploy_v2.prototxt' + ' --model ' + modelpath + 'colorization_release_v2.caffemodel' + ' --points ' + modelpath + 'pts_in_hull.npy' + ' --input ' + sourcefile + ' --usegpu '+ gc_toggle
            print(startVideoColourizing)
            self.thread.start()
            subprocess.Popen(startVideoColourizing)
            self.custom_signal.emit(startVideoColourizing)

        elif doWebcam== True:
            startWebcamColourizing = pythonpath + mediatype + ' --prototxt ' + modelpath + 'colorization_deploy_v2.prototxt' + ' --model ' + modelpath + 'colorization_release_v2.caffemodel' + ' --points ' + modelpath + 'pts_in_hull.npy' + ' --usegpu '+ gc_toggle
            print(startWebcamColourizing)
            subprocess.Popen(startWebcamColourizing)
            
        elif dodecolourize == True:
            startDecolourizing = pythonpath + mediatype + ' --image ' + sourcefile
            print(startDecolourizing)
            subprocess.Popen(startDecolourizing)

        print("test1")

class Info_thread(QtCore.QThread):
    vid_FPS = pyqtSignal(str)
    def __init__(self, parent=None):
        super(Info_thread, self).__init__(parent)
    def run(self):
        print('d')
        while 1:
            time.sleep(1)
            f = open("communicate.txt", "r")
            # print(f.read())
            self.vid_FPS.emit(f.read())

class cpu_gpu_Usage(QtCore.QThread):
    cpuUsageReading = pyqtSignal(int)
    gpuUsageReading = pyqtSignal(int)
    def __init__(self, parent=None):
        super(cpu_gpu_Usage, self).__init__(parent)
    def run(self):
        print('a')
        while 1:
            cpuPercent = psutil.cpu_percent(interval=1)
            self.cpuUsageReading.emit(cpuPercent)
            
            GPUs = GPUtil.getGPUs()
            gpuPercent = GPUs[0].load * 100
            self.gpuUsageReading.emit(gpuPercent)

app = QtWidgets.QApplication(sys.argv)
# app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
window = Ui()
sys.exit(app.exec_())
print("tail")