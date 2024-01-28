# import pandas as pd
# import numpy as np
#
# els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
#        'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
#        'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
# OERels = ['Co', 'Fe', 'Mn', 'Mo', 'Ni', 'Ti', 'Pt', 'Pd', 'Ir', 'Rh']
#
#
# class Element:
#     def __init__(self, name):
#         self.name = name
#         self.count = 0
#         new_dict = {}
#         for el in els:
#             if el != name:
#                 new_dict[el] = 0
#         self.pairs = new_dict
#
#
# def metastabilityCount(structure, els):
#     elements = []
#     for el in els:
#         elements.append(Element(el))
#     data = pd.read_excel("datasheets/5-" + structure.lower() + ".xlsx")
#     for index, row in data.iterrows():
#         if row["e_hull"] >= 0.05:
#             print("Done")
#             break
#         else:
#             currentels = [row["e1"], row["e2"], row["e3"], row["e4"], row["e5"]]
#
#             def check(el):
#                 for c in currentels:
#                     if el.name == c:
#                         return True
#                 return False
#
#             for el in elements:
#                 if check(el):
#                     for currel in currentels:
#                         if el.name == currel:
#                             el.count += 1
#                         else:
#                             el.pairs[currel] += 1
#     frame = pd.read_excel("bokas.xlsx", sheet_name=structure, index_col=0)
#     for index, row in frame.iterrows():
#         for col in range(26):
#             if str(row[col]) != "nan":
#                 row[col] = elements[col].pairs[index]
#     frame.to_excel("datasheets/metastablepairs-" + structure.lower() + ".xlsx", sheet_name="1000K")
#
# #
# # metastabilityCount("FCC", els)
# # metastabilityCount("BCC", els)
#
# def plot_omega_vs_count(structure):
#     bin_interactions = pd.read_excel("bokas.xlsx", sheet_name=structure, index_col=0)
#     count = pd.read_excel("datasheets/metastablepairs-" + structure.lower() + ".xlsx", sheet_name="1000K")
#     count.set_index('Unnamed: 0', inplace=True)
#     df_out = pd.DataFrame()
#     df_out["Binary"] = ""
#     df_out["Count"] = ""
#     k = 0
#     for row in range(26):
#         for col in range(26):
#             if str(bin_interactions.iloc[row, col]) != "nan":
#                 df_out.at[k, "Binary"] = bin_interactions.iloc[row, col]
#                 df_out.at[k, "Count"] = count.iloc[row, col]
#                 k += 1
#     df_out.to_excel("plot_count_" + structure.lower() + ".xlsx")
#
# plot_omega_vs_count("BCC")
#

import pandas as pd
import numpy as np
structure = "BCC"
els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
       'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
       'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
OERels = ['Co', 'Fe', 'Mn', 'Mo', 'Ni', 'Ti', 'Pt', 'Pd', 'Ir', 'Rh']
pd2 = pd.read_excel("stable/3-" + structure.lower() + ".xlsx")
pd3 = pd.read_excel("datasheets/3-" + structure.lower() + ".xlsx")
# pd4 = pd.read_excel("4-" + structure.lower() + ".xlsx")
# pd5 = pd.read_excel("5-" + structure.lower() + ".xlsx")
entries = []
for i, r in pd2.iterrows():
    for index, row in pd3.iterrows():
        if row["e_hull"] < r["e_hull"]:
            qin = [row["e1"], row["e2"], row["e3"]]
            if r["e1"] in qin and r["e2"]:
                entries.append(index)
        if row["e_hull"] >= r["e_hull"]:
            break
        if row["e_hull"] >= r["e_hull"]:
            break
df = pd.DataFrame()
for i in entries:
    df = df.append(pd3.iloc[i])
df.to_excel("stable/3-"+structure.lower()+".xlsx")
