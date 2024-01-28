# Unused management script to combine parallel results into one datasheet
import os
import pandas as pd
import numpy as np

structure = "FCC"
df = pd.read_excel('./5element.xlsx', sheet_name='Quinary ' + structure)
df["phase"] = ""
df["e_hull"] = ""

directory = './5bcc'

for exc in os.listdir(directory):
    print("parsing through " + str(exc))
    f = os.path.join(directory, exc)
    data = pd.read_excel(f, usecols={"phase", "e_hull"})
    cnt = 0
    for index, row in data.iterrows():
        if df.loc[index, "phase"] is not None:
            if isinstance(row["phase"], str):
                print(row["e_hull"])
                df.at[index, "phase"] = row["phase"]
                df.at[index, "e_hull"] = row["e_hull"]
        #         cnt = 1
        # elif cnt == 1:
        #     break
df.to_excel("5-bcc.xlsx", sheet_name=structure)
