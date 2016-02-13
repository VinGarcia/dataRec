#!/usr/bin/python

import os
import json

from fsTools import ropen, search

if __name__ == '__main__':
    dev = ropen('/dev/sda5')

    # To seek doc-emergencia.txt:
    #words = ['\n * * * * *', '#Tarefas', '#S3', '#Sistema', '#Blog']

    # To seek lfs_gui python scripts:
    words = [
            '\nfrom lfs_interface',
            'lfsInterfaceSp',
            '\n  print(lfs.dataFiles)',
            '\nclass lfsInterface(object):',
            ', dataFile=None):',
            "\n  interface.play('video2.mp4')"
        ]

    #os.lseek(dev, -1024*1024, os.SEEK_END)

    print('starting search...')

    result = search(dev, words)

    print('writting output...')

    with open('output.json', 'w') as file:
        file.write( json.dumps(result, indent=2) )



