import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the dataset from the file
data_path = 'path_to_your_file.csv'
data = pd.read_csv(data_path)

# Drop rows with any NA values in the relevant columns
cleaned_data = data.dropna(subset=["dars_score", "gad_score", "shaps_score", "zung_score"])

# Get the number of subjects
n_samples = cleaned_data.shape[0]

# Define short forms for questionnaire labels
questionnaire_short_names = {
    'dars_score': 'DARS',
    'gad_score': 'GAD',
    'shaps_score': 'SHAPS',
    'zung_score': 'ZUNG'
}

# Define pairs for balanced comparisons
pairs = [
    ('dars_score', 'gad_score'),
    ('dars_score', 'shaps_score'),
    ('dars_score', 'zung_score'),
    ('gad_score', 'shaps_score'),
    ('gad_score', 'zung_score'),
    ('shaps_score', 'zung_score')
]

# Create a figure with 2 columns and 3 rows
fig, axes = plt.subplots(3, 2, figsize=(15, 15))

# Flatten axes for easier indexing
axes = axes.flatten()

# Generate scatter plots for each pair
for idx, (x_var, y_var) in enumerate(pairs):
    sns.regplot(x=cleaned_data[x_var], y=cleaned_data[y_var], ax=axes[idx],
                scatter_kws={'s': 50, 'color': 'teal', 'alpha': 0.6}, 
                line_kws={"color": "salmon"}, marker='o', ci=95)
    
    # Compute correlation
    r_value, _ = stats.pearsonr(cleaned_data[x_var], cleaned_data[y_var])
    
    # Set axis labels with short forms
    axes[idx].set_xlabel(questionnaire_short_names[x_var], fontsize=12)
    axes[idx].set_ylabel(questionnaire_short_names[y_var], fontsize=12)
    
    # Add the correlation coefficient to the plot
    axes[idx].text(0.05, 0.9, f'r = {r_value:.2f}',
                   transform=axes[idx].transAxes, fontsize=12,
                   bbox=dict(facecolor='white', alpha=0.5))
    
    # Remove grid lines
    axes[idx].grid(False)

# Create a custom legend with the colored marker to match the scatter points
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='teal', markersize=10, label=f'Individual subjects (N = {n_samples})')]

# Add the custom legend outside the plot
fig.legend(handles=handles, loc='center right', fontsize=12, bbox_to_anchor=(1.5, 0.5))

# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.9, 1])

# Display the final plot
plt.show()
