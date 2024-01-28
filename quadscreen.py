import numpy as np
import pandas as pd
import xlsxwriter

# to use with zhaohan's binaries
def quad():
    elamount = 17
    sheet = pd.read_excel('RHEAs_phase_prediction-main/enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx',
                          sheet_name="our work",
                          index_col=0,
                          nrows=elamount + 1)
    wb = xlsxwriter.Workbook('RHEAs_phase_prediction-main/4z.xlsx',
                             {'strings_to_numbers': True})
    s1 = wb.add_worksheet('Sheet 1')
    s1.write(0, 0, "comp")
    for i in range(4):
        s1.write(0, i + 1, "e" + str(i + 1))
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
                    s1.write(cnt, 5, sm / 4)
                    s1.write(cnt, 6, 0.000119)
                    cnt += 1

    wb.close()

def tri():
    elamount = 17
    sheet = pd.read_excel('RHEAs_phase_prediction-main/enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx',
                          sheet_name="our work",
                          index_col=0,
                          nrows=elamount + 1)
    wb = xlsxwriter.Workbook('RHEAs_phase_prediction-main/3z.xlsx',
                             {'strings_to_numbers': True})
    s1 = wb.add_worksheet('Sheet 1')
    s1.write(0, 0, "comp")
    for i in range(3):
        s1.write(0, i + 1, "e" + str(i + 1))
    s1.write(0, 4, "enthalpy")
    s1.write(0, 5, "entropy")
    cnt = 1
    for e1 in range(elamount):
        a = sheet.columns.values[e1]
        for e2 in range(e1 + 1, elamount):
            b = sheet.columns.values[e2]
            for e3 in range(e2 + 1, elamount):
                c = sheet.columns.values[e3]
                s1.write(cnt, 1, a)
                s1.write(cnt, 2, b)
                s1.write(cnt, 3, c)
                s1.write(cnt, 0, str(a + b + c))
                sm = 0
                var = [e1, e2, e3]
                for i in range(3):
                    for j in range(i + 1, 3):
                        add = sheet.iloc[var[j], var[i]]
                        sm += float(add)
                s1.write(cnt, 4, sm/9*4)
                s1.write(cnt, 5, 0.0000947)
                cnt += 1

    wb.close()

def bi():
    elamount = 17
    sheet = pd.read_excel('RHEAs_phase_prediction-main/enthalpy_data_and_predictions/pairwise_mixing_enthalpy.xlsx',
                          sheet_name="our work",
                          index_col=0,
                          nrows=elamount + 1)
    wb = xlsxwriter.Workbook('RHEAs_phase_prediction-main/2z.xlsx',
                             {'strings_to_numbers': True})
    s1 = wb.add_worksheet('Sheet 1')
    s1.write(0, 0, "comp")
    for i in range(2):
        s1.write(0, i + 1, "e" + str(i + 1))
    s1.write(0, 3, "enthalpy")
    s1.write(0, 4, "entropy")
    cnt = 1
    for e1 in range(elamount):
        a = sheet.columns.values[e1]
        for e2 in range(e1 + 1, elamount):
            b = sheet.columns.values[e2]
            s1.write(cnt, 1, a)
            s1.write(cnt, 2, b)
            s1.write(cnt, 0, str(a + b))
            sm = 0
            var = [e1, e2]
            for i in range(2):
                for j in range(i + 1, 2):
                    add = sheet.iloc[var[j], var[i]]
                    sm += float(add)
            s1.write(cnt, 3, sm)
            s1.write(cnt, 4, 0.0000597)
            cnt += 1

    wb.close()

tri()