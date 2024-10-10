import pandas as pd
import numpy as np
import glob

# Specify the folder containing the Excel files
folder_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\granger3'  # replace with your actual folder path

# Find all Excel files in the folder
excel_files = glob.glob(f'{folder_path}/*.xlsx')

# Read the first Excel file into df1 and the second one into df2
df1 = pd.read_excel(excel_files[0])
df2 = pd.read_excel(excel_files[1])

def process_file(df1, df2, filename):
    # Find the row which has 'correct' in the 'button' column
    correct_row_df1 = df1.loc[df1['button'] == 'correct']

    # Create a DataFrame for time ranges
    time_ranges = pd.DataFrame()
    t0_correct_values = correct_row_df1['t0'].values  # Get all 't0' values from the correct rows
    # Calculate 't0' + 30 for all correct rows
    t0_plus_30_values = t0_correct_values + 30

    # Add these to the time_ranges DataFrame
    time_ranges['Start'] = t0_correct_values
    time_ranges['End'] = t0_plus_30_values

    # Sort the DataFrame by 'Start'
    time_ranges = time_ranges.sort_values('Start')

    # Initialize a list to hold the merged ranges
    merged_ranges = []
    # Initialize the current range
    current_range = [time_ranges.iloc[0]['Start'], time_ranges.iloc[0]['End']]

    for _, row in time_ranges.iterrows():
        # If the current row's start is within the current range, extend the range's end
        if row['Start'] <= current_range[1]:
            current_range[1] = max(current_range[1], row['End'])
        else:
            # If the current row's start is outside the current range, add the current range to the list
            # and start a new range
            merged_ranges.append(current_range)
            current_range = [row['Start'], row['End']]

    # Add the last range to the list
    merged_ranges.append(current_range)

    # Convert the list of lists to a DataFrame
    merged_ranges_df = pd.DataFrame(merged_ranges, columns=['Start', 'End'])

    # Calculate the duration of each range
    merged_ranges_df['Duration'] = merged_ranges_df['End'] - merged_ranges_df['Start']

    # Calculate the whole duration inside the desired time ranges
    duration_inside = merged_ranges_df['Duration'].sum()

    # Find the maximum 't0' value in the original DataFrame
    max_t0 = df1['t0'].max()

    # Calculate the duration outside of the desired time ranges
    duration_outside = max_t0 - duration_inside

    # Initialize counters
    count_inside = 0
    count_outside = 0

    # Iterate over the rows in df2
    for _, row in df2.iterrows():
        t0 = row['t0']  # Replace 't0' with the actual column name if it's different
        # Check if t0 falls within any of the ranges in merged_ranges_df
        if any((start <= t0 <= end) for start, end in merged_ranges_df[['Start', 'End']].values):
            count_inside += 1
        else:
            count_outside += 1

    # Calculate the total duration
    total_duration = duration_inside + duration_outside

    total_count = count_inside + count_outside

    # #卡方检验    
    # # Calculate the expected counts
    # expected_count_inside = total_count * (duration_inside / total_duration)
    # expected_count_outside = total_count * (duration_outside / total_duration)

    # from scipy.stats import chisquare

    # # Perform the chi-square test
    # chi2, p = chisquare([count_inside, count_outside], [expected_count_inside, expected_count_outside])

    # # Print the p-value
    # print("p-value: ", p)

    #单样本比例检验
    from statsmodels.stats.proportion import proportions_ztest
    
    # Calculate the sample proportion
    count = count_inside
    nobs = total_count
    
    # Calculate the target proportion
    value = duration_inside / total_duration
    
    # Perform the one-sample proportion test
    stat, pval = proportions_ztest(count, nobs, value)
    
    # Print the z-statistic and p-value
    print(f'z-stat: {stat}\np-value: {pval}')
    
    out_path = r'C:\Users\Robin\Desktop\granger result'

    # Print the results to a text file
    with open(f'{out_path}/{filename}', 'w') as f:
        #write chi-square and p-value
        # f.write("Chi-square: " + str(chi2) + "\n")  # Add this line
        # f.write("p-value: " + str(p) + "\n")
        f.write(f"z,p,inside,total,proporion,time_proportion\n")
        f.write(f"{stat},{pval},{count_inside},{total_count},{count_inside/total_count},{value}\n")
        f.write("Number of rows inside the time range: " + str(count_inside) + "\n")
        f.write("Number of rows outside the time range: " + str(count_outside) + "\n")
        f.write("Total duration of the time range: " + str(duration_inside) + "\n")
        f.write("Duration outside of the time range: " + str(duration_outside) + "\n")
        f.write("\nMerged time ranges:\n")
        f.write(merged_ranges_df.to_string())

# Call the function for each pair of Excel files
process_file(df1, df2, '3zresults1.txt')
process_file(df2, df1, '3zresults2.txt')


