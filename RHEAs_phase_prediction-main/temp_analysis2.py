import eahull
import pandas as pd
import itertools
from itertools import combinations
import matplotlib.pyplot as plt
df_out = pd.DataFrame(columns=["comp", "type", "e above hull"])
structure = "FCC"
elements = ["Co", "Cr", "Fe", "Mn", "W", "Zn"]
cnt = 0
for i in combinations(elements, 5):
    comp = ""
    for el in i:
        comp += el
    df_out.at[cnt, "comp"] = comp
    df_out.at[cnt, "type"] = "Quinary"
    df_out.at[cnt, "e above hull"] = eahull.run5(structure, i[0], i[1], i[2], i[3], i[4])
    cnt += 1
for i in combinations(elements, 4):
    comp = ""
    for el in i:
        comp += el
    df_out.at[cnt, "comp"] = comp
    df_out.at[cnt, "type"] = "Quaternary"
    df_out.at[cnt, "e above hull"] = eahull.run4(structure, i[0], i[1], i[2], i[3])
    cnt += 1
for i in combinations(elements, 3):
    comp = ""
    for el in i:
        comp += el
    df_out.at[cnt, "comp"] = comp
    df_out.at[cnt, "type"] = "Ternary"
    df_out.at[cnt, "e above hull"] = eahull.run3(structure, i[0], i[1], i[2])
    cnt += 1
name = structure
for i in elements:
    name += i
df_out.to_excel("temp_for_metastability/" + name + ".xlsx")
#
# data = {'ternary': [1, 2], 'quaternary': 15, 'quinary': 5}
# names = list(data.keys())
# values = list(data.values())
#
# fig, axs = plt.subplots(figsize=(1, 1))
# axs[0].bar(names, values)
# fig.suptitle('Categorical Plotting')
#
# print(eahull.run5("BCC", "Al", "Cu","Ni","W","Pt"))
# print(run3("BCC", "Co", "Cr","Mn"))