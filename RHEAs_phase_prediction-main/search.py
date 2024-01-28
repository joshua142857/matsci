import pandas as pd
def search(structure, c, e1, e2):
    tern = pd.read_excel("rubokasggabcc" + "/" + str(c) + "-e1000.xlsx")
    dfout = pd.DataFrame()
    cnt = 0
    for index, row in tern.iterrows():
        if row["comp"].find(e1) != -1 and row["comp"].find(e2) != -1:
            dfout.at[cnt, "comp"] = row["comp"]
            dfout.at[cnt, "ehull"] = row["ehull"]
            cnt += 1
    dfout.to_excel(str(c) + e1 + e2 + "tset" + structure.lower() + ".xlsx")

# search("FCC", 4, "Cu", "Ru")
search("BCC", 3, "Cu", "Ag")