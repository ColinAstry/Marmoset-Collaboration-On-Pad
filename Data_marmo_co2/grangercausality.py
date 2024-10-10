import os
import pandas as pd
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

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
        time_series = np.arange(0, max_t0, 0.1)
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

            # Combine the two spike trains into a 2D array
            data = np.vstack([spike_trains[i], spike_trains[j]]).T
            
            # Apply the Granger causality test
            gc_results = grangercausalitytests(data, maxlag=10)
            
            # Print the results
            for lag, result in gc_results.items():
                print(f'Lag: {lag}')
                print(f'F-statistic: {result[0]["ssr_ftest"][0]}')
                print(f'p-value: {result[0]["ssr_ftest"][1]}')