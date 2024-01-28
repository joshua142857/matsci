import matplotlib.pyplot as plt
# plt.style.use('classic')
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go


def bar():
    # Load the dataset
    df_1 = pd.read_excel("3CuRutsetfcc.xlsx")
    df_2 = pd.read_excel("3CuRutsetbcc.xlsx")

    # Prepare the data
    x = df_1["comp"]
    y1 = df_1["ehull"]
    y2 = df_2["ehull"]

    # Create the bar graph
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y1, name='FCC'))
    fig.add_trace(go.Bar(x=x, y=y2, name='BCC'))

    # Set the layout
    fig.update_layout(title='Cu-Ru-X Ternaries at 1000K', xaxis_title='Composition', yaxis_title='E_hull (eV)')

    # Display the graph
    fig.show()


def heatmap(structure):
# x = np.linspace(0, 10, 500)
# y = np.cumsum(rng.randn(500, 6), 0)
    data = pd.read_excel("CuAgZnfcc.xlsx", usecols="B,K:U", index_col="comp")
# data = pd.read_excel("metastablepairs-" + structure.lower() + ".xlsx", sheet_name="1000K", index_col=0)
# data = pd.read_excel("enthalpy_data_and_predictions/bokas.xlsx", sheet_name=structure, index_col=0)
    print(data)
    sns.set()
#
# els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
#        'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
#        'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd']
    sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)
# sns.heatmap(data, square=True, vmax=700, vmin=0)
# plt.title('Metastable Binary Pairs for Quaternary HEA ' + structure + ' at 1000K')
# sns.heatmap(data, square=True, cmap="coolwarm", vmax=1, vmin=-1)
# plt.title("Binary Enthalpies for " + structure)
    sns.heatmap(data, square=True, cmap="coolwarm")
    plt.title(structure + "Ternary Phase Diagram for CuAgZn")
    plt.show()

# heatmap("FCC")

def violinAllAlloys(structure):
    df_in = pd.DataFrame()
    df_2 = pd.read_excel('datasheets/2-' + structure.lower() + '.xlsx')
    df_3 = pd.read_excel('datasheets/3-' + structure.lower() + '.xlsx')
    df_4 = pd.read_excel('datasheets/4-' + structure.lower() + '.xlsx')
    df_5 = pd.read_excel('datasheets/5-' + structure.lower() + '.xlsx')

    df_in["size"] = df_5["e_hull"]
    df_in["Binary"] = df_2["e_hull"]
    df_in["Ternary"] = df_3["e_hull"]
    df_in["Quaternary"] = df_4["e_hull"]
    df_in["Quinary"] = df_5["e_hull"]
    # print(df_in)
    sns.violinplot(df_in[["Binary", "Ternary", "Quaternary", "Quinary"]])
    plt.show()


def CuAg_heatmap(add_el, structure):
    data = pd.read_excel("CuAgTernaries/CuAg" + add_el + "_" + structure.lower() + ".xlsx",
                         usecols="B,L:V",
                         index_col="x")
    # data = pd.read_excel("CuAgTernaries/CuAgAuZn.xlsx",
    #                      sheet_name=structure.lower() + temp + "K",
    #                      index_col="x")
    sns.set()
    # sns.light_palette("seagreen", as_cmap=True)
    flipped_data = data.iloc[::-1]
    # heatmap =
    sns.heatmap(flipped_data, square=True, cmap="Blues")
    # heatmap.set_yticklabels(heatmap.get_yticklabels()[::-1])
    # plt.title(structure + " E_hull vs CuAgAu$_{x}$Zn$_{y}$ at " + temp + "K")
    # plt.xlabel("CuAgAu$_{x}$Zn")
    # plt.ylabel("CuAgAuZn$_{y}$")
    plt.title(structure + " E_hull vs CuAg" + add_el + "$_{x}$ at " + "500" + "K")
    plt.xlabel("T (K)")
    plt.ylabel("CuAg" + add_el + "$_{x}$")
    plt.show()

bar()
