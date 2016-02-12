#!/usr/bin/python

import json
import os
from funcs import fileDesc
from findDoc import ropen, goto

# Read data produced with findDoc.py:
data = None
with open('output.json.bkp') as file:
    data = json.load(file)

# Try to guess where are the files:
guess = fileDesc.findall(data['\n * * * * *'], dist=60000, min=60 )

# Get the file with the most ocurrencies of "\n * * * * *":
file = max(guess, key=lambda x: x.count)

print(file)

text = file.read(padTop=1600)

with open('file.txt', 'w') as file:
  file.write(text)

with open('guess.json', 'w') as file:
    guess = [item.toJSON() for item in guess]
    file.write( json.dumps(guess, indent=2) )


