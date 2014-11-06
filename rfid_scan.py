# -*- coding: utf-8 -*-
"""
帮助文件
help files:
1.xml.etree.ElementTree
http://www.cnblogs.com/ifantastic/archive/2013/04/12/3017110.html

2.string
http://blog.sina.com.cn/s/blog_89e14117010133vl.html

3.hashlib:
http://blog.csdn.net/zhaoweikid/article/details/1640516

4.telnet
http://blog.csdn.net/five3/article/details/8099997

"""
print "start\r\n~~~~~~~~~~~~~\r\n"


#RFID 范例数据
rfid_example_text ="""\
<Alien-RFID-Tag-List>
<Alien-RFID-Tag>
  <TagID>E200 3000 050B 0198 2090 421C</TagID>
  <DiscoveryTime>2014/11/06 14:56:48.140</DiscoveryTime>
  <LastSeenTime>2014/11/06 14:56:48.140</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
</Alien-RFID-Tag-List>
"""
import xml.etree.ElementTree as ET
import hashlib
import socket, traceback, os, sys,time
from threading import *
import telnetlib#for telnet login
import re

#for RFID
rfid_id=""
rfid_id_hash=""

#for socket
host = ''
port = 4000

#for telnet
telnet_host = '192.168.1.105'
telnet_port = 23
username = 'alien'
passwd = 'password'


#解析TagID函数,分析XML数据
def rey_get_tagid(rfid_text):
    print "~\r\n",rfid_text,"~\r\n"
    #过滤非法字符
    rfid_text=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",rfid_text)
    root = ET.fromstring(rfid_text)
    for child in root.iter('TagID'):
        rfid_id = child.text.replace(" ","")
        rfid_id_hash = hashlib.md5(rfid_id).hexdigest()
        print rfid_id,"\tmd5:\r\n",hashlib.md5(rfid_id).hexdigest(),"\r\n"
        #print rfid_id,"\tsha1:\r\n",hashlib.sha1(rfid_id).hexdigest(),"\r\n"
        #print rfid_id,"\tsha224:\r\n",hashlib.sha224(rfid_id).hexdigest(),"\r\n"
        #print rfid_id,"\tsha256:\r\n",hashlib.sha256(rfid_id).hexdigest(),"\r\n"
        #print rfid_id,"\tsha384:\r\n",hashlib.sha384(rfid_id).hexdigest(),"\r\n"
        #print rfid_id,"\tsha512:\r\n",hashlib.sha512(rfid_id).hexdigest(),"\r\n"
        
    print "\r\n=========\r\n"

#tcp socket进程
def handlechild(clientsock):
    #print "New child", currentThread().getName()
    #print "Got connection from", clientsock.getpeername()
    while 1:
        data = clientsock.recv(4096)
        if not len(data):
            break
        #print "received:\r\n",data        
        #clientsock.sendall(data)
        rey_get_tagid(data)
    
    # Close the connection
    clientsock.close()
    print "connection closed:\r\n"

#使用telnet开关读卡器的自动扫描模式
def rey_con(start_con):
    tn = telnetlib.Telnet(telnet_host, telnet_port, timeout=5)  
    #tn.set_debuglevel(2)
    
    # 输入登录用户名  
    tn.read_until('Username>')  
    tn.write(username + '\n') 
    
    # 输入登录密码  
    tn.read_until('Password>')  
    tn.write(passwd + '\n')
    
    
    
    tn.read_until('Alien>')
    
    if start_con:
        #start collection
        tn.write('automode=on')
        tn.write('\n') 
    else: 
        #stop collection
        tn.write('automode=off')
        tn.write('\n') 
        
    #执行完毕后，终止Telnet连接（或输入exit退出）  
    tn.read_until('Alien>')
    tn.close() #tn.write('exit\n')
    
    
# 创建tcpsocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#创建socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#创建socket
s.bind((host, port))#绑定端口
s.listen(5)#开始监听

print "start----------------------------"
#rey_get_tagid(rfid_example_text)#测试XML解析TagID

rey_con(1)#开启扫描模式

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

rey_con(0)

print "\r\n~~~~~~~~~~~~~\r\nDone"
x.close()
