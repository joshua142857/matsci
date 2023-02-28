import itertools
import random
import time
import pandas as pd
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry, Element
from matminer.data_retrieval.retrieve_MP import MPDataRetrieval
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from mp_api.client import MPRester, Composition
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

def run3(structure, el1, el2, el3):
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

    df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/bokas.xlsx', sheet_name=structure)
    # df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx', sheet_name="our work")
    df_sqs_2.set_index('Unnamed: 0', inplace=True)

    df_3 = pd.read_excel('./enthalpy_data_and_predictions/3element.xlsx', sheet_name='Ternary ' + structure)
    # df_3 = pd.read_excel('./enthalpy_data_and_predictions/mixing_enthalpy_predictions.xlsx', sheet_name='ternary')
    df_3["phase"] = ""
    for index, row in df_3.iterrows():
        e1 = row['e1']
        e2 = row['e2']
        e3 = row['e3']
        if str(e1 + e2 + e3) == str(el1 + el2 + el3):
            df_pd = pd.DataFrame()
            # ternary
            df_pd.at[0, 'comp'] = row['comp']
            df_pd.at[0, 'Hf'] = row['enthalpy']
            df_pd.at[0, 'S'] = row['entropy']
            # binary
            df_pd.at[1, 'comp'] = e1 + e2
            df_pd.at[1, 'Hf'] = df_sqs_2[e1][e2]
            df_pd.at[1, 'S'] = 5.9730802545007364e-05
            df_pd.at[2, 'comp'] = e1 + e3
            df_pd.at[2, 'Hf'] = df_sqs_2[e1][e3]
            df_pd.at[2, 'S'] = 5.9730802545007364e-05
            df_pd.at[3, 'comp'] = e2 + e3
            df_pd.at[3, 'Hf'] = df_sqs_2[e2][e3]
            df_pd.at[3, 'S'] = 5.9730802545007364e-05
            # elements
            df_pd.at[4, 'comp'] = e1
            df_pd.at[4, 'Hf'] = 0
            df_pd.at[4, 'S'] = 0
            df_pd.at[5, 'comp'] = e2
            df_pd.at[5, 'Hf'] = 0
            df_pd.at[5, 'S'] = 0
            df_pd.at[6, 'comp'] = e3
            df_pd.at[6, 'Hf'] = 0
            df_pd.at[6, 'S'] = 0
            # query binary intermetallic from the materials project
            el = {e1, e2, e3}
            df_1 = DataRetrieval(binary())
            df_2 = DataRetrieval(ternary())
            if not df_2.empty:
                df_1 = pd.concat([df_2, df_1], ignore_index=True)
            df_in = pd.DataFrame()
            df_in['comp'] = df_1['pretty_formula']
            df_in['Hf'] = df_1['formation_energy_per_atom']
            df_in['S'] = 0
            df_final = pd.concat([df_pd, df_in], ignore_index=True)
            # build phase diagram
            comps = df_final['comp']
            temp = 100

            def phasecheck(t):
                Ef = df_final['Hf'] - t * df_final['S']
                mg_comp = [None] * len(comps)
                for i in range(len(comps)):
                    mg_comp[i] = Composition(comps[i])
                    entries3 = [None] * len(mg_comp)
                for i in range(len(mg_comp)):
                    entries3[i] = PDEntry(composition=mg_comp[i], energy=Ef[i])
                for i in range(len(entries3)):
                    print(entries3[i])
                phase = PhaseDiagram(entries3)
                df_3.loc[index, 'phase'] = phase
                # print(phase)
                # get decomposition and e_above_hull
                test = PDEntry(composition=mg_comp[0], energy=Ef[0])
                # for i in range(len(entries3)):
                #     test = PDEntry(composition=mg_comp[i], energy=Ef[i])
                #     entry = str(phase.get_decomp_and_e_above_hull(test))
                #     print(entry)
                print(test)
                entry = str(phase.get_decomp_and_e_above_hull(test))
                # print(entry)
                ehull = entry.split("}, ")[1].rstrip(")")
                phase = entry.split("}, ")[0].lstrip("(") + "}"
                # ehull = str(phase.get_e_above_hull(test))
                df_3.loc[index, "e_hull"] = ehull
                # for i in entries3:
                #     print(i)
                print(ehull)
                print(phase)
                return float(ehull)

            temperature = []
            eahull = []
            for x in range(20):
                temperature.append(temp)
                x = phasecheck(temp)
                eahull.append(x)
                temp += 100
            fig, ax = plt.subplots()
            ax.plot(temperature, eahull)
            plt.xlabel('Temperature (K)')
            plt.ylabel('Energy above hull')
            title = "Stability vs. Temperature for " + el1 + el2 + el3
            plt.title(title)
            plt.show()
            return
    return "Not Found"


def run4(structure, el1, el2, el3, el4):
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

    df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/bokas.xlsx', sheet_name=structure)
    df_sqs_2.set_index('Unnamed: 0', inplace=True)

    df_3 = pd.read_excel('./enthalpy_data_and_predictions/3element.xlsx', sheet_name='Ternary ' + structure)
    df_4 = pd.read_excel('./enthalpy_data_and_predictions/4element.xlsx', sheet_name='Quaternary ' + structure)
    df_4["phase"] = ""
    for index, row in df_4.iterrows():
        e1 = row['e1']
        e2 = row['e2']
        e3 = row['e3']
        e4 = row['e4']
        if str(e1 + e2 + e3 + e4) == str(el1 + el2 + el3 + el4):
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
            df_1 = DataRetrieval(binary())
            df_2 = DataRetrieval(ternary())
            if not df_2.empty:
                df_1 = pd.concat([df_2, df_1], ignore_index=True)
            df_in = pd.DataFrame()
            df_in['comp'] = df_1['pretty_formula']
            df_in['Hf'] = df_1['formation_energy_per_atom']
            df_in['S'] = 0
            df_final = pd.concat([df_pd, df_in], ignore_index=True)
            # build phase diagram
            comps = df_final['comp']
            temp = 0

            def phasecheck(t):
                Ef = df_final['Hf'] - t * df_final['S']
                mg_comp = [None] * len(comps)
                for i in range(len(comps)):
                    mg_comp[i] = Composition(comps[i])
                    entries3 = [None] * len(mg_comp)
                for i in range(len(mg_comp)):
                    entries3[i] = PDEntry(composition=mg_comp[i], energy=Ef[i])
                phase = PhaseDiagram(entries3)
                df_4.loc[index, 'phase'] = phase
                # print(phase)
                # get decomposition and e_above_hull
                test = PDEntry(composition=mg_comp[0], energy=Ef[0])
                # for i in range(len(entries3)):
                #     test = PDEntry(composition=mg_comp[i], energy=Ef[i])
                #     entry = str(phase.get_decomp_and_e_above_hull(test))
                #     print(entry)
                print(test)
                entry = str(phase.get_decomp_and_e_above_hull(test))
                print(entry)
                ehull = entry.split("}, ")[1].rstrip(")")
                phase = entry.split("}, ")[0].lstrip("(") + "}"
                df_4.loc[index, "e_hull"] = ehull
                # for i in entries3:
                #     print(i)
                print(ehull)
                print(phase)
                return float(ehull)

            temperature = []
            eahull = []
            for x in range(20):
                temperature.append(temp)
                x = phasecheck(temp)
                eahull.append(x)
                temp += 100
            fig, ax = plt.subplots()
            ax.plot(temperature, eahull)
            plt.xlabel('Temperature (K)')
            plt.ylabel('Energy above hull')
            title = "Stability vs. Temperature for " + el1 + el2 + el3 + el4
            plt.title(title)
            plt.show()
            return
    return "Not Found"


def run5(structure, el1, el2, el3, el4, el5):
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

    df_sqs_2 = pd.read_excel('./enthalpy_data_and_predictions/bokas.xlsx', sheet_name=structure)
    df_sqs_2.set_index('Unnamed: 0', inplace=True)

    df_3 = pd.read_excel('./enthalpy_data_and_predictions/3element.xlsx', sheet_name='Ternary ' + structure)
    df_4 = pd.read_excel('./enthalpy_data_and_predictions/4element.xlsx', sheet_name='Quaternary ' + structure)
    df_5 = pd.read_excel('./enthalpy_data_and_predictions/5element.xlsx', sheet_name='Quinary ' + structure)
    df_5["phase"] = ""
    for index, row in df_5.iterrows():
        e1 = row['e1']
        e2 = row['e2']
        e3 = row['e3']
        e4 = row['e4']
        e5 = row['e5']
        if str(e1 + e2 + e3 + e4 + e5) == str(el1 + el2 + el3 + el4 + el5):
            df_pd = pd.DataFrame()
            # quinary
            df_pd.at[0, 'comp'] = row['comp']
            df_pd.at[0, 'Hf'] = row['enthalpy']
            df_pd.at[0, 'S'] = row['entropy']
            # quarternary
            df_a = df_4[df_4['comp'].str.match(e1 + e2 + e3 + e4)]
            df_a.reset_index(drop=True, inplace=True)
            df_b = df_4[df_4['comp'].str.match(e1 + e2 + e3 + e5)]
            df_b.reset_index(drop=True, inplace=True)
            df_c = df_4[df_4['comp'].str.match(e1 + e3 + e4 + e5)]
            df_c.reset_index(drop=True, inplace=True)
            df_d = df_4[df_4['comp'].str.match(e2 + e3 + e4 + e5)]
            df_d.reset_index(drop=True, inplace=True)
            df_e = df_4[df_4['comp'].str.match(e1 + e2 + e4 + e5)]
            df_e.reset_index(drop=True, inplace=True)
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
            df_pd.at[5, 'comp'] = df_e.loc[0, 'comp']
            df_pd.at[5, 'Hf'] = df_e.loc[0, 'enthalpy']
            df_pd.at[5, 'S'] = df_e.loc[0, 'entropy']
            # ternary
            df_a1 = df_3[df_3['comp'].str.match(e1 + e2 + e3)]
            df_a1.reset_index(drop=True, inplace=True)
            df_b1 = df_3[df_3['comp'].str.match(e1 + e2 + e4)]
            df_b1.reset_index(drop=True, inplace=True)
            df_c1 = df_3[df_3['comp'].str.match(e1 + e2 + e5)]
            df_c1.reset_index(drop=True, inplace=True)
            df_d1 = df_3[df_3['comp'].str.match(e1 + e3 + e4)]
            df_d1.reset_index(drop=True, inplace=True)
            df_e1 = df_3[df_3['comp'].str.match(e1 + e3 + e5)]
            df_e1.reset_index(drop=True, inplace=True)
            df_f1 = df_3[df_3['comp'].str.match(e1 + e4 + e5)]
            df_f1.reset_index(drop=True, inplace=True)
            df_g1 = df_3[df_3['comp'].str.match(e2 + e3 + e4)]
            df_g1.reset_index(drop=True, inplace=True)
            df_h1 = df_3[df_3['comp'].str.match(e2 + e3 + e5)]
            df_h1.reset_index(drop=True, inplace=True)
            df_i1 = df_3[df_3['comp'].str.match(e2 + e4 + e5)]
            df_i1.reset_index(drop=True, inplace=True)
            df_j1 = df_3[df_3['comp'].str.match(e3 + e4 + e5)]
            df_j1.reset_index(drop=True, inplace=True)
            df_pd.at[6, 'comp'] = df_a1.loc[0, 'comp']
            df_pd.at[6, 'Hf'] = df_a1.loc[0, 'enthalpy']
            df_pd.at[6, 'S'] = df_a1.loc[0, 'entropy']
            df_pd.at[7, 'comp'] = df_b1.loc[0, 'comp']
            df_pd.at[7, 'Hf'] = df_b1.loc[0, 'enthalpy']
            df_pd.at[7, 'S'] = df_b1.loc[0, 'entropy']
            df_pd.at[8, 'comp'] = df_c1.loc[0, 'comp']
            df_pd.at[8, 'Hf'] = df_c1.loc[0, 'enthalpy']
            df_pd.at[8, 'S'] = df_c1.loc[0, 'entropy']
            df_pd.at[9, 'comp'] = df_d1.loc[0, 'comp']
            df_pd.at[9, 'Hf'] = df_d1.loc[0, 'enthalpy']
            df_pd.at[9, 'S'] = df_d1.loc[0, 'entropy']
            df_pd.at[10, 'comp'] = df_e1.loc[0, 'comp']
            df_pd.at[10, 'Hf'] = df_e1.loc[0, 'enthalpy']
            df_pd.at[10, 'S'] = df_e1.loc[0, 'entropy']
            df_pd.at[11, 'comp'] = df_f1.loc[0, 'comp']
            df_pd.at[11, 'Hf'] = df_f1.loc[0, 'enthalpy']
            df_pd.at[11, 'S'] = df_f1.loc[0, 'entropy']
            df_pd.at[12, 'comp'] = df_g1.loc[0, 'comp']
            df_pd.at[12, 'Hf'] = df_g1.loc[0, 'enthalpy']
            df_pd.at[12, 'S'] = df_g1.loc[0, 'entropy']
            df_pd.at[13, 'comp'] = df_h1.loc[0, 'comp']
            df_pd.at[13, 'Hf'] = df_h1.loc[0, 'enthalpy']
            df_pd.at[13, 'S'] = df_h1.loc[0, 'entropy']
            df_pd.at[14, 'comp'] = df_i1.loc[0, 'comp']
            df_pd.at[14, 'Hf'] = df_i1.loc[0, 'enthalpy']
            df_pd.at[14, 'S'] = df_i1.loc[0, 'entropy']
            df_pd.at[15, 'comp'] = df_j1.loc[0, 'comp']
            df_pd.at[15, 'Hf'] = df_j1.loc[0, 'enthalpy']
            df_pd.at[15, 'S'] = df_j1.loc[0, 'entropy']
            # binary
            df_pd.at[16, 'comp'] = e1 + e2
            df_pd.at[16, 'Hf'] = df_sqs_2[e1][e2]
            df_pd.at[16, 'S'] = 5.9730802545007364e-05
            df_pd.at[17, 'comp'] = e1 + e3
            df_pd.at[17, 'Hf'] = df_sqs_2[e1][e3]
            df_pd.at[17, 'S'] = 5.9730802545007364e-05
            df_pd.at[18, 'comp'] = e1 + e4
            df_pd.at[18, 'Hf'] = df_sqs_2[e1][e4]
            df_pd.at[18, 'S'] = 5.9730802545007364e-05
            df_pd.at[19, 'comp'] = e1 + e5
            df_pd.at[19, 'Hf'] = df_sqs_2[e1][e5]
            df_pd.at[19, 'S'] = 5.9730802545007364e-05
            df_pd.at[20, 'comp'] = e2 + e3
            df_pd.at[20, 'Hf'] = df_sqs_2[e2][e3]
            df_pd.at[20, 'S'] = 5.9730802545007364e-05
            df_pd.at[21, 'comp'] = e2 + e4
            df_pd.at[21, 'Hf'] = df_sqs_2[e2][e4]
            df_pd.at[21, 'S'] = 5.9730802545007364e-05
            df_pd.at[22, 'comp'] = e2 + e5
            df_pd.at[22, 'Hf'] = df_sqs_2[e2][e5]
            df_pd.at[22, 'S'] = 5.9730802545007364e-05
            df_pd.at[23, 'comp'] = e3 + e4
            df_pd.at[23, 'Hf'] = df_sqs_2[e3][e4]
            df_pd.at[23, 'S'] = 5.9730802545007364e-05
            df_pd.at[24, 'comp'] = e3 + e5
            df_pd.at[24, 'Hf'] = df_sqs_2[e3][e5]
            df_pd.at[24, 'S'] = 5.9730802545007364e-05
            df_pd.at[25, 'comp'] = e4 + e5
            df_pd.at[25, 'Hf'] = df_sqs_2[e4][e5]
            df_pd.at[25, 'S'] = 5.9730802545007364e-05
            # elements
            df_pd.at[26, 'comp'] = e1
            df_pd.at[26, 'Hf'] = 0
            df_pd.at[26, 'S'] = 0
            df_pd.at[27, 'comp'] = e2
            df_pd.at[27, 'Hf'] = 0
            df_pd.at[27, 'S'] = 0
            df_pd.at[28, 'comp'] = e3
            df_pd.at[28, 'Hf'] = 0
            df_pd.at[28, 'S'] = 0
            df_pd.at[29, 'comp'] = e4
            df_pd.at[29, 'Hf'] = 0
            df_pd.at[29, 'S'] = 0
            df_pd.at[30, 'comp'] = e5
            df_pd.at[30, 'Hf'] = 0
            df_pd.at[30, 'S'] = 0
            # query binary intermetallic from the materials project
            el = {e1, e2, e3, e4, e5}
            df_1 = DataRetrieval(binary())
            df_2 = DataRetrieval(ternary())
            if not df_2.empty:
                df_1 = pd.concat([df_2, df_1], ignore_index=True)
            df_in = pd.DataFrame()
            df_in['comp'] = df_1['formula_pretty']
            df_in['Hf'] = df_1['formation_energy_per_atom']
            df_in['S'] = 0
            df_final = pd.concat([df_pd, df_in], ignore_index=True)
            # build phase diagram
            comps = df_final['comp']
            temp = 0

            def phasecheck(t):
                Ef = df_final['Hf'] - t * df_final['S']
                mg_comp = [None] * len(comps)
                for i in range(len(comps)):
                    mg_comp[i] = Composition(comps[i])
                    entries3 = [None] * len(mg_comp)
                for i in range(len(mg_comp)):
                    entries3[i] = PDEntry(composition=mg_comp[i], energy=Ef[i])
                phase = PhaseDiagram(entries3)
                df_5.loc[index, 'phase'] = phase
                # get decomposition and e_above_hull
                test = PDEntry(composition=mg_comp[0], energy=Ef[0])
                entry = str(phase.get_decomp_and_e_above_hull(test))
                ehull = entry.split("}, ")[1].rstrip(")")
                decomp = entry.split("}, ")[0].lstrip("(") + "}"
                df_5.loc[index, "e_hull"] = ehull
                return float(ehull), decomp

            temperature = []
            eahull = []
            decomps = []
            for x in range(50):
                temperature.append(temp)
                x, phase = phasecheck(temp)
                decomps.append((phase, temp))
                eahull.append(x)
                temp += 50
            fig, ax = plt.subplots()
            ax.plot(temperature, eahull)
            ax.fill_between(temperature, eahull, 0, alpha=0.3)
            plt.xlabel('Temperature (K)')
            plt.ylabel('Energy above hull')
            tempphase = ""
            for d in decomps:
                if decompsplit(d[0]) != tempphase:
                    ax.text(d[1], 0.0001*(decomps.index(d)), decompsplit(d[0]))
                    tempphase = decompsplit(d[0])
            title = "Stability vs. Temperature for " + el1 + el2 + el3 + el4 + el5
            plt.title(title)
            plt.show()
            return

def decompsplit(string):
    begin = []
    end = []
    comps = []
    string = string.replace("PDEntry : ", "|")
    string = string.replace(" with energy ", "?")
    for i in range(len(string)):
        if string[i] == "|":
            begin.append(i)
        if string[i] == "?":
            end.append(i)
    for i in range(len(begin)):
        comps.append(Composition(string[begin[i] + 1: end[i]]).reduced_formula)
    return comps




print(run5("FCC", "Co", "Cr", "Fe", "Ni", "W"))
