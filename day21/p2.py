#!/usr/bin/env python3
import sys
from collections import defaultdict
def load(path):
    f = open(path, 'r')
    return [int(y) for _, y in [line.split(': ') for line in f]]
#
# Strategy from reddit
#
# Keep a dictionary keyed by (score, position) which is your 'multiverse'. Populate it with score of 0 and starting position, mapping to the value of 1 (=state occurs 1 times)
# Starting from any position/score, you can end up in 7 different positions with 7 different scores, depending on the dice rolls.
# You need to iterate over all current states = dictionary key / values and create a new 'era', ie the next multiverse map. If at any point you achieve the target score, increase the win count for that era number. Otherwise, just add the current state counters to multiple new state counters

# ways to throw
possible_throws = [
        (3, 1), # one way to throw 3
        (4, 3), # three ways to throw 4
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1),
]

def turn(universes, wins=([], [])):
    new = defaultdict(int)
    wins[0].append(0) # p1 wins
    wins[1].append(0) # p2 wins
    turn = len(wins[0])
    
    # XXX: this might work. flip turns
    for (p1pos, s1, p2pos, s2), unicount in universes.items():
        # make a universe for each
        for total, ways in possible_throws:
            score = (p1pos + total)
            if score > 10: score -= 10
            if s1 + score >= 21:
                wins[0][-1] += (unicount * ways)
            else:
                new[(score, s1 + score, p2pos, s2)] += (unicount * ways)

    universes = new
    new = defaultdict(int)
    for (p1pos, s1, p2pos, s2), unicount in universes.items():
        # make a universe for each
        for total, ways in possible_throws:
            score = (p2pos + total)
            if score > 10: score -= 10
            if s2 + score >= 21:
                wins[1][-1] += unicount * ways
            else:
                new[(p1pos, s1, score, s2 + score)] += (unicount * ways)
    print("{:2} p1:{:15};p2:{:15} | Δ p1 {:14} p2 {:14}; pending: {:13}; low p1/p2: {}/{}".format(
        turn, sum(wins[0]), sum(wins[1]), wins[0][-1], wins[1][-1], sum(new.values()),
        len(new) and min([x for _, x, _, _ in new.keys()]),
        len(new) and min([y for _, _, _, y in new.keys()]),
        ))

    return new, wins

# counts the occurrences of a universe per (position, score)
from itertools import chain
p1, p2 = load(sys.argv[1])
n = defaultdict(int); n[(p1, 0, p2, 0)] = 1
wins = ([], [])
while n:
    n, wins = turn(n, wins)
