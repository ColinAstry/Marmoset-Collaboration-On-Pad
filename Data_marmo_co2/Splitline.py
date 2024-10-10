import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pandas as pd


# Load your data into a pandas DataFrame
df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure3\4\analysis\723test1_20240520.xlsx')

# Calculate the number of correct buttons and total buttons
df['correct_count'] = df['button'].eq('correct').cumsum()
df['total_count'] = df['button'].isin(['correct', 'wrong']).cumsum()

# Assign these counts to x and y
points = df[['correct_count', 'total_count']].values
x = points[:, 1]
y = points[:, 0]

# Define a piecewise function
def piecewise_linear(x, *params):
    x0 = np.sort(params[::3])
    y0 = params[1::3]
    k = params[2::3]
    return np.piecewise(x, [x < xi for xi in x0], 
                        [lambda x, xi=xi, yi=yi, ki=ki: ki*x + yi-ki*xi for xi, yi, ki in zip(x0, y0, k)])

def error(params, x, y):
    return np.sum((y - piecewise_linear(x, *params)) ** 2) / len(x)

# Initialize a list to store the results
results = []

max_num_lines = 5

# Loop over the desired number of lines
for num_lines in range(1, 6):
    # Initialize the parameters
    p0 = [0, y[0], (y[-1]-y[0])/x[-1]] * num_lines
    # Use scipy's minimize function to minimize the error function
    res = minimize(error, p0, args=(x, y), method='Nelder-Mead')
    # Pad the res.x list with None values to ensure it always has 2*max_num_lines elements
    params = list(res.x)
    params += [None] * (2*max_num_lines - len(params))
    # Store the result
    results.append([num_lines, res.fun] + params)  # Use params instead of list(res.x)

# Create a DataFrame from the results
max_columns = max(len(r) for r in results)
df_results = pd.DataFrame(results, columns=['num_lines', 'MSE'] + ['x' + str(i//2+1) if i%2==0 else 'k' + str(i//2+1) for i in range(2, max_columns)])

import os

# Assume this is your input data path
file_path = r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure3\4\analysis\723test1_20240520.xlsx'

# Get the directory of the input data
file_dir = os.path.dirname(file_path)

# Create the output file path
output_file_path = os.path.join(file_dir, 'results.xlsx')

# Save the DataFrame to the output file
df_results.to_excel(output_file_path, index=False)