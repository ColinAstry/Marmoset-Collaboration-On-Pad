import os
import pandas as pd
import matplotlib.pyplot as plt
# Load your data into a pandas DataFrame
df = pd.read_excel(r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure3\4\analysis\723test1_20240520.xlsx')

# Calculate the number of correct buttons and total buttons
df['correct_count'] = df['button'].eq('correct').cumsum()
df['total_count'] = df['button'].isin(['correct', 'wrong']).cumsum()

# Assign these counts to x and y
points = df[['correct_count', 'total_count']].values
x = points[:, 1]
y = points[:, 0]

import numpy as np
from scipy.optimize import curve_fit

# Define the piecewise function
def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0, x >= x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

# Fit the data
p , e = curve_fit(piecewise_linear, x, y)
xd = np.linspace(0, max(x), 10000)
yd = piecewise_linear(xd, *p)

# Plot the data and the fit
import matplotlib.pyplot as plt
plt.figure()
plt.plot(x, y, "o")
plt.plot(xd, yd, '-')
plt.show()