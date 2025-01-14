# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the data files for Non-Anhedonic and Anhedonic
nonanhedonic_data = pd.read_csv('/mnt/data/nonanhedonic_modelparameters.csv')
simulated_nonanhedonic_data = pd.read_csv('/mnt/data/simulated_modelparameters.csv')
anhedonic_data = pd.read_csv('/mnt/data/anhedonic_modelparameters.csv')
anhedonic_simulated_data = pd.read_csv('/mnt/data/anhedonic_simulated_modelparameters.csv')

# Merge the datasets on 'subjID'
nonanhedonic_merged_data = pd.merge(nonanhedonic_data, simulated_nonanhedonic_data, on="subjID", suffixes=("_orig", "_sim"))
anhedonic_merged_data = pd.merge(anhedonic_data, anhedonic_simulated_data, on="subjID", suffixes=("_orig", "_sim"))

# Define the parameters and their full forms for axis labels
parameter_details = {
    "Arew": ("Reward Learning Rate", "Reward Learning Rate"),
    "Apun": ("Punishment Learning Rate", "Punishment Learning Rate"),
    "R": ("Reward Sensitivity", "Reward Sensitivity"),
    "P": ("Punishment Sensitivity", "Punishment Sensitivity")
}

# Function to create plots with trend line, SEM, and modified 'r' value label in a box, using variable marker colors
def plot_with_trendline_markers(data, parameter, ax, color):
    # Compute correlation
    correlation_test = stats.pearsonr(data[f"{parameter}_orig"], data[f"{parameter}_sim"])
    
    # Create plot with customized color markers
    sns.regplot(x=data[f"{parameter}_orig"], y=data[f"{parameter}_sim"], 
                ax=ax, scatter_kws={'alpha':0.7, 'color':color, 's':80, 'marker':'o'}, 
                line_kws={'color':'black'}, ci=95)
    
    # Annotate with correlation coefficient (lowercase 'r') in a box with black outline
    ax.text(0.05, 0.95, f"r = {correlation_test[0]:.2f}",
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, 
            bbox=dict(facecolor='white', edgecolor='black'), fontsize=12)
    
    # Set axis labels
    ax.set_xlabel(f"Original {parameter_details[parameter][0]}", fontsize=14)
    ax.set_ylabel(f"Simulated {parameter_details[parameter][1]}", fontsize=14)
    
    # Remove gridlines
    ax.grid(False)

# Plot for Non-Anhedonic Data (Turquoise)
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

for i, param in enumerate(parameter_details):
    ax = axes[i//2, i%2]
    plot_with_trendline_markers(nonanhedonic_merged_data, param, ax, 'turquoise')

plt.tight_layout()
plt.show()

# Plot for Anhedonic Data (Salmon)
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

for i, param in enumerate(parameter_details):
    ax = axes[i//2, i%2]
    plot_with_trendline_markers(anhedonic_merged_data, param, ax, 'salmon')

plt.tight_layout()
plt.show()

# Create a separate legend for the two groups with circular markers
fig, ax = plt.subplots(figsize=(6, 4))

# Create legend with circular markers
for color, label in zip(['turquoise', 'salmon'], ['Non-Anhedonic', 'Anhedonic']):
    ax.scatter([], [], c=color, alpha=0.7, s=80, label=label, marker='o', edgecolor=None)
    
ax.legend(title="Group", fontsize=12, title_fontsize=14)
ax.set_axis_off()  # Remove axis for the legend-only plot
plt.show()
