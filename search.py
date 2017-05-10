#!/usr/bin/python

import os
import json
from threading import Timer, main_thread as get_main

from os.path import basename, splitext

def ftell(file):
    return os.lseek(file, 0, os.SEEK_CUR)

def fsize(file):
    cur = os.lseek(file, 0, os.SEEK_CUR)
    size = os.lseek(file, 0, os.SEEK_END)
    os.lseek(file, cur, os.SEEK_SET)
    return size

class Search():

    descs = []

    def addDesc(self, file):

        if not os.path.exists(file):
            raise ("%s does not exist!" % file)
        if not os.path.isfile(file):
            raise ("%s is not a file!" % file)

        with open(file) as _file:
            desc = json.load(_file)

        desc['name'], ext = splitext(basename(file))

        # 'on_it' words also count as 'words':
        desc['words'] += desc['desc']['on_it']

        self.descs.append(desc)

    def run(self, dev, maxChunks=None):

        descs = self.descs

        if len(descs) == 0:
            return {}

        pos = ftell(dev)
        size = fsize(dev)

        fmap = {}
        for d in descs:
            fmap[d['name']] = []

        if maxChunks == None:
            maxChunks = (size-pos)//1024

        buffer = None
        bsize = 1024*4

        chunk = 0

        print('total size:', size/(1024*1024), 'MB')
        print('total chunks:', maxChunks)

        factor = 1024
        unit = 'MB'
        if maxChunks < 1024:
            factor = 1
            unit = 'KB'

        obj = { 'count': 0 }
        def start(timer=None):
            print('chunks:', (chunk*bsize//1024)//factor, '/', maxChunks//factor, unit)
            if timer == None:
                timer = Timer(3, start, timer)
    
            if chunk < maxChunks:
                #timer = Timer(3, start, timer)
                obj['timer'] = timer.start()
                obj['count'] += 1
    
            if obj['count'] % 10 == 0:
                with open('search.log', 'w') as file:
                    file.write( json.dumps(fmap) )
    
            return timer
    
        obj['timer'] = start()
    
        try:
            while buffer != '':
        
                buffer = os.read(dev, bsize)
                pos = ftell(dev)
                if pos >= size:
                    print('buffer length',len(buffer))
                    print('pos ',pos)
                    print('size',size)
                    break
        
                for d in descs:
                    wpos = -1 
                    for w in d['words']:
                        while True:
                            wpos = buffer.find(w.encode('utf-8'), wpos+1)
                            if wpos == -1:
                                break
                            else:
                                fmap[d['name']].append(pos+wpos)
                if chunk >= size:
                    break
                chunk += 1

            for d in descs:
                fmap[d['name']].sort()
        finally:
            obj['timer'].cancel()
    
        print('FINISHED')
        return fmap




