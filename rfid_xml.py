# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import hashlib

class rfid_xml:
    def __init__(self, need_debug = False):
        '''Initializes RFID XML'''
        #print "Need Debug =",need_debug
        self.debug = need_debug
        self.example_text ="""\
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

    def get_tagid(self,rfid_text):
        if self.debug:
            print "~\r\n",rfid_text,"~\r\n"
        
        #过滤非法字符
        rfid_text=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",rfid_text)

        #用ElementTree分析
        root = ET.fromstring(rfid_text)
        #遍历TagID
        for child in root.iter('TagID'):
            rfid_id = child.text.replace(" ","")
            rfid_id_hash = hashlib.md5(rfid_id).hexdigest()
            if self.debug:
                print rfid_id,"\tmd5:\r\n",hashlib.md5(rfid_id).hexdigest(),"\r\n"

    def test_fun(self):
        print "Need Debug =",self.debug
        print "\r\nDebug Text is\r\n",self.example_text
        self.get_tagid(self.example_text)