import os
import pandas as pd
from datetime import datetime

#change folder path, marmoset' ID and and expriments' name (bottom) before running
########################################################################################
# Set the directory path
folder_path = r"D:\Research\MarmoCo2\Data\ToProcess"

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

########################################################################################
# Filter the files that contain ".434" in their name
excel_files = [file for file in file_list if ".434" in file]

# Initialize an empty list to store dataframes
dataframes = []

# Initialize a variable to store the accumulated "t0" value
accumulated_t0 = 0

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
        date = file[:4]
        id = file[5:8]
        
        # Add columns with the date and ID
        df['Date'] = date
        df['ID'] = id

        # Neglect rows with "exp" in the "note" column or "t0" value less than 0
        df = df[(df['note'] != 'exp') & (df['t0'] >= 0)]

        # Accumulate the "t0" value
        df['t0'] += accumulated_t0

        # Update the accumulated "t0" value
        accumulated_t0 = df['t0'].iloc[-1]

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

# Define the order of columns
column_order = ['ID', 'Date', 'button', 'positionLeft', 'positionTop', 'positionLeftw', 'positionTopw', 't0', 'note', 'time', 'location_x', 'location_y', 'finger']

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
output_file = os.path.join(folder_path, "analysis",f"{id}hab1_{current_date}.xlsx")
combined_df.to_excel(output_file, index=False)

print("Combined sheets saved to:", output_file)


	
