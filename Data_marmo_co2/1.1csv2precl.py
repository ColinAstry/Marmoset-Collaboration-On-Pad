import os
import subprocess

#将原始数据转换为预处理数据

folder_path = r'D:\Research\MarmoCo2\Data\ToFilter'  # replace with your actual folder path

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Call c2xls1.py 将csv文件转换为xlsx文件
subprocess.Popen(["python", os.path.join(current_dir, "zc2xlsx.py"), folder_path])

# Call raw2precl.py 在xlsx文件里插入新列
subprocess.Popen(["python", os.path.join(current_dir, "zraw2precl.py"), folder_path])