#!/usr/bin/env python

__author__ = 'eric'


import os
import sys
import time
import paramiko
import logging



class Connect:

    def __init__(self,data):
        self.ip = data['connect']['ip']
        self.port = data['connect']['port']
        self.username = data['connect']['username']
        self.password = data['connect']['password']
        self.logfile = data['logger']['logfile']
        self.logging = logging
        self.data = data
        self.logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='{0}'.format(self.logfile),
                    filemode='w')


    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print 'Connecting {0}:{1}'.format(self.ip, self.port)
            self.logging.debug('Connecting {0}:{1}'.format(self.ip, self.port))

            self.ssh.connect(self.ip, username=self.username, password=self.password, allow_agent=False,look_for_keys=False)
            print 'Connected {0}:{1}'.format(self.ip, self.port)
            self.logging.debug('Connected {0}:{1}'.format(self.ip, self.port))
        except:
            print 'Connect {0}:{1} Error'.format(self.ip, self.port)
            self.logging.debug('Connect {0}:{1} Error'.format(self.ip, self.port))
            sys.exit(1)
        self.chan = self.ssh.invoke_shell()
        time.sleep(1)



    def enable(self):
        self.logging.debug('chan.sending "enable"')
        self.chan.send('enable\n')
        self.logging.debug('chan.send enable success')

        self.logging.debug('chan.sending enable password')
        self.chan.send('{0}\n'.format(self.data['enable']['password']))
        self.logging.debug('chan.send enable password success')

        time.sleep(1)

        self.logging.debug('chan.sending "ter length 0"')
        self.chan.send('ter length 0\n')
        self.logging.debug('chan.send "ter length 0" success')

        if self.data['enable']['enable'] is True:
            if self.data['enable']['input']:
                for i in self.data['enable']['input']:
                    print i
                    self.logging.debug('chan.sending "{0}"'.format(i))
                    self.chan.send('{0}\n'.format(i))
                    self.logging.debug('chan.send "{0}" success'.format(i))
                    time.sleep(3)

                    output = self.chan.recv(9999)
                    self.logging.debug('collect "{0}" info'.format(i))

                    self.data['enable']['output'].append(output.split('\n')[1:-2])
                    self.logging.debug('collect "{0}" success'.format(i))
                    time.sleep(1)




    def configure(self):
        if self.data['configure']['configure'] is True:

            self.logging.debug('chan.sending "configure terminal"')
            self.chan.send('configure terminal\n')
            self.logging.debug('chan.send "configure terminal" success')

            if data['configure']['input']:
                for i in self.data['configure']['input']:
                    print i
                    self.logging.debug('chan.sending "{0}"'.format(i))
                    self.chan.send('{0}\n'.format(i))
                    self.logging.debug('chan.send "{0}" success'.format(i))
                    time.sleep(1)

                    output = self.chan.recv(9999)
                    self.logging.debug('collect "{0}" info'.format(i))

                    self.data['configure']['output'].append(output.split('\n')[1:-2])
                    self.logging.debug('collect "{0}" success'.format(i))
                    time.sleep(1)

    def show(self):
        return self.data


    def close(self):
        self.chan.close()
        self.ssh.close()


if __name__ == "__main__":
    c = Connect()
    c.connect()
    c.enable()
    output=c.show()
    c.close()
    for i in output['enable']['output']:
       c = Connect()
       for x in i:
           print x

