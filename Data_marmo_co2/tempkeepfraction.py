import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.anova import AnovaRM
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the Excel file
file_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\2024-05-26_butcounts.xlsx'
df = pd.read_excel(file_path)

grouped = df.groupby('id')
filteredtouch = grouped['total'].sum()
orignialtouch = grouped['totalp'].sum()
fraction = grouped['total'].sum() / grouped['totalp'].sum()

import os

# Assuming filteredtouch, orignialtouch, and fraction are defined above this
print(filteredtouch)
print(orignialtouch)
print(fraction)

# Get the directory of the Excel file
dir_path = os.path.dirname(os.path.realpath(file_path))

# Create the result file in the same directory
with open(os.path.join(dir_path, 'results.txt'), 'w') as f:
    f.write(f'filteredtouch: {filteredtouch}\n')
    f.write(f'orignialtouch: {orignialtouch}\n')
    f.write(f'fraction: {fraction}\n')

