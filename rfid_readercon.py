# -*- coding: utf-8 -*-

import telnetlib

class reader_con:
    def __init__(self,host ='192.168.1.105',port = 23,username ='alien',passwd ='password',mode = "telnet",debuglevel = 0):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        self.mode = mode
        self.debug_level= debuglevel

        if debuglevel:
            print "reader_con details:"
            print self.host,"\t",self.port,"\t",self.username,"\t",self.passwd,"\t",self.mode,"\t",self.debug_level
        self.ssh_error()

    def ssh_error(self):
        print "ssh is not ready now"

    #ʹ��telnet���ض��������Զ�ɨ��ģʽ
    def scan_con(self,start_con):
        if self.mode == "telnet":
            self.con = telnetlib.Telnet(self.host, self.port, timeout=1)
            self.con.set_debuglevel(self.debug_level)
            
            # �����¼�û���  
            tn.read_until('Username>')  
            tn.write(username + '\n') 
            
            # �����¼����  
            tn.read_until('Password>')  
            tn.write(passwd + '\n')

            tn.read_until('Alien>')
            
            if start_con:
                #start collection
                tn.write('automode=on')
                tn.write('\n') 
                print "Scanning mode started"
            else: 
                #stop collection
                tn.write('automode=off')
                tn.write('\n') 
                print "Scanning mode stoped"
                
            #ִ����Ϻ���ֹTelnet���ӣ�������exit�˳���  
            tn.read_until('Alien>')
            tn.close() #tn.write('exit\n')
        elif self.mode == "ssh":
            self.ssh_error() 
        
        