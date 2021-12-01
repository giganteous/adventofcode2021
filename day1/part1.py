#!/usr/bin/python

import os, sys

infile = open('input.csv', 'r')
lines = infile.readlines()

lastm = 0
increases = 0
for l in lines[1:]:
    l = int(l.strip('\n'))
    if l > lastm:
        increases += 1
    lastm = l

print('total increases: ', increases)


