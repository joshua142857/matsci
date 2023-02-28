import matplotlib.pyplot as plt
plt.style.use('classic')
import numpy as np
import pandas as pd
structure = "BCC"
# rng = np.random.RandomState(0)
# x = np.linspace(0, 10, 500)
# y = np.cumsum(rng.randn(500, 6), 0)
data = pd.read_excel("metastablepairs-" + structure.lower() + ".xlsx", sheet_name="1000K", index_col=0)
# data = pd.read_excel("enthalpy_data_and_predictions/bokas.xlsx", sheet_name=structure, index_col=0)
print(data)
import seaborn as sns
sns.set()
#
# els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
#        'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
#        'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)
sns.heatmap(data, square=True, vmax=200, vmin=0)
plt.title('Metastable Binary Pairs for Quaternary HEA ' + structure + ' at 1000K')
# sns.heatmap(data, square=True, cmap="coolwarm", vmax=1, vmin=-1)
# plt.title("Binary Enthalpies for " + structure)
plt.show()

