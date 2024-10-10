import matplotlib.pyplot as plt
import pandas as pd
import os
from openpyxl import load_workbook

# Define the directory containing the Excel files
dir_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure1\ti'
import matplotlib.pyplot as plt

# Initialize an empty DataFrame to store the 't1' columns
df_t1 = pd.DataFrame()

# Loop through all the files
for filename in os.listdir(dir_path):
    if '.723.xlsx' in filename and not filename.startswith('~'):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(os.path.join(dir_path, filename))

        # Calculate t1
        df['t1'] = (df['t0'].shift(-1) - df['t0'])*1000

        # Append the 't1' column to the df_t1 DataFrame
        df_t1 = pd.concat([df_t1, df['t1']], ignore_index=True)

# Print the total number of t1 values
print('Total number of t1 values:', len(df_t1))

# Plot the histogram of t1
df_t1.hist(bins=100, range=(0, 5000))
plt.title('Distribution of time interval for 723')
plt.xlabel('t1')
plt.ylabel('Frequency')
plt.show()