# Correcting the code to load the file and execute the plot with the new legend

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd

# Load the dataset from the file provided earlier
data = pd.read_csv('/mnt/data/4AB_vs_3AB_model_parameters.csv')

# Get the number of subjects (samples) in the data
n_samples = len(data)

# Full form labels for the parameters (axis titles)
parameters_4AB = ['Arew_4AB', 'Apun_4AB', 'R_4AB', 'P_4AB']
parameters_3AB = ['Arew_3AB', 'Apun_3AB', 'R_3AB', 'P_3AB']
simple_titles = ['Reward Learning Rate', 'Punishment Learning Rate', 
                 'Reward Sensitivity', 'Punishment Sensitivity']

# Prepare the figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# Iterate over the pairs of parameters for each subplot
for i, (param_4AB, param_3AB, simple_title) in enumerate(zip(parameters_4AB, parameters_3AB, simple_titles)):
    row = i // 2
    col = i % 2
    
    # Scatter plot with transparency and a regression line with confidence interval shading
    sns.regplot(x=data[param_4AB], y=data[param_3AB], ax=axes[row, col],
                scatter_kws={'s': 50, 'color': 'teal', 'alpha': 0.6}, 
                line_kws={"color": "salmon"}, marker='o', ci=95)
    
    # Compute correlation
    r_value, _ = stats.pearsonr(data[param_4AB], data[param_3AB])
    
    # Set axis labels without subplot titles
    axes[row, col].set_xlabel(f'{simple_title} (4AB)', fontsize=12)
    axes[row, col].set_ylabel(f'{simple_title} (3AB)', fontsize=12)
    
    # Add the correlation coefficient to the plot
    axes[row, col].text(0.05, 0.9, f'r = {r_value:.2f}',
                        transform=axes[row, col].transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.5))
    
    # Remove grid lines
    axes[row, col].grid(False)

# Add a main title for the entire plot
fig.suptitle('Comparison of Model Parameters Between 4AB and 3AB Tasks', fontsize=16)

# Adjust layout to create much more space between the legend and the graphs
plt.tight_layout(rect=[0, 0, 0.7, 0.95])

# Add a legend in a separate space with the updated text
fig.legend([f'Individual subjects (n = {n_samples})'], loc='center right', fontsize=12, bbox_to_anchor=(1.5, 0.5))

# Display the plot
plt.show()
