import numpy as np
import pandas as pd
import xlsxwriter
elamount = 17
sheet = pd.read_excel('RHEAs_phase_prediction-main/enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx',
                      sheet_name="our work",
                      index_col=0,
                      usecols='A:S',
                      nrows=elamount+1)

wb = xlsxwriter.Workbook('RHEAs_phase_prediction-main/enthalpy_data_and_predictions/4z.xlsx',
                         {'strings_to_numbers': True})
s1 = wb.add_worksheet('Sheet 1')
s1.write(0, 0, "comp")
for i in range(4):
    s1.write(0, i + 1, "e" + str(i+1))
s1.write(0, 5, "enthalpy")
s1.write(0, 6, "entropy")
cnt = 1
for e1 in range(elamount):
    a = sheet.columns.values[e1]
    for e2 in range(e1 + 1, elamount):
        b = sheet.columns.values[e2]
        for e3 in range(e2 + 1, elamount):
            c = sheet.columns.values[e3]
            for e4 in range(e3 + 1, elamount):
                d = sheet.columns.values[e4]
                s1.write(cnt, 1, a)
                s1.write(cnt, 2, b)
                s1.write(cnt, 3, c)
                s1.write(cnt, 4, d)
                s1.write(cnt, 0, str(a + b + c + d))
                sm = 0
                var = [e1, e2, e3, e4]
                for i in range(4):
                    for j in range(i + 1, 4):
                        add = sheet.iloc[var[j], var[i]]
                        sm += float(add)
                s1.write(cnt, 5, sm/4)
                s1.write(cnt, 6, 0.000119)
                cnt += 1

wb.close()
