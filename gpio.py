import os,time

class rey_pyio:
    def __init__(self):
        self.leds=[25,26,27,28]
        self.keys=[21,22,23,24]
        self.IOOUT = "out"
        self.IOIN = "in"
        self.IOPWM = "pwm"
        self.IOCLOCK = "clock"
        self.IOUP = "up"
        self.IODOWN = "down"
        self.IOTRI = "tri"

    def init_all(self):
        for i in self.leds:
            str2run = "gpio mode "+str(i)+" out"
            ret = os.popen(str2run).readlines()
            if(ret):
                print "run:",str2run
                print "return:",ret
            
        for i in self.keys:
            str2run = "gpio mode "+str(i)+" in"
            ret = os.popen(str2run).readlines()
            if(ret):
                print "run:",str2run
                print "return:",ret

    def mode(self,ionum,iostate):
        str2run = "gpio mode "+str(ionum)+" "+str(iostate)
        
        ret = os.popen(str2run).readlines()
        if(ret):
            print "run:",str2run
            print "return:",ret

    def write(self,ionum,iostate):
        str2run = "gpio write "+str(ionum)+" "+str(iostate)
        
        ret = os.popen(str2run).readlines()
        if(ret):
            print "run:",str2run
            print "return:",ret

    def read(self,ionum):
        str2run = "gpio read "+str(ionum)
        
        ret = str(os.popen(str2run).readlines())
        ret = ret.replace("[","")
        ret = ret.replace("]","")
        ret = ret.replace("\\","")
        ret = ret.replace("n","")
        ret = ret.replace("'","")
        #print "return after replace is:",ret
        
        return ret