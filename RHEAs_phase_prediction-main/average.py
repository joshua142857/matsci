import eahull
import pandas as pd
import itertools
import matplotlib.pyplot as plt

sheet = pd.read_excel("5-bcc.xlsx")
els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
       'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
       'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
elsdict = dict.fromkeys(els)
elscol = ["e1", "e2", "e3", "e4", "e5"]
for index, row in sheet.iterrows():
    if row["e_hull"] > 0.03:
        break
    for i in elscol:
        if elsdict[row[i]] == None:
            elsdict[row[i]] = float(row["e_hull"])
        else:
            elsdict[row[i]] += float(row["e_hull"])

for v in sorted(elsdict, key=elsdict.get, reverse=True):
    print(v, elsdict[v])
