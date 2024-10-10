import pandas as pd
import os
import sys

dir_path = sys.argv[1]  # replace with your actual folder path
def convert_csv_to_xlsx(dir_path):
    # Loop through each file in the directory
    for filename in os.listdir(dir_path):
        if filename.endswith('.csv'):
            # Read the CSV data into a DataFrame without a header
            df = pd.read_csv(os.path.join(dir_path, filename), header=None)

            # Transpose the DataFrame
            df_transposed = df.transpose()

            # # Append the four new columns
            # df_transposed['times'] = df_transposed['time'] / 1000
            # df_transposed['timem'] = df_transposed['time'] / 60000
            # df_transposed['t0'] = ""
            # df_transposed['note'] = ""

            # Save the transposed DataFrame to an Excel file without column names
            df_transposed.to_excel(os.path.join(dir_path, f'{os.path.splitext(filename)[0]}.xlsx'), index=False, header=False)

convert_csv_to_xlsx(dir_path)
