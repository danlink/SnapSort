# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Daniel\git\SnapSort\SnapSort/gui\waitwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Waitwin(object):
    def setupUi(self, Waitwin):
        Waitwin.setObjectName("Waitwin")
        Waitwin.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Waitwin)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButtonStop = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.gridLayout.addWidget(self.pushButtonStop, 3, 0, 1, 1)
        self.pushButtonRename = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonRename.setObjectName("pushButtonRename")
        self.gridLayout.addWidget(self.pushButtonRename, 2, 0, 1, 1)
        self.selectDirButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.selectDirButton.setObjectName("selectDirButton")
        self.gridLayout.addWidget(self.selectDirButton, 1, 0, 1, 1)

        self.retranslateUi(Waitwin)
        QtCore.QMetaObject.connectSlotsByName(Waitwin)

    def retranslateUi(self, Waitwin):
        _translate = QtCore.QCoreApplication.translate
        Waitwin.setWindowTitle(_translate("Waitwin", "Form"))
        self.label.setText(_translate("Waitwin", "waiting..."))
        self.pushButtonStop.setText(_translate("Waitwin", "Stop"))
        self.pushButtonRename.setText(_translate("Waitwin", "Open rename dialog"))
        self.selectDirButton.setText(_translate("Waitwin", "Select directory"))

