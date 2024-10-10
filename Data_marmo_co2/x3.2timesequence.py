import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#folder_path = r"D:\Xu_Haoxin\Research\Gradu_thesis\Data\Pure3\4"

import sys
folder_path = sys.argv[1]


# Create a figure
fig = go.Figure()

# Define colors
correct_color_no_772 = 'rgb(255, 0, 0)'
correct_color_772 = 'rgb(65, 105, 225)'
wrong_color = 'rgba(144, 238, 144, 1.0)'
other_color = 'rgba(220, 220, 220, 0.5)'  # Adjusted transparency for gray color
dot_size = 4  # Adjust the dot size as desired

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    # Skip temporary files created by Excel
    if filename.startswith('~$'):
        continue
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.xlsx'):
        # Read the Excel file
        data = pd.read_excel(file_path)

        # Convert any NaN values in the "note" column to an empty string
        data['note'] = data['note'].fillna('')

        # Filter rows where the "note" column does not contain "exp"
        filtered_data = data[data['note'].astype(str).str.contains('exp') == False]

        # Get other button data (outside and blank)
        other_data = filtered_data[filtered_data['button'].isin(['outside', 'blank'])]

        # # Plot other buttons (outside and blank) with adjusted transparency and dot size
        # fig.add_trace(go.Scatter(x=other_data['t0']/60, y=[filename] * len(other_data),
        #                          mode='markers', marker=dict(color=other_color, size=dot_size), showlegend=False))

        # Get "wrong" button data
        wrong_data = filtered_data[filtered_data['button'] == 'wrong']

        # Plot "wrong" buttons in red
        fig.add_trace(go.Scatter(x=wrong_data['t0']/60, y=[filename] * len(wrong_data),
                                 mode='markers', marker=dict(color=wrong_color, size=dot_size), showlegend=False))

        # Get "correct" button data
        correct_data = filtered_data[filtered_data['button'] == 'correct']

        # Plot "correct" buttons in red if filename doesn't contain ".772", otherwise in blue
        if '.772' not in filename:
            fig.add_trace(go.Scatter(x=correct_data['t0']/60, y=[filename] * len(correct_data),
                                     mode='markers', marker=dict(color=correct_color_no_772, size=dot_size),
                                     showlegend=False))
        else:
            fig.add_trace(go.Scatter(x=correct_data['t0']/60, y=[filename] * len(correct_data),
                                     mode='markers', marker=dict(color=correct_color_772, size=dot_size),
                                     showlegend=False))

# Set layout title, axis labels, and background color
fig.update_layout(title='Button Sticks Plot', xaxis_title='Time (minutes)', yaxis_title='File',
                  plot_bgcolor='rgb(255, 255, 255)')

# Reverse the order of y-axis ticks and labels
fig.update_yaxes(autorange="reversed")

# Show the plot
fig.show()

