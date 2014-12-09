# -*- coding: utf-8 -*-

import time,sqlite3

class rfid_devicemanager:
    def __init__(self,debuglevel=False):
        self.devlist = list()
        self.debuglevel = debuglevel
        try:
            self.conn = sqlite3.connect('rfid.db',check_same_thread = False)
        except :
            print "Unexpected error happened devmgr_init"
            
        try:
            self.c = self.conn.cursor()
        except :
            print "Error create cursor"
            
        try:
            self.c.execute('''CREATE TABLE history\
                 (hashid text, time_readable text,time real)''')
        except :
            print "Error create Table"
            

    def adddev(self,hashid):
        print "I'll add\t",hashid
        # if hashid in self.devlist:
            # #self.showall()
            # pass
            # if self.debuglevel :
                # print "Already in list"
        # else:
            # self.devlist.append(hashid)
            # self.showall()
            
    def logDB(self,hashid):
        str_exec = '''INSERT INTO history VALUES("%s","%s",%f)'''\
                    %((hashid),time.asctime(),time.time())
        print str_exec
        try:
            self.c.execute(str_exec)
            self.conn.commit()
        except Exception, e:
            print "Error when Insert into SQL:",e

    def showall(self):
        pass
        # print "*"*20
        # for i in self.devlist:
            # print i
        # print "*"*20

    def op2files(self):
        pass
        # fname = time.strftime("ScanList-%Y-%m-%d-%A-%H-%M.txt")
        # f = open(fname,'w')
        # for i in self.devlist:
            # str2write = str(i)+"\n"
            # #str2write = #check DB and output str to str2write
            # if self.debuglevel :
                # print str2write
            # f.write(str2write)
        # f.close()
    