import pandas as pd
import matplotlib.pyplot as plt


OERels = ['Pt', 'Ir', 'Rh', 'Pd', 'Au']
els = ['Cu', 'Co', 'Fe', 'Mn', 'Mo', 'Ni', 'Ta', 'Ti', 'Pt', 'Ir', 'Rh', 'Pd', 'Au']
pairs = []
for x in els:
    for y in els:
        if x != y and not pairs.__contains__((y, x)):
            pairs.append((x, y))
structure = "BCC"


def stabilize(t, cnt=-1):
    out = []
    alloySize = len(t[0])
    if alloySize == 2:
        dp = pd.read_excel("3-" + structure.lower() + ".xlsx", sheet_name=structure)
    if alloySize == 3:
        dp = pd.read_excel("4-" + structure.lower() + ".xlsx", sheet_name=structure)
    if alloySize == 4:
        dp = pd.read_excel("5-" + structure.lower() + ".xlsx", sheet_name="1000K")
    for alloy in pairs:
        for index, row in dp.iterrows():
            ehull = row['e_hull']
            if ehull >= 0.015:
                break
            se = ()
            for j in range(alloySize + 1):
                se += (row['e' + str(j + 1)],)
            if inset(se, alloy):
                tu = ()
                for x in se:
                    tu += (x,)
                if not out.__contains__((ehull, tu)):
                    out.append((ehull, tu))
    out.sort()
    if cnt > len(out):
        return out
    else:
        return out[0:cnt]



def inset(set, tuple):
    for a in tuple:
        if a not in set:
            return False
    return True


ternary = []
for unit in stabilize(pairs):
    ternary.append(unit[1])
# print(ternary)

data4 = []
data5 = []
quaternary = []
quinary = []
for unit in stabilize(ternary):
    data4.append(unit[0]*1000)
    quaternary.append(unit[1])
for unit in stabilize(quaternary):
    data5.append(unit[0]*1000)
    quinary.append(unit[1])
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(data4, bins=10)
ax1.set_xlabel('Energy Above Hull (meV)')
ax1.set_ylabel('Frequency')
ax1.set_title('Quaternary Frequencies')
# ax1.set_xticks(range(0, 50, 5))
# ax1.set_yticks(range(0, 20, 5))
ax2.hist(data5, bins=10)
ax2.set_xlabel('Energy Above Hull (meV)')
ax2.set_ylabel('Frequency')
ax2.set_title('Quinary Frequencies')
# ax2.set_xticks(range(0, 50, 5))
# ax2.set_yticks(range(0, 5, 2))

# print(quinary)
o= ""
for a in quinary:
    i = ""
    for b in a:
        i+=b
    o+=i
    o+=", "
print(o)
plt.show()
