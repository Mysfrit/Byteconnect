# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Download\bleh_no_peepo_cert_check(2).ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(798, 568)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.certName = QtWidgets.QLabel(self.centralwidget)
        self.certName.setGeometry(QtCore.QRect(300, 30, 151, 16))
        self.certName.setObjectName("certName")
        self.certPass = QtWidgets.QLabel(self.centralwidget)
        self.certPass.setGeometry(QtCore.QRect(300, 80, 151, 16))
        self.certPass.setObjectName("certPass")
        self.loadCerts = QtWidgets.QLabel(self.centralwidget)
        self.loadCerts.setGeometry(QtCore.QRect(20, 10, 201, 16))
        self.loadCerts.setObjectName("loadCerts")
        self.actionLog = QtWidgets.QLabel(self.centralwidget)
        self.actionLog.setGeometry(QtCore.QRect(510, 10, 151, 16))
        self.actionLog.setObjectName("actionLog")
        self.sendFile = QtWidgets.QLabel(self.centralwidget)
        self.sendFile.setGeometry(QtCore.QRect(20, 200, 151, 16))
        self.sendFile.setObjectName("sendFile")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(510, 30, 281, 491))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 279, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.log = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
        self.log.setEnabled(True)
        self.log.setGeometry(QtCore.QRect(0, 0, 281, 491))
        self.log.setPlainText("")
        self.log.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.log.setObjectName("log")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(20, 310, 251, 41))
        self.sendButton.setObjectName("sendButton")
        self.pemPath = QtWidgets.QLineEdit(self.centralwidget)
        self.pemPath.setEnabled(True)
        self.pemPath.setGeometry(QtCore.QRect(20, 50, 181, 21))
        self.pemPath.setReadOnly(True)
        self.pemPath.setObjectName("pemPath")
        self.pem = QtWidgets.QLabel(self.centralwidget)
        self.pem.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.pem.setObjectName("pem")
        self.pkcs12 = QtWidgets.QLabel(self.centralwidget)
        self.pkcs12.setGeometry(QtCore.QRect(20, 80, 151, 16))
        self.pkcs12.setObjectName("pkcs12")
        self.p12Path = QtWidgets.QLineEdit(self.centralwidget)
        self.p12Path.setEnabled(True)
        self.p12Path.setGeometry(QtCore.QRect(20, 100, 181, 21))
        self.p12Path.setReadOnly(True)
        self.p12Path.setObjectName("p12Path")
        self.loadPEM = QtWidgets.QPushButton(self.centralwidget)
        self.loadPEM.setGeometry(QtCore.QRect(210, 50, 61, 21))
        self.loadPEM.setObjectName("loadPEM")
        self.loadP12 = QtWidgets.QPushButton(self.centralwidget)
        self.loadP12.setGeometry(QtCore.QRect(210, 100, 61, 21))
        self.loadP12.setObjectName("loadP12")
        self.filePathInput = QtWidgets.QLineEdit(self.centralwidget)
        self.filePathInput.setEnabled(True)
        self.filePathInput.setGeometry(QtCore.QRect(20, 220, 181, 21))
        self.filePathInput.setReadOnly(True)
        self.filePathInput.setObjectName("filePathInput")
        self.loadFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadFileButton.setGeometry(QtCore.QRect(210, 220, 61, 21))
        self.loadFileButton.setObjectName("loadFileButton")
        self.nameIPInput = QtWidgets.QComboBox(self.centralwidget)
        self.nameIPInput.setGeometry(QtCore.QRect(20, 270, 251, 22))
        self.nameIPInput.setAcceptDrops(False)
        self.nameIPInput.setEditable(True)
        self.nameIPInput.setObjectName("nameIPInput")
        self.nameIPInput.addItem("")
        self.nameIPInput.addItem("")
        self.recIP = QtWidgets.QLabel(self.centralwidget)
        self.recIP.setGeometry(QtCore.QRect(20, 250, 231, 16))
        self.recIP.setObjectName("recIP")
        self.certNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.certNameInput.setGeometry(QtCore.QRect(300, 50, 181, 21))
        self.certNameInput.setObjectName("certNameInput")
        self.certPassInput = QtWidgets.QLineEdit(self.centralwidget)
        self.certPassInput.setGeometry(QtCore.QRect(300, 100, 181, 21))
        self.certPassInput.setObjectName("certPassInput")
        self.impossible = QtWidgets.QLabel(self.centralwidget)
        self.impossible.setEnabled(True)
        self.impossible.setGeometry(QtCore.QRect(20, 370, 471, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.impossible.setFont(font)
        self.impossible.setObjectName("impossible")
        self.storeFile = QtWidgets.QLabel(self.centralwidget)
        self.storeFile.setEnabled(True)
        self.storeFile.setGeometry(QtCore.QRect(20, 410, 231, 16))
        self.storeFile.setObjectName("storeFile")
        self.storeYes = QtWidgets.QPushButton(self.centralwidget)
        self.storeYes.setEnabled(True)
        self.storeYes.setGeometry(QtCore.QRect(20, 430, 111, 41))
        self.storeYes.setObjectName("storeYes")
        self.storeNo = QtWidgets.QPushButton(self.centralwidget)
        self.storeNo.setEnabled(True)
        self.storeNo.setGeometry(QtCore.QRect(140, 430, 121, 41))
        self.storeNo.setObjectName("storeNo")
        self.storeTime = QtWidgets.QLabel(self.centralwidget)
        self.storeTime.setEnabled(True)
        self.storeTime.setGeometry(QtCore.QRect(20, 490, 341, 16))
        self.storeTime.setObjectName("storeTime")
        self.storeHoursInput = QtWidgets.QSpinBox(self.centralwidget)
        self.storeHoursInput.setGeometry(QtCore.QRect(270, 490, 61, 21))
        self.storeHoursInput.setMinimum(1)
        self.storeHoursInput.setMaximum(999)
        self.storeHoursInput.setObjectName("storeHoursInput")
        self.fileSent = QtWidgets.QLabel(self.centralwidget)
        self.fileSent.setEnabled(True)
        self.fileSent.setGeometry(QtCore.QRect(20, 370, 471, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.fileSent.setFont(font)
        self.fileSent.setObjectName("fileSent")
        self.check = QtWidgets.QPushButton(self.centralwidget)
        self.check.setGeometry(QtCore.QRect(300, 140, 181, 21))
        self.check.setObjectName("check")
        self.succLoad = QtWidgets.QLabel(self.centralwidget)
        self.succLoad.setGeometry(QtCore.QRect(20, 140, 241, 16))
        self.succLoad.setObjectName("succLoad")
        self.unsuccLoad = QtWidgets.QLabel(self.centralwidget)
        self.unsuccLoad.setGeometry(QtCore.QRect(20, 140, 261, 16))
        self.unsuccLoad.setObjectName("unsuccLoad")
        self.intLabel = QtWidgets.QLabel(self.centralwidget)
        self.intLabel.setGeometry(QtCore.QRect(290, 200, 151, 16))
        self.intLabel.setObjectName("intLabel")
        self.intSelect = QtWidgets.QComboBox(self.centralwidget)
        self.intSelect.setGeometry(QtCore.QRect(290, 220, 191, 22))
        self.intSelect.setAcceptDrops(False)
        self.intSelect.setEditable(False)
        self.intSelect.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.intSelect.setObjectName("intSelect")
        self.intSelect.addItem("")
        self.intSelect.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionView_database = QtWidgets.QAction(MainWindow)
        self.actionView_database.setObjectName("actionView_database")
        self.actionView_stored_files = QtWidgets.QAction(MainWindow)
        self.actionView_stored_files.setObjectName("actionView_stored_files")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuMenu.addAction(self.actionView_database)
        self.menuMenu.addAction(self.actionView_stored_files)
        self.menuMenu.addAction(self.actionQuit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Byteconnect - Early Beta v2.1576"))
        self.certName.setText(_translate("MainWindow", "Certificate name"))
        self.certPass.setText(_translate("MainWindow", "Certificate password"))
        self.loadCerts.setText(_translate("MainWindow", "Load your certificate in both formats:"))
        self.actionLog.setText(_translate("MainWindow", "Recent actions log:"))
        self.sendFile.setText(_translate("MainWindow", "Send a file:"))
        self.sendButton.setText(_translate("MainWindow", "SEND"))
        self.pem.setText(_translate("MainWindow", "PEM"))
        self.pkcs12.setText(_translate("MainWindow", "PKCS12"))
        self.loadPEM.setText(_translate("MainWindow", "Load"))
        self.loadP12.setText(_translate("MainWindow", "Load"))
        self.loadFileButton.setText(_translate("MainWindow", "Load"))
        self.nameIPInput.setItemText(0, _translate("MainWindow", "Jméno 1"))
        self.nameIPInput.setItemText(1, _translate("MainWindow", "Jméno 2"))
        self.recIP.setText(_translate("MainWindow", "Receiver IP address / Name if already known"))
        self.impossible.setText(_translate("MainWindow", "Impossible to send selected file, receiver unavailable."))
        self.storeFile.setText(_translate("MainWindow", "Store the file and send when possible?"))
        self.storeYes.setText(_translate("MainWindow", "Yes, store"))
        self.storeNo.setText(_translate("MainWindow", "No, don\'t store"))
        self.storeTime.setText(_translate("MainWindow", "Time in hours for which the file should be stored:"))
        self.fileSent.setText(_translate("MainWindow", "File sent."))
        self.check.setText(_translate("MainWindow", "Check credentials"))
        self.succLoad.setText(_translate("MainWindow", "Certificates loaded successfully."))
        self.unsuccLoad.setText(_translate("MainWindow", "Incorrect name or password."))
        self.intLabel.setText(_translate("MainWindow", "Select interface:"))
        self.intSelect.setItemText(0, _translate("MainWindow", "Jméno 1"))
        self.intSelect.setItemText(1, _translate("MainWindow", "Jméno 2"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionView_database.setText(_translate("MainWindow", "View database"))
        self.actionView_stored_files.setText(_translate("MainWindow", "View stored files"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))