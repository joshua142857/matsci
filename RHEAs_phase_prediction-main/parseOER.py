import pandas as pd
import numpy as np

els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
       'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
       'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']


def findAlloys(structure):
    pd2 = pd.read_excel("collection4" + structure + ".xlsx", sheet_name="Sheet1")
    pd3 = pd.read_excel("5-" + structure.lower() + ".xlsx")
    # pd4 = pd.read_excel("4-" + structure.lower() + ".xlsx")
    # pd5 = pd.read_excel("5-" + structure.lower() + ".xlsx")
    entries = []
    for i, r in pd2.iterrows():
        print(i)
        for index, row in pd3.iterrows():
            if row["e_hull"] < r["e_hull"]:
                qin = [row["e1"], row["e2"], row["e3"], row["e4"], row["e5"]]
                if r["e1"] in qin and r["e2"] in qin and r["e3"] in qin and r["e4"] in qin:
                    entries.append(index)
            if row["e_hull"] >= r["e_hull"]:
                break
    df = pd.DataFrame()
    for i in entries:
        df = df.append(pd3.iloc[i])
    df.to_excel("collection5" + structure + ".xlsx")

elsp = ['Zr', 'Au']
ehull = 0.04

def targetBinaries(structure, OERels):
    pd2 = pd.read_excel("datasheets/3-" + structure.lower() + ".xlsx")
    # for a in [pd2]:
    #     a.set_index('Unnamed: 0', inplace=True)
    for index, row in pd2.iterrows():
        if row["e_hull"] > ehull:
            pd2 = pd2.drop(index)
        elif row["e1"] not in OERels or row["e2"] not in OERels:
            pd2 = pd2.drop(index)
    pd2.to_excel("stable/" + OERels[0] + OERels[1] + structure + ".xlsx")


targetBinaries("FCC")
# targetBinaries("BCC")