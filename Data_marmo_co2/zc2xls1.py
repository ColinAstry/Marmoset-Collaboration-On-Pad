import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

#############这个程序会把第一列删除，不能用

def convert_csv_to_xlsx(folder_path):
    # 获取文件夹中的所有CSV文件
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    for csv_file in csv_files:
        # 构建CSV文件路径
        csv_path = os.path.join(folder_path, csv_file)

        # 读取CSV文件
        df = pd.read_csv(csv_path)

        # 转置数据
        df = df.transpose()

        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active

        # 将数据写入工作表
        for r in dataframe_to_rows(df, index=False, header=False):  # 设置index=False，header=False
            ws.append(r)

        # 构建XLSX文件路径
        xlsx_file = os.path.splitext(csv_file)[0] + '.xlsx'
        xlsx_path = os.path.join(folder_path, xlsx_file)

        # 保存为XLSX文件
        wb.save(xlsx_path)

        print(f'转换完成：{csv_file} -> {xlsx_file}')

    print('所有CSV文件已转换为XLSX格式并保存在相同文件夹中。')

# 使用示例

import sys

# The first argument is the script name itself, so we get the second argument
# folder_path = sys.argv[1]  # replace with your actual folder path
folder_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data434M2\ToProcess'
convert_csv_to_xlsx(folder_path)
