# -*- coding: utf-8 -*-
import socket, traceback, os, sys,time
from threading import *

from rfid_xml import *          #XML解析部分,返回UID的hash
from rfid_readercon import *    #与读卡器连接,控制扫描模式的开关

print "start\r\n~~~~~~~~~~~~~"

#for socket
host = ''
port = 4000

#tcp socket处理进程
def handlechild(clientsock):
    #print "New child", currentThread().getName()
    #print "Got connection from", clientsock.getpeername()
    while 1:
        data = clientsock.recv(4096)
        if not len(data):
            break
        #print "received:\r\n",data        
        #clientsock.sendall(data)
        xmlparser.get_tagid(data)
    
    # Close the connection
    clientsock.close()
    print "connection closed:\r\n"


#===================================
xmlparser = rfid_xml()
#测试XML解析TagID
#xmlparser.test_fun()
#===================================
rd_con = reader_con()
rd_con.scan_con(True)
print "Done with telnet"
#===================================
# 创建tcpsocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#创建socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#创建socket
s.bind((host, port))#绑定端口
s.listen(5)#开始监听
print "Start listen"
#===================================

#循环等待连接
while 1:
    try:
        clientsock, clientaddr = s.accept()#接受外部连接
    except KeyboardInterrupt:
        raise
    except:
        #
        traceback.print_exc()
        continue

    t = Thread(target = handlechild, args = [clientsock])#创建进程
    t.setDaemon(1)#设置后台
    t.start()#start新进程

#关闭scan模式
rd_con.scan_con(False)
