
import rotation as r

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
scanners = r.load_scanners(argv[1])
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
        F, delta = r.search_rotation(left, right, r.funcs)

        if not F:
            print(f"Weird: no rot ({i}&{j}) but overlap!")
            continue

        explore.add(j)
        scanners[j].set_location(delta)
        scanners[j].set_rotation(F)
        print(f"Scanner {j} sits at {scanners[j].location} (from {i})")

allbeacons = set()
for x in scanners:
    if not x.location:
        print("still no location for ", x.name)
    for b in x.beacons:
        allbeacons.add(b.pos)
print(len(allbeacons))

#unmapped[1].set_rotation(F)
#unmapped[1].set_location(delta)
#
#left, right = unmapped[1].search_fingerprints(unmapped[4])
#F, delta = r.search_rotation(left, right, r.funcs)
#printlistof(left, right)
