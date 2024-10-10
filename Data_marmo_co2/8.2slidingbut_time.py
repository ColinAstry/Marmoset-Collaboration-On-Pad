import os
import pandas as pd
import matplotlib.pyplot as plt

import sys

file_path = sys.argv[1]

# Read the Excel file
df = pd.read_excel(file_path)

# Sort the DataFrame by 't0' column
df.sort_values('t0', inplace=True)

# Calculate the number of buttons in every 600-second interval
df['t0_group'] = df['t0'].floordiv(600) * 600  # Create a new column for grouping t0 values
button_counts = df.groupby('t0_group')['button'].size()

# Calculate the number of correct + wrong buttons in every 600-second interval
correct_wrong_counts = df[df['button'].isin(['correct', 'wrong'])].groupby('t0_group')['button'].size()

# Calculate the number of correct buttons in every 600-second interval
correct_counts = df[df['button'] == 'correct'].groupby('t0_group')['button'].size()

# Calculate the fraction of correct buttons to all buttons in every 600-second interval
correct_fraction = correct_counts / correct_wrong_counts

fig, ax1 = plt.subplots()

# Plot the counts on the primary y-axis
ax1.plot(correct_wrong_counts, label='Correct + Wrong Buttons', color='orange')
#ax1.plot(button_counts, label='All Buttons', color='green')
ax1.plot(correct_counts, label='Correct Buttons', color='blue')
ax1.set_ylabel('Counts')

# Create a secondary y-axis and plot the fraction on it
ax2 = ax1.twinx()
ax2.plot(correct_fraction, label='Fraction of Correct Buttons', color='red')
ax2.set_ylabel('Fraction')
ax2.set_ylim([-0.05, 1.05])

# Combine legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

#save the plot
# Get the directory of the Excel file
dir_path = os.path.dirname(file_path)
# Get the filename of the Excel file without extension
file_name = os.path.splitext(os.path.basename(file_path))[0]
# Construct the filename for the plot
plot_filename = f"{file_name}_slidingbut_vs_time.png"
# Construct the full path for the plot
plot_path = os.path.join(dir_path, plot_filename)
# Save the plot
plt.savefig(plot_path)

plt.show()