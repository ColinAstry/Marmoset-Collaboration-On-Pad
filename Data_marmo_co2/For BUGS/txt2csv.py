import csv
import os

def txt_to_csv(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        content = input_file.read()
        content = content.replace(', ', '\n')  # 将 ", " 替换为换行符
        rows = content.split('\n')  # 按换行符分割为行

        csv_data = [row.split(',') for row in rows]  # 按逗号分割为单元格

        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(csv_data)


# 文件夹路径，包含要处理的文本文件
folder_path = r'C:\Users\Robin\Desktop\1'

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        input_txt_path = os.path.join(folder_path, filename)
        output_csv_path = os.path.splitext(input_txt_path)[0] + '.csv'

        # 将 txt 转换为 csv
        txt_to_csv(input_txt_path, output_csv_path)