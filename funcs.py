import os
import json

def readable(number):
    if number//1024 == 0:
        return str(number) + "B"
    if number//1024**2 == 0:
        return str(number//1024) + "KB"
    if number//1024**3 == 0:
        return str(number//1024**2) + "MB"
    if number//1024**4 == 0:
        return str(number//1024**3) + "GB"

class fileDesc():
    spos = None
    pos = None
    size = None
    count = 0
    _device = '/dev/sda5'
    def __init__(self, spos):
        self.spos = spos
        self.pos = spos
        self.count += 1
        self.size = 0
    def add(self, pos):
        self.pos = pos
        self.count += 1
        self.size = pos - self.spos
    def __repr__(self):
        return json.dumps(self.toJSON())
    def toJSON(self):
        return {
                'spos': readable(self.spos),
                'pos': readable(self.pos),
                'size': readable(self.size),
                'count': self.count
            }
    # Read file from device.
    def read(self, padTop=0, padBottom=0, encoding='utf-8'):
        dev = os.open(self._device, os.O_RDONLY)
        os.lseek(dev, self.spos-padTop, os.SEEK_SET)

        text = os.read(dev, self.size + padTop + padBottom)
        os.close(dev)
        return text.decode(encoding)


    # Guess where files start and end, based on proximity
    # Static function:
    def findall(List, dist=2048, min=10):
    
        last=0
        nList = [fileDesc(List[0])]
    
        for pos in List:
            if pos - nList[last].pos < dist:
                nList[last].add(pos)
            else:
                last += 1
                nList.append( fileDesc(pos) )
    
        return [ item for item in nList if item.count >= min ]
    
