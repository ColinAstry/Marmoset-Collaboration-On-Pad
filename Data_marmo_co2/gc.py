import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import scipy.stats as stats

dir_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\granger4\analysis'
max_t0_dict = {}

# Create the output directory if it doesn't exist
output_dir = os.path.join(dir_path)
os.makedirs(output_dir, exist_ok=True)

# First pass: calculate the maximum t0 for each date without considering 'exp' rows
for filename in os.listdir(dir_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{3}', filename).group()
        df = pd.read_excel(os.path.join(dir_path, filename))
        df_filtered = df[df['note'] != 'exp'] 
        #df_filtered = df[(df['note'] != 'exp') & (df['experiment'] != 'test2')]
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
        df_filtered = df[df['note'] != 'exp']
        #df_filtered = df[(df['note'] != 'exp') & (df['experiment'] != 'test2')]# filter out rows with 'exp' in 'note' column
        frequency, _ = np.histogram(df_filtered['t0'], bins=np.arange(0, max_t0_dict[date] + bin_width, bin_width))
        all_frequencies[date].append(frequency)

#########格兰杰因果检验

# #check if the data is stationary
# from statsmodels.tsa.stattools import adfuller

######ADF检验平稳性
# # Perform the ADF test on the first frequency
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
import numpy as np

# Define the maximum number of lags that you want to test
maxlag = 16

# Stack your two frequencies into a 2D array
data = np.vstack([frequencies[0], frequencies[1]]).T
data_reversed = data[:, ::-1]


# #####检查序列是不是对的
# import numpy as np

# # Save the data array to a CSV file
# np.savetxt("data.csv", data, delimiter=",")

# # Save the reversed data array to a CSV file
# np.savetxt("data_reversed.csv", data_reversed, delimiter=",")


# #####显示全部的summary
# from statsmodels.tsa.stattools import grangercausalitytests

# # Open a new text file in write mode
# with open("granger_results_Y_to_X.txt", "w") as file:
#     # Loop over the range from 1 to maxlag
#     for i in range(1, maxlag+1):
#         # Perform the Granger causality test for i lags
#         results_X_predicts_Y = grangercausalitytests(data, i, verbose=False)
#         results_Y_predicts_X = grangercausalitytests(data_reversed, i, verbose=False)

#         # Write the summary for the model where X predicts Y to the file
#         # file.write(f"Number of lags: {i}\n")
#         # file.write("Model where X predicts Y:\n")
#         # file.write(results_X_predicts_Y[i][1][1].summary().as_text())
#         # file.write("\n")

#         # Write the summary for the model where Y predicts X to the file
#         file.write("Model where Y predicts X:\n")
#         file.write(results_Y_predicts_X[i][1][1].summary().as_text())
#         file.write("\n\n")




########################把结果写进excel
# Create the 'excels' subfolder if it doesn't exist
if not os.path.exists(os.path.join(dir_path, 'excels')):
    os.makedirs(os.path.join(dir_path, 'excels'))

# Create the path for the output file
output_file_path = os.path.join(dir_path, 'excels', 'granger_results12345.xlsx')

import pandas as pd

results_X_predicts_Y = grangercausalitytests(data, maxlag, verbose=False)
results_Y_predicts_X = grangercausalitytests(data_reversed, maxlag, verbose=False)

# Prepare lists to store the results
lags = []
F_values_X_predicts_Y = []
p_values_X_predicts_Y = []
F_values_Y_predicts_X = []
p_values_Y_predicts_X = []
df_X_predicts_Y = []
df_Y_predicts_X = []

# Extract the F statistic, p-value and degree of freedom of the ssr_ftest
for i in range(1, maxlag + 1):
    lags.append(i)
    F_values_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][0])
    p_values_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][1])
    df_X_predicts_Y.append(results_X_predicts_Y[i][0]['ssr_ftest'][2])  # degree of freedom
    F_values_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][0])
    p_values_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][1])
    df_Y_predicts_X.append(results_Y_predicts_X[i][0]['ssr_ftest'][2])  # degree of freedom

# Create a DataFrame
df = pd.DataFrame({
    '滞后': lags,
    'X 预测 Y - F 统计量': F_values_X_predicts_Y,
    'X 预测 Y - p值': p_values_X_predicts_Y,
    'X 预测 Y - 自由度': df_X_predicts_Y,  # degree of freedom
    'Y 预测 X - F 统计量': F_values_Y_predicts_X,
    'Y 预测 X - p值': p_values_Y_predicts_X,
    'Y 预测 X - 自由度': df_Y_predicts_X,  # degree of freedom
})

# Save the DataFrame as an Excel file
df.to_excel(output_file_path, index=False)




#######画出频率图
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


# #######用AIC选model

# results_X_predicts_Y = grangercausalitytests(data, maxlag, verbose=False)
# results_Y_predicts_X = grangercausalitytests(data_reversed, maxlag, verbose=False)


# # Get the AIC for each model
# aic_X_predicts_Y = [result[1][1].aic for result in results_X_predicts_Y.values()]
# aic_Y_predicts_X = [result[1][1].aic for result in results_Y_predicts_X.values()]

# # Find the number of lags for the model with the smallest AIC
# best_lag_X_predicts_Y_aic = np.argmin(aic_X_predicts_Y) + 1
# best_lag_Y_predicts_X_aic = np.argmin(aic_Y_predicts_X) + 1

# # Get the best models based on the AIC
# best_model_X_predicts_Y_aic = results_X_predicts_Y[best_lag_X_predicts_Y_aic]
# best_model_Y_predicts_X_aic = results_Y_predicts_X[best_lag_Y_predicts_X_aic]

# # Print the AIC for the best models
# print(f"AIC for the best model for X predicting Y: {best_model_X_predicts_Y_aic[1][1].aic}")
# print(f"AIC for the best model for Y predicting X: {best_model_Y_predicts_X_aic[1][1].aic}")
# print(f"Number of lags for the best model for X predicting Y: {best_lag_X_predicts_Y_aic}")
# print(f"Number of lags for the best model for Y predicting X: {best_lag_Y_predicts_X_aic}")

# # Print the summary of the best model for X predicting Y
# print("Summary of the best model for X predicting Y:")
# print(best_model_X_predicts_Y_aic[1][1].summary())

# # Print the summary of the best model for Y predicting X
# print("Summary of the best model for Y predicting X:")
# print(best_model_Y_predicts_X_aic[1][1].summary())


#######用BIC选model

results_X_predicts_Y = grangercausalitytests(data, maxlag, verbose=False)
results_Y_predicts_X = grangercausalitytests(data_reversed, maxlag, verbose=False)

# Get the BIC for each model
bic_X_predicts_Y = [result[1][1].bic for result in results_X_predicts_Y.values()]
bic_Y_predicts_X = [result[1][1].bic for result in results_Y_predicts_X.values()]

# Ensure the selection starts from the 8th lag, adjusting for zero-based indexing
offset = 8 - 1

# Find the number of lags for the model with the smallest BIC, considering only lags >= 8
best_lag_X_predicts_Y_bic = np.argmin(bic_X_predicts_Y[offset:]) + 8
best_lag_Y_predicts_X_bic = np.argmin(bic_Y_predicts_X[offset:]) + 8

# Get the best models based on the BIC
best_model_X_predicts_Y_bic = results_X_predicts_Y[best_lag_X_predicts_Y_bic]
best_model_Y_predicts_X_bic = results_Y_predicts_X[best_lag_Y_predicts_X_bic]

# Print the BIC for the best models
print(f"BIC for the best model for X predicting Y: {best_model_X_predicts_Y_bic[1][1].bic}")
print(f"BIC for the best model for Y predicting X: {best_model_Y_predicts_X_bic[1][1].bic}")
print(f"Number of lags for the best model for X predicting Y: {best_lag_X_predicts_Y_bic}")
print(f"Number of lags for the best model for Y predicting X: {best_lag_Y_predicts_X_bic}")

# # Print the summary of the best model for X predicting Y
# print("Summary of the best model for X predicting Y:")
# print(best_model_X_predicts_Y_bic[1][1].summary())

# # Print the summary of the best model for Y predicting X
# print("Summary of the best model for Y predicting X:")
# print(best_model_Y_predicts_X_bic[1][1].summary())
