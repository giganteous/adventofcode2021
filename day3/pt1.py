#!/usr/bin/python

import sys,os

fh = open('input.txt', 'r')
data = [map(int, line.strip()) for line in fh]

#for row in data: print(row)

l = len(data) / 2

cols = list(zip(*data))

gamma, epsilon = 0, 0
for col in cols:
    if sum(col) > l:
        gamma = (gamma << 1) | 1
        epsilon = (epsilon << 1) | 0
    else:
        gamma = (gamma << 1) | 0
        epsilon = (epsilon << 1) | 1

print(gamma * epsilon)
