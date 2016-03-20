__author__ = 'eric'


import os
import sys
import socket
import logging

sys.path.append("C:\\Users\\eric\\PycharmProjects\\NetworkAutomation")

from NetworkAutomation.NetworkAPI.CiscoAPI.Common import ssh_connect

class collect(ssh_connect.Connect):
    def __init__(self):
        ssh_connect.Connect.__init__(ip,port,user,passwd)
        self.ssh = ssh_connect.Connect.__connect__('en')

    def collectCPU(self):
        pass


collect(ip='192.168.133.200 ',port=22,user='kft',password='123456')