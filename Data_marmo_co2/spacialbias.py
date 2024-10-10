import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency

# Load the Excel file
df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\723.xlsx')

# Convert the date column to integer
df['date'] = df['Date'].astype(int)

# Select rows where the date is within the range [316, 416]
df = df[df['date'].between(402.5,508.5)]
# select rows button is correct
#df = df[df['button'] == 'correct']

# Extract the touch coordinates
x = df['location_x']
y = df['location_y']

# Create new columns for the binned coordinates
df['x_bin'] = pd.cut(x, bins=[0, 340, 680, np.inf], labels=['0-340', '340-680', '680+'])
df['y_bin'] = pd.cut(y, bins=[0, 200, 400, np.inf], labels=['0-200', '200-400', '400+'])

# Calculate the frequency of touches in each bin
frequency = pd.crosstab(df['x_bin'], df['y_bin'])
observed = frequency.values

# perform chi-square test
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(observed)

print("chi2 statistic", chi2)
print("p-value", p)
print("degrees of freedom", dof)
print("expected counts", expected)

# # Plot the frequencies as a heatmap
# plt.figure(figsize=(10, 8))
# sns.heatmap(frequency, annot=True, cmap='YlGnBu', fmt='d')
# plt.title('Touch Frequencies Heatmap')
# #save the heatmap
# plt.savefig(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\723allheatmap.png')
# plt.show()