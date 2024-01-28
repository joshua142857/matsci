# import itertools
# import os
# import random
# import time
# import pandas as pd
# import xlsxwriter
# import math
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry, Element
from mp_api.client import MPRester
# from pymatgen.core import Composition

with MPRester(api_key="NUNc2qkYfekFR1DkxzhKvBCAMVAgOLoF") as mpr:
    thermo_docs = mpr.thermo.search(material_ids=["mp-989695"], thermo_types=["GGA_GGA+U"])

    # In addition, you can specify the level of theory by using "thermo_type", the default is "GGA_GGA+U_R2SCAN":
    # thermo_docs = mpr.summary.search(formula="Ag", fields=["structure", "material_id"])

print(thermo_docs)