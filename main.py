#!/usr/bin/python

import os
import sys
import json

from search import Search

if __name__ == '__main__':
    # Validate parameters:

    files = sys.argv[1:]
    if len(files) == 0:
        print("Usage: %s <file1.json> <file2.json> ..." % sys.argv[0])
        exit(1)

    search = Search()

    for file in files:
        search.addDesc(file)

    dev = os.open('/dev/sda5', os.O_RDONLY)

    #os.lseek(dev, -1024*1024, os.SEEK_END)

    print('starting search...')

    result = search.run(dev)

    print('writting output...')

    with open('mapped.json', 'w') as file:
        file.write( json.dumps(result, indent=2) )



