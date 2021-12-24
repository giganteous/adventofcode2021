#!/usr/bin/python

import sys,os

def load_diagnostics_from_file(path):
  with open(path, "r") as f:
    data = [list(map(int, line.strip())) for line in f]
  return data

#00100
#   11110
#               10110
#                   10111 -> 23
#           10101
#01111
#00111
#    11100
#10000
#    11001
#00010
#01010

# For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

# Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
# Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
# In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
# In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
# In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
# As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

def pos(alist, column=0):
    l = len(alist)
    if l == 1: return alist[0]
    ones = []
    zeroes = []
    for row in alist:
        print(f"{column}: {row}")
        if row[column] == 1:
            ones.append(row)
        else:
            zeroes.append(row)
    if len(ones) >= l/2: return pos(ones, column+1)
    return pos(zeroes, column+1)

def neg(alist, column=0):
    l = len(alist)
    if l == 1: return alist[0]
    ones = []
    zeroes = []
    for row in alist:
        if row[column] == 1:
            ones.append(row)
        else:
            zeroes.append(row)
    if len(ones) < l/2: return neg(ones, column+1)
    return neg(zeroes, column+1)

def myint(row):
    gamma = 0
    for col in row:
        gamma = (gamma << 1) | col
    return gamma

filename = 'example'
if len(sys.argv) > 1:
    filename = sys.argv[1]
    
data = load_diagnostics_from_file(filename)
ox = myint(pos(data))
co2 = myint(neg(data))
print(f"ox {ox}, co2 {co2}, and their factor: { ox * co2 }")
