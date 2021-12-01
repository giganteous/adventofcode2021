#!/usr/bin/python

import pandas as pd
df = pd.read_csv('input.csv')
df["difference"] = df.x.diff()

print('total increases: ', len(df[df.difference > 0]))


