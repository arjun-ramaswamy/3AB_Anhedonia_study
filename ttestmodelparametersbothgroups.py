import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('/mnt/data/organized_data.csv')

# Define the parameters we are interested in
parameters = ['Arew', 'Apun', 'R', 'P']

# Initialize a list to store the data frames for plotting
plot_data_list = []

# Loop through each parameter and calculate mean and SEM for both groups
for param in parameters:
    group_summary = data.groupby('Group').agg(
        Mean=(param, 'mean'),
        SEM=(param, lambda x: np.std(x) / np.sqrt(len(x)))
    ).reset_index()
    
    group_summary['Parameter'] = param
    plot_data_list.append(group_summary)

# Combine all the data frames into one for plotting
plot_data = pd.concat(plot_data_list, ignore_index=True)

# Bright colors for Anhedonic and Non-Anhedonic groups
shiny_colors = {'Anhedonic': '#FF6666', 'Non-Anhedonic': '#00CCCC'}

# Create the figure with four subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Define the parameters in order of their positions in the subplots
parameters_in_order = ['Arew', 'Apun', 'R', 'P']

# Loop through the subplots and the parameters to plot each one
for ax, param in zip(axes.flat, parameters_in_order):
    ax_data = plot_data[plot_data['Parameter'] == param]
    
    # Bar plot for each parameter with custom group colors
    sns.barplot(x='Group', y='Mean', data=ax_data, ax=ax, palette=shiny_colors, ci=None)
    
    # Add error bars
    ax.errorbar(
        x=np.arange(len(ax_data['Group'])),
        y=ax_data['Mean'],
        yerr=ax_data['SEM'],
        fmt='none', c='black', capsize=5
    )
    
    # Adjust y-axis ticks for 'Arew' and 'Apun'
    max_height = ax_data['Mean'].max() + ax_data['SEM'].max() + 0.05
    if param in ['Arew', 'Apun']:
        ax.set_yticks(np.arange(0, max_height, 0.1))
    else:
        ax.set_yticks(np.arange(0, max_height, 1))
    
    # Set the title for each subplot
    ax.set_title(param)
    
    # Remove grid lines
    ax.grid(False)
    
    # Remove x-axis label
    ax.set_xlabel('')

# Set common labels
fig.text(0.5, 0.04, 'Group', ha='center', fontsize=12)
fig.text(0.04, 0.5, 'Mean with SEM', va='center', rotation='vertical', fontsize=12)

# Add a legend with title 'Group'
handles = [plt.Rectangle((0,0),1,1, color=shiny_colors[group]) for group in shiny_colors]
labels = ['Anhedonic', 'Non-Anhedonic']
fig.legend(handles, labels, title='Group', loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.05))

# Adjust layout
plt.tight_layout(rect=[0.05, 0.05, 1, 0.95])

# Show the final plot
plt.show()