# -*- coding: utf-8 -*-
import socket, traceback, os, sys,time,platform,threading,optparse
from gpio import *
from rfid_xml import *          #XML解析部分,返回UID的hash
from rfid_readercon import *    #与读卡器连接,控制扫描模式的开关
from rfid_devicemanager import *


 

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
                for hashID in hashid_list:
                    dev.logDB(hashID)
                    #print "I get a tag:",hashID
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
parser = optparse.OptionParser(
        usage = "%prog [options] port",
        description = "RFID Scanner",
        epilog = """\
Note it's me
""")

parser.add_option("-p", "--localport",
#        dest = "local_port",
        action = "store",
        type = 'int',
        help = "Local TCP port for comming tcp data",
        default = 4000
    )

parser.add_option("-i", "--gpio_in",
        dest = "gpio_in",
        action = "store",
        type = 'int',
        help = "GPIO Number for RaspberryPi Key(GPIO IN)",
        default = 21
    )

parser.add_option("-o", "--gpio_out",
        dest = "gpio_out",
        action = "store",
        type = 'int',
        help = "GPIO Number for RaspberryPi notice(like beep and LEDs GPIO IN)",
        default = 25
    )

parser.add_option("--reader_address",
        dest = "reader_address",
        action = "store",
        type = 'string',
        help = "Address for reader",
        default = "192.168.1.108"
    )

parser.add_option("--reader_port",
        dest = "reader_port",
        action = "store",
        type = 'int',
        help = "Port for reader",
        default = 23
    )

parser.add_option("--reader_username",
        dest = "reader_username",
        action = "store",
        type = 'string',
        help = "Username for reader",
        default = "alien"
    )

parser.add_option("--reader_password",
        dest = "reader_password",
        action = "store",
        type = 'string',
        help = "PassWord for reader",
        default = "password"
    )

parser.add_option("--reader_method",
        dest = "reader_method",
        action = "store",
        type = 'string',
        help = "Control method for reader",
        default = "telnet"
    )

#===================================
(options, args) = parser.parse_args()
#for local socket
address = ('', options.local_port)
#===================================
if (platform.system() != 'Windows'):
    g = rey_pyio()
    g.init_all()
    g.mode(gpio_in,g.IOIN)
#===================================
xmlparser = rfid_xml()
#测试XML解析TagID
#xmlparser.test_fun()
#===================================
rd_con = reader_con()
rd_con.scan_con(True)
#===================================
dev = rfid_devicemanager(options.reader_address,options.reader_port,options.username,options.password,options.reader_method)
dev.load_db2dic("pair")
#===================================
# 创建tcpsocket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.setblocking(0)
s.bind(address)
s.listen(5)#开始监听
print "Start listen"
#===================================

#循环等待连接
while 1:
    if (platform.system() != 'Windows'):
        if g.read(gpio_in) == '0':
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

    t = Thread(target = handlechild, args = [clientsock])#创建进程
    t.setDaemon(0)#设置后台
    t.start()#start新进程

print "end of accecpt while"
#关闭scan模式
rd_con.scan_con(False)
#dev.op2files()
