import os
import glob
import pandas as pd
from functools import reduce

file_path = r'C:\Research\EpiSearch\original_data\search\Norovirus'

all_files = glob.glob(os.path.join(file_path, "*.xlsx"))

if not all_files:
    print("Not Found")
else:
    df_list = []
    
    for file in all_files:
        try:
            df = pd.read_excel(file)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    merged_df = reduce(lambda left, right: pd.merge(left, right, on='Week', how='outer'), df_list)

    merged_df = merged_df.sort_values(by='Week').reset_index(drop=True)

    output_filename = os.path.join(file_path, 'Norovirus_search.xlsx')

    merged_df.to_excel(output_filename, index=False)