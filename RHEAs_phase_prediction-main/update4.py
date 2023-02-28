import itertools
import time
import pandas as pd
import math
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry, Element
from mp_api.client import MPRester, Composition


def run(start, end, structure):
    df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/bokas.xlsx', sheet_name=structure)
    df_sqs_2.set_index('Unnamed: 0', inplace=True)
    mpr = MPRester("NUNc2qkYfekFR1DkxzhKvBCAMVAgOLoF")

    def DataRetrieval(chemsys):
        fields = ['formula_pretty', 'formation_energy_per_atom', 'energy_above_hull']
        docs = mpr.summary.search(chemsys=chemsys, fields=fields)
        df = pd.DataFrame(columns=fields)
        for row in range(len(docs)):
            df.at[row, 'formula_pretty'] = docs[row].formula_pretty
            df.at[row, 'formation_energy_per_atom'] = docs[row].formation_energy_per_atom
            df.at[row, 'energy_above_hull'] = docs[row].energy_above_hull
            row += 1
        return df
    def binary():
        """
        Return a sorted list of chemical systems
            of the form [...,"Li-Be-S",...,"Al-Zr-Se",...]
        """
        first_el = el
        second_el = el
        return sorted(["{}-{}".format(*sorted(pair))
                       for pair in itertools.product(first_el, second_el)])

    def ternary():
        """
        Return a sorted list of chemical systems
            of the form [...,"Li-Be-S",...,"Al-Zr-Se",...]
        """
        first_el = el
        second_el = el
        third_el = el
        return sorted(["{}-{}-{}".format(*sorted(triple))
                       for triple in itertools.product(first_el, second_el, third_el)])

    df_3 = pd.read_excel('./enthalpy_data_and_predictions/3element.xlsx', sheet_name='Ternary ' + structure)
    df_4 = pd.read_excel('./enthalpy_data_and_predictions/4element.xlsx', sheet_name='Quaternary ' + structure)
    df_4["phase"] = ""
    initial_row = start
    current_row = initial_row
    for index, row in df_4.iterrows():
        if index < current_row:
            pass
        if current_row >= end:
            break
        else:
            e1 = row['e1']
            e2 = row['e2']
            e3 = row['e3']
            e4 = row['e4']
            df_pd = pd.DataFrame()
            # quarternary
            df_pd.at[0, 'comp'] = row['comp']
            df_pd.at[0, 'Hf'] = row['enthalpy']
            df_pd.at[0, 'S'] = row['entropy']
            # ternary
            df_a = df_3[df_3['comp'].str.match(e1 + e2 + e3)]
            df_a.reset_index(drop=True, inplace=True)
            df_b = df_3[df_3['comp'].str.match(e1 + e2 + e4)]
            df_b.reset_index(drop=True, inplace=True)
            df_c = df_3[df_3['comp'].str.match(e1 + e3 + e4)]
            df_c.reset_index(drop=True, inplace=True)
            df_d = df_3[df_3['comp'].str.match(e2 + e3 + e4)]
            df_d.reset_index(drop=True, inplace=True)
            df_pd.at[1, 'comp'] = df_a.loc[0, 'comp']
            df_pd.at[1, 'Hf'] = df_a.loc[0, 'enthalpy']
            df_pd.at[1, 'S'] = df_a.loc[0, 'entropy']
            df_pd.at[2, 'comp'] = df_b.loc[0, 'comp']
            df_pd.at[2, 'Hf'] = df_b.loc[0, 'enthalpy']
            df_pd.at[2, 'S'] = df_b.loc[0, 'entropy']
            df_pd.at[3, 'comp'] = df_c.loc[0, 'comp']
            df_pd.at[3, 'Hf'] = df_c.loc[0, 'enthalpy']
            df_pd.at[3, 'S'] = df_c.loc[0, 'entropy']
            df_pd.at[4, 'comp'] = df_d.loc[0, 'comp']
            df_pd.at[4, 'Hf'] = df_d.loc[0, 'enthalpy']
            df_pd.at[4, 'S'] = df_d.loc[0, 'entropy']
            # binary
            df_pd.at[5, 'comp'] = e1 + e2
            df_pd.at[5, 'Hf'] = df_sqs_2[e1][e2]
            df_pd.at[5, 'S'] = 5.9730802545007364e-05
            df_pd.at[6, 'comp'] = e1 + e3
            df_pd.at[6, 'Hf'] = df_sqs_2[e1][e3]
            df_pd.at[6, 'S'] = 5.9730802545007364e-05
            df_pd.at[7, 'comp'] = e1 + e4
            df_pd.at[7, 'Hf'] = df_sqs_2[e1][e4]
            df_pd.at[7, 'S'] = 5.9730802545007364e-05
            df_pd.at[8, 'comp'] = e2 + e3
            df_pd.at[8, 'Hf'] = df_sqs_2[e2][e3]
            df_pd.at[8, 'S'] = 5.9730802545007364e-05
            df_pd.at[9, 'comp'] = e2 + e4
            df_pd.at[9, 'Hf'] = df_sqs_2[e2][e4]
            df_pd.at[9, 'S'] = 5.9730802545007364e-05
            df_pd.at[10, 'comp'] = e3 + e4
            df_pd.at[10, 'Hf'] = df_sqs_2[e3][e4]
            df_pd.at[10, 'S'] = 5.9730802545007364e-05
            # elements
            df_pd.at[11, 'comp'] = e1
            df_pd.at[11, 'Hf'] = 0
            df_pd.at[11, 'S'] = 0
            df_pd.at[12, 'comp'] = e2
            df_pd.at[12, 'Hf'] = 0
            df_pd.at[12, 'S'] = 0
            df_pd.at[13, 'comp'] = e3
            df_pd.at[13, 'Hf'] = 0
            df_pd.at[13, 'S'] = 0
            df_pd.at[14, 'comp'] = e4
            df_pd.at[14, 'Hf'] = 0
            df_pd.at[14, 'S'] = 0
            # query binary intermetallic from the materials project
            el = {e1, e2, e3, e4}


            df_in = pd.DataFrame()
            df_in['comp'] = df_1['formula_pretty']
            df_in['Hf'] = df_1['formation_energy_per_atom']
            df_in['S'] = 0
            df_final = pd.concat([df_pd, df_in], ignore_index=True)
            # build phase diagram
            comps = df_final['comp']
            Ef = df_final['Hf'] - 1000 * df_final['S']
            mg_comp = [None] * len(comps)
            for i in range(len(comps)):
                mg_comp[i] = Composition(comps[i])
                entries3 = [None] * len(mg_comp)
            for i in range(len(mg_comp)):
                entries3[i] = PDEntry(composition=mg_comp[i], energy=Ef[i])
            phase = PhaseDiagram(entries3)
            df_4.loc[index, 'phase'] = phase
            # get decomposition and e_above_hull
            test = PDEntry(composition=mg_comp[0], energy=Ef[0])
            out = str(phase.get_decomp_and_e_above_hull(test))
            x = out.split("}, ")[1].rstrip(")")
            df_4.at[index, "e_hull"] = x
            y = out.split("}, ")[0].lstrip("(") + "}"
            df_4.at[index, "phase"] = y
            print(y)
            current_row += 1
    df_4.to_excel("4" + structure.lower() + "/4-e" + str(initial_row) + "-" + str(current_row) + ".xlsx")


run(0, 15000, "FCC")
