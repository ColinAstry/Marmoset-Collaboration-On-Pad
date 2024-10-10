import csv
import os

def split_csv(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        reader = csv.reader(file)
        row = next(reader)  # Read the single row from the input CSV

        csv_data = []
        current_row = []

        for cell in row:
            if cell in ['stage', 'button', 'positionLeft', 'positionTop', 'positionLeftw',
                        'positionTopw', 'time', 'location_x', 'location_y', 'finger']:
                if current_row:
                    csv_data.append(current_row)
                current_row = [cell]
            else:
                current_row.append(cell)

        if current_row:
            csv_data.append(current_row)

    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)


# Folder path containing the input CSV files
folder_path = r'C:\Users\Robin\Desktop\1'

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        input_csv_path = os.path.join(folder_path, filename)
        output_csv_path = os.path.splitext(input_csv_path)[0] + '_split.csv'

        # Split the CSV into multiple rows
        split_csv(input_csv_path, output_csv_path)