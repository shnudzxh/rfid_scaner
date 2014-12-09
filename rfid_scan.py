# -*- coding: utf-8 -*-
import socket, traceback, os, sys,time,platform
from threading import *
from gpio import *
from rfid_xml import *          #XML解析部分,返回UID的hash
from rfid_readercon import *    #与读卡器连接,控制扫描模式的开关
from rfid_devicemanager import *

#for socket
address = ('', 4000) 

#tcp socket处理进程
def handlechild(clientsock):
    #print "New child", currentThread().getName()
    #print "Got connection from", clientsock.getpeername()
    while 1:
        try:
            data = clientsock.recv(8192)
            if not len(data):
                break
            if len(data) == 8192:
                print "Socket buffer full"
            # print "*"*20,"received:"
            # print data
            # print "*"*20
            hashid_list = xmlparser.get_tagid(data)
            if hashid_list != None:
                for i in hashid_list:
                    dev.logDB(i)
        except socket.error, e:
            if ((e.args[0] == 10035) or (e.args[0] == 11)):
                continue
            else:
                print "Unexpected error happened:",e
                traceback.print_exc()

    # Close the connection
    clientsock.close()
    print "connection closed:\r\n"


#===================================
if (platform.system() != 'Windows'):
    g = rey_pyio()
    g.init_all()
    g.mode(21,g.IOIN)
#===================================
xmlparser = rfid_xml()
#测试XML解析TagID
#xmlparser.test_fun()
#===================================
rd_con = reader_con()
rd_con.scan_con(True)
#===================================
dev = rfid_devicemanager()
#===================================
# 创建tcpsocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#创建socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)#创建socket
s.setblocking(0)
s.bind(address)
s.listen(5)#开始监听
print "Start listen"
#===================================

#循环等待连接
while 1:
    if (platform.system() != 'Windows'):
        if g.read(21) == '0':
            break

    try:
        #print "waitting accept"
        clientsock, clientaddr = s.accept()#接受外部连接
        #print "connection from:\t",clientsock,clientaddr
    except KeyboardInterrupt:
        print "KeyBoard INT detected"
        break
    except socket.error, e:
        if ((e.args[0] == 10035) or (e.args[0] == 11)):
            continue
        else:
            print "Unexpected error happened:",e
            traceback.print_exc()
        break
    print "I'll start a Thread"
    t = Thread(target = handlechild, args = [clientsock])#创建进程
    t.setDaemon(0)#设置后台
    t.start()#start新进程

print "end of accecpt while"
#关闭scan模式
rd_con.scan_con(False)
dev.op2files()
