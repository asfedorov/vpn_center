# -*- coding:utf-8-*-
import sys, random

from PyQt4 import QtCore, QtGui, Qt
from ui_main import Ui_MainWindow

import __main__


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)   
        # super(Window, self).__init__(parent)
        self.ui.setupUi(self)

        self.connect(self.ui.add_server_button, QtCore.SIGNAL('pressed()'),self.add_server_to_list)

    def add_server_to_list(self):
        group_box = QtGui.QGroupBox(self)

        name = self.ui.server_name.text()
        # print name.toUtf8()
        if name != "":
            group_box.setTitle(str(name.toUtf8()).decode("utf-8"))
        else:
            group_box.setTitle("New Server")

        ##### ip configs #####

        ip_row_layout = QtGui.QHBoxLayout()
        
        ip_row_label = QtGui.QLabel("IP Address")
        ip_row_value = QtGui.QLineEdit()

        ip_row_layout.addWidget(ip_row_label)
        ip_row_layout.addWidget(ip_row_value)


        server_config_layout = QtGui.QVBoxLayout()

        server_config_layout.addLayout(ip_row_layout)


        group_box.setLayout(server_config_layout)            
        
        self.ui.server_list_layout.addWidget(group_box)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("VPN Center")
    myapp = MainForm()
    myapp.show()
    # myapp.add_server_to_list()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
