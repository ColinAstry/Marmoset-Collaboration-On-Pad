import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from openpyxl import load_workbook

# Define the directory containing the Excel files
dir_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure0'

# Initialize an empty DataFrame to store the 'yd' columns
df_yd = pd.DataFrame()

# Loop through all the files
for filename in os.listdir(dir_path):
    if '.xlsx' in filename and not filename.startswith('~'):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(os.path.join(dir_path, filename))

        # Calculate yd
        df['yd'] = df['location_y'].shift(-1) - df['location_y']

        # Append the 'yd' column to the df_yd DataFrame
        df_yd = pd.concat([df_yd, df['yd']], ignore_index=True)

# Print the total number of yd values
print('Total number of yd values:', len(df_yd))

# Calculate the logarithm of the 'yd' values
df_yd_log = np.log(df_yd)

# Plot the histogram of log(yd)
df_yd_log.hist(bins=100)
plt.title('Distribution of log(vertical distance)')
plt.xlabel('log(y-axis distance) (pixel)')
plt.ylabel('Frequency')

# Save the plot under the same directory
plt.savefig(os.path.join(dir_path, 'log_yd_distribution.png'))

# Display the plot
plt.show()

# Initialize an empty DataFrame to store the 't1' columns
df_t1 = pd.DataFrame()

# Loop through all the files
for filename in os.listdir(dir_path):
    if '.xlsx' in filename and not filename.startswith('~'):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(os.path.join(dir_path, filename))

        # Calculate t1
        df['t1'] = df['t0'].shift(-1) - df['t0']

        # Append the 't1' column to the df_t1 DataFrame
        df_t1 = pd.concat([df_t1, df['t1']], ignore_index=True)

# Print the total number of t1 values
print('Total number of t1 values:', len(df_t1))

# Plot the histogram of t1
df_t1.hist(bins=100, range=(0, 5))
plt.title('Distribution of time interval')
plt.xlabel('time interval (s)')
plt.ylabel('Frequency')
#save the plot under the same directory
plt.savefig(os.path.join(dir_path, 'ti_distribution.png'))
plt.show()