
#!/usr/bin/env python3

import sys

def m(value, maxrange=50):
    value = int(value)
    return value > 0 and min(maxrange, value) or max(-maxrange, value)

# we offset every coordinate by +50
#  -50 .. 0  ..  50   <- original
#    0 .. 50 .. 100   <- new
def load(path):
    f = open(path, "r")
    program = [] # containing (1|0, (xrange, yrange, zrange))
    for line in f:
        what, coords = line.strip().split(' ')
        xr, yr, zr = [(int(s)+50,int(e)+51)
                for s, e in [d.split('..')
                    for _, d in [c.split('=')
                        for c in coords.split(',')]]]
        program.append((what == 'on' and 1 or 0, (xr, yr, zr)))
    return program

m = 50
grid = []
for z in range(m * 2 + 1):
    grid.append([])
    for y in range(m * 2 + 1):
        grid[z].append([])
        grid[z][-1] = [0] * (m*2 + 1)

program = load(sys.argv[1])
for newvalue, (xr, yr, (zb, ze)) in program:
    for z in range(*zr):
        if z < 0 or z > 100: continue
        for y in range(*yr):
            if y < 0 or y > 100: continue
            for x in range(*xr):
                if x < 0 or x > 100: 
                    continue
                grid[z][y][x] = newvalue

from itertools import chain
def counttrue(grid):
    return sum(chain(*chain(*grid)))

print(counttrue(grid))
