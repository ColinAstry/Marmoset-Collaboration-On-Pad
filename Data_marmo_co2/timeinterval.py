import pandas as pd
import os
from openpyxl import load_workbook

# Define the directory containing the Excel files
dir_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure1'

# Create a new subdirectory named "concise"
os.makedirs(os.path.join(dir_path, 'ti'), exist_ok=True)

# Loop through all the Excel files in the directory
for filename in os.listdir(dir_path):
    if (filename.endswith('.xlsx') or filename.endswith('.xls')) and not filename.startswith('~'):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(os.path.join(dir_path, filename))

        #t1 = t0.shift(-1) - t0
        df['t1'] = df['t0'].shift(-1) - df['t0']

        # Save the modified DataFrame back to the Excel file
        df.to_excel(os.path.join(dir_path, 'ti', filename), index=False)
    else:
        print(f"Skipping file {filename} as it does not have a recognized Excel extension.")

    