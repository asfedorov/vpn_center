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
        if name != "":
            group_box.setTitle(str(name))
        else:
            group_box.setTitle("New Server")

        server_config = QtGui.QTableWidget(self)

        server_config_layout = QtGui.QVBoxLayout(self)

        server_config_layout.addWidget(server_config)

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
