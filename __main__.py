#-*- coding:utf-8 -*-

#
# name will be rewritten in time
#

import paramiko

class ServerList():
    server_list = []
    def __init__(self):
        pass

    def add_server_node(self, server):
        if not server in self.server_list and server != None:
            self.server_list.append(server)
            print "server named "+server.name+" added"
            return True
        else:
            print "server already in list"
            return False

class vpnServerNode():
    name = ""
    ip = ""
    user = ""
    passwd = ""
    port = "22"
    def __init__(self):
        pass

    def set_name(self, name):
        self.name = name
    def set_ip(self, ip):
        self.ip = ip
    def set_user(self, user):
        self.user = user
    def set_passwd(self, passwd):
        self.passwd = passwd
    def set_port(self, port):
        self.port = port


def get_config(config_file=None):
    if config_file==None:
        config_file = open("config", "r")

    server_list = ServerList()
    server = None
    for config_line in config_file.readlines():
        if config_line.replace("\n","") == "[server]":
            server_list.add_server_node(server)
            server = vpnServerNode()
        elif config_line.__len__() < 7:
            continue
        else:
            config_line_array = config_line.split("=")
            config_var = config_line_array[0]
            config_val = config_line_array[1].replace("\n","")
            if config_var == "Name":
                server.set_name(config_val)
            if config_var == "IP":
                server.set_ip(config_val)
            if config_var == "User":
                server.set_user(config_val)
            if config_var == "Passwd":
                server.set_passwd(config_val)
            if config_var == "Port":
                server.set_port(config_val)

    server_list.add_server_node(server)            



get_config()