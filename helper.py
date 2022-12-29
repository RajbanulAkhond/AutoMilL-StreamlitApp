import os
import numpy as np
import pandas as pd


def extract(uploaded_files):
    # FULLY AUTOMATED FILE SELECTION
    data1_start_row = 4
    data1_cols = [0, 13, 22, 25, 27, 31, 33, 35, 37, 40, 42, 44]
    data2_cols = [3, 5, 7, 9, 13, 15, 20, 23, 26, 29, 32, 34, 36, 38, 41]
    cols_name = ['HeatNo','Scrap','Steel','Energy',	'Power','P_on',	'P_off','TaptoTap','Delay','Temp','C','O','T_O2','T_NG','RCB_O2_Lc','RCB_O2_Bur','RCB_NG','PCC_NG','FB_NG','FB_O2','O2_Top_Lc','Alloy','Slag','F_Carbon','F_Lime','F_Dolo','Inj_Carbon']
    # Initialize empty numpy arrays to store the data
    data1 = np.empty((0, len(data1_cols)))
    data2 = np.empty((0, len(data2_cols)))
    # Loop through all files
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file)

        cmp_range = df.iloc[:100, 0]
        idx = cmp_range.index[cmp_range == 'GENERAL'].tolist()[-1] if 'GENERAL' in cmp_range.values else len(cmp_range)

        data_in_file = idx - 10
        data1_end_row = idx - 4
        data2_start_row = data1_end_row + 7
        data2_end_row = data2_start_row + data_in_file + 2

        # Append the selected rows to the data1 and data2 arrays
        data1 = np.concatenate((data1, df.iloc[data1_start_row:data1_end_row, data1_cols].values))
        data2 = np.concatenate((data2, df.iloc[data2_start_row:data2_end_row, data2_cols].values))

    # Concatenate the data1 and data2 arrays to create the raw_data array
    raw_data = np.concatenate((data1, data2),axis=1)
    raw_data = pd.DataFrame(raw_data)
    raw_data.columns = cols_name

    return raw_data


def clean(raw_data):
    # Remove the HeatNo column
    raw_data.drop(columns=['HeatNo'], inplace=True)
    # Fill in missing values using interpolation
    clean_data = raw_data.interpolate()

    return clean_data

# Utility functions
