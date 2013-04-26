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

    def connect_to_server(self):
        paramiko.util.log_to_file('ssh_'+self.name+'_session.log')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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
            output = output + line.strip('\n').replace("/etc/openvpn/","")

        return output


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

    server_list.add_server_node(server)   

    return server_list         


server_list = get_config()

main_server = server_list.server_list[0]
print main_server.connect_to_server()

print main_server.conf_exist()
