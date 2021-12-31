#!/usr/bin/env python3

import sys

def load(path):
    f = open(path, "r")
    return [list(map(int, line.strip())) for line in f]

def pg(grid, fh=None):
    for r in grid:
        l = ''.join(map(str, r))
        if fh:
            fh.write(l + "\n")
        else:
            print(l)

from copy import deepcopy as dc
def explode(grid, factor=5):
    orig = dc(grid)
    h = len(grid)
    w = len(grid[0])
    for row in range(h):
        for x in range((factor - 1 ) * w):
            cur = grid[row][x]
            if cur == 9:
                grid[row].append(1)
            else:
                grid[row].append(cur+1)
    for row in range((factor -1 ) * h):
        grid.append([])
        for x in range(factor * w):
            cur = grid[row][x]
            if cur == 9:
                grid[-1].append(1)
            else:
                grid[-1].append(cur+1)


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

from heapq import heappush, heappop
def dijkstra(grid):
    w = len(grid[0]); h=len(grid)
    start = (0, 0)
    end = (w-1, h-1)
    costs = {}
    visited = set()
    todo = [(0, start)]

    while todo:
        risk, node = heappop(todo)
        if node == end:
            return risk
        for m in moves(node, w, h):
            if m in visited:
                continue
            nextrisk = grid[m[1]][m[0]]
            sumrisk = risk + nextrisk

            if sumrisk < costs.get(m, 100000):
                costs[m] = sumrisk
                heappush(todo, (sumrisk, m))

        # outside forloop
        visited.add(node)

grid = load(sys.argv[1])
total = dijkstra(grid)
print(total)
explode(grid)
total = dijkstra(grid)
print(total)

