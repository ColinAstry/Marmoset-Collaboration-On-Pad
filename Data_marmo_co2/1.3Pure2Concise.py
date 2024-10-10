import pandas as pd
import os
from openpyxl import load_workbook

#将纯净数据转换为简洁数据（剔除连续重复的行）

# Define the directory containing the Excel files
dir_path = r'D:\Research\MarmoCo2\Data\ToFilter\precl\Pure'

# Create a new subdirectory named "concise"
os.makedirs(os.path.join(dir_path, 'concise'), exist_ok=True)

# Loop through all the Excel files in the directory
for filename in os.listdir(dir_path):
    if (filename.endswith('.xlsx') or filename.endswith('.xls')) and not filename.startswith('~'):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(os.path.join(dir_path, filename))

        original_rows_count = len(df)
        # Create a boolean mask where True indicates the row has 'location_x' or 'location_y' within 0.1 of the previous row's value,
        # or 'finger' is 2, and 'button' is either "blank" or "outside"
        mask = (((df['location_x'].shift(1) - df['location_x']).abs() <= 10) | 
            ((df['location_y'].shift(1) - df['location_y']).abs() <= 10) | 
            ((df['t0'].shift(1) - df['t0']).abs() <= 0.3)) & df['button'].isin(['blank', 'outside'])

        # Use the mask to drop the rows from the DataFrame
        df = df.loc[~mask]

        new_rows_count = len(df)

        # Save the modified DataFrame back to the Excel file
        df.to_excel(os.path.join(dir_path, 'concise', filename), index=False)
    else:
        print(f"Skipping file {filename} as it does not have a recognized Excel extension.")
