#!/usr/bin/python

import os
import json
from threading import Timer, main_thread as get_main

def ropen(fileAddr):
    return os.open(fileAddr, os.O_RDONLY)

def ftell(file):
    return os.lseek(file, 0, os.SEEK_CUR)

def fsize(file):
    cur = os.lseek(file, 0, os.SEEK_CUR)
    size = os.lseek(file, 0, os.SEEK_END)
    os.lseek(file, cur, os.SEEK_SET)
    return size

def goto(file, pos):
    return os.lseek(file, pos, os.SEEK_SET)

def rlines(buffer):
    return buffer.split('\n')

def search(file, words, maxChunks=None):

    pos = ftell(file)
    size = fsize(file)

    fmap = {}
    for w in words:
        fmap[w] = []

    if maxChunks == None:
        maxChunks = (size-pos)//1024

    buffer = None
    bsize = 1024

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
        print('chunks:', chunk//factor, '/', maxChunks//factor, unit)

        if timer == None:
            timer = Timer(3, start, timer)

        if chunk < maxChunks:
            #timer = Timer(3, start, timer)
            timer.start()
            obj['count'] += 1

        if obj['count'] % 10 == 0:
            with open('search.log', 'w') as file:
                file.write( json.dumps(fmap) )

        return timer

    timer = start()

    while buffer != '':

        buffer = os.read(file, 1024)
        pos = ftell(file)
        if pos >= size:
            print('buffer length',len(buffer))
            print('pos ',pos)
            print('size',size)
            break

        for w in words:
            wpos = -1 
            while True:
                wpos = buffer.find(w.encode('utf-8'), wpos+1)
                if wpos == -1:
                    break
                else:
                    fmap[w].append(pos+wpos)
        if chunk >= size:
            break
        chunk += 1

    timer.cancel()
    print('FIIIIIIIIIIIIIIIM')
    return fmap




