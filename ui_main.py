# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri Apr 26 14:33:17 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(795, 597)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 791, 551))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(20, 30, 461, 471))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.server_list_container = QtGui.QWidget()
        self.server_list_container.setGeometry(QtCore.QRect(0, 0, 459, 469))
        self.server_list_container.setObjectName(_fromUtf8("server_list_container"))
        self.verticalLayoutWidget = QtGui.QWidget(self.server_list_container)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 461, 471))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.server_list_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.server_list_layout.setContentsMargins(-1, -1, -1, 0)
        self.server_list_layout.setObjectName(_fromUtf8("server_list_layout"))
        self.scrollArea.setWidget(self.server_list_container)
        self.add_server_button = QtGui.QPushButton(self.tab)
        self.add_server_button.setGeometry(QtCore.QRect(510, 30, 61, 51))
        self.add_server_button.setObjectName(_fromUtf8("add_server_button"))
        self.server_name = QtGui.QLineEdit(self.tab)
        self.server_name.setGeometry(QtCore.QRect(590, 40, 113, 27))
        self.server_name.setObjectName(_fromUtf8("server_name"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 795, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.add_server_button.setText(_translate("MainWindow", "Add", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Список серверов", None))

