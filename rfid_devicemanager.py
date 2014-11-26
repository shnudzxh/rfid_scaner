# -*- coding: utf-8 -*-

import time

class rfid_devicemanager:
    def __init__(self,debuglevel=False):
        self.devlist = list()
        self.debuglevel = debuglevel

    def adddev(self,hashid):
        if hashid in self.devlist:
            #self.showall()
            pass
            if self.debuglevel :
                print "Already in list"
        else:
            self.devlist.append(hashid)
            self.showall()

    def showall(self):
        for i in self.devlist:
            print i

    def op2files(self):
        fname = time.strftime("ScanList-%Y-%m-%d-%A-%H-%M.txt")
        f = open(fname,'w')
        for i in self.devlist:
            str2write = str(i)+"\n"
            #str2write = #check DB and output str to str2write
            if self.debuglevel :
                print str2write
            f.write(str2write)
        f.close()
    