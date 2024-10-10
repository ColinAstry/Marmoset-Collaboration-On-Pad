import pandas as pd
import os
import glob

# Specify the directory you want to use
directory = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Concise4'

# Get all Excel files in the directory
excel_files = glob.glob(os.path.join(directory, '*.xlsx'))

for file in excel_files:
    # Load the Excel file
    df = pd.read_excel(file)

    # Add the new column with the value 'hab1'
    df['experiment'] = 'test2'

    # Save the DataFrame back to the Excel file
    df.to_excel(file, index=False)