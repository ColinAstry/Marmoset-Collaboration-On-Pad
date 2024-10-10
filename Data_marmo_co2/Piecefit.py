from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pandas as pd
from sklearn.metrics import mean_squared_error

# Load your data into a pandas DataFrame
df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure3\4\analysis\723test1_20240520.xlsx')

# Calculate the number of correct buttons and total buttons
df['correct_count'] = df['button'].eq('correct').cumsum()
df['total_count'] = df['button'].isin(['correct', 'wrong']).cumsum()

# Assign these counts to x and y
points = df[['correct_count', 'total_count']].values
x = points[:, 1]
y = points[:, 0]

max_num_lines = 5

# Initialize the best MSE and best number of lines
best_mse = np.inf
best_num_lines = 0
best_popt = None

# Define the piecewise linear function
def piecewise_linear(x, *params):
    num_lines = len(params) // 2
    y = np.zeros_like(x, dtype=float)
    for i in range(num_lines - 1):
        a, t = params[i*2:i*2+2]
        y += np.where((np.sum(params[1::2][:i]) < x) & (x <= np.sum(params[1::2][:i+1])), a * t, 0)
    a, t = params[(num_lines-1)*2:(num_lines-1)*2+2]
    y += np.where(x > np.sum(params[1::2][:num_lines-1]), a * (x - np.sum(params[1::2][:num_lines-1])), 0)
    return y

# Initialize a dictionary to store MSEs and parameters
results_dict = {}

for num_lines in range(1, 5):
    # Initialize the parameters
    p0 = [0, y[0]] * num_lines

    # Use scipy's curve_fit function to fit the piecewise function
    popt, pcov = curve_fit(piecewise_linear, x, y, p0=p0)

    # Calculate the MSE
    mse = mean_squared_error(y, piecewise_linear(x, *popt))

    # Store the MSE and parameters in the dictionary
    parameters = [{'a': popt[i], 'b': popt[i+1]} for i in range(0, len(popt), 2)]
    split_points = [np.sum(popt[1::2][:i+1]) for i in range(num_lines - 1)]  # Add this line
    results_dict[num_lines] = {'mse': mse, 'split_points': split_points, 'parameters': parameters}

    # If this MSE is better than the best MSE so far, update the best MSE and best number of lines
    if mse < best_mse:
        best_mse = mse
        best_num_lines = num_lines
        best_popt = popt

# Print the MSEs, parameters, and split points
for num_lines, result in results_dict.items():
    print(f'Number of lines: {num_lines}, MSE: {result["mse"]}, Parameters: {result["parameters"]}, Split points: {result["split_points"]}')

# Print the best number of lines and the best MSE
print(f'Best number of lines: {best_num_lines}')
print(f'Best MSE: {best_mse}')

# Open the text file in write mode
with open('results.txt', 'w') as f:
    # Write the MSEs and parameters
    for num_lines, result in results_dict.items():
        f.write(f'Number of lines: {num_lines}, MSE: {result["mse"]}, Parameters: {result["parameters"]}, Split points: {result["split_points"]}\n')

    # Write the best number of lines and the best MSE
    f.write(f'Best number of lines: {best_num_lines}\n')
    f.write(f'Best MSE: {best_mse}\n')

# Plot the data and the best fitted curve
plt.plot(x, y, "o")
plt.plot(x, piecewise_linear(x, *best_popt))
plt.show()
