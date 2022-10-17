import os
import pandas as pd
import numpy as np

structure = "FCC"
df = pd.read_excel('./enthalpy_data_and_predictions/5element.xlsx', sheet_name='Quinary ' + structure)
df["phase"] = ""
df["e_hull"] = ""

directory = './sheets2'

for exc in os.listdir(directory):
    print("parsing through " + str(exc))
    f = os.path.join(directory, exc)
    data = pd.read_excel(f, usecols={"phase"})
    cnt = 0
    for index, row in data.iterrows():
        if df.loc[index, "phase"] + " " == " ":
            if isinstance(row[0], str):
                print(row[0])
                df.loc[index, "phase"] = row[0]
                cnt = 1
        elif cnt == 1:
            break
df.to_excel("5-ebcc.xlsx", sheet_name='BCC')
