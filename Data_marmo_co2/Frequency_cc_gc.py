import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import scipy.stats as stats

dir_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\granger\analysis'
max_t0_dict = {}

# Create the output directory if it doesn't exist
output_dir = os.path.join(dir_path)
os.makedirs(output_dir, exist_ok=True)

# First pass: calculate the maximum t0 for each date without considering 'exp' rows
for filename in os.listdir(dir_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{3}', filename).group()
        df = pd.read_excel(os.path.join(dir_path, filename))
        df_filtered = df[(df['note'] != 'exp') & (df['experiment'] != 'test2')]
        max_t0 = df_filtered['t0'].max()
        if date in max_t0_dict:
            max_t0_dict[date] = max(max_t0_dict[date], max_t0)
        else:
            max_t0_dict[date] = max_t0

# Print the max t0 for each date
for date, max_t0 in max_t0_dict.items():
    print(f"Max t0 for {date}: {max_t0}")

# Initialize a dictionary to store all frequencies
all_frequencies = defaultdict(list)

bin_width = 1  

# Second pass: calculate the frequencies for each date
for filename in os.listdir(dir_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{3}', filename).group()
        df = pd.read_excel(os.path.join(dir_path, filename))
        df_filtered = df[(df['note'] != 'exp') & (df['experiment'] != 'test2')]# filter out rows with 'exp' in 'note' column
        frequency, _ = np.histogram(df_filtered['t0'], bins=np.arange(0, max_t0_dict[date] + bin_width, bin_width))
        all_frequencies[date].append(frequency)

# # Get the times of all experiment changes
# change_times = df_filtered.loc[df_filtered['experiment'].shift() != df_filtered['experiment'], 't0'].values
# # Neglect the first change
# change_times = change_times[1:]
# # Convert the change times to minutes if necessary
# change_times_in_minutes = change_times / 60  # Remove this line if the change times are already in minutes

# # Plot the frequencies for each date
# # Define the labels and colors
# labels = ['723', '772']
# colors = [(255/255, 140/255, 0/255), (70/255, 130/255, 180/255)]

# for date, frequencies in all_frequencies.items():
#     plt.figure(figsize=(10, 5))
#     for i, frequency in enumerate(frequencies):
#         bins = np.arange(0, max_t0_dict[date] + bin_width, bin_width)
#         bin_midpoints = bins[:-1] + np.diff(bins)/2  # Calculate the mid-point of each bin
#         bin_midpoints_in_minutes = bin_midpoints / 60  # Convert to minutes
#         plt.plot(bin_midpoints_in_minutes, frequency, label=labels[i], color=colors[i])  # Use the mid-point of each bin as x-values
    
#     # Add a vertical line at each time when the experiment changes
#     for change_time_in_minutes in change_times_in_minutes:
#         plt.axvline(x=change_time_in_minutes, color='r', linestyle='--')

#     plt.xlabel('time (minutes)')
#     plt.ylabel('Frequency')
#     plt.title(f'Frequency of touches')
#     plt.xticks(rotation=90)
#     plt.legend()
#     plt.tight_layout()
#     #save the plot
#     plt.savefig(os.path.join(output_dir, f'frequency_{date}.png'))

# plt.show()

# #理论上计算互相关函数并检验显著性
# # Calculate cross-correlation for each date
# for date, frequencies in all_frequencies.items():
#     if len(frequencies) >= 2:
#         # Calculate cross-correlation
#         cross_correlation = np.correlate(frequencies[0], frequencies[1], mode='full')

#         # Normalize cross-correlation
#         norm_factor = np.sqrt(np.sum(frequencies[0]**2) * np.sum(frequencies[1]**2))
#         cross_correlation = cross_correlation / norm_factor

#         # Calculate the lag at which the cross-correlation is maximum
#         lag = cross_correlation.argmax() - (len(frequencies[0]) - 1)

#         # Test if the cross-correlation is significant
#         # Null hypothesis: the sequences are uncorrelated
#         # We will use the Fisher transformation to convert the correlation coefficient to a z-score
#         max_corr = cross_correlation.max()
        
#         # Check if max_corr is within the valid range for np.arctanh
#         if not -1 <= max_corr <= 1:
#             print(f"Warning: max_corr = {max_corr} is outside the valid range for np.arctanh")
        
#         z = np.arctanh(max_corr)
#         p = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed p-value

#         print(f"Date: {date}")
#         print(f"Cross-correlation: {max_corr}")
#         print(f"Lag: {lag}")
#         print(f"P-value: {p}")

#         # Plot the cross-correlation
#         plt.figure(figsize=(10, 5))
#         lags = np.arange(-len(frequencies[0]) + 1, len(frequencies[0]))
#         plt.plot(lags, cross_correlation)
#         plt.xlabel('Lag')
#         plt.ylabel('Cross-correlation')
#         plt.title(f'Cross-correlation for date {date}')
#         plt.show()

# #最大点的皮尔逊相关检验
# from scipy import stats

# # Find the lag where the cross-correlation is the largest
# lag_max_corr = np.argmax(cross_correlation)

# # Shift one of your sequences by this lag
# shifted_freq = np.roll(frequencies[0], lag_max_corr)

# # Compute the Pearson correlation
# pearson_corr, _ = stats.pearsonr(shifted_freq, frequencies[1])

# # Perform a hypothesis test
# p_value = stats.pearsonr(shifted_freq, frequencies[1])[1]

# print(f"Pearson correlation: {pearson_corr}")
# print(f"P-value: {p_value}")    


#格兰杰因果检验

#check if the data is stationary
from statsmodels.tsa.stattools import adfuller

# Perform the ADF test on the first frequency
frequencies = all_frequencies[date]  # Define the variable "frequencies"
# result1 = adfuller(frequencies[0])
# print(f'ADF Statistic for first frequency: {result1[0]}')
# print(f'p-value: {result1[1]}')
# print(f'Number of lags used: {result1[2]}')
# print(f'Number of observations: {result1[3]}')

# # Perform the ADF test on the second frequency
# result2 = adfuller(frequencies[1])
# print(f'ADF Statistic for second frequency: {result2[0]}')
# print(f'p-value: {result2[1]}')
# print(f'Number of lags used: {result2[2]}')
# print(f'Number of observations: {result2[3]}')

from statsmodels.tsa.stattools import grangercausalitytests

# Define the maximum number of lags that you want to test
maxlag = 16

# Stack your two frequencies into a 2D array
data = np.vstack([frequencies[0], frequencies[1]]).T

# import sys

# # Perform the Granger causality test in the original direction (X predicting Y)
# results_X_predicts_Y = grangercausalitytests(data, maxlag)

# # Perform the Granger causality test in the reverse direction (Y predicting X)
# # Swap the order of the variables in the input data
data_reversed = data[:, ::-1]
# results_Y_predicts_X = grangercausalitytests(data_reversed, maxlag)

# import contextlib

# # Create the 'excels' subfolder if it doesn't exist
# if not os.path.exists(os.path.join(dir_path, 'excels')):
#     os.makedirs(os.path.join(dir_path, 'excels'))

# # Create the path for the output file
# output_file_path = os.path.join(dir_path, 'excels', 'granger_results.xlsx')

# # Create the path for the output file
# output_file_path = os.path.join(dir_path, 'excels', 'granger_results.xlsx')

# import pandas as pd

# # Prepare lists to store the results
# lags = []
# F_values_X_predicts_Y = []
# p_values_X_predicts_Y = []
# F_values_Y_predicts_X = []
# p_values_Y_predicts_X = []
# df_X_predicts_Y = []
# df_Y_predicts_X = []

# # Extract the F statistic, p-value and degree of freedom of the ssr_ftest
# for i in range(1, maxlag + 1):
#     lags.append(i)
#     F_values_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][0])
#     p_values_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][1])
#     df_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][2])  # degree of freedom
#     F_values_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][0])
#     p_values_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][1])
#     df_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][2])  # degree of freedom

# # Create a DataFrame
# df = pd.DataFrame({
#     '滞后': lags,
#     'X 预测 Y - F 统计量': F_values_X_predicts_Y,
#     'X 预测 Y - p值': p_values_X_predicts_Y,
#     'X 预测 Y - 自由度': df_X_predicts_Y,  # degree of freedom
#     'Y 预测 X - F 统计量': F_values_Y_predicts_X,
#     'Y 预测 X - p值': p_values_Y_predicts_X,
#     'Y 预测 X - 自由度': df_Y_predicts_X,  # degree of freedom
# })

# # Save the DataFrame as an Excel file
# df.to_excel(output_file_path, index=False)

######检查序列是不是对的
# import numpy as np

# # Save the data array to a CSV file
# np.savetxt("data.csv", data, delimiter=",")

# # Save the reversed data array to a CSV file
# np.savetxt("data_reversed.csv", data_reversed, delimiter=",")