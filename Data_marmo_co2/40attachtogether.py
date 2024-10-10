import os
import pandas as pd
from datetime import datetime

#change folder path, marmoset' ID and and expriments' name (bottom) before running
########################################################################################
# Set the directory path
folder_path = r"D:\Xu_Haoxin\Research\Gradu_thesis\Data\Concise0"

# Initialize a dictionary to store the maximum t0 for each date
max_t0_dict = {}

# Initialize a dictionary to store the accumulated max t0 for each date
accumulated_max_t0 = {}

# Get a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Sort the files by date
excel_files.sort(key=lambda f: f[:3])

# First pass: calculate the maximum t0 for each date without considering 'exp' rows
for filename in excel_files:
    date = filename[:3]
    df = pd.read_excel(os.path.join(folder_path, filename))
    df_filtered = df[df['note'] != 'exp']  # filter out rows with 'exp' in 'note' column
    #check if there is any negative value in t0
    if df_filtered['t0'].lt(0).any():
        print(f"Warning: Negative value in t0 for {filename}")
    max_t0 = df_filtered['t0'].max()
    if date in max_t0_dict:
        max_t0_dict[date] = max(max_t0_dict[date], max_t0)
    else:
        max_t0_dict[date] = max_t0

#print the max t0 for each date
for date, max_t0 in max_t0_dict.items():
    print(f"Max t0 for {date}: {max_t0}")

# Second pass: calculate the accumulated max t0 for each date
previous_date = None
for date in sorted(max_t0_dict.keys()):
    if previous_date is not None:
        accumulated_max_t0[date] = accumulated_max_t0[previous_date] + max_t0_dict[date]
    else:
        accumulated_max_t0[date] = max_t0_dict[date]
    previous_date = date

#print(accumulated_max_t0)
# Print the accumulated max t0 for each date
for date, max_t0 in accumulated_max_t0.items():
    print(f"Accumulated max t0 for {date}: {max_t0}")

########################################################################################
# Filter the files that contain ".723" in their name
excel_files = [file for file in excel_files if ".772" in file]

# Initialize an empty list to store dataframes
dataframes = []

# Iterate over the Excel files and sheets
for file in excel_files:
    # Skip temporary files created by Excel
    if file.startswith('~$'):
        continue
    file_path = os.path.join(folder_path, file)
    xls = pd.ExcelFile(file_path)

    # Iterate over the sheets in each Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = xls.parse(sheet_name)

        # Extract date and ID from the file name
        date = file[:3]
        id = file[4:7]
        
        # Add columns with the date and ID
        df['Date'] = date
        df['ID'] = id

        # Neglect rows with "exp" in the "note" column or "t0" value less than 0
        df = df[(df['note'] != 'exp') & (df['t0'] >= 0)]

        # Append the DataFrame to the list
        dataframes.append(df)

# Get the common columns across all dataframes
common_columns = set(dataframes[0].columns)
for df in dataframes[1:]:
    common_columns.intersection_update(df.columns)

# Convert the set to a list
common_columns = list(common_columns)

# Concatenate the dataframes by aligning common columns
combined_df = pd.concat([df.loc[:, common_columns] for df in dataframes], axis=0)

# Rename the 't0' column to 't00'
combined_df.rename(columns={'t0': 't00'}, inplace=True)

# Initialize the previous date
previous_date = None

# Create a new 't0' column
for date in combined_df['Date'].unique():
    # Get the indices for the current date
    indices = combined_df['Date'] == date

    # Add the accumulated max t0 of the previous date to the 't00' values
    if previous_date is not None:
        combined_df.loc[indices, 't0'] = combined_df.loc[indices, 't00'] + accumulated_max_t0[previous_date]
    else:
        combined_df.loc[indices, 't0'] = combined_df.loc[indices, 't00']

    # Update the previous date
    previous_date = date

# Update the column order
column_order = ['ID', 'Date', 'button', 'positionLeft', 'positionTop', 'positionLeftw', 'positionTopw', 't00', 't0', 'note', 'location_x', 'location_y', 'finger','experiment']

# Reorder the columns
combined_df = combined_df[column_order]

# Get the list of other columns that were not included in column_order
other_columns = [col for col in combined_df.columns if col not in column_order]

# Combine column_order and other_columns
new_order = column_order + other_columns

# Reorder the columns of the combined dataframe
combined_df = combined_df.reindex(columns=new_order)

# Write the combined DataFrame to a new Excel file
# Define the output directory
output_dir = os.path.join(folder_path, "analysis")
# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

current_date = datetime.now().strftime('%Y%m%d')

##############################################################################################
output_file = os.path.join(folder_path, "analysis",f"{id}.xlsx")
combined_df.to_excel(output_file, index=False)

print("Combined sheets saved to:", output_file)


	
