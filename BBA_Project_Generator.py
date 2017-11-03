"""
#==============================================================================
#!/usr/bin/env python
#title           :BBA_Project_Generator.py
#description     :Script used to automate project folder creation
#author          :Doug Halley
#date            :20171103
#version         :2.0
#usage           :Standalone Python Application Executed by BBA_Project_Generator.exe
#notes           :
#python_version  :2.7.14
#pyqt_version    :4.11.4
#==============================================================================
"""

import os
import sys
import json
import datetime

from PyQt4 import QtGui
from PyQt4 import QtCore

class Main(QtGui.QMainWindow):
    """
    The class that contains, defines, and creates the UI
    """

    def __init__(self, parent=None):
        """
        Class init
        """
        super(Main, self).__init__(parent)
        self.initUI()

    def initUI(self):
        """
        Creates UI
        """

        #==============================================================================
        # Global Variables
        #==============================================================================

        # window title
        self.setWindowTitle("BBA Project Generator")

        if getattr(sys, 'frozen', False):
            # we are running in a |PyInstaller| bundle
            self.scriptLocation = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            # os.path.realpath(__file__) -  gets path of the current file
            self.scriptLocation = os.path.dirname(os.path.realpath(__file__))

        self.defaultConfig = self.scriptLocation + "\\" + "config.json"
        self.setWindowIcon(QtGui.QIcon(self.scriptLocation + "\\" + "bbalogo.ico"))

        # initlizes string to be used
        # initilized to use Orlando Project Drive
        self.projectTargetLocation = "\\\\FB2\\BBA_Jobs"
        self.orlandoJobsLocation = "\\\\FB2\\BBA_Jobs"
        self.tampaJobsLocation = "\\\\BBA-Tampa\\Tampajobs"

        #==============================================================================
        # PYQT Widget Defintions
        #==============================================================================        

        # main widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(QtGui.QVBoxLayout())

        # widget for project location radio buttons and year combobox
        self.projectWidget = QtGui.QWidget()
        self.projectWidget.setLayout(QtGui.QHBoxLayout())

        projectName_lbl = QtGui.QLabel("Create Project for")
        self.orlando_radioBtn = QtGui.QRadioButton("Orlando")
        projectOr_lbl = QtGui.QLabel("- or -")
        projectOr_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.tampa_radioBtn = QtGui.QRadioButton("Tampa")

        # set self.orlando_radioBtn to be true
        self.orlando_radioBtn.setChecked(True)

        # widget for project number line edit
        self.projectYearWidget = QtGui.QWidget()
        self.projectYearWidget.setLayout(QtGui.QHBoxLayout())

        projectYear_lbl = QtGui.QLabel("Project Year")

        # creates combobox for year
        self.projectYear_comboBox = QtGui.QComboBox()

        # gets current year
        year = datetime.datetime.today().year

        # oldest year for projects is 2013
        # plus 1 is meant to include 2013 in years
        # get difference of years
        DiffYears = year - 2013 + 1

        YEARS = range(year, year - DiffYears, -1)

        # iterate over years to fill years combobox
        for x in YEARS:
            self.projectYear_comboBox.addItem(QtCore.QString(str(x)))
        
        # widget for project number line edit
        self.projectNumberWidget = QtGui.QWidget()
        self.projectNumberWidget.setLayout(QtGui.QHBoxLayout())

        projectNumber_lbl = QtGui.QLabel("Project Number")
        self.numberOfProject_le = QtGui.QLineEdit()
        self.numberOfProject_le.setPlaceholderText("Enter Number Here...")

        # Validator in QtGui
        validator = QtGui.QDoubleValidator()
        validator.setDecimals(2)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        self.numberOfProject_le.setValidator(validator)

        self.actionButtonWidget = QtGui.QWidget()
        self.actionButtonWidget.setLayout(QtGui.QVBoxLayout())

        self.addProject = QtGui.QPushButton("Create Project")        
        self.copySourceAssetPath_bttn = QtGui.QPushButton("Copy Project Path")

        #==============================================================================
        # PYQT Widget Assignments
        #==============================================================================

        self.projectWidget.layout().layout().addWidget(projectName_lbl)
        self.projectWidget.layout().layout().addWidget(self.orlando_radioBtn)
        self.projectWidget.layout().layout().addWidget(projectOr_lbl)
        self.projectWidget.layout().layout().addWidget(self.tampa_radioBtn)        

        self.addDeleteWidget = QtGui.QWidget()
        self.addDeleteWidget.setLayout(QtGui.QHBoxLayout())

        self.addDeleteWidget.layout().layout().addWidget(self.addProject)

        self.projectYearWidget.layout().layout().addWidget(projectYear_lbl)
        self.projectYearWidget.layout().layout().addWidget(self.projectYear_comboBox)

        self.projectNumberWidget.layout().layout().addWidget(projectNumber_lbl)
        self.projectNumberWidget.layout().layout().addWidget(self.numberOfProject_le)

        self.actionButtonWidget.layout().layout().addWidget(self.projectYearWidget)
        self.actionButtonWidget.layout().layout().addWidget(self.projectNumberWidget)
        self.actionButtonWidget.layout().layout().addWidget(self.addDeleteWidget)
        self.actionButtonWidget.layout().layout().addWidget(self.copySourceAssetPath_bttn)
        
        # adds project widget and tools widget to central widget
        self.centralWidget.layout().addWidget(self.projectWidget)
        self.centralWidget.layout().addWidget(self.actionButtonWidget)

        # sets central widget for PyQt window
        self.setCentralWidget(self.centralWidget)

        #==============================================================================
        # PYQT Execution Connections
        #==============================================================================

        # triggers for buttons
        self.addProject.clicked.connect(lambda: self.createProject())
        self.copySourceAssetPath_bttn.clicked.connect(lambda: self.copyProjectPath())

        # toggle trigger for orlando_radioBtn which connects to function that is used by both radio buttons
        self.orlando_radioBtn.toggled.connect(lambda: self.checkRadioButtonState())

    def checkRadioButtonState(self):
        """
        Function to check state of radio buttons to determine which studio to use
        Only needs to be called by one of the radio buttons since it sets the value for both
        """
        
        if self.orlando_radioBtn.isChecked():
            self.tampa_radioBtn.setChecked(False)

            self.projectTargetLocation = self.orlandoJobsLocation
            #self.popupOkWindow(self.orlandoJobsLocation)

        elif self.tampa_radioBtn.isChecked():
            self.orlando_radioBtn.setChecked(False)

            self.projectTargetLocation = self.tampaJobsLocation
            #self.popupOkWindow(self.tampaJobsLocation)        

    def openExplorerWindow(self, path):
        """ Function to open a windows explorer window """
        
        if self.osPath(path):
            os.startfile(path)
        else:
            self.popupOkWindow("PATH DOESN'T EXIST")

    def copyProjectPath(self):
        """ Adds current project path to clipboard """

        # if project number line edit is not empty
        if self.numberOfProject_le.text():
            
            # creates variable of target path
            path = str(self.projectTargetLocation) + "\\" + str(self.projectYear_comboBox.currentText()) + "\\" + \
                str(self.numberOfProject_le.text())
            
            # if path is valid, copies string of path to clipboard
            if self.osPath(path):

                clipboard = QtGui.QApplication.clipboard()
                clipboard.clear()
                clipboard.setText(path)

                self.popupOkWindow(path + "\n" + "was copied to your clipboard")
            else:
                self.popupOkWindow("PATH DOESN'T EXIST")
        else:
            self.popupOkWindow("PATH WAS NOT ENTERED")

    def loadJSONConfig(self, configFile):
        """ Loads the JSON file that defines project structure """

        with open(configFile) as data_file:

            # try to load json data and if possible return it otherwise generate error window
            try:
                configData = json.load(data_file)
                return configData
            except:
                self.popupOkWindow("Error with JSON File")

    def popupOkWindow(self, message):
        """ Generic popup window with an OK button and can display message based on use """

        popupWindow = QtGui.QMessageBox()
        
        popupWindow.setText(str(message))
        popupWindow.setStandardButtons(QtGui.QMessageBox.Ok)

        popupWindow.exec_()

    #function to create window to 
    def createProject(self):
        """ Function to create folder structure """

        #runs some if else statements to check what was clicked since buttons were set to checkable
        #if create_btn.isChecked():
        #if preRendered_radioBtn.isChecked() or realTime_radioBtn.isChecked():
        if not self.numberOfProject_le.text() == "":
            
            # creates variable of target path
            newPath = str(self.projectTargetLocation) + "\\" + str(self.projectYear_comboBox.currentText()) + \
                "\\" + str(self.numberOfProject_le.text())
            
            #if path does not exist, the directory will be created based on JSON folder structure
            if not os.path.exists(newPath):
                
                try:

                    #load JSON as dictionary into variable
                    JSON = self.loadJSONConfig(self.defaultConfig)
                    
                    os.mkdir(newPath)

                    #iterate over dictionary to create structure
                    for key, value in JSON["BBA Structure"].iteritems():
                        #print key

                        os.mkdir(newPath + "\\" + str(key))
                        for item in value:
                            #print item

                            os.mkdir(newPath + "\\" + str(key) + "\\" + str(item))                        
                    
                    self.popupOkWindow("Successfully Created Structure For: " + str(self.numberOfProject_le.text()))
                    
                except:
                    self.popupOkWindow("AN ERROR OCCURED WHEN MAKING THE FOLDER STRUCTURE")
            else:
                self.popupOkWindow("PATH EXISTS")
        else:
            self.popupOkWindow("NAME WASN'T ENTERED")

    def getPath(self, filePath):
        """ Get list of directories if path exists """

        if self.osPath(filePath): 
            return os.listdir(filePath)
    
    def osPath(self, filePath):
        """ Determines if path exists """

        if os.path.isdir(filePath):
            return True
        else:
            return False

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWidget = Main()
    myWidget.show()
    sys.exit(app.exec_())
