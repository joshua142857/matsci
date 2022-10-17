# import pandas as pd
#
# df = pd.read_excel('5-e.xlsx')
# for index, row in df.iterrows():
#     entry = row["phase"]
#     x = entry.split("}, ")[1].rstrip(")")
#     df.at[index, "e_hull"] = x
#     y = entry.split("}, ")[0].lstrip("(") + "}"
#     df.at[index, "phase"] = y
#
# df.to_excel('5-efinal.xlsx', sheet_name="1000K")
import matplotlib.pyplot as plt
data = {'ternary': 5, 'quaternary': 15, 'quinary': 5}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(figsize=(1, 1))
axs[0].bar(names, values)
fig.suptitle('Categorical Plotting')

