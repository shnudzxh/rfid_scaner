# -*- coding: utf-8 -*-

import telnetlib

class reader_con:
    def __init__(self,host ='192.168.1.108',port = 23,username ='alien',passwd ='password',mode = "telnet",debuglevel = 0):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        self.mode = mode
        self.debug_level= debuglevel

        if self.debug_level:
            print "reader_con details:"
            print self.host,"\t",self.port,"\t",self.username,"\t",self.passwd,"\t",self.mode,"\t",self.debug_level
        
        if self.mode == "ssh":
            self.ssh_error()

    def ssh_error(self):
        print "ssh for reader control is not ready now"

    #使用telnet开关读卡器的自动扫描模式
    def scan_con(self,start_con):
        if self.mode == "telnet":
            self.con = telnetlib.Telnet(self.host, self.port, timeout=1)
            self.con.set_debuglevel(self.debug_level)
            
            # 输入登录用户名  
            self.con.read_until('Username>')  
            self.con.write(self.username + '\n') 
            
            # 输入登录密码  
            self.con.read_until('Password>')  
            self.con.write(self.passwd + '\n')

            self.con.read_until('Alien>')
            
            if start_con:
                #start collection
                self.con.write('automode=on')
                self.con.write('\n') 
                print "Scanning mode started"
            else: 
                #stop collection
                self.con.write('automode=off')
                self.con.write('\n') 
                print "Scanning mode stoped"
                
            #执行完毕后，终止Telnet连接（或输入exit退出）  
            self.con.read_until('Alien>')
            self.con.close() #self.con.write('exit\n')
        elif self.mode == "ssh":
            self.ssh_error() 