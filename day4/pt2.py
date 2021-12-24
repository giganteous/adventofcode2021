#!/usr/bin/python

import sys,os

def load(path):
  with open(path, "r") as f:
    numbers = list(map(int, next(f).split(",")))
    boards = []

    next(f)
    t = []
    for line in f:
        if line.strip() == "":
            boards.append(t)
            t = []
        else:
            t.extend(list(map(int, line.split())))
    boards.append(t)
    return numbers, boards

def total(board):
    return sum([((x != None) and x) or 0 for x in board])

def wins(board):
    for i in range(5):
        row = board[i*5:i*5+5]
        if all([x is None for x in row]):
            return True
        col = board[i::5]
        if all([x is None for x in col]):
            return True

def printboards(boards):
    for b in boards:
        for i in range(5):
            for n in b[i*5:i*5+5]:
                if n is None:
                    print('<> ', end='')
                else:
                    print('{:02} '.format(n), end='')
            print()
        print()

def mark(boards, num):
    for b in range(len(boards)):
        for i in range(len(boards[b])):
            if boards[b][i] == num:
                boards[b][i] = None



def game():
    filename = 'example'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    numbers, data = load(filename)
    won = [False] * len(data)
    print('numbers: ', numbers)
    for n in numbers:
        mark(data, n)
        for b in range(len(data)):
            if not won[b] and wins(data[b]):
                won[b] = True
                if all(won):
                    #printboards(data)
                    left = total(data[b])
                    print(f"board {b+1} won last")
                    print(f"the remaining total on that board is {left}")
                    print(f"the last call was {n}")
                    print(f"the answer: {n * left}")
                    return

if __name__ == "__main__":
    game()
