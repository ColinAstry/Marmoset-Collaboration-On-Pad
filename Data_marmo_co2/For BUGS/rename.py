import os

folder_path = r"D:\Xu_Haoxin\Research\gradu_thesis\Data\Pure1"
# Iterate over each file in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.xlsx'):
        # Split the file name into parts
        name_parts = file_name.split('.')
        if len(name_parts) == 3:
            new_file_name = f"{name_parts[1]}.{name_parts[0]}.{name_parts[2]}"
            new_file_path = os.path.join(folder_path, new_file_name)
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed file: {file_name} -> {new_file_name}")
        else:
            print(f"Cannot rename file: {file_name} - Invalid file name format")
    else:
        print(f"Skipping file: {file_name} - Not an Excel file")