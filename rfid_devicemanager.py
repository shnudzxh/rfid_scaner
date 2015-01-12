# -*- coding: utf-8 -*-

import time,sqlite3,threading

class rfid_devicemanager:
    def __init__(self,debuglevel=False):
        self.devlist = list()
        self.debuglevel = debuglevel
        self.pairdic = dict()
        try:
            self.conn = sqlite3.connect('rfid_db.db',check_same_thread = False)
        except :
            print "Unexpected error happened devmgr_init"
            
        try:
            self.c = self.conn.cursor()
        except :
            print "Error create cursor"
            
        try:
            self.c.execute('''CREATE TABLE history\
                 (hashid text,time real)''')
        except :
            print "Error create Table history"

        try:
            self.c.execute('''CREATE TABLE pair\
                 (carID text, peopleID text)''')
        except :
            print "Error create Table pair"

    def logDB(self,hashid):
        #Insert tagID to table as log data
        tm = time.time()
        str_exec = '''INSERT INTO history VALUES("%s",%f)'''\
                    %((hashid),tm)
        #print str_exec
        try:
            self.c.execute(str_exec)
            self.conn.commit()
        except Exception, e:
            print "Error when Insert into SQL:",e

        if self.pairdic.has_key(hashid):
            #hashid is a car ID,I'll search people ID in history
            peoID = self.pairdic.get(hashid)
            t = threading.Timer(5.0,self.checkinhistory,[peoID,tm])
            t.start()
        #else:
            #print hashid,"Not a car in pair I'll ignore"

    def load_db2dic(self,table_name):
        str_exec = '''select * from %s'''\
                %(table_name)

        try:
            self.c.execute(str_exec)
        except Exception, e:
            print "Error when check pair:",e
        
        i=0
        for row in self.c:
            i=i+1
            carid,peoid = row
            self.pairdic[carid]=peoid
        print "load %d Pair(s)"%(i)

        #print self.pairdic

    def checkinhistory(self,hashid,tm):
        str_exec = '''SELECT * FROM history WHERE hashid="%s" AND time<%s AND time>%s'''\
                %(hashid,tm+5,tm-5)
        #print str_exec

        try:
            self.c.execute(str_exec)
        except Exception, e:
            print "Error when check carid in history:",e

        #print "after check i get:",self.c.fetchall()
        if not self.c.fetchall():
            print "*********",hashid,"******warnning*******"
        

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
    