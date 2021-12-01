#!/usr/bin/python

import os, sys
import pandas as pd
import numpy as np

infile = open('input.csv', 'r')
lines = infile.readlines()

alist = []
lastm = 0
increases = 0
for l in lines[1:]:
    l = int(l.strip('\n'))
    alist.append(l)

s = pd.Series(alist).astype("Int64")
lastreading = np.NaN
increases=0
for element in s.rolling(window=3).sum():
    #if element == np.NaN:
    #elif lastreading == np.NaN:
    #if lastreading > element: print(element, ' (decrease)')
    if lastreading < element:
        #print(element, ' (increase)')
        increases += 1
    #else:
        #print(element, ' (steady)')
        #print(element, 'not enough readings (or no last, or steady)')
    lastreading = element

print('total increases: ', increases)

