import numpy
import numpy as np
import pandas as pd
import math
import itertools
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, PDEntry, Element
from pymatgen.core import Composition
import plotly.io as pio
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import display
import plotly.graph_objects as go


def run(list_of_elements):
    df_sqs_2 = pd.read_excel('enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx',
                             sheet_name="our work",
                             index_col=0,
                             nrows=18)
    dfca = pd.DataFrame()
    els = list(df_sqs_2.columns)
    comp = []
    for e in els:
        if e in list_of_elements:
            comp.append(e)
    e1 = comp[0]
    e2 = comp[1]
    e3 = comp[2]
    e4 = comp[3]
    #
    # def pick_two(list_of_items):
    #     output = []
    #     for first in range(len(list_of_items) - 1):
    #         for second in range(len(list_of_items) - first - 1):
    #             output.append((list_of_items[first], list_of_items[second + first + 1]))
    #     return output
    #
    # dfca["comp"] = ""
    # for i in range(11):
    #     for j in range(11):
    #         for k in range(11):
    #             for l in range(11):
    #                 index = 11**3*i + 11**2*j + 11*k + l - 1
    #                 if index == -1:
    #                     pass
    #                 else:
    #                     dfca.loc[index, "i"] = i / 10.0
    #                     dfca.loc[index, "j"] = j / 10.0
    #                     dfca.loc[index, "k"] = k / 10.0
    #                     dfca.loc[index, "l"] = l / 10.0
    #                     dfca.loc[index, e1] = i / (i + j + k + l)
    #                     dfca.loc[index, e2] = j / (i + j + k + l)
    #                     dfca.loc[index, e3] = k / (i + j + k + l)
    #                     dfca.loc[index, e4] = l / (i + j + k + l)
    #                     coord = (i, j, k, l)
    #                     dfca.loc[index, "comp"] = "?"
    #                     # bug 0.1.1 : not sure why I have to initialize as a string during manipulation
    #                     for cor in range(4):
    #                         if coord[cor] != 0:
    #                             dfca.loc[index, "comp"] = dfca.loc[index, "comp"] + comp[cor]
    #                             if coord[cor] != 10:
    #                                 dfca.loc[index, "comp"] = dfca.loc[index, "comp"] + str(coord[cor] / 10.0)
    #                     dfca.loc[index, "comp"] = dfca.loc[index, "comp"].strip("?") # bug 0.1.1
    #                     dfca.loc[index, "enthalpy"] = 0
    #                     dfca.loc[index, "entropy"] = 0
    #                     # enthalpy
    #                     for a, b in pick_two(comp):
    #                         dfca.loc[index, "enthalpy"] = dfca.loc[index, "enthalpy"] \
    #                                                       + df_sqs_2.loc[b, a] \
    #                                                       * dfca.loc[index, a] \
    #                                                       * dfca.loc[index, b] * 4.0
    #                     # entropy
    #                     for element in comp:
    #                         molar_fraction = dfca.loc[index, element]
    #                         if molar_fraction != 0:
    #                             dfca.loc[index, "entropy"] = dfca.loc[index, "entropy"] - 8.617333262e-05 * molar_fraction \
    #                                                      * math.log(molar_fraction)
    # dfca.to_excel("1ouTi.xlsx")
    dfca = pd.read_excel("1ouTi.xlsx")
    x = []
    y = []
    z = []
    w = []
    c = []

    def binary():
        """
        Return a sorted list of chemical systems
            of the form [...,"Li-Be",...,"Al-Zr",...]
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

    # rearrange Materials project database entries into dictionary
    dfim = pd.read_excel("intermetallics_zhaohan.xlsx")
    # dfim.set_index("Unnamed:0", inplace=True)
    im = {}
    for index, row in dfim.iterrows():
        if row["comptype"] not in im:
            im[row["comptype"]] = [(row["comp"], row["Hf"])]
        else:
            im[row["comptype"]].append((row["comp"], row["Hf"]))
    df_3 = pd.read_excel('3z.xlsx')
    df_3.reset_index()
    for index, row in dfca.iterrows():
        df_pd = pd.DataFrame()
        # quaternary
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
        # query intermetallic from the materials project
        el = {e1, e2, e3, e4}
        df_in = pd.DataFrame()
        cnt = 0
        templist = []
        for pair in binary():
            p = pair.replace("-", "")
            if p in im:
                for item in im[p]:
                    df_in.at[cnt, "comp"] = item[0]
                    df_in.at[cnt, "Hf"] = item[1]
                    df_in.at[cnt, "S"] = 0
                    cnt += 1
                templist.append(p)
        for pair in ternary():
            p = pair.replace("-", "")
            if p in im:
                for item in im[p]:
                    df_in.at[cnt, "comp"] = item[0]
                    df_in.at[cnt, "Hf"] = item[1]
                    df_in.at[cnt, "S"] = 0
                    cnt += 1
                templist.append(p)
        df_final = pd.concat([df_pd, df_in], ignore_index=True)
        comps = df_final['comp']
        # print(df_final.head())
        # build phase diagram
        def phasecheck(t):
            Ef = df_final['Hf'] - t * df_final['S']
            mg_comp = [None] * len(comps)
            for i in range(len(comps)):
                mg_comp[i] = Composition(comps[i])
                entries3 = [None] * len(mg_comp)
            for i in range(len(mg_comp)):
                entries3[i] = PDEntry(composition=mg_comp[i], energy=Ef[i] * mg_comp[i].num_atoms)
            entries3.append(PDEntry(composition=Composition("NbV2"), energy=-.059*Composition("NbV2").num_atoms))
            phase = PhaseDiagram(entries3)
            # test = PDEntry(composition=mg_comp[0], energy=Ef[0] * mg_comp[0].num_atoms)
            test = entries3[0]
            return float(phase.get_e_above_hull(test))

        for temp in range(0, 2050, 50):
            ehull = phasecheck(temp)
            if ehull < 1e-5: # cutoff for minimum rounding error
                x.append(dfca.at[index, "i"])
                y.append(dfca.at[index, "j"])
                z.append(dfca.at[index, "k"])
                w.append(dfca.at[index, "l"])
                c.append(temp)
                dfca.at[index, "temp"] = temp
                break
    dfca.to_excel(str(comp) + ".xlsx")
    np.save("x", x)
    np.save("y", y)
    np.save("z", z)
    np.save("w", w)
    np.save("c", c)
    x = np.load("x.npy")
    y = np.load("y.npy")
    z = np.load("z.npy")
    w = np.load("w.npy")
    c = np.load("c.npy")

    # plot

    # Create initial scatter plot
    fig = go.FigureWidget(data=go.Scatter3d(
        x=x[w == 0],
        y=y[w == 0],
        z=z[w == 0],
        mode='markers',
        marker=dict(
            size=5,
            color=c[w == 0],
            colorscale='Viridis',
            opacity=0.8,
            showscale=True,
            colorbar=dict(
                title='Temperature of Stability',
            ),
        ),
        hovertemplate='x: %{x}<br>y: %{y}<br>z: %{z}<br>Temperature of Stability: %{marker.color:.2f}<extra></extra>'
    ))

    # Define update function
    def update_plot(value):
        fixed_dimension = int(value)
        x_values = x[w == fixed_dimension]
        y_values = y[w == fixed_dimension]
        z_values = z[w == fixed_dimension]
        color_values = c[w == fixed_dimension]

        with fig.batch_update():
            fig.data[0].x = x_values
            fig.data[0].y = y_values
            fig.data[0].z = z_values
            fig.data[0].marker.color = color_values

    # Create the slider widget
    slider = widgets.FloatSlider(min=0, max=1, step=0.1, value=0)

    # Observe the slider value and update the plot
    slider.observe(lambda change: update_plot(change.new), names='value')

    # Display the slider and the plot
    display(slider)
    display(fig)

    # Update the plot initially
    update_plot(slider.value)


run(["Nb", "V", "Zr", "Ti"])
