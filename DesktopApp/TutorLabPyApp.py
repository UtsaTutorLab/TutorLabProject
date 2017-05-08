# -*- coding: utf-8 -*-
# Author: Koby Huckabee CS 2017
#

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal, pyqtSlot
import ctypes, getpass, json, os, requests, socket, sys, threading, time

# for purpose of this app and testing i am using the secret key from the website
# and checking if they are the same on the site. 
# For production should create a special secret key, probably a sha256 of some string?
APP_KEY = "cdyna7f^!8c=#$-#nw5@j&$7ig-)li8@53$-=z78vccn0b+(y#"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TutorLab(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(Ui_TutorLab, self).__init__(*args, **kwargs)
        self.setupUi(self)

    def closeEvent(self,event):
        '''
        Overwrites the apps current close method.\n
        closeEvent will check what page the app is on an display a corresponding confirmation to the user.\n
        This will also call corresponding delete functions to update website. \ni.e. cancel_request() and delete_survey()
        '''
        idx = self.stackedWidget.currentIndex()
        if idx == 1:
            message = "Are you sure you want to exit?\nYou will be removed from the queue."
        elif idx == 3:
            message = "Are you sure you want to exit?\nYour survey will not be sent.\nWe'd really like your feed back!"
        else:
            message = "Are you sure you want to exit?\nYou won't get to tell us how we did."
        if idx >= 1 and idx < 4:
            result = QtGui.QMessageBox.question(self,
                        "Confirm Exit...",
                        message, 
                        QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
            event.ignore()

            if result == QtGui.QMessageBox.Yes:
                if idx == 1:
                    self.cancel_request()
                if idx == 3:
                    self.delete_survey()
                event.accept()

    def setupUi(self, TutorLab): 
        '''
        setupUi is a standard function used by PyQt4 to initialize the apps layouts, lables, and names.\n
        Calls get_address() and actions()
        '''
        TutorLab.setObjectName(_fromUtf8("TutorLab"))
        TutorLab.setEnabled(True)
        
        self.gridLayout = QtGui.QGridLayout(TutorLab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.stackedWidget = QtGui.QStackedWidget(TutorLab)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.home = QtGui.QWidget()
        self.home.setObjectName(_fromUtf8("home"))
        self.gridLayout_2 = QtGui.QGridLayout(self.home)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.line_5 = QtGui.QFrame(self.home)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_2.addWidget(self.line_5, 8, 0, 1, 1)
        self.chairDrop = QtGui.QComboBox(self.home)
        self.chairDrop.setObjectName(_fromUtf8("chairDrop"))
        self.chairDrop.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.chairDrop.setMaxVisibleItems(10)
        self.gridLayout_2.addWidget(self.chairDrop, 11, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.home)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 15, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 19, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.home)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 12, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.home)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 7, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.line_4 = QtGui.QFrame(self.home)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_2.addWidget(self.line_4, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 22, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.home)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 6, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.line_3 = QtGui.QFrame(self.home)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 23, 0, 1, 1)
        self.classDrop = QtGui.QComboBox(self.home)
        self.classDrop.setObjectName(_fromUtf8("classDrop"))
        self.classDrop.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.classDrop.setMaxVisibleItems(10)
        self.classDrop.setEnabled(False) 
        self.gridLayout_2.addWidget(self.classDrop, 16, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 13, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.home)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 20, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.questionDrop = QtGui.QComboBox(self.home)
        self.questionDrop.setObjectName(_fromUtf8("questionDrop"))
        self.questionDrop.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.questionDrop.setMaxVisibleItems(10)
        self.questionDrop.setEnabled(False)
        self.gridLayout_2.addWidget(self.questionDrop, 21, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.home)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 10, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 9, 0, 1, 1)
        self.studentNameLabel = QtGui.QLabel(self.home)
        self.studentNameLabel.setEnabled(True)
        self.studentNameLabel.setText(_fromUtf8(""))
        self.studentNameLabel.setObjectName(_fromUtf8("studentNameLabel"))
        self.gridLayout_2.addWidget(self.studentNameLabel, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.sendRequest = QtGui.QPushButton(self.home)
        self.sendRequest.setObjectName(_fromUtf8("sendRequest"))
        self.gridLayout_2.addWidget(self.sendRequest, 24, 0, 1, 1)
        self.label = QtGui.QLabel(self.home)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.line = QtGui.QFrame(self.home)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 18, 0, 1, 1)
        self.studentFullName = QtGui.QLineEdit(self.home)
        self.studentFullName.setText(_fromUtf8(""))
        self.studentFullName.setMaxLength(70)
        self.studentFullName.setObjectName(_fromUtf8("studentFullName"))
        self.gridLayout_2.addWidget(self.studentFullName, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.home)
        self.in_queue = QtGui.QWidget()
        self.in_queue.setObjectName(_fromUtf8("in_queue"))
        self.gridLayout_3 = QtGui.QGridLayout(self.in_queue)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.in_queue)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 4, 0, 1, 1)
        self.cancelRequest = QtGui.QPushButton(self.in_queue)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.cancelRequest.setFont(font)
        self.cancelRequest.setObjectName(_fromUtf8("cancelRequest"))
        self.gridLayout_3.addWidget(self.cancelRequest, 7, 0, 1, 2)
        self.queueMessage = QtGui.QLabel(self.in_queue)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.queueMessage.setFont(font)
        self.queueMessage.setObjectName(_fromUtf8("queueMessage"))
        self.gridLayout_3.addWidget(self.queueMessage, 3, 0, 1, 2, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 0, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem6, 2, 0, 1, 1)
        self.queueNum = QtGui.QLabel(self.in_queue)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.queueNum.setFont(font)
        self.queueNum.setObjectName(_fromUtf8("queueNum"))
        self.gridLayout_3.addWidget(self.queueNum, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.in_queue)
        self.in_session = QtGui.QWidget()
        self.in_session.setObjectName(_fromUtf8("in_session"))
        self.gridLayout_4 = QtGui.QGridLayout(self.in_session)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_8 = QtGui.QLabel(self.in_session)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem7, 2, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.in_session)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem8, 0, 0, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem9, 4, 0, 1, 1)
        self.stackedWidget.addWidget(self.in_session)
        self.survey = QtGui.QWidget()
        self.survey.setObjectName(_fromUtf8("survey"))
        self.gridLayout_5 = QtGui.QGridLayout(self.survey)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.surveyProgressBar = QtGui.QProgressBar(self.survey)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.surveyProgressBar.setFont(font)
        self.surveyProgressBar.setProperty("value", 0)
        self.surveyProgressBar.setObjectName(_fromUtf8("surveyProgressBar"))
        self.gridLayout_5.addWidget(self.surveyProgressBar, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.survey)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_11 = QtGui.QLabel(self.survey)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_5.addWidget(self.label_11, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.surveyStackedWidget = QtGui.QStackedWidget(self.survey)
        self.surveyStackedWidget.setObjectName(_fromUtf8("surveyStackedWidget"))
        self.gridLayout_5.addWidget(self.surveyStackedWidget, 4, 0, 1, 1)
        self.stackedWidget.addWidget(self.survey)
        self.thankYou = QtGui.QWidget()
        self.thankYou.setObjectName(_fromUtf8("thankYou"))
        self.gridLayout_11 = QtGui.QGridLayout(self.thankYou)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.label_12 = QtGui.QLabel(self.thankYou)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_11.addWidget(self.label_12, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.stackedWidget.addWidget(self.thankYou)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.retranslateUi(TutorLab)
        self.stackedWidget.setCurrentIndex(0)
        self.surveyStackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TutorLab)

        self.get_address() #FOR TESTING!! REMOVE WHEN WE GET STATIC ADDRESS
        # CHANGE THE IP HOST IN SITE SETTINGS

        # self.address = 'tutorlab.cs.utsarr.net'

        self.actions()

    def retranslateUi(self, TutorLab):
        '''
        retranslateUi ia a standard function PyQt4 uses.\n
        It sets the text for the lables in all pages of the app.
        '''
        TutorLab.setWindowTitle(_translate("TutorLab", "TutorLab", None))
        self.label_5.setText(_translate("TutorLab", "Class you need assistance in", None))
        self.label_3.setText(_translate("TutorLab", "abc123", None))
        self.label_2.setText(_translate("TutorLab", "abc123", None))
        self.label_6.setText(_translate("TutorLab", "Issue or Problem", None))
        self.label_7.setText(_translate("TutorLab", "Chair Number", None))
        self.sendRequest.setText(_translate("TutorLab", "Request", None))
        self.label.setText(_translate("TutorLab", "Student Name", None))
        self.studentFullName.setPlaceholderText(_translate("TutorLab", "First and Last Name ", None))
        self.label_4.setText(_translate("TutorLab", "Queue Position:", None))
        self.cancelRequest.setText(_translate("TutorLab", "Cancel Request", None))
        self.queueMessage.setText(_translate("TutorLab", "We will be right with you!", None))
        self.queueMessage.setWordWrap(True)
        self.queueMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.queueNum.setText(_translate("TutorLab", "#", None))
        self.label_8.setText(_translate("TutorLab", "In Session", None))
        self.label_8.setWordWrap(True)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setText(_translate("TutorLab", "Please keep this window open!", None))
        self.label_9.setWordWrap(True)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setText(_translate("TutorLab", "Survey", None))
        self.label_11.setText(_translate("TutorLab", "Progress", None))
        self.label_12.setText(_translate("TutorLab", "Thank You for your feedback!", None))
        self.label_12.setWordWrap(True)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)

    def get_address(self):
        '''
        This sets the IP address the app will use to communicate with the website.
        Also used for testing to quickly change IP if needed
        '''

        self.address = "10.100.126.10"
        #self.address = "127.0.0.1:8000"


        # text, ok = QtGui.QInputDialog.getText(self,'Address Input', 'Enter IP address:')
        
        # if ok:
        #     self.address = str(text)
        

    def actions(self):
        '''
        No return\n
        Sets up the buttons and dropdowns in the GUI.
        '''
        # get file for student name 
        try:
            prefix = '.' if os.name != 'nt' else ''
            nameFile = open(prefix+"studentname.txt", "r")
            for line in nameFile:
                self.studentName = line
            self.studentNameLabel.setText(_translate("TutorLab", self.studentName, None))
            self.studentFullName.hide()
            nameFile.close()
            self.isfile = True
        except:
            self.isfile = False

        # get student abc123
        try:
            getuser = getpass.getuser()
            self.abc123 = getuser[:6]
            # self.abc123 = "pur489"
        except: 
            self.abc123 = "abc123"

        # set up dropdowns
        chairNum = ["---Select Chair---"]
        for x in range(1,51):
            if os.name != 'nt':
                chairNum.append("Linux "+str(x))
            else:
                chairNum.append("VDI "+str(x))

        self.chairDrop.addItems(chairNum)

        self.chairDrop.currentIndexChanged.connect(self.set_classes)

        self.classDrop.currentIndexChanged.connect(self.set_issue_list)

        self.ans_set = []

        # connect buttons
        self.label_3.setText(_translate("TutorLab", self.abc123, None))
        self.sendRequest.clicked.connect(self.send_request)
        self.cancelRequest.clicked.connect(self.cancel_request)

        # runs local server thread
        self.run_thread()

    def set_classes(self):
        '''
        Checks if a chair is selected, fetches the class list, sets it and enables the class list dropdown.
        '''
        self.classDrop.clear()
        if self.chairDrop.currentIndex() > 0:
            classes = self.get_classes()
            for c in classes:
                s = c[0]
                d = int(c[1])
                self.classDrop.addItem(s, d)
            self.classDrop.setEnabled(True)
        else:
            self.classDrop.setEnabled(False)
        


    def set_issue_list(self):
        '''
        Checks if a class is selected, fetches the issue list, sets it and enables the issue list dropdown.
        '''
        self.questionDrop.clear()
        if self.classDrop.currentIndex() > 0:
            self.questionDrop.addItems(self.get_issue_list())
            self.questionDrop.setEnabled(True)
        else:
            self.questionDrop.setEnabled(False)

    @pyqtSlot()
    def set_position(self):
        '''
        Slot used to get signal from server thread to update student position text in main thread.
        '''
        # set queue position text
        self.queueNum.setText(_translate("TutorLab", self.serverThread.position, None))
    
   
    @pyqtSlot()
    def set_questions(self):
        '''
        Slot used to get signal from server thread to set the question widget in main thread.
        '''
        # init question page content
        self.question = {}
        self.questionGridLayout = {}
        self.questionSpacerItem = {}
        self.questionText = {}
        self.nextQuestion = {}
        self.rangeLayout = {}
        self.scaleLayout = {}
        self.radioButton = {}
        self.questionLow = {}
        self.questionHigh = {}

        for ndx, q in enumerate(self.serverThread.questions):
            self.create_question_page(ndx, q)
        self.create_comment_page()

    def create_question_page(self, ndx, q):
        '''
        Parameters: ndx - question index number
                    q - question text
        This method will create a single survey page widget and add it to the survey_stackedwidget
        '''
        start = ndx*5
        end = (ndx+1)*5

        self.question[ndx] = QtGui.QWidget()
        self.question[ndx].setObjectName(_fromUtf8("question_"+str(ndx)))
        self.questionGridLayout[6+ndx] = QtGui.QGridLayout(self.question[ndx])
        self.questionGridLayout[6+ndx].setObjectName(_fromUtf8("gridLayout_"+str((6+ndx))))
        self.questionSpacerItem[start+1] = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.questionGridLayout[6+ndx].addItem(self.questionSpacerItem[start+1], 6, 0, 1, 1)
        self.questionSpacerItem[start+2] = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.questionGridLayout[6+ndx].addItem(self.questionSpacerItem[start+2], 1, 0, 1, 1)
        self.nextQuestion[ndx] = QtGui.QPushButton(self.question[ndx])
        self.nextQuestion[ndx].setObjectName(_fromUtf8("nextQuestion_"+str(ndx)))
        self.questionGridLayout[6+ndx].addWidget(self.nextQuestion[ndx], 7, 0, 1, 1)
        self.rangeLayout[ndx] = QtGui.QHBoxLayout()
        self.rangeLayout[ndx].setObjectName(_fromUtf8("rangeLayout_"+str(ndx)))
        self.scaleLayout[ndx] = QtGui.QHBoxLayout()
        self.scaleLayout[ndx].setObjectName(_fromUtf8("scaleLayout_"+str(ndx)))

        # set up radio buttons
        for idx, x in enumerate(range(start,end)):
            self.radioButton[x] = QtGui.QRadioButton(self.question[ndx])
            self.radioButton[x].setObjectName(_fromUtf8("radioButton"+str(x)))
            self.rangeLayout[ndx].addWidget(self.radioButton[x], QtCore.Qt.AlignHCenter)
            self.radioButton[x].setText(_translate("TutorLab", str(idx+1), None))

        # set up scale lables
        self.questionLow[ndx] = QtGui.QLabel(self.question[ndx])
        self.questionLow[ndx].setObjectName(_fromUtf8("questionLow"+str(ndx)))
        self.questionLow[ndx].setWordWrap(True)
        self.scaleLayout[ndx].addWidget(self.questionLow[ndx], QtCore.Qt.AlignLeft)
        self.questionLow[ndx].setText(_translate("TutorLab", q[1], None))

        self.questionHigh[ndx] = QtGui.QLabel(self.question[ndx])
        self.questionHigh[ndx].setObjectName(_fromUtf8("questionHigh"+str(ndx)))
        self.questionHigh[ndx].setWordWrap(True)
        self.scaleLayout[ndx].addWidget(self.questionHigh[ndx])
        self.questionHigh[ndx].setText(_translate("TutorLab", q[2], None))

        # add to layout
        self.questionGridLayout[6+ndx].addLayout(self.rangeLayout[ndx], 4, 0, 1, 1)
        self.questionGridLayout[6+ndx].addLayout(self.scaleLayout[ndx], 5, 0, 1, 1)
        self.questionSpacerItem[start+3] = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.questionGridLayout[6+ndx].addItem(self.questionSpacerItem[start+3], 3, 0, 1, 1)
        self.questionText[ndx] = QtGui.QLabel(self.question[ndx])
        self.questionText[ndx].setAlignment(QtCore.Qt.AlignCenter)
        self.questionText[ndx].setWordWrap(True)
        self.questionText[ndx].setObjectName(_fromUtf8("questionText"+str(ndx)))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.questionText[ndx].setFont(font)
        self.questionGridLayout[6+ndx].addWidget(self.questionText[ndx], 2, 0, 1, 1)
        self.surveyStackedWidget.addWidget(self.question[ndx])

        # set labels and connect buttons
        self.nextQuestion[ndx].setText(_translate("TutorLab", "Next", None))
        self.nextQuestion[ndx].clicked.connect(self.get_answer)            

        # sets each question text
        self.questionText[ndx].setText(_translate("TutorLab", q[0], None))

    def create_comment_page(self):
        '''
        This will create the last page on the survey_stackedwidget for comments and to submit the survey
        '''
        self.comment_page = QtGui.QWidget()
        self.comment_page.setObjectName(_fromUtf8("comment_page"))
        self.gridLayout_12 = QtGui.QGridLayout(self.comment_page)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.comments = QtGui.QTextEdit(self.comment_page)
        self.comments.setObjectName(_fromUtf8("comments"))
        self.gridLayout_12.addWidget(self.comments, 2, 0, 1, 1)
        spacerItem25 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem25, 3, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.comment_page)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_12.addWidget(self.label_14, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        spacerItem26 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem26, 0, 0, 1, 1)
        self.submitSurvey = QtGui.QPushButton(self.comment_page)
        self.submitSurvey.setObjectName(_fromUtf8("submitSurvey"))
        self.gridLayout_12.addWidget(self.submitSurvey, 4, 0, 1, 1)
        self.surveyStackedWidget.addWidget(self.comment_page)
        self.label_14.setText(_translate("TutorLab", "Comments:", None))
        self.submitSurvey.setText(_translate("TutorLab", "Submit", None))
        self.submitSurvey.clicked.connect(self.submit_survey)

    def run_thread(self):
        '''
        Runs the server thread in the background.
        '''
        self.serverThread = StartServerThread(self)
        self.serverThread.daemon = True
        self.serverThread.start()


   
    def show_message(self, title, text, message):
        '''
        Displays message box for given title, text, and message.
        '''
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()


    def get_answer(self):
        '''
        Gets the current survey question answer from the user and stores in the array "self.ans_set"\n
        Then updates progress bar and goes to next question.
        '''
        ndx = self.surveyStackedWidget.currentIndex()
        start = ndx*5
        end = (ndx+1)*5
        for x in range(start, end):
            if self.radioButton[x].isChecked():
                self.ans_set.append(self.questionText[ndx].text() + " = " + str(self.radioButton[x].text()))
                self.__next_survey_page()
                self.surveyProgressBar.setProperty("value", (ndx+1)*20)

    
    @pyqtSlot()
    def next_page(self):
        '''
        Changes stackedWidget page to next index.\n
        Also used as a Slot to get a signal from server thread. 
        '''
        idx = self.stackedWidget.currentIndex()
        if idx < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(idx + 1)
        else:
            self.stackedWidget.setCurrentIndex(0)
        if idx == 2:
            TutorLab.resize(399, 499)
            

    def __next_survey_page(self):
        '''
        Changes surveyStackedWidget page to next index
        '''
        idx = self.surveyStackedWidget.currentIndex()
        if idx < self.surveyStackedWidget.count() - 1:
            self.surveyStackedWidget.setCurrentIndex(idx + 1)
        else:
            self.next_page()



#--------Http request functions-------#
    def get_classes(self):
        '''
        Returns array of strings of classes\n
        Sends Http request to get list of pairs of class id's and class names
        '''
        try:
            URL = 'http://' + self.address + '/student/api/get-classes/' #to be changed to static address later
            data = {
                'abc123':self.abc123,
            }
            r = requests.get(URL, params=data)
            response = r.json()
            return response
        except:
            self.show_message(
                "Request Error",
                "Could not connect to the site",
                "There was an error connecting to the site, can not get classes"
            )

    def get_issue_list(self):
        '''
        Returns array of issue strings\n
        Sends Http request to get list of issues and questions
        '''
        try:
            URL = 'http://' + self.address + '/student/api/get-issue-list/'
            data = {
                'course': self.classDrop.itemData(self.classDrop.currentIndex())
            }
            r = requests.get(URL, params=data)
            response = r.json()
            return(response)
        except:
            self.show_message(
                "Request Error", 
                "Could not connect to the site", 
                "There was an error connecting to the site, can not get issues"
            )
    
    def send_request(self):
        '''
        Error checks the dropdowns to make sure info is selected\n
        Sends a http request to the website which will return a json response with the structure {bool:x, num:y}\n
        otherwise, show an error message
        '''
        if not self.isfile:
            if not self.studentFullName.text():
                self.show_message("Check again", "Some fields are missing",  "Full name required")
            # no name file, write name to new file
            else:
                if os.name != 'nt':
                    prefix = '.' 
                else:
                    prefix = ''
                self.nameFile = open(prefix+"studentname.txt", "w")
                self.studentName = self.studentFullName.text().strip()
                self.nameFile.write(self.studentName)
                self.nameFile.close()
                self.isfile = True

        if self.chairDrop.currentIndex() <= 0:
            self.show_message("Check again", "Some fields are missing", "Chair number is required")
        elif self.classDrop.currentIndex() <= 0:
            self.show_message("Check again", "Some fields are missing", "Class number is required")
        elif self.questionDrop.currentIndex() <= 0:
            self.show_message("Check again", "Some fields are missing", "Issue is required")
        else:
            r = ""
            try:
                URL = 'http://' + self.address + '/student/api/post-request/' #to be changed to static address later
                data = {'app_key': APP_KEY,
                        'fullname':self.studentName,
                        'abc123':self.abc123,
                        'chairNumber': self.chairDrop.currentText(),
                        'className': self.classDrop.currentText(),
                        'classId': self.classDrop.itemData(self.classDrop.currentIndex()),
                        'question': self.questionDrop.currentText(),
                        'host':self.serverThread.host,
                        'port':self.serverThread.port
                        }
                r = requests.post(URL, data=data)
                response = r.json()
                if response['bool'] == 'True':
                    self.next_page()
                    self.queueNum.setText(_translate("TutorLab", str(response['num']), None))
                else:
                    self.show_message("Already in Queue", "Could not add you to the Queue", "You are already in the queue, if you feel this is incorrect plesase let us know, otherwise we will be with you shortly.")
            except:
                self.show_message("Error", "Error connecting to website", "Request could not be sent")


    def cancel_request(self):
        '''
        Sends http request to the website to cancel request\n
        returns json response with structure {bool:x}
        '''
        try:
            URL = 'http://' + self.address + '/student/api/cancel-request/' #to be changed to static address later/'
            data = {'app_key': APP_KEY,
                    'abc123':self.abc123,
                    }
            r = requests.post(URL, data=data)
            response = r.json()
            if response['bool'] == 'true':
                QtGui.QApplication.quit()
            else:
                self.show_message("Error", "Can not remove you from the queue", response['message'])
        except:
            self.show_message("Error", "Can not remove you from the queue", "There seems to be an error on our end")
        

    def submit_survey(self):
        '''
        Sends http request to submit survey questions, answers, and comment/n
        Returns a json response with the structure {bool:x, message:y}
        '''
        self.ans_set.append(self.comments.toPlainText())
        try:
            URL = 'http://' + self.address + '/student/api/submit-survey/' #to be changed to static address later
            data = {'app_key': APP_KEY,
                    'survey_token':self.serverThread.surveyToken,
                    'ans1':self.ans_set[0],
                    'ans2':self.ans_set[1],
                    'ans3':self.ans_set[2],
                    'ans4':self.ans_set[3],
                    'ans5':self.ans_set[4],
                    'comment':self.ans_set[5],
                    }
            r = requests.post(URL, data=data)
            response = r.json()
            if response['bool'] == 'True':
                self.next_page()
            else:
                self.show_message("Error", "Error connecting to website", response['message'])
        except:
            self.show_message("Error", "Error connecting to website", "Survey could not be sent")

    def delete_survey(self):
        '''
        Sends http request to submit survey questions, answers, and comment/n
        Returns a json response with the structure {bool:x, message:y}
        '''
        try:
            URL = 'http://' + self.address + '/student/api/delete-survey/' #to be changed to static address later
            data = {
                'app_key': APP_KEY,
                'survey_token':self.serverThread.surveyToken,
            }
            r = requests.post(URL, data=data)
            response = r.json()
            if response['bool'] != 'True':
                self.show_message("Error", "Error connecting to website", response['message'])
        except:
            self.show_message("Error", "Error connecting to website", "Survey could not be sent")


#---------SERVER THREAD CLASS---------#

class StartServerThread(QtCore.QThread):
    '''
    The application creates a server that the website can reach it at.
    It creates a server using the localhost and the first free port. From there it will wait and listen for the site to send data.
    This data is in a json format, the most important data is the 'APP_KEY' and the 'bool' fields.
    These verify that the connection is only coming from the site.
    '''
    def __init__(self, Ui_TutorLab):
        QtCore.QThread.__init__(self)
        self.sigs = appSignals()
        self.sigs.pageSignal.connect(Ui_TutorLab.next_page)
        self.sigs.positionSignal.connect(Ui_TutorLab.set_position)
        self.sigs.questionSignal.connect(Ui_TutorLab.set_questions)

    def run(self):
        '''
        '''        
        # create a socket object
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        if os.name == "nt":  # For windows
            self.host = socket.gethostbyname(socket.gethostname())
        else: # For linux
            import netifaces as ni
            ni.ifaddresses('eth0')
            ip = ni.ifaddresses('eth0')[2][0]['addr']
            self.host = ip

        # used for testing on mac
        #self.host = socket.gethostbyname(socket.gethostname())

        # bind to the port
        serversocket.bind((self.host, 0))                                 

        # save selected port number
        self.port = serversocket.getsockname()[1]   

        # queue 1 request
        serversocket.listen(1)     

        created = False                                      
        while True:
            # establish a connection
            clientsocket,addr = serversocket.accept()
            
            # send connection msg with APP_KEY
            msg={'app_key':APP_KEY, 'message':"Connection test"}
            clientsocket.send(json.dumps(msg).encode('ascii'))
            
            # wait to recieve a message from site
            get = clientsocket.recv(1024)
            getmsg = json.loads(get.decode('ascii'))

            try:    
                if getmsg['app_key'] != APP_KEY:
                    # print('App Key does not match, closing connection')
                    clientsocket.close()
                if getmsg['bool'] == "False":
                    clientsocket.close()
                if getmsg['message'] == "queue update":
                    self.position = str(getmsg['position'])
                    self.sigs.updatePositionSignal()
                elif getmsg['message'] == "in session":
                    if created: # STUDENT IN SESSION
                        self.sigs.changePageSignal()
                    else: # STUDENT ADDED TO QUEUE
                        created = True
                elif getmsg['message'] == "end session":
                    self.surveyToken = getmsg['survey_token']
                    self.questions = getmsg['questions']
                    self.sigs.setQuestionsSignal()
                    self.sigs.changePageSignal()
                    clientsocket.close()
                
            except KeyError:
                # print('Data does not have App_Key field')
                clientsocket.close()


#---------- SIGNAL CLASS ----------#

class appSignals(QtCore.QObject):
    '''
    The app needs signals for the two threads (main, server) to communicate and trigger finctions.
    This class sets up those signals and creates function calls to emit those signals.
    '''
    pageSignal = pyqtSignal()
    positionSignal = pyqtSignal()
    questionSignal = pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)

    def changePageSignal(self):
        self.pageSignal.emit()

    def updatePositionSignal(self):
        self.positionSignal.emit()

    def setQuestionsSignal(self):
        self.questionSignal.emit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))
    screen_resolution = app.desktop().screenGeometry()
    screenWidth, screenHeight = screen_resolution.width(), screen_resolution.height()
    # print("width = ", screenWidth, " height = ", screenHeight)
    if screenWidth > 1700 or screenHeight > 1100:
        width = 300
        height = 400
    else:
        width = 400
        height = 500
    TutorLab = Ui_TutorLab()
    TutorLab.setGeometry((screenWidth/2)-(width/2),(screenHeight/2)-(height/2), width, height)
    TutorLab.setMaximumSize(QtCore.QSize(width, height))
    TutorLab.setMinimumSize(QtCore.QSize(width, height))
    TutorLab.show()
    # print('Main thread:', app.instance().thread())
    sys.exit(app.exec_())
