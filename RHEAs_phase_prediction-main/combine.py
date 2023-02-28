import os
import pandas as pd
import numpy as np

structure = "BCC"
df = pd.read_excel('./enthalpy_data_and_predictions/4element.xlsx', sheet_name='Quaternary ' + structure)
df["phase"] = ""
df["e_hull"] = ""

directory = './4bcc'

for exc in os.listdir(directory):
    print("parsing through " + str(exc))
    f = os.path.join(directory, exc)
    data = pd.read_excel(f, usecols={"phase", "e_hull"})
    cnt = 0
    for index, row in data.iterrows():
        if df.loc[index, "phase"] is not None:
            if isinstance(row["phase"], str):
                # print(row[0])
                # entry = row["phase"]
                # x = entry.split("}, ")[1].rstrip(")")
                # df.at[index, "e_hull"] = x
                # y = entry.split("}, ")[0].lstrip("(") + "}"
                # df.at[index, "phase"] = y
                print(row["e_hull"])
                df.at[index, "phase"] = row["phase"]
                df.at[index, "e_hull"] = row["e_hull"]
        #         cnt = 1
        # elif cnt == 1:
        #     break
df.to_excel("4-bcc.xlsx", sheet_name=structure)
