import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# folder_path = r"D:\Xu_Haoxin\Research\Gradu_thesis\Data434M2\ToProcess\613"

import sys
folder_path = sys.argv[1]

fig = go.Figure()

correct_color_no_772 = 'rgb(255, 0, 0)'
correct_color_772 = 'rgb(65, 105, 225)'
wrong_color = 'rgba(144, 238, 144, 1.0)'
other_color = 'rgba(150, 150, 150, 0.8)'  
dot_size = 4  

for filename in os.listdir(folder_path):
    if filename.startswith('~$') or not filename.endswith('.xlsx'):
        continue
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.xlsx'):
        data = pd.read_excel(file_path)

        data['note'] = data['note'].fillna('')

        filtered_data = data[data['note'].astype(str).str.contains('exp') == False]

        other_data = filtered_data[filtered_data['button'].isin(['outside', 'blank'])]

        fig.add_trace(go.Scatter(x=other_data['t0']/60, y=[filename[:8]] * len(other_data),
                     mode='markers', marker=dict(color=other_color, size=dot_size), showlegend=False))

    wrong_data = filtered_data[filtered_data['button'] == 'wrong']

    fig.add_trace(go.Scatter(x=wrong_data['t0']/60, y=[filename[:8]] * len(wrong_data),
                 mode='markers', marker=dict(color=wrong_color, size=dot_size), showlegend=False))

    correct_data = filtered_data[filtered_data['button'] == 'correct']

    if '.434' not in filename:
        fig.add_trace(go.Scatter(x=correct_data['t0']/60, y=[filename[:8]] * len(correct_data),
                     mode='markers', marker=dict(color=correct_color_no_772, size=dot_size),
                     showlegend=False))
    else:
        fig.add_trace(go.Scatter(x=correct_data['t0']/60, y=[filename[:8]] * len(correct_data),
                     mode='markers', marker=dict(color=correct_color_772, size=dot_size),
                     showlegend=False))

fig.update_layout(title='Button Sticks Plot', xaxis_title='Time (minutes)', yaxis_title='File',
          plot_bgcolor='rgb(255, 255, 255)')

fig.update_yaxes(autorange="reversed")

fig.show()

