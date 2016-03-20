__author__ = 'eric'


import os
import sys
import time

sys.path.append('/home/eric/NetworkAutomation')
from DevicesApi.Devices.Login.ssh import cisco

data = {
    'effect' :  'show device config',
    'device' :  'C7200-ADVSECURITYK9-M',
    'connect': {'ip': '192.168.133.200',
                'port' : 22,
                'username': 'kft',
                'password': '123456',
                },

    'enable' : {
        'enable'   : True,
        'password' : '123456',
        'input'    : ['copy startup-config tftp',
                      '192.168.133.158',
                      'startup-config-%s' %time.time()],
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

}


class get_config_file:

    def __init__(self,data):
        self.data = data


    def __call__(self):
        c = cisco.Connect(self.data)
        c.connect()
        c.enable()
        output = c.show()
        c.close()
        print output



if __name__ == '__main__':
    s = get_config_file(data)
    s.__call__()