# Retrieves known compounds from Materials Project
# Creates database of intermetallics for use in phase diagrams
# alloySystem.create_intermetallics()

import itertools
import pandas as pd
from mp_api.client import MPRester
from pymatgen.core import Composition, Element


def run(el):
    mpr = MPRester(api_key="NUNc2qkYfekFR1DkxzhKvBCAMVAgOLoF")  # Materials ID

    def DataRetrieval(chemsys):
        fields = ['formula_pretty', 'formation_energy_per_atom']
        # fields = ['formula_pretty', 'formation_energy_per_atom', 'energy_above_hull']
        docs = mpr.summary.search(chemsys=chemsys, fields=fields)
        df = pd.DataFrame(columns=fields)
        for row in range(len(docs)):
            df.at[row, 'formula_pretty'] = docs[row].formula_pretty
            df.at[row, 'formation_energy_per_atom'] = docs[row].formation_energy_per_atom
            # df.at[row, 'energy_above_hull'] = docs[row].energy_above_hull
        return df

    def binary():
        first_el = el
        second_el = el
        return sorted({"{}-{}".format(*sorted(pair))
                       for pair in itertools.product(first_el, second_el)})

    def ternary():
        """
        Return a sorted list of chemical systems
            of the form [...,"Li-Be-S",...,"Al-Zr-Se",...]
        """
        first_el = el
        second_el = el
        third_el = el
        return sorted({"{}-{}-{}".format(*sorted(triple))
                       for triple in itertools.product(first_el, second_el, third_el)})

    # el = {"Mo", "Nb", "Ta", "V", "W", "Zr", "Ti", "Al", "Hf", "Cr", "C", "Re", "Ru", "Os", "Rh", "Ir", "Si"}
    # el = {'Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
    #       'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
    #       'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd'}
    df_1 = pd.DataFrame()
    dfinal = pd.DataFrame()
    temp = []
    for pair in binary():
        df_1 = pd.concat([df_1, DataRetrieval(pair)], ignore_index=False)
        temp.append(pair)
        print(pair)
    for triple in ternary():
        df_1 = pd.concat([df_1, DataRetrieval(triple)], ignore_index=False)
        temp.append(triple)
        print(triple)
    dfinal['comp'] = df_1['formula_pretty']
    dfinal['enthalpy'] = df_1['formation_energy_per_atom']
    dfinal.reset_index(inplace=True, drop=True)
    for index, row in dfinal.iterrows():
        dfinal.at[
            index, "comptype"] = f"{''.join([e for e in sorted(list(el)) if Element(e) in Composition(row['comp']).elements])}"
    return dfinal


run({'Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
     'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
     'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd'})
