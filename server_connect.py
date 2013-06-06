#-*- coding:utf-8 -*-

#
# name will be rewritten in time
#

import paramiko
import re

class ServerList():
    server_list = []
    def __init__(self):
        pass

    def add_server_node(self, server):
        print server
        if not server in self.server_list and server != None:
            self.server_list.append(server)
            print "server named "+server.name+" added"
            return True
        else:
            print "server already in list"
            return False

class vpnConfNode():
    
    def __init__(self,name):
        self.name = name
        self.conf = {}

class vpnServerNode():

    def __init__(self):
        self.name = ""
        self.ip = ""
        self.user = ""
        self.passwd = ""
        self.port = "22"
        self.conf = {}

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

    def connect_to_server(self):
        paramiko.util.log_to_file('ssh_'+self.name+'_session.log')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print "trying.."
        # self.ssh.connect(self.ip, self.port, self.user, self.passwd)
        try:
            self.ssh.connect(self.ip, self.port, self.user, self.passwd)
            print 'Connected to server'
            return True
        except:
            print 'Error connect'
            return False

    def is_openvpn_installed(self):
        stdin, stdout, stderr = self.ssh.exec_command("openvpn --version")
        # print stdout
        output = ""
        for line in stdout:
            output = output + line.strip('\n')

        if output != "":
            return True
        else:
            return False

    def what_running(self):
        stdin, stdout, stderr = self.ssh.exec_command("service openvpn status")

        output = ""
        for line in stdout:
            output = output + line.strip('\n')

        return output

    def conf_exist(self):
        stdin, stdout, stderr = self.ssh.exec_command("ls /etc/openvpn/*.conf")

        output = ""
        for line in stdout:
            line = line.replace("/etc/openvpn/","")
            output = output + line
            conf_name = line.replace(".conf","").replace('\n',"")
            node = vpnConfNode(conf_name)

            self.conf[conf_name] = node

        return output

    def get_conf_file(self, conf_file):
        print conf_file.name
        print conf_file
        stdin, stdout, stderr = self.ssh.exec_command("cat /etc/openvpn/"+conf_file.name+".conf")



        output = ""
        for line in stdout:
            line_parsing = re.sub("#.*\\n|;.*\\n", "", line).strip()
            line_array = line_parsing.split(" ",1)
            if line_array.__len__() > 1:
                conf_file.conf[line_array[0]] = line_array[1]
            else:
                conf_file.conf[line_array[0]] = True
            output = output + line_parsing

        return output


def get_config(config_file_name=None):
    if config_file_name==None:
        
        config_file = open("config", "rw")

    else:
        config_file = open(config_file_name,"rw")


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
            config_val = config_line_array[1].split(";")[0]
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

    if server != None:
        server_list.add_server_node(server)   


    return server_list         


# server_list = get_config()

# main_server = server_list.server_list[0]
# print main_server.connect_to_server()

# print main_server.conf_exist()
