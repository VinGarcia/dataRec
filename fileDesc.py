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

def renumerate(L):
    for index in reversed(range(len(L))):
        yield index, L[index]

def back(dev, pos, maxI=50000000):
    c_pos = pos % 1024
    c_block = pos - c_pos
    os.lseek(dev, c_block, os.SEEK_SET)
    buf = os.read(dev, 1024)

    for i in range(maxI):
        if c_pos < 0:
            c_pos = 1023
            c_block -= 1024
            os.lseek(dev, c_block, os.SEEK_SET)
            buf = os.read(dev, 1024)

        if pos == 0:
            return pos, buf[0]

        yield pos, buf[c_pos]

        pos -= 1
        c_pos -= 1

def ahead(dev, pos, maxI=50000000):
    d_size = os.lseek(dev, 0, os.SEEK_END)

    c_pos = pos % 1024
    c_block = pos - c_pos
    os.lseek(dev, c_block, os.SEEK_SET)
    buf = os.read(dev, 1024)
    
    for i in range(maxI):
        if c_pos == 1024:
            c_pos = 0
            c_block += 1024
            os.lseek(dev, c_block, os.SEEK_SET)
            buf = os.read(dev, 1024)

        if pos == d_size-1:
            return pos, buf[d_size-1]

        yield pos, buf[c_pos]

        pos += 1
        c_pos += 1

class fileDesc():
    text = None

    spos = None
    fpos = None
    size = None

    count = 0
    _device = '/dev/sda5'
    def __init__(self, spos, delim=None, maxI=50000000):
        # If loading from json:
        if type(spos) == type({}) or type(spos) == type(""):
            self.fromJSON(spos)
            return

        self.count += 1
        self.spos = spos
        self.fpos = spos
        self.expand(delim)

    def add(self, pos):
        if pos >= self.spos and pos < self.fpos:
            self.count += 1
            return True
        return False

    def expand(self, delim=None, maxI=50000000):
        base_delim = [0x00, 0xff]
        if delim == None:
            delim = base_delim
        else:
            delim += base_delim

        dev = os.open(self._device, os.O_RDONLY)

        spos = self.spos
        fpos = self.fpos

        # Look ahead:
        for pos, c in ahead(dev, fpos, maxI):
            if c in delim:
                break
        fpos = pos


        # Look back:
        for pos, c in back(dev, spos, maxI):
            if c in delim:
                break
        spos = pos

        # Read it all:
        os.lseek(dev, spos, os.SEEK_SET)
        text = os.read(dev, fpos-spos)

        # Close file:
        os.close(dev)

        # Save info:
        self.spos = spos
        self.fpos = fpos
        self.text = text.decode('utf-8', errors='replace')
        self.size = fpos - spos
        return self.spos, self.fpos, self.text

    def __repr__(self):
        return json.dumps(self.toJSON())
    def toJSON(self):
        return {
                'spos': [ readable(self.spos), self.spos ],
                'fpos': [ readable(self.fpos), self.fpos ],
                'size': [ readable(self.size), self.size ],
                'count': self.count
            }
    def fromJSON(self, json_obj):
        if type(json_obj) == type(""):
            json_obj = json.loads(json_obj)

        self.spos = json_obj['spos'][1]
        self.fpos = json_obj['fpos'][1]
        self.size = json_obj['size'][1]
        self.count = json_obj['count']

    # Read file from device.
    def read(self, padTop=0, padBottom=0, encoding='utf-8'):
        dev = os.open(self._device, os.O_RDONLY)
        os.lseek(dev, self.spos-padTop, os.SEEK_SET)

        text = os.read(dev, self.size + padTop + padBottom)
        os.close(dev)
        self.text = text.decode('utf-8', errors='replace')
        return text.decode(encoding, errors='replace')

    def groupFiles(list, delim=None, maxI=50000000):
        last = 0
        files = [ fileDesc(list[0], delim) ]

        for pos in list[1:]:

            if not files[last].add( pos ):
                last+=1
                files.append( fileDesc(pos, delim, maxI) )

        files.sort(key=lambda x : x.count, reverse=True)
        return files


