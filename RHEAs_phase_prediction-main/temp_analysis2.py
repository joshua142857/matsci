import eahull
import pandas as pd
import itertools
from itertools import combinations
import matplotlib.pyplot as plt
df_out = pd.DataFrame(columns=["comp", "type", "e above hull"])
structure = "FCC"
elements = ["Co", "Cr", "Mn", "Ni", "W", "Pd"]
cnt = 0
for i in combinations(elements, 5):
    comp = ""
    for el in i:
        comp += el
    df_out.iat[cnt, "comp"] = comp
    df_out.iat[cnt, "type"] = "Quinary"
    print(i[0])
    # df_out.iat[cnt, "e above hull"] = eahull.run5(structure, i[0], i[1], i[2], i[3], i[4])
    cnt += 1
for i in combinations(elements, 4):
    comp = ""
    for el in i:
        comp += el
    df_out.iat[cnt, "comp"] = comp
    df_out.iat[cnt, "type"] = "Quaternary"
    df_out.iat[cnt, "e above hull"] = eahull.run4(structure, i[0], i[1], i[2], i[3])
    cnt += 1
for i in combinations(elements, 3):
    comp = ""
    for el in i:
        comp += el
    df_out.iat[cnt, "comp"] = comp
    df_out.iat[cnt, "type"] = "Ternary"
    df_out.iat[cnt, "e above hull"] = eahull.run3(structure, i[0], i[1], i[2])
    cnt += 1
df_out.to_excel("temp_for_metastability.xlsx")
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