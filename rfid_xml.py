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
  <TagID>E200 6877 7716 0219 0370 EC07</TagID>
  <DiscoveryTime>2014/11/26 09:10:43.091</DiscoveryTime>
  <LastSeenTime>2014/11/26 09:10:43.091</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
<Alien-RFID-Tag>
  <TagID>E200 6877 7716 0219 1460 8358</TagID>
  <DiscoveryTime>2014/11/26 09:10:43.095</DiscoveryTime>
  <LastSeenTime>2014/11/26 09:10:43.095</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
<Alien-RFID-Tag>
  <TagID>E200 6877 7716 0219 1450 8357</TagID>
  <DiscoveryTime>2014/11/26 09:10:43.101</DiscoveryTime>
  <LastSeenTime>2014/11/26 09:10:43.101</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
<Alien-RFID-Tag>
  <TagID>E200 3035 100C 0118 2620 0D7D</TagID>
  <DiscoveryTime>2014/11/26 09:10:43.105</DiscoveryTime>
  <LastSeenTime>2014/11/26 09:10:43.105</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
<Alien-RFID-Tag>
  <TagID>E200 6877 7716 0219 0380 EC08</TagID>
  <DiscoveryTime>2014/11/26 09:10:43.115</DiscoveryTime>
  <LastSeenTime>2014/11/26 09:10:43.115</LastSeenTime>
  <Antenna>0</Antenna>
  <ReadCount>1</ReadCount>
  <Protocol>2</Protocol>
</Alien-RFID-Tag>
</Alien-RFID-Tag-List>
"""

    def get_tagid(self,rfid_text):
        if self.debug:
            print "~"*20,"\r\n",rfid_text,"\r\n","~"*20

        rfid_text=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",rfid_text)
        
        idlist=list()

        try:
            root = ET.fromstring(rfid_text)
        except SyntaxError:
            print "ParseError(SyntaxError) happened"
            #当接收数据不完整(实际数据包大小大于缓冲区)时,可以换用正则去解析
            #parse_byRE(rfid_text)
            return None

        for child in root.iter('TagID'):
            rfid_id = child.text.replace(" ","")
            rfid_id_hash = hashlib.md5(rfid_id).hexdigest()
            idlist.append(rfid_id_hash)
            if self.debug:
                print rfid_id,"\tmd5:\r\n",hashlib.md5(rfid_id).hexdigest(),"\r\n"
        return idlist

    def test_fun(self):
        #print "Need Debug =",self.debug
        #print "\r\nDebug Text is\r\n",self.example_text
        t = self.get_tagid(self.example_text)
        print t