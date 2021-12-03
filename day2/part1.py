#!/usr/bin/python

import csv

fh = open('input.csv', newline='')

reader = csv.DictReader(fh, delimiter=',')

aim = 0
pos = 0
depth = 0
for row in reader:
    units = int(row['units'])
    if row['direction'] == 'up':
        aim = aim - units
    elif row['direction'] == 'down':
        aim = aim + units
    else:
        # increase horizontal position by X units
        pos += units
        depth += ( aim * units )

print(f"Position: {pos}, depth: {depth}. multiplied: {pos * depth}")


#df["r"] = df.rolling(3).x.sum() # rolling window
#print('total increases: ', len(df[df.diff() > 0]))
#df["difference"] = df.r.diff()  # difference with previous row
#print('total increases: ', len(df[df.difference > 0]))

