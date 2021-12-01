#!/usr/bin/python

import os, sys

infile = open('input', 'r')
lines = infile.readlines()

lastm = 0
increases = 0
for l in lines:
    l = int(l.strip('\n'))
    if lastm == 0:
        print(l, ' (N/A - no previous measurement)')
    elif l < lastm:
        print(l, ' (decreased)')
    elif l > lastm:
        print(l, ' (increased)')
        increases += 1
    else:
        print(l, ' (same!)')
    lastm = l

print('total increases: ', increases)


