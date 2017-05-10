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

    # Produce an empty search class:
    search = Search()

    # Add the argument files to the class instance:
    for file in files:
        search.addDesc(file)

    # Ask for the partition address
    sys.stdout.write("Please write the address of the desired read-only partition (e.g. /dev/sdb1): ")
    dev = os.open(input(), os.O_RDONLY)

    print('starting search...')

    result = search.run(dev)

    print('writting output...')

    with open('mapped.json', 'w') as file:
        file.write( json.dumps(result, indent=2) )



