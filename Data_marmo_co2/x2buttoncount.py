import os
import pandas as pd
from datetime import datetime
import re

#统计每个文件中的correct、wrong、total按键数

#folder_path = r"D:\Xu_Haoxin\Research\Gradu_thesis\Data434M2\ToProcess\613"

import sys
folder_path = sys.argv[1]

max_t0_dict = {}

# First pass: calculate the maximum t0 for each date without considering 'exp' rows
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{4}', filename).group()
        df = pd.read_excel(os.path.join(folder_path, filename))
        df_filtered = df[df['note'] != 'exp']  # filter out rows with 'exp' in 'note' column
        max_t0 = df_filtered['t0'].max()
        if date in max_t0_dict:
            max_t0_dict[date] = max(max_t0_dict[date], max_t0)
        else:
            max_t0_dict[date] = max_t0

# Create a dictionary to store the button counts
button_counts = {}

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    # Skip temporary files created by Excel
    if filename.startswith('~$'):
        continue

    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.xlsx'):
        # Print the file path
        #print(f'Reading file: {file_path}')

        # Read the Excel file
        data = pd.read_excel(file_path, engine='openpyxl')

        # Exclude rows with "exp" in the 'note' column
        data = data[data['note'] != 'exp']

        # Get "correct" button data
        correct_data = data[data['button'] == 'correct']

        # Get "wrong" button data
        wrong_data = data[data['button'] == 'wrong']

        # Get "outside" button data
        outside_data = data[data['button'] == 'outside']

        # Get "blank" button data
        blank_data = data[data['button'] == 'blank']

        # Count number of correct buttons and total buttons
        num_correct = len(correct_data)
        num_wrong = len(wrong_data)
        num_total = len(data)
        num_outside = len(outside_data)
        num_blank = len(blank_data)

        #get the largest t0 value
        max_t0 = data['t0'].max()

        # Get the value in the "experiment" column
        #experiment = data['experiment'].unique()[0]

        # Store the button counts in the dictionary
        button_counts[filename] = (num_correct,num_wrong,num_total,max_t0,num_outside,num_blank)

# Replace the original max_t0 in button_counts with the max_t0 values from max_t0_dict
for filename in button_counts:
    date = re.search(r'^\d{4}', filename).group()
    if date in max_t0_dict:
        button_counts[filename] = button_counts[filename][:3] + (max_t0_dict[date],) + button_counts[filename][4:]

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Define the output directory
output_dir = os.path.join(folder_path, "analysis")
# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Create the output file name
output_file = os.path.join(output_dir, f"{current_date}_butcounts.txt")

# Write the button counts to a text file with aligned numbers
with open(output_file, 'w') as f:
    for filename, count in button_counts.items():
        correct_count = str(count[0]).rjust(4)
        wrong_count = str(count[1]).rjust(4)
        total_count = str(count[2]).rjust(4)
        outside_count = str(count[4]).rjust(4)
        blank_count = str(count[5]).rjust(4)
        f.write(f"{filename[:-5]}: {correct_count} | {wrong_count} |  {total_count} | {outside_count} | {blank_count} \n")

with open(output_file, 'a') as f:  # 'a' for append mode
    for filename, count in button_counts.items():
        correct_count = str(count[0]).rjust(4)
        wrong_count = str(count[1]).rjust(4)
        total_count = str(count[2]).rjust(4)
        f.write(f"{correct_count} | {wrong_count} |  {total_count}\n")


print(f"Aligned button counts written to {output_file}")

# Define the output path
output_excel = os.path.join(output_dir, f"{current_date}_butcounts.xlsx")

# Convert the button_counts dictionary to a DataFrame
df = pd.DataFrame.from_dict(button_counts, orient='index', columns=['correct', 'wrong', 'total', 'max_t0', 'outside', 'blank'])

# Add 'date' and 'id' columns
df['date'] = df.index.str[:4]
df['id'] = df.index.str[5:8]

# Reorder the columns so 'date' and 'id' are first
df = df[['date', 'id', 'correct', 'wrong', 'total', 'outside', 'blank', 'max_t0']]

# Save the DataFrame to an Excel file
df.to_excel(output_excel, index=False)

#plot the button counts
import matplotlib.pyplot as plt

# Filter filenames and counts for .434.xlsx and .3M2.xlsx files
filenames_434 = [filename for filename in button_counts.keys() if '.xlsx' in filename]

#filenames_3M2 = [filename for filename in button_counts.keys() if '0831.xlsx' in filename]

# Calculate the average counts per hour
correct_counts_434 = [(button_counts[filename][0] / button_counts[filename][3]) * 3600 for filename in filenames_434]
wrong_counts_434 = [(button_counts[filename][1] / button_counts[filename][3]) * 3600 for filename in filenames_434]
total_counts_434 = [(button_counts[filename][2] / button_counts[filename][3]) * 3600 for filename in filenames_434]
outside_counts_434 = [(button_counts[filename][4] / button_counts[filename][3]) * 3600 for filename in filenames_434]
blank_counts_434 = [(button_counts[filename][5] / button_counts[filename][3]) * 3600 for filename in filenames_434]

# correct_counts_3M2 = [(button_counts[filename][0] / button_counts[filename][3]) * 3600 for filename in filenames_3M2]
# wrong_counts_3M2 = [(button_counts[filename][1] / button_counts[filename][3]) * 3600 for filename in filenames_3M2]
# total_counts_3M2 = [(button_counts[filename][2] / button_counts[filename][3]) * 3600 for filename in filenames_3M2]
# outside_counts_3M2 = [(button_counts[filename][4] / button_counts[filename][3]) * 3600 for filename in filenames_3M2]
# blank_counts_3M2 = [(button_counts[filename][5] / button_counts[filename][3]) * 3600 for filename in filenames_3M2]
# # Create a new figure with a specific size
fig, axs = plt.subplots(2, figsize=(10, 12))
# Define the width of the bars and the positions
width = 0.2
pos_434 = [i for i in range(len(filenames_434))]
# pos_3M2 = [i for i in range(len(filenames_3M2))]

# Define the colors for the bars
colors = ['skyblue', 'salmon', 'lightgreen']

# Create bar plots for .434.xlsx files
axs[0].bar([p  for p in pos_434], correct_counts_434, width, label='Correct', color=colors[0])
axs[0].bar([p -  width for p in pos_434], wrong_counts_434, width, label='Wrong', color=colors[1])
axs[0].bar([p +  width  for p in pos_434], total_counts_434, width, label='Total', color=colors[2])
axs[0].bar([p +  width for p in pos_434], outside_counts_434, width, label='Outside', color='gray')
axs[0].bar([p + 2*width for p in pos_434], blank_counts_434, width, label='Blank', color='black')
# # Create bar plots for .3M2.xlsx files
# axs[1].bar([p  for p in pos_3M2], correct_counts_3M2, width, label='Correct', color=colors[0])
# axs[1].bar([p - width for p in pos_3M2], wrong_counts_3M2, width, label='Wrong', color=colors[1])
# axs[1].bar([p + width for p in pos_3M2], total_counts_3M2, width, label='Total', color=colors[2])
# axs[1].bar([p + width for p in pos_3M2], outside_counts_3M2, width, label='Outside', color='gray')
# axs[1].bar([p + 2*width for p in pos_3M2], blank_counts_3M2, width, label='Blank', color='black')

# Set the y-axis limits
axs[0].set_ylim(0, 450)
axs[1].set_ylim(0, 450)

# Set the x-ticks to be the filenames
axs[0].set_xticks(pos_434)
axs[0].set_xticklabels([filename[:4] for filename in filenames_434], rotation='vertical')
# axs[1].set_xticks(pos_3M2)
# axs[1].set_xticklabels([filename[:4] for filename in filenames_3M2], rotation='vertical')

# Add labels and a title
axs[0].set_ylabel('Count')
axs[0].set_title('lef')
axs[0].legend()

axs[1].set_xlabel('Date')
axs[1].set_ylabel('Count')
axs[1].set_title('rig')
axs[1].legend()

# Save the plot as an image
fig.savefig(os.path.join(output_dir, f"{current_date}_average_butcounts.png"))

# Show the plot
plt.tight_layout()
plt.show()