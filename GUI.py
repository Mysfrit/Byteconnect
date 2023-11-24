import os
import re
import socket
import sys
import threading
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
from struct import pack, unpack

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
import fileFunctions


logging = ""
signedIn = False
Name = ""
password = ""
errorDuringSending = False
pendingFiles = list()
tryTime = 60000
x = threading.Thread()


notSendFile = []

Path_to_folder = "C:\\Byteconnect\\"

Path_of_p12_cert = ""
Path_to_sendingFile = ""
Path_to_secret_file = ""
Path_to_pem_cert = ""
Path_to_rec_files = "C:\\Byteconnect\\receivedFiles"
Path_to_cert_folder = "C:\\Byteconnect\\certs"
Path_to_time_folder = "C:\\Byteconnect\\timeout"
Path_to_time_config_file = "C:\\Byteconnect\\timeout.txt"


# UI setup
class Ui_MainWindow(QMainWindow):
    def sizeHint(self):
        return QSize(810, 590)

    def __init__(self):

        super().__init__()

        self.setupUi(self)
        self.retranslateUi(self)

        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().hide()
        self.show()

    # UI setup
    def setupUi(self, MainWindow):
        global logging
        global pendingFiles

        self.CreateFolders()

        self.loadSavedTimeoutFiles(pendingFiles)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(self.sizeHint())

        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("BC.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/BC.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:1 rgba(140, 15, 69, 255), stop:0 rgba(23, 14, 69, 255));\n"
            "color: rgb(255, 255, 255);\n"
            "")
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(".QWidget{\n"
                                         "  background-color:transparent;\n"
                                         " \n"
                                         "}\n"
                                         "\n"
                                         ".QPushButton{\n"
                                         "  background-color: transparent;\n"
                                         "  color: rgb(255, 255, 255);\n"
                                         "  border: 2px solid white;\n"
                                         "  text-align: center;\n"
                                         "  font-size: 11px;\n"
                                         "  /*margin: 4px 2px;*/\n"
                                         "  border-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         ".QPushButton:hover{\n"
                                         "  background-color: transparent; \n"
                                         "  color: rgb(255, 255, 255);\n"
                                         "  border-top: 1px solid rgb(151, 151, 151); \n"
                                         "  border-left: 1px solid rgb(151, 151, 151);\n"
                                         "  border-bottom: 1px solid rgb(151, 151, 151);\n"
                                         "  border-right: 1px solid rgb(151, 151, 151);\n"
                                         "  text-align: center;\n"
                                         "  font-size: 11px;\n"
                                         "    /*margin: 4px 2px;*/\n"
                                         "  border-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         ".QPushButton:pressed{\n"
                                         "  background-color: transparent;\n"
                                         "  color: rgb(255, 255, 255);\n"
                                         "  border-top: 1px solid rgb(109, 109, 109);\n"
                                         "  border-left: 1px solid rgb(109, 109, 109);\n"
                                         "  border-bottom: 1px solid rgb(109, 109, 109);\n"
                                         "  border-right: 1px solid rgb(109, 109, 109);\n"
                                         "  text-align: center;\n"
                                         "  font-size: 11px;\n"
                                         "  /*margin: 4px 2px;*/\n"
                                         "  border-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         ".QSpinBox{\n"
                                         "  background-color: transparent;\n"
                                         "  color: rgb(255, 255, 255);\n"
                                         "  border: 2px solid white;\n"
                                         "  border-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         ".QLabel{\n"
                                         "   color: rgb(255, 255, 255);\n"
                                         "   font-weight: bold;\n"
                                         "}\n"
                                         "\n"
                                         ".QComboBox{\n"
                                         "  color: rgb(255, 255, 255);\n"
                                         "  background-color: transparent;\n"
                                         "  border: 2px solid white;\n"
                                         "  border-radius: 10px;\n"
                                         "  padding: 0px 0px 0px 4px;\n"
                                         "}\n"
                                         "\n"
                                         "\n"
                                         ".QComboBox::drop-down{\n"
                                         "  \n"
                                         "  background-color: transparent;\n"
                                         "  border: 0px;\n"
                                         "  border-radius: 6px;\n"
                                         "}\n"
                                         "\n"
                                         ".QComboBox::down-arrow{ \n"
                                         "  image: url(white-down-arrow-png-2.png);\n"
                                         "  height: 13px;\n"
                                         "  width: 13px;\n"
                                         "  padding: 0px 5px 0px 0px;\n"
                                         "}\n"
                                         "\n"
                                         ".QLineEdit{\n"
                                         "  background-color: transparent;\n"
                                         "  border: 2px solid white;\n"
                                         "  border-radius: 10px;\n"
                                         "}")

        self.centralwidget.setObjectName("centralwidget")
        self.certName = QtWidgets.QLabel(self.centralwidget)
        self.certName.setGeometry(QtCore.QRect(300, 40, 151, 16))
        self.certName.setAutoFillBackground(False)
        self.certName.setStyleSheet("background: transparent")

        self.certName.setObjectName("certName")
        self.certPass = QtWidgets.QLabel(self.centralwidget)
        self.certPass.setGeometry(QtCore.QRect(300, 100, 151, 16))
        self.certPass.setStyleSheet("background: transparent")
        self.certPass.setObjectName("certPass")

        self.check = QtWidgets.QPushButton(self.centralwidget)
        self.check.setGeometry(QtCore.QRect(300, 160, 181, 31))
        self.check.setStyleSheet("")
        self.check.setObjectName("check")
        self.check.clicked.connect(self.checkCredentials)

        self.succLoad = QtWidgets.QLabel(self.centralwidget)
        self.succLoad.setGeometry(QtCore.QRect(30, 170, 241, 16))
        self.succLoad.setStyleSheet("background: transparent")
        self.succLoad.setObjectName("succLoad")
        self.succLoad.setVisible(False)

        self.unsuccLoad = QtWidgets.QLabel(self.centralwidget)
        self.unsuccLoad.setGeometry(QtCore.QRect(30, 170, 261, 16))
        self.unsuccLoad.setObjectName("unsuccLoad")
        self.unsuccLoad.setStyleSheet("background: transparent")
        self.unsuccLoad.setVisible(False)

        self.loadCerts = QtWidgets.QLabel(self.centralwidget)
        self.loadCerts.setGeometry(QtCore.QRect(20, 20, 221, 16))
        self.loadCerts.setStyleSheet("background: transparent")
        self.loadCerts.setObjectName("loadCerts")

        self.actionLog = QtWidgets.QLabel(self.centralwidget)
        self.actionLog.setGeometry(QtCore.QRect(510, 20, 151, 16))
        self.actionLog.setStyleSheet("background: transparent;\n"
                                     " color: rgb(255, 255, 255);")
        self.actionLog.setObjectName("actionLog")

        self.sendFile = QtWidgets.QLabel(self.centralwidget)
        self.sendFile.setGeometry(QtCore.QRect(20, 220, 151, 16))
        self.sendFile.setStyleSheet("background: transparent")
        self.sendFile.setObjectName("sendFile")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(510, 50, 281, 491))
        self.scrollArea.setStyleSheet("background: transparent;\n"
                                      "border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 281, 491))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.log = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
        self.log.setGeometry(QtCore.QRect(0, -5, 281, 491))
        self.log.setObjectName("log")
        self.log.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.log.setStyleSheet("")
        self.log.setPlainText("")
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.confirm = QtWidgets.QPushButton(self.centralwidget)
        self.confirm.setEnabled(True)
        self.confirm.setGeometry(QtCore.QRect(290, 520, 191, 31))
        self.confirm.setObjectName("confirm")
        self.confirm.setStyleSheet("")
        self.confirm.clicked.connect(
            lambda: self.saveTempFile(self.nameIPInput.currentText(), os.path.splitext(self.filePathInput.text())[1]))

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(20, 330, 251, 41))
        self.sendButton.setObjectName("sendButton")

        self.pemPath = QtWidgets.QLineEdit(self.centralwidget)
        self.pemPath.setGeometry(QtCore.QRect(20, 60, 181, 21))
        self.pemPath.setObjectName("pemPath")
        self.pemPath.setReadOnly(True)

        self.pem = QtWidgets.QLabel(self.centralwidget)
        self.pem.setGeometry(QtCore.QRect(20, 40, 151, 16))
        self.pem.setObjectName("pem")
        self.pem.setStyleSheet("background: transparent")

        self.pkcs12 = QtWidgets.QLabel(self.centralwidget)
        self.pkcs12.setGeometry(QtCore.QRect(20, 100, 151, 16))
        self.pkcs12.setObjectName("pkcs12")
        self.pkcs12.setStyleSheet("background: transparent")

        self.p12Path = QtWidgets.QLineEdit(self.centralwidget)
        self.p12Path.setGeometry(QtCore.QRect(20, 120, 181, 21))
        self.p12Path.setObjectName("p12Path")
        self.p12Path.setReadOnly(True)

        self.loadPEM = QtWidgets.QPushButton(self.centralwidget)
        self.loadPEM.setGeometry(QtCore.QRect(210, 60, 61, 21))
        self.loadPEM.setObjectName("loadPEM")

        self.loadPEM.clicked.connect(self.getPemCert)

        self.loadP12 = QtWidgets.QPushButton(self.centralwidget)
        self.loadP12.setGeometry(QtCore.QRect(210, 120, 61, 21))
        self.loadP12.setObjectName("loadP12")

        self.loadP12.clicked.connect(self.getP12Cert)

        self.filePathInput = QtWidgets.QLineEdit(self.centralwidget)
        self.filePathInput.setGeometry(QtCore.QRect(20, 240, 181, 21))
        self.filePathInput.setObjectName("filePathInput")
        self.filePathInput.setReadOnly(True)

        self.loadFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadFileButton.setGeometry(QtCore.QRect(210, 240, 61, 21))
        self.loadFileButton.setObjectName("loadFileButton")

        self.nameIPInput = QtWidgets.QComboBox(self.centralwidget)
        self.nameIPInput.setGeometry(QtCore.QRect(20, 300, 251, 22))
        self.nameIPInput.setAcceptDrops(False)
        self.nameIPInput.setEditable(True)
        self.nameIPInput.setObjectName("nameIPInput")

        for file in os.listdir(Path_to_cert_folder):
            self.nameIPInput.addItem(file.replace(".pem", "").replace(",", ", "))

        self.recIP = QtWidgets.QLabel(self.centralwidget)
        self.recIP.setGeometry(QtCore.QRect(20, 280, 261, 16))
        self.recIP.setObjectName("recIP")
        self.recIP.setStyleSheet("background: transparent")

        self.certNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.certNameInput.setGeometry(QtCore.QRect(300, 60, 181, 21))
        self.certNameInput.setObjectName("certNameInput")
        self.certNameInput.setStyleSheet("")

        self.certPassInput = QtWidgets.QLineEdit(self.centralwidget)
        self.certPassInput.setGeometry(QtCore.QRect(300, 120, 181, 21))
        self.certPassInput.setObjectName("certPassInput")
        self.certPassInput.setEchoMode(QLineEdit.Password)

        self.impossible = QtWidgets.QLabel(self.centralwidget)
        self.impossible.setEnabled(True)
        self.impossible.setGeometry(QtCore.QRect(20, 400, 471, 16))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.impossible.setFont(font)
        self.impossible.setStyleSheet("background: transparent")
        self.impossible.setObjectName("impossible")

        self.intLabel = QtWidgets.QLabel(self.centralwidget)
        self.intLabel.setGeometry(QtCore.QRect(290, 220, 151, 16))
        self.intLabel.setStyleSheet("background: transparent")
        self.intLabel.setObjectName("intLabel")

        self.intSelect = QtWidgets.QComboBox(self.centralwidget)
        self.intSelect.setGeometry(QtCore.QRect(290, 240, 191, 22))
        self.intSelect.setAcceptDrops(False)
        self.intSelect.setEditable(False)
        self.intSelect.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.intSelect.setObjectName("intSelect")

        ip_address = socket.gethostbyname_ex(socket.gethostname())[2]
        for addr in ip_address:
            self.intSelect.addItem(addr)

        self.storeFile = QtWidgets.QLabel(self.centralwidget)
        self.storeFile.setEnabled(True)
        self.storeFile.setGeometry(QtCore.QRect(20, 430, 251, 16))
        self.storeFile.setObjectName("storeFile")
        self.storeFile.setStyleSheet("background: transparent")

        self.storeYes = QtWidgets.QPushButton(self.centralwidget)
        self.storeYes.setEnabled(True)
        self.storeYes.setGeometry(QtCore.QRect(20, 450, 111, 41))
        self.storeYes.setObjectName("storeYes")
        self.storeYes.clicked.connect(self.yesStore)

        self.storeNo = QtWidgets.QPushButton(self.centralwidget)
        self.storeNo.setEnabled(True)
        self.storeNo.setGeometry(QtCore.QRect(140, 450, 121, 41))
        self.storeNo.setObjectName("storeNo")
        self.storeNo.clicked.connect(self.noStore)

        self.storeTime = QtWidgets.QLabel(self.centralwidget)
        self.storeTime.setEnabled(True)
        self.storeTime.setGeometry(QtCore.QRect(20, 510, 251, 21))
        self.storeTime.setObjectName("storeTime")
        self.storeTime.setStyleSheet("background: transparent")

        self.storeHoursInput = QtWidgets.QSpinBox(self.centralwidget)
        self.storeHoursInput.setGeometry(QtCore.QRect(120, 510, 51, 21))
        self.storeHoursInput.setStyleSheet("")
        self.storeHoursInput.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.storeHoursInput.setObjectName("storeHoursInput")
        self.storeHoursInput.setMinimum(1)
        self.storeHoursInput.setMaximum(999)
        self.storeHoursInput.setVisible(False)

        self.fileSent = QtWidgets.QLabel(self.centralwidget)
        self.fileSent.setEnabled(True)
        self.fileSent.setGeometry(QtCore.QRect(20, 400, 471, 16))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.fileSent.setFont(font)
        self.fileSent.setObjectName("fileSent")
        self.fileSent.setStyleSheet("background: transparent")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionView_database = QtWidgets.QAction(MainWindow)
        self.actionView_database.setObjectName("actionView_database")
        self.actionView_database.triggered.connect(lambda: os.system(f'explorer.exe "{Path_to_cert_folder}"'))

        self.actionView_stored_files = QtWidgets.QAction(MainWindow)
        self.actionView_stored_files.setObjectName("actionView_stored_files")
        self.actionView_stored_files.triggered.connect(lambda: os.system(f'explorer.exe "{Path_to_time_folder}"'))

        self.actionView_received_files = QtWidgets.QAction(MainWindow)
        self.actionView_received_files.setObjectName("actionView_received_files")
        self.actionView_received_files.triggered.connect(lambda: os.system(f'explorer.exe "{Path_to_rec_files}"'))

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionQuit.triggered.connect(lambda: self.close())

        self.tmpLabel = QtWidgets.QLabel(self.centralwidget)
        self.tmpLabel.setGeometry(QtCore.QRect(10, 10, 481, 191))
        self.tmpLabel.setStyleSheet("background-color:transparent;\n"
                                    "border: 3px solid white;\n"
                                    "border-radius: 10px;")

        self.tmpLabel.setText("")
        self.tmpLabel.setObjectName("tmpLabel")
        self.tmpLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.tmpLabel2.setGeometry(QtCore.QRect(10, 210, 481, 171))
        self.tmpLabel2.setStyleSheet("background-color: transparent;\n"
                                     "border: 3px solid white;\n"
                                     "border-radius: 10px; ")
        self.tmpLabel2.setText("")
        self.tmpLabel2.setObjectName("tmpLabel2")
        self.tmpLabel3 = QtWidgets.QLabel(self.centralwidget)
        self.tmpLabel3.setGeometry(QtCore.QRect(10, 390, 481, 171))
        self.tmpLabel3.setStyleSheet("background-color: transparent;\n"
                                     "border: 3px solid white;\n"
                                     "border-radius: 10px;")
        self.tmpLabel3.setText("")
        self.tmpLabel3.setObjectName("tmpLabel3")
        self.tmpLabel3.setVisible(False)
        self.tmpLabel2_2 = QtWidgets.QLabel(self.centralwidget)
        self.tmpLabel2_2.setGeometry(QtCore.QRect(500, 10, 301, 551))
        self.tmpLabel2_2.setStyleSheet("background-color: transparent;\n"
                                       "border: 3px solid white;\n"
                                       "border-radius: 10px; ")
        self.tmpLabel2_2.setText("")
        self.tmpLabel2_2.setObjectName("tmpLabel2_2")

        self.hrsminSelect = QtWidgets.QComboBox(self.centralwidget)
        self.hrsminSelect.setGeometry(QtCore.QRect(180, 510, 81, 22))
        self.hrsminSelect.setAcceptDrops(False)
        self.hrsminSelect.setEditable(False)
        self.hrsminSelect.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.hrsminSelect.setObjectName("hrsminSelect")
        self.hrsminSelect.addItem("")
        self.hrsminSelect.addItem("")

        self.tmpLabel2_2.raise_()
        self.tmpLabel3.raise_()
        self.tmpLabel2.raise_()
        self.tmpLabel.raise_()
        self.certName.raise_()
        self.certPass.raise_()
        self.loadCerts.raise_()
        self.actionLog.raise_()
        self.sendFile.raise_()
        self.scrollArea.raise_()
        self.sendButton.raise_()
        self.pemPath.raise_()
        self.pem.raise_()
        self.pkcs12.raise_()
        self.p12Path.raise_()
        self.loadPEM.raise_()
        self.loadP12.raise_()
        self.filePathInput.raise_()
        self.loadFileButton.raise_()
        self.nameIPInput.raise_()
        self.recIP.raise_()
        self.certNameInput.raise_()
        self.certPassInput.raise_()
        self.impossible.raise_()
        self.storeFile.raise_()
        self.storeYes.raise_()
        self.storeNo.raise_()
        self.storeTime.raise_()
        self.storeHoursInput.raise_()
        self.fileSent.raise_()
        self.check.raise_()
        self.succLoad.raise_()
        self.unsuccLoad.raise_()
        self.intLabel.raise_()
        self.intSelect.raise_()
        self.confirm.raise_()
        self.hrsminSelect.raise_()

        self.menuMenu.addAction(self.actionView_database)
        self.menuMenu.addAction(self.actionView_stored_files)
        self.menuMenu.addAction(self.actionView_received_files)
        self.menuMenu.addAction(self.actionQuit)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.loadFileButton.clicked.connect(self.getFileToSend)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        timer = QTimer(self)
        timer.timeout.connect(self.timerUpdate)
        timer.start(100)

        sendingTimer = QTimer(self)
        sendingTimer.timeout.connect(self.sendTimeOutFiles)
        global tryTime
        sendingTimer.start(tryTime)
    # loading pending Files from folder
    def loadSavedTimeoutFiles(self, pendingFiles):

        file = open(Path_to_time_config_file, "r", encoding='utf-16')
        while True:
            logs = file.readline()
            print(logs)
            if logs != "":
                if logs != "\n":
                    log = re.split(r"(.*) - ", logs)[1]
                    pendingFiles.append({
                        "ipAddr": re.split(r"timeout\\(.*),", log)[1],
                        "filePath": log,
                        "timeToStore": re.split(r"(.*) - ", logs)[2]
                    })
            else:
                break
        file.close()
        print("PENDING FILES...")
        print(pendingFiles)

    # Creating file folders
    def CreateFolders(self):

        if not os.path.exists(Path_to_folder):
            os.makedirs(Path_to_folder, exist_ok=True)
        if not os.path.exists(Path_to_cert_folder):
            os.mkdir(Path_to_cert_folder)
        if not os.path.exists(Path_to_rec_files):
            os.mkdir(Path_to_rec_files)
        if not os.path.exists(Path_to_time_folder):
            os.mkdir(Path_to_time_folder)
        if not os.path.exists(Path_to_time_config_file):
            file = open(Path_to_time_config_file, "x")
            file.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Byteconnect - Early Beta v8 5.0L"))
        self.certName.setText(_translate("MainWindow", "Certificate name"))
        self.certPass.setText(_translate("MainWindow", "Certificate password"))
        self.loadCerts.setText(_translate("MainWindow", "Load your certificate in both formats:"))
        self.actionLog.setText(_translate("MainWindow", "Recent actions log:"))
        self.sendFile.setText(_translate("MainWindow", "Send a file:"))
        self.log.setPlainText(_translate("MainWindow", logging))
        self.sendButton.setText(_translate("MainWindow", "SEND"))
        self.sendButton.setEnabled(False)
        self.sendButton.clicked.connect(self.checkParams)
        self.confirm.setText(_translate("MainWindow", "Confirm"))
        self.pem.setText(_translate("MainWindow", "PEM"))
        self.pkcs12.setText(_translate("MainWindow", "PKCS12"))
        self.loadPEM.setText(_translate("MainWindow", "Load"))
        self.loadP12.setText(_translate("MainWindow", "Load"))
        self.loadFileButton.setText(_translate("MainWindow", "Load"))


        self.recIP.setText(_translate("MainWindow", "Receiver IP address, name:"))
        self.impossible.setText(_translate("MainWindow", "Impossible to send selected file, receiver unavailable."))
        self.storeFile.setText(_translate("MainWindow", "Store the file and send when possible?"))
        self.storeYes.setText(_translate("MainWindow", "Yes, store"))
        self.storeNo.setText(_translate("MainWindow", "No, don\'t store"))
        self.storeTime.setText(_translate("MainWindow", "Store the file for"))
        self.fileSent.setText(_translate("MainWindow", "File sent."))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionView_database.setText(_translate("MainWindow", "View database"))

        self.actionView_stored_files.setText(_translate("MainWindow", "View stored files"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionView_received_files.setText(_translate("MainWindow", "View received files"))

        self.check.setText(_translate("MainWindow", "Check credentials"))
        self.hrsminSelect.setItemText(0, _translate("MainWindow", "hours"))
        self.hrsminSelect.setItemText(1, _translate("MainWindow", "minutes"))
        self.hrsminSelect.setVisible(False)
        self.succLoad.setText(_translate("MainWindow", "Certificates loaded successfully."))
        self.unsuccLoad.setText(_translate("MainWindow", "Incorrect name or password."))
        self.intLabel.setText(_translate("MainWindow", "Select interface:"))
        self.fileSent.setVisible(False)
        self.impossible.setVisible(False)
        self.storeFile.setVisible(False)
        self.storeYes.setVisible(False)
        self.storeNo.setVisible(False)
        self.storeTime.setVisible(False)
        self.storeHoursInput.setVisible(False)
        self.confirm.setVisible(False)

    # updating UI every X miliseconds
    def timerUpdate(self):
        global logging
        try:
            global errorDuringSending
            global pendingFiles
            global x
            self.setSaveLabels(errorDuringSending)
            self.log.setPlainText(logging)
            self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

            file = open(Path_to_time_config_file, "w", encoding="utf-16")
            for item in pendingFiles:
                file.write(item["filePath"] + " - " + item["timeToStore"] + "\n")

            if signedIn:
                if not x.is_alive():
                    x = threading.Thread(target=listeningThread, args=(self.intSelect.currentText(),))
                    x.daemon = True
                    x.start()

        except Exception as e:
            print(e)

    # Changing visible labels
    def setSaveLabels(self, visibility):
        self.impossible.setVisible(visibility)
        self.storeFile.setVisible(visibility)
        self.storeYes.setVisible(visibility)
        self.storeNo.setVisible(visibility)
        self.tmpLabel3.setVisible(visibility)

    # Browsing files
    def getFileToSend(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath())
        self.filePathInput.setText(fileName)

    def getP12Cert(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.p12')
        self.p12Path.setText(fileName)

    def getPemCert(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(),
                                                            'PEM (*.pem);;CER (*.cer)')
        self.pemPath.setText(fileName)

    # Checking valid credentials for cert
    def checkCredentials(self):
        global logging
        global signedIn
        self.check.setEnabled(False)
        if self.pemPath.text() != "" and self.p12Path.text() != "" and self.certNameInput.text() != "" and self.certNameInput.text() != "":
            try:
                with open(self.p12Path.text(), "rb") as f:
                    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(),
                                                                                                         self.certPassInput.text().encode())

                    name = re.split(r"CN=([^,]+)", str(certificate))
                    if name[1] == self.certNameInput.text():

                        pemCert = x509.load_pem_x509_certificate(fileFunctions.readFile(self.pemPath.text()),
                                                                 default_backend())
                        nameInCert = re.split(r"CN=([^,]+)", str(pemCert.subject))
                        if nameInCert[1] == self.certNameInput.text():
                            global signedIn
                            signedIn = True
                            global Name
                            Name = nameInCert[1]
                            self.sendButton.setEnabled(True)
                            global password
                            password = self.certPassInput.text()
                            global Path_of_p12_cert
                            Path_of_p12_cert = self.p12Path.text()
                            global Path_to_pem_cert
                            Path_to_pem_cert = self.pemPath.text()
                            global Path_to_secret_file
                            Path_to_secret_file = self.filePathInput.text()
                            self.succLoad.setVisible(True)
                            self.unsuccLoad.setVisible(False)
                            self.check.setEnabled(True)

                            if signedIn:
                                global x
                                x = threading.Thread(target=listeningThread, args=(self.intSelect.currentText(),))
                                x.daemon = True

                                if not x.is_alive():
                                    x.start()

                            #logging += "Checking credentials succ!\n"
                            return True
            except Exception as e:
                logging+= e
                self.succLoad.setVisible(False)
                self.unsuccLoad.setVisible(True)
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Wrong credentials")
                error_dialog.setText("Wrong credentials")
                error_dialog.exec()
                self.check.setEnabled(True)
                return False
        else:
            self.succLoad.setVisible(False)
            self.unsuccLoad.setVisible(True)
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Wrong credentials")
            error_dialog.setText("Wrong credentials")
            logging += "Wrong credentials!\n"
            error_dialog.exec()
            self.check.setEnabled(True);
            return False

    # Check valid parameters from GUI
    def checkParams(self):
        global logging
        self.sendButton.setEnabled(False)
        try:
            if self.checkCredentials():
                if self.filePathInput.text() != "":
                    re.split(r"(.+),", self.nameIPInput.currentText().replace(", ", ","))[1]
                    initThraed = threading.Thread(target=initCommThread, args=(self.filePathInput.text(),
                                                                      re.split(r"(.+),",
                                                                               self.nameIPInput.currentText().replace(
                                                                                   ", ", ","))[1]))
                    initThraed.daemon = True
                    initThraed.start()

                else:
                    error_dialog = QMessageBox()
                    error_dialog.setWindowTitle("File path")
                    error_dialog.setText("File Path is empty")
                    error_dialog.exec()
                    return
            else:
                return

        except Exception as err:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Invalid IP and name")
            error_dialog.setText("Has to be in format <IP>,<NAME> ")
            error_dialog.exec()
            self.sendButton.setEnabled(True)
            print(err)
            return

    # if file stored
    def yesStore(self):
        try:
            self.storeTime.setVisible(True)
            self.storeHoursInput.setVisible(True)
            self.hrsminSelect.setVisible(True)
            self.confirm.setVisible(True)
        except Exception as e:
            print(e)

    # if file not stored
    def noStore(self):
        global errorDuringSending
        global notSendFile
        errorDuringSending = False
        notSendFile = []
        self.fileSent.setVisible(False)
        self.impossible.setVisible(False)
        self.storeFile.setVisible(False)
        self.storeYes.setVisible(False)
        self.storeNo.setVisible(False)
        self.filePathInput.setText("")
        self.storeTime.setVisible(False)
        self.storeHoursInput.setVisible(False)
        self.hrsminSelect.setVisible(False)
        self.confirm.setVisible(False)

    # How to save file to pending files
    def saveTempFile(self, addr, name):
        try:
            global errorDuringSending
            global logging
            errorDuringSending = False
            logging += f"Saving file in {Path_to_time_folder} with name {addr}{name} for {self.storeHoursInput.text()} {self.hrsminSelect.currentText()}.\n"
            print(f"{Path_to_time_folder}\\{addr}{name}")
            currentTime = datetime.now()
            print(
                f"{Path_to_time_folder}\\{addr},{name} - {currentTime.year}/{currentTime.month}/{currentTime.day}/{currentTime.hour}/{currentTime.minute}")
            try:
                file = open(Path_to_time_config_file, "a", encoding='utf-16')
                if self.hrsminSelect.currentText() == "hours":
                    currentTime = datetime.now() + timedelta(hours=int(self.storeHoursInput.text()))
                else:
                    currentTime = datetime.now() + timedelta(minutes=int(self.storeHoursInput.text()))
                file.write(
                    f"{Path_to_time_folder}\\{addr}{name} - {currentTime.year}/{currentTime.month}/{currentTime.day}/{currentTime.hour}/{currentTime.minute}\n")
            except Exception as e:
                logging+= e
                print(e)
            secretData = fileFunctions.encryptDataFinal(fileFunctions.readFile(self.filePathInput.text()),
                                                        x509.load_pem_x509_certificate(
                                                            fileFunctions.readFile(Path_to_pem_cert),
                                                            default_backend()))

            fileFunctions.writeToFile(f"{Path_to_time_folder}\\{addr}{name}", secretData.encode())

            self.hrsminSelect.setVisible(False)
            self.storeHoursInput.setVisible(False)
            self.storeTime.setVisible(False)
            self.confirm.setVisible(False)
            self.fileSent.setVisible(False)
            self.impossible.setVisible(False)
            self.storeFile.setVisible(False)
            self.storeYes.setVisible(False)
            self.storeNo.setVisible(False)
            self.filePathInput.setText("")

            global pendingFiles
            global notSendFile
            notSendFile["filePath"] = f"{Path_to_time_folder}\\{addr}{name}"
            notSendFile[
                "timeToStore"] = f"{currentTime.year}/{currentTime.month}/{currentTime.day}/{currentTime.hour}/{currentTime.minute}"
            pendingFiles.append(notSendFile)
            notSendFile = []
        except Exception as e:
            logging+= e
            print(e)

    # Sending timeout files 1-by-1
    def sendTimeOutFiles(self):
        global signedIn
        global x
        if signedIn:
            try:
                global pendingFiles
                pendingFilesList = pendingFiles
                for pendingFileEntry in pendingFilesList:
                    print(pendingFileEntry)
                    time = pendingFileEntry["timeToStore"].replace("\n", "")
                    print(time)
                    time = datetime.strptime(time, '%Y/%m/%d/%H/%M')

                    xxx = fileFunctions.readFile(pendingFileEntry["filePath"]).decode()

                    rawData = fileFunctions.decryptDataFinal(xxx, password, Path_of_p12_cert)

                    #rawData = rawData.decode(encoding='utf-16')

                    trash, XXXextension = os.path.splitext(pendingFileEntry["filePath"])

                    if time < datetime.now():
                        x = threading.Thread(target=initCommThread,
                                             kwargs=dict(PathToData=rawData, addr=pendingFileEntry["ipAddr"],
                                                         resend=True,
                                                         timeout=True, Path=False, Extension=XXXextension))
                    else:
                        x = threading.Thread(target=initCommThread,
                                             kwargs=dict(PathToData=rawData, addr=pendingFileEntry["ipAddr"],
                                                         resend=True,
                                                         timeout=False, Path=False, Extension=XXXextension))
                    x.start()

            except Exception as e:
                print("here")
                print(e)


# Thread for sending files
def initCommThread(PathToData, addr=None, resend=False, timeout=False, Path=True, Extension=None):
    global logging
    global errorDuringSending
    global pendingFiles

    try:
        if Path:
            data = fileFunctions.readFile(str(PathToData).replace(r"\\\\", r"\\"))
        else:
            data = PathToData

        if addr is None:
            addr = "192.168.56.1"
        serverSocketRec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging += f"Connecting to {addr}...\n"
        serverSocketRec.connect((addr, 15000))
        logging += f"Connection successful to {addr}.\n"
        logging += f"Asking for name of {addr}.\n"
        serverSocketRec.send(b"hello, who are you")
        answer = serverSocketRec.recv(4096)
        answer = answer.decode()
        matches = ""
        for file in os.listdir(Path_to_cert_folder):
            if file.endswith(".pem") and addr in file and answer in file:
                logging += f"Found match in saved files.\n"
                matches = file
                break
        print(matches)
        if len(list(matches)) == 0:
            logging += f"Asking for cert.\n"
            serverSocketRec.send(b"pls cert")

            bs = serverSocketRec.recv(8)
            (length,) = unpack('>Q', bs)
            cert = b''
            while len(cert) < length:
                to_read = length - len(cert)
                cert += serverSocketRec.recv(
                    4096 if to_read > 4096 else to_read)
            logging += f"Cert recieved!\n"
            cert = cert.decode()
            cert = cert.replace("\r", "")

            logging += f"Verifying certificate.\n"
            pemCert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            nameInCert = re.split(r"CN=([^,]+)", str(pemCert.subject))
            print("NAME")
            print(nameInCert[1])
            print("SPLIT ANSWER")
            print(answer)

            if answer == nameInCert[1]:
                print("SAVING CERT")
                logging += f"Saving certificate to " + Path_to_cert_folder + "\\" + addr + "," + answer + ".pem" + ".\n"
                fileFunctions.writeToFile(Path_to_cert_folder + "\\" + addr + "," + answer + ".pem",
                                          cert.encode())
                secretData = fileFunctions.encryptDataFinal(data, pemCert)
                logging += f"Seding message to {addr}.\n"

                if Extension is None:
                    trash, XXXextension = os.path.splitext(PathToData)
                else:
                    XXXextension = Extension

                serverSocketRec.send(f"EXT: {XXXextension}".encode())
                serverSocketRec.sendall(pack('>Q', len("Message: ".encode() + secretData.encode())))
                serverSocketRec.sendall(("Message: " + secretData).encode())
                logging += f"Send complete on IP {addr}.\n"

            else:
                print("YOU ARE NOT THE ONE")
                return

        else:
            print("GOT THE CERT")

            logging += f"Seding message to {addr}.\n"
            certificate = fileFunctions.readFile(Path_to_cert_folder + "\\" + matches)

            if Path:
                secretData = fileFunctions.encryptDataFinal(fileFunctions.readFile(PathToData),
                                                            x509.load_pem_x509_certificate(certificate,
                                                                                           default_backend()))
            else:
                secretData = fileFunctions.encryptDataFinal(PathToData,
                                                            x509.load_pem_x509_certificate(certificate,

                                                                                           default_backend()))
            if Extension is None:
                trash, XXXextension = os.path.splitext(PathToData)
            else:
                XXXextension = Extension

            serverSocketRec.send(f"EXT: {XXXextension}".encode())
            serverSocketRec.sendall(pack('>Q', len("Message: ".encode() + secretData.encode())))
            serverSocketRec.sendall(("Message: " + secretData).encode())
            serverSocketRec.close()
            serverSocketRec.close()

        if resend:
            for file in os.listdir(Path_to_time_folder):
                if addr in file and answer in file:
                    if os.path.exists(Path_to_time_folder + "\\" + file):
                        os.remove(Path_to_time_folder + "\\" + file)

            for i in range(len(pendingFiles)):
                print("HERE!!!!!")
                print(pendingFiles[i])

                if pendingFiles[i]["ipAddr"] in addr:
                    print(f"deleting pendingFiles[{i}] {pendingFiles[i]}")
                    del pendingFiles[i]
                    break

    except WindowsError as err:

        if err.winerror == 10054:
            pass
        else:
            logging += f"Unable to connect to addr {addr} after 5 tries, destination unreachable or declining.\n"
            print(err)
            if not resend:
                if Extension is None:
                    trash, XXXextension = os.path.splitext(PathToData)
                else:
                    XXXextension = Extension

                errorDuringSending = True
                global notSendFile
                notSendFile = {
                    "ipAddr": addr,
                    "filePath": f"{Path_to_time_folder}\\{addr}{XXXextension}",
                    "timeToStore": ""
                }
                serverSocketRec.close()

            if resend:
                if timeout:
                    onlyfiles = [f for f in listdir(Path_to_time_folder) if
                                 isfile(join(Path_to_time_folder, f))]

                    for file in onlyfiles:
                        if file.__contains__(addr):
                            os.remove(Path_to_time_folder + "\\" + file)
                    for i in range(len(pendingFiles)):
                        if pendingFiles[i]["ipAddr"] == addr:
                            del pendingFiles[i]
                            break
                return
            else:
                for i in range(len(pendingFiles)):
                    if pendingFiles[i]["ipAddr"] in addr:
                        serverSocketRec.close()
                        return

    except Exception as e:
        print(e)


# Listening thread on port 15000
def listeningThread(ip_address: str):
    global logging
    global Name
    try:
        print(ip_address)
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((ip_address, 15000))
        serverSocket.listen()
        (clientConnected, clientAddress) = serverSocket.accept()
        logging += f"Accepted connection from {clientAddress}.\n"
        print("accept")
        while True:
            packet = clientConnected.recv(4096).decode()
            if "hello, who are you" in packet:
                logging += f"{clientAddress} asking for name.\n"
                data = Name
                clientConnected.send(data.encode())

            elif "pls cert" in packet:
                logging += f"{clientAddress} asking for public certificate.\n"
                logging += f"Sending public certificate.\n"
                data = fileFunctions.readFile(Path_to_pem_cert).decode()
                clientConnected.sendall(pack('>Q', len(data.encode())))
                clientConnected.sendall(data.encode())

            elif "EXT: " in packet:
                logging += f"Recieving message from {clientAddress}.\n"

                XXXextension = packet.replace("EXT: ", "")

                bs = clientConnected.recv(8)
                (length,) = unpack('>Q', bs)
                recData = b''
                while len(recData) < length:
                    to_read = length - len(recData)
                    recData += clientConnected.recv(
                        4096 if to_read > 4096 else to_read)
                print(recData.decode())
                recData = recData.decode()
                data = recData.replace("Message: ", "")
                time = datetime.now()
                fileFunctions.writeToFile(Path_to_rec_files + "\\" + time.strftime("%H-%M-%S") + XXXextension,
                                          fileFunctions.decryptDataFinal(data, password, Path_of_p12_cert))
                logging += f"Message saved to " + Path_to_rec_files + "\\" + time.strftime(
                    "%H-%M-%S") + XXXextension + ".\n"
                serverSocket.close()
                clientConnected.close()
                return
    except Exception as err:
        print(err)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    sys.exit(app.exec())
