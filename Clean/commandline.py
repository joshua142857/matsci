import os
from pair import list_to_pairs
els = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Mn', 'Mo',
           'Nb', 'Ni', 'Ta', 'Ti', 'W', 'Zr', 'V', 'Mg', 'Re',
           'Os', 'Rh', 'Ir', 'Pd', 'Pt', 'Ag', 'Au', 'Zn', 'Cd', 'Ru']
for tup in list_to_pairs(els):
    el1, el2 = tup

fcc_rndstr = f"""1 1 1 90 90 90
                .0 .5 .5
                .5 .0 .5
                .5 .5 .0
                .0 .0 .0 {el1}=.5,{el2}=.5"""
bcc_rndstr = f"""1 1 1 90 90 90
                 1 0 0
                 0 1 0
                 0 0 1
                 0 0 0 {el1}=.5, {el2}=.5"""
with open("rndstr.in", "w") as f1:
    f1.write(fcc_rndstr)

# in case sqscell.out is necessary:
fcc_sqscell = """1
                 
                 2 0 0
                 0 2 0
                 0 0 2"""
with open("sqscell.out", "w") as f2:
    f2.write(fcc_sqscell)
os.system("corrdump -l=rndstr.in -ro -noe -nop -clus -2=1.1")
# wait?
# os.system("mcsqs -n 24")

os.system("mcsqs -rc")