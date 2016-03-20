__author__ = 'eric'


import os
import sys
import time
import re

sys.path.append('/home/eric/NetworkAutomation')
from DevicesApi.Devices.Login.ssh import cisco

data = {
    'effect' :  'show device config',
    'device' :  'C7200-ADVSECURITYK9-M',
    'connect': {'ip': '192.168.133.254',
                'port' : 22,
                'username': 'kft',
                'password': '123456',
                },

    'enable' : {
        'enable'   : True,
        'password' : '123456',
        'input'    : ['show version',
                      'show inventory',
                      'show interfaces',],
        'output'   : [],
    },

    'configure' : {
        'configure' : False,
        'input'     : [],
        'output'    : [],
    },

    'logger':{
        'level'    : 'debug',
        'logfile' : '/tmp/%s-%s.log' % ('C7200-ADVSECURITYK9-M',time.time()),
    },

    'data': {},

}



#deviceinfo = {

    #'base_info':{
        #'device_name'          : '',
        #'device_soft_version'  : '',
        #'device_manufacturer'  : '',
        #'device_type'          : 'Switch',
        #'device_model'         : '',
        #'device_serial_number' : '',
        #'device_memory'        : '',
        #'device_cpu'           : '',
        #'device_uptime'        : '',
        #'device_configuration_register' : '',
    #},

    #module_info = {
        #    'NAME' : '',
        #    'DESCR': '',
        #    'PID'  : '',
        #    'VID'  : '',
        #    'SN'   : '',
    #},


    #'interfaces_info':{
        #'interface_Name'           : '',
        #'interface_Type'           : '',
        #'interface_IPaddress'      : '',
        #'interface_MACaddress'     : '',
        #'interface_Status'         : '',
        #'interface_runStatus'      : '',
        #'interface_Duplex'         : '',
        #'interface_MTU'            : '',
        #'interface_Vlan'           : '',



    # },

#}


class collect_device_info:

    def __init__(self,data):

        self.deviceinfo = {
            'base_info'       : {},
            'module_info'     : {},
            'interfaces_info' : {},
        }

        self.c = cisco.Connect(data)
        self.c.connect()
        self.c.enable()
        self.output = self.c.show()
        self.c.close()


    def base_info(self):

        for x in self.output['enable']['output'][0]:
            if re.search("Cisco IOS Software",x):
                self.deviceinfo['device_manufacturer'] = x.split()[0]
                self.deviceinfo['device_soft_version'] = ( x.split(',')[1] + ' ' + x.split(',')[2] )

            if re.search('uptime',x):
                self.deviceinfo['device_name'] = x.split()[0]
                self.deviceinfo['device_uptime'] = ' '.join(x.split()[1:])

            if re.search('bytes of memory',x):
                self.deviceinfo['device_model'] = x.split('processor')[0]
                self.deviceinfo['device_memory'] = x.split('with')[1]

            if re.search('CPU',x):
                self.deviceinfo['device_cpu'] = x.strip('\r')

            if re.search('Configuration register',x):
                self.deviceinfo['device_configuration_register'] = x.split()[-1]


        print self.deviceinfo


    def module_info(self):

        inventory = []

        for i in self.output['enable']['output'][1]:
            #print i
            inv = {}
            #inv = {
            #    'NAME' : '',
            #    'DESCR': '',
            #    'PID'  : '',
            #    'VID'  : '',
            #    'SN'   : '',
            #}

            if re.search('NAME:',i) and re.search('DESCR:',i):
                inv['NAME'], = re.findall('NAME: "(.*)",',i)
                inv['DESCR'], = re.findall('DESCR: "(.*)"',i)


            if re.search('PID:',i) and re.search('VID:',i) and re.search('SN:',i):
                inv['PID'], = re.findall('PID:\s(.*),\sVID:',i)
                inv['VID'], = re.findall('VID:(.*),\sSN:',i)
                inv['SN'], = re.findall('SN:\s(.*)',i)
                #search = re.findall('PID:\s(.*)\s,\sVID:\s(.*)\s,\sSN:\s(.*)',i)


            #print inv

            if inv:
                inventory.append(inv)

        print inventory


    def interfaces_info(self):
        for i in self.output['enable']['output'][2]:
            print i


        #print self.deviceinfo


if __name__ == '__main__':
    s = collect_device_info(data)
    s.base_info()

