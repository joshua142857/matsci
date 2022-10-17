import eahull
import pandas as pd
import matplotlib.pyplot as plt
df_out = pd.DataFrame(columns = ["comp","e1","e2","e3","e4","e5"])
structure = "FCC"
elements = ["Cr", "Mn", "Ni", "W", "Pd"]
for i in range(len(elements)):
    elfour = []
    for j in range(len(elements)):
        if j != i:
            elfour.append(elements[j])
            elthree = []
            comp = ""
            for k in range(len(elements)):
                if k != i and k != j:
                    elthree.append(elements[k])
                    comp += elements[k]
                    # df_out["e" + str(k+1)] = elthree[k]
            # df_out["comp"] = comp
            print(elthree)
            print(comp + str(eahull.run3(structure, elthree[0], elthree[1], elthree[2])))
    print(elfour)
    print(eahull.run4(structure, elfour[0], elfour[1], elfour[2], elfour[3]))
print(elements)
print(eahull.run5(structure, elements[0], elements[1], elements[2], elements[3], elements[4]))
#
# data = {'ternary': [1, 2], 'quaternary': 15, 'quinary': 5}
# names = list(data.keys())
# values = list(data.values())
#
# fig, axs = plt.subplots(figsize=(1, 1))
# axs[0].bar(names, values)
# fig.suptitle('Categorical Plotting')
#
# print(eahull.run5("BCC", "Al", "Cu","Ni","W","Pt"))
# print(run3("BCC", "Co", "Cr","Mn"))