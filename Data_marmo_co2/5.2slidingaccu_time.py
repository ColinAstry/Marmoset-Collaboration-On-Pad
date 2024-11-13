import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

file_path = sys.argv[1]

# Read the original Excel file
data = pd.read_excel(file_path)

# Extract the relevant columns
results = data[data["button"].isin(["correct", "wrong"])]  # Select "correct" and "outside" trials
time_sequences = results["t0"].tolist()
dates = results["Date"].astype(str).tolist()  # Convert "File Name" to string

# Calculate the accumulating accuracy for data points 1 to 9
def calculate_accumulating_accuracy(results):
    num_trials = len(results)
    accumulating_accuracy = []

    for i in range(1, num_trials + 1):
        window = results[:i]
        num_correct = window.count("correct")
        num_outside = window.count("wrong")
        accuracy = (num_correct / i) * 100  # Calculate accuracy as a percentage
        accumulating_accuracy.append(accuracy)

    return accumulating_accuracy

accumulating_accuracy = calculate_accumulating_accuracy(results["button"].tolist()[:9])

# Calculate the sliding window accuracy for the remaining data points
def calculate_sliding_window_accuracy(results, window_width):
    num_trials = len(results)
    accuracy_scores = []

    for i in range(num_trials - window_width + 1):
        window = results[i:i+window_width]
        num_correct = window.count("correct")
        num_outside = window.count("wrong")
        accuracy = (num_correct / window_width) * 100  # Calculate accuracy as a percentage
        accuracy_scores.append(accuracy)

    return accuracy_scores

num_data_points = len(results)
window_width = min(10, num_data_points)  # Adjust window width based on available data points
sliding_window_accuracy = calculate_sliding_window_accuracy(results["button"].tolist(), window_width)

# Combine the accumulating accuracy and sliding window accuracy
accuracy_values = accumulating_accuracy + sliding_window_accuracy

# Create a new DataFrame for the results
result_data = pd.DataFrame({"Date": dates, "Accuracy": accuracy_values, "Time": time_sequences})

#get the point where the accuracy >= 90
index = 0
for i in range(len(result_data["Accuracy"])):
    if result_data["Accuracy"][i] >= 90:
        index = i
        break

print(result_data["Time"][index])
#print the number of trials needed to reach 90% accuracy
print(index)

# Save results to Excel file
# Get the directory of the original file
original_file_dir = os.path.dirname(file_path)
# Get the base name of the original file (without extension)
original_file_base = os.path.splitext(os.path.basename(file_path))[0]
# Define the output file name
output_file_name = original_file_base + "_sliacc_time.xlsx"
# Define the output file path
output_file_path = os.path.join(original_file_dir, output_file_name)

with pd.ExcelWriter(output_file_path) as writer:
    result_data.to_excel(writer, sheet_name="Results", index=False)
    data.to_excel(writer, sheet_name="Original Data", index=False)

# Plot the results
plt.plot(result_data["Time"], result_data["Accuracy"])
plt.xlabel("Time")
plt.ylabel("Accuracy (%)")
plt.title("Accumulating Accuracy")

# Set the y-axis range from -0.05 to 1
plt.ylim(-5, 105)

# Add vertical dashed lines at each change in File Name
date_changes = []
prev_date = None

for i, date in enumerate(dates):
    if date != prev_date:
        date_changes.append(i)
        prev_date = date

for change_index in date_changes:
    plt.axvline(result_data["Time"][change_index], color='gray', linestyle='--')

#plot red vertical line at the point where accuracy >= 90
plt.axvline(result_data["Time"][index], color='red', linestyle='--')

# Define the plot file name (same as output file name but with .png extension)
plot_file_name = original_file_base + "_sliacc_time.png"

# Define the plot file path
plot_file_path = os.path.join(original_file_dir, plot_file_name)

# Save the plot as a PNG file
plt.savefig(plot_file_path)

# Show the plot
plt.show()
