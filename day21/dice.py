#!/usr/bin/env python3
import sys

def load(path):
    f = open(path, 'r')
    return [ Player(name='player'+ k, start=int(v))
            for k, v in [
                line.strip().strip('Player ').split(' starting position: ')
                for line in f
                ]
            ]

class Player:
    def __init__(self, name, start):
        self.name = name
        self.space = start
        self.score = 0
    def move(self, sides):
        steps = (sum(sides) % 10) # add rest
        self.space += steps
        if self.space > 10: self.space = self.space % 10
        self.score += self.space
        #print(self.name, 'rolled', score, 'and moved', steps, 'spaces to', self.space, 'for a total score of', self.score)
        return self.score >= 1000

class Dice:
    def __init__(self, sides=100):
        self.sides = sides
        self.face = 0
        self.rollcount = 0
    def throw(self, times=1):
        s = []
        for t in range(times):
            self.rollcount+=1
            self.face += 1
            if self.face > 100: self.face = 1
            s.append(self.face)
            #print('threw', self.face)
        return s

def setupgame():
    players = load(sys.argv[1])
    d = Dice()
    nowinner = False
    for p in players:
        print(p.name, "starting position:", p.space)
    winner = playgame(players, d)
    players.remove(winner)
    for o in players:
        print(o.name, "scored", o.score, "points.")
        print("Factor:", d.rollcount * o.score)

def playgame(players, dice):
    while 1:
        for p in players:
            t = dice.throw(3)
            if p.move(t):
                print(p.name, 'threw', t, "and now wins and the game ends.")
                return p

p1 = Player('x', 4)
p1.move([1,2,3])
assert p1.score == 10, "this must be 10"
