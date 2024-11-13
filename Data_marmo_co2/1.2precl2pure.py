import os
import pandas as pd
import re

#将预处理数据转换为纯净数据（剔除exp行，并重新对齐时间）

# dir_path = r'D:\Research\MarmoCo2\Data\ToFilter\precl'
dir_path = r'D:\Research\MarmoCo24fall\Data_B8\ToFilter\precl'

print(dir_path)
min_abstime_dict = {}

# Create the output directory if it doesn't exist
output_dir = os.path.join(dir_path, 'Pure')
os.makedirs(output_dir, exist_ok=True)

# First pass: calculate the minimum abstime for each date without considering 'exp' rows
for filename in os.listdir(dir_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{4}', filename).group()
        df = pd.read_excel(os.path.join(dir_path, filename))
        df_filtered = df[df['note'] != 'exp']  # filter out rows with 'exp' in 'note' column
        min_abstime = df_filtered['abstime'].min()
        if date in min_abstime_dict:
            min_abstime_dict[date] = min(min_abstime_dict[date], min_abstime)
        else:
            min_abstime_dict[date] = min_abstime

# Second pass: subtract the minimum abstime from the abstime values in each file considering all rows
for filename in os.listdir(dir_path):
    if filename.endswith('.xlsx'):
        date = re.search(r'^\d{4}', filename).group()
        df = pd.read_excel(os.path.join(dir_path, filename))
        df['t0'] = (df['abstime'] - min_abstime_dict[date])/1000
        df['t1'] = (df['abstime'] - min_abstime_dict[date])/60000
        df.to_excel(os.path.join(output_dir, filename), index=False)



