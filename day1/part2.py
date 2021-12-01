#!/usr/bin/python

import pandas as pd

df = pd.read_csv('input.csv')
df["r"] = df.rolling(3).x.sum() # rolling window
#print('total increases: ', len(df[df.diff() > 0]))
df["difference"] = df.r.diff()  # difference with previous row
print('total increases: ', len(df[df.difference > 0]))

