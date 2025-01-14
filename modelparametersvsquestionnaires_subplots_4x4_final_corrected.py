import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np

# Load the data
data = pd.read_csv('/mnt/data/organized_data.csv')

# Filter out rows with NaN values in dars_score and shaps_score
filtered_data = data.dropna(subset=['dars_score', 'shaps_score'])

# Define colors for groups with transparency
named_colors_adjusted = {"Non-Anhedonic": (64/255, 224/255, 208/255, 0.5),  # Turquoise with transparency
                         "Anhedonic": (250/255, 128/255, 114/255, 0.5)}  # Salmon with transparency

# Define full names for x and y labels
x_labels = {
    'dars_score': 'DARS Scale',
    'shaps_score': 'SHAPS Scale'
}

y_labels = {
    'Arew': 'Reward Learning Rate',
    'Apun': 'Punishment Learning Rate',
    'R': 'Reward Sensitivity',
    'P': 'Punishment Sensitivity'
}

# Function to create scatter plots with r and p value annotations
def plot_correlation(score, model, ax):
    # Calculate correlation coefficient and p-value
    r, p_val = pearsonr(filtered_data[score], filtered_data[model])
    
    # Plot using circles as markers
    sns.scatterplot(
        x=filtered_data[score], 
        y=filtered_data[model], 
        hue=filtered_data['Group'], 
        palette=named_colors_adjusted, 
        s=100, 
        ax=ax,
        marker='o',
        legend=False  # Disable individual subplot legends
    )
    
    # Set the x and y labels with full names
    ax.set_xlabel(x_labels[score], fontsize=12)
    ax.set_ylabel(y_labels[model], fontsize=12)
    
    # Add the correlation and p-value as an annotation
    ax.text(np.min(filtered_data[score]), np.max(filtered_data[model]),
            f'r = {r:.2f}\np = {p_val:.4f}', 
            fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    
    # Remove grid lines and titles
    ax.grid(False)
    ax.set_title("")

# Create a new figure for the 4x4 layout
fig, axes = plt.subplots(2, 4, figsize=(20, 10))

# Define model parameters
model_params = ['Arew', 'Apun', 'R', 'P']

# Loop through model parameters and x-variables
for i, model in enumerate(model_params):
    for j, score in enumerate(['dars_score', 'shaps_score']):
        ax = axes[j, i]  # Select the appropriate subplot
        plot_correlation(score, model, ax)

# Adjust layout for the plots
plt.tight_layout()

# Save the final plot with 4x4 subplots
subplot_path_final = '/mnt/data/subplots_4x4_final_update.png'
fig.savefig(subplot_path_final, bbox_inches='tight')

# Show the file path for download
subplot_path_final
