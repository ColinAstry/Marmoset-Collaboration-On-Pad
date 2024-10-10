import os
import pandas as pd
import matplotlib.pyplot as plt
#画出correct_count随correct + wrong count变化的图

import sys

file_path = sys.argv[1]

# Read the Excel file
df = pd.read_excel(file_path)

# Sort the DataFrame by 't0' column
df.sort_values('t0', inplace=True)

# Calculate the number of correct buttons and total buttons
df['correct_count'] = df['button'].eq('correct').cumsum()
df['total_count'] = df['button'].isin(['correct', 'wrong']).cumsum()

# Find the indices where the "File Name" changes
file_changes = df['Date'].ne(df['Date'].shift())

# Plot the relationship between the number of total buttons and the number of correct buttons
plt.plot(df['total_count'], df['correct_count'], color='blue')

# Add vertical dashed lines at the points where the "File Name" changes
x_coords = df.loc[file_changes, 'total_count']
for x in x_coords:
    plt.axvline(x=x, color='gray', linestyle='--')

# Set the plot labels and title
plt.xlabel('Number of Correct + Wrong Buttons')
plt.ylabel('Number of Correct Buttons')
plt.title('Number of Correct Buttons vs Number of Correct + Wrong Buttons')

#save the plot
# Get the directory of the Excel file
dir_path = os.path.dirname(file_path)
# Get the filename of the Excel file without extension
file_name = os.path.splitext(os.path.basename(file_path))[0]
# Construct the filename for the plot
plot_filename = f"{file_name}_correctbut_vs_totalbut.png"
# Construct the full path for the plot
plot_path = os.path.join(dir_path, plot_filename)
# Save the plot
plt.savefig(plot_path)

# Display the plot
plt.show()