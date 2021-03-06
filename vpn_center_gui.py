# -*- coding:utf-8-*-
import sys, random

from PyQt4 import QtCore, QtGui, Qt
from ui_main import Ui_MainWindow

import server_connect

class ServerGUI_Node(server_connect.vpnServerNode):
    
    def __init__(self,mainform_obj,name="",ip="",user="",passwd="",port=22):
        self.name = name
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = int(port)
        self.mainform_obj = mainform_obj
        self.conf_box_pointer_list = {}
        self.conf = {}

        self.make_group_box()
        

    def make_group_box(self):
        self.group_box = QtGui.QGroupBox()


        ## magick here. with this statement signal-to-slot connection 
        ## for function defined in other class, that MainForm
        ## works fine (at least i see its' output)
        self.group_box.obj_pointer = self

        # print name.toUtf8()
        if self.name != "":
            # name = name.decode("utf-8")
            self.group_box.setTitle(self.name.decode("utf-8"))
        else:
            self.name = self.mainform_obj.ui.server_name.text()
            if self.name != "":
                self.group_box.setTitle(str(self.name.toUtf8()).decode("utf-8"))
            else:
                self.group_box.setTitle("New Server")
                self.name = "New Server"

        ##### ip configs #####

        ip_row_layout = QtGui.QHBoxLayout()
        
        ip_row_label = QtGui.QLabel("IP Address")
        ip_row_label.setFixedWidth(100)
        ip_row_delimeter = QtGui.QLabel(" : ")
        if self.port == 22:
            ip_row_value = QtGui.QLineEdit(self.ip)
        else:
            ip_row_value = QtGui.QLineEdit(self.ip+":"+str(self.port))
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

        connect_button = QtGui.QPushButton()
        connect_button.setText("Connect to Server")

        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addWidget(connect_button)
        buttons_layout.addWidget(delete_button)

        ##### server layout #####

        server_config_layout = QtGui.QVBoxLayout()

        server_config_layout.addLayout(ip_row_layout)
        server_config_layout.addLayout(user_row_layout)
        server_config_layout.addLayout(passwd_row_layout)
        server_config_layout.addLayout(buttons_layout)


        self.group_box.setLayout(server_config_layout)  
        self.group_box.adjustSize()

        ##### signals connections #####

        self.mainform_obj.connect(delete_button, 
            QtCore.SIGNAL('pressed()'),self.remove_server)


        self.mainform_obj.connect(connect_button, 
            QtCore.SIGNAL('pressed()'), self.fill_server_tab)

        self.mainform_obj.connect(ip_row_value, 
            QtCore.SIGNAL('textChanged(QString)'), self.ip_changed)
        self.mainform_obj.connect(user_row_value, 
            QtCore.SIGNAL('textChanged(QString)'), self.user_changed)
        self.mainform_obj.connect(passwd_row_value, 
            QtCore.SIGNAL('textChanged(QString)'), self.passwd_changed)


        ##### tab for configuration #####
        self.conf_tab_pointer = self.make_server_tab()
        self.fill_server_tab()
        # print self
        # print self.conf_box_pointer_list
        # print self.mainform_obj.ui.tabWidget.indexOf(self.conf_tab_pointer)


    def ip_changed(self, q_ip_str):
        self.ip = str(q_ip_str)

    def user_changed(self, q_user_str):
        self.user = str(q_user_str)

    def passwd_changed(self, q_passwd_str):
        self.passwd = str(q_passwd_str)
        

    def make_server_tab(self):

        server_tab_widget = QtGui.QWidget()

        server_tab_widget.content_set = "conf"

        self.server_tab_widget = server_tab_widget

        server_layout = QtGui.QVBoxLayout()
        server_widget = QtGui.QScrollArea()

        conf_row_add_button = QtGui.QPushButton()
        conf_row_add_button.setText("+1 line")

        server_layout.addWidget(server_widget)
        server_layout.addWidget(conf_row_add_button)
        server_tab_widget.setLayout(server_layout)

        self.mainform_obj.connect(conf_row_add_button, 
            QtCore.SIGNAL('pressed()'), self.add_conf_line)


        self.mainform_obj.ui.tabWidget.addTab(server_tab_widget,
            str(self.name).decode("utf-8"))

        return server_widget

    def fill_server_tab(self):

        server_widget = self.conf_tab_pointer

        self.connected = self.connect_to_server()
        print self.connected

        if self.connected == True:
            connection_label = QtGui.QLabel("Connected")
            
            #conf = self.get_conf_file()
            
            conf_files = self.conf_exist()
            # conf_files_array = conf_files.split("\n")

            for conf_file_name in self.conf:
                conf_file = self.conf[conf_file_name]
                if conf_file.name != "":

                    conf_box = QtGui.QGroupBox()
                    conf_box.setTitle(conf_file.name)

                    conf_layout = QtGui.QVBoxLayout()
                    self.conf = self.get_conf_file(conf_file)
                    conf_box.setLayout(conf_layout)

                    # print conf_file
                    # print conf_file.conf

                    for conf_line in conf_file.conf:

                        conf_row_box = self.create_conf_row(conf_line,
                            str(conf_file.conf[conf_line]))
                        
                        conf_layout.addWidget(conf_row_box)

                    server_widget.setWidget(conf_box)

                    self.conf_box_pointer_list[conf_file.name] = conf_box

        else:
            connection_label = QtGui.QLabel("Not Connected")

            server_widget.setWidget(connection_label)

    def create_conf_row(self,label,value=""):
        conf_row_layout = QtGui.QHBoxLayout()
        
        conf_row_label = QtGui.QLabel(label)
        conf_row_label.setFixedWidth(100)
        conf_row_delimeter = QtGui.QLabel(" : ")
        conf_row_value = QtGui.QLineEdit(value)
        conf_row_value.setFixedWidth(200)

        conf_row_layout.addWidget(conf_row_label)
        conf_row_layout.addWidget(conf_row_delimeter)
        conf_row_layout.addWidget(conf_row_value)

        conf_row_del_button = QtGui.QPushButton()
        conf_row_del_button.setText("x__X")

        self.mainform_obj.connect(conf_row_del_button, 
            QtCore.SIGNAL('pressed()'), self.remove_conf_line)

        conf_row_layout.addWidget(conf_row_del_button)

        conf_row_box = QtGui.QGroupBox()

        conf_row_box.setContentsMargins(10,3,10,3)
        
        conf_row_box.setLayout(conf_row_layout)

        return conf_row_box

    def remove_server(self):
        self.conf_tab_pointer.parentWidget().setParent(None)
        # print self.group_box.parentWidget()
        self.group_box.setParent(None)
        # print self.mainform_obj.server_pointers
        # print 
        self.mainform_obj.server_pointers.remove(self)
        print "::",self.mainform_obj.server_pointers

        
    def remove_conf_line(self):
        button = self.mainform_obj.sender()
        conf_line = button.parentWidget()
        # conf_line.setParent(None)
        conf_row_label = str(conf_line.children()[1].text())
        conf_file = str(conf_line.parentWidget().title())

        self.conf[conf_file].conf.pop(conf_row_label)
        conf_line.setParent(None)
        # print conf_row_label

    def add_conf_line(self):

        button = self.mainform_obj.sender()
        conf_line = button.parentWidget()

        ### A lot of work need to be redone there
        ### chosing to which conf file to add
        ### etc...
        
        ### there.. need to pick it in any way
        #conf_file = str(conf_line.parentWidget().title())
        # print conf_line.children()[1].children()[0].children()[0].title()
        conf_file = str(conf_line.children()[1].children()[0].children()[0].title())

        dialog = QtGui.QInputDialog()
        dialog.setLabelText("Enter config line label")

        dialog.exec_()

        label = str(dialog.textValue()).strip()

        if label != "":
            conf_row_box = self.create_conf_row(label)

            conf_box = self.conf_box_pointer_list[conf_file]

            conf_box.children()[0].addWidget(conf_row_box)


        

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.server_pointers = []
        self.config_file = "config"

        self.server_list_layout = QtGui.QVBoxLayout()
        self.ui.server_list_container.setLayout(self.server_list_layout)

        self.ui.tab.content_set = "server_list"

        self.connect(self.ui.add_server_button, 
            QtCore.SIGNAL('pressed()'),self.add_server_to_list)

        self.connect(self.ui.tabWidget,
            QtCore.SIGNAL("currentChanged(int)"),self.tab_changed)

        ### menu triggers
        ### wonder if i can connect this ways buttons, etc...
        ### lazy to read manual for it :P
        self.ui.actionExit.triggered.connect(QtGui.qApp.quit)
        ### :'-(((can not connect to a function)))-':
        #self.ui.actionOpen.triggered.connect(self.open_config_file())
        self.connect(self.ui.actionOpen,
            QtCore.SIGNAL("triggered()"),self.open_config_file)

        self.get_servers_from_config()

        

    def open_config_file(self):
        open_dialog = QtGui.QFileDialog()
        # open_dialog.exec_()

        # print open_dialog

        self.config_file = open_dialog.getOpenFileName()
        self.rebuild_config_gui(self.config_file)

    def rebuild_config_gui(self, config_file):
        print self.server_pointers
        for server in self.server_pointers:
            server.remove_server()
            print self.server_pointers

        self.get_servers_from_config(config_file)


    def add_server_to_list(self,name="",ip="",user="",passwd="",port="22"):
        
        server = ServerGUI_Node(self,name,ip,user,passwd,port)
        if self.server_pointers != None:
            self.server_pointers.append(server)
        else:
            self.server_pointers = []
            self.server_pointers.append(server)

        self.server_list_layout.addWidget(server.group_box)
        

        # self.ui.server_list_layout.addWidget(group_box)

    def get_servers_from_config(self, config_file=None):
        server_list = server_connect.get_config(config_file)
        print server_list.server_list
        for server in server_list.server_list:

            self.add_server_to_list(server.name,server.ip,
                server.user,server.passwd,server.port)

    def set_edit_conf_menu_active(self):
        self.ui.menuConfiguration.setDisabled(False)

    def tab_changed(self, i):
        if self.ui.tabWidget.currentWidget().content_set == "conf":
            self.set_edit_conf_menu_active()
        elif self.ui.tabWidget.currentWidget().content_set == "server_list":
            self.ui.menuConfiguration.setDisabled(True)
    



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
