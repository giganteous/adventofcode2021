#!/usr/bin/python

import sys,re

def load(path):
    maxx, maxy = 0, 0
    vents = []
    with open(path, "r") as f:
        for line in f:
            [x1,y1,x2,y2] = list(map(int, re.split(',| -> ', line)))
    
            if x1 == x2 or y1 == y2:
                maxx = max(maxx, x1, x2)
                maxy = max(maxy, y1, y2)
                vents.append((x1,y1,x2,y2))
    return maxx, maxy, vents


def game():
    filename = 'example'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    x, y, vents = load(filename)
    print('x: ', x)
    print('y: ', y)
    print('vents: ', vents)

    grid = []
    for i in range(y+1):
        grid.append([0] * (x+1))
    markvents(grid, vents)
    printgrid(grid)

def markvents(grid, vents):
    for vent in vents:
        x1,y1,x2,y2 = vent
        #print("mapping ", vent)
        for x in range(min(x1, x2), max(x1, x2)+1):
            for y in range(min(y1, y2), max(y1, y2)+1):
                #print(f"covers {x},{y}")
                grid[y][x] += 1

def printgrid(data):
    largeoverlaps = 0
    for row in data:
        for plot in row:
            print(plot != 0 and plot or '.', end='')
            if plot >= 2: largeoverlaps+=1
        print()
    print(f"amount of overlaps > 2: {largeoverlaps}")


if __name__ == "__main__":
    game()
