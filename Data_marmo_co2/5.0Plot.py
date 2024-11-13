
import os
import subprocess

#画图

file_path = r'D:\Research\MarmoCo2\Data\ToProcess_Exp\analysis\xlsExp1_20241017.xlsx'  # replace with your actual folder path

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Call 5.1slidingaccu_cumbut.py, 滑窗正确率随correct+wrong按键次数的变化 
subprocess.Popen(["python", os.path.join(current_dir, "5.1slidingaccu_cumbut.py"), file_path])

# Call 5.2slidingaccu_time.py, 滑窗正确率随time的变化 
subprocess.Popen(["python", os.path.join(current_dir, "5.2slidingaccu_time.py"), file_path])

# Call 6correctbut_cumbut.py, correct按键随correct+wrong按键次数的变化
subprocess.Popen(["python", os.path.join(current_dir, "6correctbut_cumbut.py"), file_path])

# Call 7.1cumbutall_time.py，按键数随time的变化
subprocess.Popen(["python", os.path.join(current_dir, "7.1cumbutall_time.py"), file_path])

# Call 7.2cumbut_time.py，按键数（不包括outside和blank）随time的变化
subprocess.Popen(["python", os.path.join(current_dir, "7.2cumbut_time.py"), file_path])

# Call 8.1slidingbutall_time.py，平均按键数随time的变化
subprocess.Popen(["python", os.path.join(current_dir, "8.1slidingbutall_time.py"), file_path])

# Call 8.2slidingbut_time.py， 按键数（不包括outside和blank）随time的变化
subprocess.Popen(["python", os.path.join(current_dir, "8.2slidingbut_time.py"), file_path])
