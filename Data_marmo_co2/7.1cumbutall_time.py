import os
import pandas as pd
import matplotlib.pyplot as plt

#画出累积按键数all_count、correct_count、correct + wrong count、correct/c+w随时间变化的图

import sys

file_path = sys.argv[1]

# Read the Excel file
df = pd.read_excel(file_path)

# Sort the DataFrame by 't0' column
df.sort_values('t0', inplace=True)

# Calculate the number of all buttons, correct buttons, correct + wrong buttons, and fraction of correct buttons
#df['all_count'] = df['button'].notna().cumsum()
df['all_count'] = (df['button'].eq('correct') | df['button'].eq('outside')).cumsum()
df['correct_count'] = df['button'].eq('correct').cumsum()
df['correct + wrong_count'] = (df['button'].eq('correct') | df['button'].eq('wrong')).cumsum()
df['correct_fraction'] = df['correct_count'] / df['all_count']

# Find the indices where the "File Name" changes
file_changes = df['Date'].ne(df['Date'].shift())

# Create a figure with two subplots
fig, ax1 = plt.subplots()

# Plot the number of correct buttons，correct + wrong buttons，all buttons
ax1.plot(df['t0'], df['all_count'], color='green', label='All Buttons')
ax1.plot(df['t0'], df['correct_count'], color='blue', label='Correct Buttons')
#ax1.plot(df['t0'], df['correct + wrong_count'], color='orange', label='Correct + Wrong Buttons')

# Set the y-axis label for the first subplot
ax1.set_ylabel('Number of Buttons')

# Create a second subplot sharing the x-axis with the first subplot
ax2 = ax1.twinx()

# Plot the fraction of correct buttons
ax2.plot(df['t0'], df['correct_fraction'], color='red', label='Correct Fraction')

# Set the y-axis label for the second subplot
ax2.set_ylabel('Fraction of Correct Buttons')

# Set the range of the y-axis for the second subplot
ax2.set_ylim([-0.05, 1.05])

# Add vertical dashed lines at the points where the "File Name" changes
x_coords = df.loc[file_changes, 't0']
for x in x_coords:
    ax1.axvline(x=x, color='gray', linestyle='--')

# Set the x-axis label and title
ax1.set_xlabel('t0')
ax1.set_title('Button Analysis')

# Combine the legends of both subplots
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

# Adjust the layout to prevent overlapping labels
fig.tight_layout()

#save the plot
# Get the directory of the Excel file
dir_path = os.path.dirname(file_path)
# Get the filename of the Excel file without extension
file_name = os.path.splitext(os.path.basename(file_path))[0]
# Construct the filename for the plot
plot_filename = f"{file_name}_cumbutall_vs_time.png"
# Construct the full path for the plot
plot_path = os.path.join(dir_path, plot_filename)
# Save the plot
plt.savefig(plot_path)

# Display the plot
plt.show()