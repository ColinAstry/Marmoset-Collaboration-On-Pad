import os
import pandas as pd
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

# Get a list of all Excel files in the directory
folder_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\trials'
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Group the Excel files by date
files_by_date = {}
for file in excel_files:
    date = file[:3]
    if date not in files_by_date:
        files_by_date[date] = []
    files_by_date[date].append(file)

from scipy.ndimage import gaussian_filter
from scipy.stats import percentileofscore

# For each date, create spike trains and compute cross-correlation
for date, files in files_by_date.items():
    # Find the maximum t0 across all files with this date
    max_t0 = max(pd.read_excel(os.path.join(folder_path, file)).loc[~pd.read_excel(os.path.join(folder_path, file))['note'].fillna('').str.contains('exp')]['t0'].max() for file in files)
    
    # Create a spike train for each file
    spike_trains = []
    for file in files:
        df = pd.read_excel(os.path.join(folder_path, file))
        time_series = np.arange(df['t0'].min(), max_t0, 0.1)
        spike_train = np.zeros_like(time_series)
        indices = np.searchsorted(time_series, df['t0'])
        valid_indices = indices[indices < len(spike_train)]
        spike_train[valid_indices] = 1

        # Smooth the spike train with a Gaussian filter
        smoothed_spike_train = gaussian_filter(spike_train, sigma=2)

        spike_trains.append(smoothed_spike_train)

        # # Plot the smoothed spike train
        # plt.figure(figsize=(10, 6))
        # plt.plot(time_series, smoothed_spike_train)
        # plt.title(f'Smoothed spike train for file {file}')
        # plt.show()

    # Compute the cross-correlation between each pair of spike trains
    for i in range(len(spike_trains)):
        for j in range(i+1, len(spike_trains)):
      
            # Compute the cross-correlation
            cross_corr = np.correlate(spike_trains[i], spike_trains[j], mode='full')
            
            # Normalize the cross-correlation
            cross_corr = cross_corr / np.sqrt(np.sum(spike_trains[i]**2) * np.sum(spike_trains[j]**2))
            
            # Compute the maximum absolute value of the cross-correlation
            max_cross_corr = np.max(np.abs(cross_corr))

            #print the maximum cross correlation
            print(f'Maximum cross-correlation between spike trains {i} and {j}: {max_cross_corr}')
            
            # # Compute the Fisher transformation
            # fisher_z = np.arctanh(max_cross_corr)
            
            # # Compute the standard error
            # se = 1/np.sqrt(len(spike_trains[i])-3)
            
            # # Compute the confidence interval
            # ci = [np.tanh(fisher_z - 1.96*se), np.tanh(fisher_z + 1.96*se)]
            
            # # Print the confidence interval
            # print(f'Confidence interval: {ci}')
            
            # # If the confidence interval does not include zero, the correlation is statistically significant
            # if ci[0] > 0 or ci[1] < 0:
            #     print('The correlation is statistically significant.')
            # else:
            #     print('The correlation is not statistically significant.')

            # Plot the cross-correlation
            plt.figure(figsize=(10, 6))
            plt.plot(range(-len(cross_corr)//2, len(cross_corr)//2), cross_corr)
            plt.title(f'Cross-correlation on {date}')
            plt.show()

            