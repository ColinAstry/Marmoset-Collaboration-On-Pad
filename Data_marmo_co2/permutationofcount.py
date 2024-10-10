import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.anova import AnovaRM
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the data from the Excel file
import scipy.stats as stats

df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\2024-05-26_butcounts.xlsx')

# Convert the 'ID' and 'experiment' columns to categories
df['ID'] = df['id'].astype('category')
df['Date'] = df['date'].astype('category')

# Number of times to sample
num_samples = 1000

# Get the unique IDs
ids = df['ID'].unique()

# Initialize a dictionary to store the confidence intervals for each ID
conf_ints = {}

# # For each ID, randomly select an 'average2' value num_samples times and calculate the confidence interval
# for id in ids:
#     means = []
#     for _ in range(num_samples):
#         sample = df.loc[df['ID'] == id, 'average2'].sample(n=len(df.loc[df['ID'] == id, 'average2']), replace=True)
#         means.append(sample.mean())
#     conf_int_low = np.percentile(means, 2.5)
#     conf_int_high = np.percentile(means, 97.5)
#     conf_ints[id] = (conf_int_low, conf_int_high)
#     print(f'Bootstrap confidence interval for mean of ID {id}: ({conf_int_low}, {conf_int_high})')

import scipy.stats as stats

# For each ID, calculate the mean and standard deviation of 'average2' and use them to calculate the confidence interval
for id in ids:
    data = df.loc[df['ID'] == id, 'average2']
    mean = data.mean()
    std_dev = data.std()
    conf_int_low = mean - (1.96 * std_dev / np.sqrt(len(data)))
    conf_int_high = mean + (1.96 * std_dev / np.sqrt(len(data)))
    conf_ints[id] = (conf_int_low, conf_int_high)
    print(f'Confidence interval for mean of ID {id}: ({conf_int_low}, {conf_int_high})')

# Add a new column to the dataframe indicating whether each day's 'average2' value is within the confidence interval for its ID
df['in_conf_int'] = df.apply(lambda row: conf_ints[row['ID']][0] <= row['average2'] <= conf_ints[row['ID']][1], axis=1)

# # Select only the columns of interest
# df_interest = df[['Date', 'ID', 'average2', 'in_conf_int']]

# # Print the dataframe
# print(df_interest)

#画图plot the average counts out
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming df is your DataFrame and it's already prepared

# Get the unique IDs
ids = df['ID'].unique()

# Convert 'Date' to string to treat it as a category
df['Date'] = df['Date'].astype(str)

# Get all unique dates
all_dates = df['Date'].unique()

# # Define the width of the bars and the colors for the bars
# width = 0.2
# colors = {'correct': 'skyblue', 'wrong': 'salmon', 'total': 'lightgreen', 'outside': 'black', 'sum': 'gray'}

# # Plot the counts for each category normalized by 'max_t0'
# categories = ['wrong', 'correct', 'outside', 'total']
# fig, axs = plt.subplots(len(ids), 1, figsize=(10, 8))

# for i, id in enumerate(ids):
#     ind = np.arange(len(all_dates))  # the x locations for the groups

#     # Create a new DataFrame with all dates and fill missing values with 0
#     df_id = pd.DataFrame(all_dates, columns=['Date']).merge(df.loc[df['ID'] == id], on='Date', how='left')
#     for category in categories:
#         if df_id[category].dtype.name == 'category':
#             df_id[category] = df_id[category].cat.add_categories([0])
#         df_id[category] = df_id[category].fillna(0)
#         df_id[category] = df_id[category] / df_id['max_t0'] * 3600

#     # Plot the bars in the order of 'wrong', 'correct', 'total', 'outside'
#     for j, category in enumerate(['wrong', 'correct', 'total', 'outside']):
#         axs[i].bar(ind - 1.5*width + j*width, df_id[category], width, label=category, color=colors[category])
    
#     # Add a new bar for the sum of 'wrong', 'correct', and 'outside'
#     df_id['sum'] = df_id['wrong'] + df_id['correct'] + df_id['outside']
#     axs[i].bar(ind + 0.5*width, df_id['sum'], width, label='total-blank', color=colors['sum'])

#     #plot ci for each id as yellow dashed line
#     if id in conf_ints:
#         axs[i].axhline(y=conf_ints[id][0], color='yellow', linestyle='--',label = "95% CI (lower)")
#         axs[i].axhline(y=conf_ints[id][1], color='yellow', linestyle='--')


#     axs[i].set_xticks(ind)
#     axs[i].set_xticklabels(all_dates, rotation=45)
#     axs[i].legend()
#     axs[i].set_title(f'ID {id}')

# #add gray dashed vertical line between date 321 and 327, 416 and 417, 505 and 508
# for ax in axs:
#     ax.axvline(x=5.5, color='gray', linestyle='--',label = "experiment change")
#     ax.axvline(x=12.5, color='gray', linestyle='--')
#     ax.axvline(x=20.5, color='gray', linestyle='--')


# # Set the y-axis limits
# axs[0].set_ylim(0, 450)
# axs[1].set_ylim(0, 450)
# plt.xlabel('Date')
# plt.tight_layout()
# # Save the plot as an image
# fig.savefig(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\528_butcounts.png')
# plt.show()


#只画sum
# Define the width of the bars and the colors for the bars
width = 0.6
colors = {'correct': 'skyblue', 'wrong': 'salmon', 'total': 'lightgreen', 'outside': 'black', 'sum': 'skyblue'}

# Plot the counts for each category normalized by 'max_t0'
categories = ['wrong', 'correct', 'outside', 'total']
fig, axs = plt.subplots(len(ids), 1, figsize=(10, 8))

for i, id in enumerate(ids):
    ind = np.arange(len(all_dates))  # the x locations for the groups

    # Create a new DataFrame with all dates and fill missing values with 0
    df_id = pd.DataFrame(all_dates, columns=['Date']).merge(df.loc[df['ID'] == id], on='Date', how='left')
    for category in categories:
        if df_id[category].dtype.name == 'category':
            df_id[category] = df_id[category].cat.add_categories([0])
        df_id[category] = df_id[category].fillna(0)
        df_id[category] = df_id[category] / df_id['max_t0'] * 3600
    
    # Add a new bar for the sum of 'wrong', 'correct', and 'outside'
    df_id['sum'] = df_id['wrong'] + df_id['correct'] + df_id['outside']
    axs[i].bar(ind, df_id['sum'], width, label='sum', color=colors['sum'])

    #plot ci for each id as yellow dashed line
    if id in conf_ints:
        axs[i].axhline(y=conf_ints[id][0], color='yellow', linestyle='--',label = "95% CI (lower)")
        axs[i].axhline(y=conf_ints[id][1], color='yellow', linestyle='--')


    axs[i].set_xticks(ind)
    axs[i].set_xticklabels(all_dates, rotation=45)
    axs[i].legend()
    axs[i].set_title(f'ID {id}')

#add gray dashed vertical line between date 321 and 327, 416 and 417, 505 and 508
for ax in axs:
    ax.axvline(x=5.5, color='gray', linestyle='--',label = "experiment change")
    ax.axvline(x=12.5, color='gray', linestyle='--')
    ax.axvline(x=20.5, color='gray', linestyle='--')


# Set the y-axis limits
axs[0].set_ylim(0, 450)
axs[1].set_ylim(0, 450)
plt.xlabel('Date')
plt.tight_layout()
# Save the plot as an image
fig.savefig(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\concise0\analysis\605_butcounts.png')
plt.show()