from mp_api.client import MPRester
import pandas as pd

def DataRetrieval(chemsys):
    fields = ['formula_pretty','formation_energy_per_atom','energy_above_hull']
    with MPRester("NUNc2qkYfekFR1DkxzhKvBCAMVAgOLoF") as mpr:
        docs = mpr.summary.search(chemsys=chemsys, fields=fields)
    df = pd.DataFrame(columns=fields)
    for row in range(len(docs)):
        df.at[row, 'formula_pretty'] = docs[row].formula_pretty
        df.at[row, 'formation_energy_per_atom'] = docs[row].formation_energy_per_atom
        df.at[row, 'energy_above_hull'] = docs[row].energy_above_hull
        row += 1
    return df
