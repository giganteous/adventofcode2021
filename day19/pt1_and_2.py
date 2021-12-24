#!/usr/bin/python3

from sys import argv
import re
from collections import namedtuple
import operator
from math import dist

def load_scanners(filename):
    scanners = []
    beacons = []
    beacon_index = 0
    with open(filename, "r") as f:
        for line in f:
            if "scanner" in line:
                groups = re.match("-+\s+(scanner \d+)\s+-+", line)
                scanner = Scanner(groups[1])
                beacon_index = 0
                beacons = []
                scanner.add_beacons(beacons)
                scanners.append(scanner)
            elif "," in line:
                pos = tuple(map(int, line.strip().split(",")))
                beacons.append(Beacon(pos, i=beacon_index))
                beacon_index += 1
    for x in scanners:
        x.make_fingerprints()
    scanners[0].location=(0, 0, 0)
    return scanners

class Beacon:
    def __init__(self, pos, i=''):
        self.pos = pos
        self.orig_pos = pos
        self.i = i

    def reset(self):
        self.pos = self.orig_pos

    def __str__(self):
        if type(self.i) == type(0):
            return "<{:2}> {:4},{:4},{:4}".format(self.i, self.pos[0], self.pos[1], self.pos[2])
        return "{}{:4},{:4},{:4}".format(self.i, self.pos[0], self.pos[1], self.pos[2])

    def __repr__(self):
        return "<{:4},{:4},{:4} i={}>".format(self.pos[0], self.pos[1], self.pos[2], self.i)

    def __sub__(self, other):
        return tuple(c1 - c2 for c1, c2 in zip(self.pos, other.pos))

    def __eq__(self, other):
        return self.pos == other.pos

    def __add__(self, other):
        return tuple(c1 + c2 for c1, c2 in zip(self.pos, other.pos))

    def apply(self, f):
        """ Adjust myself to a new base grid """
        self.pos = f(self.pos)

    def view(self, f):
        """ View myself to a new base grid or orientation """
        return Beacon(f(self.pos))

    def distance(self, other):
        return dist(self.pos, other.pos)

class Scanner():
    def __init__(self, name):
        self.name = name
        self.beacons = []
        self.fingerprints = []
        self.location = None

    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def make_fingerprints(self):
        self.fingerprints = [set([b.distance(o) for b in self.beacons]) for o in self.beacons]

    def add_beacons(self, coords):
        self.beacons = coords

    def set_location(self, function):
        """ Moving the scanner in space """
        if not self.location:
            self.location = function((0, 0, 0))
        [ b.apply(function) for b in self.beacons ]

    def set_rotation(self, function):
        [ b.apply(function) for b in self.beacons ]

    def reset(self):
        self.location = None
        [ b.reset() for b in self.beacons ]

    def search_fingerprints(self, other):
        selflist = []
        otherlist = []
        for n in range(len(self.fingerprints)):
            for o in range(len(other.fingerprints)):
                l = len(self.fingerprints[n].intersection(other.fingerprints[o]))
                if l>=12:
                    selflist.append(self.beacons[n])
                    otherlist.append(other.beacons[o])
        return selflist, otherlist

from itertools import product
def make_transformations():
    def attitude_and_bank():
        """ change either the attitude (forward or backward)
                   either the bank (left roll, right roll)
            or make a complete flip (180°).
            heading will fix the nose of the scanner"""
        yield lambda x, y, z: (+x,+y,+z) # do nothing
        yield lambda x, y, z: (+x,+z,-y) # nose dive forward
        yield lambda x, y, z: (+x,-z,+y) # node dive backward
        yield lambda x, y, z: (+z,+y,-x) # bank left
        yield lambda x, y, z: (-z,+y,+x) # bank right
        yield lambda x, y, z: (-x,+y,-z) # bank 180°

    def heading():
        """ change the heading of the scanner """
        yield lambda x, y, z: (+x,+y,+z) # do nothing
        yield lambda x, y, z: (-y,+x,+z) # scanner turns right
        yield lambda x, y, z: (+y,-x,+z) # scanner turns left
        yield lambda x, y, z: (-x,-y,+z) # scanner turns around

    def apply_both(h, ab):
        return lambda pos: h(*ab(*pos))

    return [
                apply_both(change_h, change_ab) #lambda x: change_h(*change_ab(*x)) 
                for change_h, change_ab in product(heading(), attitude_and_bank())
        ]

funcs = make_transformations()

def search_rotation(left, right, try_funcs):
    """given 2 overlapping beacons (l and r) try to
       match the rotation of scanner R with the scanner L.

       If the Δ between each pair of beacons is the same, 
       we know we have the right rotation, and we know
       the Δ to apply to R.
    """
    for f in range(len(try_funcs)):
        compare = left[0] - right[0].view(try_funcs[f])
        if all([compare == left[i] - right[i].view(try_funcs[f])
            for i in range(1, len(left))]):
            #print("Rotation", f)
            return try_funcs[f], lambda x: (x[0]+compare[0],x[1]+compare[1],x[2]+compare[2])
    return None, None


# utility functions
def sortbyright(left, right):
    return zip(*sorted(zip(left, right), key=lambda x: x[1].i))

def printlistof(left, right=None, f=None, adjust=None):
    """Print set of coordinates compared to each other"""
    print("%-21s %-21s %s"%('left', 'right', 'Δ'))
    if right:
        for l, r in zip(left, right):
            if f:
                r = r.view(f)
            print("%-21s %-21s %s" % (l, r, l-r))
    else:
        for b in left:
            print(" {}".format(b))

from sys import argv
if len(argv) != 2:
    print(f"Usage: {argv[0]} <filename>")
    exit(1)
scanners = load_scanners(argv[1])
explore = set([0])
unfinished = True

while len(explore):
    i = explore.pop()
    for j in range(len(scanners)):
        if i == j or scanners[j].location:
            continue

        # see if we have an overlap
        left, right = scanners[i].search_fingerprints(scanners[j])

        if not len(left):
            continue

        # search for a rotation in j
        F, transform = search_rotation(left, right, funcs)

        if not F:
            print(f"Weird: no rot ({i}&{j}) but overlap!")
            continue

        explore.add(j)
        scanners[j].set_rotation(F)
        scanners[j].set_location(transform)
        print(f"Scanner {j} sits at {scanners[j].location} (from {i})")

allbeacons = set()
for x in scanners:
    if not x.location:
        print("still no location for ", x.name)
    for b in x.beacons:
        allbeacons.add(b.pos)
print(len(allbeacons))

def taxi_distance(a, b):
    return sum([abs(c1 - c2) for c1, c2 in zip(a, b)])
from itertools import combinations
m = max([taxi_distance(p1.location, p2.location) for p1, p2 in combinations(scanners, 2)])
print(f"Max distance between 2 scanners: {m}")
