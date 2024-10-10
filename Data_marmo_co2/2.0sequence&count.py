import os
import subprocess

#按键序列图和按键总数统计

folder_path = r"D:\Research\MarmoCo2\Data\ToProcess"

current_dir = os.path.dirname(os.path.abspath(__file__))  # Define the variable current_dir

#call x2buttoncount.py
subprocess.Popen(["python", os.path.join(current_dir, "x2buttoncount.py"), folder_path])

#call x3.1timesequenceall.py
subprocess.Popen(["python", os.path.join(current_dir, "x3.1timesequenceall.py"), folder_path])

#call x3.2timesequence.py
#subprocess.Popen(["python", os.path.join(current_dir, "x3.2timesequence.py"), folder_path])
