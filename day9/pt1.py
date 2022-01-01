#!/usr/bin/env python3

import sys

def load(path):
    f = open(path, "r")
    return [list(map(int, line.strip())) for line in f]

def moves(cur, w, h): # grid, width, height
    for dx, dy in (
            (cur[0]  , cur[1]-1),
            (cur[0]  , cur[1]+1),
            (cur[0]-1, cur[1]  ),
            (cur[0]+1, cur[1]  ),
            ):
        if dx < 0 or dx >= w or dy < 0 or dy >= h:
            continue
        yield dx, dy

import string
from collections import Counter

grid = load(sys.argv[1])
w = len(grid[0])
h = len(grid)

basins = {} # color cache
color = 10
def setcolor(coord):
    basins[coord] = color
def isborder(coord):
    return grid[coord[1]][coord[0]] == 9

def colorize_from(coord, w, h):
    """Method to walk from coord going all directions until
    we meet a border, and color each step"""
    if isborder(coord): return

    for m in moves(coord, w, h):
        if m in basins: continue
        if isborder(m): continue # go back

        setcolor(m)
        colorize_from(m, w, h)

for y in range(h):
    for x in range(w):
        cur = (x, y)
        if cur in basins: continue # aerea already filled

        colorize_from(cur, w, h)
        # for next area, choose new color
        color+=1

c = Counter(basins.values())
one, two, three = [n for _, n in c.most_common(3)]
print("Factor of 3 biggest basins: ", one * two * three)
