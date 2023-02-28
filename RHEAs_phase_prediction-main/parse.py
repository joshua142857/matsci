import pandas as pd
import numpy as np

structure = "FCC"
els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
       'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
       'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
OERels = ['Co', 'Fe', 'Mn', 'Mo', 'Ni', 'Ti', 'Pt', 'Pd', 'Ir', 'Rh']

class Element:
    def __init__(self, name):
        self.name = name
        self.count = 0
        new_dict = {}
        for el in els:
            if el != name:
                new_dict[el] = 0
        self.pairs = new_dict


def metastabilityCount(structure, els):
    elements = []
    for el in els:
        elements.append(Element(el))
    data = pd.read_excel("5-" + structure.lower() + ".xlsx", sheet_name="1000K")
    for index, row in data.iterrows():
        if row["e_hull"] >= 0.05:
            print("Done")
            break
        else:
            currentels = [row["e1"], row["e2"], row["e3"], row["e4"], row["e5"]]

            def check(el):
                for c in currentels:
                    if el.name == c:
                        return True
                return False

            for el in elements:
                if check(el):
                    for currel in currentels:
                        if el.name == currel:
                            el.count += 1
                        else:
                            el.pairs[currel] += 1
    frame = pd.read_excel("enthalpy_data_and_predictions/bokas.xlsx", sheet_name=structure, index_col=0)
    for index, row in frame.iterrows():
        for col in range(26):
            print(row[0])
            if str(row[col]) != "nan":
                row[col] = elements[col].pairs[index]
    frame.to_excel("metastablepairs-" + structure.lower() + ".xlsx", sheet_name="1000K")
