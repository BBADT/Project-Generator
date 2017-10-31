"""
#!/usr/bin/env python
#title           :CreateJointAtPivot.py
#description     :Script used to automate project folder creation
#author          :Doug Halley
#date            :20171031
#version         :1.0
#usage           :In Maya CreateJointAtPivot.CreateJointAtPivot()
#notes           :
#python_version  :2.7.14
#pyqt_version    :4.11.4
#==============================================================================
"""

import os
import sys
import stat
import json
import shutil
import datetime
import pyperclip

from functools import partial

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

        #window title
        self.setWindowTitle("BBA Project Generator")  

        #os.path.realpath(__file__) -  gets path of the current file
        self.scriptLocation = os.path.dirname(os.path.realpath(__file__))
        self.defaultConfig = self.scriptLocation + "\\" + "config.json"
        self.setWindowIcon(QtGui.QIcon(self.scriptLocation + "\\" + "bbalogo.ico"))

        #initlizes string to be used
        #initilized to use Orlando Project Drive
        self.projectTargetLocation = "\\\\FB2\\BBA_Jobs"
        self.orlandoJobsLocation = "\\\\FB2\\BBA_Jobs"
        self.tampaJobsLocation = "\\\\BBA-Tampa\\Tampajobs"

        #==============================================================================
        # PYQT Widget Defintions
        #==============================================================================        

        #main widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(QtGui.QVBoxLayout())

        #widget for project location radio buttons and year combobox
        self.projectWidget = QtGui.QWidget()
        self.projectWidget.setLayout(QtGui.QHBoxLayout())

        projectName_lbl = QtGui.QLabel("Create Project for")

        #widget for radio buttons to choose studio location
        #set as a vertical layout to conserve space in UI
        self.studioLocationWidget = QtGui.QWidget()
        self.studioLocationWidget.setLayout(QtGui.QVBoxLayout())

        self.orlando_radioBtn = QtGui.QRadioButton("Orlando")
        self.tampa_radioBtn = QtGui.QRadioButton("Tampa")

        # set self.orlando_radioBtn to be true
        self.orlando_radioBtn.setChecked(True)

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

        searchProjectName_lbl = QtGui.QLabel("Enter Project Number ")
        self.nameOfProject_le = QtGui.QLineEdit()
        self.nameOfProject_le.setPlaceholderText("Enter Number Here...")

        projectNameDot_lbl = QtGui.QLabel(".")
        self.projectDecimals_le = QtGui.QLineEdit("00")

        #Validator in QtGui
        doubleValidator = QtGui.QDoubleValidator()
        doubleValidator.setDecimals(2)
        doubleValidator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        self.nameOfProject_le.setValidator(doubleValidator)

        #defined width to limit size of lineEdit for decimal place
        width = self.projectDecimals_le.fontMetrics().boundingRect("00").width() + 10
        self.projectDecimals_le.setMaximumWidth(width)

        self.actionButtonWidget = QtGui.QWidget()
        self.actionButtonWidget.setLayout(QtGui.QVBoxLayout())

        self.addProject = QtGui.QPushButton("Add Project")        
        self.copySourceAssetPath_bttn = QtGui.QPushButton("Copy Project Path")

        #==============================================================================
        # PYQT Widget Assignments
        #==============================================================================

        self.studioLocationWidget.layout().layout().addWidget(self.orlando_radioBtn)
        self.studioLocationWidget.layout().layout().addWidget(self.tampa_radioBtn)

        self.projectWidget.layout().layout().addWidget(projectName_lbl)
        self.projectWidget.layout().layout().addWidget(self.studioLocationWidget)
        self.projectWidget.layout().layout().addWidget(self.projectYear_comboBox)

        self.addDeleteWidget = QtGui.QWidget()
        self.addDeleteWidget.setLayout(QtGui.QHBoxLayout())

        self.addDeleteWidget.layout().layout().addWidget(self.addProject)

        self.projectNumberWidget.layout().layout().addWidget(searchProjectName_lbl)
        self.projectNumberWidget.layout().layout().addWidget(self.nameOfProject_le)
        self.projectNumberWidget.layout().layout().addWidget(projectNameDot_lbl)
        self.projectNumberWidget.layout().layout().addWidget(self.projectDecimals_le)

        self.actionButtonWidget.layout().layout().addWidget(self.projectNumberWidget)
        self.actionButtonWidget.layout().layout().addWidget(self.addDeleteWidget)
        self.actionButtonWidget.layout().layout().addWidget(self.copySourceAssetPath_bttn)
        
        #adds project widget and tools widget to central widget
        self.centralWidget.layout().addWidget(self.projectWidget)
        self.centralWidget.layout().addWidget(self.actionButtonWidget)

        #sets central widget for PyQt window
        self.setCentralWidget(self.centralWidget)

        #==============================================================================
        # PYQT Execution Connections
        #==============================================================================

        self.addProject.clicked.connect(lambda: self.createProject())
        self.copySourceAssetPath_bttn.clicked.connect(lambda: self.copyProjectPath())

        self.projectYear_comboBox.currentIndexChanged.connect(lambda: self.fillProjectComboBox(self.project_comboBox, (str(self.orlandoJobsLocation) + "\\" + str(self.projectYear_comboBox.currentText()))))
        self.projectYear_comboBox.currentIndexChanged.connect(lambda: self.createCompleter(self.nameOfProject_le))

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
        if self.nameOfProject_le.text():
            
            # creates variable of target path
            path = str(self.projectTargetLocation) + "\\" + str(
                self.projectYear_comboBox.currentText()) + "\\" + str(self.nameOfProject_le.text()) + "." + \
                str(self.projectDecimals_le.text())
            
            # if path is valid, copies string of path to clipboard
            if self.osPath(path):
                pyperclip.copy(str(path))

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
    
    def checkLineEditState(self, lineEdit):
        """ Function used to create color feedback based on correct input into tool """

        sender = lineEdit
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]

        if state == QtGui.QValidator.Acceptable:
            fontColor = '#000000' # black
            bgColor = '#c4df9b' # green
            sender.setStyleSheet('QlineEdit { color: %s; background-color: %s }' % (fontColor, bgColor))
        elif sender.text() == "":
            sender.setStyleSheet('')

    #function to create window to 
    def createProject(self):
        """ Function to create folder structure """

        #runs some if else statements to check what was clicked since buttons were set to checkable
        #if create_btn.isChecked():
        #if preRendered_radioBtn.isChecked() or realTime_radioBtn.isChecked():
        if not self.nameOfProject_le.text() == "":
            
            # creates variable of target path
            newPath = self.projectTargetLocation + "\\" + self.projectYear_comboBox.currentText() + \
                "\\" + str(self.nameOfProject_le.text()) + "." + \
                str(self.projectDecimals_le.text())
            
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
                    
                    self.popupOkWindow("Successfully Created Structure For: " + str(self.nameOfProject_le.text()))
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
