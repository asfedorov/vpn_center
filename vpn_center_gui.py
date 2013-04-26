# -*- coding:utf-8-*-
import sys, random

from PyQt4 import QtCore, QtGui, Qt
from ui_main import Ui_MainWindow

import server_connect

class ServerGUI_Node(server_connect.vpnServerNode):
    def __init__(self,mainform_obj,name="",ip="",user="",passwd="",port="22"):
        self.name = name
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = port
        self.mainform_obj = mainform_obj
        self.make_group_box()

    def make_group_box(self):
        self.group_box = QtGui.QGroupBox()

        # print name.toUtf8()
        if self.name != "":
            # name = name.decode("utf-8")
            self.group_box.setTitle(self.name.decode("utf-8"))
        else:
            self.name = self.ui.server_name.text()
            if self.name != "":
                self.group_box.setTitle(str(self.name.toUtf8()).decode("utf-8"))
            else:
                self.group_box.setTitle("New Server")

        ##### ip configs #####

        ip_row_layout = QtGui.QHBoxLayout()
        
        ip_row_label = QtGui.QLabel("IP Address")
        ip_row_label.setFixedWidth(100)
        ip_row_delimeter = QtGui.QLabel(" : ")
        if self.port == "22":
            ip_row_value = QtGui.QLineEdit(self.ip)
        else:
            ip_row_value = QtGui.QLineEdit(self.ip+":"+self.port)
        ip_row_value.setFixedWidth(200)

        ip_row_layout.addWidget(ip_row_label)
        ip_row_layout.addWidget(ip_row_delimeter)
        ip_row_layout.addWidget(ip_row_value)

        ##### user configs #####

        user_row_layout = QtGui.QHBoxLayout()
        
        user_row_label = QtGui.QLabel("User Name")
        user_row_label.setFixedWidth(100)
        user_row_delimeter = QtGui.QLabel(" : ")
        user_row_value = QtGui.QLineEdit(self.user)
        user_row_value.setFixedWidth(200)

        user_row_layout.addWidget(user_row_label)
        user_row_layout.addWidget(user_row_delimeter)
        user_row_layout.addWidget(user_row_value)

        ##### passwd configs #####

        passwd_row_layout = QtGui.QHBoxLayout()
        
        passwd_row_label = QtGui.QLabel("Passwd")
        passwd_row_label.setFixedWidth(100)
        passwd_row_delimeter = QtGui.QLabel(" : ")
        passwd_row_value = QtGui.QLineEdit(self.passwd)
        passwd_row_value.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        passwd_row_value.setFixedWidth(200)

        passwd_row_layout.addWidget(passwd_row_label)
        passwd_row_layout.addWidget(passwd_row_delimeter)
        passwd_row_layout.addWidget(passwd_row_value)

        ##### buttons #####

        delete_button = QtGui.QPushButton()
        delete_button.setText("Delete Server")

        ##### server layout #####

        server_config_layout = QtGui.QVBoxLayout()

        server_config_layout.addLayout(ip_row_layout)
        server_config_layout.addLayout(user_row_layout)
        server_config_layout.addLayout(passwd_row_layout)
        server_config_layout.addWidget(delete_button)


        self.group_box.setLayout(server_config_layout)  
        self.group_box.adjustSize()

        self.mainform_obj.connect(delete_button, QtCore.SIGNAL('pressed()'),self.mainform_obj.remove_server_from_list)

    def make_server_tab(self):
        pass


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)   
        # super(Window, self).__init__(parent)
        self.ui.setupUi(self)

        self.server_list_layout = QtGui.QVBoxLayout()
        self.ui.server_list_container.setLayout(self.server_list_layout)

        self.connect(self.ui.add_server_button, QtCore.SIGNAL('pressed()'),self.add_server_to_list)

        self.get_servers_from_config()

    def remove_server_from_list(self):
        # print "Nya"
        button = self.sender()
        group_box = button.parentWidget()
        # layout = group_box.parentLayout()
        # print layout
        # layout.removeItem(group_box)
        i = self.server_list_layout.indexOf(group_box)
        # print i
        self.server_list_layout.removeItem(self.server_list_layout.itemAt(i))
        group_box.hide()
        # print str(parent)

    def add_server_to_list(self,name="",ip="",user="",passwd="",port="22"):
        
        server = ServerGUI_Node(self,name,ip,user,passwd,port)
        
        self.server_list_layout.addWidget(server.group_box)
        
        
        self.create_server_tab(name.decode("utf-8"))

        # self.ui.server_list_layout.addWidget(group_box)

    def get_servers_from_config(self):
        server_list = server_connect.get_config()
        for server in server_list.server_list:
            self.add_server_to_list(server.name,server.ip,server.user,server.passwd,server.port)

    def create_server_tab(self,name=""):
        server_widget = QtGui.QScrollArea()
        self.ui.tabWidget.addTab(server_widget,name)



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
